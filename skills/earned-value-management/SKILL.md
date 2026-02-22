---
name: earned-value-management
description: >
  Unified scope-schedule-cost performance measurement using Earned Value Management (EVM) methodology. Calculates SPI, CPI, SV, CV, EAC, ETC, VAC, and TCPI. Generates three-line S-curves (BCWS/BCWP/ACWP), variance analysis, and project forecasting. Extends cost-tracking with schedule integration for complete project health assessment. Triggers: "earned value", "EVM", "S-curve", "SPI", "CPI", "cost performance index", "schedule performance index", "estimate at completion", "EAC", "ETC", "variance analysis", "BCWS", "BCWP", "ACWP", "planned value", "earned value report", "project performance", "cost variance", "schedule variance".
version: 1.0.0
---

# Earned Value Management (EVM)

## Overview

Earned Value Management is the gold standard for integrated project performance measurement, combining scope, schedule, and cost into a unified analytical framework. EVM answers the three critical questions every project manager must ask:

1. **Are we ahead or behind schedule?** (Schedule Performance Index / Schedule Variance)
2. **Are we over or under budget?** (Cost Performance Index / Cost Variance)
3. **What will the project cost at completion?** (Estimate at Completion / Variance at Completion)

Unlike traditional cost-tracking (which shows only spending vs. budget) or schedule-tracking (which shows only timeline progress), EVM integrates both dimensions. It reveals whether cost overruns are due to inefficiency, scope growth, schedule delays, or a combination of factors. The methodology is endorsed by the Project Management Institute (PMI), the Association for the Advancement of Cost Engineering (AACE), and the U.S. Department of Defense as the standard for project performance measurement.

In construction, EVM is particularly valuable because:
- Weather delays and rework can inflate costs while appearing to maintain schedule
- Change orders obscure true project health if not properly integrated
- Retainage and payment schedules create timing mismatches between "earned value" and "actual cost"
- Early trades may bill heavily upfront while late trades carry schedule risk
- The S-curve visualization clearly shows schedule slippage before it becomes critical

Foreman OS EVM skill extends the cost-tracking foundation by adding schedule integration, providing the unified three-dimensional view necessary for proactive project management.

---

## EVM Fundamentals

All EVM analysis rests on four foundational variables, each representing a different perspective on project progress:

### BAC (Budget at Completion)

**Definition**: The total approved project budget at the time of baseline establishment or latest authorized re-baseline.

**Context**:
- Established at project authorization
- Adjusted only through formal change order process (re-baselining decisions)
- Includes all authorized work: direct labor, materials, subcontractors, equipment, overhead allocations
- Excludes contingency in most construction applications (though some organizations include contingency in BAC)

**Example**: A $2,805,000 senior care facility project has BAC = $2,805,000. A $250,000 approved change order re-baselines BAC to $3,055,000.

---

### PV / BCWS (Planned Value / Budgeted Cost of Work Scheduled)

**Definition**: The cumulative budgeted cost of all work that should have been completed by a given reporting date, according to the baseline plan.

**Calculation**: Sum the budget values of all baseline activities scheduled to be complete (or partially complete) by the measurement date.

**Context**:
- Represents "the plan" — what was supposed to happen
- Built from the cost-loaded baseline schedule
- Cumulative and monotonically increasing (never decreases)
- Typically S-shaped for construction projects (slow ramp-up in early phases, rapid middle phases, tail-off at completion)

**Example**:
- Jan baseline: 10% of work scheduled = $280,500 PV
- Feb baseline: 18% of work scheduled = $504,900 PV
- Mar baseline: 28% of work scheduled = $785,400 PV

---

### EV / BCWP (Earned Value / Budgeted Cost of Work Performed)

**Definition**: The cumulative budgeted cost of all work that has actually been completed by a given reporting date.

**Calculation**:
- For each project activity, multiply (Baseline Task Budget) × (Percent Complete)
- Sum all activities' earned values for cumulative EV
- Percent complete assessment uses weighted milestones, units completed, cost ratio, or superintendent estimate

**Context**:
- Represents "what we earned" — actual accomplishment measured against the budget plan
- Cannot exceed PV at any point (unless scope was added and BAC increased)
- Should closely track PV if the project is on schedule
- Separates scheduling accomplishment from spending — a task can be 100% complete but under- or over-budget
- The gap between EV and PV is the Schedule Variance

**Example**:
- Foundation task: Baseline budget $180,000, scheduled to complete Feb, actually 60% complete by Feb 28
- Earned value = $180,000 × 0.60 = $108,000
- If PV for that task was $180,000 but only 60% is done, SV = $108,000 - $180,000 = -$72,000 (behind schedule)

---

### AC / ACWP (Actual Cost / Actual Cost of Work Performed)

**Definition**: The cumulative actual cost incurred for work performed, regardless of when it was budgeted or scheduled.

**Calculation**:
- Sum all actual expenditures: labor costs, material purchases, equipment rentals, subcontractor invoices, consultant fees, overhead charged
- Match to the same work (scope) that generated the EV
- Cumulative from project start through the measurement date

**Context**:
- Represents "what we spent" — hard financial reality
- Must align with the project cost accounting system (GL accounts, cost codes, CSI divisions)
- Includes both internal (W Principles labor) and external (subcontractor, supplier) costs
- In construction, AC reflects invoices received and costs accrued, plus retainage effects if applicable
- The gap between AC and EV is the Cost Variance

**Example**:
- Same foundation task: Actual labor cost $95,000 + actual material cost $28,000 + subcontractor $62,000 = $185,000 AC
- EV for 60% complete task = $108,000
- CV = $108,000 - $185,000 = -$77,000 (over budget on this task)

---

## Core Metrics Table

The following six core metrics and three forecasting metrics are calculated from the four fundamentals above:

### Schedule Performance Metrics

| Metric | Formula | Interpretation | Green / Yellow / Red |
|--------|---------|-----------------|---------------------|
| **Schedule Variance (SV)** | SV = EV - PV | Positive = ahead of schedule; Negative = behind schedule; Dollar amount of schedule variance | SV > 0 / SV near 0 / SV < 0 |
| **Schedule Performance Index (SPI)** | SPI = EV / PV | Ratio of earned to planned. SPI = 1.0 is perfect, >1.0 ahead, <1.0 behind. Interpreted as "earning $X for every $1 of planned work" | 0.95–1.10 / 0.85–0.94 / <0.85 |

#### SV / SPI Examples

| Scenario | PV | EV | SV | SPI | Interpretation |
|----------|-----|-----|-----|------|-----------------|
| On schedule | $100k | $100k | $0 | 1.00 | Earning at planned rate |
| Ahead of schedule | $100k | $110k | +$10k | 1.10 | Earning 10% faster than plan |
| Behind schedule (severe) | $100k | $80k | -$20k | 0.80 | Earning only 80 cents per dollar planned; 20% behind |

**Construction Context**: In weather-heavy projects, SPI <0.90 indicates schedule compression risk. Recovery requires either extended working hours, additional crews, or scope deferral. An SPI of 0.88 at 8% project completion (as in the MOSC example) suggests 10-14 day slip in a 151-day baseline.

---

### Cost Performance Metrics

| Metric | Formula | Interpretation | Green / Yellow / Red |
|--------|---------|-----------------|---------------------|
| **Cost Variance (CV)** | CV = EV - AC | Positive = under budget; Negative = over budget; Dollar amount of cost variance | CV > 0 / CV near 0 / CV < 0 |
| **Cost Performance Index (CPI)** | CPI = EV / AC | Ratio of earned to actual cost. CPI = 1.0 is perfect, >1.0 under budget, <1.0 over budget. Interpreted as "earning $X for every $1 spent" | 0.95–1.10 / 0.85–0.94 / <0.85 |

#### CV / CPI Examples

| Scenario | EV | AC | CV | CPI | Interpretation |
|----------|-----|-----|-----|------|-----------------|
| On budget | $100k | $100k | $0 | 1.00 | Spending at planned rate |
| Under budget | $100k | $95k | +$5k | 1.053 | Earning 5.3% more per dollar spent; efficient |
| Over budget (severe) | $100k | $120k | -$20k | 0.833 | Earning only 83 cents per dollar spent; 20% overrun |

**Construction Context**: CPI <0.95 in early foundation phase often indicates:
- Rework due to geotechnical surprises or inspection failures
- Labor inefficiency due to weather, crew learning curve, or site congestion
- Material waste or premium purchasing
- Subcontractor delays requiring extended general condition costs

---

### Forecasting Metrics

| Metric | Formula | Interpretation | Notes |
|--------|---------|-----------------|-------|
| **Estimate at Completion (EAC)** | See three methods below | Project cost at completion based on current trends and assumptions | Primary decision metric |
| **Estimate to Complete (ETC)** | ETC = EAC - AC | Remaining budget needed to finish the project | ETC = BAC only if on budget |
| **Variance at Completion (VAC)** | VAC = BAC - EAC | Final budget variance (positive = under budget) | Used to flag if project will overrun |
| **To-Complete Performance Index (TCPI)** | TCPI = (BAC - EV) / (BAC - AC) | Required cost performance for remaining work to stay within BAC | If TCPI > 1.15, recovery is difficult |

---

## Three Methods for EAC (Estimate at Completion)

### Method 1: CPI-Based (Current Trend Continues)

**Formula**: EAC = BAC / CPI

**Logic**: If current cost efficiency continues unchanged for all remaining work, multiply the remaining budget by the inverse of CPI.

**When to use**:
- Early project phases when future conditions are uncertain
- When cost drivers are systemic (labor productivity, subcontractor pricing) and unlikely to change
- For quick/conservative forecasts

**Example**:
- BAC = $2,805,000
- EV = $198,000 (7.1% complete)
- AC = $210,000
- CPI = 198,000 / 210,000 = 0.943
- EAC = 2,805,000 / 0.943 = $2,975,716
- Project overrun forecast: $170,716

**Weakness**: Ignores schedule performance and assumes cost inefficiency persists.

---

### Method 2: Remaining Work at Original Rate

**Formula**: EAC = AC + (BAC - EV)

**Logic**: Assume remaining work will be completed at the original budgeted rate (CPI = 1.0).

**When to use**:
- When cost overruns are temporary or one-time (e.g., unexpected soil condition now remediated)
- When corrective actions have been implemented and expect to restore cost efficiency
- Conservative forecast assuming management correction

**Example**:
- BAC = $2,805,000
- EV = $198,000
- AC = $210,000
- EAC = 210,000 + (2,805,000 - 198,000) = 210,000 + 2,607,000 = $2,817,000
- Project overrun forecast: $12,000 (minor)

**Weakness**: Unrealistic if cost overrun root causes are not addressed (e.g., persistent labor inefficiency).

---

### Method 3: Composite (CPI × SPI) — Both Schedule and Cost

**Formula**: EAC = AC + [(BAC - EV) / (CPI × SPI)]

**Logic**: Remaining work will be completed at a rate influenced by both cost and schedule performance.

**When to use**:
- Most realistic for construction projects where schedule affects cost
- When schedule delays (SPI < 1.0) are extending general conditions, overhead, and crew inefficiency
- For mid-to-late project phases with established trends

**Example**:
- BAC = $2,805,000
- EV = $198,000
- AC = $210,000
- CPI = 0.943, SPI = 0.88
- Combined efficiency = CPI × SPI = 0.943 × 0.88 = 0.830
- EAC = 210,000 + [(2,805,000 - 198,000) / 0.830] = 210,000 + 3,148,193 = $3,358,193
- Project overrun forecast: $553,193 (severe)

**Interpretation**: The composite method reveals that if both cost overruns and schedule delays persist, the project completion cost will be nearly $3.36M — a $553k overrun. This scenario typically triggers:
1. Value engineering review of remaining work
2. Schedule acceleration analysis (crash costs vs. delay costs)
3. Scope deferral decision
4. Change order tracking and delay claims management

---

## Three-Line S-Curve

The S-curve is the signature EVM visualization. It plots three cumulative cost curves over the project timeline, revealing performance at a glance:

### Curve 1: Planned Value (PV / BCWS)

- **Color**: Blue (or green)
- **Definition**: Cumulative budgeted cost of work scheduled
- **Shape**: Typically S-shaped for construction
  - Shallow start (mobilization, permits, early long-lead items)
  - Steep middle (main construction, PEMB erection, rough-in)
  - Tail-off (finishes, punch list, closeout)
- **Interpretation**: The "plan." If the project is on schedule, EV should track closely to PV.
- **Example trajectory** (MOSC 151-day project):
  - Month 1 (Jan): 5% PV = $140,250
  - Month 2 (Feb): 12% PV = $336,600
  - Month 3 (Mar): 28% PV = $785,400 (PEMB erection drives spike)
  - Month 4 (Apr): 55% PV = $1,542,750
  - Month 5 (May): 82% PV = $2,296,100
  - Month 6 (Jun): 95% PV = $2,664,750
  - Month 7 (Jul): 100% PV = $2,805,000

### Curve 2: Earned Value (EV / BCWP)

- **Color**: Orange (or yellow)
- **Definition**: Cumulative budgeted cost of work actually performed
- **Expected behavior**: Closely tracks PV if project is on schedule
- **Gap interpretation**:
  - If EV < PV (orange below blue): Schedule is behind baseline — gap widens as delays accumulate
  - If EV > PV (orange above blue): Project is ahead of schedule (rare in construction until closeout)
  - If EV = PV: Project is on schedule
- **Example with 2-week delay entering Month 3**:
  - Month 1: $140,250 EV (on schedule)
  - Month 2: $320,000 EV (slightly behind plan, -$16,600 SV)
  - Month 3: $640,000 EV (significant slip, -$145,400 SV)
  - Month 4 and beyond: Gap narrows if recovery crew added, widens if no recovery

### Curve 3: Actual Cost (AC / ACWP)

- **Color**: Red (or black)
- **Definition**: Cumulative actual cost incurred
- **Expected behavior**: Should track EV if project is on budget
- **Gap interpretation**:
  - If AC > EV (red above orange): Project is over budget — cost inefficiency
  - If AC < EV (red below orange): Project is under budget — cost efficiency (rare unless scope reduced)
  - If AC = EV: Project is on budget
- **Construction context**: AC often spikes when major invoices arrive (PEMB delivery, payroll, subcontractor lump-sum payments)
- **Example with 5% cost overrun**:
  - Month 1: $147,500 AC (slightly over PV and EV)
  - Month 2: $345,000 AC (over budget)
  - Month 3: $680,000 AC (slight overrun)
  - Cumulative AC exceeds cumulative EV throughout, indicating project is inefficient

### Visual Interpretation

A healthy S-curve has:
1. PV curve follows the baseline plan (usually S-shape)
2. EV curve closely tracks PV (within 3-5% variance acceptable for construction)
3. AC curve closely tracks EV (within 2-3% variance)
4. All three curves reach BAC by project completion

Warning signs:
- **EV falls below PV**: Schedule variance growing — delays accumulating
- **AC significantly above EV**: Cost variance growing — spending exceeds earned value
- **All three curves diverge widely**: Project health is poor; escalation needed
- **Early spike in AC without corresponding EV**: Possible front-loading, change order backlog, or misalignment

---

## EVM Data Model (JSON)

The following JSON structure captures all monthly EVM data needed for reporting, forecasting, and dashboarding:

```json
{
  "evm_data": {
    "project_id": "825021",
    "project_name": "Morehead One Senior Care",
    "bac": 2805000,
    "currency": "USD",
    "baseline_start_date": "2026-01-21",
    "baseline_end_date": "2026-07-29",
    "baseline_duration_days": 151,
    "reporting_periods": [
      {
        "period": "2026-01",
        "period_end_date": "2026-01-31",
        "pv_cumulative": 140250,
        "ev_cumulative": 140250,
        "ac_cumulative": 142000,
        "sv": 0,
        "cv": -1750,
        "spi": 1.00,
        "cpi": 0.988,
        "eac_cpi": 2838675,
        "eac_remaining": 2808000,
        "eac_composite": 2823456,
        "etc": 2681000,
        "vac": -33675,
        "tcpi": 1.003,
        "percent_complete_planned": 5.0,
        "percent_complete_earned": 5.0,
        "percent_complete_actual_cost": 5.1,
        "notes": "Mobilization on schedule. Minor material procurement delays."
      },
      {
        "period": "2026-02",
        "period_end_date": "2026-02-28",
        "pv_cumulative": 336600,
        "ev_cumulative": 320000,
        "ac_cumulative": 345000,
        "sv": -16600,
        "cv": -25000,
        "spi": 0.951,
        "cpi": 0.928,
        "eac_cpi": 3021258,
        "eac_remaining": 2808000,
        "eac_composite": 3145623,
        "etc": 2800258,
        "vac": -216258,
        "tcpi": 1.021,
        "percent_complete_planned": 12.0,
        "percent_complete_earned": 11.4,
        "percent_complete_actual_cost": 12.3,
        "notes": "Foundation delayed 3 days due to weather/ground conditions. Concrete costs escalated 2.5% due to admixture changes."
      },
      {
        "period": "2026-03",
        "period_end_date": "2026-03-31",
        "pv_cumulative": 785400,
        "ev_cumulative": 710000,
        "ac_cumulative": 768000,
        "sv": -75400,
        "cv": -58000,
        "spi": 0.904,
        "cpi": 0.925,
        "eac_cpi": 3034054,
        "eac_remaining": 2808000,
        "eac_composite": 3289456,
        "etc": 2521054,
        "vac": -229054,
        "tcpi": 1.041,
        "percent_complete_planned": 28.0,
        "percent_complete_earned": 25.3,
        "percent_complete_actual_cost": 27.4,
        "notes": "PEMB delayed to 3/8 due to foundation schedule slip. Excavation overrun 8%. Alexander Construction (PEMB) crew added on 3/15 to compress erection schedule."
      },
      {
        "period": "2026-04",
        "period_end_date": "2026-04-30",
        "pv_cumulative": 1542750,
        "ev_cumulative": 1485000,
        "ac_cumulative": 1603000,
        "sv": -57750,
        "cv": -118000,
        "spi": 0.963,
        "cpi": 0.926,
        "eac_cpi": 3032326,
        "eac_remaining": 2808000,
        "eac_composite": 3156234,
        "etc": 1429326,
        "vac": -227326,
        "tcpi": 1.031,
        "percent_complete_planned": 55.0,
        "percent_complete_earned": 52.9,
        "percent_complete_actual_cost": 57.1,
        "notes": "PEMB erection 95% complete. CFS framing and MEP rough-in commenced. Labor productivity improving; SPI trending toward 0.97. CPI stable at 0.925–0.928 (cost overrun root causes: rework 2%, inflation 1%, front-loaded long-lead delivery 1%)."
      }
    ]
  }
}
```

### Data Source Mapping

Each EVM data point is pulled from source systems:

- **BAC**: From budget establishment and change-order tracker (incremented only on approved COs)
- **PV (BCWS)**: From cost-loaded baseline schedule; recalculated monthly based on work scheduled per baseline
- **EV (BCWP)**: From pay-applications (billed % complete × task budget) or weekly timecards + material requisitions
- **AC (ACWP)**: From cost-accounting system (GL accounts mapped to project cost codes/CSI divisions)
- **Percent complete**: From superintendent field reports, milestone achievement, or formula-based (cost ratio, units completed)
- **SPI, CPI, etc.**: Calculated from PV, EV, AC formulas

---


## Project Intelligence Integration

When project intelligence is loaded, auto-populate EVM baseline data, actual costs, and earned value from project data files instead of requiring manual entry for every reporting period.

### Budget Baseline (BAC)
Pull baseline budget from cost tracking data:
- Read `cost-data.json` → `budget_by_division[]` → sum all division budgets for BAC
- Read `change-order-log.json` → filter by `status` = "approved" → sum `cost_approved` amounts → add to original BAC for re-baselined BAC
- Example: Original BAC $2,805,000 + approved CO-005 $17,800 = re-baselined BAC $2,822,800

### Planned Value (BCWS) / Schedule Baseline
Build the planned value curve from schedule data:
- Read `schedule.json` → `milestones[]` + `critical_path[]` → map planned work percentage over time
- Cross-reference `cost-data.json` → `budget_by_division[]` → distribute budget across scheduled activities for cost-loaded baseline
- Use `schedule.json` → `percent_complete` (baseline) → calculate cumulative PV at each reporting period

### Actual Cost (ACWP)
Aggregate actual expenditures from multiple sources:
- Read `labor-tracking.json` → `crew_summaries[]` → sum labor costs per reporting period
- Read `procurement-log.json` → `total_cost` for delivered items → sum material costs per period
- Read `cost-data.json` → actual costs by division → validate against labor + material totals
- Example: Feb labor $95,000 + materials $28,000 + sub invoices $62,000 = $185,000 AC

### Earned Value (BCWP)
Calculate earned value from progress and baseline:
- Read `cost-data.json` → `percent_complete_by_division[]` → multiply each division's budget × percent complete
- Read `schedule.json` → `percent_complete` → validate overall earned value aligns with schedule progress
- Cross-reference `daily-report-data.json` → work completed entries → ground-truth percent complete against field observations

### Change Order Adjustments
Adjust baseline for approved scope changes:
- Read `change-order-log.json` → filter `status` = "approved" → for each approved CO, add `cost_approved` to BAC
- Read `change-order-log.json` → `schedule_impact_days` → adjust planned value curve for approved time extensions
- Flag unapproved COs with `cost_estimate` > $10,000 as potential BAC adjustment risks

### Forecast Validation
Cross-check EAC forecasts against bottom-up estimates:
- Read `cost-data.json` → `forecast_to_complete[]` → compare bottom-up ETC against CPI-based ETC
- If bottom-up ETC diverges from CPI-based ETC by >10%, flag for superintendent review
- Read `delay-log.json` → active delays → factor delay cost impact into composite EAC (Method 3: CPI x SPI)

---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
