# As-Built Drawings — Deep Extraction Guide

Extract structured data from as-built (record) drawings that document actual field conditions versus original design. As-builts are critical closeout deliverables showing exactly what was installed, where deviations occurred, and what is concealed behind walls, underground, or above ceilings. This guide covers deviation detection, system routing updates, final fixture locations, concealed conditions, and code compliance notes.

---

## Extraction Priority Matrix

| Priority | Data Type | Use Case | Completeness Target |
|----------|-----------|----------|-------------------|
| **CRITICAL** | Deviations from design (location, size, routing changes) | Owner maintenance, future renovations, liability | 100% — every deviation |
| **CRITICAL** | Underground utility routing (actual vs. designed) | Future excavation safety, utility locates | 100% — all buried utilities |
| **CRITICAL** | Concealed structural modifications | Structural integrity for future modifications | 100% |
| **HIGH** | MEP routing (actual pipe/duct/conduit paths) | Maintenance access, future tenant improvements | All main runs |
| **HIGH** | Final fixture/equipment locations | O&M, replacement, service access | All permanent equipment |
| **HIGH** | Fire-rated assembly deviations | Code compliance verification | All fire-rated elements |
| **MEDIUM** | Dimensional changes (room sizes, openings) | Space planning, furniture layout | If significant (>2" change) |
| **MEDIUM** | Finish material substitutions | Maintenance/replacement matching | All approved substitutions |
| **LOW** | Minor field adjustments (±1" typical) | Reference only | Note existence |

---

## DOCUMENT IDENTIFICATION

### Signals this is an as-built drawing set

- Drawings stamped "AS-BUILT", "RECORD DRAWING", or "AS-CONSTRUCTED"
- Red-line markups on original design drawings (traditional method)
- Cloud or revision marks highlighting deviations
- Field measurement notations (actual dimensions alongside design dimensions)
- Updated title block with "As-Built" designation and date
- Signatures from superintendent, subcontractor foremen, and/or engineer
- Notes referencing field conditions, RFIs, or change orders that caused deviations
- Separate from original conformance set — later issue date

### As-Built vs. Record Drawing

| Term | Definition | Who Prepares |
|------|-----------|-------------|
| **As-Built** | Contractor's marked-up field drawings showing actual conditions | GC superintendent + subs |
| **Record Drawing** | Architect/engineer's cleaned-up version incorporating as-built data | A/E firm |

Both serve the same purpose for extraction. Record drawings are cleaner but may arrive later.

---

## DEVIATION DETECTION

The primary value of as-built extraction is identifying WHERE actual construction differs from design.

### Extraction Targets — Per Deviation

| Data Point | Type | Example |
|-----------|------|---------|
| `deviation_id` | string | "DEV-001" |
| `sheet_number` | string | "S-1.1" |
| `discipline` | string | "Structural" |
| `location` | string | "Grid C/3, Foundation" |
| `grid_reference` | string | "C-3" |
| `floor_level` | string | "Foundation" |
| `element_type` | string | "Footing" |
| `design_value` | string | "Footing F-3: 4'-0\" × 4'-0\" × 12\" deep" |
| `actual_value` | string | "Footing F-3: 4'-6\" × 4'-6\" × 14\" deep" |
| `deviation_description` | string | "Footing enlarged per RFI-012 due to soft soil at bearing elevation" |
| `deviation_type` | string | "enlargement" |
| `cause` | string | "RFI-012 — field condition (soft soil)" |
| `authorized_by` | string | "Structural engineer, per RFI-012 response" |
| `change_order` | string | "CO-003" |
| `cost_impact` | string | "+$2,400 (additional concrete and rebar)" |
| `schedule_impact` | string | "None — absorbed in float" |
| `concealed` | boolean | true |

### Deviation Types

| Type | Description | Examples |
|------|-------------|---------|
| `relocation` | Element moved from designed position | Equipment shifted for clearance, wall moved for code |
| `enlargement` | Element made larger than designed | Footing enlarged for bearing, duct upsized for CFM |
| `reduction` | Element made smaller than designed | Opening reduced for structural, pipe downsized |
| `reroute` | Linear element path changed | Duct rerouted around beam, pipe rerouted for clearance |
| `addition` | Element added not on original plans | Added cleanout, added junction box, added support |
| `deletion` | Element on plans but not installed | Deleted door, deleted fixture, abandoned in place |
| `substitution` | Different product/material installed | Different manufacturer, different material type |
| `elevation_change` | Vertical position differs from design | Pipe invert changed, equipment height adjusted |
| `field_condition` | Design changed due to discovered condition | Rock encountered, existing utilities found |

---

## SYSTEM ROUTING UPDATES

### Underground Utilities

**CRITICAL for future safety** — accurate underground routing prevents utility strikes during future work.

| Data Point | Type | Example |
|-----------|------|---------|
| `system` | string | "Storm sewer" |
| `segment_id` | string | "SS-MH1-to-MH2" |
| `design_route` | string | "Straight run, 15' west of building" |
| `actual_route` | string | "Offset 3' east due to rock encountered at Sta 2+50" |
| `pipe_size` | string | "12\" HDPE" |
| `pipe_material` | string | "HDPE (changed from RCP per CO-005)" |
| `design_invert_upstream` | string | "98.50'" |
| `actual_invert_upstream` | string | "98.75'" |
| `design_invert_downstream` | string | "97.80'" |
| `actual_invert_downstream` | string | "97.95'" |
| `design_slope` | string | "0.70%" |
| `actual_slope` | string | "0.80%" |
| `depth_of_cover` | string | "4'-2\" (design: 4'-0\")" |
| `as_built_coordinates` | string | "GPS: N 38.2451, W 85.7612 at MH-1" |
| `deviation_notes` | string | "Rock ledge at 4' depth required reroute" |

### Above-Ceiling MEP Routing

| Data Point | Type | Example |
|-----------|------|---------|
| `system` | string | "Supply duct from RTU-1" |
| `design_routing` | string | "East-west along Grid 3, then north to diffusers" |
| `actual_routing` | string | "Shifted 18\" south to clear structural beam at Grid C/3" |
| `size` | string | "24\" × 12\" rectangular" |
| `elevation` | string | "10'-6\" AFF to bottom of duct (design: 10'-8\")" |
| `access_points` | array | ["Access panel at Grid C/3", "Access panel at Grid D/3"] |
| `deviation_reason` | string | "Beam depth greater than shown on structural — coordination conflict" |

### Conduit and Electrical Routing

| Data Point | Type | Example |
|-----------|------|---------|
| `circuit_or_system` | string | "Panel LP-1 feeder, 4\" EMT" |
| `design_path` | string | "Vertical in wall at Grid B/2, horizontal in ceiling to panel" |
| `actual_path` | string | "Rerouted around mechanical equipment in ceiling space" |
| `conduit_size` | string | "4\" EMT" |
| `pull_box_locations` | array | ["Added pull box at Grid C/2 (not on design)"] |
| `junction_box_locations` | array | ["JB at ceiling, Grid B-C/2 (added for routing)"] |

---

## FINAL FIXTURE AND EQUIPMENT LOCATIONS

### Extraction Targets

For every permanent fixture and equipment item, extract actual installed location:

| Data Point | Type | Example |
|-----------|------|---------|
| `equipment_tag` | string | "RTU-1" |
| `design_location` | string | "Roof, Grid C-D/3-4 center" |
| `actual_location` | string | "Roof, Grid C-D/3-4, shifted 2' east for curb clearance" |
| `mounting` | string | "Roof curb, 14\" high" |
| `access_path` | string | "Roof hatch at Grid E/5, walk path along east parapet" |
| `service_clearances` | string | "36\" clear on all sides (verified)" |
| `electrical_disconnect` | string | "Disconnect on north side, 6' from unit" |
| `control_wiring` | string | "BACnet trunk via conduit to mech room" |

### Equipment Categories to Extract

- **HVAC**: RTUs, AHUs, exhaust fans, split systems, VRF units — roof or mech room locations
- **Electrical**: Panels, switchboards, transformers, disconnect switches, generators
- **Plumbing**: Water heaters, pumps, backflow preventers, grease interceptors, roof drains
- **Fire protection**: Fire alarm panel, FDC, standpipe connections, sprinkler riser
- **Specialty**: Elevator machine room equipment, security panels, AV equipment
- **Site**: Light poles, transformers, fire hydrants, backflow, meters, manholes

---

## CONCEALED CONDITIONS

### What to Extract

Items that are buried, enclosed, or otherwise hidden from view after construction:

| Data Point | Type | Example |
|-----------|------|---------|
| `condition_id` | string | "CC-001" |
| `location` | string | "Foundation at Grid A/1" |
| `description` | string | "Existing abandoned fuel oil tank found during excavation" |
| `disposition` | string | "Tank removed and disposed per environmental protocol" |
| `documentation` | string | "Environmental closure report dated 2026-03-15" |
| `differs_from_design` | boolean | true |
| `impact` | string | "Footing F-1 relocated 3' north per RFI-008" |
| `photos` | array | ["Photo 2026-02-10_tank_discovery.jpg"] |
| `concealment_date` | string | "2026-03-20" |

### Common Concealed Conditions

| Category | Examples | Why It Matters |
|----------|---------|----------------|
| **Underground utilities** | Abandoned pipes, unknown cables, old foundations | Future excavation safety |
| **Soil conditions** | Rock, contaminated soil, high water table | Future foundation work |
| **Structural modifications** | Added reinforcement, field-welded connections | Future structural changes |
| **In-wall MEP** | Rerouted pipes/conduit, added backing, fire stopping | Future renovation access |
| **Above-ceiling** | Rerouted ducts, added supports, fire damper locations | Future tenant improvement |
| **Below-slab** | Underslab plumbing, vapor barrier condition, radon piping | Future slab penetrations |

---

## CODE COMPLIANCE NOTES

### Extraction Targets

Capture all code-related field changes:

| Data Point | Type | Example |
|-----------|------|---------|
| `code_note_id` | string | "CN-001" |
| `code_reference` | string | "IBC 1020.1" |
| `description` | string | "Exit corridor width increased from 44\" to 48\" per inspector direction" |
| `inspector` | string | "Building Official, inspection dated 2026-04-10" |
| `drawings_affected` | array | ["A-101", "A-102"] |
| `deviation_from_design` | string | "Corridor C widened 4\" — wall at Grid D/3 shifted" |
| `impact_on_other_systems` | string | "MEP in corridor ceiling shifted to match new wall location" |

---

## OUTPUT MAPPING

### For plans-spatial.json → as_built_overlay

```json
{
  "as_built_overlay": {
    "as_built_date": "2026-08-01",
    "prepared_by": "Smith Construction, Superintendent: John Doe",
    "total_deviations": 23,
    "deviations": [
      {
        "deviation_id": "DEV-001",
        "sheet": "S-1.1",
        "discipline": "Structural",
        "location": "Grid C/3, Foundation",
        "element": "Footing F-3",
        "design_value": "4'-0\" × 4'-0\" × 12\" deep",
        "actual_value": "4'-6\" × 4'-6\" × 14\" deep",
        "type": "enlargement",
        "cause": "RFI-012 — soft soil",
        "authorized_by": "Structural engineer",
        "change_order": "CO-003",
        "concealed": true
      }
    ],
    "routing_updates": [
      {
        "system": "Storm sewer",
        "segment": "SS-MH1-to-MH2",
        "deviation": "Offset 3' east due to rock",
        "actual_inverts": {"upstream": "98.75'", "downstream": "97.95'"},
        "actual_material": "HDPE (changed from RCP)",
        "change_order": "CO-005"
      }
    ],
    "concealed_conditions": [
      {
        "id": "CC-001",
        "location": "Grid A/1",
        "description": "Abandoned fuel oil tank removed",
        "documentation": "Environmental closure report 2026-03-15"
      }
    ],
    "code_compliance_notes": [
      {
        "id": "CN-001",
        "code": "IBC 1020.1",
        "description": "Exit corridor widened per inspector",
        "sheets_affected": ["A-101", "A-102"]
      }
    ]
  }
}
```

### For drawing-log.json → as-built tracking

```json
{
  "as_built_status": [
    {
      "sheet_number": "S-1.1",
      "discipline": "Structural",
      "title": "Foundation Plan",
      "as_built_markup": "complete",
      "deviations_count": 3,
      "markup_by": "Superintendent",
      "markup_date": "2026-07-15",
      "reviewed_by": "Structural Engineer",
      "review_date": "2026-07-20"
    }
  ]
}
```

---

## CROSS-REFERENCE RULES

| As-Built Data | Cross-Reference Against | Purpose |
|--------------|------------------------|---------|
| Deviations with RFI reference | `rfi-log.json` | Link deviation to RFI decision |
| Deviations with CO reference | `change-order-log.json` | Link to cost/schedule impact |
| Underground routing | `plans-spatial.json` → site_utilities | Update actual utility locations |
| Equipment locations | MEP equipment schedules | Verify all equipment accounted for |
| Concealed conditions | `daily-report-data.json` | Link to discovery date and documentation |
| Code notes | `inspection-log.json` | Link to inspector-directed changes |
| Routing changes | `quality-data.json` → inspections | Verify changed routing was inspected |

---

## AS-BUILT COMPLETENESS TRACKING

### Per-Discipline Checklist

```
AS-BUILT MARKUP STATUS

| Discipline | Sheets | Marked Up | Reviewed | Complete |
|-----------|--------|-----------|----------|----------|
| Civil (C) | 8 | 8 | 6 | 75% |
| Architectural (A) | 15 | 12 | 8 | 53% |
| Structural (S) | 10 | 10 | 10 | 100% |
| Mechanical (M) | 12 | 8 | 4 | 33% |
| Electrical (E) | 10 | 6 | 2 | 20% |
| Plumbing (P) | 8 | 5 | 2 | 25% |
| Fire Protection (FP) | 4 | 2 | 0 | 0% |
| TOTAL | 67 | 51 | 32 | 48% |
```

### As-Built Quality Standards

Each marked-up sheet should include:
- [ ] All deviations clearly marked with cloud or callout
- [ ] Actual dimensions noted alongside design dimensions
- [ ] RFI/CO references noted for each change
- [ ] Date of as-built markup
- [ ] Signature of responsible party (sub foreman or superintendent)
- [ ] Concealed items photographed before cover-up
- [ ] Underground items located with GPS or offset measurements
- [ ] Equipment access paths and service clearances documented

---

## SUMMARY CHECKLIST — AS-BUILT EXTRACTION

**On Receipt of As-Built Drawing Set**:

- [ ] **Identify discipline** (Civil, Arch, Struct, Mech, Elec, Plumb, FP)
- [ ] **Scan for deviation markups** — clouds, red-lines, callouts
- [ ] **Extract each deviation** with design vs. actual values
- [ ] **Link deviations** to RFIs and change orders
- [ ] **Extract routing updates** for all underground and concealed systems
- [ ] **Extract final equipment locations** with actual coordinates/grid refs
- [ ] **Document concealed conditions** with disposition and photos
- [ ] **Capture code compliance notes** from inspector-directed changes
- [ ] **Store deviations** in `plans-spatial.json` → as_built_overlay
- [ ] **Update drawing-log.json** with as-built completion status
- [ ] **Cross-reference** all deviations against related project records
- [ ] **Track completeness** by discipline — target 100% before closeout
