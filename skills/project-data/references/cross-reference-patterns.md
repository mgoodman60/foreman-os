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

## Pattern 8: Risk → Schedule → Cost

**Trigger:** A risk event is identified, discussed, or a risk register review is requested. Also triggered when a schedule activity or cost division shows unexpected variance that could be linked to a known risk.

**Purpose:** Connect risk register entries to the schedule activities they threaten and the cost accounts they may impact, enabling integrated risk-schedule-cost analysis.

### Files to Read
1. `risk-register.json` → `risks[]` — match risk by ID, category, or description
2. `schedule.json` → `activities[]` — match by `linked_activity_id` or activity name keyword
3. `cost-data.json` → `budget_by_division[]`, `contingency` — match by cost code or division
4. `delay-log.json` → `delays[]` — check if risk has already materialized as a delay

### Fields to Extract
```
risk-register.json → risks[match]
  .risk_id           → Risk identifier (RSK-NNN)
  .description       → Risk description
  .category          → schedule/cost/safety/quality/external
  .probability       → Likelihood (0.0 - 1.0)
  .impact            → Impact score (1-10)
  .risk_exposure     → probability × impact
  .risk_owner        → Who owns the mitigation
  .mitigation_plan   → Planned response
  .mitigation_status → not_started/in_progress/complete
  .contingency_allocated → Reserved contingency for this risk
  .linked_activity_id → Schedule activity this risk threatens

schedule.json → activities[match by linked_activity_id]
  .activity_name     → Activity description
  .early_start       → Planned start
  .total_float       → Available float (days)
  .is_critical       → On critical path
  .percent_complete  → Current progress

cost-data.json → budget_by_division[match by risk.cost_code]
  .division          → CSI division number
  .original_amount   → Budget baseline
  .current_amount    → Current budget (with COs)
  .committed_costs   → Committed to date

cost-data.json → contingency
  .original_amount   → Total contingency
  .spent             → Contingency used
```

### Chain Logic
```
Forward chain (risk threatens schedule and cost):
  RSK-003 "Steel delivery delay" (probability: 0.7, impact: 8)
    → Linked activity: "Steel Erection - Level 2" (critical path, float: 0)
    → Cost impact: Division 05 (Metals) — $450K committed, $380K budget
    → Contingency allocated: $85,000
    → Mitigation: Pre-qualify alternate supplier (status: in_progress)

Reverse chain (schedule/cost anomaly traced to risk):
  Activity "Steel Erection - Level 2" showing 5-day slip
    → Check risk-register for linked risks → RSK-003 (active)
    → Risk materialized → check delay-log for matching entry
    → Cost variance in Div 05 → risk contingency draw needed
```

### Output Format
```
RISK-SCHEDULE-COST LINK — RSK-003
  Risk: Steel delivery delay (exposure: 5.6 — Critical)
  Schedule Impact: Steel Erection Level 2 (critical path, 0 float)
    — If triggered: 12-day delay, cascading to 3 successor activities
  Cost Impact: Division 05 variance potential $85,000
    — Contingency allocated: $85,000 (18.9% of total contingency)
  Mitigation: Pre-qualify alternate supplier — IN PROGRESS
  Owner: Project Manager
```

### Consuming Skills
`risk-management`, `cost-tracking`, `earned-value-management`, `/morning-brief`, `/weekly-report`

---

## Pattern 9: Claims → Delay → CO

**Trigger:** A claim is filed, a notice of claim is sent, or a discussion references contractual disputes, time extensions, or differing site conditions. Also triggered when reviewing delay log entries or change orders that may support a claim.

**Purpose:** Link claims documentation to the underlying delay events and change orders that form the factual basis of each claim, ensuring complete evidence chains for dispute resolution.

### Files to Read
1. `claims-log.json` → `claims[]` — match claim by ID, type, or description
2. `delay-log.json` → `delays[]` — match by `related_delay_ids` or date range overlap
3. `change-order-log.json` → `change_orders[]` — match by `related_co_ids` or description
4. `daily-report-data.json` → `entries[]` — contemporaneous records supporting the claim
5. `schedule.json` → `activities[]` — critical path impact analysis

### Fields to Extract
```
claims-log.json → claims[match]
  .claim_id              → Claim identifier (CLM-NNN)
  .description           → Claim description
  .claim_type            → time_extension/cost/acceleration/differing_conditions
  .status                → draft/notice_sent/filed/under_review/negotiation/resolved/denied
  .claimed_amount        → Dollar amount claimed
  .claimed_days          → Time extension days claimed
  .notice_required_by    → Contractual notice deadline
  .notice_sent_date      → Date notice was sent
  .related_delay_ids     → Linked delay log entries
  .related_co_ids        → Linked change orders
  .evidence_documents[]  → Supporting documentation references

delay-log.json → delays[match by related_delay_ids]
  .delay_id        → Delay identifier
  .cause           → Weather/owner/design/unforeseen/sub
  .delay_days      → Duration of delay
  .date_identified → When delay was identified
  .impact          → critical_path/near_critical/non_critical

change-order-log.json → change_orders[match by related_co_ids]
  .co_number             → CO identifier
  .description           → Change description
  .amount                → CO amount
  .status                → draft/submitted/approved/rejected
  .schedule_impact_days  → Time impact
```

### Chain Logic
```
Forward chain (claim built from delays and COs):
  CLM-002 "Differing site conditions — unexpected rock"
    → Delay events: DEL-008 (14 days, critical path), DEL-009 (3 days, concurrent)
    → Change orders: CO-012 ($350K, pending), CO-013 ($42K, approved)
    → Daily reports: Feb 1-14 entries documenting rock removal
    → Schedule impact: 14 days on critical path, extending completion

Reverse chain (delay/CO triggers claim evaluation):
  DEL-008 "Unforeseen rock at foundation" (owner-caused, 14 days)
    → Check claims-log: CLM-002 references this delay
    → CO-012 submitted for cost recovery
    → Evidence: daily reports, geotech report, contract Section 4.3
```

### Output Format
```
CLAIMS CHAIN — CLM-002
  Claim: Differing site conditions — unexpected rock ($350,000 + 14 days)
  Status: Filed — under review
  Delay Basis:
    DEL-008: 14 days (critical path) — unforeseen subsurface conditions
    DEL-009: 3 days (concurrent) — additional dewatering
  CO Linkage:
    CO-012: $350,000 (pending) — rock removal and foundation redesign
    CO-013: $42,000 (approved) — dewatering equipment
  Evidence: 14 daily reports, geotech boring logs, contract Section 4.3.1
  Notice: Sent 2026-01-12 (within 7-day requirement)
```

### Consuming Skills
`change-order-tracker`, `delay-tracker`, `meeting-minutes`, `/weekly-report`

---

## Pattern 10: Environmental → Inspection → Safety

**Trigger:** An environmental compliance event is referenced (SWPPP inspection, LEED credit tracking, waste diversion report, hazmat incident), or when environmental factors intersect with inspection scheduling or safety management.

**Purpose:** Connect environmental compliance records to related inspection events and safety incidents, ensuring that environmental obligations are tracked alongside the inspection and safety programs.

### Files to Read
1. `environmental-log.json` → `swppp`, `leed_credits[]`, `waste_diversion`, `hazmat` — environmental compliance data
2. `inspection-log.json` → `inspections[]` — match environmental inspections
3. `safety-log.json` → `incidents[]` — match environmental safety incidents
4. `specs-quality.json` → `spec_sections[]` — environmental spec requirements
5. `daily-report-data.json` → `entries[]` — weather conditions for SWPPP triggers

### Fields to Extract
```
environmental-log.json → swppp
  .inspections[]        → SWPPP inspection records
  .permit_expiration    → Permit expiration date
  .required_frequency   → Inspection frequency requirement

environmental-log.json → hazmat
  .incidents[]          → Hazmat incidents
    .type               → spill/release/exposure/storage_violation
    .severity           → minor/moderate/major
    .date               → Incident date
    .location           → Location on site

inspection-log.json → inspections[match by type == "environmental"]
  .inspection_type      → SWPPP/erosion_control/dust_control/noise
  .result               → pass/fail/conditional
  .corrective_actions[] → Required follow-ups
  .date                 → Inspection date

safety-log.json → incidents[match by type == "environmental"]
  .description          → Incident description
  .severity             → Severity level
  .sub_name             → Responsible sub
  .corrective_action    → Required response
```

### Chain Logic
```
Forward chain (environmental event triggers inspection and safety):
  SWPPP inspection finding: "Silt fence damaged at south perimeter"
    → Corrective action created in inspection-log
    → If hazmat release risk: safety-log entry created
    → Daily report weather check: rain event within 24 hours?
    → Spec check: erosion control requirements per Section 31 25 00

Reverse chain (safety incident traces to environmental compliance):
  Safety incident: "Fuel spill at equipment staging area"
    → Environmental-log: hazmat incident recorded
    → SWPPP corrective action: spill containment verification
    → Inspection scheduled: post-incident environmental inspection
```

### Output Format
```
ENVIRONMENTAL-INSPECTION-SAFETY LINK
  Environmental Event: SWPPP finding — damaged silt fence (south perimeter)
  Inspection: SWPPP-024 (2026-02-17) — pass with findings
  Corrective Action: Repair silt fence — due 2026-02-28
  Safety Implication: Erosion risk to adjacent property
  Spec Reference: Section 31 25 00 (Erosion and Sedimentation Controls)
  Weather Context: Rain forecast 2026-02-25 — repair urgency elevated
```

### Consuming Skills
`safety-management`, `inspection-tracker`, `report-qa`, `/daily-report`, `/weekly-report`

---

## Pattern 11: Closeout → Quality → Drawing

**Trigger:** A closeout activity is referenced (commissioning, warranty, O&M manuals, training, substantial completion checklist), or when quality records and as-built drawings need to be verified against closeout requirements.

**Purpose:** Link closeout tracking items to the quality records (test results, commissioning reports) and drawing records (as-built status) that prove system completion and compliance.

### Files to Read
1. `closeout-data.json` → `systems[]`, `warranties[]` — closeout tracking by system
2. `quality-data.json` → `system_tests[]`, `test_results[]`, `equipment_data[]` — commissioning and test data
3. `drawing-log.json` → `drawings[]` — as-built drawing status
4. `punch-list.json` → `items[]` — remaining punch items by system
5. `specs-quality.json` → `spec_sections[]` — closeout requirements per spec section

### Fields to Extract
```
closeout-data.json → systems[match]
  .system_name           → System identifier (HVAC, Plumbing, Electrical, etc.)
  .commissioning_status  → not_started/in_progress/complete
  .oam_manual_status     → not_submitted/submitted/approved
  .warranty_status       → not_received/received/filed
  .training_status       → not_scheduled/scheduled/complete
  .completion_pct        → Overall closeout completion

quality-data.json → system_tests[match by system]
  .test_type             → Commissioning test type
  .result                → pass/fail/conditional
  .date                  → Test date
  .deficiencies[]        → Outstanding deficiencies

quality-data.json → equipment_data[match by system]
  .equipment_tag         → Equipment identifier
  .oam_manual_received   → Boolean
  .warranty_document     → Reference to warranty document

drawing-log.json → drawings[match by discipline/system]
  .sheet_number          → Drawing sheet number
  .as_built_status       → not_started/in_progress/submitted/approved
  .current_revision      → Latest revision
  .discipline            → Drawing discipline
```

### Chain Logic
```
Forward chain (closeout item needs quality and drawing verification):
  System "HVAC" closeout (completion: 85%)
    → Commissioning tests: 12 of 14 complete (2 pending)
    → Punch items: 3 open HVAC items
    → As-built drawings: M1.1-M3.2 (8 sheets) — 6 submitted, 2 in progress
    → O&M manuals: Submitted, under review
    → Warranties: AHU-1 through AHU-4 received; VAV boxes pending

Reverse chain (quality issue blocks closeout):
  System test failure: "AHU-3 airflow balancing — 15% below design"
    → Closeout blocked: commissioning_status remains "in_progress"
    → Punch item created: PUNCH-089 (HVAC balancing deficiency)
    → As-built impact: M2.3 diffuser schedule may need revision
```

### Output Format
```
CLOSEOUT STATUS — HVAC System
  Completion: 85%
  Commissioning: 12/14 tests complete (2 pending: AHU-3 balancing, VAV zone 4)
  Quality Records:
    Test results: 12 pass, 0 fail, 2 pending
    Deficiencies: 1 open (AHU-3 airflow — 15% below design)
  Punch Items: 3 open (2 minor, 1 major)
  As-Built Drawings: 6/8 sheets submitted (M2.3, M3.1 in progress)
  O&M Manuals: Submitted — under review
  Warranties: 4/6 received (VAV boxes, exhaust fans pending)
  Training: Scheduled 2026-03-15
```

### Consuming Skills
`closeout-commissioning`, `quality-management`, `drawing-control`, `punch-list`, `/weekly-report`

---

## Pattern 12: Annotation → Drawing → RFI

**Trigger:** A document annotation or markup is created, reviewed, or discussed. Also triggered when a drawing revision or RFI response references annotations or markups.

**Purpose:** Link document annotations and markups to the drawing sheets they reference and any RFIs generated from annotation review, creating a complete trail from field observation to design clarification.

### Files to Read
1. `annotation-log.json` → `annotations[]` — match annotation by ID, document, or author
2. `drawing-log.json` → `drawings[]` — match by `document_id` (sheet number)
3. `rfi-log.json` → `rfis[]` — match by linked annotation or drawing reference
4. `plans-spatial.json` → `sheet_cross_references` — drawing context

### Fields to Extract
```
annotation-log.json → annotations[match]
  .annotation_id     → Annotation identifier (ANN-NNN)
  .document_id       → Sheet number or document reference
  .document_type     → plans/specs/submittals/rfis
  .annotation_type   → comment/markup/revision_cloud/dimension_override
  .description       → Annotation content
  .author            → Who created it
  .assigned_to       → Who needs to respond
  .date_created      → When created
  .status            → open/in_review/pending_response/resolved/closed
  .priority          → low/medium/high/critical
  .linked_rfi_id     → RFI generated from this annotation

drawing-log.json → drawings[match by document_id]
  .sheet_number      → Sheet identifier
  .title             → Drawing title
  .discipline        → Architectural/Structural/MEP
  .current_revision  → Latest revision
  .as_built_status   → As-built markup status

rfi-log.json → rfis[match by linked_annotation or drawing reference]
  .rfi_number        → RFI identifier
  .subject           → RFI topic
  .status            → Current status
  .response_text     → Architect's response
  .schedule_impact   → Impact assessment
```

### Chain Logic
```
Forward chain (annotation generates RFI):
  ANN-045 markup on S2.1: "Column size at D-4 conflicts with architectural"
    → Drawing: S2.1 (Foundation Plan, Rev 3, Structural)
    → Status: open, assigned to Structural Engineer
    → RFI generated: RFI-028 "Verify column size at Grid D-4"
    → RFI response pending → annotation remains open

Reverse chain (RFI response resolves annotation):
  RFI-028 resolved: "Column to remain per structural — arch plan revised"
    → ANN-045 status updated to "resolved"
    → Drawing S2.1 revision triggered (Rev 4)
    → Architectural plan A2.1 also revised
    → Distribution: annotation author notified of resolution
```

### Output Format
```
ANNOTATION-DRAWING-RFI CHAIN — ANN-045
  Annotation: "Column size at D-4 conflicts with architectural" (markup)
  Document: S2.1 — Foundation Plan (Structural, Rev 3)
  Author: J. Martinez (Superintendent)
  Assigned To: Structural Engineer
  Status: Open — pending response (12 days)
  RFI Generated: RFI-028 "Verify column size at Grid D-4" (issued 2026-02-12)
  RFI Status: Under review by architect
  Impact: Potential revision to S2.1 and A2.1 if column size changes
```

### Consuming Skills
`drawing-control`, `rfi-preparer`, `document-intelligence`, `/morning-brief`

---

## Pattern Usage Guidelines

1. **Always check if project intelligence is loaded** before attempting cross-references. If `plans-spatial.json` or `specs-quality.json` is empty, skip enrichment and note the gap.

2. **Cascade resolution** — start with the most specific identifier (room number, sub name, element mark) and cascade outward to gather related context.

3. **Never block on missing data** — if a cross-reference target doesn't exist (e.g., sub not in directory), proceed with available data and flag the gap.

4. **Source attribution** — when presenting cross-referenced data, always note which file and field the data came from so the superintendent can verify.

5. **Freshness awareness** — data may be stale if documents haven't been reprocessed recently. Note `documents_loaded.date_loaded` to assess data freshness.
