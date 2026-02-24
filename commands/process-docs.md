---
description: Extract intelligence from project documents
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [document type, filename, "scan", or "interactive"]
---

Process new or updated project documents. Extracts intelligence and merges it into the existing project data without overwriting what's already there.

**CRITICAL PROCESSING RULE — ONE DOCUMENT AT A TIME:**
This command processes documents **one at a time** by default. After processing each document, Claude MUST stop, report results to the user, and **use AskUserQuestion** to ask the user what to process next. Claude must NEVER chain multiple documents together in a single processing pass — this causes context overload and extraction loops.

Read the document-intelligence skill at `${CLAUDE_PLUGIN_ROOT}/skills/document-intelligence/SKILL.md` and the project-data skill at `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md` before proceeding. Also read `${CLAUDE_PLUGIN_ROOT}/skills/document-intelligence/references/extraction-rules.md` for type-specific extraction rules. After extraction is complete, read the doc-orchestrator agent at `${CLAUDE_PLUGIN_ROOT}/agents/doc-orchestrator.md` to validate extraction output and ensure data quality. If available, also read the `construction-takeoff` Cowork skill for extracting material quantities from plan sheets during document processing.

## Step 1: Load Existing Project Data

Search for `project-config.json` in the user's working directory. Check these locations in order:
1. `AI - Project Brain/project-config.json`
2. `project-config.json` in the working directory root

If not found, tell the user: "No project is set up yet. Run `/set-project` first to create your project, then come back to process documents."

If found, load it and check the `documents_loaded` array to see what's already been processed.

## Step 2: Identify What to Process

### Mode A: Specific file or type (`/process-docs ASI-003.pdf` or `/process-docs schedule`)

If `$ARGUMENTS` contains a filename:
- Locate that file in the mapped folders (using `folder_mapping` from config) and process it.
- If the file isn't found, tell the user: "I couldn't find [filename] in your project folders. Check the path or drag the file into this chat."

If `$ARGUMENTS` contains a document type (e.g., "schedule", "specs", "plans", "safety"):
- Look in the relevant mapped folder for that type
- If multiple files of that type exist, list them and **use AskUserQuestion** to ask the user which ONE to process

### Mode B: User uploads a file directly

If the user drags/drops or uploads a file into the chat:
- Process the uploaded file directly. No folder lookup needed.

### Mode C: No arguments (`/process-docs`)

If no arguments and no uploaded file:
- Tell the user: "What would you like me to process? You can:"
  - "Drag a file into this chat"
  - "Tell me a filename: `/process-docs ASI-003.pdf`"
  - "Tell me a document type: `/process-docs schedule`"
  - "Run `/process-docs scan` to see what's new in your folders"
  - "Run `/process-docs interactive` to walk through folders one at a time"

### Mode D: Scan (`/process-docs scan`)

Lightweight folder scan. Compares what's in the project folders against what's already been processed. Reports what's new, what's changed, and what's ready to process. Does NOT extract or process any documents — just looks and reports.

1. **Load folder_mapping and documents_loaded** from `project-config.json`
2. **Walk every mapped folder** — list all supported file types (`.pdf`, `.xlsx`, `.xls`, `.csv`, `.docx`, `.doc`). Record filename, full path, file size, and parent folder.
3. **Compare against documents_loaded**:
   - Not in documents_loaded -> **NEW**
   - Same filename and file size -> **UNCHANGED**
   - Same filename, different file size -> **UPDATED**
4. **Present scan report** grouped by status.

   If nothing's new: "All [X] documents are up to date. Your project intelligence is current."

   If no documents have been processed yet: list all files grouped by folder and recommend starting with specs and schedule.

This scan is read-only — safe to run as often as needed.

### Mode E: Interactive Folder Walk (`/process-docs interactive`)

**This is the recommended mode for initial project processing or reprocessing.** It walks through every mapped folder one at a time, presenting each folder's contents and asking the user whether to process it.

**Step E1: Scan all folders and build inventory**

Walk every folder in `folder_mapping`. For each folder, count files and identify document types. Build a folder inventory and present it to the user with a summary: "I found X files across Y folders. Let's go through them one folder at a time."

**Step E2: Process folder by folder using AskUserQuestion**

For each folder in the inventory, use **AskUserQuestion** to present the folder contents and ask the user what to do. Options:
- "Process this folder" — Process the file(s) in this folder one at a time
- "Skip this folder" — Move to the next folder
- "Process deeper (with visual analysis)" — Process with full graphical/visual extraction (for plan sheets)

**IMPORTANT:** If the folder contains multiple files, process them ONE AT A TIME within the folder. After each file, provide a brief status update. Only use AskUserQuestion between folders, not between individual files within the same folder (to avoid excessive prompting). However, if a single file is very large (>20 pages), you may split it into logical sections and process section by section.

**Step E3: Process the selected folder**

Process ONLY the files in the current folder. Follow Steps 3-8 below for each file.

**Step E4: Report results and ask for next folder**

After processing all files in the current folder, report what was extracted. Then use **AskUserQuestion** to present the NEXT folder. Continue until all folders have been offered.

**CRITICAL ANTI-LOOP RULE:** After processing each folder's files, Claude MUST:
1. Save all extracted data to the appropriate JSON files
2. Update `documents_loaded` in `project-config.json`
3. Report a concise summary of what was extracted
4. **STOP and wait for user input** via AskUserQuestion before moving to the next folder
5. NEVER process the next folder automatically — always ask first

### Duplicate Check

Before processing, check if the file is already in `documents_loaded`:
- If the same filename with the same file size exists: already processed — ask if user wants to re-extract
- If the same filename with a different file size exists: updated version — extract the changes

## Step 3: Classify and Extract (Single Document)

For the document being processed, run the **document-intelligence** skill's extraction pipeline:

### Pass 1: Metadata Extraction
Extract PDF metadata (creator application, title, dates, page count). Auto-classify the document type.

### Pass 2: Structural Text Analysis
Scan for structural patterns (sheet index, TOC, tables, headers) to confirm type and guide extraction.

### Pass 3: Targeted Content Extraction
Extract intelligence following the extraction rules for the identified document type.

### Pass 4: Visual / Graphical Analysis (Plan Sheets and Drawings ONLY)

**CRITICAL — This pass is REQUIRED for any PDF that contains construction drawings, plan sheets, details, sections, or schedules embedded as graphics (not text tables).**

For plan sheet PDFs, extract graphical intelligence that text extraction misses.

#### Pass 4A: Scale Calibration (MUST run FIRST)

**Scale calibration is REQUIRED before extracting ANY measurement data from a sheet.** Follow this priority order:

1. **Graphic Scale Bar** (highest priority — survives PDF resizing):
   - Scan bottom-right quadrant, title block area, and below each view
   - Look for: horizontal line + evenly-spaced ticks + increasing distance labels
   - Calculate `pixels_per_foot = bar_pixel_length / bar_real_world_feet`
   - Confidence: HIGH (0.95)

2. **Text Scale Notation** (secondary — assumes nominal sheet size):
   - Read from title block and view labels: `1/4" = 1'-0"`, `1/8" = 1'-0"`, etc.
   - Convert to pixels_per_foot using sheet DPI
   - Confidence: MEDIUM (0.80)
   - **WARNING**: Text scales are WRONG if PDF was resized. Always prefer graphic bar.

3. **Known-Dimension Calibration** (fallback — uses longest dimension string):
   - Find longest dimension, measure its line in pixels, calculate pixels_per_foot
   - Cross-check with a second dimension (must agree within ±10%)
   - Confidence: LOW (0.65)

4. **Multi-Scale Zone Mapping** — Map each view's scale independently (main plan, enlarged areas, details, sections all typically differ)

5. **Stretch Detection** — Compare horizontal vs vertical pixels_per_foot. If >3% difference, record both values and flag `"stretch_detected": true`

**If scale calibration fails**: Record failure, flag for manual review, continue text-only extraction. Do NOT extract measurements from uncalibrated sheets.

Store all scale data in `plans-spatial.json` under `scale_calibration` with per-sheet and per-zone entries. See `references/visual-extraction-reference.md` for the full Scale Calibration methodology.

#### Pass 4B: Visual Content Extraction

After scale is calibrated, extract remaining graphical intelligence:

**Method 1 — Claude Vision (Primary, always available):**
1. Convert PDF pages to images using `pdftoppm` or PyMuPDF:
   ```bash
   mkdir -p /tmp/sheet_images && pdftoppm -png -r 200 "document.pdf" /tmp/sheet_images/sheet
   ```
2. Use the **Read tool** to view each sheet image directly (Claude's native multimodal vision)
3. For each sheet, extract:
   - **Dimension strings and chains**: Read ALL dimension values. Group sub-dimensions along common lines into chains with their overall dimension. Verify sums (sub-dims should equal overall ±1"). Tag each with zone/view and calibrated pixels_per_foot. Store chains in `plans-spatial.json → dimensions.chains`, isolated dims in `dimensions.isolated`.
   - **Elevation markers**: On sections and elevations, read all level markers (T.O. WALL, FFE, T.O. FOOTING, etc.) with their elevation values. Store in `plans-spatial.json → elevation_markers`.
   - **Spot elevations**: On civil/site plans, read decimal elevation values (e.g., 856.50) with their position. Classify as existing vs. proposed. Store in `plans-spatial.json → site_grading.spot_elevations`.
   - **Detail callouts**: Section cut markers, detail references, elevation markers.
   - **Building sections**: On section sheets (A-300, S-300), extract floor-to-floor height, foundation depth, ridge height, roof slope, ceiling height, structural depth. Store in `plans-spatial.json → sections.building`.
   - **Wall sections**: On wall section sheets (A-300/A-400), extract wall type, fire rating, layer-by-layer assembly (material, thickness, position), total thickness, base/top conditions. Store in `plans-spatial.json → sections.wall`.
   - **Roof slopes**: Slope triangle symbols and text notations (4:12, 1/4"/FT, etc.). Store with building section data.
   - **Room labels and locations**: Room numbers with approximate grid locations.
   - **Door swing directions**: Which way doors open, pocket vs. swing.
   - **Equipment locations**: MEP equipment with approximate grid coordinates.
   - **RCP ceiling data**: On reflected ceiling plans (A-102, A-5xx), extract ceiling type per room (ACT/GWB/exposed), ceiling height zones, grid module, tile product, fixture positions/tags, soffit/bulkhead locations. Store in `plans-spatial.json → ceiling_data`.
   - **MEP equipment tags**: On M/P/E-series sheets, extract all equipment tags (RTU, AHU, EF, WH, LP, etc.) with type and position. Store in `plans-spatial.json → mep_systems.equipment`.
   - **Duct sizes**: On mechanical plans, read duct size labels (rectangular WxH, round diameter) with system type (supply/return/exhaust). Store in `plans-spatial.json → mep_systems.duct_sizes`.
   - **Pipe sizes**: On plumbing plans, read pipe size + system abbreviation labels (e.g., "2\" CW", "4\" SAN") with material if noted. Store in `plans-spatial.json → mep_systems.pipe_sizes`.
   - **Panel schedules**: On electrical plans, extract panel name, voltage, phase, breaker sizes, circuit descriptions. Store in `plans-spatial.json → mep_systems.electrical.panel_schedules`.
   - **Exterior elevation materials**: On elevation sheets (A-200), extract cladding material zones per building face (type, color/finish, manufacturer code, area coverage). Store in `plans-spatial.json → elevations.exterior[].materials`.
   - **Exterior elevation openings**: Window marks (W-xxx), door marks (D-xxx), storefront marks (SF-xxx) with sizes, sill/head heights, and positions on each face. Store in `plans-spatial.json → elevations.exterior[].openings`.
   - **Exterior elevation heights**: Grade-to-eave, grade-to-ridge, grade-to-parapet, floor-to-floor at exterior from elevation dimensioning. Store in `plans-spatial.json → elevations.exterior[].heights`.
   - **Accessibility routes**: On code/life-safety plans, extract accessible route paths, door clearances, corridor widths, turning radii. Store in `plans-spatial.json → accessibility_data.routes`.
   - **ADA restroom compliance**: Grab bar positions, clearance zones, fixture mounting heights, turning radius per ADA restroom. Store in `plans-spatial.json → accessibility_data.ada_restrooms`.
   - **Ramps and slopes**: Ramp locations, slope ratios, landing dimensions, handrail details. Store in `plans-spatial.json → accessibility_data.ramps`.
   - **Accessibility signage**: Room signage types (tactile/braille), mounting heights, locations. Store in `plans-spatial.json → accessibility_data.signage`.
   - **Accessible parking**: Van-accessible counts, access aisle widths, signage, route to entrance. Store in `plans-spatial.json → accessibility_data.parking`.
   - **Counter heights**: ADA counter segments, heights, knee clearance dimensions. Store in `plans-spatial.json → accessibility_data.counters`.
   - **Hatch pattern refinement**: Refine Pass 5 material zone classifications using hatch angle analysis (45° = steel, 45°+135° = concrete, dots = earth) and density measurement (lines/inch). Cross-reference sheet legends when present. Update `plans-spatial.json → material_zones[]` with refined types and confidence.
   - **Keynote bubbles**: Numbered circles/diamonds with leader lines on plan sheets. Extract keynote number and what element the leader points to. Store in `plans-spatial.json → keynotes.callouts`.
   - **Keynote schedule**: Keynote number → description mapping tables from notes zones. Extract spec section references within descriptions. Store in `plans-spatial.json → keynotes.schedule`.
   - **General notes (numbered)**: Extract numbered general notes from notes blocks with category classification (dimensions, materials, installation, code, coordination). Store in `plans-spatial.json → general_notes`.
   - **Spec references in notes**: CSI six-digit spec section references within keynotes and general notes. Link to spec reference index from Pass 8. Store with parent keynote/note entry.
   - **General notes**: Construction notes from the drawings.
   - **Title block data**: Sheet number, title, revision date, scale, drawn by.
   - **North arrow orientation**: Plan orientation.
4. Store all visual extractions with `"source": "claude_vision"` and `"confidence": "medium"`

**Method 2 — Python Visual Pipeline (Enhanced, when dependencies available):**
Check if `cv2`, `skimage`, `sklearn` are available. If yes, also run `visual_plan_analyzer.py` for automated line detection, symbol detection, material zone identification, and dimension extraction. Cross-check against Claude Vision results. Falls back to OpenCV + Tesseract if PaddleOCR is unavailable.

**Method 3 — Tesseract OCR Supplement (Always available):**
For sheets where Claude Vision can't read small text, use:
```bash
tesseract /tmp/sheet_images/sheet-01.png /tmp/sheet_01_ocr -l eng --psm 6
```

**Visual Extraction Priority:** Claude Vision (baseline) > Python pipeline (precise coordinates) > Tesseract (text supplement)

### Multi-Document Handling — DISABLED

**Do NOT process multiple documents in a single pass.** If the user provides multiple files, classify all of them first, then process them one at a time with user confirmation between each.

## Step 4: Merge Intelligence

Use the project-data skill's merge rules when integrating new intelligence into existing config:

| Data Type | Merge Strategy |
|---|---|
| Subcontractors | Add new, update existing (match on name), never delete |
| Milestones | Update dates, add new milestones, never delete |
| Spec sections | Add new sections, update requirements, never delete |
| Grid lines | Merge (add new grids), never replace |
| Schedule (full update) | Replace current dates/critical path, keep history |
| Contract dates | Replace with newer, log change in version history |
| Weather thresholds | Update per spec section, log changes |
| Testing requirements | Add new, update frequency/agency, never delete |
| Hold points | Add new, update existing, never delete |
| Tolerances | Update per material/system |
| Safety zones | Add new, update existing |
| Geotechnical | Replace with newer data |
| SWPPP BMPs | Add new, update existing locations |
| RFIs | Add new RFIs, update status for existing |
| Submittals | Add new submittals, update status, attach product specs |
| Vendors | Add new vendors, update contact/pricing info |
| Concrete mix designs | Add new mixes, update existing, never delete |
| PEMB data | Replace with newer manufacturer data, keep version history |
| Electrical equipment | Add new, update existing, never delete |
| Permits | Add new, update expiration dates, never delete |
| Civil/utility systems | Add new runs, update inverts/sizes, never delete |

### Version History
Log all changes to key data points in the `version_history` array with date, source, field, old_value, new_value, and reason.

### Conflict Resolution
- Newer document wins, log the change
- Older document: ask the user
- Unknown dates: present both values and ask

### Document-Specific Merge Notes

Follow the detailed merge notes for each document type: RFI logs, submittal logs, vendor quotes, submittal packages, revised schedules, ASIs, change orders, sub lists, meeting minutes, geotechnical reports, safety plans, and SWPPP documents.

### Cross-Referencing After Merge

After merging new data, run cross-checks for downstream impacts based on what was processed (ASIs vs procurement, RFIs vs submittals, schedule vs procurement, sub lists vs schedule, meeting minutes vs logs, spec updates vs plan values).

## Step 5: Build Cross-References and Quantities (Incremental)

After extraction, run the **quantitative-intelligence** skill workflow — but only for data affected by the newly processed document. Update sheet cross-reference index, rebuild affected assembly chains, recalculate affected quantities, and run cross-verification.

## Step 6: Save Updated Data Files

Write changes to ONLY the data files affected by this processing run. Always update `project-config.json` to add the processed file to `documents_loaded` with these fields:

```json
{
  "filename": "document.pdf",
  "type": "schedule",
  "discipline": null,
  "date_loaded": "2026-02-12",
  "file_size": "2.1 MB",
  "page_count": 8,
  "sections_extracted": [],
  "extraction_methods": ["text", "structural_analysis"],
  "visual_extraction": false,
  "scale_data_extracted": false,
  "scale_calibration_method": null,
  "scale_calibration_confidence": null,
  "stretch_detected": false,
  "uncalibrated_sheets": [],
  "data_files_updated": ["schedule.json"],
  "coverage_notes": "",
  "confidence": "high"
}
```

## Step 7: Regenerate Project Memory File

Regenerate `CLAUDE.md` with the latest intelligence including scale data summary.

## Step 8: Post-Extraction Agent Validation

After saving extracted data (Step 6) and before presenting results to the user, automatically invoke three agents in sequence to validate the extraction:

1. **doc-orchestrator** (read agent at `${CLAUDE_PLUGIN_ROOT}/agents/doc-orchestrator.md`):
   - Run pipeline validation checks (P1-P4: metadata, structure, content, visual)
   - Run field population checks (are downstream skills' PI fields populated?)
   - Run cross-file consistency checks
   - Report pass/fail summary with any issues found

2. **data-integrity-watchdog** (read agent at `${CLAUDE_PLUGIN_ROOT}/agents/data-integrity-watchdog.md`):
   - Run orphan detection on the updated files
   - Run cross-file conflict checks focused on files touched by this extraction
   - Report any new integrity issues introduced by the extraction

3. **conflict-detection-agent** (read agent at `${CLAUDE_PLUGIN_ROOT}/agents/conflict-detection-agent.md`):
   - Run cross-discipline conflict detection against the newly extracted data
   - Compare new data against existing data in other files (e.g., new spec values vs. existing plan data)
   - Report any conflicts found, classified by severity

Present the combined agent results as part of the extraction summary:
```
Extraction Complete — [document name]

Data extracted: [summary of what was added/updated]
Files updated: [list of JSON files modified]

Agent Validation:
  doc-orchestrator: [X checks passed, Y issues]
  data-integrity-watchdog: [X clean, Y warnings]
  conflict-detection: [X conflicts found (C critical, M major, N minor)]

[If conflicts found, show top 3 by severity]
```

## Step 9: Summarize and Checkpoint

**CRITICAL — This is the anti-loop checkpoint.**

After processing a single document (or folder in interactive mode):
1. Report what was extracted with the agent validation results from Step 8
2. **STOP processing**
3. **Use AskUserQuestion** with options: Process next, Reprocess deeper, Review conflicts, Done for now, Show what's left

**NEVER automatically continue to the next document.** Always stop and ask.
