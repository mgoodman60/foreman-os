---
name: dwg-extraction
description: >
  Extract construction intelligence from AutoCAD DWG files by compiling libredwg from source,
  converting DWG to DXF, and parsing all entity types (survey points, utility structures,
  contours, property boundaries, construction keynotes, grading data). Use this skill whenever
  the user uploads or references a .dwg file, mentions AutoCAD drawings, Civil 3D files,
  grading plans, site plans in DWG format, or wants to extract data from CAD files. Also
  triggers when processing project documents that include .dwg files, or when the user says
  "read the DWG", "extract from CAD", "parse the drawing file", "process the civil plans",
  "what's in the DWG", "survey points from the drawing", "utility data from CAD".
  This skill handles the entire pipeline from binary DWG to structured JSON data.
version: 1.0.0
---

# DWG File Extraction

Extract structured construction intelligence from AutoCAD DWG files (including Civil 3D).
DWG is a proprietary binary format that requires specialized tooling — this skill handles
the full pipeline from raw .dwg to structured project data.

## Pipeline Overview

The extraction happens in four stages:

1. **Compile libredwg** — Build the open-source DWG reader from source (cached after first run)
2. **Convert DWG → DXF** — Use the compiled `dwg2dxf` binary to produce a text-based DXF file
3. **Parse DXF entities** — Custom Python parser extracts all entity types with full attribute data
4. **Structure & store** — Organize extracted data into plans-spatial.json sections

The reason we compile from source rather than using a package manager is that libredwg is
not available as an apt package in most environments, and Python DXF libraries (like ezdxf)
often fail on Civil 3D DXF output due to malformed MATERIAL entries from proprietary objects.
The manual parser in this skill handles these edge cases gracefully.

## Stage 1: Compile libredwg

Check if the binary already exists first. If not, compile it.

```bash
# Check for cached binary
if [ -f /tmp/libredwg/dwg2dxf ]; then
    echo "dwg2dxf binary found, skipping compilation"
else
    # Clone and compile
    cd /tmp
    git clone --depth 1 https://github.com/LibreDWG/libredwg.git
    cd libredwg

    # Write the config.h that works (this was developed through trial and error
    # to handle missing autotools, cmake, and various header conflicts)
    cat > src/config.h << 'CONFIGEOF'
#define PACKAGE "libredwg"
#define PACKAGE_VERSION "0.13"
#define PACKAGE_STRING "libredwg 0.13"
#define LIBREDWG_SO_VERSION "0:13:0"
#define HAVE_STDINT_H 1
#define HAVE_STDLIB_H 1
#define HAVE_STRING_H 1
#define HAVE_STRINGS_H 1
#define HAVE_INTTYPES_H 1
#define HAVE_UNISTD_H 1
#define HAVE_CTYPE_H 1
#define HAVE_WCHAR_H 1
#define HAVE_WCTYPE_H 1
#define HAVE_MEMCHR 1
#define HAVE_MEMMEM 1
#define HAVE_SCANDIR 1
#define IS_RELEASE 1
#define PACKAGE_NAME "libredwg"
#define HAVE_SYS_STAT_H 1
CONFIGEOF

    # Compile library object files
    # Skip in_json.c (needs jsmn.h submodule) and out_geojson.c (additional errors)
    # These are not needed for DWG→DXF conversion
    gcc -c -I. -Iinclude -Isrc -DHAVE_CONFIG_H \
      src/bits.c src/common.c src/classes.c src/codepages.c \
      src/decode.c src/decode_r11.c src/decode_r2007.c \
      src/dwg.c src/dwg_api.c src/hash.c src/dynapi.c \
      src/dxfclasses.c src/out_dxf.c src/out_json.c \
      src/print.c src/free.c src/encode.c -w

    # Compile the dwg2dxf program
    gcc -c -I. -Iinclude -Isrc -DHAVE_CONFIG_H programs/dwg2dxf.c -w

    # Link everything together
    gcc -o dwg2dxf *.o -lm -w

    echo "Compilation complete: $(ls -la dwg2dxf)"
fi
```

**Troubleshooting**: If the libredwg repo structure has changed, the key files needed are:
- `src/*.c` — Core library (bits, common, classes, codepages, decode, decode_r11, decode_r2007, dwg, dwg_api, hash, dynapi, dxfclasses, out_dxf, out_json, print, free, encode)
- `programs/dwg2dxf.c` — The conversion program
- `include/` — Header files
- `src/config.h` — Must be created manually (see above)

## Stage 2: Convert DWG → DXF

```bash
/tmp/libredwg/dwg2dxf -o /tmp/output.dxf "/path/to/input.dwg"
```

Expect warnings about unhandled Civil 3D objects (AcDbSurface, AcDbAlignment, etc.) —
these are normal and don't affect the extraction of standard entities. The conversion
produces a text-based DXF that can be parsed line by line.

Check the output file exists and has reasonable size (should be several MB for a typical
civil site plan).

## Stage 3: Parse DXF Entities

Run the bundled parser script. It handles all the entity types commonly found in
construction civil drawings:

```bash
python3 /path/to/dwg-extraction/scripts/parse_dxf.py /tmp/output.dxf /tmp/dxf_extracted.json
```

The parser extracts these entity categories:

### Entity Types Extracted

| Entity | DXF Type | What It Contains |
|--------|----------|-----------------|
| Survey points | INSERT + ATTRIB + SEQEND | Point number, XYZ coordinates, layer classification |
| Text annotations | TEXT | Single-line labels (elevations, structure IDs, pipe sizes) |
| Multi-line text | MTEXT | Construction notes, keynotes, legends |
| Polylines | LWPOLYLINE | Contour lines, property boundaries, utility runs |
| Lines | LINE | Grid lines, dimensions, leaders |
| Arcs | ARC | Radius returns, curved features |
| Circles | CIRCLE | Manholes, cleanouts, utility symbols |
| Points | POINT | Control points, spot elevations |
| Hatches | HATCH | Paving areas, building footprints, material fills |
| Block inserts | INSERT | Symbols (manholes, valves, meters, trees, fixtures) |

### Layer Naming Convention (Civil 3D)

Civil 3D uses a hierarchical layer naming system. The parser categorizes entities by
layer prefix to organize the extraction:

| Layer Pattern | Category | Typical Content |
|--------------|----------|----------------|
| `C-STRM-*` | Storm sewer | Pipes, structures, inlets, catch basins |
| `C-SSWR-*` | Sanitary sewer | Manholes, pipe runs, cleanouts |
| `C-WATR-*` | Water | Mains, services, meters, hydrants |
| `C-TOPO-*` | Topography | Existing contours, spot elevations |
| `C-PROP-*` | Property | Boundaries, bearings, easements |
| `C-ROAD-*` | Roadway | Curbs, pavement, striping |
| `C-EROS-*` | Erosion control | Silt fence, inlet protection, BMPs |
| `C-BLDG-*` | Building | Footprint, FFE, setbacks |
| `C-SITE-*` | Site | Grading, paving, landscaping |
| `C-SV$*` | Survey | Survey points, control, benchmarks |
| `C-ANNO-*` | Annotation | Dimensions, labels, notes |
| `V-*` | Existing (visible) | Existing utilities, features |
| `0` / `Defpoints` | System | Default layer, definition points |

Layers not matching these patterns are still extracted and categorized as "other".

### Survey Point Extraction Detail

Survey points in Civil 3D are stored as INSERT entities on survey point layers
(typically containing `SV` or `PNT` in the layer name). Each INSERT has child ATTRIB
entities that carry the point number. The XYZ coordinates come from the INSERT's
insertion point (group codes 10/20/30).

The parser tracks the INSERT → ATTRIB → SEQEND sequence to properly group
attributes with their parent block. This is important because a naive entity-by-entity
parser would lose the parent-child relationship.

### Structure Proximity Grouping

Utility structures (manholes, catch basins, junction boxes) have their attributes
(rim elevation, invert elevations, pipe sizes) stored as separate TEXT entities
positioned near the structure symbol. The parser groups these using proximity analysis:

1. Collect all TEXT entities on utility layers
2. For each text, find all other texts within a configurable radius (default: 15 units in state plane feet)
3. Group nearby texts into structure records
4. Parse elevation patterns (e.g., "RIM=739.90'", "INV=736.62'(12\")")

This approach handles the fact that CAD drawings don't have a formal "structure object" —
they're composed of individual text entities placed visually near each other.

## Stage 4: Structure & Store

After parsing, organize the extracted data into sections for plans-spatial.json:

### Data Sections

| Section Key | Content | Source Entities |
|------------|---------|----------------|
| `dwg_survey_data` | All survey points with XYZ, elevation stats, control points | INSERT+ATTRIB on SV/PNT layers |
| `dwg_storm_sewer` | Storm structures with rim/grate/invert elevations, pipe data | TEXT on C-STRM layers, proximity grouped |
| `dwg_sanitary_sewer` | Sanitary manholes with rim/inverts, pipe sizes, flow direction | TEXT on C-SSWR layers, proximity grouped |
| `dwg_water` | Water meters, hydrants, main sizes | TEXT/INSERT on C-WATR layers |
| `dwg_property` | Property boundaries, bearings, acreage, owners, plat references | TEXT on C-PROP layers, LWPOLYLINE boundaries |
| `dwg_other_utilities` | Gas, electric, telecom, field evidence notes | TEXT on V-* and utility layers |
| `dwg_erosion_control` | BMP keynotes, erosion control features | MTEXT on C-EROS/KYN layers |
| `dwg_grading` | Spot elevations, building pad, terrain analysis, pavement sections | TEXT on C-SITE/C-BLDG layers |
| `dwg_contours` | Contour line data with vertex counts and elevation ranges | LWPOLYLINE on C-TOPO layers |

### Loading Into plans-spatial.json

Read the existing plans-spatial.json, merge the new `dwg_*` sections (overwriting
previous DWG data if re-processing), and write back. Include metadata:

```json
{
  "dwg_survey_data": {
    "source_file": "filename.dwg",
    "extraction_date": "2026-02-20",
    "coordinate_system": "Kentucky State Plane NAD83 (US Survey Feet)",
    "total_points": 598,
    "elevation_range": {"min": 736.41, "max": 750.20, "unit": "ft"},
    "points": [...]
  }
}
```

Also update project-config.json under `documents_loaded` to record the DWG extraction
with a reference to which data sections were populated.

## Integration with Other Skills

This skill feeds data to several other Foreman OS skills:

- **quantitative-intelligence**: DWG geometry is Priority 1 (exact) data source for quantity calculations
- **project-data**: All extracted sections follow the plans-spatial.json schema
- **document-intelligence**: DWG files detected during /process-docs should trigger this skill
- **construction-takeoff**: DWG survey points and contours provide ground-truth measurements

When invoked from /process-docs or /set-project, this skill runs automatically for any
.dwg files found in the project folder. The extracted data integrates seamlessly with
data from other document types (PDFs, specs, schedules).

## Civil 3D Proprietary Object Limitations

The DWG extraction pipeline uses libredwg (open-source) to convert DWG to DXF, then
`parse_dxf.py` to extract entities. libredwg cannot decode Autodesk Civil 3D proprietary
objects because they use undocumented internal formats.

### Affected Object Types

| Civil 3D Object | DWG Entity Type | What It Contains | Impact |
|-----------------|----------------|-----------------|--------|
| Alignments | `AcDbAlignment` | Road centerlines, curve data, stationing | Cannot extract road geometry or station values |
| Surfaces | `AcDbSurface` / `AcDbTinSurface` | Terrain models, contours, spot elevations | Cannot extract existing/proposed grade data |
| Pipe Networks | `AcDbPipeNetwork` | Storm/sanitary pipe routing, structures | Cannot extract pipe sizes, inverts, manholes from network objects |
| Corridors | `AcDbCorridor` | Road cross-sections, assemblies | Cannot extract road design details |
| Parcels | `AcDbParcel` | Property boundaries, lot lines | Cannot extract parcel data |
| Profile Views | `AcDbProfileView` | Vertical alignments, profile grades | Cannot extract profile/grade information |
| Pressure Pipes | `AcDbPressurePipe` | Water distribution networks | Cannot extract water system layout from network objects |

### What DOES Work

- Standard DXF entities (LINE, POLYLINE, CIRCLE, ARC, TEXT, MTEXT, INSERT, ATTRIB) are fully supported
- Civil 3D drawings typically contain BOTH proprietary objects AND standard entities (labels, annotations, hatches)
- Layer names, text labels, and attribute data from standard entities are extractable even in Civil 3D files
- Block insertions (manholes, valves, hydrants as blocks) work normally

### Workaround — Export to Clean DXF from AutoCAD

If the design team has AutoCAD Civil 3D, request a DXF export with these settings:
1. In Civil 3D, use `EXPORTTOAUTOCAD` command (not `SAVEAS DXF`)
2. This "explodes" Civil 3D objects into standard AutoCAD entities:
   - Alignments become polylines with station labels as text
   - Surfaces become 3D faces or contour polylines
   - Pipe networks become lines/circles with attribute data
3. The resulting DXF is fully parseable by `parse_dxf.py`

### Alternative: Request PDF + DXF Combo

- Ask the design team for both DXF (for spatial data) and PDF plans (for annotations/details)
- `document-intelligence` extracts text/tables from PDFs
- `dwg-extraction` extracts geometry from the DXF
- Utility reconciliation (Pattern 7 in cross-reference-patterns.md) merges both sources

### Detection

When `parse_dxf.py` encounters unknown entity types, it logs them as warnings:
```
WARNING: Skipped entity type 'AcDbAlignment' at handle 0x1A3 (Civil 3D proprietary)
WARNING: Skipped entity type 'AcDbTinSurface' at handle 0x2B7 (Civil 3D proprietary)
```
If >20% of entities in a file are skipped proprietary objects, flag for superintendent with
recommendation to request `EXPORTTOAUTOCAD` DXF from the design team.

## Limitations

- **Civil 3D proprietary objects**: See the detailed section above. In short, surfaces, alignments,
  corridors, and pipe networks stored as AcDb* objects are not decoded by libredwg. The skill
  extracts the standard DXF entities that Civil 3D writes alongside these objects, which typically
  contains all the annotation data (elevations, labels, keynotes). Use `EXPORTTOAUTOCAD` as a workaround.
- **3D solids**: Complex 3D geometry (ACIS solids, meshes) is catalogued but not deeply parsed.
- **External references (XREFs)**: The skill processes the host DWG only. If critical data is
  in XREFs, they need to be bound or provided as separate files.
- **Block definitions**: Standard blocks are extracted by name and insertion point. Custom
  block geometry (internal entities) is not recursively parsed.
- **Coordinate systems**: The skill preserves whatever coordinate system the DWG uses. For
  Kentucky projects, this is typically State Plane NAD83. No coordinate transformation is performed.
