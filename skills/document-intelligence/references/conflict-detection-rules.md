---
name: conflict-detection-rules
description: Codified cross-discipline conflict detection patterns for identifying discrepancies across construction documents — plans vs specs, specs vs schedule, drawing vs drawing, cost vs scope, and dual-source conflicts. Consumed by the conflict-detection-agent, doc-orchestrator, and data-integrity-watchdog.
version: 1.0.0
---

# Conflict Detection Rules

This document defines the complete framework for automated cross-discipline conflict detection across the project intelligence data store. All conflict categories, detection rules, severity classifications, and resolution workflows are consumed by the **conflict-detection-agent**, **doc-orchestrator**, and **data-integrity-watchdog** to identify discrepancies, flag inconsistencies, and recommend resolutions.

---

## 1. Conflict Categories

Eight categories cover the full range of cross-document discrepancies encountered on construction projects. Each category identifies the two data sources being compared and the types of conflicts that arise between them.

| # | Category | Source A (JSON File + Field Path) | Source B (JSON File + Field Path) | Example Conflicts |
|---|----------|-----------------------------------|-----------------------------------|-------------------|
| 1 | **Dimensional** | `plans-spatial.json` → `quantities.rooms[].area_sf`, `room_schedule[].dimensions` | `specs-quality.json` → `spec_sections[].tolerances`, `weather_thresholds[]` | Room 107 plan shows 12'-6" width but finish schedule calculated for 12'-0" |
| 2 | **Material** | `plans-spatial.json` → `material_zones[].material_type`, `material_zones[].hatch_pattern` | `specs-quality.json` → `spec_sections[].key_req`, `key_materials[].specification` | Plan hatch indicates VCT but spec Section 09 65 00 calls for ceramic tile |
| 3 | **Equipment Capacity** | `plans-spatial.json` → `mep_systems.mechanical.equipment[].cooling.tons`, `mep_systems.mechanical.equipment[].tag` | `specs-quality.json` → `spec_sections[].key_req` (equipment requirements) | Plan shows 5-ton RTU but spec Section 23 requires 7.5-ton minimum |
| 4 | **Pipe/Duct Sizing** | `plans-spatial.json` → `mep_systems.pipe_sizes[].size`, `mep_systems.duct_sizes[].size` | `specs-quality.json` → `spec_sections[].key_req` (sizing requirements) OR DXF attributes via `dwg-extraction` | Plan note says 8" storm, DXF attribute says 6" PVC |
| 5 | **Schedule vs. Specification** | `schedule.json` → `milestones[].date`, `critical_path[].duration`, `lookahead_history[]` | `specs-quality.json` → `spec_sections[].testing`, `weather_thresholds[].min_temp`, `hold_points[].trigger` | Spec requires 28-day concrete cure but schedule shows 14-day activity |
| 6 | **Cost vs. Scope** | `cost-data.json` → `budget_by_division[].current_amount`, `sov_lines[].scheduled_value` | `plans-spatial.json` → `quantities.concrete[].volume_cy`, `quantities.rooms[].area_sf` + `directory.json` → `subcontractors[].scope` | Budget has 100 CY concrete but plans calculate to 145 CY |
| 7 | **Drawing vs. Drawing** | `plans-spatial.json` → sheet A data (e.g., `sheet_cross_references.drawing_index[]` discipline "A") | `plans-spatial.json` → sheet B data (e.g., `sheet_cross_references.drawing_index[]` discipline "S") | Architectural plan shows door at 3'-0" wide, structural opening is 2'-10" |
| 8 | **Dual-Source** | `plans-spatial.json` → entries with `source: "claude_vision"` (visual extraction) | `plans-spatial.json` → entries with `source: "dxf"` (DXF extraction) | Visual extraction measures pipe at 8", DXF XDATA says 6" |

---

## 2. Detection Rules

Each rule defines a specific comparison between two data sources, the logic for detecting a conflict, the acceptable tolerance, severity level, and downstream impact. Rules are grouped by conflict category.

---

### Dimensional (CDR-01 through CDR-04)

#### CDR-01: Room Dimension Plan vs. Finish Schedule Area

- **Category:** Dimensional
- **Description:** Compares room dimensions extracted from the floor plan against room areas implied by the finish schedule. Catches rooms where plan dimensions and finish material quantities do not agree.
- **Source A:** `plans-spatial.json` → `quantities.rooms[].area_sf` (plan-derived room area)
- **Source B:** `plans-spatial.json` → `room_schedule[].finish_schedule.floor_area` OR `specs-quality.json` → finish schedule area calculations
- **Comparison Logic:**
  ```
  FOR each room IN plans-spatial.json.quantities.rooms[]:
    plan_area = room.area_sf
    finish_area = room_schedule[room.room_number].finish_schedule.floor_area
    IF finish_area EXISTS:
      variance_pct = abs(plan_area - finish_area) / plan_area * 100
      IF variance_pct > 5:
        FLAG conflict CDR-01
        RECORD plan_area, finish_area, variance_pct, room_number
  ```
- **Tolerance:** +/- 5% or +/- 10 SF (whichever is greater)
- **Severity:** MINOR if variance 5-10%; MAJOR if variance >10%; CRITICAL if room is >500 SF and variance >15%
- **Downstream Impact:** `cost-tracking` (material quantities), `punch-list` (finish verification), `quantitative-intelligence` (area calculations)

#### CDR-02: Door Width Plan vs. Structural Opening

- **Category:** Dimensional
- **Description:** Compares door widths shown on the architectural plan against structural opening dimensions. A common clash where the structural opening is too narrow for the specified door.
- **Source A:** `plans-spatial.json` → `sheet_cross_references.schedule_references[]` (door schedule: door width) or `door_schedule[].width`
- **Source B:** `plans-spatial.json` → structural sheet dimensions for the same opening location
- **Comparison Logic:**
  ```
  FOR each door IN plans-spatial.json.door_schedule[]:
    arch_width = door.width
    struct_opening = structural_openings[match by grid/location].clear_width
    IF struct_opening EXISTS:
      delta = struct_opening - arch_width
      IF delta < 2:  # Less than 2" clearance for frame
        FLAG conflict CDR-02
        RECORD door.mark, arch_width, struct_opening, delta, location
  ```
- **Tolerance:** Structural opening must be at least 2" wider than door leaf (frame allowance)
- **Severity:** CRITICAL — door cannot be installed if opening is undersized; affects ADA compliance for accessible routes
- **Downstream Impact:** `punch-list` (door installation verification), `rfi-preparer` (design clarification), `change-order-tracker` (structural modification cost), `inspection-tracker` (ADA compliance)

#### CDR-03: Ceiling Height Plan vs. RCP vs. Section

- **Category:** Dimensional
- **Description:** Cross-checks ceiling heights shown on the floor plan finish schedule, the reflected ceiling plan (RCP), and building section views. Three independent sources should agree.
- **Source A:** `plans-spatial.json` → `room_schedule[].finish_schedule.ceiling_height` (from floor plan)
- **Source B:** `plans-spatial.json` → `ceiling_plan.rooms[].ceiling_height` (from RCP) AND section view heights
- **Comparison Logic:**
  ```
  FOR each room IN plans-spatial.json.room_schedule[]:
    plan_height = room.finish_schedule.ceiling_height
    rcp_height = ceiling_plan.rooms[room.room_number].ceiling_height
    section_height = sections[match by room location].ceiling_height
    heights = [plan_height, rcp_height, section_height].filter(EXISTS)
    IF len(heights) >= 2:
      max_delta = max(heights) - min(heights)
      IF max_delta > 1:  # Greater than 1" discrepancy
        FLAG conflict CDR-03
        RECORD room_number, plan_height, rcp_height, section_height, max_delta
  ```
- **Tolerance:** +/- 1" between sources
- **Severity:** MINOR if delta 1-3"; MAJOR if delta >3" (affects ductwork routing, fire sprinkler coverage, ADA clearances)
- **Downstream Impact:** `inspection-tracker` (fire sprinkler head coverage), `cost-tracking` (wall finish quantities), `quantitative-intelligence` (wall area calculations)

#### CDR-04: Building Footprint Plan vs. Site Plan

- **Category:** Dimensional
- **Description:** Verifies that the building footprint dimensions on the architectural floor plan match the building outline shown on the civil/site plan. Discrepancies indicate a coordination failure between disciplines.
- **Source A:** `plans-spatial.json` → `quantities.rooms[]` (aggregate building footprint area) or architectural plan overall dimensions
- **Source B:** `plans-spatial.json` → civil site plan building footprint dimensions
- **Comparison Logic:**
  ```
  FOR building_footprint:
    arch_footprint_sf = SUM(plans-spatial.json.quantities.rooms[floor="Level 1"].area_sf) + wall_thickness_allowance
    site_footprint_sf = civil_site_plan.building_outline.area_sf
    IF both EXISTS:
      variance_pct = abs(arch_footprint_sf - site_footprint_sf) / arch_footprint_sf * 100
      IF variance_pct > 2:
        FLAG conflict CDR-04
        RECORD arch_footprint_sf, site_footprint_sf, variance_pct
  ```
- **Tolerance:** +/- 2% or +/- 50 SF (whichever is greater)
- **Severity:** MAJOR — affects setback compliance, grading, and paving quantities; CRITICAL if setback violation results
- **Downstream Impact:** `cost-tracking` (site work quantities), `inspection-tracker` (setback verification), `safety-management` (site logistics)

---

### Material (CDR-05 through CDR-07)

#### CDR-05: Plan Hatch Material vs. Spec Section Material

- **Category:** Material
- **Description:** Compares the material type identified by hatch patterns on plan drawings against the material specified in the governing spec section. Catches drawings that show one material while the spec requires another.
- **Source A:** `plans-spatial.json` → `material_zones[].material_type`, `material_zones[].hatch_pattern`, `material_zones[].material_label`
- **Source B:** `specs-quality.json` → `spec_sections[match by division].key_req`, `key_materials[].specification`
- **Comparison Logic:**
  ```
  FOR each zone IN plans-spatial.json.material_zones[]:
    plan_material = zone.material_type  # e.g., "concrete", "steel", "insulation"
    plan_label = zone.material_label     # e.g., "VCT", "Ceramic Tile"
    spec_section = specs-quality.json.spec_sections[match by CSI division for material]
    spec_material = spec_section.key_req  # e.g., "Ceramic tile per ANSI A137.1"
    IF plan_label != "" AND spec_material != "":
      IF normalize(plan_label) != normalize(spec_material):
        FLAG conflict CDR-05
        RECORD zone.zone_id, zone.sheet, plan_label, spec_section.section, spec_material
  ```
- **Tolerance:** None — material type must match exactly (after normalization for abbreviations)
- **Severity:** MAJOR — wrong material installed requires removal and replacement; CRITICAL if structural or fire-rated material
- **Downstream Impact:** `cost-tracking` (material cost), `procurement-log` (ordering), `punch-list` (material verification), `submittal-intelligence` (submittal spec compliance)

#### CDR-06: Finish Schedule Material vs. Spec Section Requirements

- **Category:** Material
- **Description:** Compares materials listed in the architectural finish schedule (floor, wall, ceiling finishes per room) against specification requirements for those materials. Catches finish schedules that reference a material type the spec does not permit.
- **Source A:** `plans-spatial.json` → `room_schedule[].finish_schedule` (floor_finish, wall_finish, base, ceiling_type)
- **Source B:** `specs-quality.json` → `spec_sections[match by CSI section].key_req`, `spec_sections[].submittal_required`
- **Comparison Logic:**
  ```
  FOR each room IN plans-spatial.json.room_schedule[]:
    FOR each finish_type IN [floor_finish, wall_finish, base, ceiling_type]:
      schedule_material = room.finish_schedule[finish_type]
      spec_section = find_spec_section(schedule_material)  # Map material to CSI section
      IF spec_section EXISTS:
        IF spec_section.key_req does NOT permit schedule_material:
          FLAG conflict CDR-06
          RECORD room.room_number, finish_type, schedule_material, spec_section.section, spec_section.key_req
  ```
- **Tolerance:** None — finish material must be a type permitted by the governing spec section
- **Severity:** MAJOR — finish non-compliance requires rework; MINOR if cosmetic difference within same product family
- **Downstream Impact:** `cost-tracking` (finish material costs), `submittal-intelligence` (submittal requirements), `punch-list` (finish verification)

#### CDR-07: Structural Concrete Strength Plan Notes vs. Spec

- **Category:** Material
- **Description:** Compares concrete compressive strength (f'c) values shown in structural plan notes or mix design callouts against specification requirements in the concrete spec section.
- **Source A:** `plans-spatial.json` → structural general notes (f'c values per element type) or `quantities.concrete[].notes`
- **Source B:** `specs-quality.json` → `mix_designs[].design_fc`, `spec_sections[division="03"].key_req`
- **Comparison Logic:**
  ```
  FOR each concrete_element IN plans-spatial.json.quantities.concrete[]:
    plan_fc = parse_fc_from_notes(concrete_element.notes)  # e.g., 4000 PSI
    spec_fc = specs-quality.json.mix_designs[match by element type].design_fc
    IF plan_fc != spec_fc:
      FLAG conflict CDR-07
      RECORD element, plan_fc, spec_fc, difference
    IF plan_fc < spec_fc:
      ESCALATE severity to CRITICAL  # Under-strength concrete is structural
  ```
- **Tolerance:** Plan f'c must equal or exceed spec f'c; no negative tolerance permitted
- **Severity:** CRITICAL if plan f'c < spec f'c (structural adequacy concern); MINOR if plan f'c > spec f'c (overdesign, cost impact only)
- **Downstream Impact:** `inspection-tracker` (concrete testing requirements), `cost-tracking` (mix design cost), `intake-chatbot` (pour day verification), `quality-management` (break test thresholds)

---

### Equipment (CDR-08 through CDR-10)

#### CDR-08: HVAC Equipment Capacity Plan vs. Spec Minimum

- **Category:** Equipment Capacity
- **Description:** Compares HVAC equipment capacity shown on mechanical plans (tonnage, MBH, CFM) against minimum capacity requirements in the mechanical specification.
- **Source A:** `plans-spatial.json` → `mep_systems.mechanical.equipment[].cooling.tons`, `mep_systems.mechanical.equipment[].heating.mbh`, `mep_systems.mechanical.equipment[].airflow.cfm`
- **Source B:** `specs-quality.json` → `spec_sections[division="23"].key_req` (minimum equipment capacity requirements)
- **Comparison Logic:**
  ```
  FOR each unit IN plans-spatial.json.mep_systems.mechanical.equipment[]:
    plan_tons = unit.cooling.tons
    plan_mbh = unit.heating.mbh
    plan_cfm = unit.airflow.cfm
    spec_req = specs-quality.json.spec_sections[match "23" or unit type].key_req
    spec_min_tons = parse_min_capacity(spec_req, "cooling")
    spec_min_cfm = parse_min_capacity(spec_req, "airflow")
    IF plan_tons < spec_min_tons:
      FLAG conflict CDR-08
      RECORD unit.tag, "cooling", plan_tons, spec_min_tons
    IF plan_cfm < spec_min_cfm:
      FLAG conflict CDR-08
      RECORD unit.tag, "airflow", plan_cfm, spec_min_cfm
  ```
- **Tolerance:** Plan capacity must meet or exceed spec minimum; deficit of >15% is CRITICAL
- **Severity:** MAJOR if deficit 1-15%; CRITICAL if deficit >15% (occupant comfort and code compliance)
- **Downstream Impact:** `cost-tracking` (equipment cost), `submittal-intelligence` (equipment submittal), `change-order-tracker` (equipment upgrade cost), `inspection-tracker` (commissioning/TAB)

#### CDR-09: Electrical Panel Main Breaker vs. Connected Load

- **Category:** Equipment Capacity
- **Description:** Verifies that the panel main breaker rating is adequate for the connected load shown in the panel schedule. An overloaded panel is a code violation and fire hazard.
- **Source A:** `plans-spatial.json` → `mep_systems.electrical.panel_schedules[].main_breaker_amps`, `mep_systems.electrical.panel_schedules[].bus_rating_amps`
- **Source B:** `plans-spatial.json` → `mep_systems.electrical.panel_schedules[].totals.demand_va` (calculated demand load)
- **Comparison Logic:**
  ```
  FOR each panel IN plans-spatial.json.mep_systems.electrical.panel_schedules[]:
    main_breaker_amps = panel.main_breaker_amps
    demand_va = panel.totals.demand_va
    panel_voltage = panel.voltage  # e.g., 208
    demand_amps = demand_va / (panel_voltage * sqrt(3))  # 3-phase
    load_pct = demand_amps / main_breaker_amps * 100
    IF load_pct > 80:  # NEC 80% continuous load limit
      FLAG conflict CDR-09
      RECORD panel.panel, main_breaker_amps, demand_amps, load_pct
    IF load_pct > 100:
      ESCALATE severity to CRITICAL
  ```
- **Tolerance:** Demand load must not exceed 80% of main breaker rating for continuous loads (NEC 210.20)
- **Severity:** MAJOR if load 80-100% of breaker; CRITICAL if load >100% (code violation, fire hazard)
- **Downstream Impact:** `inspection-tracker` (electrical rough-in inspection), `safety-management` (fire hazard), `change-order-tracker` (panel upgrade), `cost-tracking` (electrical costs)

#### CDR-10: Plumbing Fixture Count Plan vs. Code Minimum

- **Category:** Equipment Capacity
- **Description:** Verifies that plumbing fixture counts shown on plans meet or exceed building code minimum requirements based on occupancy type and occupant load.
- **Source A:** `plans-spatial.json` → `mep_systems.plumbing.fixtures[]` (fixture counts by type)
- **Source B:** `specs-quality.json` → code requirements derived from `spec_sections[division="22"].key_req` and building type from `project-config.json` → `project_basics.building_type`
- **Comparison Logic:**
  ```
  FOR each fixture_type IN [water_closet, lavatory, drinking_fountain]:
    plan_count = COUNT(plans-spatial.json.mep_systems.plumbing.fixtures[type=fixture_type])
    occupant_load = calculate_occupant_load(building_type, gross_sf)
    code_min = lookup_ipc_table(fixture_type, occupancy_type, occupant_load)
    IF plan_count < code_min:
      FLAG conflict CDR-10
      RECORD fixture_type, plan_count, code_min, occupant_load, deficit
  ```
- **Tolerance:** None — code minimums are absolute; plan count must equal or exceed code requirement
- **Severity:** CRITICAL — code violation; affects certificate of occupancy
- **Downstream Impact:** `inspection-tracker` (plumbing rough-in/final), `rfi-preparer` (code compliance RFI), `change-order-tracker` (additional fixture cost), `cost-tracking` (plumbing costs)

---

### Pipe/Duct (CDR-11 through CDR-13)

#### CDR-11: Pipe Size Drawing Notes vs. DXF Attributes

- **Category:** Pipe/Duct Sizing
- **Description:** Compares pipe sizes shown in drawing annotation notes (text-based extraction) against pipe sizes extracted from DXF block attributes (structured CAD data). A dual-source conflict specific to projects with DXF files.
- **Source A:** `plans-spatial.json` → `mep_systems.pipe_sizes[].size` (from drawing note extraction, source "claude_vision" or "notes")
- **Source B:** DXF extraction → pipe block ATTRIB data (from `dwg-extraction` pipeline, source "dxf")
- **Comparison Logic:**
  ```
  FOR each pipe_run IN plans-spatial.json.mep_systems.pipe_sizes[]:
    IF pipe_run has entries from BOTH sources:
      note_size = entries[source="notes" OR source="claude_vision"].size
      dxf_size = entries[source="dxf"].size
      IF normalize_pipe_size(note_size) != normalize_pipe_size(dxf_size):
        FLAG conflict CDR-11
        RECORD pipe_run.system, note_size, dxf_size, pipe_run.sheet
  ```
- **Tolerance:** None — pipe sizes must match exactly between sources
- **Severity:** MAJOR — incorrect pipe size affects flow capacity and pressure; CRITICAL if undersized on fire protection or storm systems
- **Downstream Impact:** `cost-tracking` (pipe material cost), `quantitative-intelligence` (pipe quantities), `safety-management` (fire protection adequacy), `inspection-tracker` (underground/rough-in)

#### CDR-12: Duct CFM at Diffusers vs. Equipment Total CFM

- **Category:** Pipe/Duct Sizing
- **Description:** Verifies that the sum of CFM values at all diffusers served by an HVAC unit does not exceed the unit's rated airflow capacity. An imbalanced system results in inadequate ventilation.
- **Source A:** `plans-spatial.json` → `mep_systems.mechanical.diffusers_grilles[]` (CFM per diffuser, grouped by serving unit)
- **Source B:** `plans-spatial.json` → `mep_systems.mechanical.equipment[].airflow.cfm` (unit total CFM)
- **Comparison Logic:**
  ```
  FOR each unit IN plans-spatial.json.mep_systems.mechanical.equipment[]:
    unit_cfm = unit.airflow.cfm
    diffuser_total_cfm = SUM(diffusers_grilles[served_by=unit.tag].cfm)
    IF diffuser_total_cfm > 0 AND unit_cfm > 0:
      balance_pct = diffuser_total_cfm / unit_cfm * 100
      IF balance_pct > 110:  # Diffusers demand more than unit can deliver
        FLAG conflict CDR-12 (over-subscribed)
        RECORD unit.tag, unit_cfm, diffuser_total_cfm, balance_pct
      IF balance_pct < 85:  # Significant unaccounted airflow
        FLAG conflict CDR-12 (under-subscribed — possible missing diffusers)
        RECORD unit.tag, unit_cfm, diffuser_total_cfm, balance_pct
  ```
- **Tolerance:** Diffuser total within 85-110% of equipment capacity
- **Severity:** MAJOR if balance outside 85-110%; CRITICAL if >125% (unit cannot deliver required airflow)
- **Downstream Impact:** `inspection-tracker` (TAB testing), `submittal-intelligence` (equipment submittal), `cost-tracking` (equipment sizing), `punch-list` (comfort complaints)

#### CDR-13: Storm Pipe Size vs. Watershed Calculations

- **Category:** Pipe/Duct Sizing
- **Description:** Compares storm drain pipe sizes shown on civil plans against required sizes based on watershed area and rainfall intensity calculations per the civil engineer's drainage design.
- **Source A:** `plans-spatial.json` → `site_utilities.storm[].size` (pipe size from plans)
- **Source B:** `specs-quality.json` → `spec_sections[division="33" OR section="33 40 00"].key_req` (drainage design criteria) and civil calculations
- **Comparison Logic:**
  ```
  FOR each storm_segment IN plans-spatial.json.site_utilities.storm[]:
    plan_size = storm_segment.size  # e.g., "8\""
    design_flow_cfs = storm_segment.design_flow  # If available from calculations
    required_size = lookup_pipe_capacity(plan_size, slope, material)
    IF required_size EXISTS AND pipe_capacity(plan_size) < design_flow_cfs:
      FLAG conflict CDR-13
      RECORD storm_segment, plan_size, required_size, design_flow_cfs
  ```
- **Tolerance:** Pipe capacity must meet or exceed design flow; no undersizing permitted
- **Severity:** CRITICAL — undersized storm drains cause flooding, erosion, and code violations
- **Downstream Impact:** `inspection-tracker` (underground utility inspection), `cost-tracking` (pipe material costs), `safety-management` (erosion control), `rfi-preparer` (civil design clarification)

---

### Schedule vs. Spec (CDR-14 through CDR-17)

#### CDR-14: Concrete Cure Duration vs. Spec Requirements

- **Category:** Schedule vs. Specification
- **Description:** Compares the duration allocated for concrete cure/strength gain activities in the schedule against cure time requirements in the concrete specification.
- **Source A:** `schedule.json` → `critical_path[]` or `milestones[]` (concrete pour to next-activity duration)
- **Source B:** `specs-quality.json` → `spec_sections[section matches "03 30 00"].key_req`, `mix_designs[].cold_weather_modification`
- **Comparison Logic:**
  ```
  FOR each concrete_activity IN schedule.json:
    IF activity.description contains "concrete" OR "pour" OR "slab":
      pour_date = activity.start_date
      next_loading_activity = find_successor(activity)
      cure_days = next_loading_activity.start_date - pour_date
      spec_cure_days = specs-quality.json.spec_sections["03 30 00"].cure_time  # e.g., 28 days
      IF cure_days < spec_cure_days:
        FLAG conflict CDR-14
        RECORD activity, cure_days, spec_cure_days, deficit_days
      IF cold_weather_period(pour_date):
        extended_cure = spec_cure_days * 1.5  # Cold weather typically extends cure
        IF cure_days < extended_cure:
          FLAG conflict CDR-14 (cold weather)
          RECORD activity, cure_days, extended_cure
  ```
- **Tolerance:** Schedule duration must meet or exceed spec cure time; no deficit permitted
- **Severity:** CRITICAL — loading concrete before adequate cure is a structural safety issue
- **Downstream Impact:** `inspection-tracker` (concrete testing and stripping), `delay-tracker` (schedule impact), `safety-management` (structural loading), `intake-chatbot` (pour day scheduling)

#### CDR-15: Submittal Review Period vs. Spec Timeline

- **Category:** Schedule vs. Specification
- **Description:** Verifies that the schedule allows adequate time for submittal review as required by the specification's General Conditions or individual spec sections.
- **Source A:** `schedule.json` → submittal-related activities or `long_lead_items[].lead_time`
- **Source B:** `specs-quality.json` → `spec_sections[section matches "01 33 00"].key_req` (submittal review period, typically 14-21 days) or `contract.documentation_requirements`
- **Comparison Logic:**
  ```
  FOR each submittal IN submittal-log.json:
    IF submittal.status IN ["submitted", "under_review"]:
      submit_date = submittal.date_submitted
      need_date = find_installation_activity(submittal.spec_section).start_date
      available_days = need_date - submit_date
      spec_review_period = specs-quality.json.spec_sections["01 33 00"].review_days  # e.g., 14 days
      procurement_lead = submittal.lead_time_weeks * 7
      total_required = spec_review_period + procurement_lead
      IF available_days < total_required:
        FLAG conflict CDR-15
        RECORD submittal.id, available_days, total_required, deficit_days
  ```
- **Tolerance:** Available time must meet or exceed spec review period plus procurement lead time
- **Severity:** MAJOR if deficit 1-14 days; CRITICAL if deficit >14 days or item is on critical path
- **Downstream Impact:** `submittal-intelligence` (submittal scheduling), `procurement-log` (ordering timeline), `look-ahead-planner` (constraint identification), `meeting-minutes` (action items)

#### CDR-16: Procurement Lead Time vs. Schedule Float

- **Category:** Schedule vs. Specification
- **Description:** Identifies procurement items where the remaining lead time exceeds the available schedule float, putting the activity and potentially the critical path at risk.
- **Source A:** `procurement-log.json` → `items[].expected_delivery`, `items[].delivery_status`
- **Source B:** `schedule.json` → `critical_path[].float_days`, `near_critical[].float_days`, activity start dates
- **Comparison Logic:**
  ```
  FOR each procurement_item IN procurement-log.json.items[]:
    IF procurement_item.delivery_status != "delivered":
      delivery_date = procurement_item.expected_delivery
      install_activity = schedule.json.activities[match by material dependency]
      activity_start = install_activity.start_date
      float_days = install_activity.float_days
      margin = activity_start - delivery_date  # Days between delivery and need
      IF margin < 0:  # Delivery after activity start
        FLAG conflict CDR-16
        RECORD procurement_item.id, delivery_date, activity_start, margin
      IF margin < 7 AND float_days < 5:
        FLAG conflict CDR-16 (tight margin, low float)
        RECORD procurement_item.id, margin, float_days
  ```
- **Tolerance:** Delivery must occur at least 7 days before activity start; tighter margins flagged if float <5 days
- **Severity:** MAJOR if margin 0-7 days; CRITICAL if delivery date is after activity start or item is on critical path
- **Downstream Impact:** `look-ahead-planner` (constraint identification), `delay-tracker` (potential delay), `cost-tracking` (expediting costs), `meeting-minutes` (coordination)

#### CDR-17: Testing/Inspection Duration vs. Schedule Allowance

- **Category:** Schedule vs. Specification
- **Description:** Verifies that the schedule provides adequate duration for required testing and inspection activities as defined in the specification hold points and testing requirements.
- **Source A:** `schedule.json` → testing/inspection activity durations
- **Source B:** `specs-quality.json` → `hold_points[].trigger`, `spec_sections[].testing` (required testing duration and frequency)
- **Comparison Logic:**
  ```
  FOR each hold_point IN specs-quality.json.hold_points[]:
    schedule_activity = schedule.json.activities[match by work_type]
    inspection_duration = hold_point.required_duration  # e.g., 2 days for soil compaction testing
    schedule_allowance = schedule_activity.inspection_duration_days
    IF schedule_allowance < inspection_duration:
      FLAG conflict CDR-17
      RECORD hold_point.inspection_name, schedule_allowance, inspection_duration
    # Also check for re-inspection contingency
    IF hold_point.fail_retest_days EXISTS:
      IF schedule_activity.float_days < hold_point.fail_retest_days:
        FLAG conflict CDR-17 (insufficient re-test contingency)
  ```
- **Tolerance:** Schedule must allow at least the spec-required testing duration plus 1 day for scheduling logistics
- **Severity:** MAJOR — insufficient testing time leads to schedule delays or skipped inspections; CRITICAL if the inspection is a life-safety hold point
- **Downstream Impact:** `inspection-tracker` (inspection scheduling), `delay-tracker` (testing delays), `look-ahead-planner` (constraint), `quality-management` (test scheduling)

---

### Cost vs. Scope (CDR-18 through CDR-20)

#### CDR-18: Concrete Quantity Budget vs. Plan Calculation

- **Category:** Cost vs. Scope
- **Description:** Compares the concrete quantity carried in the cost budget against the quantity calculated from plan dimensions. Catches budgets based on outdated or inaccurate takeoffs.
- **Source A:** `cost-data.json` → `budget_by_division[division="03"].current_amount` and related quantity assumptions
- **Source B:** `plans-spatial.json` → `quantities.concrete[].volume_cy` (plan-calculated volumes)
- **Comparison Logic:**
  ```
  budget_concrete_cy = cost-data.json.budget_by_division[division="03"].quantity_cy
  plan_concrete_cy = SUM(plans-spatial.json.quantities.concrete[].volume_cy)
  IF budget_concrete_cy > 0 AND plan_concrete_cy > 0:
    variance_cy = plan_concrete_cy - budget_concrete_cy
    variance_pct = variance_cy / budget_concrete_cy * 100
    IF abs(variance_pct) > 10:
      FLAG conflict CDR-18
      RECORD budget_concrete_cy, plan_concrete_cy, variance_cy, variance_pct
      unit_cost = budget_by_division[division="03"].current_amount / budget_concrete_cy
      cost_impact = variance_cy * unit_cost
      RECORD cost_impact
  ```
- **Tolerance:** +/- 10% quantity variance
- **Severity:** MINOR if variance 10-15%; MAJOR if variance 15-25% or cost impact >$10,000; CRITICAL if variance >25% or cost impact >$50,000
- **Downstream Impact:** `cost-tracking` (budget adjustment), `change-order-tracker` (scope change), `earned-value-management` (baseline revision), `risk-management` (contingency draw)

#### CDR-19: Sub Scope of Work Value vs. Schedule of Values

- **Category:** Cost vs. Scope
- **Description:** Compares the subcontractor's contracted scope description and value against the corresponding Schedule of Values line items. Catches misalignments between contract and pay application structures.
- **Source A:** `directory.json` → `subcontractors[].scope`, `subcontractors[].contract_value`
- **Source B:** `cost-data.json` → `sov_lines[]` (matching SOV line items by trade/scope)
- **Comparison Logic:**
  ```
  FOR each sub IN directory.json.subcontractors[]:
    sub_contract_value = sub.contract_value
    sov_total = SUM(cost-data.json.sov_lines[match by sub.trade OR sub.name].scheduled_value)
    IF sub_contract_value > 0 AND sov_total > 0:
      variance = abs(sub_contract_value - sov_total)
      variance_pct = variance / sub_contract_value * 100
      IF variance_pct > 5:
        FLAG conflict CDR-19
        RECORD sub.name, sub_contract_value, sov_total, variance, variance_pct
  ```
- **Tolerance:** +/- 5% or +/- $500 (whichever is greater)
- **Severity:** MAJOR — misalignment between contract and SOV causes pay application disputes; CRITICAL if variance >$50,000
- **Downstream Impact:** `cost-tracking` (budget reconciliation), `earned-value-management` (baseline accuracy), `meeting-minutes` (billing disputes), `pay-applications` (pay app processing)

#### CDR-20: Change Order Impact vs. Contingency Remaining

- **Category:** Cost vs. Scope
- **Description:** Evaluates whether pending and approved change orders will exhaust the remaining contingency. An early warning that the project may exceed budget authorization.
- **Source A:** `change-order-log.json` → `change_orders[].cost_estimate`, `change_orders[].status`
- **Source B:** `cost-data.json` → `contingency.current_amount`, `contingency.original_amount`
- **Comparison Logic:**
  ```
  contingency_remaining = cost-data.json.contingency.current_amount
  pending_co_total = SUM(change-order-log.json.change_orders[status IN ("submitted", "under_review")].cost_estimate)
  approved_uncommitted = SUM(change-order-log.json.change_orders[status="approved" AND NOT committed].cost_approved)
  total_exposure = pending_co_total + approved_uncommitted
  IF total_exposure > contingency_remaining:
    FLAG conflict CDR-20
    RECORD contingency_remaining, total_exposure, deficit
    deficit = total_exposure - contingency_remaining
  exposure_pct = total_exposure / cost-data.json.contingency.original_amount * 100
  IF exposure_pct > 70:
    FLAG conflict CDR-20 (contingency stress)
  ```
- **Tolerance:** Total CO exposure must not exceed contingency remaining; warning at 70% of original contingency consumed
- **Severity:** MAJOR if total exposure within 90-100% of contingency; CRITICAL if total exposure exceeds contingency remaining
- **Downstream Impact:** `cost-tracking` (budget controls), `risk-management` (contingency forecast), `meeting-minutes` (owner notification), `earned-value-management` (EAC revision)

---

### Drawing vs. Drawing (CDR-21 through CDR-23)

#### CDR-21: Architectural Dimension vs. Structural Dimension

- **Category:** Drawing vs. Drawing
- **Description:** Compares dimensions of the same element as shown on architectural drawings versus structural drawings. Common clashes include wall thicknesses, opening sizes, and column locations.
- **Source A:** `plans-spatial.json` → architectural sheet data (dimensions, openings, wall locations from discipline "A" sheets)
- **Source B:** `plans-spatial.json` → structural sheet data (dimensions, openings, member sizes from discipline "S" sheets)
- **Comparison Logic:**
  ```
  FOR each shared_element IN [openings, walls, columns, slab_edges]:
    arch_dimension = plans-spatial.json[element, discipline="A"].dimension
    struct_dimension = plans-spatial.json[element, discipline="S"].dimension
    IF both EXISTS:
      delta = abs(arch_dimension - struct_dimension)
      IF delta > 2:  # Greater than 2" discrepancy
        FLAG conflict CDR-21
        RECORD element, arch_sheet, arch_dimension, struct_sheet, struct_dimension, delta
  ```
- **Tolerance:** +/- 2" for walls and openings; +/- 1" for column locations and grid-referenced elements
- **Severity:** MINOR if delta 2-4" on non-structural elements; MAJOR if delta >4" or affects structural member; CRITICAL if column location misalignment (affects foundation)
- **Downstream Impact:** `rfi-preparer` (dimension clarification), `punch-list` (field verification), `change-order-tracker` (rework cost), `cost-tracking` (quantity impact)

#### CDR-22: MEP Equipment Tag on Plan vs. Equipment Schedule

- **Category:** Drawing vs. Drawing
- **Description:** Verifies that every equipment tag shown on the MEP plan drawings has a corresponding entry in the equipment schedule, and that the schedule data matches the plan annotations.
- **Source A:** `plans-spatial.json` → `mep_systems.mechanical.equipment[].tag`, `mep_systems.electrical.panel_schedules[].panel`
- **Source B:** `plans-spatial.json` → `sheet_cross_references.schedule_references[]` (equipment schedules on drawing sheets)
- **Comparison Logic:**
  ```
  # Check for tags on plans missing from schedules
  FOR each equipment IN plans-spatial.json.mep_systems.mechanical.equipment[]:
    tag = equipment.tag  # e.g., "RTU-1"
    schedule_entry = equipment_schedules[match by tag]
    IF schedule_entry NOT EXISTS:
      FLAG conflict CDR-22 (tag on plan, missing from schedule)
      RECORD tag, equipment.source_sheet
    ELSE:
      # Compare capacity values
      IF equipment.cooling.tons != schedule_entry.cooling_tons:
        FLAG conflict CDR-22 (capacity mismatch)
        RECORD tag, "cooling", equipment.cooling.tons, schedule_entry.cooling_tons

  # Check for schedule entries missing from plans
  FOR each schedule_entry IN equipment_schedules[]:
    IF NOT EXISTS in mep_systems.mechanical.equipment[tag=schedule_entry.tag]:
      FLAG conflict CDR-22 (in schedule, missing from plan)
      RECORD schedule_entry.tag
  ```
- **Tolerance:** Tags must match exactly; capacity values within +/- 5%
- **Severity:** MAJOR — missing or mismatched equipment affects procurement, installation, and commissioning
- **Downstream Impact:** `submittal-intelligence` (equipment submittals), `cost-tracking` (equipment pricing), `inspection-tracker` (commissioning), `procurement-log` (ordering)

#### CDR-23: Door Schedule vs. Door Mark on Plan

- **Category:** Drawing vs. Drawing
- **Description:** Cross-checks door marks shown on floor plans against the door schedule. Catches doors on plans with no schedule entry, schedule entries with no plan mark, and data mismatches (size, type, rating).
- **Source A:** `plans-spatial.json` → `door_schedule[]` (from architectural plan door tags)
- **Source B:** `plans-spatial.json` → `sheet_cross_references.schedule_references[]` (door schedule table data)
- **Comparison Logic:**
  ```
  FOR each door_on_plan IN plans-spatial.json.door_schedule[]:
    schedule_entry = door_schedule_table[match by door.mark]
    IF schedule_entry NOT EXISTS:
      FLAG conflict CDR-23 (door on plan, missing from schedule)
      RECORD door.mark, door.location
    ELSE:
      IF door.width != schedule_entry.width:
        FLAG conflict CDR-23 (width mismatch)
        RECORD door.mark, door.width, schedule_entry.width
      IF door.fire_rating != schedule_entry.fire_rating:
        FLAG conflict CDR-23 (fire rating mismatch)
        RECORD door.mark, door.fire_rating, schedule_entry.fire_rating

  # Reverse check
  FOR each schedule_entry IN door_schedule_table[]:
    IF NOT EXISTS on plan:
      FLAG conflict CDR-23 (in schedule, not on plan)
      RECORD schedule_entry.mark
  ```
- **Tolerance:** None for existence checks and fire ratings; +/- 1" for dimensional values
- **Severity:** MINOR for minor dimensional differences; MAJOR for missing entries; CRITICAL for fire rating mismatches (life safety, code compliance)
- **Downstream Impact:** `punch-list` (door installation verification), `inspection-tracker` (fire-rated assembly inspection), `cost-tracking` (hardware and door costs), `submittal-intelligence` (door/hardware submittals)

---

### Dual-Source (CDR-24 through CDR-25)

#### CDR-24: DXF Room Area vs. Visual-Estimated Room Area

- **Category:** Dual-Source
- **Description:** Compares room areas calculated from DXF polyline geometry (exact mathematical calculation) against room areas estimated from visual/PDF extraction (approximate). Identifies extraction pipeline disagreements.
- **Source A:** `plans-spatial.json` → `quantities.rooms[]` entries with `source: "dxf"` (polyline-calculated area)
- **Source B:** `plans-spatial.json` → `quantities.rooms[]` entries with `source: "claude_vision"` (visually estimated area)
- **Comparison Logic:**
  ```
  FOR each room IN plans-spatial.json.quantities.rooms[]:
    IF room has entries from BOTH sources:
      dxf_area = entries[source="dxf"].area_sf
      visual_area = entries[source="claude_vision"].area_sf
      variance_pct = abs(dxf_area - visual_area) / dxf_area * 100
      IF variance_pct > 10:
        FLAG conflict CDR-24
        RECORD room.room_number, dxf_area, visual_area, variance_pct
        # DXF is Priority 1 per merge rules — use dxf_area as resolved value
        RESOLVE using dxf_area with confidence "high"
      ELSE:
        # Within tolerance — use DXF value, note visual confirmation
        RESOLVE using dxf_area with confidence "confirmed"
  ```
- **Tolerance:** +/- 10% between DXF and visual extraction; DXF governs per existing merge rules
- **Severity:** MINOR if variance 10-20% (expected visual estimation error); MAJOR if variance >20% (indicates potential extraction error in one pipeline)
- **Downstream Impact:** `quantitative-intelligence` (quantity accuracy), `cost-tracking` (material quantities), `labor-tracking` (productivity area basis)

#### CDR-25: DXF Pipe Attribute vs. Visual Pipe Size Annotation

- **Category:** Dual-Source
- **Description:** Compares pipe sizes from DXF block attributes (structured ATTRIB data) against pipe sizes read from visual/PDF text annotations. Identifies cases where the CAD model disagrees with the annotation.
- **Source A:** `plans-spatial.json` → `mep_systems.pipe_sizes[]` entries with `source: "dxf"` (from DXF ATTRIB extraction)
- **Source B:** `plans-spatial.json` → `mep_systems.pipe_sizes[]` entries with `source: "claude_vision"` or `source: "notes"` (from visual/text extraction)
- **Comparison Logic:**
  ```
  FOR each pipe_segment IN plans-spatial.json.mep_systems.pipe_sizes[]:
    IF pipe_segment has entries from BOTH sources:
      dxf_size = entries[source="dxf"].size
      visual_size = entries[source="claude_vision" OR source="notes"].size
      IF normalize_pipe_size(dxf_size) != normalize_pipe_size(visual_size):
        FLAG conflict CDR-25
        RECORD pipe_segment.system, dxf_size, visual_size, pipe_segment.sheet
        # DXF ATTRIB data is Priority 1 — but flag for review because
        # annotation may reflect a design revision not yet in CAD
        IF project-config.json.documents_loaded[sheet].revision > dxf_revision:
          MARK as "possible-revision-conflict"
        ELSE:
          RESOLVE using dxf_size per Priority 1 merge rules
  ```
- **Tolerance:** None — pipe sizes must match between sources
- **Severity:** MAJOR — pipe size discrepancy affects flow calculations and material ordering; CRITICAL if fire protection or storm system
- **Downstream Impact:** `quantitative-intelligence` (pipe quantities), `cost-tracking` (pipe material cost), `inspection-tracker` (pipe sizing verification), `safety-management` (fire protection adequacy)

---

## 3. Severity Classification

All detected conflicts are assigned one of three severity levels. Severity drives notification routing, resolution timeline, and escalation procedures.

### CRITICAL (Requires Immediate Resolution)

A conflict is CRITICAL when any of the following conditions apply:

| Condition | Threshold | Rationale |
|-----------|-----------|-----------|
| Safety impact | Any structural adequacy concern, life safety system deficiency, or fire-rated assembly discrepancy | Worker and occupant safety is non-negotiable |
| Code violation | Any ADA, fire code, structural code, or plumbing code non-compliance | Code violations prevent certificate of occupancy |
| Cost variance | >20% on any single line item with value >$10,000 | Large cost surprises threaten project viability |
| Critical path schedule impact | >5 days impact on critical path activities | Schedule slip beyond recovery without acceleration |
| Structural specification | Plan f'c < spec f'c, or structural member undersized | Structural adequacy is life safety |
| Equipment capacity | Deficit >15% on life-safety systems (fire protection, electrical service) | System cannot perform its intended function |

**Response:** Superintendent must be notified immediately. Work in the affected area may need to stop. Resolution must occur before work proceeds. Document in daily report.

### MAJOR (Resolve Within 48 Hours)

A conflict is MAJOR when any of the following conditions apply:

| Condition | Threshold | Rationale |
|-----------|-----------|-----------|
| Schedule impact | 2-5 days on critical or near-critical path activities | Recoverable with acceleration, but window is closing |
| Cost impact | $5,000 - $50,000 | Significant but manageable cost exposure |
| Spec non-compliance (non-safety) | Material or method does not meet spec but has no safety impact | Rework is required but can be scheduled |
| Equipment capacity deficit | 1-15% below spec minimum (non-safety systems) | Performance deficiency, not safety |
| Missing documentation | Equipment tag or door on plan with no schedule entry | Procurement and installation cannot proceed without data |
| Pipe/duct sizing | Size discrepancy on non-critical systems | System performance will be affected |

**Response:** Flag for superintendent review at next coordination meeting or daily report. Generate RFI if design team input is needed. Track in conflict log with 48-hour resolution target.

### MINOR (Track and Resolve at Next Coordination)

A conflict is MINOR when any of the following conditions apply:

| Condition | Threshold | Rationale |
|-----------|-----------|-----------|
| Dimensional variance within tolerance | Inconsistent documentation but within acceptable construction tolerance | Documents disagree but either value is buildable |
| Cosmetic/finish discrepancy | Different finish names for same product, or minor color/texture variation | Does not affect function, safety, or cost |
| Documentation inconsistency | Same item called by different names across documents | Causes confusion but not construction errors |
| Non-critical schedule variance | <2 days impact on non-critical activities | Absorbable within available float |
| Dual-source estimation variance | Visual vs DXF area within 10-20% on non-critical elements | Expected variance between extraction methods |
| Overdesign | Plan value exceeds spec requirement (e.g., higher f'c than required) | Conservative — no rework needed, possible cost optimization |

**Response:** Log in conflict tracking. Resolve at next OAC meeting, coordination meeting, or weekly planning session. No immediate action required.

---

## 4. Resolution Priority and Workflow

### Precedence Rules

When a conflict is detected and the correct value must be determined, apply these precedence rules in order:

1. **Specifications govern drawings** — The specification is the controlling document for material requirements, performance criteria, and quality standards. Drawings show location and geometry. When a plan note conflicts with a spec requirement, the spec governs **unless** an ASI (Architect's Supplemental Instruction), addendum, or bulletin explicitly modifies the spec section. Check `project-config.json` → `asi_log[]` for active ASIs affecting the conflicting spec section.

2. **Newer revision governs older** — When the same document has been revised, the latest revision controls. Check revision dates in `project-config.json` → `documents_loaded[].date_loaded` and revision indicators on drawing title blocks. If Source A is Rev 2 and Source B is Rev 1, Source A governs.

3. **DXF governs PDF visual** — DXF-extracted data (structured CAD geometry, block attributes) is Priority 1 per the existing dual-source merge rules defined in `cross-reference-patterns.md` Pattern 7. DXF data is mathematically exact; visual/PDF extraction is approximate. Exception: if the PDF shows a revision date newer than the DXF file date, the annotation may reflect a design change not yet in the CAD model — flag for verification.

4. **Code governs everything** — Building code requirements (IBC, ADA, NEC, IPC, NFPA, local amendments) override all other documents. When any document — plans, specs, or schedule — conflicts with code, the code-compliant value governs. No RFI is needed for code compliance; it is non-negotiable.

5. **When unresolvable** — If precedence rules do not yield a clear resolution (e.g., both sources are the same revision, or the conflict involves a design intent question), the conflict must be escalated:
   - Flag for RFI with recommended question text
   - Include affected drawing references (sheet numbers, detail numbers)
   - Include affected spec section references
   - Assign urgency based on severity classification
   - Suggest interim approach if work cannot be stopped (e.g., "proceed with spec requirement pending RFI response")

### Resolution Workflow

```
FOR each detected conflict:

  # Step 1: Classify
  CLASSIFY severity per Section 3 thresholds
  ASSIGN conflict_id (CONFLICT-YYYY-MMDD-NNN)
  RECORD source_a, source_b, detected_values, variance

  # Step 2: Determine precedence
  DETERMINE resolution precedence per Section 4 rules:
    RULE 1: Check if spec vs drawing conflict → spec governs
    RULE 2: Check revision dates → newer governs
    RULE 3: Check if DXF vs visual conflict → DXF governs
    RULE 4: Check if code requirement involved → code governs
    RULE 5: If no clear precedence → flag for review

  # Step 3: Auto-resolve or escalate
  IF auto-resolvable (clear precedence AND non-safety):
    RECOMMEND resolution with confidence level (high/medium/low)
    RECORD resolved_value, resolution_rule, confidence
    MARK status as "recommended-resolution"
  ELSE:
    FLAG for superintendent review
    IF design_team_input_needed:
      SUGGEST RFI text:
        - Subject: "[CDR-XX] {conflict description}"
        - Question: "{specific question about design intent}"
        - References: "Drawing {sheet}, Spec Section {section}"
        - Impact: "{severity} — {downstream_impact}"
        - Urgency: "{based on severity classification}"
    MARK status as "requires-review"

  # Step 4: Log and notify
  LOG to conflict-log in project-config.json:
    {
      "conflict_id": "CONFLICT-2026-0224-001",
      "rule_id": "CDR-XX",
      "category": "{category}",
      "severity": "CRITICAL|MAJOR|MINOR",
      "source_a": {"file": "...", "field": "...", "value": "..."},
      "source_b": {"file": "...", "field": "...", "value": "..."},
      "status": "recommended-resolution|requires-review|resolved|rfi-issued",
      "resolution": {"value": "...", "rule": "...", "confidence": "..."},
      "detected_date": "ISO 8601",
      "resolved_date": null,
      "rfi_id": null
    }

  # Step 5: Notify downstream
  NOTIFY affected downstream skills:
    - cost-tracking       (if cost impact)
    - inspection-tracker  (if inspection/code impact)
    - punch-list          (if field installation impact)
    - delay-tracker       (if schedule impact)
    - submittal-intelligence (if procurement/submittal impact)
    - safety-management   (if safety impact)
    - rfi-preparer        (if RFI needed)
    - earned-value-management (if baseline impact)
```

### Conflict Log Schema

All detected conflicts are appended to `project-config.json` → `conflict_log[]` with the following structure:

```json
{
  "conflict_log": [
    {
      "conflict_id": "CONFLICT-2026-0224-001",
      "rule_id": "CDR-07",
      "category": "Material",
      "severity": "CRITICAL",
      "description": "Structural plan notes show 4,000 PSI concrete for footings but Spec 03 30 00 requires 4,500 PSI minimum",
      "source_a": {
        "file": "plans-spatial.json",
        "field": "quantities.concrete[element='Footing F1'].notes",
        "value": "4,000 PSI",
        "sheet": "S2.1"
      },
      "source_b": {
        "file": "specs-quality.json",
        "field": "mix_designs[assigned_elements contains 'footing'].design_fc",
        "value": "4,500 PSI",
        "section": "03 30 00"
      },
      "status": "requires-review",
      "resolution": {
        "recommended_value": "4,500 PSI (spec governs per Rule 1)",
        "rule_applied": "Specifications govern drawings",
        "confidence": "high",
        "rfi_suggested": true,
        "rfi_text": "Structural plan note S2.1 indicates 4,000 PSI concrete for footings. Spec Section 03 30 00 requires 4,500 PSI minimum. Please confirm required concrete strength for footings."
      },
      "downstream_impact": ["inspection-tracker", "cost-tracking", "intake-chatbot", "quality-management"],
      "detected_date": "2026-02-24T08:30:00Z",
      "resolved_date": null,
      "rfi_id": null
    }
  ]
}
```
