# DWG Extraction Integration Guide

## Overview
The dwg-extraction skill converts binary AutoCAD DWG files into structured JSON data that feeds the broader Foreman OS intelligence pipeline. This reference describes the pipeline flow, when to use DWG extraction vs other methods, and the output schema.

## Pipeline Flow

```
DWG File (binary)
  ↓
compile_libredwg.sh — Builds the libredwg C library from GitHub source
  ↓                   (cached at /tmp/libredwg/dwg2dxf)
dwg2dxf — Converts DWG to DXF format (text-based CAD interchange)
  ↓
parse_dxf.py — Custom entity parser (handles Civil 3D XDATA,
  ↓             INSERT+ATTRIB sequences, proximity grouping)
Structured JSON — Entities organized by type, layer, and spatial relationships
  ↓
Consumed by: document-intelligence, quantitative-intelligence, plans-spatial.json
```

## When to Use DWG Extraction vs Document Intelligence

| Scenario | Use DWG Extraction | Use Document Intelligence |
|----------|-------------------|--------------------------|
| Native .dwg CAD file | ✓ | |
| PDF of construction plans | | ✓ (visual analysis) |
| Civil 3D site plans | ✓ (preserves XDATA) | |
| Scanned/image-based plans | | ✓ (OCR + visual) |
| Precise geometry needed | ✓ (exact coordinates) | |
| Quick visual reference | | ✓ (faster) |
| Survey point extraction | ✓ | |
| Spec/text document | | ✓ |

## Entity Types Extracted

The DXF parser extracts these entity types:

| Entity Type | DXF Code | Data Extracted | Use Case |
|-------------|----------|----------------|----------|
| LINE | LINE | Start/end coordinates, layer | Property boundaries, grid lines |
| ARC | ARC | Center, radius, angles, layer | Curved elements, utilities |
| CIRCLE | CIRCLE | Center, radius, layer | Manholes, catch basins, columns |
| TEXT/MTEXT | TEXT, MTEXT | Content, position, height, rotation | Labels, notes, dimensions |
| DIMENSION | DIMENSION | Measurement value, position | Distances, elevations |
| INSERT (Block) | INSERT | Block name, position, attributes | Utility structures, symbols, equipment |
| ATTRIB | ATTRIB | Tag, value (within INSERT) | Structured data on blocks (pipe size, rim elev) |
| HATCH | HATCH | Boundary, pattern | Area fills (concrete, gravel, etc.) |
| LWPOLYLINE | LWPOLYLINE | Vertex list, closed flag | Boundaries, contours, parcels |
| POLYLINE | POLYLINE | 2D/3D vertex list | Contour lines, utility runs |
| SPLINE | SPLINE | Control/fit points | Smooth curves |

## Civil 3D XDATA Handling

Civil 3D objects store extended entity data (XDATA) in application-specific groups. The parser handles:

- **Pipe Networks**: Pipe segments with diameter, material, invert elevations, slope. Structures (manholes, catch basins) with rim/invert elevations, size.
- **Surfaces**: TIN surface points with elevations (extracted from 3DFACE entities or XDATA references)
- **Alignments**: Horizontal alignment stations with northing/easting coordinates
- **Profiles**: Vertical profile data with station/elevation pairs
- **Parcels**: Property boundary polylines with area and label data

XDATA is identified by registered application names (e.g., "AeccDbPipe", "AeccDbStructure"). The parser checks for these patterns and extracts the structured data within.

## Output Schema

The extracted data is organized into a JSON structure compatible with plans-spatial.json:

```json
{
  "source_file": "site-plan.dwg",
  "extraction_date": "2026-02-21T10:00:00Z",
  "coordinate_system": "State Plane NAD83",
  "units": "feet",
  "layers": [
    {
      "name": "C-UTIL-SANITARY",
      "entity_count": 45,
      "entity_types": ["LINE", "INSERT", "TEXT"]
    }
  ],
  "entities": {
    "survey_points": [...],
    "utility_structures": [...],
    "contours": [...],
    "property_boundaries": [...],
    "construction_keynotes": [...],
    "pipe_networks": [...],
    "dimensions": [...]
  },
  "spatial_index": {
    "bounds": { "min_x": 0, "min_y": 0, "max_x": 1000, "max_y": 800 },
    "grid_cells": [...]
  }
}
```

## Integration with Other Skills

- **document-intelligence**: Receives DWG extraction JSON for cross-referencing with visually-extracted plan data. Can validate PDF-extracted data against CAD-precise data.
- **quantitative-intelligence**: Uses extracted dimensions, areas, and quantities for takeoff calculations. CAD data provides the most accurate measurements.
- **plans-spatial.json**: DWG-extracted grid lines, building areas, and spatial data merge into the master spatial intelligence file.
- **drawing-control**: Sheet metadata from title block INSERT/ATTRIB data feeds the drawing log.

## Error Handling

- **Corrupt DWG**: If dwg2dxf fails, log the error and suggest user re-export from AutoCAD
- **Missing XDATA**: If Civil 3D XDATA is not present, fall back to standard DXF entity parsing
- **Large files**: DWG files >100MB may take several minutes. Stream parsing to avoid memory issues
- **Unsupported versions**: libredwg supports DWG R13-R2024. Earlier versions may have limited support
