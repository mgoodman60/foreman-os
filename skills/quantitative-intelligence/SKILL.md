---
name: quantitative-intelligence
description: >
  Bridge between all measurement sources (DXF geometry, visual plan analysis, construction takeoff, text extraction) and the project intelligence data store. Builds a complete sheet cross-reference index mapping every detail callout, section cut, schedule reference, and spec reference across the entire plan set. Calculates derived quantities (concrete volumes, room areas, material totals, fixture counts) by pulling data from multiple sheets through assembly chains. Stores quantities with source attribution and flags discrepancies when sources disagree by >10%. Triggers: "how much concrete", "total flooring", "room areas", "material quantities", "what quantities", "how many outlets", "cubic yards", "square footage", "takeoff to project", "cross-reference sheets", "assembly chain", "which sheets reference", "detail callout index", "multi-sheet calculation", "aggregate quantities", "quantity discrepancy".
version: 1.0.0
---

# Quantitative Intelligence

## Overview

A calculation bridge that connects all measurement sources to the project intelligence data store, with a complete cross-sheet reference index enabling multi-page calculations and spatial correlations.

## What This Skill Does

1. **Builds a Sheet Cross-Reference Index** — Maps every detail callout, section cut, schedule reference, and spec reference across the entire plan set so Claude knows how sheets connect
2. **Creates Assembly Chains** — Links related elements across multiple sheets (e.g., footing plan view → section detail → structural notes → concrete spec) into calculation chains
3. **Calculates Derived Quantities** — Computes volumes, areas, lengths, and counts by pulling dimensions from multiple sheets through assembly chains
4. **Merges Multiple Data Sources** — Combines DXF geometry (exact), visual analysis (approximate), takeoff measurements (calibrated), and text extraction (parsed) with clear priority rules
5. **Flags Discrepancies** — When sources disagree by >10%, flags for superintendent review
6. **Stores in Project Intelligence** — All quantities go into `plans-spatial.json` with source attribution for downstream use by reports, dashboards, and briefs

## Data Source Priority

When the same measurement exists from multiple sources, use the highest-priority source and note others as validation:

| Priority | Source | Accuracy | When Available |
|----------|--------|----------|----------------|
| 1 (highest) | DXF geometry | Exact coordinates | .dxf files processed through Phase 6 parse_dxf.py |
| 2 | Visual analysis | ±5-10% | Plan sheet images processed through Phase 7 visual_plan_analyzer.py |
| 3 | Takeoff measurement | ±2-5% (calibrated) | Scale-calibrated measurements from construction-takeoff skill |
| 4 (lowest) | Text extraction | Varies | Values parsed from PDF text, notes, schedules |

**Discrepancy Rule**: When any two sources disagree by >10%, flag for review. The superintendent resolves discrepancies — Claude does not auto-resolve.

## Integration with construction-takeoff Cowork Skill

For plan-based quantity extraction, the `construction-takeoff` Cowork skill provides an alternative or complementary workflow. When a takeoff is performed using that skill, its calibrated measurements feed directly into the Data Source Priority system at Priority Level 3. If the construction-takeoff skill detects quantities that differ from DXF or visual analysis results by >10%, it triggers the discrepancy flag for superintendent review. This integration enables both tools to work together: quantitative-intelligence for cross-sheet assembly chains and derived calculations, and construction-takeoff for focused material-by-material measurement and cost rollups.

### Construction-Takeoff Integration

The cowork platform's `construction-takeoff` skill provides quantity takeoff data as a **Priority 3** source (after plan extraction and manual override).

**Data flow:**
```
construction-takeoff (cowork skill)
  → takeoff results (area, linear, count, volume by element)
    → quantitative-intelligence cross-verification
      → plans-spatial.json quantities (if validated)
```

**When to use construction-takeoff data:**
1. **Primary source unavailable**: When plan extraction cannot identify quantities (poor scan quality, hand-drawn plans, missing schedules)
2. **Cross-verification**: When plan-extracted quantities need independent validation
3. **Scope additions**: For change order scope that isn't on the original plans
4. **Owner-furnished takeoffs**: When the owner or CM provides their own takeoff data for comparison

**Integration rules:**
- Construction-takeoff results are treated as Priority 3 — they do NOT override plan-extracted (Priority 1) or manually entered (Priority 2) quantities without superintendent approval
- When construction-takeoff quantity differs from plan-extracted by >10%, trigger the Discrepancy Resolution workflow (see Discrepancy Resolution section)
- Store construction-takeoff source reference in quantity record: `source: "construction-takeoff"`, `takeoff_id: "CT-###"`

**Limitations:**
- The construction-takeoff skill runs within the cowork platform — it is NOT available in Claude Code standalone mode
- Takeoff accuracy depends on drawing quality and scale calibration
- Material-specific waste factors are NOT applied by construction-takeoff — they must be added by quantitative-intelligence using the waste factor hierarchy

---

## Cross-Sheet Reference Index (Data Source)

Assembly chains depend on a **cross-sheet reference index** stored in `plans-spatial.json → sheet_cross_references`. This index is built automatically during document processing (Pass 8 of the visual pipeline / Pass 4D of Claude Vision extraction) and contains:

- **`drawing_index`** — Every sheet in the set with number, title, discipline, type, revision
- **`detail_callouts`** — Section cuts, detail callouts, elevation markers linking source sheets to target views
- **`schedule_references`** — Door/window/equipment marks linking plan sheets to schedule sheets
- **`spec_references`** — Spec section callouts from drawing notes
- **`assembly_chains`** — Pre-built chains linking elements across sheets

**When building assembly chains**, always check `sheet_cross_references.detail_callouts` first to find which sheets are linked. This is faster and more reliable than searching through all sheets for related data.

**Orphan Reference Check**: After building chains, verify that every target sheet in the callout index exists in the drawing index. Missing targets may indicate sheets not yet processed or not included in the plan set.

---

## Assembly Chains

An assembly chain links every piece of information about a single construction element across all sheets where it appears. Chains are the foundation for multi-page calculations.

### Chain Structure

Each chain has:
- **Element identifier** (e.g., "Footing F1", "Wall Type 2A", "RTU-1")
- **Links** — ordered list of sheets and what data each provides
- **Calculated values** — derived from combining all link data
- **Source priority** — which source provided each value

### Common Chain Types

| Chain Type | Typical Links | Calculates |
|-----------|--------------|------------|
| **Footing** | Foundation plan → footing detail → structural notes → spec | Volume (CY), rebar weight (lbs), form area (SF) |
| **Wall** | Floor plan (length) → building section (height) → wall type legend (assembly) → spec | Total LF, total SF, GWB SF, insulation SF, stud count |
| **Room** | Floor plan (boundary) → finish schedule (materials) → RCP (ceiling) → spec | Area SF, perimeter LF, wall SF, ceiling SF, flooring SF |
| **SOG** | Floor plan (area) → structural notes (thickness) → spec (concrete) | Area SF, volume CY, vapor barrier SF, rebar/WWF qty |
| **Roof** | Roof plan (area) → building section (slope/assembly) → spec (roofing) | Area SF (flat), area SF (sloped), insulation SF |
| **PEMB column** | PEMB reaction drawing → foundation plan → anchor bolt layout → erection plan | Reaction loads, anchor bolt spec, tributary area |
| **Pipe run** | Plumbing plan sheet 1 + sheet 2 + ... → riser diagram → spec | Total LF by size, fitting count, hanger count |
| **Equipment** | MEP plan (location) → equipment schedule (specs) → spec (requirements) | Count, capacity, electrical requirements, clearances |

### Building Chains Automatically

1. Start from a **known element** (room number, footing mark, equipment tag)
2. Look up all **cross-references** in the index that mention this element
3. Follow each reference to its **target sheet**
4. Extract the **relevant data** from each linked sheet
5. Assemble the chain and **calculate derived quantities**

### Assembly Chain Impact from Non-Plan Documents

When `/process-docs` processes RFI responses, submittal approvals, or change orders that reference specific plan elements:

- The affected assembly chain should be marked with `needs_verification: true`
- The verification note should reference the source document: "RFI-003 response may affect Footing F1 assembly chain — rebar callout clarified"
- On the next plan processing run, chains marked `needs_verification` are rebuilt first
- This prevents quantity data from becoming stale when clarifications arrive via non-plan documents

---

## Calculation Capabilities

### Initial vs Incremental Quantity Processing

- **First run** (no existing quantities): Build the full quantity baseline. Extract all measurable elements, create all assembly chains, and establish source attribution for every value. Note in output: "Initial quantity baseline established — X elements tracked across Y sheets."
- **Incremental** (quantities already exist): Only recalculate quantities affected by newly processed sheets. Preserve existing chains and only rebuild where new data touches them. Cross-verify new values against existing ones.

### Concrete Volumes

From structural details — DXF polylines provide exact footing outlines; visual dimensions provide depth from structural notes.

| Element | Formula | Sources |
|---------|---------|---------|
| Footings | L × W × D per footing × count | Foundation plan + footing detail |
| SOG | Area × thickness | Floor plan + structural notes |
| Grade beams | L × W × D | Foundation plan + detail |
| Piers | π × r² × D or L × W × D | Foundation plan + detail |
| Walls | L × H × T | Floor plan + building section |
| Curbs | L × W × H | Site plan + detail |

Always add waste factor: 5% for formed elements, 10% for footings (over-excavation), 3% for SOG.

### Room Areas and Perimeters

From DXF closed polylines (exact) or visual measurements (approximate) or dimension annotations on plans.

- **Area**: Shoelace formula on polyline vertices (DXF), or pixel counting at calibrated scale (visual)
- **Perimeter**: Sum of polyline segment lengths (DXF), or boundary tracing (visual)
- **Wall area**: Perimeter × ceiling height (from building section or room elevation)
- **Ceiling area**: Same as floor area (flat ceiling) or calculated from section (sloped/vaulted)

### Material Quantities by CSI Division

Aggregate individual items into division totals:

- **Division 03**: Total CY of concrete by mix type, total tons of rebar by grade
- **Division 05**: Total tons of structural steel, total LF of miscellaneous metals
- **Division 07**: Total SF of roofing, insulation, waterproofing, sealant LF
- **Division 08**: Door count by type, hardware set count, window count by type
- **Division 09**: Flooring SF by type, GWB SF, ceiling SF by type, paint SF
- **Division 22**: Fixture count by type, pipe LF by size, valve count
- **Division 23**: Equipment count, ductwork LF/SF, diffuser count
- **Division 26**: Panel count, outlet count by type, switch count, light fixture count

### PEMB-Specific Quantities

- **Tributary areas** per column (bay spacing × frame spacing)
- **Bay areas** (length × width per bay)
- **Wall panel SF** (eave height × perimeter, minus openings)
- **Roof panel SF** (ridge length × slope length × 2 sides)
- **Gutter LF** (eave length, both sides)
- **Downspout count** (typically 1 per 40-50 LF of gutter)

### Flooring by Type

Total SF of each flooring material from finish schedule + room areas + visual zone detection:

1. Read finish schedule for room → flooring material mapping
2. Look up room area from quantities.rooms
3. Sum by material type
4. Cross-check against visual material zone detection (Phase 7)
5. Flag discrepancies >10%

### Symbol Counts

Total fixture/device counts from visual detection, validated against schedule counts:

1. Visual Pass 4 detects symbols on plan sheets
2. Aggregate counts across all plan sheets (avoid double-counting on overlapping sheets)
3. Compare against schedule counts (door schedule, fixture schedule, panel schedule)
4. Flag discrepancies — schedule count is authoritative; visual count validates

---

## Integration with Downstream Skills

### /morning-brief
When the morning brief mentions today's work areas, include relevant quantities:
- "Room 007 Therapy: 450 SF VCT flooring, 86 LF vinyl base"
- "Footings at Grid C-3 through D-5: 12.4 CY concrete (4,000 PSI), #5@12" E.W."
- "22 duplex outlets remaining in East Wing (63 of 85 installed = 74%)"

### /daily-report
When daily reports reference work completed, enable percentage calculations:
- "Completed VCT in Rooms 007-009: 1,240 SF of 4,800 SF total (26%)"
- "Poured Footings F1-F4: 9.5 CY of 42.3 CY total footings (22%)"
- "Installed 15 duplex outlets in Rooms 101-108 (East Wing: 63/85 = 74%)"

### /look-ahead
When generating lookahead schedules, include material quantities for upcoming activities:
- "Week 2: SOG pour Area B — 156 CY concrete needed, 4 trucks at 40 CY/day"
- "Week 3: VCT installation Rooms 201-215 — 3,200 SF, ~4 days at 800 SF/day"

### /project-dashboard
Quantity summary section showing:
- Total quantities by CSI division
- Percent complete by material type (installed / total)
- Discrepancy log with resolution status
- Source attribution breakdown (what % from DXF, visual, takeoff, text)

---

## Workflow

### Initial Quantity Extraction (during /set-project or /process-docs)

1. **Build drawing index** from sheet list (sheet numbers, titles, disciplines)
2. **Build cross-reference index** from text + visual + DXF extraction results
3. **Identify assembly chains** by tracing cross-references for key elements
4. **Calculate quantities** using assembly chains + data from all sources
5. **Flag discrepancies** where sources disagree >10%
6. **Store in config** under `plans-spatial.json` `quantities` and `sheet_cross_references`
7. **Report summary** to superintendent for validation

### Incremental Updates (when new documents added)

1. **Read existing index** from config
2. **Process new document** through extraction pipeline
3. **Update index** with new cross-references
4. **Recalculate affected chains** (only chains linked to new/changed sheets)
5. **Update quantities** and flag new discrepancies
6. **Report changes** to superintendent

### On-Demand Queries

When the superintendent asks a quantity question:

1. **Check stored quantities** in config
2. **If available**: Return with source attribution and confidence
3. **If not available**: Build assembly chain on-the-fly, calculate, store, return
4. **If discrepancy exists**: Present both values, ask for resolution

---

## Cross-Verification — Checking Your Work Across Sheets

The same data point often appears on multiple sheets. This is intentional — construction documents are redundant by design. Use this redundancy to **verify accuracy and build confidence** in extracted values.

### The Verification Principle

**Every critical measurement should be confirmed from at least two independent sources.** When two sources agree, confidence is HIGH. When they disagree, flag for review — one of them is wrong (or the drawings have a coordination error the super needs to know about).

### What to Cross-Check and Where

| Data Point | Primary Source | Verification Source(s) | How to Check |
|-----------|---------------|----------------------|-------------|
| **Pipe length** | Plan view (measured centerline) | Profile view (station-to-station distances) | Plan LF should match profile station difference |
| **Pipe size** | Plan view (label on pipe) | Profile view (pipe schedule), Plumbing schedule | All three should match |
| **Pipe invert elevation** | Profile view (invert table) | Plan view (spot elevation at manholes) | Profile inverts should match plan spot elevations |
| **Footing size** | Foundation plan (dimensions) | Footing detail (cross-section dims) | Plan L×W should match detail L×W; detail adds depth |
| **Concrete strength** | Structural general notes | Spec Section 03 30 00 | Must match — if not, spec governs per most contracts |
| **Room area** | Floor plan (scaled or dimensioned) | Finish schedule (if area column exists) | Should match within 5% |
| **Door size** | Door schedule | Door detail (if exists) | Must match — schedule is authoritative |
| **Equipment capacity** | Equipment schedule | Equipment detail/spec sheet | Must match — schedule is design intent |
| **Building dimensions** | Floor plan outer dimension string | Site plan building footprint | Must match |
| **Finish floor elevation** | Architectural floor plan (FFE) | Civil grading plan (pad + slab thickness) | Pad elev + slab thickness should = FFE |
| **Ceiling height** | Room finish schedule | Building section (floor-to-ceiling dim) | Must match |
| **Grid spacing** | Foundation plan (dimension strings) | Framing plan (dimension strings) | Must match exactly — this is the structural skeleton |
| **Slab thickness** | Structural notes (typical thickness) | Building section (shown in section) | Must match |
| **Rebar size/spacing** | Structural detail (shown in section) | Structural notes (listed by element) | Must match |
| **Wall assembly** | Wall type legend/schedule | Building section (shown in section) | Layers and thickness must match |

### Grading Plan Cross-Verification

Grading plans are a special case because **existing and proposed grades are always on separate sheets** (or separate line types on the same sheet):

1. **Existing grade** — From survey/topo sheet (C-001 or C-100 series), shown as dashed contours
2. **Proposed grade** — From grading plan (C-200 series or same sheet), shown as solid contours
3. **Cut/fill calculation** requires overlaying BOTH — at every point, subtract existing from proposed
4. **Verify FFE** — The proposed grade at the building pad should be consistent with the FFE on architectural plans minus slab thickness minus subbase
5. **Verify drainage** — Proposed contours should show water flowing AWAY from the building (grade drops away from FFE in all directions)

**Verification formula:**
```
FFE (Arch) = Pad Elevation (Civil) + Subbase Thickness + Slab Thickness
```
If this doesn't check out, there's a coordination error between civil and architectural.

### Dimension String Verification

Dimension strings contain built-in cross-checks:

```
|←— 12'-0" —→|←— 30'-0" —→|←— 30'-0" —→|←— 12'-0" —→|
|←————————————————— 84'-0" ————————————————————————→|
```

**Check:** Do the individual dimensions sum to the overall dimension?
- 12 + 30 + 30 + 12 = 84 ✓

If they don't match, the drawings have an error. Flag it — this is exactly the kind of thing a superintendent needs to catch before construction.

### Confidence Scoring

After cross-verification, assign confidence based on how many sources agree:

| Sources Checked | Agreement | Confidence Level |
|----------------|-----------|-----------------|
| 3+ sources, all agree | Full agreement | **VERIFIED** — high confidence |
| 2 sources, agree | Agreement | **CONFIRMED** — good confidence |
| 2 sources, within 5% | Minor variance | **LIKELY CORRECT** — acceptable for estimation |
| 2 sources, 5-10% apart | Moderate variance | **CHECK** — may be rounding or scale measurement error |
| 2 sources, >10% apart | Major discrepancy | **DISCREPANCY** — flag for superintendent review |
| 1 source only | No verification | **UNVERIFIED** — use with caution, note in output |

---

## Discrepancy Resolution

When quantity calculations flag discrepancies (>10% variance between sources), the superintendent must resolve them. Without resolution tracking, discrepancies re-appear on every calculation run.

### Resolution Workflow

1. **Flag raised**: Calculator identifies >10% variance between sources (e.g., plan count vs. schedule quantity vs. takeoff)
2. **Superintendent reviews**: Examines source data, determines which value is correct
3. **Resolution recorded**: Decision stored in `plans-spatial.json → discrepancy_log[]`
4. **Downstream cascade**: Resolved quantity triggers re-check in cost-tracking (budget impact), labor-tracking (production rate recalc), and procurement-log (order quantity adjustment)

### Discrepancy Log Entry Structure

```json
{
  "discrepancy_id": "DISC-001",
  "element": "Footing F1",
  "quantity_type": "concrete_volume",
  "source_values": {
    "plan_calculation": "12.5 CY",
    "schedule_quantity": "10.0 CY",
    "takeoff_quantity": "11.8 CY"
  },
  "variance_percent": 25,
  "resolved_value": "12.5 CY",
  "resolution_rationale": "Plan calculation includes haunch per structural detail S-5.2; schedule quantity was from preliminary estimate",
  "resolved_by": "Superintendent",
  "resolution_date": "2026-03-15",
  "downstream_updates": [
    "cost-data.json: Budget line 03-CONC updated",
    "procurement-log.json: PO-042 quantity confirmed"
  ]
}
```

### Auto-Skip Resolved Discrepancies

On subsequent calculation runs, check `plans-spatial.json → discrepancy_log[]` before flagging:
- If `discrepancy_id` matches a previous flag AND `resolved_value` exists → use resolved value, do NOT re-flag
- If source values have CHANGED since resolution → re-flag with note "Previously resolved — source data changed"

---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
