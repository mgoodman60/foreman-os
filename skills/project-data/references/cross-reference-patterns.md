# Cross-Reference Patterns

Codified patterns for connecting related data across the project intelligence data store. Each pattern specifies trigger conditions, files to read, fields to extract, and output format.

---

## Pattern 1: Sub → Scope → Spec → Inspection

**Trigger:** A subcontractor is mentioned (by name, trade, or casual reference).

**Purpose:** Build a full context chain from the sub to their scope, governing spec requirements, and required inspections.

### Files to Read
1. `directory.json` → `subcontractors[]` — match sub by name or trade
2. `specs-quality.json` → `spec_sections[]` — match by trade/division
3. `specs-quality.json` → `hold_points[]` — match by work type
4. `inspection-log.json` → `inspection_log[]` — find related inspections
5. `schedule.json` → `milestones[]`, `critical_path[]` — find schedule activities for this trade

### Fields to Extract
```
directory.json → subcontractors[match]
  .name           → Full company name
  .trade          → Primary trade
  .scope          → Contracted scope of work
  .foreman        → Field foreman name + phone
  .status         → active/mobilized/demobilized

specs-quality.json → spec_sections[match by division]
  .section        → CSI section number
  .title          → Section title
  .key_req        → Primary requirement
  .testing        → Testing frequency, type, agency
  .hold_points    → Required inspection hold points

specs-quality.json → hold_points[match by work_type]
  .inspection_name → Required inspection
  .trigger        → When inspection is needed
  .inspector      → Who performs it

schedule.json → milestones/critical_path[match by trade]
  .name           → Activity name
  .date           → Scheduled date
  .status         → on_track/at_risk/behind
```

### Output Format
```
Sub: Walker Construction (Excavation/Sitework)
  Scope: Site grading, utilities, paving
  Foreman: Mike Johnson (555-0101)
  Spec Sections: 31 20 00 (Earth Moving), 31 23 16 (Trenching)
  Testing: Compaction testing @ 95% modified Proctor, every 500 CY
  Hold Points: HP-06 (Underground utilities — before backfill)
  Schedule: Earthwork complete milestone — Mar 15 (on track)
```

### Consuming Skills
`intake-chatbot`, `punch-list`, `meeting-minutes`, `daily-report`, `labor-tracking`

---

## Pattern 2: Location → Grid → Area → Room

**Trigger:** A location is mentioned (room number, area name, grid reference, casual description like "east side" or "by the elevator").

**Purpose:** Resolve a casual location reference into a complete spatial context with grid coordinates, building area, floor level, and adjacent rooms.

### Files to Read
1. `plans-spatial.json` → `room_schedule[]` — match room number
2. `plans-spatial.json` → `building_areas[]` — match area name
3. `plans-spatial.json` → `floor_levels[]` — match floor
4. `plans-spatial.json` → `grid_lines` — resolve grid coordinates
5. `plans-spatial.json` → `site_utilities` — nearby utilities (for safety context)

### Resolution Logic
```
Input: "Room 107"
  → room_schedule[room_number="107"]
    → floor_level: "Level 1"
    → building_area: "East Wing"
  → building_areas[name="East Wing"]
    → grids: "E-G / 3-5"
  → grid_lines
    → columns: E, F, G
    → rows: 3, 4, 5

Input: "east side"
  → building_areas[name contains "east"]
    → "East Wing", grids "E-G / 3-5", floors "Level 1-2"
  → room_schedule[building_area="East Wing"]
    → All rooms in East Wing

Input: "at Grid C"
  → building_areas[grids contains "C"]
    → matching area(s)
  → room_schedule[grid overlaps with C]
    → rooms near Grid C
```

### Fields to Extract
```
plans-spatial.json → room_schedule[match]
  .room_number     → Room identifier
  .room_name       → Room function/name
  .floor_level     → Which floor
  .building_area   → Which zone

plans-spatial.json → building_areas[match]
  .name            → Zone name
  .grids           → Grid range
  .floors          → Floor range

plans-spatial.json → grid_lines
  .columns         → Column identifiers
  .rows            → Row identifiers
  .spacing         → Bay spacing
```

### Output Format
```
Location: Room 107 (Therapy)
  Floor: Level 1
  Area: East Wing
  Grid: E-G / 3-5
  Nearby: Rooms 105 (Office), 108 (Storage), 109 (Restroom)
```

### Consuming Skills
`intake-chatbot`, `punch-list`, `labor-tracking`, `safety-management`, `inspection-tracker`

---

## Pattern 3: Work Type → Weather Threshold → Today's Weather

**Trigger:** An outdoor or weather-sensitive work activity is being performed today (concrete, roofing, crane operations, earthwork, waterproofing, painting).

**Purpose:** Cross-check today's weather conditions against spec-mandated thresholds for the active work type to auto-flag violations.

### Files to Read
1. `specs-quality.json` → `weather_thresholds[]` — match by work type
2. `daily-report-intake.json` or daily report weather data — today's conditions
3. `specs-quality.json` → `spec_sections[match].weather_thresholds` — section-specific limits

### Fields to Extract
```
specs-quality.json → weather_thresholds[match by work_type]
  .work_type        → Activity name
  .min_temp         → Minimum temperature
  .max_temp         → Maximum temperature
  .max_wind         → Maximum wind speed
  .moisture_ok      → Whether moisture is acceptable
  .spec_reference   → Source spec section
  .mitigation_measures → Cold/hot weather adjustments

Today's weather (from daily report or intake)
  .temperature      → Current/high/low temp
  .wind_speed       → Current wind conditions
  .precipitation    → Rain/snow/moisture
```

### Evaluation Logic
```
IF today_temp < weather_thresholds[work_type].min_temp:
  FLAG: "Cold weather threshold exceeded for {work_type}"
  INCLUDE: mitigation_measures from spec
  EXAMPLE: "Concrete placement: Temp 35°F < 40°F minimum per Spec 03 30 00.
            Cold weather measures required: heated enclosures, insulated blankets."

IF today_wind > weather_thresholds[work_type].max_wind:
  FLAG: "Wind speed threshold exceeded for {work_type}"
  EXAMPLE: "Crane operations: Wind 28 mph > 25 mph limit.
            Suspend crane operations until wind subsides."

IF precipitation AND NOT weather_thresholds[work_type].moisture_ok:
  FLAG: "Moisture restriction violated for {work_type}"
  EXAMPLE: "Waterproofing: Rain detected. Spec requires dry substrate.
            Suspend waterproofing application."
```

### Output Format
```
WEATHER ALERT: Concrete Pour at Grid C-3
  Today: 35°F, wind 12 mph, clear
  Threshold: Min 40°F (Spec 03 30 00)
  Status: BELOW MINIMUM — Cold weather measures required
  Mitigation: Heated enclosures, insulated blankets, minimum 50°F for 72 hours
```

### Consuming Skills
`safety-management`, `inspection-tracker`, `intake-chatbot`, `/daily-report`

---

## Pattern 4: Element → Assembly Chain → Multi-Sheet Data

**Trigger:** A specific construction element is referenced (footing mark, wall type, equipment tag, room number for finishes).

**Purpose:** Trace the element's assembly chain across all plan sheets to gather complete dimensional, material, and specification data for calculations.

### Files to Read
1. `plans-spatial.json` → `sheet_cross_references.assembly_chains[]` — find chain for element
2. `plans-spatial.json` → `sheet_cross_references.detail_callouts[]` — find linked details
3. `plans-spatial.json` → `quantities` — find calculated values
4. `specs-quality.json` → `spec_sections[]` — governing spec for element type

### Fields to Extract
```
plans-spatial.json → assembly_chains[match by element]
  .id              → Chain identifier (CHAIN-001)
  .description     → Element description
  .links[]         → Ordered list of sheet links
    .sheet         → Sheet number
    .element       → What data this sheet provides
    .data          → Dimensions, materials, notes
  .calculated_values → Derived quantities (volume, area, weight)
    .source_priority → Which source provided each value

plans-spatial.json → quantities[match by element]
  .volume_cy_total → Total volume (concrete)
  .area_sf         → Area (rooms, flooring)
  .total_lf        → Length (pipe, wall)
  .source          → dxf/visual/takeoff/text
  .confidence      → high/medium/low
```

### Output Format
```
Element: Footing F1 at Grid C-3
  Assembly Chain: CHAIN-001
    S2.1 (Foundation Plan) → plan location, dimensions 4'-0" × 2'-0"
    S5.1 (Detail 3)       → depth 1'-6", #5 rebar @ 12" EW, 3" CLR
    S1.0 (Structural Notes)→ 4,000 PSI concrete, A615 Gr 60 rebar
  Calculated:
    Volume: 0.44 CY (source: DXF — exact)
    Rebar: 48 lbs (source: visual — estimate)
    Concrete Spec: Section 03 30 00
```

### Schedule Activity Linkage

Each assembly chain can link to one or more `schedule.json` activities via `linked_schedule_activities[]`:

```json
{
  "chain_id": "CHAIN-001",
  "element": "Footing F1",
  "assemblies": ["FTG-F1-rebar", "FTG-F1-form", "FTG-F1-pour", "FTG-F1-strip"],
  "linked_schedule_activities": [
    {"activity_id": "FOD-05", "description": "Foundation forming", "assembly_step": "FTG-F1-form"},
    {"activity_id": "FOD-06", "description": "Foundation rebar", "assembly_step": "FTG-F1-rebar"},
    {"activity_id": "FOD-07", "description": "Foundation pour", "assembly_step": "FTG-F1-pour"},
    {"activity_id": "FOD-08", "description": "Foundation strip", "assembly_step": "FTG-F1-strip"}
  ]
}
```

This enables:
- **Earned value**: Physical progress on assembly steps → percent complete on schedule activities → EVM calculations
- **Look-ahead validation**: Assembly prerequisites checked against schedule predecessor logic
- **Delay impact**: If an assembly step is delayed, linked schedule activity automatically flagged

### Consuming Skills
`quantitative-intelligence`, `cost-tracking`, `/daily-report`, `/morning-brief`

---

## Pattern 5: RFI → Submittal → Procurement Chain

**Trigger:** An RFI, submittal, or procurement item is referenced, or a material/product question arises.

**Purpose:** Trace the full documentation chain from design question through product approval to material delivery.

### Files to Read
1. `rfi-log.json` → `rfi_log[]` — find RFI by subject/ID
2. `submittal-log.json` → `submittal_log[]` — find linked submittals
3. `procurement-log.json` → `procurement_log[]` — find linked procurement
4. `specs-quality.json` → `spec_sections[]` — governing spec requirements
5. `schedule.json` → `long_lead_items[]` — lead time impact

### Fields to Extract
```
rfi-log.json → rfi_log[match]
  .id              → RFI identifier
  .subject         → Topic
  .status          → draft/issued/response_received/resolved
  .response_text   → Architect's response
  .related_submittals → Linked submittal IDs
  .schedule_impact → none/minor/major

submittal-log.json → submittal_log[match by related_rfis or spec_section]
  .id              → Submittal identifier
  .status          → submitted/approved/revise_and_resubmit
  .spec_section    → Governing spec
  .lead_time_weeks → Supplier lead time
  .related_rfis    → Linked RFI IDs

procurement-log.json → procurement_log[match by submittal_id]
  .id              → Procurement identifier
  .item            → Material item
  .expected_delivery → Delivery date
  .delivery_status → ordered/shipped/delivered/delayed
  .total_cost      → PO amount
```

### Chain Logic
```
Forward chain (RFI triggers submittal):
  RFI-003 "Alternate concrete mix" (status: resolved)
    → Response: "Approved per RFI response dated 2/15"
    → Triggers: SUB-C-005 "Concrete mix design submittal"
    → Approval: "approved" on 2/20
    → Triggers: PROC-012 "Ready-mix concrete order"
    → Status: "ordered", delivery: 3/1

Reverse chain (procurement delay triggers RFI):
  PROC-015 "PEMB steel" (status: delayed, 3 weeks)
    → Linked submittal: SUB-S-002 (approved)
    → NEW RFI needed: "Alternate steel supplier approval"
    → Schedule impact: major (critical path)
```

### Output Format
```
Chain: RFI-003 → SUB-C-005 → PROC-012
  RFI: "Alternate concrete mix" — Resolved 2/15
  Submittal: Concrete mix design — Approved 2/20
  Procurement: Ready-mix concrete — Ordered, delivering 3/1
  Spec: 03 30 00 (Cast-in-Place Concrete)
  Schedule Impact: None (delivery before pour date 3/5)
```

### Consuming Skills
`meeting-minutes`, `change-order-tracker`, `/morning-brief`, `/look-ahead`

---

## Pattern 6: Assembly → Schedule → Earned Value

```
Assembly Chain (plans-spatial.json → assembly_chains[])
  → linked_schedule_activities[] → schedule.json activities
    → percent_complete → cost-data.json EVM fields
      → earned-value-management skill calculations
```

**When to use**: Any time physical progress needs to flow into cost/schedule reporting. The assembly chain is the "what was built," schedule activity is "when it was planned," and EVM is "how do planned vs. actual compare."

---

## Pattern 7: Dual-Source Utility Reconciliation

```
Drawing Notes (document-intelligence) → plans-spatial.json → site_utilities[]
DWG Layers (dwg-extraction) → plans-spatial.json → dwg_storm_sewer[], dwg_water[], dwg_sanitary[], dwg_gas[], dwg_electric[], dwg_telecom[]
```

**Problem**: Two extraction pipelines produce utility data independently. Document-intelligence extracts from drawing notes (text-based: pipe material, size callouts, invert elevations). DWG-extraction extracts from CAD layers (spatial: line coordinates, polyline paths, block insertions).

**Resolution Priority**:

| Data Type | Primary Source | Secondary Source | Rationale |
|-----------|---------------|-----------------|-----------|
| Spatial routing (coordinates, paths) | DWG extraction | Drawing notes | CAD geometry is more precise |
| Pipe/conduit size | DWG extraction (ATTRIB data) | Drawing notes | ATTRIBs are structured data |
| Pipe material | Drawing notes | DWG extraction | Material callouts are text-heavy, not in CAD attributes |
| Invert elevations | Drawing notes | DWG extraction | Elevations are typically annotated, not in line geometry |
| Utility type classification | DWG extraction (layer name) | Drawing notes | Layer naming conventions are reliable |
| Connection points (manholes, valves) | DWG extraction (block insertions) | Drawing notes | Blocks have precise coordinates |

**Reconciliation Workflow**:
1. After both pipelines run, compare `site_utilities[]` entries against `dwg_*[]` entries for the same utility system
2. For each utility segment, merge data: take spatial data from DWG, metadata from drawing notes
3. Flag conflicts (e.g., drawing note says "8" PVC" but DWG ATTRIB says "6" PVC") for superintendent review
4. Store reconciled data in `site_utilities[]` with `source` field indicating "dwg", "notes", or "reconciled"

**When to use**: After any `/process-docs` run that includes both plan sheets and DWG files for site/civil work. The reconciled utility data feeds into as-built comparisons, excavation safety checks, and quantity calculations.

---

## Pattern Usage Guidelines

1. **Always check if project intelligence is loaded** before attempting cross-references. If `plans-spatial.json` or `specs-quality.json` is empty, skip enrichment and note the gap.

2. **Cascade resolution** — start with the most specific identifier (room number, sub name, element mark) and cascade outward to gather related context.

3. **Never block on missing data** — if a cross-reference target doesn't exist (e.g., sub not in directory), proceed with available data and flag the gap.

4. **Source attribution** — when presenting cross-referenced data, always note which file and field the data came from so the superintendent can verify.

5. **Freshness awareness** — data may be stale if documents haven't been reprocessed recently. Note `documents_loaded.date_loaded` to assess data freshness.
