#!/usr/bin/env python3
"""
DXF Entity Parser for Construction Civil Drawings

Parses DXF files produced by libredwg's dwg2dxf converter and extracts
structured construction data. Handles Civil 3D layer conventions and
entity relationships (INSERT+ATTRIB+SEQEND sequences).

Usage:
    python3 parse_dxf.py input.dxf output.json [--proximity-radius 15]

Output: JSON file with categorized entities organized by layer group.
"""

import json
import logging
import re
import sys
import math
from collections import defaultdict
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


# ── Civil 3D Proprietary Object Types ────────────────────────────────
# These entity types use undocumented Autodesk internal formats and
# cannot be decoded by libredwg or parsed from DXF output. See the
# "Civil 3D Proprietary Object Limitations" section in SKILL.md.

CIVIL3D_PROPRIETARY_TYPES = {
    'ACDBALIGNMENT', 'ACDBSURFACE', 'ACDBTINSURFACE', 'ACDBPIPENETWORK',
    'ACDBCORRIDOR', 'ACDBPARCEL', 'ACDBPROFILEVIEW', 'ACDBPRESSUREPIPE',
    'ACDBPROFILE', 'ACDBASSEMBLY', 'ACDBSUBASSEMBLY', 'ACDBFEATURELINE',
    'ACDBGRADING', 'ACDBINTERFERENCE', 'ACDBSAMPLELINE', 'ACDBSECTIONVIEW',
    'AABORNEENTITY', 'ABORNEENTITY',
}


# ── Layer Classification ──────────────────────────────────────────────

LAYER_CATEGORIES = {
    'storm':      [r'C-STRM', r'STORM', r'STM'],
    'sanitary':   [r'C-SSWR', r'SANITARY', r'SAN', r'SEWER'],
    'water':      [r'C-WATR', r'WATER', r'WTR'],
    'topography': [r'C-TOPO', r'TOPO', r'CONTOUR'],
    'property':   [r'C-PROP', r'PROPERTY', r'BNDY', r'BOUNDARY'],
    'road':       [r'C-ROAD', r'ROAD', r'PVMT', r'CURB'],
    'erosion':    [r'C-EROS', r'EROSION', r'EROS', r'KYN'],
    'building':   [r'C-BLDG', r'BLDG', r'BUILDING'],
    'site':       [r'C-SITE', r'SITE', r'GRADE', r'GRADING'],
    'survey':     [r'C-SV', r'SURVEY', r'PNT', r'COGO'],
    'annotation': [r'C-ANNO', r'ANNO', r'DIM', r'LABEL'],
    'existing':   [r'^V-', r'EXIST'],
}


def classify_layer(layer_name):
    """Classify a layer name into a category based on known patterns."""
    upper = layer_name.upper()
    for category, patterns in LAYER_CATEGORIES.items():
        for pattern in patterns:
            if re.search(pattern, upper):
                return category
    return 'other'


# ── DXF Line Reader ──────────────────────────────────────────────────

def read_dxf_pairs(filepath):
    """Read a DXF file and yield (group_code, value) pairs."""
    with open(filepath, 'r', errors='replace') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines) - 1:
        try:
            code = int(lines[i].strip())
        except ValueError:
            i += 1
            continue
        value = lines[i + 1].strip()
        yield code, value
        i += 2


def read_dxf_lines(filepath):
    """Read all lines from DXF file into a list for indexed access."""
    with open(filepath, 'r', errors='replace') as f:
        return f.readlines()


# ── Entity Parsers ────────────────────────────────────────────────────

def parse_entities_section(lines):
    """
    Parse the ENTITIES section of a DXF file.

    Returns a dict of entity lists organized by type:
    {
        'TEXT': [...], 'MTEXT': [...], 'LINE': [...],
        'LWPOLYLINE': [...], 'INSERT': [...], etc.
    }

    INSERT entities include their child ATTRIB entities grouped together.
    """
    entities = defaultdict(list)
    layers = set()
    skipped_proprietary = defaultdict(int)  # Track Civil 3D proprietary entity counts

    # Find ENTITIES section
    in_entities = False
    i = 0
    while i < len(lines) - 1:
        code = lines[i].strip()
        value = lines[i + 1].strip() if i + 1 < len(lines) else ''
        if code == '2' and value == 'ENTITIES':
            in_entities = True
            i += 2
            break
        i += 2

    if not in_entities:
        # Try finding entity type markers directly
        i = 0

    # State machine for parsing entities
    current_entity = None
    current_type = None
    current_insert = None
    current_attribs = []
    in_attrib_sequence = False

    while i < len(lines) - 1:
        try:
            code = int(lines[i].strip())
        except ValueError:
            i += 1
            continue
        value = lines[i + 1].strip()

        # End of ENTITIES section
        if code == 0 and value == 'ENDSEC':
            # Save any pending entity
            if current_type and current_entity:
                if current_type == 'INSERT' and in_attrib_sequence:
                    current_insert['attribs'] = current_attribs
                    entities['INSERT'].append(current_insert)
                else:
                    entities[current_type].append(current_entity)
            break

        # New entity starts
        if code == 0:
            # Save previous entity
            if current_type and current_entity and not in_attrib_sequence:
                entities[current_type].append(current_entity)
            elif current_type == 'INSERT' and not in_attrib_sequence and current_entity:
                # INSERT without ATTRIBs
                current_insert = current_entity
                current_insert['attribs'] = []
                entities['INSERT'].append(current_insert)

            if value == 'SEQEND':
                # End of INSERT+ATTRIB sequence
                # Save last ATTRIB if pending
                if current_type == 'ATTRIB' and current_entity:
                    current_attribs.append(current_entity)
                if in_attrib_sequence and current_insert:
                    current_insert['attribs'] = current_attribs
                    entities['INSERT'].append(current_insert)
                in_attrib_sequence = False
                current_insert = None
                current_attribs = []
                current_entity = None
                current_type = None
                i += 2
                continue

            elif value == 'ATTRIB':
                # Save previous ATTRIB if there was one
                if current_type == 'ATTRIB' and current_entity and in_attrib_sequence:
                    current_attribs.append(current_entity)
                if not in_attrib_sequence and current_type == 'INSERT':
                    # First ATTRIB after INSERT — start sequence
                    in_attrib_sequence = True
                    current_insert = current_entity
                    current_attribs = []
                current_entity = {'type': 'ATTRIB', 'layer': '', 'tag': '', 'text': '', 'x': 0, 'y': 0}
                current_type = 'ATTRIB'
                i += 2
                continue

            elif value in ('TEXT', 'MTEXT', 'LINE', 'LWPOLYLINE', 'ARC',
                           'CIRCLE', 'POINT', 'HATCH', 'INSERT', 'SPLINE',
                           'ELLIPSE', 'DIMENSION', 'LEADER', 'SOLID',
                           '3DFACE', 'VIEWPORT'):
                if in_attrib_sequence:
                    # Non-ATTRIB entity during sequence — close it
                    if current_insert:
                        current_insert['attribs'] = current_attribs
                        entities['INSERT'].append(current_insert)
                    in_attrib_sequence = False
                    current_insert = None
                    current_attribs = []

                current_type = value
                current_entity = {'type': value, 'layer': ''}

                if value == 'TEXT':
                    current_entity.update({'x': 0, 'y': 0, 'z': 0, 'text': '', 'height': 0, 'rotation': 0})
                elif value == 'MTEXT':
                    current_entity.update({'x': 0, 'y': 0, 'z': 0, 'text': '', 'height': 0, 'width': 0})
                elif value == 'LINE':
                    current_entity.update({'x1': 0, 'y1': 0, 'z1': 0, 'x2': 0, 'y2': 0, 'z2': 0})
                elif value == 'LWPOLYLINE':
                    current_entity.update({'vertices': [], 'closed': False, 'elevation': 0})
                elif value == 'ARC':
                    current_entity.update({'cx': 0, 'cy': 0, 'cz': 0, 'radius': 0, 'start_angle': 0, 'end_angle': 0})
                elif value == 'CIRCLE':
                    current_entity.update({'cx': 0, 'cy': 0, 'cz': 0, 'radius': 0})
                elif value == 'POINT':
                    current_entity.update({'x': 0, 'y': 0, 'z': 0})
                elif value == 'INSERT':
                    current_entity.update({'x': 0, 'y': 0, 'z': 0, 'block_name': '', 'scale_x': 1, 'scale_y': 1, 'rotation': 0})
                elif value == 'HATCH':
                    current_entity.update({'pattern': '', 'num_paths': 0})

                i += 2
                continue
            else:
                # Unknown entity type — check if it's a Civil 3D proprietary object
                normalized = value.upper().replace(' ', '')
                if normalized in CIVIL3D_PROPRIETARY_TYPES:
                    # Extract handle if available for diagnostic logging
                    handle_str = ''
                    peek = i + 2
                    while peek < len(lines) - 1 and peek < i + 20:
                        try:
                            peek_code = int(lines[peek].strip())
                        except ValueError:
                            peek += 1
                            continue
                        if peek_code == 5:  # DXF group code 5 = entity handle
                            handle_str = f" at handle 0x{lines[peek + 1].strip()}"
                            break
                        peek += 2
                    logger.warning(
                        "Skipped entity type '%s'%s (Civil 3D proprietary)",
                        value, handle_str
                    )
                    skipped_proprietary[value] += 1
                current_type = None
                current_entity = None
                i += 2
                continue

        # Parse entity attributes based on group codes
        if current_entity is None:
            i += 2
            continue

        try:
            if current_type == 'TEXT':
                if code == 8: current_entity['layer'] = value
                elif code == 10: current_entity['x'] = float(value)
                elif code == 20: current_entity['y'] = float(value)
                elif code == 30: current_entity['z'] = float(value)
                elif code == 1: current_entity['text'] = value
                elif code == 40: current_entity['height'] = float(value)
                elif code == 50: current_entity['rotation'] = float(value)

            elif current_type == 'MTEXT':
                if code == 8: current_entity['layer'] = value
                elif code == 10: current_entity['x'] = float(value)
                elif code == 20: current_entity['y'] = float(value)
                elif code == 30: current_entity['z'] = float(value)
                elif code == 1: current_entity['text'] = value
                elif code == 3: current_entity['text'] += value  # Continuation
                elif code == 40: current_entity['height'] = float(value)
                elif code == 41: current_entity['width'] = float(value)

            elif current_type == 'LINE':
                if code == 8: current_entity['layer'] = value
                elif code == 10: current_entity['x1'] = float(value)
                elif code == 20: current_entity['y1'] = float(value)
                elif code == 30: current_entity['z1'] = float(value)
                elif code == 11: current_entity['x2'] = float(value)
                elif code == 21: current_entity['y2'] = float(value)
                elif code == 31: current_entity['z2'] = float(value)

            elif current_type == 'LWPOLYLINE':
                if code == 8: current_entity['layer'] = value
                elif code == 10:
                    current_entity['vertices'].append({'x': float(value), 'y': 0})
                elif code == 20:
                    if current_entity['vertices']:
                        current_entity['vertices'][-1]['y'] = float(value)
                elif code == 38: current_entity['elevation'] = float(value)
                elif code == 70:
                    flags = int(value)
                    current_entity['closed'] = bool(flags & 1)

            elif current_type == 'ARC':
                if code == 8: current_entity['layer'] = value
                elif code == 10: current_entity['cx'] = float(value)
                elif code == 20: current_entity['cy'] = float(value)
                elif code == 30: current_entity['cz'] = float(value)
                elif code == 40: current_entity['radius'] = float(value)
                elif code == 50: current_entity['start_angle'] = float(value)
                elif code == 51: current_entity['end_angle'] = float(value)

            elif current_type == 'CIRCLE':
                if code == 8: current_entity['layer'] = value
                elif code == 10: current_entity['cx'] = float(value)
                elif code == 20: current_entity['cy'] = float(value)
                elif code == 30: current_entity['cz'] = float(value)
                elif code == 40: current_entity['radius'] = float(value)

            elif current_type == 'POINT':
                if code == 8: current_entity['layer'] = value
                elif code == 10: current_entity['x'] = float(value)
                elif code == 20: current_entity['y'] = float(value)
                elif code == 30: current_entity['z'] = float(value)

            elif current_type == 'INSERT':
                if code == 8: current_entity['layer'] = value
                elif code == 2: current_entity['block_name'] = value
                elif code == 10: current_entity['x'] = float(value)
                elif code == 20: current_entity['y'] = float(value)
                elif code == 30: current_entity['z'] = float(value)
                elif code == 41: current_entity['scale_x'] = float(value)
                elif code == 42: current_entity['scale_y'] = float(value)
                elif code == 50: current_entity['rotation'] = float(value)
                elif code == 66: current_entity['has_attribs'] = int(value)
                # XDATA: Civil 3D stores point numbers as extended data
                elif code == 1001:
                    current_entity.setdefault('xdata_app', [])
                    current_entity['xdata_app'].append(value)
                elif code == 1000:
                    current_entity.setdefault('xdata_values', [])
                    current_entity['xdata_values'].append(value)

            elif current_type == 'ATTRIB':
                if code == 8: current_entity['layer'] = value
                elif code == 2: current_entity['tag'] = value
                elif code == 1 and not current_entity.get('text'):
                    current_entity['text'] = value
                elif code == 10: current_entity['x'] = float(value)
                elif code == 20: current_entity['y'] = float(value)
                # When ATTRIB is fully parsed, add to attribs list
            if current_type == 'ATTRIB' and code == 0:
                # This won't trigger here — handled above at entity boundary
                pass

            elif current_type == 'HATCH':
                if code == 8: current_entity['layer'] = value
                elif code == 2: current_entity['pattern'] = value
                elif code == 91: current_entity['num_paths'] = int(value)

        except (ValueError, KeyError):
            pass

        if current_entity and code == 8:
            layers.add(value)

        i += 2

    # Report Civil 3D proprietary object summary
    if skipped_proprietary:
        total_skipped = sum(skipped_proprietary.values())
        total_parsed = sum(len(v) for v in entities.values())
        total_all = total_parsed + total_skipped
        skip_pct = (total_skipped / total_all * 100) if total_all > 0 else 0

        logger.warning(
            "Skipped %d Civil 3D proprietary entities (%d unique types, %.1f%% of total):",
            total_skipped, len(skipped_proprietary), skip_pct
        )
        for etype, count in sorted(skipped_proprietary.items(), key=lambda x: -x[1]):
            logger.warning("  %s: %d", etype, count)

        if skip_pct > 20:
            logger.warning(
                "ATTENTION: >20%% of entities are Civil 3D proprietary objects. "
                "Recommend requesting EXPORTTOAUTOCAD DXF from the design team "
                "for complete data extraction. See SKILL.md 'Civil 3D Proprietary "
                "Object Limitations' section for details."
            )

    return dict(entities), sorted(layers)


# ── Survey Point Extraction ──────────────────────────────────────────

def extract_survey_points(entities):
    """Extract survey points from INSERT+ATTRIB sequences on survey layers."""
    points = []
    inserts = entities.get('INSERT', [])

    for insert in inserts:
        layer = insert.get('layer', '').upper()
        # Check if this is a survey point layer
        if not any(pat in layer for pat in ['SV', 'PNT', 'COGO', 'SURVEY']):
            continue

        point = {
            'x': insert.get('x', 0),
            'y': insert.get('y', 0),
            'z': insert.get('z', 0),
            'layer': insert.get('layer', ''),
            'block': insert.get('block_name', ''),
            'point_number': None,
            'description': None,
        }

        # Extract point number from ATTRIBs
        for attrib in insert.get('attribs', []):
            tag = attrib.get('tag', '').upper()
            text = attrib.get('text', '')
            if 'PT' in tag or 'NUM' in tag or tag == 'PTNUMBER':
                point['point_number'] = text
            elif 'DESC' in tag or 'NOTE' in tag:
                point['description'] = text
            elif 'ELEV' in tag:
                point['description'] = text  # Elevation label

        # Also extract point number from XDATA (Civil 3D pattern)
        # Civil 3D stores PNTNO in extended data: 1001=PNTNO, 1000=<number>
        xdata_apps = insert.get('xdata_app', [])
        xdata_vals = insert.get('xdata_values', [])
        if not point['point_number'] and 'PNTNO' in xdata_apps:
            pntno_idx = xdata_apps.index('PNTNO')
            # The value follows the PNTNO app registration
            # XDATA pattern: 1001=PNTNO, 1000=<pt_number>, 1070=<flags>, 1000=<desc>
            if pntno_idx < len(xdata_vals):
                point['point_number'] = xdata_vals[pntno_idx]

        # Use Z as elevation
        point['elevation'] = point['z']
        points.append(point)

    return points


# ── Utility Structure Extraction ──────────────────────────────────────

def extract_utility_structures(entities, category_layers, proximity_radius=15):
    """
    Extract utility structures by grouping nearby TEXT annotations.

    Utility structures in CAD are represented as individual text entities
    placed near each other. This function groups them by proximity and
    parses elevation/pipe data from the text content.
    """
    # Collect TEXT entities on matching layers
    annotations = []
    for text_ent in entities.get('TEXT', []):
        layer_cat = classify_layer(text_ent.get('layer', ''))
        if layer_cat in category_layers:
            annotations.append({
                'x': text_ent.get('x', 0),
                'y': text_ent.get('y', 0),
                'text': text_ent.get('text', ''),
                'layer': text_ent.get('layer', ''),
                'category': layer_cat,
            })

    # Also check MTEXT
    for mtext_ent in entities.get('MTEXT', []):
        layer_cat = classify_layer(mtext_ent.get('layer', ''))
        if layer_cat in category_layers:
            # Clean MTEXT formatting codes
            text = re.sub(r'\\[A-Za-z][^;]*;', '', mtext_ent.get('text', ''))
            text = re.sub(r'[{}]', '', text)
            annotations.append({
                'x': mtext_ent.get('x', 0),
                'y': mtext_ent.get('y', 0),
                'text': text.strip(),
                'layer': mtext_ent.get('layer', ''),
                'category': layer_cat,
            })

    # Group by proximity
    structures = []
    used = set()

    for idx, ann in enumerate(annotations):
        if idx in used:
            continue
        group = [ann]
        used.add(idx)

        for jdx, other in enumerate(annotations):
            if jdx in used:
                continue
            dist = math.sqrt((ann['x'] - other['x'])**2 + (ann['y'] - other['y'])**2)
            if dist < proximity_radius:
                group.append(other)
                used.add(jdx)

        # Parse the group into a structure record
        structure = parse_structure_group(group)
        if structure:
            structures.append(structure)

    return structures


def parse_structure_group(group):
    """Parse a group of nearby text annotations into a structure record."""
    structure = {
        'x': sum(a['x'] for a in group) / len(group),
        'y': sum(a['y'] for a in group) / len(group),
        'texts': [a['text'] for a in group],
        'layers': list(set(a['layer'] for a in group)),
        'rim_elevation': None,
        'grate_elevation': None,
        'inverts': [],
        'pipe_sizes': [],
        'structure_type': None,
    }

    for ann in group:
        text = ann['text'].upper()

        # Rim elevation
        rim_match = re.search(r'RIM\s*[=:]\s*([\d.]+)', text)
        if rim_match:
            structure['rim_elevation'] = float(rim_match.group(1))

        # Grate elevation
        grate_match = re.search(r'GR(?:ATE)?\s*[=:]\s*([\d.]+)', text)
        if grate_match:
            structure['grate_elevation'] = float(grate_match.group(1))

        # Invert elevations with optional pipe size
        inv_matches = re.finditer(r'INV\s*[=:]\s*([\d.]+)(?:\s*\(?\s*(\d+)["\']?\s*\)?)?', text)
        for m in inv_matches:
            inv = {'elevation': float(m.group(1))}
            if m.group(2):
                inv['pipe_size'] = m.group(2) + '"'
            structure['inverts'].append(inv)

        # Pipe sizes standalone
        pipe_matches = re.finditer(r'(\d+)["\']?\s*(?:HDPE|PVC|RCP|CMP|DIP|STEEL|CLAY|CI)', text)
        for m in pipe_matches:
            structure['pipe_sizes'].append(m.group(0))

        # Structure type identification
        if 'MH' in text or 'MANHOLE' in text:
            structure['structure_type'] = 'manhole'
        elif 'CB' in text or 'CATCH' in text:
            structure['structure_type'] = 'catch_basin'
        elif 'JB' in text or 'JUNCTION' in text:
            structure['structure_type'] = 'junction_box'
        elif 'FH' in text or 'HYDRANT' in text:
            structure['structure_type'] = 'fire_hydrant'
        elif 'METER' in text:
            structure['structure_type'] = 'meter'
        elif 'INLET' in text:
            structure['structure_type'] = 'inlet'
        elif 'CO' in text or 'CLEANOUT' in text:
            structure['structure_type'] = 'cleanout'

    return structure


# ── Contour Extraction ────────────────────────────────────────────────

def extract_contours(entities):
    """Extract contour lines from LWPOLYLINE entities on topography layers."""
    contours = []
    for poly in entities.get('LWPOLYLINE', []):
        layer_cat = classify_layer(poly.get('layer', ''))
        if layer_cat == 'topography':
            contour = {
                'layer': poly.get('layer', ''),
                'elevation': poly.get('elevation', 0),
                'vertex_count': len(poly.get('vertices', [])),
                'closed': poly.get('closed', False),
            }
            contours.append(contour)
    return contours


# ── Property Data Extraction ──────────────────────────────────────────

def extract_property_data(entities):
    """Extract property boundaries, bearings, and ownership from property layers."""
    property_texts = []
    bearings = []
    owners = []
    plat_refs = []

    for text_ent in entities.get('TEXT', []) + entities.get('MTEXT', []):
        layer_cat = classify_layer(text_ent.get('layer', ''))
        if layer_cat != 'property':
            continue

        text = text_ent.get('text', '')
        clean_text = re.sub(r'\\[A-Za-z][^;]*;', '', text)
        clean_text = re.sub(r'[{}]', '', clean_text).strip()

        property_texts.append({
            'text': clean_text,
            'x': text_ent.get('x', 0),
            'y': text_ent.get('y', 0),
            'layer': text_ent.get('layer', ''),
        })

        # Bearing pattern: N/S dd°mm'ss" E/W
        bearing_match = re.search(r'[NS]\s*\d+[°]\s*\d+[\']\s*[\d.]+["]\s*[EW]', clean_text)
        if bearing_match:
            bearings.append(bearing_match.group(0))

        # Owner/deed pattern
        if 'DB' in clean_text.upper() and 'PG' in clean_text.upper():
            plat_refs.append(clean_text)

        # Acreage
        if 'ACRE' in clean_text.upper() or 'AC' in clean_text.upper():
            owners.append(clean_text)

    return {
        'texts': property_texts,
        'bearings': bearings,
        'plat_references': plat_refs,
        'acreage_notes': owners,
    }


# ── Erosion Control Keynotes ─────────────────────────────────────────

def extract_keynotes(entities):
    """Extract construction keynotes from MTEXT entities on keynote/erosion layers."""
    keynotes = []
    for mtext in entities.get('MTEXT', []):
        layer = mtext.get('layer', '').upper()
        if 'KYN' in layer or 'EROS' in layer or 'NOTE' in layer:
            text = mtext.get('text', '')
            # Clean MTEXT formatting
            text = re.sub(r'\\[A-Za-z][^;]*;', '', text)
            text = re.sub(r'[{}]', '', text).strip()
            if len(text) > 10:  # Skip very short annotations
                keynotes.append({
                    'text': text,
                    'layer': mtext.get('layer', ''),
                    'x': mtext.get('x', 0),
                    'y': mtext.get('y', 0),
                })
    return keynotes


# ── Grading / Spot Elevations ─────────────────────────────────────────

def extract_grading_data(entities):
    """Extract spot elevations and grading annotations from site/building layers."""
    spot_elevations = []
    grading_notes = []

    for text_ent in entities.get('TEXT', []):
        layer_cat = classify_layer(text_ent.get('layer', ''))
        if layer_cat not in ('site', 'building', 'grading'):
            continue

        text = text_ent.get('text', '').strip()

        # Spot elevation pattern: plain number like 741.55 or TW744.0
        elev_match = re.match(r'^(?:TW|BW|TC|BC|FL|FF|FS|HP|LP|PAD)?\s*([\d]{3}\.[\d]+)$', text)
        if elev_match:
            spot_elevations.append({
                'elevation': float(elev_match.group(1)),
                'prefix': text.replace(elev_match.group(1), '').strip(),
                'x': text_ent.get('x', 0),
                'y': text_ent.get('y', 0),
                'layer': text_ent.get('layer', ''),
            })
        elif len(text) > 5:
            grading_notes.append({
                'text': text,
                'x': text_ent.get('x', 0),
                'y': text_ent.get('y', 0),
                'layer': text_ent.get('layer', ''),
            })

    return {
        'spot_elevations': spot_elevations,
        'grading_notes': grading_notes,
    }


# ── Summary Statistics ────────────────────────────────────────────────

def compute_summary(entities, layers):
    """Compute summary statistics for the parsed DXF data."""
    entity_counts = {}
    for etype, elist in entities.items():
        entity_counts[etype] = len(elist)

    layer_counts = defaultdict(int)
    for etype, elist in entities.items():
        for ent in elist:
            layer = ent.get('layer', 'UNKNOWN')
            layer_counts[layer] += 1

    category_counts = defaultdict(int)
    for layer in layers:
        cat = classify_layer(layer)
        category_counts[cat] += 1

    return {
        'entity_counts': dict(entity_counts),
        'total_entities': sum(entity_counts.values()),
        'total_layers': len(layers),
        'layers_by_category': dict(category_counts),
    }


# ── Main ──────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 parse_dxf.py <input.dxf> <output.json> [--proximity-radius N]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    proximity_radius = 15
    if '--proximity-radius' in sys.argv:
        idx = sys.argv.index('--proximity-radius')
        if idx + 1 < len(sys.argv):
            proximity_radius = float(sys.argv[idx + 1])

    print(f"Parsing DXF: {input_path}")
    print(f"Proximity radius: {proximity_radius}")

    # Read and parse
    lines = read_dxf_lines(input_path)
    print(f"Read {len(lines)} lines from DXF file")

    entities, layers = parse_entities_section(lines)
    print(f"Found {len(layers)} layers")
    for etype, elist in sorted(entities.items(), key=lambda x: -len(x[1])):
        print(f"  {etype}: {len(elist)} entities")

    # Extract structured data
    print("\nExtracting survey points...")
    survey_points = extract_survey_points(entities)
    print(f"  Found {len(survey_points)} survey points")

    print("Extracting storm sewer structures...")
    storm_structures = extract_utility_structures(entities, ['storm'], proximity_radius)
    print(f"  Found {len(storm_structures)} storm structures")

    print("Extracting sanitary sewer structures...")
    sanitary_structures = extract_utility_structures(entities, ['sanitary'], proximity_radius)
    print(f"  Found {len(sanitary_structures)} sanitary structures")

    print("Extracting water features...")
    water_structures = extract_utility_structures(entities, ['water'], proximity_radius)
    print(f"  Found {len(water_structures)} water features")

    print("Extracting contours...")
    contours = extract_contours(entities)
    print(f"  Found {len(contours)} contour polylines")

    print("Extracting property data...")
    property_data = extract_property_data(entities)
    print(f"  Found {len(property_data['bearings'])} bearings, {len(property_data['plat_references'])} plat refs")

    print("Extracting erosion control keynotes...")
    keynotes = extract_keynotes(entities)
    print(f"  Found {len(keynotes)} keynotes")

    print("Extracting grading data...")
    grading = extract_grading_data(entities)
    print(f"  Found {len(grading['spot_elevations'])} spot elevations")

    # Compute summary
    summary = compute_summary(entities, layers)

    # Elevation statistics for survey points
    if survey_points:
        elevations = [p['elevation'] for p in survey_points if p['elevation'] != 0]
        if elevations:
            summary['elevation_range'] = {
                'min': min(elevations),
                'max': max(elevations),
                'mean': sum(elevations) / len(elevations),
                'unit': 'ft',
            }

    # Build output
    output = {
        'metadata': {
            'source_file': input_path,
            'extraction_date': datetime.now().isoformat(),
            'parser_version': '1.0.0',
            'proximity_radius': proximity_radius,
        },
        'summary': summary,
        'layers': layers,
        'survey_points': survey_points,
        'storm_sewer': {
            'structures': storm_structures,
            'count': len(storm_structures),
        },
        'sanitary_sewer': {
            'structures': sanitary_structures,
            'count': len(sanitary_structures),
        },
        'water': {
            'structures': water_structures,
            'count': len(water_structures),
        },
        'contours': {
            'polylines': len(contours),
            'total_vertices': sum(c['vertex_count'] for c in contours),
            'elevation_range': {
                'min': min((c['elevation'] for c in contours if c['elevation']), default=0),
                'max': max((c['elevation'] for c in contours if c['elevation']), default=0),
            } if contours else {},
        },
        'property': property_data,
        'erosion_control': {
            'keynotes': keynotes,
            'count': len(keynotes),
        },
        'grading': grading,
        'entity_type_counts': summary['entity_counts'],
    }

    # Write output
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nExtraction complete. Output saved to: {output_path}")
    print(f"Total entities: {summary['total_entities']}")
    print(f"Total layers: {summary['total_layers']}")

    return output


if __name__ == '__main__':
    main()
