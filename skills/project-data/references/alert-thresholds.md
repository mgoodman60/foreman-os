---
name: alert-thresholds
description: KPI thresholds, anomaly detection rules, and severity scoring for the project-health-monitor and dashboard-intelligence-analyst agents. Defines per-metric tiered alerts, trend calculation methodology, and narrative templates for automated project health reporting.
version: 1.0.0
---

# Alert Thresholds and Anomaly Detection Reference

This document defines the complete threshold framework for automated project health monitoring. All thresholds, anomaly rules, and severity scores are consumed by the **project-health-monitor** and **dashboard-intelligence-analyst** agents to generate alerts, dashboards, and narrative summaries.

---

## 1. Per-KPI Threshold Definitions

Each KPI uses a tiered alert system with four levels: **info**, **warning**, **critical**, and a target/healthy range. Agents must evaluate each KPI against these tiers every reporting cycle.

### 1.1 SPI (Schedule Performance Index)

| Tier | Range | Label | Action |
|------|-------|-------|--------|
| Info (Ahead) | SPI > 1.05 | Ahead of schedule | Log positive trend; verify not due to data lag |
| Healthy | 0.95 <= SPI <= 1.05 | On track | No action required |
| Warning | 0.90 <= SPI < 0.95 | Behind schedule | Flag for PM review; check critical path float |
| Critical | SPI < 0.90 | Significantly behind | Escalate to PM and owner; recovery plan required |

**Data source**: `schedule.json` fields `earned_value.bcwp`, `earned_value.bcws`
**Calculation**: SPI = BCWP / BCWS
**Update frequency**: Weekly (aligned with schedule update cycle)

### 1.2 CPI (Cost Performance Index)

| Tier | Range | Label | Action |
|------|-------|-------|--------|
| Info (Under budget) | CPI > 1.05 | Under budget | Log positive trend; verify coding accuracy |
| Healthy | 0.95 <= CPI <= 1.05 | On budget | No action required |
| Warning | 0.90 <= CPI < 0.95 | Over budget | Flag for cost review; check division-level variances |
| Critical | CPI < 0.90 | Significantly over budget | Escalate to PM; contingency draw assessment required |

**Data source**: `cost-data.json` fields `earned_value.bcwp`, `earned_value.acwp`
**Calculation**: CPI = BCWP / ACWP
**Update frequency**: Weekly or upon cost posting

### 1.3 FPIR (First-Pass Inspection Rejection Rate)

| Tier | Range | Label | Action |
|------|-------|-------|--------|
| Healthy | FPIR < 10% | Good quality performance | No action required |
| Info | 10% <= FPIR < 20% | Monitor quality | Track by sub and trade; look for clustering |
| Warning | 20% <= FPIR < 30% | Investigate quality issues | Root cause analysis; sub performance review |
| Critical | FPIR >= 30% | Quality failure pattern | Stop-work evaluation; corrective action plan required |

**Data source**: `quality-data.json` field `first_pass_inspection_results[]`, `inspection-log.json`
**Calculation**: FPIR = (inspections_failed_first_pass / total_inspections) * 100
**Update frequency**: Rolling 30-day window, recalculated daily
**Breakdown dimensions**: By sub, by trade, by location, by inspection type

### 1.4 TRIR (Total Recordable Incident Rate)

| Tier | Range | Label | Action |
|------|-------|-------|--------|
| Target | TRIR = 0 | Zero incidents | Maintain safety program |
| Info | TRIR > 0 (non-recordable near-misses only) | Near-miss activity | Review near-miss reports; reinforce toolbox talks |
| Warning | TRIR > 2.0 | Above industry average | Safety stand-down consideration; program review |
| Critical | Any recordable incident | Recordable event | Immediate incident investigation; OSHA reporting review |

**Data source**: `safety-log.json` fields `incidents[]`, `hours_worked`
**Calculation**: TRIR = (recordable_incidents * 200,000) / total_hours_worked
**Update frequency**: Real-time on incident entry; rolling 12-month for rate
**Special rule**: Any single recordable incident triggers critical regardless of rate

### 1.5 PPC (Percent Plan Complete)

| Tier | Range | Label | Action |
|------|-------|-------|--------|
| Healthy | PPC > 85% | Strong plan reliability | Acknowledge team performance |
| Info | 70% < PPC <= 85% | Acceptable plan reliability | Identify variance reasons; no escalation |
| Warning | 60% < PPC <= 70% | Improvement needed | Root cause analysis of misses; constraint review |
| Critical | PPC <= 60% | Plan reliability failure | Replanning session required; constraint log review |

**Data source**: `schedule.json` field `lookahead_history[]` (planned vs completed)
**Calculation**: PPC = (activities_completed / activities_planned) * 100 for the period
**Update frequency**: Weekly (end of each lookahead period)

### 1.6 Contingency Remaining

| Tier | Range | Label | Action |
|------|-------|-------|--------|
| Healthy | > 50% remaining | Adequate reserves | No action required |
| Info | 30% < remaining <= 50% | Monitor reserves | Track burn rate; review pending COs |
| Warning | 15% < remaining <= 30% | Low reserves | Restrict discretionary spending; escalate to owner |
| Critical | remaining <= 15% | Reserves depleted | Freeze non-critical COs; owner notification required |

**Data source**: `cost-data.json` fields `contingency.original_amount`, `contingency.committed`, `contingency.spent`
**Calculation**: remaining_pct = ((original - committed - spent) / original) * 100
**Update frequency**: Upon any change order approval or cost posting
**Secondary metric**: Burn rate = contingency_used / months_elapsed vs contingency_total / total_months

### 1.7 Sub No-Show Rate

| Tier | Range | Label | Action |
|------|-------|-------|--------|
| Healthy | < 5% | Normal absenteeism | No action required |
| Info | 5% <= rate < 10% | Elevated absenteeism | Monitor by sub; check weather/holiday factors |
| Warning | 10% <= rate < 20% | Investigate attendance | Contact sub PM; document pattern |
| Critical | rate >= 20% | Attendance failure | Back-charge evaluation; replacement sub consideration |

**Data source**: `labor-tracking.json` fields `daily_entries[].workers_expected`, `daily_entries[].workers_present`; cross-ref `directory.json` for sub details
**Calculation**: no_show_rate = ((expected - present) / expected) * 100, aggregated by sub over rolling 2-week window
**Update frequency**: Daily
**Exclusions**: Weather days, holidays, owner-directed standdowns

### 1.8 Punch List Aging

| Tier | Range | Label | Action |
|------|-------|-------|--------|
| Healthy | < 14 days average age | Normal resolution pace | No action required |
| Info | 14 <= age < 30 days | Monitor aging items | Identify items approaching 30-day mark |
| Warning | 30 <= age < 60 days | Items aging | Escalate to responsible subs; track by trade |
| Critical | age >= 60 days | Stale punch items | Back-charge consideration; closeout risk flag |

**Data source**: `punch-list.json` fields `items[].date_identified`, `items[].date_resolved`, `items[].status`
**Calculation**: age = today - date_identified for items where status != "resolved"
**Update frequency**: Daily
**Aggregation**: Report both average age and count per tier

---

## 2. Anomaly Detection Rules

Anomalies are deviations from established patterns that may not trigger KPI thresholds but indicate emerging problems. Each rule defines a detection condition, lookback period, and response.

### 2.1 Headcount Swing

**Condition**: Day-over-day total site headcount change exceeds 25%
**Lookback**: Compare today's headcount to previous workday
**Calculation**: abs(today_count - yesterday_count) / yesterday_count > 0.25
**Data source**: `labor-tracking.json` field `daily_entries[].total_workers`
**Exclusions**: First day after weekend/holiday (compare to last workday instead); mobilization/demobilization events logged in `schedule.json`
**Severity**: Warning if unexpected; Info if aligned with schedule mobilization
**Response**: Verify against schedule; check if sub mobilization/demob was planned

### 2.2 Delivery Slippage

**Condition**: 3 or more procurement items past their expected delivery date within a rolling 7-day window
**Lookback**: Rolling 7 calendar days
**Calculation**: Count items where `expected_delivery < today` AND `delivery_status != "delivered"` AND `expected_delivery >= (today - 7)`
**Data source**: `procurement-log.json` fields `items[].expected_delivery`, `items[].delivery_status`
**Severity**: Warning at 3 items; Critical at 5+ items or if any item is on critical path
**Response**: Cross-reference with `schedule.json` for activity impact; notify procurement manager

### 2.3 Delay Acceleration

**Condition**: Cumulative delay days increasing at more than 2x the project average rate
**Lookback**: Compare last 2-week period to project-to-date average
**Calculation**:
  - `avg_delay_rate` = total_delay_days / project_weeks_elapsed
  - `recent_rate` = delay_days_last_2_weeks / 2
  - Trigger if `recent_rate > 2 * avg_delay_rate`
**Data source**: `delay-log.json` fields `delays[].delay_days`, `delays[].date_identified`
**Severity**: Warning if recent_rate between 2x and 3x average; Critical if > 3x
**Response**: Identify contributing delays; check for common root cause

### 2.4 Inspection Failure Clustering

**Condition**: 3 or more inspection failures in the same location OR same sub within a rolling 7-day window
**Lookback**: Rolling 7 calendar days
**Calculation**: Group `inspection-log.json` failures by `location` and by `sub_name`; trigger if any group count >= 3
**Data source**: `inspection-log.json` fields `inspections[].result`, `inspections[].location`, `inspections[].sub_name`, `inspections[].date`
**Severity**: Warning at 3 clustered failures; Critical at 5+ or if failures involve life-safety inspections
**Response**: Root cause analysis; sub quality meeting; potential stop-work for affected area

### 2.5 Cost Variance Spike

**Condition**: Any single cost division showing variance exceeding 15% of its period budget in a single reporting period
**Lookback**: Current reporting period (typically monthly)
**Calculation**: For each division: `period_variance_pct = abs(actual_cost - budgeted_cost) / budgeted_cost * 100`; trigger if > 15%
**Data source**: `cost-data.json` fields `divisions[].actual_cost`, `divisions[].budgeted_cost`, period-filtered
**Severity**: Warning at 15% variance; Critical at 25%+ variance
**Response**: Verify cost coding; check for misallocated charges; review change order impacts

---

## 3. Severity Scoring Rubric

All alerts are assigned a severity score from 1 to 5 based on the following criteria. The score drives notification routing and dashboard prioritization.

| Score | Label | Criteria | Notification |
|-------|-------|----------|--------------|
| 1 | Informational | Positive trend or minor deviation within healthy range; no action needed | Dashboard only; included in weekly summary |
| 2 | Advisory | Metric approaching threshold boundary; early warning indicator | Dashboard highlight; included in daily summary |
| 3 | Warning | Metric has crossed into warning tier; requires attention within 48 hours | Dashboard alert; PM notification; included in daily report |
| 4 | Elevated | Multiple warning-tier metrics in same domain; or single metric approaching critical | Dashboard priority alert; PM + superintendent notification; action item created |
| 5 | Critical | Metric in critical tier; safety incident; or cascading failures across domains | Dashboard top-of-page alert; immediate notification to PM, superintendent, and owner; recovery plan trigger |

### Compound Severity Rules

When multiple KPIs are in warning or critical simultaneously, apply the following escalation:
- 2+ KPIs at warning level in the same domain (e.g., cost) → escalate to severity 4
- 3+ KPIs at warning level across different domains → escalate to severity 4
- Any KPI at critical + any other KPI at warning → escalate to severity 5
- Safety critical (TRIR recordable) always remains severity 5 regardless of other metrics

---

## 4. Trend Calculation Methodology

### 4.1 Rolling Period Comparison

All trend indicators use a **3-period rolling comparison** where the period length matches the KPI update frequency:
- Weekly KPIs (SPI, CPI, PPC): Compare current week to prior 2 weeks
- Daily KPIs (headcount, no-show rate, punch list aging): Compare current day to prior 2 workdays
- Monthly KPIs (TRIR, cost variance): Compare current month to prior 2 months

### 4.2 Direction Indicators

| Indicator | Symbol | Condition |
|-----------|--------|-----------|
| Improving | UP | Current period value is better than both prior periods |
| Stable | FLAT | Current period value is within +/- 5% of the 3-period average |
| Declining | DOWN | Current period value is worse than both prior periods |
| Volatile | MIXED | Current period value alternates better/worse across the 3 periods |

"Better" and "worse" are defined per KPI:
- SPI, CPI, PPC, Contingency remaining: Higher is better
- FPIR, TRIR, No-show rate, Punch list aging: Lower is better

### 4.3 Trend Weighting

When generating composite health scores, apply recency weighting:
- Current period: weight 0.50
- Prior period: weight 0.30
- Two periods ago: weight 0.20

---

## 5. Narrative Templates

Agents use these templates to generate human-readable alert descriptions. Placeholders are enclosed in `{curly_braces}`.

### 5.1 KPI Threshold Alerts

**SPI Warning**:
> Schedule Performance Index has declined to {spi_value} ({trend_direction} trend over {period_count} periods). The project is approximately {days_behind} days behind the baseline schedule. Critical path float has reduced to {float_days} days. Key impacted activities: {activity_list}.

**SPI Critical**:
> CRITICAL: SPI has fallen to {spi_value}, indicating the project is earning only {earned_pct}% of planned value. At the current rate, the projected completion date is {projected_completion}, which is {slip_days} days beyond the contractual date of {contract_completion}. Immediate recovery planning is required. Primary delay drivers: {delay_drivers}.

**CPI Warning**:
> Cost Performance Index is at {cpi_value} ({trend_direction}). The project is spending ${overspend_amount} more than earned to date. Top cost variance divisions: {division_list}. Estimate at completion (EAC) is ${eac_amount} vs budget of ${budget_amount}.

**CPI Critical**:
> CRITICAL: CPI has dropped to {cpi_value}. At the current burn rate, the project will exceed budget by ${overrun_amount} ({overrun_pct}%). Contingency remaining is {contingency_pct}%. Immediate cost review required. Largest variances: {variance_details}.

**FPIR Warning**:
> First-Pass Inspection Rejection Rate has risen to {fpir_value}% ({trend_direction}). In the past {lookback_period}, {fail_count} of {total_count} inspections failed on first attempt. Top failing subs: {sub_list}. Top failing inspection types: {type_list}.

**FPIR Critical**:
> CRITICAL: FPIR has reached {fpir_value}%. Quality performance is significantly below acceptable levels. Concentrated failures in: {location_list}. Affected subs: {sub_list}. Corrective action plans are required before work continues in affected areas.

**TRIR Alert**:
> Safety Alert: A {incident_type} incident was recorded on {incident_date} at {location}. Current TRIR is {trir_value}. {worker_trade} worker {injury_description}. Investigation status: {investigation_status}. Days since last recordable prior to this: {days_since_last}.

**PPC Warning**:
> Percent Plan Complete for the {period_name} lookahead was {ppc_value}%. Of {planned_count} planned activities, {completed_count} were completed. Top reasons for misses: {reason_list}. Subs with lowest plan reliability: {sub_list}.

**PPC Critical**:
> CRITICAL: PPC has fallen to {ppc_value}% for the {period_name} period. Plan reliability is failing. {miss_count} activities were not completed as planned. Constraint analysis shows: {constraint_summary}. A replanning session is recommended.

**Contingency Warning**:
> Contingency reserves have been drawn down to {contingency_pct}% ({remaining_amount} of {original_amount}). Current burn rate: ${burn_rate}/month. At this rate, reserves will be exhausted by {exhaustion_date}. Pending change orders that may draw contingency: {pending_co_list}.

**Contingency Critical**:
> CRITICAL: Contingency reserves are at {contingency_pct}%. Only ${remaining_amount} remains against pending claims of ${pending_claims}. Spending controls must be implemented immediately. Owner notification is required per contract Section {contract_section}.

### 5.2 Anomaly Alerts

**Headcount Swing**:
> Site headcount changed by {swing_pct}% ({direction}) from {yesterday_count} to {today_count} workers. {sub_detail}. This {was_expected} based on the current schedule. {schedule_context}.

**Delivery Slippage**:
> {slipped_count} procurement items have slipped past their expected delivery dates in the last 7 days: {item_list}. {critical_path_impact}. Longest overdue: {item_name} by {days_overdue} days.

**Delay Acceleration**:
> Delay accumulation has accelerated to {recent_rate} days/week vs project average of {avg_rate} days/week ({multiplier}x acceleration). Recent delays: {delay_list}. Primary causes: {cause_summary}.

**Inspection Failure Clustering**:
> Inspection failure cluster detected: {fail_count} failures in {cluster_dimension} "{cluster_value}" over the past 7 days. Failed inspections: {inspection_list}. Pattern suggests: {pattern_analysis}.

**Cost Variance Spike**:
> Cost variance spike in Division {division_number} ({division_name}): {variance_pct}% variance this period (${actual} actual vs ${budgeted} budgeted). Contributing factors: {factor_list}.

---

## 6. Data Source Reference

Each KPI and anomaly rule reads from specific JSON files. This table provides a complete mapping for agent configuration.

| KPI / Rule | Primary File | Fields | Secondary File | Fields |
|------------|-------------|--------|----------------|--------|
| SPI | schedule.json | earned_value.bcwp, earned_value.bcws | cost-data.json | earned_value (cross-validation) |
| CPI | cost-data.json | earned_value.bcwp, earned_value.acwp | schedule.json | earned_value (cross-validation) |
| FPIR | quality-data.json | first_pass_inspection_results[] | inspection-log.json | inspections[].result, .sub_name, .location |
| TRIR | safety-log.json | incidents[], hours_worked | labor-tracking.json | daily_entries[].total_workers (hours calc) |
| PPC | schedule.json | lookahead_history[].planned, .completed | — | — |
| Contingency | cost-data.json | contingency.original_amount, .committed, .spent | change-order-log.json | change_orders[].status, .amount |
| Sub no-show | labor-tracking.json | daily_entries[].workers_expected, .workers_present | directory.json | subs[].name, .trade |
| Punch list aging | punch-list.json | items[].date_identified, .date_resolved, .status | directory.json | subs[].name (responsible sub) |
| Headcount swing | labor-tracking.json | daily_entries[].total_workers, .date | schedule.json | activities[].mobilization (expected changes) |
| Delivery slippage | procurement-log.json | items[].expected_delivery, .delivery_status | schedule.json | activities[].material_dependencies |
| Delay acceleration | delay-log.json | delays[].delay_days, .date_identified, .cause | schedule.json | critical_path (impact assessment) |
| Inspection clustering | inspection-log.json | inspections[].result, .location, .sub_name, .date | quality-data.json | first_pass_inspection_results[] |
| Cost variance spike | cost-data.json | divisions[].actual_cost, .budgeted_cost | change-order-log.json | change_orders[].division, .amount |
