---
name: document-intelligence
description: >
  Comprehensive construction document intelligence extraction system. Use when processing ANY construction documents (plans, specs, schedules, contracts, geotech, safety, SWPPP, sub lists, RFIs, submittals) to extract field-actionable data for daily reports, project management, quality control, and procurement. Also generates the Project Intelligence Dashboard and construction schedules (door, hardware, fixture, finish, plumbing, equipment, room) from extracted data. Triggers: "process documents", "extract from plans", "read the specs", "analyze schedule", "set up project", "add documents", "show project intelligence", "project intel", "what data do we have", "door schedule", "hardware schedule", "finish schedule", "generate schedules", "room schedule", "equipment schedule", any mention of construction document processing or project intelligence building. This skill should be used EVERY TIME construction documents need to be processed - it extracts deep, comprehensive data including specific values, schedules, specifications, and coordination information that goes far beyond basic document reading.
version: 1.0.0
---

# Construction Document Intelligence

A comprehensive extraction system for construction project documents that captures deep, field-actionable intelligence for daily reports, project management, quality control, and procurement tracking.

## Overview

This skill transforms raw construction documents into structured, actionable project intelligence by:

1. **Classifying documents** automatically (plans, specs, schedules, contracts, etc.)
2. **Extracting comprehensive data** with specific numerical values, not just descriptions
3. **Cross-referencing** information across multiple documents
4. **Tracking extraction quality** with confidence levels and coverage metrics
5. **Structuring output** for downstream consumption by project management systems

**Key difference from basic document reading**: This skill extracts SPECIFIC VALUES and COMPLETE SCHEDULES rather than just summaries. For example:
- Not just "concrete requirements" → "4,000 PSI concrete, w/c ratio 0.45 max, slump 4\"±1\", air content 5.5%±1.5%, cure 7 days wet"
- Not just "room list" → Complete room schedule with ALL 50+ rooms, numbers, names, areas, departments
- Not just "schedule milestones" → Full critical path with durations, float, predecessors, constraints

## When to Use This Skill

**ALWAYS use this skill when**:
- Setting up a new project (/set-project, /process-docs, project initialization)
- Processing construction drawings (plans, elevations, sections, details)
- Processing specification books or spec sections
- Processing CPM schedules (P6, MS Project, Asta)
- Processing geotech reports, safety plans, SWPPP documents
- Processing contracts, subcontractor lists, RFI logs, submittal logs
- Updating project intelligence with new document revisions
- Any task involving "extract", "process", "read", "analyze" + construction documents

**Triggers include**:
- "Process these plans and extract grid lines, rooms, and finishes"
- "Read the spec book and get concrete requirements"
- "Analyze this schedule for critical path and milestones"
- "Extract subcontractor information from these contracts"
- "Process the geotech report for bearing capacity and compaction requirements"
- "What are the weather thresholds in the specs?"
- "Set up project intelligence from these documents"
- "Show me the project intelligence" / "project intel dashboard" / "what data do we have"
- "Show me the door schedule" / "generate schedules" / "hardware schedule" / "finish schedule"
- "What schedules have been extracted?" / "room schedule" / "equipment schedule"

---

## Core Capabilities

### 1. Three-Pass Extraction System

#### Pass 1: Metadata Extraction (Automatic)
Before reading content, extract PDF metadata:
- Creator application (signals document type)
- Creation/modification dates
- Page count
- Title, author, subject

#### Pass 2: Structural Analysis (Quick Scan)
Scan for structural patterns:
- Sheet index (for drawings)
- Table of contents (for specs)
- Headers, footers, tables
- Content signals for classification

#### Pass 3: Deep Content Extraction (Targeted)
Based on document type, extract comprehensive intelligence following specialized references.

#### Pass 4: Visual / Graphical Analysis (Plan Sheets and Drawings)

**This pass is REQUIRED for any PDF that contains construction drawings, plan sheets, details, sections, or schedules embedded as graphics.** Construction documents communicate ~80% of their information through drawings, not text. Skipping this pass means missing scale data, dimensions, room locations, door swings, equipment positions, and graphical notes.

**Method 1 — Claude Vision (Primary, always available in Cowork):**
1. Convert PDF pages to images: `pdftoppm -png -r 200 "document.pdf" /tmp/sheet_images/sheet` (or PyMuPDF)
2. Use the Read tool to view each sheet image directly (Claude's native multimodal vision)
3. Extract: scale data (per-view), dimension strings, detail callouts, room labels with grid locations, door swings, equipment locations, general notes, title block data, north arrow
4. Store with `"source": "claude_vision"` and `"confidence": "medium"`

**Method 2 — Python Visual Pipeline (Enhanced, when dependencies available):**
If `cv2`, `skimage`, `sklearn` are installed, also run `visual_plan_analyzer.py` for automated extraction:
- OCR text extraction (room labels, dimensions, notes, title block data)
- Wall/line detection and classification (walls, grids, dimension lines)
- Construction symbol recognition (doors, outlets, fixtures, markers)
- Material zone detection (hatches → concrete, VCT, tile, insulation)
- Dimension extraction (pairing OCR text with dimension lines)
- Scale calibration (graphic scale bars AND text-format scales)
Falls back to OpenCV + Tesseract if PaddleOCR is unavailable.

**Method 3 — Tesseract OCR (Always available):**
Supplement small text that Claude Vision misses: `tesseract sheet.png output -l eng --psm 6`

**Priority:** Claude Vision (baseline + validation) > Python pipeline (precise coordinates) > Tesseract (text supplement)

#### Pass 4A: Scale Calibration Protocol (REQUIRED before any measurement)

**Scale calibration MUST be completed before extracting dimensions, areas, or any measurement data from a sheet.** Without a calibrated scale, pixel-based measurements are meaningless. This sub-pass runs as the FIRST step of Pass 4 for every plan sheet.

**Step 1 — Graphic Scale Bar Detection (Highest Priority):**

Graphic scale bars are the most reliable scale anchor because they survive PDF resizing, printing at different sizes, and scanning. They are typically located near the title block or below individual views.

**What to look for:**
- A horizontal line with evenly-spaced tick marks (short perpendicular lines)
- Distance labels at ticks (e.g., "0", "4'", "8'", "16'" or "0", "5", "10", "20")
- Often has a subdivided first segment (finer ticks between 0 and the first major tick)
- May be labeled "GRAPHIC SCALE" or just have the unit label ("FEET", "INCHES")
- Common styles: open bar (ticks only), filled bar (alternating black/white segments), ladder bar (enclosed rectangles)

**Claude Vision detection method:**
1. Scan the bottom-right quadrant of each sheet first (most common location), then title block area, then below each view
2. Look for the characteristic pattern: horizontal line + evenly-spaced ticks + number labels increasing left-to-right
3. Record: bar pixel length (endpoint to endpoint), bar real-world length (from labels), tick count, unit
4. Calculate `pixels_per_foot = bar_pixel_length / bar_real_world_feet`

**Python pipeline detection method (Pass 7 enhanced):**
1. Detect candidate horizontal line segments 50-500px long
2. Find perpendicular tick marks (short lines within 5px of the candidate, 10-30px tall)
3. Require minimum 3 evenly-spaced ticks (spacing variance < 15%)
4. Match nearby OCR text to tick positions for distance labels
5. Calculate pixels_per_foot from tick spacing and label values

**Step 2 — Text Scale Notation (Secondary):**

Read text-format scale notations from title blocks and view labels:
- Architectural: `1/4" = 1'-0"`, `1/8" = 1'-0"`, `3/16" = 1'-0"`, `1/2" = 1'-0"`, `1" = 1'-0"`, `3" = 1'-0"`
- Metric: `1:50`, `1:100`, `1:200`
- Verbal: `SCALE: 1/4" = 1'-0"`, `PLAN SCALE: 1/8"`
- Per-view: Detail views often have their own scale different from the main plan

**IMPORTANT:** Text scales assume the sheet was printed or rendered at the nominal size (24×36", 30×42", etc.). If the PDF was resized during export or scanning, text scales will be WRONG. Always prefer graphic scale bar calibration when available.

**Step 3 — Multi-Scale Zone Mapping:**

Most plan sheets contain multiple views at different scales on the same sheet. Each view's scale must be mapped independently:
- **Main floor plan**: Typically 1/4" = 1'-0" or 1/8" = 1'-0"
- **Enlarged plans** (restrooms, kitchens, lobbies): Typically 1/2" = 1'-0"
- **Details**: Typically 1" = 1'-0", 1-1/2" = 1'-0", or 3" = 1'-0"
- **Site plans**: Typically 1" = 20'-0", 1" = 30'-0", or 1" = 50'-0"

For each view on a sheet, record:
```json
{
  "view_name": "FLOOR PLAN",
  "scale_text": "1/4\" = 1'-0\"",
  "pixels_per_foot": 62.5,
  "calibration_method": "graphic_bar",
  "zone_bbox": [120, 80, 2800, 3200],
  "confidence": "high"
}
```

**Step 4 — Known-Dimension Calibration Fallback:**

When neither graphic scale bar nor text scale is found (rare but possible on details, sections, or scanned documents):
1. Find the longest dimension string on the sheet (e.g., "132'-8\"" for an overall building dimension)
2. Measure its dimension line in pixels (endpoint to endpoint)
3. Calculate: `pixels_per_foot = pixel_length / dimension_feet`
4. Mark calibration as `"method": "known_dimension"`, `"confidence": "low"`
5. Cross-check: if ANY other dimension on the sheet can be measured and verified against this calibration, upgrade confidence to "medium"

**Step 5 — Double Calibration (Stretch Detection):**

Scanned documents and some PDF exports may have different horizontal and vertical scaling (stretched/skewed). After establishing scale:
1. Find a horizontal dimension and calculate `h_pixels_per_foot`
2. Find a vertical dimension and calculate `v_pixels_per_foot`
3. If they differ by more than 3%: the image is stretched
4. Record both values and set `"stretch_detected": true`
5. All subsequent area calculations must use the geometric mean: `pixels_per_foot = sqrt(h * v)`

**Scale Data Storage — REQUIRED:**

Every plan sheet must have scale data recorded in `plans-spatial.json` under `scale_calibration` with per-sheet and per-view scale information:

```json
"scale_calibration": {
  "sheets": {
    "A-101": {
      "sheet_name": "FLOOR PLAN",
      "calibration_method": "graphic_bar",
      "graphic_bar": {
        "pixel_length": 250,
        "real_world_feet": 16,
        "tick_count": 5,
        "location": [2400, 3600]
      },
      "text_scale": "1/4\" = 1'-0\"",
      "pixels_per_foot": {
        "horizontal": 62.5,
        "vertical": 62.3,
        "mean": 62.4
      },
      "stretch_detected": false,
      "zones": [
        {
          "view_name": "FLOOR PLAN",
          "scale_text": "1/4\" = 1'-0\"",
          "pixels_per_foot": 62.4,
          "zone_bbox": [120, 80, 2800, 3200],
          "confidence": "high"
        },
        {
          "view_name": "ENLARGED RESTROOM PLAN",
          "scale_text": "1/2\" = 1'-0\"",
          "pixels_per_foot": 124.8,
          "zone_bbox": [2850, 80, 3600, 1200],
          "confidence": "high"
        }
      ],
      "confidence": "high",
      "calibration_date": "2026-02-20"
    }
  }
}
```

**If scale calibration fails for a sheet** (no graphic bar, no text scale, no readable dimensions):
- Record `"calibration_method": "none"`, `"confidence": "failed"`
- Flag the sheet for manual review: "Sheet X-XXX: Scale calibration failed — superintendent should confirm scale"
- Do NOT attempt pixel-based measurements on uncalibrated sheets
- Text-based data (room names, door marks, notes) can still be extracted without scale

Without scale data, quantity calculations and dimensional verification are impossible. **A sheet with failed scale calibration is NOT fully processed** — flag it and move on.

#### Pass 4B: Dimension String Chaining and Verification

After scale calibration, extract and chain dimension strings. Dimension chains are the primary cross-check for measurement accuracy.

**What is a dimension chain?**
On construction drawings, dimensions are arranged in "strings" — a series of sub-dimensions along a common line that sum to an overall dimension. For example, column grid spacing (31'-4" + 29'-0" + 29'-0" + 29'-0" + 14'-4" = 132'-8"). If the sub-dimensions don't sum to the overall, there's either an extraction error or a drawing error worth flagging.

**Claude Vision extraction method:**
1. For each dimension string visible on the sheet, read ALL individual dimension values along the line
2. Identify the overall dimension (the one spanning the entire string, usually offset further from the drawing)
3. Sum the sub-dimensions and compare to the overall:
   - Match within ±1": chain verified ✓
   - Discrepancy > 1": flag for review — may indicate OCR misread or drawing error
4. Tag each dimension with its orientation (horizontal/vertical/angled)
5. Where possible, note what elements the dimension connects (e.g., "Grid 1 to Grid 2")

**Store dimension chains in `plans-spatial.json` under `dimensions.chains`:**
```json
{
  "chain_id": "DIM-CHAIN-001",
  "sheet": "A-100",
  "orientation": "horizontal",
  "overall_value": "132'-8\"",
  "overall_numeric_ft": 132.67,
  "segments": [
    {"value": "31'-4\"", "numeric_ft": 31.33, "from_element": "Grid 1", "to_element": "Grid 2"},
    {"value": "29'-0\"", "numeric_ft": 29.0, "from_element": "Grid 2", "to_element": "Grid 3"}
  ],
  "segments_sum_ft": 132.67,
  "sum_matches_overall": true,
  "discrepancy_ft": 0
}
```

Dimensions NOT part of any chain go into `dimensions.isolated`.

#### Pass 4C: Elevation Marker and Spot Elevation Extraction

**Elevation markers** appear on building sections, wall sections, and elevation views. They provide critical vertical measurement data.

**What to look for:**
- **Level markers**: Horizontal lines with text like "T.O. WALL 12'-0\"", "FFE 0'-0\"", "T.O. FOOTING -4'-0\""
- **Relative elevations**: Dimensions prefixed with +/- relative to FFE (Finished Floor Elevation)
- **Absolute elevations**: Text like "EL. 856'-6\"" referencing MSL (Mean Sea Level) datum

**Spot elevations** appear on civil/site plans as standalone numbers (e.g., "856.50") with an X or + marker:
- **Existing spot elevations**: Typically shown with parentheses or dashed text "(856.50)"
- **Proposed spot elevations**: Typically bold or standard text "856.50"
- **FFE**: Finished Floor Elevation, often boxed or highlighted
- **Top of curb (TC)**: Labeled "TC" or "T/C"

**Store elevation markers** in `plans-spatial.json` under `elevation_markers`:
```json
{
  "sheet": "A-300",
  "label": "T.O. WALL",
  "elevation": "12'-0\"",
  "elevation_ft": 12.0,
  "datum": "FFE = 0'-0\"",
  "marker_type": "level"
}
```

**Store spot elevations** in `plans-spatial.json` under `site_grading.spot_elevations`:
```json
{
  "sheet": "C-103",
  "elevation_ft": 856.50,
  "type": "proposed",
  "label": "856.50'"
}
```

#### Pass 4D: Cross-Sheet Reference Extraction

Cross-sheet references are the connective tissue of a plan set. Every section cut, detail callout, elevation marker, and schedule reference on one sheet points to a view on another sheet. Building this index is what enables assembly chains and multi-page calculations.

**What to extract:**

1. **Section Cut Markers** — Circle with number/letter + arrow indicating viewing direction. Format: `number / sheet_number` (e.g., "3/A-301" means "Section 3 is on sheet A-301").
   - Record: source sheet, marker location (grid reference), target sheet, section number, viewing direction

2. **Detail Callouts** — Circle or diamond with `detail_number / sheet_number`. Points to an enlarged detail view.
   - Record: source sheet, marker location, target sheet, detail number, what's being detailed (wall, footing, connection, etc.)

3. **Elevation Markers** — Circle with number/letter, NO arrow (unlike section cuts). References an exterior or interior elevation view.
   - Record: source sheet, target sheet, elevation number

4. **Enlarged Plan References** — Dashed rectangle on the main plan with label pointing to a larger-scale view on another sheet.
   - Record: source sheet, target sheet, boundary on source (approximate grid bounds)

5. **Schedule References** — Door marks (D101), window marks (W-3), room numbers, equipment tags that cross-reference to schedule sheets.
   - Record: mark/tag, plan sheet where it appears, schedule sheet it references

6. **Spec Section References** — Text like "SEE SECTION 03 30 00" or "PER SPEC 09 65 00" on drawings.
   - Record: source sheet, spec section number, context

**Store in `plans-spatial.json` under `sheet_cross_references`:**
```json
{
  "detail_callouts": [
    {
      "id": "XREF-001",
      "source_sheet": "A-100",
      "source_location": {"grid": "C-3", "zone": "plan_area"},
      "target_sheet": "A-501",
      "target_detail": "3",
      "callout_type": "section",
      "description": "Building section at Grid 3",
      "linked_elements": ["grid_3", "wall_type_2A"]
    }
  ]
}
```

**IMPORTANT**: Cross-reference extraction should happen on EVERY sheet, not just architectural. Structural sheets reference details, MEP sheets reference riser diagrams, civil sheets reference profile views. Build the index incrementally — each processed sheet adds its references to the master index.

**After processing all sheets in a document**, verify the index:
- Every target sheet referenced should exist in the drawing index
- Flag "orphan references" — callouts pointing to sheets not in the set (may indicate missing sheets)
- Flag "unreferenced sheets" — sheets in the index that no other sheet points to (may be standalone or may be missing callouts)

#### Pass 4E: Contour Line and Grading Extraction (Civil/Site Sheets)

**This pass applies ONLY to civil/site plan sheets** (C-series sheets, grading plans, site plans with contour lines). Skip for architectural, structural, MEP, and other disciplines.

Contour lines represent terrain elevations. The difference between existing and proposed contours at any point equals the cut or fill depth — critical for earthwork volume estimation.

**What to extract:**

1. **Contour Elevation Labels** — 3-4 digit numbers (e.g., 856, 857, 858) placed along curved lines. These are the elevation values for each contour.

2. **Existing Contours** (current terrain):
   - **Dashed lines** with elevation labels
   - Represent the ground as it exists before construction
   - Sometimes shown lighter or in a different color

3. **Proposed Contours** (design terrain):
   - **Solid lines** with elevation labels
   - Represent the finished grade after construction
   - Usually shown heavier/darker than existing

4. **Index Contours** — Every 5th or 10th contour is drawn thicker. Labels are always shown on index contours. Use index contour spacing to determine the contour interval (typically 1', 2', or 5').

5. **Drainage Patterns** — Water flows perpendicular to contours, from high elevation to low. V-shaped contour patterns pointing uphill indicate valleys/swales (drainage paths). Contours bowing away from buildings should confirm positive drainage.

6. **Cut/Fill Zones** — Where proposed contours are LOWER than existing = CUT (excavation). Where proposed contours are HIGHER than existing = FILL (import/compaction). Document the general cut/fill pattern for the site.

**Store in `plans-spatial.json` under `site_grading`:**
```json
{
  "contours": {
    "existing": [{"elevation_ft": 856.0, "line_style": "dashed", "sheet": "C-103"}],
    "proposed": [{"elevation_ft": 856.0, "line_style": "solid", "sheet": "C-103"}],
    "contour_interval_ft": 1.0
  },
  "cut_fill_volumes": {
    "net_operation": "cut",
    "avg_cut_depth_ft": 3.5,
    "max_cut_depth_ft": 6.0,
    "confidence": "low",
    "note": "Rough estimate — verify with earthwork quantity takeoff"
  },
  "drainage_patterns": [
    {"direction": "southeast", "high_elevation": 862, "low_elevation": 854, "fall_ft": 8}
  ]
}
```

**Cross-check with SWPPP**: The contour/grading data should be consistent with SWPPP disturbed area and cut/fill volumes. Flag if the grading plan shows significantly different earthwork than the SWPPP.

#### Pass 4F: Building Section and Wall Section Extraction (Section/Detail Sheets)

**This pass applies to architectural section sheets** (A-300 series), structural sections (S-300 series), wall section details (A-400/A-500 series), and any sheet containing building or wall section cuts. Skip for plan views, site plans, MEP plans, and reflected ceiling plans.

Building sections and wall sections are the primary source of vertical dimensioning, assembly composition, and structural depth data that cannot be obtained from plan views.

**What to extract:**

**1. Building Sections (full-height cross-sections through the building):**

- **Floor-to-floor height**: Distance from finished floor (FFE) to the next level or roof structure. For single-story buildings, this is the floor-to-roof structure distance.
- **Foundation depth**: Distance from finished grade to bottom of footing. Includes footing thickness, stem wall height, and any grade beam depth.
- **Ridge height**: Top of roof ridge above finished floor.
- **Eave/parapet height**: Top of exterior wall above finished floor.
- **Roof slope**: Read from slope triangle symbols (e.g., 4:12, 1/4":12") or calculate from rise/run dimensions.
- **Ceiling height**: Distance from FFE to bottom of ceiling system (ACT grid, GWB, exposed structure).
- **Structural depth**: Depth of roof joists, trusses, purlins, or beams visible in section.
- **SOG thickness**: Slab-on-grade thickness from section detail.
- **Cut location**: Which grid line and direction the section is cut through (from section marker on plan).

**2. Wall Sections (enlarged vertical cuts through wall assemblies):**

- **Wall type identifier**: Match to wall type legend (Type 1, Type 2, etc.) or wall schedule.
- **Total wall thickness**: Overall dimension from face to face.
- **Layer-by-layer assembly** (from exterior to interior):
  - Material name (e.g., "5/8\" Type X GWB", "3-5/8\" metal stud", "R-13 batt insulation")
  - Thickness of each layer
  - Position classification: exterior_finish, sheathing, air_barrier, insulation, stud_cavity, interior_finish
- **Fire rating**: If noted on section (e.g., "1-HR FIRE PARTITION")
- **Head/sill/jamb details**: Conditions at top of wall, window sill, and door jamb if shown
- **Base condition**: How wall meets floor (reveals, base trim, sealant joints)
- **Top condition**: How wall meets structure above (deflection track, fire safing, sealant)

**3. Section Identification:**

- **Section mark/number**: The label that identifies this section (e.g., "1/A-300")
- **Cut line reference**: Which sheet and location the section is cut from
- **Scale**: Section scale (typically 3/4"=1'-0" for building sections, 1-1/2"=1'-0" or 3"=1'-0" for wall sections)
- **Title**: Section title as shown below the drawing

**Store in `plans-spatial.json` under `sections`:**
```json
{
  "sections": {
    "building": [
      {
        "section_id": "SECT-A300-1",
        "sheet": "A-300",
        "section_mark": "1",
        "cut_line_on_sheet": "A-100",
        "cut_location": "Grid line 3, looking east",
        "scale": "3/4\" = 1'-0\"",
        "title": "Building Section - East/West",
        "floor_to_floor_ft": 14.5,
        "foundation_depth_ft": 4.0,
        "footing_thickness_in": 12,
        "stem_wall_height_ft": 2.0,
        "ridge_height_ft": 22.5,
        "eave_height_ft": 14.0,
        "parapet_height_ft": 0,
        "roof_slope": "4:12",
        "roof_slope_degrees": 18.43,
        "ceiling_height_ft": 10.0,
        "ceiling_type": "ACT",
        "structural_depth_in": 24,
        "structural_member": "PEMB rafter",
        "sog_thickness_in": 5,
        "measurements": [
          {"label": "FFE to T.O. Steel", "value_ft": 14.5, "confidence": "high"}
        ]
      }
    ],
    "wall": [
      {
        "section_id": "WSECT-A302-1",
        "sheet": "A-302",
        "section_mark": "1",
        "wall_type": "Type 4",
        "fire_rating": "1-HR",
        "total_thickness_in": 5.25,
        "layers": [
          {"material": "5/8\" Type X GWB", "thickness_in": 0.625, "position": "interior_finish"},
          {"material": "3-5/8\" 20ga metal stud @ 16\" OC", "thickness_in": 3.625, "position": "stud_cavity"},
          {"material": "R-13 batt insulation", "thickness_in": 3.5, "position": "insulation"},
          {"material": "5/8\" Type X GWB", "thickness_in": 0.625, "position": "interior_finish"}
        ],
        "base_condition": "Vinyl base on GWB, sealant at floor line",
        "top_condition": "Deflection track, fire safing above ceiling",
        "head_detail": null,
        "sill_detail": null,
        "measurements": [
          {"label": "Total assembly", "value_in": 5.25, "confidence": "high"}
        ]
      }
    ]
  }
}
```

**Cross-checks after section extraction:**
- **Wall types vs plan annotations**: Every wall type referenced on floor plans should have a corresponding wall section. Flag missing sections.
- **Ceiling heights vs RCP**: Section ceiling heights should match reflected ceiling plan height zones. Flag discrepancies > 2".
- **Foundation depth vs geotech**: Foundation embedment from sections should meet geotech minimum (e.g., 24" below grade for frost). Flag if shallower.
- **Roof slope vs structural**: Section roof slope should match structural framing slope. Flag if different.
- **Fire ratings vs plan partitions**: Wall section fire ratings should match fire-rated partition callouts on plans.

#### Pass 4G: Reflected Ceiling Plan (RCP) and MEP System Extraction

**This pass applies to RCP sheets** (A-102, A-5xx series, sheets titled "Reflected Ceiling Plan") **and MEP plan sheets** (M-series mechanical, P-series plumbing, E-series electrical). Skip for site plans, structural framing plans, and architectural floor plans (unless they contain MEP overlay data).

RCPs and MEP plans are the primary source for overhead-plane data (ceiling heights, fixture placement, HVAC devices) and system-level data (pipe sizes, duct sizes, panel schedules, equipment tags) that cannot be obtained from architectural floor plans or sections.

**What to extract:**

**1. Reflected Ceiling Plan Data:**

- **Ceiling type per room/zone**: ACT (acoustic ceiling tile), GWB (gypsum board), exposed structure, specialty (wood slat, metal panel, etc.)
- **Ceiling grid module**: 2'×2' or 2'×4' for ACT ceilings
- **Ceiling tile product**: Manufacturer and model from legend or notes (e.g., Armstrong Fine Fissured 1761)
- **Ceiling height zones**: Group rooms by ceiling height. Read height callouts (e.g., "9'-0\" AFF", "CLG @ 10'-0\"")
- **Height transitions**: Where ceiling height changes within or between rooms — soffits, bulkheads, stepped ceilings
- **Lighting fixture positions**: Symbol type + tag (e.g., 2×4 recessed troffer "A", 6" downlight "C") with room locations
- **HVAC devices on ceiling**: Supply diffusers, return grilles, exhaust grilles — tag and room
- **Sprinkler heads**: Approximate count per room (reference only — FP drawings govern)
- **Access panels**: Locations for above-ceiling MEP access

**Store in `plans-spatial.json` under `ceiling_data`:**
```json
{
  "ceiling_data": {
    "source_sheet": "A-102",
    "grid_type": "2x2",
    "grid_module": "24\" x 24\"",
    "tile_product": "Armstrong Fine Fissured Second Look 1761",
    "height_zones": [
      {"rooms": ["101", "102", "103"], "ceiling_height_ft": 9.0, "ceiling_type": "ACT"},
      {"rooms": ["104"], "ceiling_height_ft": 10.0, "ceiling_type": "GWB"}
    ],
    "fixture_positions": [
      {"tag": "A", "type": "2x4 recessed troffer", "rooms": ["101", "102"], "count": 12},
      {"tag": "C", "type": "6\" LED downlight", "rooms": ["103", "104"], "count": 8}
    ],
    "soffits_bulkheads": [
      {"room": "101", "description": "Soffit at perimeter, 8'-0\" AFF, 18\" wide"}
    ]
  }
}
```

**2. MEP System Data (Mechanical, Plumbing, Electrical):**

**Mechanical (M-series):**
- **Equipment tags and locations**: RTU, AHU, EF, VRF, ERV — tag, grid/room position, capacity (tons, CFM, MBH)
- **Duct sizes**: Supply, return, exhaust — read duct size labels (e.g., "12×8", "10\" RD") with system type
- **Diffuser/grille tags**: Cross-reference to RCP positions and mechanical schedule
- **Ductwork routing**: Major trunk runs with sizes, branches to rooms

**Plumbing (P-series):**
- **Pipe sizes**: Domestic cold/hot, sanitary, storm, gas, medical — read size labels (e.g., "2\" CW", "4\" SAN")
- **Pipe material**: As noted (copper, CPVC, PVC, cast iron, SS)
- **Fixture connections**: Which fixtures connect to which pipe runs
- **Equipment**: Water heaters, pumps, grease traps, backflow preventers — tag and location

**Electrical (E-series):**
- **Panel schedules**: Panel name, voltage, phase, main breaker, circuit list with loads
- **Single-line diagram data**: Service entrance size, transformer, main distribution, sub-panels
- **Circuit assignments**: Which circuits serve which rooms/equipment
- **Receptacle and device counts**: Per room counts of receptacles, switches, special outlets (GFCI, dedicated)
- **Equipment connections**: HVAC equipment electrical requirements (voltage, phase, MCA, MOCP)

**Store in `plans-spatial.json` under `mep_systems`:**
```json
{
  "mep_systems": {
    "electrical": {
      "source_sheets": ["E-100", "E-101", "E-200"],
      "panel_schedules": [
        {
          "panel": "LP-1",
          "location": "Electrical Room 110",
          "voltage": "208/120V",
          "phase": "3-phase",
          "main_breaker": "225A",
          "circuits": [
            {"circuit": 1, "description": "Lighting - Rooms 101-103", "breaker": "20A", "load_va": 1800}
          ]
        }
      ],
      "single_line_data": {
        "service_size": "400A",
        "voltage": "208/120V 3-phase",
        "transformer": "75 KVA"
      },
      "circuit_assignments": [
        {"room": "101", "circuits": [1, 3, 5], "description": "Lighting + receptacles"}
      ]
    },
    "pipe_sizes": [
      {"system": "domestic_cold", "size": "2\"", "material": "copper", "sheet": "P-100", "run_segments": []}
    ],
    "duct_sizes": [
      {"size": "12x8", "type": "supply", "sheet": "M-100", "run_segments": []}
    ],
    "equipment": [
      {
        "tag": "RTU-1",
        "type": "rooftop_unit",
        "sheet": "M-100",
        "position": {"grid": "C-3", "room": "Roof"},
        "schedule_data": {"cooling_tons": 10, "heating_mbh": 250, "cfm": 4000, "voltage": "208V/3ph"}
      }
    ]
  }
}
```

**Cross-checks after RCP + MEP extraction:**
- **RCP room numbers vs floor plan**: Every room on RCP must exist in the floor plan room schedule
- **Ceiling heights vs finish schedule**: RCP height zones should match finish schedule ceiling column
- **Fixture counts vs lighting schedule**: Sum of fixture tags on RCP should match schedule quantities
- **Diffuser counts vs mechanical schedule**: Supply/return diffuser count should support required CFM per room
- **Pipe sizes vs plumbing riser diagram**: Pipe sizes on plan should match riser diagram
- **Panel schedule loads vs connected equipment**: Equipment MCA should not exceed circuit breaker rating
- **Equipment tags on plan vs equipment schedules**: Every tag on plan must appear in corresponding schedule

See `references/plans-deep-extraction.md` (MEP Drawings section and Reflected Ceiling Plan section) for detailed extraction rules, symbol libraries, and cross-reference tables.

**MEP Extraction Depth Requirements:**

For EVERY MEP sheet processed, the extraction must achieve the following minimums:

| Discipline | Minimum Extraction |
|---|---|
| Mechanical | Every equipment tag + cooling tons + heating MBH + CFM + electrical (V/ph/MCA/MOCP) + served rooms |
| Electrical | Every panel schedule with ALL circuits, single-line diagram hierarchy, lighting fixture schedule with types/quantities/wattages |
| Plumbing | Every fixture from schedule with type/mounting/connections/ADA/flow rate, water heater specs, pipe sizes by system |
| Fire Protection | System type (wet/dry/pre-action), riser location, FDC, head schedule (type/temp/K-factor), fire pump if present |

**Do NOT stop at equipment tags only.** The extraction must capture schedule data (capacity, ratings, electrical requirements) from mechanical/electrical/plumbing schedule sheets (M-300, E-300, P-400 series).

**Reference**: See `references/mep-deep-extraction.md` for complete field-by-field extraction templates.

#### Pass 4G-2: MEP Schedule Sheets (M-300, E-300, P-400 Series)

**This pass is MANDATORY for any project with MEP drawings.** Schedule sheets contain the engineering data that equipment tags on plan sheets reference. Without schedule extraction, you only get tag names — not capacities, ratings, or specifications.

**Processing order:**
1. **M-300 series** (Mechanical Schedules): Extract EVERY row from HVAC equipment schedules, exhaust fan schedules, diffuser/grille schedules
2. **E-300 series** (Panel Schedules, Lighting Schedules): Extract EVERY panel with ALL circuits, EVERY lighting fixture type with quantities
3. **P-400 series** (Plumbing Schedules): Extract EVERY fixture from plumbing fixture schedule, water heater/boiler schedule
4. **FP sheets** (Fire Protection): Extract system type, riser diagram data, sprinkler head schedule

**Output depth per discipline** — see `references/mep-deep-extraction.md` for complete field lists.

**Validation**: After processing, verify:
- Every equipment tag on plan sheets has a matching schedule entry
- Panel schedule connected load ≤ main breaker rating
- Total CFM from diffusers ≤ equipment total CFM
- Every occupied room has lighting fixtures assigned

#### Pass 4H: Exterior Elevation and Accessibility Extraction

**This pass applies to exterior elevation sheets** (A-200 series) **and architectural floor plans** with accessibility annotations. Skip for sections, MEP plans, and civil/site sheets (except site accessibility routes).

Exterior elevations provide the vertical face of the building — material zones, window/door positions, grade line, and overall proportions. Accessibility data is typically annotated on floor plans and site plans as required routes, clearances, and signage.

**What to extract:**

**1. Exterior Elevation Data (A-200 series):**

- **Elevation face**: North, South, East, West (from title or orientation)
- **Material zones**: Each distinct cladding area with material type, color/finish, and approximate coverage area
  - Primary cladding (metal panels, CMU, brick, etc.)
  - Accent materials (stone veneer, brick banding, decorative panels)
  - Foundation/base visible material
  - Trim/fascia material and color
- **Window and door positions**: Mark numbers with their vertical positions on the elevation. Cross-reference to window/door schedules.
- **Grade line elevation**: The finished grade line with elevation value if noted
- **Overall building dimensions**: Height measurements (grade to eave, grade to ridge, floor-to-floor if multi-story)
- **Roof material and slope**: Visible from elevation — material type, color, slope direction
- **Canopy/entry features**: Portico structure, canopy material, entry surround
- **Signage locations**: Where building signage is indicated

**Store in `plans-spatial.json` under `elevations.exterior`:**
```json
{
  "elevations": {
    "exterior": [
      {
        "face": "South",
        "sheet": "A-200",
        "materials": [
          {"zone": "primary_cladding", "material": "Vertical metal panels", "color": "Champagne tan", "mfg_code": "Nucor 12-45"},
          {"zone": "base", "material": "Split-face CMU", "color": "Warm gray", "height_ft": 4.0},
          {"zone": "trim", "material": "Aluminum", "color": "Dark bronze anodized"}
        ],
        "grade_line_elevation_ft": 856.0,
        "window_positions": [
          {"mark": "W-101", "sill_height_ft": 3.0, "head_height_ft": 7.0}
        ],
        "door_positions": [
          {"mark": "101", "type": "storefront entry", "width_ft": 6.0, "height_ft": 7.0}
        ],
        "measurements": [
          {"label": "Grade to eave", "value_ft": 14.0},
          {"label": "Grade to ridge", "value_ft": 22.5}
        ]
      }
    ]
  }
}
```

**2. Accessibility Data (Floor Plans + Site Plans):**

- **Accessible routes**: Paths of travel from parking/entrance to all public spaces. Note route width (min 36" clear, 44" in corridors) and any obstructions.
- **ADA restroom clearances**: 60" turning radius, 18" centerline to side wall at WC, lavatory clearance (min 30"×48" clear floor space), grab bar locations (42" side, 36" rear).
- **Door clearances**: Maneuvering clearances at accessible doors (pull side: 18" beside latch, push side: 12"). Door hardware type (lever vs knob — lever required for accessible).
- **Ramp data**: Slope (max 1:12 = 8.33%), width (min 36"), landing size (60"×60" at top/bottom/turns), handrail heights (34"-38").
- **Signage locations**: Tactile/Braille signage at room doors, exit signs, directional signs. Mounting height (48"-60" AFF, latch side).
- **Parking accessibility**: Accessible stalls (8' wide + 5' access aisle), van accessible (8' + 8' aisle), signage, slope (max 2%).
- **Counter heights**: ADA service counter (max 36" AFF), transaction counter (max 34"), knee clearance (min 27" high, 30" wide, 19" deep).

**Store in `plans-spatial.json` under `accessibility_data`:**
```json
{
  "accessibility_data": {
    "accessible_routes": [
      {
        "from": "Accessible parking",
        "to": "Main entrance",
        "route_width_in": 60,
        "surface": "Concrete sidewalk",
        "slope_pct": 2.0,
        "compliant": true
      }
    ],
    "ada_restrooms": [
      {
        "room": "109",
        "turning_radius_in": 60,
        "wc_centerline_in": 18,
        "grab_bars": true,
        "lavatory_clearance": true,
        "door_width_in": 36,
        "compliant": true
      }
    ],
    "ramps": [
      {"location": "Main entry", "slope": "1:12", "width_in": 44, "handrails": true, "landings": true}
    ],
    "signage_locations": [
      {"type": "tactile_braille", "location": "All room doors", "mounting_height_in": 60, "side": "latch"}
    ],
    "accessible_parking": {
      "standard_count": 2,
      "van_accessible_count": 1,
      "signage": true,
      "access_aisle_width_ft": 5
    },
    "counter_heights": [
      {"location": "Reception 101", "height_in": 34, "type": "transaction", "knee_clearance": true}
    ]
  }
}
```

**Cross-checks after elevation + accessibility extraction:**
- **Material zones vs spec sections**: Elevation materials should match Div 07 (thermal/moisture), Div 04 (masonry), Div 05 (metals) specifications
- **Window/door positions vs schedules**: Every mark on elevation should exist in the door/window schedule
- **Grade elevation vs civil/site**: Elevation grade line should match site grading plan at the building perimeter
- **ADA route widths vs code**: 36" min passage, 44" min corridor, 60" turning. Flag violations.
- **Restroom clearances vs code**: 60" turning radius, 18" WC centerline. Flag non-compliant rooms.
- **Ramp slopes vs code**: Max 1:12 (8.33%). Flag steeper ramps.
- **Parking count vs code**: Verify accessible stall count meets IBC Table 1106.1 minimums for total parking count.

See `references/plans-deep-extraction.md` (Exterior Elevations section) for detailed rendering data extraction rules and material zone formatting.

#### Pass 4I: Hatch Pattern Refinement and Keynote Extraction

**This pass applies to ALL architectural and structural plan sheets** that contain hatched regions or keynote/general note annotations. It is a refinement pass that improves existing Pass 5 material zone data and adds keynote intelligence that no prior pass extracts.

**Why this pass exists:** Pass 5 uses raw Gabor texture analysis to classify hatched regions, but construction hatching follows AIA/ANSI standards with specific patterns mapped to specific materials. This pass overlays standard-pattern matching on top of Pass 5 results to improve classification accuracy. It also extracts keynote bubbles and general note schedules — critical text-based intelligence that links numbered callouts on drawings to their full descriptions.

**What to extract:**

**Hatch Refinement (improves Pass 5 material_zones):**

For each material zone already detected by Pass 5, refine the classification:
- **Hatch direction analysis**: Measure the dominant line angle(s) within each zone — single diagonal (45°) = steel/section cut (ANSI31), double diagonal (45°+135°) = concrete (AR-CONC), dots/stipple = earth, wavy lines = insulation, closely-spaced parallel lines = wood (end-grain vs. with-grain)
- **Hatch density measurement**: Lines per inch within the zone — distinguishes similar patterns (dense = concrete, sparse = earth fill)
- **Legend cross-reference**: If the sheet contains a material legend/key, match each zone's visual pattern to the legend entries and use the legend label as the authoritative material type
- **Section-cut vs plan-view hatch**: In section views, hatching represents cut material. In plan views, hatching represents surface finish or material below. Tag each zone with `"context": "section_cut"` or `"context": "plan_view"` based on the sheet type detected in Pass 10/12
- **Adjacent label matching**: If a leader line or text label is within 50px of a hatch zone boundary, associate that label with the zone as `material_label`
- **Hatch spacing measurement**: Measure the inter-line spacing in pixels and convert using scale calibration to actual spacing (validates pattern identity)

Store refined zones by UPDATING existing entries in `plans-spatial.json → material_zones[]`:
```json
{
  "zone_id": "MATZ-001",
  "sheet": "A-301",
  "material_type": "concrete",
  "hatch_pattern": "AR-CONC",
  "hatch_angle_deg": [45, 135],
  "hatch_spacing_in": 0.125,
  "hatch_density_lpi": 8.0,
  "context": "section_cut",
  "material_label": "4000 PSI CONC",
  "legend_match": true,
  "area_sf": 12.5,
  "bbox": [120, 340, 280, 520],
  "confidence": "high"
}
```

**Keynote Extraction:**

Keynotes are numbered callouts on drawings that reference a keynote schedule (either on the same sheet or on a general notes sheet). They are the primary way architects communicate specification-level information on plan sheets.

- **Keynote bubbles**: Detect numbered circles/diamonds/hexagons with leader lines pointing to drawing elements. Extract the keynote number and the x,y position of the leader endpoint (what it points to)
- **Keynote schedule**: Find the keynote schedule table on the sheet (or referenced sheet). Extract each keynote number → description mapping
- **General notes**: Extract numbered general notes from notes blocks (identified in Pass 1 zone detection). Each note typically starts with a number or letter (1., 2., A., B.)
- **Note-to-element linking**: For each keynote bubble on the drawing, record what element it points to (wall, door, detail, etc.) based on leader endpoint proximity to other detected elements
- **Specification references in notes**: Extract spec section references within notes (e.g., "per Section 03 30 00", "see Spec 07 92 00") and link to the spec reference index

Store keynotes in `plans-spatial.json → keynotes`:
```json
{
  "keynotes": {
    "schedule": [
      {
        "number": "1",
        "description": "PROVIDE 5/8\" TYPE X GWB ON RATED SIDE OF PARTITION",
        "spec_section": "09 29 00",
        "sheet_source": "A-001"
      }
    ],
    "callouts": [
      {
        "keynote_number": "1",
        "sheet": "A-101",
        "position": [1240, 890],
        "points_to": {"element_type": "wall", "element_id": "Type 2 partition"},
        "leader_endpoint": [1180, 870]
      }
    ]
  },
  "general_notes": [
    {
      "sheet": "A-001",
      "note_number": "1",
      "text": "ALL DIMENSIONS ARE TO FACE OF STUD UNLESS OTHERWISE NOTED",
      "spec_refs": [],
      "category": "dimensions"
    }
  ]
}
```

**Cross-checks after hatch refinement + keynote extraction:**
- **Hatch vs legend**: Every hatch zone with a legend on the sheet should have `legend_match: true`. Zones without legend matches get `confidence: "medium"` at best
- **Keynote completeness**: Every keynote bubble number on the drawing should have a matching entry in the keynote schedule. Missing = flag as incomplete
- **General notes vs spec sections**: Spec section references in notes should exist in the spec reference index (from Pass 8). Missing = flag for review
- **Hatch zone coverage**: On section sheets, hatched regions should cover most of the cut material area. Large unhatched cut areas = possible missed zones
- **Keynote density check**: Sheets with many keynotes but no schedule reference = schedule may be on another sheet. Flag for multi-sheet linking
- **Material consistency**: Hatch classification should be consistent across sheets — same material hatched the same way. Flag conflicting classifications for the same material across different sheets

See `references/visual-extraction-reference.md` (Pass 13 methodology section) for hatch angle measurement algorithms, keynote bubble detection, and standard pattern classification tables.

Merge visual results with text-based extraction. Visual data fills gaps where PDF text extraction misses graphical content. See `references/visual-extraction-reference.md` for accuracy expectations and integration rules.

### 2. Modular Specialized References

This skill uses domain-specific extraction guides. **Read the appropriate reference(s) before extracting**:

| Reference | When to Use | Contains |
|-----------|-------------|----------|
| **[construction-document-conventions.md](references/construction-document-conventions.md)** | **Always read first** — before any extraction | How drawings are organized, sheet numbering navigation, cross-reference system, scale/measurement, quantity calculation formulas, contour/grading, line types, hatch patterns, abbreviations |
| **[extraction-rules.md](references/extraction-rules.md)** | Read second | Framework, classification, principles |
| **[plans-deep-extraction.md](references/plans-deep-extraction.md)** | Processing plans/drawings | Complete room/finish/door/window schedules, MEP equipment, structural specs |
| **[specifications-deep-extraction.md](references/specifications-deep-extraction.md)** | Processing specs | All CSI divisions with exact values, weather thresholds, testing frequencies |
| **[schedule-deep-extraction.md](references/schedule-deep-extraction.md)** | Processing CPM schedules | Activity details, sequencing logic, float, critical path, constraints |
| **[civil-deep-extraction.md](references/civil-deep-extraction.md)** | Processing civil/site drawings | Storm/sanitary/water systems with pipe sizes and elevations |
| **[compliance-deep-extraction.md](references/compliance-deep-extraction.md)** | Processing geotech, safety, SWPPP | Bearing capacity, compaction, BMPs, inspection requirements |
| **[project-docs-deep-extraction.md](references/project-docs-deep-extraction.md)** | Processing contracts, sub lists, RFIs, subcontracts, POs | Contract terms, sub contacts, RFI status, submittal tracking, SC scope/exclusions, PO line items |
| **[pemb-deep-extraction.md](references/pemb-deep-extraction.md)** | Processing PEMB manufacturer documents | Column reactions, anchor bolts, framing, erection sequence, panels, accessories |
| **[submittals-deep-extraction.md](references/submittals-deep-extraction.md)** | Processing submittal packages | Concrete mixes, door hardware, shop drawings, MEP equipment, finishes |
| **[dxf-extraction.md](references/dxf-extraction.md)** | Processing .dxf/.dwg CAD files | Layer mapping, block attributes, hatch areas, polyline geometry, dimensions, parse_dxf.py |
| **[visual-extraction-reference.md](references/visual-extraction-reference.md)** | Processing plan sheet images (PDF→PNG) | OCR text extraction, line/wall detection, symbol recognition, material zones, dimensions, scale calibration |
| **[masterformat-reference.md](references/masterformat-reference.md)** | Enriching reports, QA checks, morning briefs | CSI Div 01-33: sequencing, QC issues, hold points, testing, weather limits, PEMB + healthcare overlays |
| **[mep-deep-extraction.md](references/mep-deep-extraction.md)** | Processing MEP plan sheets | Complete HVAC/plumbing/electrical equipment, panel schedules, fixture schedules, pipe/duct sizes, fire protection |

---

## Workflow

### For Single Document

1. **Read base extraction rules**:
   ```
   Read references/extraction-rules.md
   ```

2. **Classify the document** (Pass 1 + 2):
   - Check PDF metadata (creator application)
   - Scan for structural patterns
   - Identify document type

3. **Read appropriate specialized reference(s)**:
   ```
   # If plans/drawings:
   Read references/plans-deep-extraction.md

   # If specifications:
   Read references/specifications-deep-extraction.md

   # If schedule:
   Read references/schedule-deep-extraction.md

   # etc.
   ```

4. **Extract comprehensively** following the reference guide

5. **Track extraction quality** and structure output

### For Multiple Documents

**CRITICAL: Process ONE document at a time.** Do NOT batch-process multiple documents in a single pass — this causes context overload and extraction loops. Instead:

1. **Read base rules**: `references/extraction-rules.md`

2. **Classify all documents** first (Pass 1 + 2 for each) — this is a lightweight scan, not full extraction

3. **Present classification** to user for confirmation

4. **Use AskUserQuestion** to let the user choose which document to process first

5. **Recommended processing order** (earlier provides context for later):
   - Plans/drawings FIRST (establishes spatial framework)
     - For plan sheet PDFs: MUST run visual analysis (Pass 4) for scale data and graphical intelligence
   - DXF/DWG files FIRST-A (exact spatial data takes priority over PDF estimates)
   - Specifications SECOND (adds material/quality details)
   - Schedule THIRD (adds time dimension)
   - Contract FOURTH (adds constraints)
   - Sub list FIFTH (adds personnel)
   - Support docs LAST (RFIs, submittals, minutes)

6. **After each document: STOP, report results, ask user what to process next**

7. **Cross-reference** data across documents incrementally as each new document is processed

8. **Report results** after each document with metrics

---

## Extraction Depth Guidance

### Extract DEEP (100% completeness)

**Plans**:
- Grid lines (ALWAYS - critical for spatial reference)
- ALL room numbers and names
- ALL doors in door schedule
- ALL equipment in MEP schedules
- Structural general notes with EXACT VALUES (PSI, rebar sizes, embedments)

**Specifications**:
- Weather thresholds with NUMBERS (40°F, 90°F, 25 mph)
- Testing frequencies with NUMBERS ("1 set per 50 CY")
- Hold points vs. witness points (clearly distinguished)
- Tolerances with LIMITS (FF 35/FL 25, ±1/4")

**Schedule**:
- ALL milestones with dates
- Critical path activities (float = 0)
- Activity durations, dates, predecessors for critical/near-critical

### Extract BROAD (key items only)

- Meeting minutes (action items, decisions only)
- Correspondence (directives, not entire threads)
- Historical RFIs (closed items, not deep detail)

---

## Integration with Downstream Systems

### Daily Reports
- Auto-complete location references
- Spell subcontractor names correctly
- Track room-by-room progress
- Flag weather threshold conflicts

### Project Management
- Phase completion percentages
- Schedule health monitoring
- Procurement status tracking
- Resource loading analysis

### Quality Control
- Test result verification
- Tolerance acceptance
- Hold point tracking
- Inspection frequency compliance

### Procurement
- Equipment lead times
- Submittal approval status
- Long-lead item tracking
- Critical path dependencies

### Quantitative Intelligence
After extraction, the **quantitative-intelligence** skill uses extracted data + sheet cross-references to:
- Build assembly chains linking elements across multiple sheets
- Calculate derived quantities (concrete CY, flooring SF, fixture counts)
- Merge DXF, visual, takeoff, and text sources with priority rules
- Flag discrepancies when sources disagree by >10%
- Store quantities in `plans-spatial.json` and sheet references in the respective data files for use by reports, briefs, and dashboards

---

## Success Metrics

A successful extraction includes:
- **Completeness**: 100% of critical items extracted
- **Specificity**: Numerical values extracted, not just "per spec"
- **Structure**: JSON output ready for consumption
- **Quality tracking**: Coverage and confidence metrics
- **Cross-references**: Related data linked across documents
- **User validation**: Conflicts and low-confidence items flagged

---

## Project Intelligence Dashboard

When the user asks to see extracted project data ("show me the project intelligence", "project intel dashboard", "what data do we have"), generate a comprehensive Project Intelligence Dashboard:

1. Load the project data files from the user's working directory (`project-config.json`, `plans-spatial.json`, `specs-quality.json`, `schedule.json`, `directory.json`, and all log files)
2. If not found: "No project intelligence found. Run /set-project first to extract data from your construction documents."
3. Generate a single self-contained HTML file with:
   - **Sidebar navigation** with sections for: Overview, Documents Loaded, Grid Lines, Building Areas, Room Schedule (searchable), Site Layout, Spec Sections (searchable/filterable by CSI division), Key Materials, Weather Thresholds, Hold Points & Inspections, Construction Tolerances, Schedule, Contract Intelligence, Subcontractor Directory (searchable), Safety Intelligence, SWPPP & Erosion Control, Geotechnical Data, RFI Log, Submittal Log, Procurement & Materials, Vendor Database, Quantities (by CSI division, with source attribution), Sheet Cross-References (drawing index, detail callouts, assembly chains), Discrepancies (unresolved quantity variances)
   - **Data embedding**: Embed the entire config as a JavaScript object (fully self-contained)
   - **Color palette**: Navy #1B2A4A (headers), Blue #2E5EAA (accents), Light gray #F8F9FB (background), Light blue #EDF2F9 (sections), Amber #E8A838 (warnings), Green #2D8F4E (success), Red #C0392B (danger)
   - **Features**: Search and filter, status badges, sidebar count badges, coverage checklist, responsive layout
4. Save as `{PROJECT_CODE}_Project_Intelligence.html` in the user's output folder


---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
