---
name: data-query-patterns
description: Cross-file query patterns for common construction project analysis scenarios. Documents join logic, filter conditions, aggregation methods, and output formats for multi-file data queries used by the dashboard-intelligence-analyst and project-data-navigator agents.
version: 1.0.0
---

# Data Query Patterns Reference

This document defines reusable cross-file query patterns for analyzing construction project data across the 23-file JSON data store. Each pattern specifies the files to read, fields to extract, join/filter logic, aggregation method, and example output format.

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

## 6. Join Key Reference Table

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
| date | Date | All files | Various date fields (used for time-range filtering and period alignment) |

---

## 7. Time-Series Query Patterns

### 7.1 Date Range Filtering

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

### 7.2 Period Comparison

To compare two time periods:
```
period_a_value = aggregate(records.filter(date in period_a))
period_b_value = aggregate(records.filter(date in period_b))
change = period_b_value - period_a_value
change_pct = (change / period_a_value) * 100
```

### 7.3 Trend Calculation

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

## 8. Aggregation Patterns

### 8.1 Sum
```
total = records.reduce((sum, record) => sum + record.value, 0)
```
Use for: costs, hours, headcounts, quantities

### 8.2 Count
```
count = records.filter(condition).length
```
Use for: incident counts, inspection counts, item counts

### 8.3 Average
```
average = records.reduce((sum, r) => sum + r.value, 0) / records.length
```
Use for: pass rates, average age, average duration

### 8.4 Min / Max
```
min_value = records.reduce((min, r) => r.value < min ? r.value : min, Infinity)
max_value = records.reduce((max, r) => r.value > max ? r.value : max, -Infinity)
```
Use for: oldest punch item, highest headcount, lowest float

### 8.5 Group By
```
grouped = records.reduce((groups, record) => {
  key = record[group_field]
  groups[key] = groups[key] || []
  groups[key].push(record)
  return groups
}, {})
```
Use for: breakdown by sub, by trade, by location, by division, by inspection type

### 8.6 Distinct
```
unique_values = [...new Set(records.map(r => r[field]))]
```
Use for: list of subs on site, list of active trades, list of impacted locations
