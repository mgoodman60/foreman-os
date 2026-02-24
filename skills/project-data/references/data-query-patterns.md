---
name: data-query-patterns
description: Cross-file query patterns for common construction project analysis scenarios. Documents join logic, filter conditions, aggregation methods, and output formats for multi-file data queries used by the dashboard-intelligence-analyst and project-data-navigator agents.
version: 1.0.0
---

# Data Query Patterns Reference

This document defines reusable cross-file query patterns for analyzing construction project data across the 28-file JSON data store. Each pattern specifies the files to read, fields to extract, join/filter logic, aggregation method, and example output format.

---

## 1. Material / Procurement Queries

### QP-MAT-01: Overdue Materials

**Description**: Identify all procurement items that have not been delivered by their expected delivery date.

**Files**: `procurement-log.json`

**Fields**:
- `items[].item_name`
- `items[].expected_delivery`
- `items[].delivery_status`
- `items[].supplier`
- `items[].spec_section`

**Filter logic**:
```
items.filter(item =>
  item.expected_delivery < TODAY
  AND item.delivery_status != "delivered"
)
.sort_by(expected_delivery ASC)
```

**Aggregation**: Count of overdue items; group by supplier

**Example output**:
```json
{
  "overdue_count": 4,
  "items": [
    {
      "item_name": "Structural Steel W12x26",
      "expected_delivery": "2026-02-10",
      "days_overdue": 13,
      "supplier": "Allied Steel",
      "spec_section": "05 12 00",
      "delivery_status": "in_transit"
    }
  ],
  "by_supplier": { "Allied Steel": 2, "Valley Concrete": 1, "Metro Electric": 1 }
}
```

### QP-MAT-02: Material-to-Activity Linkage

**Description**: For each pending material delivery, identify the schedule activity that depends on it and calculate the impact of late delivery.

**Files**: `procurement-log.json`, `schedule.json`

**Fields**:
- `procurement-log.json` → `items[].item_name`, `items[].expected_delivery`, `items[].delivery_status`, `items[].linked_activity_id`
- `schedule.json` → `activities[].activity_id`, `activities[].activity_name`, `activities[].early_start`, `activities[].total_float`

**Join logic**:
```
procurement_items
  .join(schedule_activities)
  .on(item.linked_activity_id == activity.activity_id)
```

**Filter**: `item.delivery_status != "delivered"`

**Derived field**: `delivery_gap = item.expected_delivery - activity.early_start` (negative means material arrives after activity needs to start)

**Aggregation**: List sorted by delivery_gap ascending (most impactful first)

**Example output**:
```json
{
  "material_activity_links": [
    {
      "material": "Structural Steel W12x26",
      "expected_delivery": "2026-02-10",
      "activity": "Steel Erection - Level 2",
      "activity_start": "2026-02-05",
      "delivery_gap_days": -5,
      "activity_float_days": 3,
      "net_impact_days": -2,
      "on_critical_path": true
    }
  ]
}
```

### QP-MAT-03: Certification Status Check

**Description**: Find delivered materials that are missing required certifications or test reports.

**Files**: `procurement-log.json`, `specs-quality.json`

**Fields**:
- `procurement-log.json` → `items[].item_name`, `items[].delivery_status`, `items[].cert_status`, `items[].delivery_date`, `items[].spec_section`
- `specs-quality.json` → `sections[].section_number`, `sections[].testing_requirements[]`

**Filter logic**:
```
items.filter(item =>
  item.delivery_status == "delivered"
  AND (item.cert_status != "verified" OR item.cert_status IS NULL)
)
```

**Join**: Match `item.spec_section` to `section.section_number` to retrieve the required testing/certification list

**Aggregation**: Count uncertified; group by spec section

### QP-MAT-04: Material Cost Tracking

**Description**: Compare actual procurement costs against budget allocations for each material category.

**Files**: `procurement-log.json`, `cost-data.json`

**Fields**:
- `procurement-log.json` → `items[].item_name`, `items[].actual_cost`, `items[].spec_section`
- `cost-data.json` → `divisions[].division_number`, `divisions[].budgeted_cost`, `divisions[].actual_cost`

**Join**: Map `item.spec_section` (first 2 digits) to `division.division_number`

**Aggregation**: Sum actual procurement costs per division; compare to budgeted amounts; calculate variance

---

## 2. Subcontractor Queries

### QP-SUB-01: Sub Performance Scorecard

**Description**: Generate a composite performance score for a subcontractor by joining data across attendance, quality, safety, and inspection results.

**Files**: `directory.json`, `labor-tracking.json`, `quality-data.json`, `safety-log.json`, `inspection-log.json`

**Fields**:
- `directory.json` → `subs[].name`, `subs[].trade`, `subs[].contract_value`
- `labor-tracking.json` → `daily_entries[].sub_name`, `daily_entries[].workers_expected`, `daily_entries[].workers_present`
- `quality-data.json` → `first_pass_inspection_results[].sub_name`, `first_pass_inspection_results[].result`
- `safety-log.json` → `incidents[].sub_name`, `incidents[].severity`
- `inspection-log.json` → `inspections[].sub_name`, `inspections[].result`

**Join key**: `sub_name` across all files (see Join Key Reference Table below)

**Filter**: Specify sub name or trade to filter; or generate for all subs

**Aggregation**:
```
For each sub:
  attendance_rate = sum(workers_present) / sum(workers_expected) * 100
  inspection_pass_rate = count(result == "pass") / count(all_inspections) * 100
  safety_incidents = count(incidents for sub)
  quality_fpir = count(first_pass_fail) / count(first_pass_total) * 100
  composite_score = (attendance * 0.25) + (inspection_pass * 0.30) + (safety_score * 0.25) + (quality_score * 0.20)
```

**Example output**:
```json
{
  "sub_name": "Walker Concrete",
  "trade": "Concrete",
  "attendance_rate": 92.5,
  "inspection_pass_rate": 87.3,
  "safety_incidents": 0,
  "first_pass_rejection_rate": 12.7,
  "composite_score": 88.4,
  "trend": "stable",
  "period": "2026-01-01 to 2026-02-23"
}
```

### QP-SUB-02: Sub Mobilization Status vs Schedule Need

**Description**: Compare which subs are currently on site vs which subs are needed based on upcoming schedule activities.

**Files**: `directory.json`, `labor-tracking.json`, `schedule.json`

**Fields**:
- `directory.json` → `subs[].name`, `subs[].trade`, `subs[].scope_activities[]`
- `labor-tracking.json` → `daily_entries[].sub_name`, `daily_entries[].date`, `daily_entries[].workers_present`
- `schedule.json` → `activities[].activity_name`, `activities[].assigned_sub`, `activities[].early_start`, `activities[].early_finish`

**Logic**:
```
subs_on_site = labor_tracking
  .filter(entry.date == TODAY AND entry.workers_present > 0)
  .distinct(sub_name)

subs_needed = schedule_activities
  .filter(activity.early_start <= TODAY + 14 AND activity.early_finish >= TODAY)
  .distinct(assigned_sub)

missing = subs_needed - subs_on_site
unexpected = subs_on_site - subs_needed
```

**Aggregation**: Lists of missing, present, and unexpected subs with activity context

### QP-SUB-03: Sub Headcount Trends

**Description**: Track a specific sub's headcount over time to identify mobilization/demobilization patterns.

**Files**: `labor-tracking.json`

**Fields**: `daily_entries[].sub_name`, `daily_entries[].date`, `daily_entries[].workers_present`, `daily_entries[].hours_worked`

**Filter**: `sub_name == {target_sub}` AND `date BETWEEN {start_date} AND {end_date}`

**Aggregation**: Daily headcount series; calculate 7-day rolling average; identify peaks and valleys

### QP-SUB-04: Sub Quality Metrics

**Description**: Calculate inspection pass rate for a specific sub from inspection log data.

**Files**: `inspection-log.json`, `directory.json`

**Fields**:
- `inspection-log.json` → `inspections[].sub_name`, `inspections[].result`, `inspections[].inspection_type`, `inspections[].date`, `inspections[].location`
- `directory.json` → `subs[].name`, `subs[].trade`

**Filter**: `sub_name == {target_sub}` AND date range

**Aggregation**: pass_rate = count(pass) / count(all) * 100; group by inspection_type and by month

---

## 3. Schedule Queries

### QP-SCH-01: Critical Path Status with Float Analysis

**Description**: Extract all critical and near-critical activities with current float values.

**Files**: `schedule.json`

**Fields**: `activities[].activity_id`, `activities[].activity_name`, `activities[].total_float`, `activities[].early_start`, `activities[].early_finish`, `activities[].actual_start`, `activities[].actual_finish`, `activities[].percent_complete`, `activities[].is_critical`

**Filter**: `is_critical == true` OR `total_float <= 5`

**Sort**: `total_float ASC`, then `early_start ASC`

**Aggregation**: Count of critical activities; average float; count of near-critical (float 1-5 days)

### QP-SCH-02: Milestone Tracking with Earned Value

**Description**: Report on milestone status with associated earned value data.

**Files**: `schedule.json`, `cost-data.json`

**Fields**:
- `schedule.json` → `milestones[].name`, `milestones[].baseline_date`, `milestones[].forecast_date`, `milestones[].actual_date`, `milestones[].status`
- `cost-data.json` → `earned_value.bcwp`, `earned_value.bcws`, `earned_value.acwp` (snapshot at milestone date)

**Derived fields**:
- `variance_days = forecast_date - baseline_date`
- `spi_at_milestone = bcwp / bcws`
- `cpi_at_milestone = bcwp / acwp`

**Sort**: `baseline_date ASC`

### QP-SCH-03: Activity Completion vs Plan (PPC)

**Description**: Calculate Percent Plan Complete for a given lookahead period.

**Files**: `schedule.json`

**Fields**: `lookahead_history[].period_start`, `lookahead_history[].period_end`, `lookahead_history[].activities_planned`, `lookahead_history[].activities_completed`, `lookahead_history[].reasons_for_misses[]`

**Filter**: `period_start >= {target_period_start}` AND `period_end <= {target_period_end}`

**Calculation**: `PPC = activities_completed / activities_planned * 100`

**Aggregation**: PPC per period; trend over multiple periods; top miss reasons by frequency

### QP-SCH-04: Schedule-Cost Alignment

**Description**: Correlate SPI and CPI to identify whether schedule and cost performance are moving in the same direction.

**Files**: `schedule.json`, `cost-data.json`

**Fields**:
- `schedule.json` → `earned_value.bcwp`, `earned_value.bcws` (periodic snapshots)
- `cost-data.json` → `earned_value.bcwp`, `earned_value.acwp` (periodic snapshots)

**Calculation**: SPI = BCWP/BCWS; CPI = BCWP/ACWP; correlation = SPI - CPI (positive = cost worse than schedule, negative = schedule worse than cost)

**Aggregation**: Time series of SPI, CPI, and their divergence

---

## 4. Location Queries

### QP-LOC-01: Activity by Location

**Description**: Show all current and upcoming activities filtered by a specific grid reference, building area, or room.

**Files**: `plans-spatial.json`, `schedule.json`, `daily-report-data.json`

**Fields**:
- `plans-spatial.json` → `grid_lines[]`, `rooms[].room_number`, `rooms[].floor`, `building_areas[].area_name`
- `schedule.json` → `activities[].location`, `activities[].activity_name`, `activities[].early_start`, `activities[].percent_complete`
- `daily-report-data.json` → `entries[].location`, `entries[].work_description`, `entries[].date`

**Join**: Match `activity.location` and `entry.location` against `plans-spatial` grid/room identifiers using substring or pattern matching

**Filter**: Location matches user-specified grid, room, or area

### QP-LOC-02: Punch List by Location

**Description**: List all open punch items for a specific location.

**Files**: `punch-list.json`, `plans-spatial.json`

**Fields**:
- `punch-list.json` → `items[].description`, `items[].location`, `items[].responsible_sub`, `items[].status`, `items[].date_identified`, `items[].priority`
- `plans-spatial.json` → `rooms[].room_number`, `rooms[].floor`

**Filter**: `item.location` matches target AND `item.status != "resolved"`

**Sort**: `priority DESC`, `date_identified ASC`

### QP-LOC-03: Inspection Results by Location

**Description**: Aggregate inspection pass/fail results for a specific location to identify quality hotspots.

**Files**: `inspection-log.json`, `plans-spatial.json`

**Fields**:
- `inspection-log.json` → `inspections[].location`, `inspections[].result`, `inspections[].inspection_type`, `inspections[].date`, `inspections[].sub_name`

**Filter**: `inspection.location` matches target location

**Aggregation**: pass_count, fail_count, pass_rate; group by inspection_type

### QP-LOC-04: Resource Allocation by Building Area

**Description**: Show total headcount and trades currently working in each building area.

**Files**: `labor-tracking.json`, `plans-spatial.json`

**Fields**:
- `labor-tracking.json` → `daily_entries[].location`, `daily_entries[].sub_name`, `daily_entries[].trade`, `daily_entries[].workers_present`, `daily_entries[].date`
- `plans-spatial.json` → `building_areas[].area_name`

**Filter**: `entry.date == TODAY` (or target date range)

**Aggregation**: Sum workers_present by building_area, then by trade within each area

---

## 5. Cost Queries

### QP-COST-01: Budget Variance by Division

**Description**: Calculate cost variance for each CSI division.

**Files**: `cost-data.json`

**Fields**: `divisions[].division_number`, `divisions[].division_name`, `divisions[].budgeted_cost`, `divisions[].actual_cost`, `divisions[].committed_cost`

**Calculation**:
```
variance = budgeted_cost - actual_cost - committed_cost
variance_pct = variance / budgeted_cost * 100
```

**Sort**: `variance ASC` (worst overruns first)

**Aggregation**: Total budget, total actual, total variance; count of divisions over/under

### QP-COST-02: Contingency Drawdown Tracking

**Description**: Track contingency usage over time.

**Files**: `cost-data.json`, `change-order-log.json`

**Fields**:
- `cost-data.json` → `contingency.original_amount`, `contingency.committed`, `contingency.spent`, `contingency.history[]`
- `change-order-log.json` → `change_orders[].amount`, `change_orders[].status`, `change_orders[].date_approved`, `change_orders[].contingency_funded`

**Calculation**:
```
remaining = original_amount - committed - spent
remaining_pct = remaining / original_amount * 100
burn_rate = spent / months_elapsed
months_remaining = remaining / burn_rate
exhaustion_date = today + months_remaining
```

### QP-COST-03: Change Order Impact Analysis

**Description**: Summarize all change orders with their cost and schedule impacts.

**Files**: `change-order-log.json`, `schedule.json`, `cost-data.json`

**Fields**:
- `change-order-log.json` → `change_orders[].co_number`, `change_orders[].description`, `change_orders[].amount`, `change_orders[].status`, `change_orders[].schedule_impact_days`, `change_orders[].division`
- `schedule.json` → `activities[]` (impacted activities)
- `cost-data.json` → `contingency` (funding source)

**Aggregation**: Total approved CO value; total pending CO value; total schedule impact days; group by status (approved/pending/rejected)

### QP-COST-04: Labor Cost vs Budget

**Description**: Compare actual labor costs from tracking against budgeted labor amounts.

**Files**: `labor-tracking.json`, `cost-data.json`

**Fields**:
- `labor-tracking.json` → `daily_entries[].hours_worked`, `daily_entries[].cost_code`, `daily_entries[].hourly_rate`
- `cost-data.json` → `divisions[].budgeted_labor_cost`

**Join**: Map `cost_code` to division number

**Calculation**: actual_labor = sum(hours_worked * hourly_rate) per cost code; compare to budgeted_labor_cost per division

---

## 6. Closeout Queries

### QP-CLO-001: Closeout Completion Status by System

**Description**: Track closeout completion percentage for each building system (HVAC, plumbing, electrical, fire protection, etc.) including commissioning, punch list, O&M manuals, and warranty documentation.

**Files**: `closeout-data.json`, `quality-data.json`, `punch-list.json`

**Fields**:
- `closeout-data.json` → `systems[].system_name`, `systems[].commissioning_status`, `systems[].oam_manual_status`, `systems[].warranty_status`, `systems[].training_status`, `systems[].completion_pct`
- `quality-data.json` → `system_tests[].system`, `system_tests[].result`
- `punch-list.json` → `items[].system`, `items[].status`

**Join logic**:
```
closeout_systems
  .join(quality_system_tests)
  .on(system.system_name == system_test.system)
  .join(punch_items)
  .on(system.system_name == punch_item.system)
```

**Filter**: Optional — filter by `system.completion_pct < 100` for incomplete systems only

**Aggregation**: Average completion percentage across all systems; count of systems by status tier (complete/in-progress/not-started); breakdown by closeout component (commissioning, O&M, warranty, training)

**Example output**:
```json
{
  "overall_closeout_pct": 62.5,
  "systems": [
    {
      "system_name": "HVAC",
      "completion_pct": 85,
      "commissioning_status": "complete",
      "oam_manual_status": "submitted",
      "warranty_status": "received",
      "training_status": "scheduled",
      "open_punch_items": 3,
      "test_pass_rate": 92.0
    }
  ],
  "by_status": { "complete": 2, "in_progress": 5, "not_started": 1 }
}
```

### QP-CLO-002: Warranty Expiration Timeline

**Description**: List all warranties with expiration dates, grouped by time horizon, to identify upcoming expirations that require final walkthroughs or inspections before coverage ends.

**Files**: `closeout-data.json`, `directory.json`

**Fields**:
- `closeout-data.json` → `warranties[].item`, `warranties[].sub_name`, `warranties[].start_date`, `warranties[].expiration_date`, `warranties[].warranty_type`, `warranties[].duration_months`
- `directory.json` → `subcontractors[].name`, `subcontractors[].phone`

**Join logic**:
```
warranties
  .join(directory_subs)
  .on(warranty.sub_name == sub.name)
```

**Filter logic**:
```
warranties.filter(warranty =>
  warranty.expiration_date >= TODAY
)
.sort_by(expiration_date ASC)
```

**Derived field**: `days_until_expiration = warranty.expiration_date - TODAY`

**Aggregation**: Count of warranties expiring within 30/60/90 days; group by warranty_type (manufacturer/installer/extended)

**Example output**:
```json
{
  "expiring_30_days": 2,
  "expiring_60_days": 5,
  "expiring_90_days": 8,
  "warranties": [
    {
      "item": "Roofing membrane",
      "sub_name": "Summit Roofing",
      "sub_phone": "555-0145",
      "warranty_type": "manufacturer",
      "expiration_date": "2026-03-15",
      "days_until_expiration": 19
    }
  ]
}
```

---

## 7. Risk Queries

### QP-RSK-001: Active Risks by Severity Level

**Description**: Retrieve all active risk entries from the risk register, scored by probability and impact, sorted by risk exposure (probability x impact).

**Files**: `risk-register.json`, `schedule.json`

**Fields**:
- `risk-register.json` → `risks[].risk_id`, `risks[].description`, `risks[].category`, `risks[].probability`, `risks[].impact`, `risks[].risk_owner`, `risks[].status`, `risks[].linked_activity_id`
- `schedule.json` → `activities[].activity_id`, `activities[].activity_name`, `activities[].is_critical`

**Join logic**:
```
risks
  .join(schedule_activities)
  .on(risk.linked_activity_id == activity.activity_id)
```

**Filter**: `risk.status == "active"`

**Derived field**: `risk_exposure = risk.probability * risk.impact`

**Sort**: `risk_exposure DESC`

**Aggregation**: Count of risks by severity band (critical/high/medium/low); count by category (schedule/cost/safety/quality/external); total risk exposure score

**Example output**:
```json
{
  "active_risk_count": 12,
  "total_exposure": 284,
  "risks": [
    {
      "risk_id": "RSK-003",
      "description": "Steel delivery delay due to supplier capacity constraints",
      "category": "schedule",
      "probability": 0.7,
      "impact": 8,
      "risk_exposure": 5.6,
      "severity": "critical",
      "risk_owner": "Project Manager",
      "linked_activity": "Steel Erection - Level 2",
      "on_critical_path": true
    }
  ],
  "by_severity": { "critical": 2, "high": 4, "medium": 4, "low": 2 },
  "by_category": { "schedule": 4, "cost": 3, "safety": 2, "quality": 2, "external": 1 }
}
```

### QP-RSK-002: Risk Mitigation Status and Contingency Burn Rate

**Description**: Track the status of mitigation plans for active risks and calculate the burn rate of risk contingency funds.

**Files**: `risk-register.json`, `cost-data.json`

**Fields**:
- `risk-register.json` → `risks[].risk_id`, `risks[].description`, `risks[].mitigation_plan`, `risks[].mitigation_status`, `risks[].contingency_allocated`, `risks[].contingency_spent`, `risks[].trigger_date`
- `cost-data.json` → `contingency.original_amount`, `contingency.committed`, `contingency.spent`

**Filter**: `risk.status == "active"` AND `risk.mitigation_plan IS NOT NULL`

**Derived fields**:
```
risk_contingency_burn_rate = sum(risks.contingency_spent) / months_elapsed
risk_contingency_remaining = sum(risks.contingency_allocated) - sum(risks.contingency_spent)
mitigation_completion_rate = count(mitigation_status == "complete") / count(all_active_mitigations) * 100
```

**Aggregation**: Total contingency allocated to risks vs spent; mitigation plan completion rate; list of overdue mitigations (trigger_date < TODAY and mitigation_status != "complete")

**Example output**:
```json
{
  "total_risk_contingency_allocated": 450000,
  "total_risk_contingency_spent": 125000,
  "risk_contingency_remaining": 325000,
  "burn_rate_per_month": 31250,
  "mitigation_completion_rate": 58.3,
  "overdue_mitigations": [
    {
      "risk_id": "RSK-005",
      "description": "Concrete supply chain disruption",
      "mitigation_plan": "Pre-qualify alternate supplier",
      "trigger_date": "2026-02-01",
      "mitigation_status": "in_progress"
    }
  ]
}
```

---

## 8. Claims Queries

### QP-CLM-001: Active Claims by Status and Value

**Description**: List all active claims with their current status, claimed amounts, and documentation completeness.

**Files**: `claims-log.json`, `delay-log.json`, `change-order-log.json`

**Fields**:
- `claims-log.json` → `claims[].claim_id`, `claims[].description`, `claims[].status`, `claims[].claimed_amount`, `claims[].claim_type`, `claims[].date_filed`, `claims[].documentation_completeness_pct`, `claims[].related_delay_ids`, `claims[].related_co_ids`
- `delay-log.json` → `delays[].delay_id`, `delays[].delay_days`, `delays[].cause`
- `change-order-log.json` → `change_orders[].co_number`, `change_orders[].status`, `change_orders[].amount`

**Join logic**:
```
claims
  .join(delay_events)
  .on(claim.related_delay_ids CONTAINS delay.delay_id)
  .join(change_orders)
  .on(claim.related_co_ids CONTAINS co.co_number)
```

**Filter**: `claim.status IN ("draft", "notice_sent", "filed", "under_review", "negotiation")`

**Sort**: `claimed_amount DESC`

**Aggregation**: Total claimed amount by status; count of claims by type (time_extension/cost/acceleration/differing_conditions); total associated delay days

**Example output**:
```json
{
  "active_claims_count": 4,
  "total_claimed_amount": 875000,
  "claims": [
    {
      "claim_id": "CLM-002",
      "description": "Differing site conditions — unexpected rock at foundation",
      "status": "filed",
      "claim_type": "differing_conditions",
      "claimed_amount": 350000,
      "date_filed": "2026-01-15",
      "documentation_completeness_pct": 85,
      "associated_delay_days": 14,
      "related_co": "CO-012 (pending)"
    }
  ],
  "by_status": { "notice_sent": 1, "filed": 2, "negotiation": 1 },
  "by_type": { "time_extension": 1, "differing_conditions": 2, "cost": 1 }
}
```

### QP-CLM-002: Claims Notice Deadline Tracking

**Description**: Track notice period deadlines for active claims and potential claims to ensure contractual notice requirements are met.

**Files**: `claims-log.json`

**Fields**:
- `claims-log.json` → `claims[].claim_id`, `claims[].description`, `claims[].notice_required_by`, `claims[].notice_sent_date`, `claims[].formal_claim_deadline`, `claims[].status`, `claims[].contract_notice_period_days`

**Filter logic**:
```
claims.filter(claim =>
  (claim.notice_required_by >= TODAY AND claim.notice_sent_date IS NULL)
  OR (claim.formal_claim_deadline >= TODAY AND claim.status == "notice_sent")
)
.sort_by(notice_required_by ASC)
```

**Derived fields**:
```
days_until_notice_deadline = claim.notice_required_by - TODAY
days_until_formal_deadline = claim.formal_claim_deadline - TODAY
notice_compliance = claim.notice_sent_date <= claim.notice_required_by
```

**Aggregation**: Count of claims with upcoming notice deadlines within 7/14/30 days; count of overdue notices

**Example output**:
```json
{
  "upcoming_deadlines": [
    {
      "claim_id": "CLM-004",
      "description": "Owner-directed acceleration costs",
      "notice_required_by": "2026-03-01",
      "days_until_deadline": 5,
      "contract_notice_period_days": 21,
      "status": "draft",
      "action_needed": "Send written notice within 5 days"
    }
  ],
  "deadlines_within_7_days": 1,
  "deadlines_within_14_days": 2,
  "overdue_notices": 0
}
```

---

## 9. Environmental Queries

### QP-ENV-001: Environmental Compliance Rate by Category

**Description**: Calculate compliance rates across environmental categories including LEED credits, waste diversion, SWPPP, and hazmat management.

**Files**: `environmental-log.json`

**Fields**:
- `environmental-log.json` → `leed_credits[].credit_id`, `leed_credits[].status`, `leed_credits[].points_available`, `leed_credits[].points_achieved`
- `environmental-log.json` → `waste_diversion.total_waste_tons`, `waste_diversion.diverted_tons`, `waste_diversion.diversion_rate`
- `environmental-log.json` → `swppp.inspections[].date`, `swppp.inspections[].result`, `swppp.inspections[].corrective_actions`
- `environmental-log.json` → `hazmat.incidents[].date`, `hazmat.incidents[].type`, `hazmat.incidents[].status`

**Aggregation**:
```
leed_compliance = sum(points_achieved) / sum(points_available) * 100
waste_diversion_rate = diverted_tons / total_waste_tons * 100
swppp_compliance = count(inspections where result == "pass") / count(all_inspections) * 100
hazmat_incident_rate = count(hazmat_incidents) / project_months
```

**Example output**:
```json
{
  "leed": {
    "target_level": "Gold",
    "points_achieved": 48,
    "points_available": 60,
    "compliance_pct": 80.0,
    "at_risk_credits": ["MR Credit 2 — Construction Waste", "SS Credit 7.1 — Heat Island"]
  },
  "waste_diversion": {
    "total_waste_tons": 245,
    "diverted_tons": 183,
    "diversion_rate": 74.7,
    "target_rate": 75.0,
    "gap": -0.3
  },
  "swppp": {
    "inspections_total": 24,
    "inspections_passed": 22,
    "compliance_rate": 91.7,
    "open_corrective_actions": 1
  },
  "hazmat": {
    "incidents_total": 2,
    "open_incidents": 0,
    "incident_rate_per_month": 0.25
  }
}
```

### QP-ENV-002: SWPPP Inspection Status

**Description**: Track SWPPP inspection compliance, including inspection frequency, results, and outstanding corrective actions.

**Files**: `environmental-log.json`, `inspection-log.json`

**Fields**:
- `environmental-log.json` → `swppp.inspections[].date`, `swppp.inspections[].inspector`, `swppp.inspections[].result`, `swppp.inspections[].findings[]`, `swppp.inspections[].corrective_actions[].description`, `swppp.inspections[].corrective_actions[].status`, `swppp.inspections[].corrective_actions[].due_date`
- `environmental-log.json` → `swppp.permit_expiration`, `swppp.required_frequency`
- `inspection-log.json` → `inspections[]` (for cross-reference with general inspection log)

**Filter logic**:
```
swppp.inspections
  .sort_by(date DESC)

corrective_actions.filter(action =>
  action.status != "resolved"
)
.sort_by(due_date ASC)
```

**Derived fields**:
```
days_since_last_inspection = TODAY - max(swppp.inspections[].date)
next_inspection_due = last_inspection_date + required_frequency_days
inspection_overdue = days_since_last_inspection > required_frequency_days
days_until_permit_expiration = swppp.permit_expiration - TODAY
```

**Aggregation**: Last inspection date and result; days until next required inspection; count of open corrective actions; permit expiration countdown

**Example output**:
```json
{
  "last_inspection": {
    "date": "2026-02-17",
    "result": "pass_with_findings",
    "findings_count": 2
  },
  "next_inspection_due": "2026-02-24",
  "days_until_next": 0,
  "inspection_overdue": false,
  "permit_expiration": "2026-09-30",
  "days_until_permit_expiration": 218,
  "open_corrective_actions": [
    {
      "description": "Repair silt fence at south perimeter",
      "due_date": "2026-02-28",
      "days_until_due": 4
    }
  ]
}
```

---

## 10. Annotation Queries

### QP-ANN-001: Annotation Activity by Document Type

**Description**: Summarize annotation and markup activity across documents, grouped by document type, to identify which document sets have the most active markup and review cycles.

**Files**: `annotation-log.json`, `drawing-log.json`

**Fields**:
- `annotation-log.json` → `annotations[].annotation_id`, `annotations[].document_type`, `annotations[].document_id`, `annotations[].author`, `annotations[].date_created`, `annotations[].annotation_type`, `annotations[].status`
- `drawing-log.json` → `drawings[].sheet_number`, `drawings[].discipline`, `drawings[].current_revision`

**Join logic**:
```
annotations
  .join(drawings)
  .on(annotation.document_id == drawing.sheet_number)
```

**Filter**: Optional — filter by date range or `annotation_type`

**Aggregation**: Count of annotations by document_type (plans/specs/submittals/RFIs); count by annotation_type (comment/markup/revision_cloud/dimension_override); count by author; trend over time (weekly annotation volume)

**Example output**:
```json
{
  "total_annotations": 156,
  "period": "2026-02-01 to 2026-02-24",
  "by_document_type": {
    "plans": 89,
    "specs": 32,
    "submittals": 22,
    "rfis": 13
  },
  "by_annotation_type": {
    "comment": 64,
    "markup": 48,
    "revision_cloud": 28,
    "dimension_override": 16
  },
  "top_authors": [
    { "author": "J. Martinez (Superintendent)", "count": 45 },
    { "author": "A. Chen (Architect)", "count": 38 }
  ],
  "weekly_trend": [
    { "week": "2026-W06", "count": 32 },
    { "week": "2026-W07", "count": 41 },
    { "week": "2026-W08", "count": 83 }
  ]
}
```

### QP-ANN-002: Unresolved Annotations Aging

**Description**: Identify all unresolved annotations with aging analysis to ensure markups, comments, and revision requests are being addressed in a timely manner.

**Files**: `annotation-log.json`

**Fields**:
- `annotation-log.json` → `annotations[].annotation_id`, `annotations[].document_id`, `annotations[].document_type`, `annotations[].description`, `annotations[].author`, `annotations[].assigned_to`, `annotations[].date_created`, `annotations[].status`, `annotations[].priority`

**Filter logic**:
```
annotations.filter(annotation =>
  annotation.status IN ("open", "in_review", "pending_response")
)
.sort_by(date_created ASC)
```

**Derived field**: `age_days = TODAY - annotation.date_created`

**Aggregation**: Count of unresolved by age band (0-7 days, 8-14 days, 15-30 days, 30+ days); count by assigned_to; count by priority; average age of unresolved annotations

**Example output**:
```json
{
  "unresolved_count": 23,
  "average_age_days": 11.4,
  "by_age_band": {
    "0_to_7_days": 8,
    "8_to_14_days": 7,
    "15_to_30_days": 5,
    "over_30_days": 3
  },
  "by_assigned_to": {
    "Architect": 9,
    "Structural Engineer": 6,
    "MEP Engineer": 5,
    "Superintendent": 3
  },
  "oldest_unresolved": {
    "annotation_id": "ANN-034",
    "document_id": "S2.1",
    "description": "Verify column size at Grid D-4 — conflicts with architectural",
    "age_days": 42,
    "assigned_to": "Structural Engineer",
    "priority": "high"
  }
}
```

---

## 11. Join Key Reference Table

This table documents which fields serve as join keys between JSON files, enabling multi-file queries.

| Key Name | Type | Files Using This Key | Field Path |
|----------|------|---------------------|------------|
| sub_name | String | directory.json | subs[].name |
| | | labor-tracking.json | daily_entries[].sub_name |
| | | inspection-log.json | inspections[].sub_name |
| | | quality-data.json | first_pass_inspection_results[].sub_name |
| | | safety-log.json | incidents[].sub_name |
| | | punch-list.json | items[].responsible_sub |
| | | daily-report-data.json | entries[].sub_name |
| activity_id | String | schedule.json | activities[].activity_id |
| | | procurement-log.json | items[].linked_activity_id |
| | | labor-tracking.json | daily_entries[].activity_id |
| | | cost-data.json | earned_value.activity_snapshots[].activity_id |
| location | String | plans-spatial.json | rooms[].room_number, grid_lines[], building_areas[].area_name |
| | | inspection-log.json | inspections[].location |
| | | punch-list.json | items[].location |
| | | labor-tracking.json | daily_entries[].location |
| | | daily-report-data.json | entries[].location |
| | | safety-log.json | incidents[].location |
| spec_section | String | specs-quality.json | sections[].section_number |
| | | procurement-log.json | items[].spec_section |
| | | inspection-log.json | inspections[].spec_section |
| | | submittal-log.json | submittals[].spec_section |
| | | quality-data.json | test_results[].spec_section |
| cost_code | String | cost-data.json | divisions[].division_number |
| | | labor-tracking.json | daily_entries[].cost_code |
| | | change-order-log.json | change_orders[].division |
| | | procurement-log.json | items[].cost_code |
| rfi_number | String | rfi-log.json | rfis[].rfi_number |
| | | delay-log.json | delays[].related_rfi |
| | | change-order-log.json | change_orders[].related_rfi |
| co_number | String | change-order-log.json | change_orders[].co_number |
| | | cost-data.json | contingency.co_draws[].co_number |
| | | delay-log.json | delays[].related_co |
| | | claims-log.json | claims[].related_co_ids[] |
| delay_id | String | delay-log.json | delays[].delay_id |
| | | claims-log.json | claims[].related_delay_ids[] |
| risk_id | String | risk-register.json | risks[].risk_id |
| | | claims-log.json | claims[].related_risk_ids[] |
| claim_id | String | claims-log.json | claims[].claim_id |
| system_name | String | closeout-data.json | systems[].system_name |
| | | quality-data.json | system_tests[].system |
| document_id | String | annotation-log.json | annotations[].document_id |
| | | drawing-log.json | drawings[].sheet_number |
| | | rfi-log.json | rfis[].rfi_number |
| date | Date | All files | Various date fields (used for time-range filtering and period alignment) |

---

## 12. Time-Series Query Patterns

### 12.1 Date Range Filtering

All time-series queries accept a date range defined by `start_date` and `end_date`. Apply filters as:
```
records.filter(record => record.date >= start_date AND record.date <= end_date)
```

Common shorthand ranges:
- "today": `start_date = end_date = TODAY`
- "this week": `start_date = Monday of current week`, `end_date = TODAY`
- "last 30 days": `start_date = TODAY - 30`, `end_date = TODAY`
- "this month": `start_date = first of month`, `end_date = TODAY`
- "last month": `start_date = first of prior month`, `end_date = last of prior month`

### 12.2 Period Comparison

To compare two time periods:
```
period_a_value = aggregate(records.filter(date in period_a))
period_b_value = aggregate(records.filter(date in period_b))
change = period_b_value - period_a_value
change_pct = (change / period_a_value) * 100
```

### 12.3 Trend Calculation

For trend analysis over multiple periods:
```
periods = split_date_range(start_date, end_date, period_length)
values = periods.map(period => aggregate(records.filter(date in period)))
trend_direction = linear_regression_slope(values)
  positive slope → "improving" (for metrics where higher is better)
  negative slope → "improving" (for metrics where lower is better)
  near-zero slope → "stable"
```

---

## 13. Aggregation Patterns

### 13.1 Sum
```
total = records.reduce((sum, record) => sum + record.value, 0)
```
Use for: costs, hours, headcounts, quantities

### 13.2 Count
```
count = records.filter(condition).length
```
Use for: incident counts, inspection counts, item counts

### 13.3 Average
```
average = records.reduce((sum, r) => sum + r.value, 0) / records.length
```
Use for: pass rates, average age, average duration

### 13.4 Min / Max
```
min_value = records.reduce((min, r) => r.value < min ? r.value : min, Infinity)
max_value = records.reduce((max, r) => r.value > max ? r.value : max, -Infinity)
```
Use for: oldest punch item, highest headcount, lowest float

### 13.5 Group By
```
grouped = records.reduce((groups, record) => {
  key = record[group_field]
  groups[key] = groups[key] || []
  groups[key].push(record)
  return groups
}, {})
```
Use for: breakdown by sub, by trade, by location, by division, by inspection type

### 13.6 Distinct
```
unique_values = [...new Set(records.map(r => r[field]))]
```
Use for: list of subs on site, list of active trades, list of impacted locations
