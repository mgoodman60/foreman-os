---
description: Extract intelligence from AutoCAD DWG files
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [filename.dwg]
---

Process AutoCAD DWG files (.dwg) to extract survey points, utility structures, contours, property data, erosion control keynotes, and grading information. Converts DWG to DXF via libredwg, then parses all entity types into structured project data.

Read the dwg-extraction skill at `${CLAUDE_PLUGIN_ROOT}/skills/dwg-extraction/SKILL.md` and the project-data skill at `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md` before proceeding. After extraction is complete, read the doc-orchestrator agent at `${CLAUDE_PLUGIN_ROOT}/agents/doc-orchestrator.md` to validate extraction output and ensure data quality.

## Step 1: Locate the DWG File

If `$ARGUMENTS` contains a filename:
- Search for that file in the mapped project folders (using `folder_mapping` from `project-config.json`)
- Also check the uploads directory and working directory root

If no arguments:
- Search project folders for any `.dwg` files
- Present findings to the user and ask which to process

## Step 2: Compile libredwg (if needed)

Check if `/tmp/libredwg/dwg2dxf` exists. If not, run the compilation script:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/dwg-extraction/scripts/compile_libredwg.sh
```

This clones libredwg from GitHub and compiles the `dwg2dxf` binary using gcc. The binary is cached at `/tmp/libredwg/dwg2dxf` for the duration of the session.

## Step 3: Convert DWG → DXF

```bash
/tmp/libredwg/dwg2dxf -o /tmp/extracted_drawing.dxf "/path/to/file.dwg"
```

Verify the output file was created and has reasonable size. Warnings about unhandled Civil 3D objects (AcDbSurface, AcDbAlignment, etc.) are expected and can be ignored.

## Step 4: Parse DXF Entities

Run the bundled parser:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dwg-extraction/scripts/parse_dxf.py /tmp/extracted_drawing.dxf /tmp/dxf_extracted.json
```

Review the parser output summary for entity counts and extraction results.

## Step 5: Deep Analysis

After the automated parser runs, perform additional manual analysis on the DXF data:

1. **Survey Point Deduplication** — Remove duplicate points (same XYZ within 0.01 ft tolerance)
2. **Elevation Distribution** — Analyze elevation histogram to identify key grades (building pad, parking, road)
3. **Structure Cross-Reference** — Match DWG structures with RFI field measurements if available
4. **Utility Network Tracing** — Follow pipe runs from structure to structure using invert elevations
5. **Construction Note Extraction** — Parse MTEXT keynotes for subgrade requirements, erosion BMPs, pavement sections
6. **Property Data** — Extract bearings, owners, plat references, acreage from property layer annotations

## Step 6: Load Into Project Intelligence

Read existing `plans-spatial.json` from `AI - Project Brain/`. Merge the extracted DWG data sections:

- `dwg_survey_data` — Survey points with XYZ, elevation statistics, control points
- `dwg_storm_sewer` — Storm structures with rim/grate/invert elevations, pipe materials
- `dwg_sanitary_sewer` — Sanitary manholes with rim/inverts, pipe sizes, flow direction
- `dwg_water` — Water meters, hydrants, main sizes, field evidence notes
- `dwg_property` — Property boundaries, bearings, acreage, owners, plat references
- `dwg_other_utilities` — Gas, electric, telecom locations
- `dwg_erosion_control` — BMP keynotes, erosion control features
- `dwg_grading` — Spot elevations, building pad, terrain analysis, pavement sections
- `dwg_contours` — Contour line data with vertex counts and elevation ranges

Also update `project-config.json`:
- Add the DWG file to `documents_loaded` with extraction metadata
- Record which `data_sections_loaded` were populated

## Step 7: Summarize Results

Report:
- Total survey points extracted (with/without point numbers)
- Elevation range
- Utility structures found per system (storm, sanitary, water)
- Layer count and category breakdown
- Any cross-references with existing project data (e.g., RFI field measurements)
- Data sections loaded into plans-spatial.json
