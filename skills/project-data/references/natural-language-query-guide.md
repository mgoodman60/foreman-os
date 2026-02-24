---
name: natural-language-query-guide
description: Maps common superintendent questions and natural language patterns to structured data queries across the 28-file project intelligence store. Used by the project-data-navigator agent to interpret field questions and route them to the correct files and fields.
version: 1.0.0
---

# Natural Language Query Guide

This document maps how construction superintendents ask questions in plain English to the structured data queries needed to answer them. The **project-data-navigator** agent uses this guide to detect intent, extract entities, route queries to the correct JSON files and fields, and format responses for fast field consumption.

All query pattern IDs (QP-*) reference `data-query-patterns.md`. All threshold references use `alert-thresholds.md`. All cross-file joins use the Join Key Reference Table in `data-query-patterns.md` Section 11.

---

## 1. Question Category Taxonomy

Each category maps a class of superintendent questions to the files, fields, and query patterns needed to answer them.

---

### 1.1 Schedule / Timeline

**Common question patterns:**
- "When does [activity] start?"
- "Are we on track?"
- "What's the critical path look like?"
- "How far behind are we?"
- "What's our float on [activity]?"
- "When's the next milestone?"
- "What's the completion date now?"
- "Show me the three-week lookahead"
- "What's our PPC this week?"
- "Did we hit our lookahead targets?"

**Primary files:**
- `schedule.json` — activities, milestones, critical path, lookahead history
- `cost-data.json` — earned value (SPI cross-check)

**Key fields:**
- `schedule.json` → `activities[].activity_name`, `.early_start`, `.early_finish`, `.total_float`, `.percent_complete`, `.is_critical`, `.actual_start`
- `schedule.json` → `milestones[].name`, `.baseline_date`, `.forecast_date`, `.status`
- `schedule.json` → `critical_path[]`, `near_critical[]`
- `schedule.json` → `lookahead_history[].activities_planned`, `.activities_completed`, `.reasons_for_misses[]`
- `cost-data.json` → `earned_value.bcwp`, `.bcws` (for SPI calculation)

**Query patterns:**
- Activity lookup → filter `activities[]` by name fuzzy match
- Critical path status → QP-SCH-01
- Milestone tracking → QP-SCH-02
- PPC calculation → QP-SCH-03
- Schedule-cost alignment → QP-SCH-04

---

### 1.2 Subcontractor

**Common question patterns:**
- "How's [sub name] doing?"
- "Who's on site today?"
- "What subs are scheduled this week?"
- "How many guys does [sub] have out there?"
- "Is [sub] keeping up?"
- "What's [sub]'s inspection pass rate?"
- "Any issues with [sub]?"
- "Who's the foreman for [trade]?"
- "When does [sub] mobilize?"
- "Is [sub] supposed to be here today?"

**Primary files:**
- `directory.json` — sub roster, trades, contacts, scope
- `labor-tracking.json` — headcounts, hours, attendance
- `quality-data.json` — first-pass inspection results
- `safety-log.json` — incidents by sub
- `inspection-log.json` — inspection results by sub
- `schedule.json` — activities assigned to subs

**Key fields:**
- `directory.json` → `subcontractors[].name`, `.trade`, `.scope`, `.foreman`, `.phone`, `.status`, `.start_date`
- `labor-tracking.json` → `daily_entries[].sub_name`, `.workers_present`, `.workers_expected`, `.hours_worked`, `.date`
- `quality-data.json` → `first_pass_inspection_results[].sub_name`, `.result`
- `safety-log.json` → `incidents[].sub_name`, `.severity`
- `inspection-log.json` → `inspections[].sub_name`, `.result`

**Query patterns:**
- Sub performance scorecard → QP-SUB-01
- Mobilization vs schedule need → QP-SUB-02
- Headcount trends → QP-SUB-03
- Quality metrics by sub → QP-SUB-04

**Cross-reference pattern:** Pattern 1 (Sub -> Scope -> Spec -> Inspection) from `cross-reference-patterns.md`

---

### 1.3 Materials / Procurement

**Common question patterns:**
- "Where's the steel?"
- "What deliveries are coming this week?"
- "Any materials late?"
- "When's the [material] showing up?"
- "Did we get the certs for that concrete?"
- "What's the lead time on [item]?"
- "Any long-lead items we need to worry about?"
- "Did that submittal get approved so we can order?"
- "How much did we spend on materials this month?"

**Primary files:**
- `procurement-log.json` — items, delivery dates, status, costs
- `submittal-log.json` — approval status, lead times
- `schedule.json` — material requirements, long-lead items
- `specs-quality.json` — certification requirements

**Key fields:**
- `procurement-log.json` → `items[].item_name`, `.expected_delivery`, `.delivery_status`, `.supplier`, `.cert_status`, `.total_cost`, `.submittal_id`, `.linked_activity_id`
- `submittal-log.json` → `submittals[].status`, `.lead_time_weeks`, `.spec_section`
- `schedule.json` → `long_lead_items[]`, `material_requirements_by_activity[]`

**Query patterns:**
- Overdue materials → QP-MAT-01
- Material-to-activity linkage → QP-MAT-02
- Certification status → QP-MAT-03
- Material cost tracking → QP-MAT-04

**Cross-reference pattern:** Pattern 5 (RFI -> Submittal -> Procurement Chain) from `cross-reference-patterns.md`

---

### 1.4 Cost / Budget

**Common question patterns:**
- "How's the budget looking?"
- "What's our contingency at?"
- "How much have change orders cost us?"
- "Are we over budget on [division]?"
- "What's the cost to complete?"
- "What's our CPI?"
- "How much have we spent vs earned?"
- "What's the burn rate on contingency?"
- "Any big cost variances?"
- "What's the EAC?"

**Primary files:**
- `cost-data.json` — budget, actuals, earned value, contingency
- `change-order-log.json` — change order amounts and status
- `labor-tracking.json` — labor costs
- `procurement-log.json` — material costs

**Key fields:**
- `cost-data.json` → `budget_by_division[].division`, `.original_amount`, `.current_amount`, `.committed_costs`
- `cost-data.json` → `contingency.original_amount`, `.current_amount`, `.draws[]`
- `cost-data.json` → `earned_value.bcwp`, `.bcws`, `.acwp`
- `cost-data.json` → `original_contract_value`
- `change-order-log.json` → `change_orders[].amount`, `.status`, `.cost_approved`

**Query patterns:**
- Budget variance by division → QP-COST-01
- Contingency drawdown → QP-COST-02
- Change order impact → QP-COST-03
- Labor cost vs budget → QP-COST-04
- Schedule-cost alignment → QP-SCH-04

---

### 1.5 Quality / Inspections

**Common question patterns:**
- "Any failed inspections?"
- "What inspections are needed this week?"
- "How's our FPIR?"
- "Did we pass the [inspection type]?"
- "What hold points do we need for [work type]?"
- "Any quality issues on [location]?"
- "What's [sub]'s pass rate?"
- "Are the concrete tests passing?"
- "Any corrective actions open?"
- "Do we have the test results for [material]?"

**Primary files:**
- `inspection-log.json` — inspection records, results
- `quality-data.json` — first-pass results, test results, corrective actions, deficiencies
- `specs-quality.json` — hold points, testing requirements
- `punch-list.json` — open quality items

**Key fields:**
- `inspection-log.json` → `inspection_log[].type`, `.result`, `.date`, `.sub_name`, `.location`, `.linked_hold_point`
- `quality-data.json` → `first_pass_inspection_results[].sub_name`, `.result`
- `quality-data.json` → `test_results[].test_type`, `.result`, `.actual_value`, `.spec_requirement`
- `quality-data.json` → `corrective_actions[].status`
- `specs-quality.json` → `hold_points[].work_type`, `.inspection_name`, `.trigger`

**Query patterns:**
- Inspection results by location → QP-LOC-03
- Sub quality metrics → QP-SUB-04
- Cross-ref: Pattern 1 (Sub -> Scope -> Spec -> Inspection)

**Alert thresholds:** FPIR tiers from `alert-thresholds.md` Section 1.3

---

### 1.6 Safety

**Common question patterns:**
- "Any incidents?"
- "What's our TRIR?"
- "Any safety concerns in that area?"
- "When was the last toolbox talk?"
- "Any near misses this week?"
- "What are the fall protection zones?"
- "Any confined spaces near [location]?"
- "Is it safe to do crane work today?"
- "What's [sub]'s safety record?"
- "How many hours without a recordable?"

**Primary files:**
- `safety-log.json` — incidents, near misses, toolbox talks, OSHA data
- `specs-quality.json` — safety zones, weather thresholds for crane/hot work
- `plans-spatial.json` — site utilities (strike risk), building areas
- `labor-tracking.json` — total hours worked (for TRIR calculation)

**Key fields:**
- `safety-log.json` → `recordable_incidents[]`, `near_misses[]`, `first_aid_log[]`, `osha_300_log.trir`, `toolbox_talks[]`
- `specs-quality.json` → `safety.fall_protection_zones[]`, `.confined_spaces[]`, `.hot_work_areas[]`, `.crane_exclusion_zones[]`
- `specs-quality.json` → `weather_thresholds[].max_wind` (crane operations)
- `plans-spatial.json` → `site_utilities` (underground strike risk)

**Query patterns:**
- TRIR calculation: `(recordable_incidents * 200,000) / total_hours_worked`
- Safety zone lookup: filter `specs-quality.json` safety arrays by location proximity
- Sub safety record: join `safety-log.json` incidents by `sub_name`

**Alert thresholds:** TRIR tiers from `alert-thresholds.md` Section 1.4

**Cross-reference pattern:** Pattern 3 (Work Type -> Weather Threshold -> Today's Weather) for crane/weather safety

---

### 1.7 Location-Based

**Common question patterns:**
- "What's happening at the second floor?"
- "Show me Building A activity"
- "Any punch items in Room 204?"
- "Who's working in the east wing?"
- "What inspections happened at [location]?"
- "Any safety issues near Grid C?"
- "What's the status of the lobby area?"
- "How many guys are on Level 2?"

**Primary files:**
- `plans-spatial.json` — grid lines, rooms, building areas, floor levels
- `schedule.json` — activities with location
- `labor-tracking.json` — workers by location
- `punch-list.json` — items by location
- `inspection-log.json` — inspections by location
- `daily-report-data.json` — work entries by location
- `safety-log.json` — incidents by location

**Key fields:**
- `plans-spatial.json` → `room_schedule[].room_number`, `.floor_level`, `.building_area`
- `plans-spatial.json` → `building_areas[].name`, `.grids`, `.floors`
- `plans-spatial.json` → `grid_lines.columns`, `.rows`
- All activity files → `[].location` field (matched against spatial data)

**Query patterns:**
- Activity by location → QP-LOC-01
- Punch list by location → QP-LOC-02
- Inspection results by location → QP-LOC-03
- Resource allocation by area → QP-LOC-04

**Cross-reference pattern:** Pattern 2 (Location -> Grid -> Area -> Room) from `cross-reference-patterns.md`

---

### 1.8 Delays

**Common question patterns:**
- "Why are we behind?"
- "What's causing delays?"
- "How many delay days this month?"
- "Is [issue] going to delay us?"
- "What's the weather delay total?"
- "Are we eating float on [activity]?"
- "How much schedule impact from that change order?"
- "What's the delay trend?"

**Primary files:**
- `delay-log.json` — delay events, weather delays, concurrent delays
- `schedule.json` — critical path, float analysis
- `change-order-log.json` — schedule impact days from COs
- `daily-report-data.json` — weather conditions (delay verification)
- `specs-quality.json` — weather thresholds (delay justification)

**Key fields:**
- `delay-log.json` → `delay_events[].type`, `.duration`, `.impact`, `.date_identified`, `.cause`
- `delay-log.json` → `weather_delays[].date`, `.conditions`, `.duration`
- `schedule.json` → `activities[].total_float`, `.is_critical`
- `change-order-log.json` → `change_orders[].schedule_impact_days`

**Query patterns:**
- Delay acceleration anomaly: see `alert-thresholds.md` Section 2.3
- Float analysis: QP-SCH-01 (filter by total_float)
- CO schedule impact: QP-COST-03

---

### 1.9 RFIs / Submittals

**Common question patterns:**
- "Any open RFIs?"
- "What's pending review?"
- "When was that submittal submitted?"
- "How long has RFI [number] been open?"
- "Did the architect respond to [RFI]?"
- "What submittals do we need for [spec section]?"
- "Any submittals holding up procurement?"
- "How many RFIs this month?"
- "What's the RFI aging average?"

**Primary files:**
- `rfi-log.json` — RFI records
- `submittal-log.json` — submittal records
- `procurement-log.json` — linked procurement items
- `specs-quality.json` — submittal requirements per section

**Key fields:**
- `rfi-log.json` → `rfis[].rfi_number`, `.subject`, `.status`, `.date_issued`, `.schedule_impact`, `.related_submittals`
- `submittal-log.json` → `submittals[].id`, `.status`, `.spec_section`, `.lead_time_weeks`, `.related_rfis`
- `specs-quality.json` → `spec_sections[].submittal_required`

**Query patterns:**
- Open RFI list: filter `rfis[]` where `status != "resolved"`, sort by `date_issued ASC`
- Pending submittals: filter `submittals[]` where `status IN ("submitted", "under_review")`
- Aging calculation: `age_days = TODAY - date_issued` for open items
- Schedule-blocking submittals: filter where `schedule_impact == "critical_path_blocked"`

**Cross-reference pattern:** Pattern 5 (RFI -> Submittal -> Procurement Chain) from `cross-reference-patterns.md`

---

### 1.10 Closeout / Commissioning

**Common question patterns:**
- "What's our closeout status?"
- "Which systems are commissioned?"
- "Any warranties expiring soon?"
- "Where are we on O&M manuals?"
- "Is the HVAC system signed off?"
- "What's left for substantial completion?"
- "When does the roofing warranty expire?"
- "Have we received all the training certificates?"
- "What punch items are blocking closeout?"
- "Show me closeout progress by system"

**Primary files:**
- `closeout-data.json` — system completion status, warranties, commissioning, O&M, training
- `quality-data.json` — commissioning test results, system tests
- `drawing-log.json` — as-built drawing status
- `punch-list.json` — open items by system
- `directory.json` — sub contacts for warranty follow-up

**Key fields:**
- `closeout-data.json` → `systems[].system_name`, `.commissioning_status`, `.oam_manual_status`, `.warranty_status`, `.training_status`, `.completion_pct`
- `closeout-data.json` → `warranties[].item`, `.sub_name`, `.expiration_date`, `.warranty_type`
- `quality-data.json` → `system_tests[].system`, `.test_type`, `.result`
- `drawing-log.json` → `drawings[].as_built_status`, `.discipline`
- `punch-list.json` → `items[].system`, `.status`

**Query patterns:**
- Closeout completion by system → QP-CLO-001
- Warranty expiration timeline → QP-CLO-002

**Cross-reference pattern:** Pattern 11 (Closeout -> Quality -> Drawing) from `cross-reference-patterns.md`

**Alert thresholds:** Closeout completion tiers from `alert-thresholds.md` Section 1.9; warranty expiration sub-thresholds

---

### 1.11 Risk Management

**Common question patterns:**
- "What are our top risks?"
- "What's the risk exposure?"
- "What are our biggest risks right now?"
- "Any new risks this week?"
- "How's the risk contingency looking?"
- "Is that risk still active?"
- "What's the mitigation status for [risk]?"
- "Any risks on the critical path?"
- "Show me the risk register"
- "What risks are tied to the schedule?"

**Primary files:**
- `risk-register.json` — risk entries, probability, impact, mitigation plans, contingency
- `schedule.json` — activity linkage for schedule risks
- `cost-data.json` — contingency status for cost risks
- `delay-log.json` — check if risks have materialized as delays

**Key fields:**
- `risk-register.json` → `risks[].risk_id`, `.description`, `.category`, `.probability`, `.impact`, `.status`, `.risk_owner`, `.mitigation_plan`, `.mitigation_status`, `.contingency_allocated`, `.contingency_spent`, `.linked_activity_id`
- `schedule.json` → `activities[].activity_id`, `.activity_name`, `.is_critical`, `.total_float`
- `cost-data.json` → `contingency.original_amount`, `.committed`, `.spent`

**Query patterns:**
- Active risks by severity → QP-RSK-001
- Mitigation status and contingency burn → QP-RSK-002

**Cross-reference pattern:** Pattern 8 (Risk -> Schedule -> Cost) from `cross-reference-patterns.md`

**Alert thresholds:** Risk exposure tiers from `alert-thresholds.md` Section 1.10; contingency burn rate sub-thresholds

---

### 1.12 Claims

**Common question patterns:**
- "What's our claims status?"
- "Any pending notices?"
- "How much are we claiming?"
- "What's the claims documentation look like?"
- "When's the notice deadline?"
- "Did we send the notice for [issue]?"
- "Any claims in negotiation?"
- "What delays support that claim?"
- "What's our total claims exposure?"
- "Are there any claims deadlines coming up?"

**Primary files:**
- `claims-log.json` — claims records, notice tracking, documentation status
- `delay-log.json` — supporting delay events
- `change-order-log.json` — related change orders
- `daily-report-data.json` — contemporaneous records for evidence

**Key fields:**
- `claims-log.json` → `claims[].claim_id`, `.description`, `.claim_type`, `.status`, `.claimed_amount`, `.claimed_days`, `.date_filed`, `.notice_required_by`, `.notice_sent_date`, `.documentation_completeness_pct`, `.related_delay_ids`, `.related_co_ids`
- `delay-log.json` → `delays[].delay_id`, `.cause`, `.delay_days`, `.impact`
- `change-order-log.json` → `change_orders[].co_number`, `.status`, `.amount`

**Query patterns:**
- Active claims by status and value → QP-CLM-001
- Claims notice deadline tracking → QP-CLM-002

**Cross-reference pattern:** Pattern 9 (Claims -> Delay -> CO) from `cross-reference-patterns.md`

**Alert thresholds:** Claims status tiers from `alert-thresholds.md` Section 1.11; notice period sub-thresholds

---

### 1.13 Environmental

**Common question patterns:**
- "What's our LEED status?"
- "When was the last SWPPP inspection?"
- "What's the waste diversion rate?"
- "Any environmental issues?"
- "Are we compliant on stormwater?"
- "When does the SWPPP permit expire?"
- "Any hazmat incidents?"
- "What LEED credits are at risk?"
- "How much waste have we diverted?"
- "Is there a SWPPP corrective action open?"

**Primary files:**
- `environmental-log.json` — LEED credits, SWPPP compliance, waste diversion, hazmat incidents
- `inspection-log.json` — environmental inspection records
- `safety-log.json` — hazmat incident cross-reference
- `daily-report-data.json` — weather conditions for SWPPP context

**Key fields:**
- `environmental-log.json` → `leed_credits[].credit_id`, `.status`, `.points_available`, `.points_achieved`
- `environmental-log.json` → `swppp.inspections[].date`, `.result`, `.corrective_actions[]`
- `environmental-log.json` → `swppp.permit_expiration`, `.required_frequency`
- `environmental-log.json` → `waste_diversion.total_waste_tons`, `.diverted_tons`, `.diversion_rate`
- `environmental-log.json` → `hazmat.incidents[].date`, `.type`, `.status`

**Query patterns:**
- Environmental compliance rate by category → QP-ENV-001
- SWPPP inspection status → QP-ENV-002

**Cross-reference pattern:** Pattern 10 (Environmental -> Inspection -> Safety) from `cross-reference-patterns.md`

**Alert thresholds:** Environmental compliance tiers from `alert-thresholds.md` Section 1.12; SWPPP, waste diversion, and permit sub-thresholds

---

### 1.14 Annotations / Markups

**Common question patterns:**
- "Any recent markups?"
- "What's the annotation status?"
- "Any unresolved annotations?"
- "Who has open markups?"
- "What annotations are on sheet S2.1?"
- "Did the architect respond to that markup?"
- "How many annotations this week?"
- "What's outstanding on the structural drawings?"
- "Any markups that need my attention?"
- "Show me open comments on the plans"

**Primary files:**
- `annotation-log.json` — annotations, markups, comments, revision clouds
- `drawing-log.json` — drawing context, revision status
- `rfi-log.json` — RFIs generated from annotations

**Key fields:**
- `annotation-log.json` → `annotations[].annotation_id`, `.document_id`, `.document_type`, `.annotation_type`, `.description`, `.author`, `.assigned_to`, `.date_created`, `.status`, `.priority`, `.linked_rfi_id`
- `drawing-log.json` → `drawings[].sheet_number`, `.title`, `.discipline`, `.current_revision`
- `rfi-log.json` → `rfis[].rfi_number`, `.status`, `.response_text`

**Query patterns:**
- Annotation activity by document type → QP-ANN-001
- Unresolved annotations aging → QP-ANN-002

**Cross-reference pattern:** Pattern 12 (Annotation -> Drawing -> RFI) from `cross-reference-patterns.md`

---

### 1.15 Daily / Weekly Reports

**Common question patterns:**
- "What happened yesterday?"
- "Give me the weekly summary"
- "What did [sub] do last Tuesday?"
- "What was the weather on [date]?"
- "How many guys were on site last week?"
- "Show me the daily report for [date]"
- "What work was done in [location] this week?"
- "Any issues reported yesterday?"

**Primary files:**
- `daily-report-data.json` — all daily report entries
- `daily-report-intake.json` — raw intake entries awaiting report generation
- `labor-tracking.json` — headcounts by date
- `safety-log.json` — incidents by date

**Key fields:**
- `daily-report-data.json` → `entries[].date`, `.location`, `.work_description`, `.sub_name`
- `daily-report-data.json` → `weather.temperature`, `.conditions`, `.precipitation`
- `daily-report-data.json` → `crew.subs_on_site`, `.headcounts`
- `labor-tracking.json` → `daily_entries[].date`, `.sub_name`, `.workers_present`, `.hours_worked`

**Query patterns:**
- Date-range filter: Time-Series patterns from `data-query-patterns.md` Section 7
- Sub activity on date: filter `daily-report-data.json` entries by `sub_name` AND `date`
- Weekly aggregation: Group By pattern from Section 13.5, grouped by date

---

## 2. Intent Detection Patterns

The agent must classify each question into one or more categories before routing the query. Use the following trigger words and disambiguation rules.

### 2.1 Category Trigger Words

| Category | Trigger Words / Phrases |
|----------|------------------------|
| Schedule | "schedule", "on track", "behind", "ahead", "float", "critical path", "milestone", "completion date", "start date", "finish", "lookahead", "PPC", "percent plan complete", "when does", "when is", "timeline" |
| Subcontractor | "sub", "contractor", "foreman", "[company name]", "[trade name]", "who's on site", "headcount", "mobilize", "demob", "crew", "guys" |
| Materials | "material", "delivery", "steel", "concrete", "lumber", "shipment", "procurement", "order", "supplier", "vendor", "certs", "certification", "long lead", "lead time" |
| Cost | "budget", "cost", "money", "contingency", "change order", "CO", "variance", "CPI", "over budget", "under budget", "EAC", "burn rate", "spend", "estimate at completion" |
| Quality | "inspection", "pass", "fail", "FPIR", "quality", "hold point", "test", "concrete test", "compaction", "corrective action", "deficiency", "punch" |
| Safety | "safety", "incident", "TRIR", "near miss", "toolbox talk", "fall protection", "confined space", "crane", "OSHA", "recordable", "injury" |
| Location | "floor", "level", "room", "grid", "wing", "building", "area", "zone", "east", "west", "north", "south", "lobby", "basement", "roof" |
| Delays | "delay", "behind", "late", "slip", "float", "weather day", "impact", "extension", "time" |
| RFI/Submittal | "RFI", "submittal", "pending review", "architect response", "open items", "approval", "revise and resubmit" |
| Closeout | "closeout", "commissioning", "warranty", "O&M", "O&M manual", "training", "substantial completion", "turnover", "sign-off", "final inspection", "as-built" |
| Risk | "risk", "risk register", "exposure", "mitigation", "contingency burn", "probability", "impact", "risk owner", "biggest risk", "top risks" |
| Claims | "claim", "claims", "notice", "notice period", "time extension", "differing conditions", "acceleration", "dispute", "claims package", "claims documentation" |
| Environmental | "LEED", "SWPPP", "stormwater", "waste diversion", "hazmat", "environmental", "recycling", "erosion control", "permit", "green building", "sustainability" |
| Annotations | "annotation", "markup", "comment", "revision cloud", "marked up", "marked-up", "annotated", "unresolved markup", "open comments", "document markup" |
| Daily/Weekly | "yesterday", "today", "last week", "this week", "daily report", "weekly report", "what happened", "summary" |

### 2.2 Disambiguation Rules

When a question matches multiple categories, apply these priority rules:

**Rule 1: Explicit category wins over implied.**
- "How's Walker doing on the schedule?" — Subcontractor (explicit: "Walker") + Schedule (explicit: "schedule") = route to QP-SUB-02 (sub mobilization vs schedule need) with schedule context
- "Is Walker behind?" — Subcontractor + Schedule = QP-SUB-01 (scorecard) with emphasis on schedule adherence

**Rule 2: Named entity anchors the primary category.**
- If a sub name is detected, primary = Subcontractor
- If a room/grid/floor is detected, primary = Location
- If an RFI/submittal number is detected, primary = RFI/Submittal
- If a cost term (CPI, budget, contingency) is detected, primary = Cost

**Rule 3: "Behind" requires context analysis.**
- "Are we behind?" (no entity) → Schedule (project-level SPI)
- "Is Walker behind?" (sub entity) → Subcontractor (schedule adherence score)
- "Is the steel behind?" (material entity) → Materials (delivery status)
- "Is Building A behind?" (location entity) → Location + Schedule (activities in that area)

**Rule 4: Compound questions get multi-category routing.**
- "Is Walker behind and over budget?" → Subcontractor + Schedule + Cost (multi-step query; see Section 4)
- "What inspections are needed for this week's work?" → Schedule + Quality (multi-step; see Section 4)

**Rule 5: Time-frame words modify but don't determine category.**
- "yesterday", "this week", "last month" → apply as date filters, not as primary category indicators
- Exception: "What happened yesterday?" with no other context → Daily/Weekly Reports category

---

## 3. Entity Recognition Rules

The agent must extract structured entities from natural language before building queries.

### 3.1 Subcontractor Names

**Matching strategy:** Fuzzy match against `directory.json` → `subcontractors[].name`

| Input Pattern | Resolution Logic |
|---------------|-----------------|
| Full company name ("Walker Construction") | Exact match against `subs[].name` |
| Partial name ("Walker") | Substring match; if multiple hits, disambiguate (see Section 6) |
| Trade reference ("the electrician", "our concrete guy") | Map trade keyword to `subs[].trade`; filter by `subs[].status == "active"` |
| Foreman name ("Mike", "Mike Johnson") | Match against `subs[].foreman` |
| Abbreviation ("WC", "ACE") | Check for common abbreviations; fall back to substring match |
| DBA / informal name ("Walker", "ACE Plumbing") | Substring match on name field |

**Trade keyword mapping:**

| Keywords | Trade Value |
|----------|------------|
| "electrician", "electrical", "wire", "conduit", "panel" | Electrical |
| "plumber", "plumbing", "pipe", "piping" | Plumbing |
| "concrete", "pour", "slab", "footing" | Concrete |
| "steel", "iron", "erection", "ironworker" | Structural Steel |
| "HVAC", "mechanical", "ductwork", "air handler" | Mechanical / HVAC |
| "framing", "drywall", "stud", "gyp" | Drywall / Framing |
| "roofing", "roof", "membrane" | Roofing |
| "excavation", "dig", "grade", "sitework", "earthwork" | Excavation / Sitework |
| "painting", "paint", "coatings" | Painting |
| "fire protection", "sprinkler", "fire alarm" | Fire Protection |
| "mason", "masonry", "block", "brick", "CMU" | Masonry |
| "glazing", "glass", "curtain wall", "storefront" | Glazing |
| "flooring", "tile", "carpet", "VCT", "epoxy" | Flooring |
| "landscape", "irrigation", "sod" | Landscaping |

### 3.2 Locations

**Matching strategy:** Match against `plans-spatial.json` spatial data using cascading resolution (Pattern 2 from `cross-reference-patterns.md`).

| Input Pattern | Resolution Logic |
|---------------|-----------------|
| Room number ("Room 204", "204") | Match `room_schedule[].room_number` |
| Floor reference ("second floor", "Level 2", "2nd floor") | Match `floor_levels[].name`; normalize ordinals ("second" → "2", "third" → "3") |
| Building area ("east wing", "Building A") | Fuzzy match `building_areas[].name` |
| Grid reference ("Grid C", "at C-3", "bay C/3") | Match against `grid_lines.columns` and `.rows` |
| Directional ("south side", "north end", "east") | Map to building areas with matching directional names; if no match, check grid extremes |
| Landmark ("by the elevator", "near the lobby", "at the loading dock") | Match against `room_schedule[].room_name` for functional matches |
| Informal zone ("out back", "the parking lot", "the courtyard") | Match against `building_areas[].name` or `site_utilities` context |

### 3.3 Dates and Time Ranges

**Parsing rules:**

| Input | Resolved Range |
|-------|---------------|
| "today" | start = end = TODAY |
| "yesterday" | start = end = TODAY - 1 (skip weekends: if Monday, use previous Friday) |
| "this week" | start = Monday of current week, end = TODAY |
| "last week" | start = Monday of prior week, end = Friday of prior week |
| "this month" | start = 1st of current month, end = TODAY |
| "last month" | start = 1st of prior month, end = last day of prior month |
| "last Tuesday" | most recent Tuesday before TODAY |
| "January", "in February" | start = 1st of named month, end = last day of named month (current year unless specified) |
| "past 30 days", "last 30 days" | start = TODAY - 30, end = TODAY |
| "since [date]" | start = parsed date, end = TODAY |
| Specific date ("February 10", "2/10", "2/10/26") | start = end = parsed date |
| "next week" | start = Monday of next week, end = Friday of next week |
| "coming week" | same as "next week" |

Align with Time-Series Query Patterns in `data-query-patterns.md` Section 12.

### 3.4 Spec Sections

| Input Pattern | Resolution Logic |
|---------------|-----------------|
| CSI format ("05 12 00", "03 30 00") | Direct match to `specs-quality.json` → `spec_sections[].section` |
| Division only ("Division 5", "Div 03") | Match first 2 digits of `spec_sections[].division` |
| Informal name ("the concrete spec", "steel spec") | Map trade keyword to CSI division, then match `spec_sections[].division` |
| Section reference ("Section 3", "section 03 30 00") | Strip "Section" prefix; match as CSI format or division number |

**CSI division keyword mapping:**

| Keywords | Division |
|----------|----------|
| "concrete" | 03 |
| "masonry" | 04 |
| "metals", "steel" | 05 |
| "wood", "carpentry" | 06 |
| "thermal", "insulation", "roofing", "waterproofing" | 07 |
| "doors", "windows", "glazing" | 08 |
| "finishes", "drywall", "painting", "flooring", "ceiling" | 09 |
| "specialties" | 10 |
| "equipment" | 11 |
| "furnishings" | 12 |
| "conveying" (elevator) | 14 |
| "plumbing" | 22 |
| "HVAC", "mechanical" | 23 |
| "electrical" | 26 |
| "fire protection", "sprinkler", "fire alarm" | 21 / 28 |
| "earthwork", "excavation", "sitework" | 31 |
| "exterior improvements", "paving" | 32 |
| "utilities" | 33 |

### 3.5 Activity Names

**Matching strategy:** Fuzzy match against `schedule.json` → `activities[].activity_name`

- Strip common filler words ("the", "that", "our")
- Match keywords against activity names using substring containment
- If no match, try matching against `milestones[].name`
- If still no match, try matching against `critical_path[].name`

### 3.6 Cost Codes / Divisions

**Matching strategy:**
- Numeric input ("03", "Division 5") → match `cost-data.json` → `budget_by_division[].division`
- Trade name ("concrete costs") → map trade to CSI division number via Section 3.4 keyword mapping, then match division

---

## 4. Multi-Step Query Routing

Complex questions require joining data from multiple files in sequence. Each routing defines the step order, intermediate results, and final assembly.

### 4.1 "Is [sub] behind and over budget?"

**Steps:**
1. **Entity extraction:** Identify sub name → resolve via `directory.json`
2. **Schedule adherence:** QP-SUB-01 (attendance + inspection scores) + filter `schedule.json` activities where `assigned_sub` matches → check `percent_complete` vs expected
3. **Cost check:** Map sub's trade to CSI division → QP-COST-01 (budget variance for that division) + QP-COST-04 (labor cost for that sub)
4. **Composite answer:** Combine schedule adherence score with cost variance

**Files touched:** `directory.json` → `labor-tracking.json` → `schedule.json` → `cost-data.json`

### 4.2 "What inspections are needed for the work scheduled this week?"

**Steps:**
1. **Schedule filter:** Get activities from `schedule.json` where `early_start` falls within this week's date range
2. **Work type extraction:** For each activity, extract the work type (from activity name or linked trade)
3. **Hold point lookup:** For each work type, query `specs-quality.json` → `hold_points[]` where `work_type` matches
4. **Already-done check:** Query `inspection-log.json` → filter inspections already completed for those hold points and locations
5. **Result:** List of upcoming required inspections with the activity, hold point, and inspector

**Files touched:** `schedule.json` → `specs-quality.json` → `inspection-log.json`

### 4.3 "Are any late materials going to delay the schedule?"

**Steps:**
1. **Overdue materials:** QP-MAT-01 → get all items past `expected_delivery` that are not delivered
2. **Activity linkage:** QP-MAT-02 → for each overdue item, find linked `schedule.json` activity via `linked_activity_id`
3. **Float analysis:** For each linked activity, check `total_float` — if float is consumed by the delivery delay, flag as schedule-impacting
4. **Critical path check:** Flag any items linked to `is_critical == true` activities

**Files touched:** `procurement-log.json` → `schedule.json`

### 4.4 "How's the project health overall?"

**Steps:**
1. **SPI:** Calculate from `schedule.json` earned value fields → evaluate against `alert-thresholds.md` Section 1.1
2. **CPI:** Calculate from `cost-data.json` earned value fields → evaluate against Section 1.2
3. **FPIR:** Calculate from `quality-data.json` → evaluate against Section 1.3
4. **TRIR:** Calculate from `safety-log.json` → evaluate against Section 1.4
5. **PPC:** Calculate from `schedule.json` lookahead history → evaluate against Section 1.5
6. **Contingency:** Calculate from `cost-data.json` contingency fields → evaluate against Section 1.6
7. **Composite:** Apply severity scoring rubric from `alert-thresholds.md` Section 3

**Files touched:** `schedule.json` → `cost-data.json` → `quality-data.json` → `safety-log.json`

### 4.5 "What's the full story on RFI [number]?"

**Steps:**
1. **RFI lookup:** Find RFI in `rfi-log.json` by number
2. **Linked submittals:** Follow `related_submittals` to `submittal-log.json`
3. **Linked procurement:** Follow `submittal_id` link from `procurement-log.json`
4. **Spec context:** Look up `spec_section` in `specs-quality.json` for requirements context
5. **Schedule impact:** If `schedule_impact != "none"`, check linked activities in `schedule.json`
6. **CO linkage:** Check `change-order-log.json` for `related_rfi` matching this RFI

**Files touched:** `rfi-log.json` → `submittal-log.json` → `procurement-log.json` → `specs-quality.json` → `schedule.json` → `change-order-log.json`

**Cross-reference pattern:** Pattern 5 (RFI -> Submittal -> Procurement Chain)

### 4.6 "What's going on at [location] today?"

**Steps:**
1. **Location resolution:** Pattern 2 (Location -> Grid -> Area -> Room) → resolve to structured spatial references
2. **Scheduled work:** Filter `schedule.json` activities by resolved location where dates overlap TODAY
3. **Workers present:** Filter `labor-tracking.json` daily entries by location and TODAY
4. **Open items:** Filter `punch-list.json` items by location where status is open
5. **Inspections:** Filter `inspection-log.json` by location for today's date
6. **Safety context:** Check `specs-quality.json` safety zones + `safety-log.json` recent incidents at location

**Files touched:** `plans-spatial.json` → `schedule.json` → `labor-tracking.json` → `punch-list.json` → `inspection-log.json` → `specs-quality.json` → `safety-log.json`

### 4.7 "What's our closeout status and what's blocking substantial completion?"

**Steps:**
1. **Closeout overview:** QP-CLO-001 → get completion percentage per system
2. **Blocking items:** Filter `closeout-data.json` systems where `completion_pct < 100` → identify missing components (commissioning, O&M, warranty, training)
3. **Punch items:** Filter `punch-list.json` for items blocking closeout by system
4. **As-built status:** Check `drawing-log.json` for incomplete as-built drawings
5. **Warranty gaps:** QP-CLO-002 → identify warranties not yet received

**Files touched:** `closeout-data.json` → `quality-data.json` → `punch-list.json` → `drawing-log.json` → `directory.json`

**Cross-reference pattern:** Pattern 11 (Closeout -> Quality -> Drawing)

### 4.8 "What are our biggest risks and how do they affect the schedule?"

**Steps:**
1. **Risk ranking:** QP-RSK-001 → get all active risks sorted by exposure
2. **Schedule linkage:** For each top risk with `linked_activity_id`, look up activity in `schedule.json`
3. **Critical path check:** Flag risks linked to critical path activities
4. **Mitigation status:** QP-RSK-002 → check mitigation plan progress for top risks
5. **Delay correlation:** Check `delay-log.json` for any risks that have already materialized

**Files touched:** `risk-register.json` → `schedule.json` → `delay-log.json` → `cost-data.json`

**Cross-reference pattern:** Pattern 8 (Risk -> Schedule -> Cost)

### 4.9 "What's our claims exposure and are we meeting notice deadlines?"

**Steps:**
1. **Claims overview:** QP-CLM-001 → get all active claims with amounts and status
2. **Notice compliance:** QP-CLM-002 → check upcoming and overdue notice deadlines
3. **Evidence chain:** For each claim, follow `related_delay_ids` to `delay-log.json` and `related_co_ids` to `change-order-log.json`
4. **Documentation completeness:** Check `documentation_completeness_pct` for each claim
5. **Total exposure:** Calculate total `claimed_amount` as percentage of contract value from `cost-data.json`

**Files touched:** `claims-log.json` → `delay-log.json` → `change-order-log.json` → `cost-data.json`

**Cross-reference pattern:** Pattern 9 (Claims -> Delay -> CO)

### 4.10 "Are we compliant on environmental requirements?"

**Steps:**
1. **Environmental overview:** QP-ENV-001 → get compliance rates across all categories
2. **SWPPP status:** QP-ENV-002 → check inspection frequency compliance and open corrective actions
3. **LEED tracking:** Filter `leed_credits[]` for at-risk credits
4. **Waste diversion:** Compare `diversion_rate` against target
5. **Permit check:** Verify `permit_expiration` is not approaching

**Files touched:** `environmental-log.json` → `inspection-log.json` → `daily-report-data.json`

**Cross-reference pattern:** Pattern 10 (Environmental -> Inspection -> Safety)

---

## 5. Response Format Templates

Superintendents need fast, scannable answers. Each category has a standard response format. Use these templates — do not produce long paragraphs.

### 5.1 Schedule Response

```
SCHEDULE STATUS — [Activity or Project]
  Status: [On Track / Behind X days / Ahead X days]
  Float: [X days] ([critical / near-critical / healthy])
  Start: [date] (baseline: [date])
  Finish: [date] (baseline: [date])
  % Complete: [X%]
  [If behind]: Primary driver: [reason]
  [If milestone]: Next milestone: [name] — [date] ([status])
```

### 5.2 Subcontractor Response

```
SUB STATUS — [Company Name] ([Trade])
  Foreman: [Name] ([Phone])
  Status: [active / mobilized / demobilized]
  Today's Headcount: [X] workers (expected: [Y])
  Inspection Pass Rate: [X%] ([trend])
  Safety: [X incidents / clean record]
  Schedule: [on track / behind on [activity]]
  [If issues]: Notable: [issue summary]
```

### 5.3 Materials Response

```
MATERIAL STATUS — [Item Name]
  Supplier: [Name]
  Status: [ordered / shipped / delivered / OVERDUE by X days]
  Expected: [date]
  Linked Activity: [activity name] (starts [date])
  Float Impact: [X days] — [no impact / at risk / critical]
  Certs: [verified / pending / missing]
  Cost: $[amount]
```

### 5.4 Cost Response

```
COST STATUS — [Division or Project]
  Budget: $[budgeted]
  Actual: $[actual]
  Variance: $[variance] ([X%] [over/under])
  CPI: [value] ([healthy / warning / critical])
  Contingency: [X%] remaining ($[amount])
  [If COs]: Pending COs: $[amount] ([count] items)
  EAC: $[amount]
```

### 5.5 Quality / Inspection Response

```
INSPECTION STATUS — [Type or Location]
  Result: [PASS / FAIL / conditional]
  Date: [date]
  Inspector: [name]
  Sub: [name]
  Location: [location]
  Spec: [section number] — [requirement]
  [If fail]: Deficiency: [description]
  [If aggregate]: Pass Rate: [X%] ([period])
    FPIR: [X%] ([healthy / warning / critical])
```

### 5.6 Safety Response

```
SAFETY STATUS — [Project or Location]
  TRIR: [value] ([X recordables / Y hours])
  Days Since Last Recordable: [X]
  Near Misses (30 days): [count]
  Open Corrective Actions: [count]
  [If incident]: Last Incident: [date] — [type] — [description]
  [If location query]: Hazard Zones: [fall protection / confined space / etc.]
```

### 5.7 Location Summary Response

```
LOCATION — [Resolved Location Name]
  Grid: [grid reference]  Floor: [floor]  Area: [area]
  ---
  Active Work:
    - [Activity] — [Sub] — [X workers]
  Open Punch Items: [count] ([priority breakdown])
  Inspections Today: [count] ([pass/fail/scheduled])
  Safety Notes: [hazard zones if any]
```

### 5.8 Delay Response

```
DELAY STATUS — [Project or Activity]
  Total Delay Days: [X] (this month: [Y])
  Weather Days: [X]
  Owner-Caused: [X]  Contractor-Caused: [X]
  CO-Related: [X]
  Trend: [accelerating / stable / improving]
  [If activity]: Float Remaining: [X days]
  [If critical]: Critical Path Impact: [description]
```

### 5.9 RFI / Submittal Response

```
[RFI or SUBMITTAL] STATUS — [ID]: [Subject]
  Status: [status]
  Issued: [date]  Age: [X days]
  [If RFI]: Directed To: [party]
  [If submittal]: Spec Section: [number]
  Schedule Impact: [none / minor / major]
  Linked Items: [related RFIs, submittals, or procurement]
  [If open]: Action Needed: [who needs to do what]
```

### 5.10 Closeout Response

```
CLOSEOUT STATUS — [System or Project]
  Overall Completion: [X%]
  Commissioning: [status] ([X/Y tests complete])
  O&M Manuals: [status]
  Warranties: [X/Y received]
  Training: [status]
  Open Punch Items: [count] ([priority breakdown])
  As-Built Drawings: [X/Y submitted]
  [If warranty query]: Expiring Within 90 Days: [count]
    - [Item]: [Sub] — expires [date] ([X days])
```

### 5.11 Risk Response

```
RISK STATUS — [Risk ID or Project]
  Active Risks: [count] (Critical: [X], High: [Y], Medium: [Z])
  Top Risk: [description] (exposure: [score])
  Risk Contingency: $[allocated] allocated, $[spent] spent ($[remaining] remaining)
  Mitigation Completion: [X%] ([Y overdue])
  [If specific risk]: RSK-[NNN]: [description]
    Probability: [X] | Impact: [Y] | Exposure: [score]
    Owner: [name] | Status: [status]
    Mitigation: [plan] — [status]
    Schedule Link: [activity] ([critical path status])
```

### 5.12 Claims Response

```
CLAIMS STATUS — [Claim ID or Project]
  Active Claims: [count] | Total Claimed: $[amount]
  [If specific claim]: CLM-[NNN]: [description]
    Type: [type] | Status: [status]
    Amount: $[amount] | Days: [X]
    Documentation: [X%] complete
    Notice: [sent/pending] ([deadline info])
    Supporting Delays: [delay list]
    Related COs: [CO list]
  [If overview]: By Status: [status breakdown]
  Upcoming Notice Deadlines: [count within 14 days]
```

### 5.13 Environmental Response

```
ENVIRONMENTAL STATUS — [Category or Project]
  LEED: [target level] — [points achieved]/[points available] ([X%])
    At-Risk Credits: [list]
  SWPPP: [compliance rate]%
    Last Inspection: [date] — [result]
    Next Due: [date] ([X days])
    Open Corrective Actions: [count]
    Permit Expires: [date] ([X days])
  Waste Diversion: [rate]% (target: [target]%)
  Hazmat: [incident count] incidents ([open count] open)
```

### 5.14 Annotation Response

```
ANNOTATION STATUS — [Document or Project]
  Total Annotations: [count] ([period])
  Unresolved: [count] (avg age: [X days])
  [If document-specific]: [Document ID] — [title]
    Open: [count] | In Review: [count] | Resolved: [count]
  [If unresolved focus]:
    By Assigned To: [party breakdown]
    Oldest: ANN-[NNN] — [description] ([X days], assigned to [party])
  [If activity focus]: This Week: [count] new annotations
    Top Authors: [author list with counts]
```

### 5.15 Daily Summary Response

```
DAILY SUMMARY — [Date]
  Weather: [temp], [conditions], [precipitation]
  Total Headcount: [X workers], [Y subs on site]
  Key Work Performed:
    - [Location]: [Sub] — [work description]
    - [Location]: [Sub] — [work description]
  Issues/Delays: [count items]
  Inspections: [X pass, Y fail, Z scheduled]
  Safety: [incidents or "No incidents"]
```

---

## 6. Fallback / Disambiguation Prompts

When the agent cannot determine intent or finds ambiguous entities, use these follow-up templates rather than guessing.

### 6.1 Ambiguous Sub Name

```
I found [X] subs matching "[input]":
  1. [Full Name 1] ([Trade 1]) — [status]
  2. [Full Name 2] ([Trade 2]) — [status]
  3. [Full Name 3] ([Trade 3]) — [status]
Which one did you mean?
```

### 6.2 Ambiguous Location

```
"[input]" could refer to:
  1. [Location A] — [Floor], [Area], Grid [X]
  2. [Location B] — [Floor], [Area], Grid [Y]
Which area are you asking about?
```

### 6.3 Ambiguous Time Frame

```
Do you want:
  1. This week's lookahead ([start] to [end])
  2. The full project schedule
  3. A specific date range
```

### 6.4 Missing Data

```
I don't have [data type] loaded yet. This requires:
  - [File name] (populated by [command/skill])
  - Run [/command] to load this data
[If partial]: I can answer with what's available, but the [missing piece] won't be included.
```

### 6.5 Category Unclear

```
I want to make sure I get you the right answer. Are you asking about:
  1. [Interpretation A] — I'd check [file/metric]
  2. [Interpretation B] — I'd check [file/metric]
```

### 6.6 Compound Question Confirmation

```
That's a multi-part question. Let me break it down:
  1. [Part A] — from [file]
  2. [Part B] — from [file]
  3. [Part C] — from [files, joined]
I'll pull all three. Anything else you want included?
```

---

## 7. Query Construction Reference

### 7.1 Single-File Query Template

```
FILE: [filename.json]
FILTER: [field] [operator] [value]
FIELDS: [field1], [field2], [field3]
SORT: [field] [ASC/DESC]
LIMIT: [N] (if applicable)
AGGREGATION: [count/sum/avg/min/max/group_by]
```

### 7.2 Multi-File Join Template

```
PRIMARY: [filename.json] → [fields]
  FILTER: [condition]
JOIN: [filename2.json] → [fields]
  ON: [primary.key] == [secondary.key]
  (see Join Key Reference Table, data-query-patterns.md Section 6)
DERIVED: [calculated field] = [formula]
SORT: [field] [ASC/DESC]
```

### 7.3 Time-Series Query Template

```
FILE: [filename.json]
DATE_FIELD: [field path]
RANGE: [start_date] to [end_date]
  (see date parsing rules, Section 3.3)
PERIOD: [daily/weekly/monthly]
AGGREGATION: [per-period calculation]
TREND: [3-period rolling comparison per alert-thresholds.md Section 4]
```

---

## 8. Data Freshness and Confidence

Before returning any answer, the agent should check data freshness and communicate confidence.

### 8.1 Freshness Check

Read `project-config.json` → `documents_loaded[]` to determine when data was last extracted:
- **Fresh** (loaded within 7 days): Report data normally
- **Aging** (loaded 7-30 days ago): Include note: "Data last updated [X days ago] on [date]"
- **Stale** (loaded 30+ days ago): Include warning: "This data is [X days old] and may not reflect current conditions. Consider re-running /process-docs."

### 8.2 Confidence Indicators

When data is incomplete or derived from multiple sources with varying confidence:

| Confidence | Condition | Display |
|-----------|-----------|---------|
| High | Data from primary file, recently updated, exact match | No qualifier needed |
| Medium | Data joined across files, or entity resolution used fuzzy matching | "Based on available data" |
| Low | Partial data, stale files, or multiple disambiguation assumptions | "Approximate — [specific caveat]" |

### 8.3 Missing File Handling

If a required JSON file does not exist or is empty:
1. Do not fail the query
2. Answer with whatever data is available from other files
3. Explicitly state what data is missing: "I don't have [file] data loaded, so I can't include [specific data point]. Run `/process-docs` with [document type] to populate this."
