---
name: cost-tracking
description: >
  Comprehensive project cost management including budget vs actual tracking, cost forecasting, variance analysis, invoice reconciliation, change order cost impact, cash flow projections, and cost reporting. Integrates with pay-app, change-order, procurement, and schedule systems. Triggers: "cost tracking", "cost report", "budget vs actual", "cost forecast", "cost variance", "invoice reconciliation", "cash flow", "budget status", "cost performance", "cost summary", "EAC", "burn rate", "cost overrun".
version: 1.0.0
---

# Cost Tracking Skill

## Overview

The **cost-tracking** skill provides comprehensive cost management for construction projects. It enables superintendents and project managers to track actual costs against budget, forecast final costs, identify cost variances, reconcile invoices against commitments, manage change order costs, and project cash flow. The skill integrates seamlessly with pay applications, change orders, procurement logs, and schedules to maintain real-time project financial health.

## Cost Tracking Philosophy

Project cost management operates on three core pillars:

1. **Budget Establishment** — Original contract value + approved change orders = current contract value
2. **Cost Accumulation** — Track committed costs, invoiced costs, and paid costs against each budget line
3. **Performance Analysis** — Compare spending to schedule progress to identify cost/schedule misalignment

The cost-tracking skill manages all three pillars with early warning alerts when spending deviates from plan.

## Budget Structure (CSI Division Organization)

Budgets are organized by **CSI Division** to align with project specifications and standard construction cost accounting:

```json
{
  "budget": {
    "original_contract_value": 2770000,
    "approved_cos_amount": 35000,
    "current_contract_value": 2805000,
    "budget_by_division": [
      {
        "division_number": "01",
        "division_title": "General Requirements",
        "description": "Site mobilization, project management, temporary facilities",
        "original_amount": 145000,
        "applied_cos": [
          { "co_id": "CO-001", "amount": 5000 },
          { "co_id": "CO-003", "amount": -2000 }
        ],
        "current_amount": 148000,
        "committed_costs": 65000,
        "invoiced_costs": 45000,
        "paid_costs": 40500,
        "forecast_to_complete": 85000,
        "total_forecast": 130500,
        "notes": ""
      },
      {
        "division_number": "02",
        "division_title": "Existing Conditions",
        "description": "Demolition and site preparation",
        "original_amount": 85000,
        "applied_cos": [],
        "current_amount": 85000,
        "committed_costs": 78500,
        "invoiced_costs": 65000,
        "paid_costs": 58500,
        "forecast_to_complete": 12000,
        "total_forecast": 77000,
        "notes": ""
      }
    ]
  }
}
```

### Budget Line Item Fields

| Field | Description | Example |
|-------|-------------|---------|
| **division_number** | CSI division code (01–33) | "03" (Concrete) |
| **division_title** | CSI division name | "Cast-in-Place Concrete" |
| **description** | Detailed scope summary | "Foundations, slabs, ramps" |
| **original_amount** | Contract baseline for this division | $185,000 |
| **applied_cos** | Array of approved COs affecting this division | [{"co_id":"CO-001","amount":5000}] |
| **current_amount** | Original + applied COs = current budget | $190,000 |
| **committed_costs** | PO amounts, sub contracts, approved purchase orders | $130,000 |
| **invoiced_costs** | Amounts invoiced by subs/suppliers (not yet paid) | $85,000 |
| **paid_costs** | Cumulative paid amounts | $80,000 |
| **forecast_to_complete** | Estimated cost to finish remaining work | $110,000 |
| **total_forecast** | Invoiced + forecast to complete | $195,000 |

## Budget Initialization

When the superintendent first sets up cost tracking via `/cost`, initialize `cost-data.json` with:

**Required fields:**
- `original_contract_value` (number) — Total contract amount from the executed contract
- `budget_by_division[]` — Array of CSI division budget line items, each with:
  - `division` (string) — CSI division code (e.g., "03", "04", "05")
  - `description` (string) — Division name (e.g., "Concrete", "Masonry", "Metals")
  - `original_amount` (number) — Original budget for this division
  - `current_amount` (number) — Current budget (original + approved COs)
  - `committed_costs` (number) — Subcontract + PO amounts
  - `applied_cos[]` (array) — Change orders applied to this division, each referencing `change-order-log.json` entries
- `contingency` (object):
  - `original_amount` (number) — Starting contingency
  - `current_amount` (number) — Remaining after draws
  - `draws[]` (array) — Each draw with date, amount, description, CO reference
- `allowances[]` (array) — Contract allowances with original vs. spent tracking

**Schedule of Values (SOV) linkage:**
- Each division line item links to `pay-app-log.json` SOV line items via `sov_line_number`
- Percent complete per line feeds earned value calculations in `earned-value-management`
- SOV structure: `sov_line_number`, `description`, `scheduled_value`, `work_completed_previous`, `work_completed_this_period`, `materials_presently_stored`, `total_completed_and_stored`, `percent_complete`, `balance_to_finish`, `retainage`

---

## Cost Performance Index (CPI) Calculation

The **Cost Performance Index** measures how efficiently the project is spending money:

```
CPI = Earned Value / Actual Costs

Where:
  Earned Value = Current budget × % complete
  Actual Costs = Invoiced + paid costs to date
```

**Interpretation:**
- CPI = 1.0: Spending perfectly on schedule
- CPI > 1.0: Under budget (spending less than earned)
- CPI < 1.0: Over budget (spending more than earned)

**Example:**
- Current Budget: $2,805,000
- Project % Complete: 12%
- Earned Value: $2,805,000 × 0.12 = $336,600
- Actual Costs: $320,000 (invoiced)
- CPI = $336,600 / $320,000 = 1.05 (5% under budget)

## Cost Forecasting Methods

### Method 1: Estimate at Completion (EAC) — CPI-Based

Uses current cost performance to project final cost:

```
EAC = Actual Costs + (Remaining Work / CPI)

Or equivalently:
EAC = Budget / CPI
```

**Example:**
- Current Budget: $2,805,000
- CPI: 1.05 (spending efficiently)
- EAC = $2,805,000 / 1.05 = $2,671,429
- Projected Savings: $133,571

### Method 2: EAC — Revised Estimate

Uses fresh estimate of remaining work (accounting for known scope changes):

```
EAC = Actual Costs + Revised Estimate to Complete

Where:
  Revised Estimate = Original estimate − (% complete work)
```

**Example:**
- Actual Costs: $320,000
- Original remaining estimate: $2,485,000
- % Complete: 12%
- Revised remaining = $2,485,000 × (1 − 0.12) = $2,186,600
- EAC = $320,000 + $2,186,600 = $2,506,600

### Method 3: Forecast by Burn Rate

Projects final cost based on average daily/weekly spending:

```
EAC = Actual Costs + (Daily Burn Rate × Days Remaining)
```

**Example:**
- Current Spent: $320,000
- Days Elapsed: 27
- Daily Burn Rate: $320,000 / 27 = $11,852/day
- Days Remaining: 124
- Forecast Remaining: $11,852 × 124 = $1,469,648
- EAC = $320,000 + $1,469,648 = $1,789,648

## Variance Analysis

Variance tracking identifies where costs deviate from plan:

### Budget Variance by Division

```
Budget Variance = Current Budget − Total Forecast

Or as % of Budget:
Variance % = (Budget Variance / Current Budget) × 100%
```

**Example — Division 03 (Concrete):**
- Current Budget: $190,000
- Total Forecast (invoiced + remaining): $195,000
- Variance: −$5,000 (5.3% over budget)
- Flag: Red alert when variance exceeds ±5%

### Schedule Variance Impact on Costs

When a project falls behind schedule, labor and overhead costs extend:

```
Schedule Variance Cost = Daily overhead rate × Days behind schedule

Where:
  Daily overhead = (Division 01 budget / Total project days)
```

**Example:**
- General Requirements (overhead): $145,000
- Total project days: 151
- Daily overhead: $145,000 / 151 = $961/day
- If 10 days behind schedule:
- Schedule Variance Cost = $961 × 10 = $9,610

### Material Cost Variance

Actual material costs vs. estimated:

```
Material Variance = (Actual Material Cost − Budgeted Material Cost)

By Line Item:
  Concrete variance = Actual spent on concrete − budgeted for concrete
  Steel variance = Actual spent on steel − budgeted for steel
```

**Example:**
- Budgeted PEMB Steel (Division 05): $85,000
- Committed through supplier POs: $88,500
- Material Variance: −$3,500 (4.1% over)

## Contingency Tracking

Contingency is reserve funds to cover unforeseen conditions and changes:

```json
{
  "contingency": {
    "original_contingency_amount": 150000,
    "contingency_percentage_of_budget": 5.4,
    "spent_against_contingency": [
      { "co_id": "CO-001", "amount": 50000, "description": "Owner-directed scope addition" },
      { "co_id": "CO-003", "amount": -15000, "description": "Value engineering credit" }
    ],
    "total_spent_from_contingency": 35000,
    "available_contingency": 115000,
    "available_contingency_percentage": 4.1,
    "drawdown_rate_per_month": 5833,
    "months_of_contingency_remaining": 19.7,
    "alert_threshold_percent": 50,
    "contingency_status": "healthy"
  }
}
```

**Contingency Drawdown Rules:**
- 0–25% drawn: Green — Healthy reserve
- 25–50% drawn: Yellow — Monitor closely
- 50–75% drawn: Orange — Review budget; may need change order to owner
- 75%+ drawn: Red — Contingency at risk

## Invoice Reconciliation Process

### Sub Invoice Verification Workflow

1. **Receive Sub Invoice**: Sub submits invoice for work/materials
2. **Verify Against SOV**: Check invoice amount ≤ (% complete × contract amount)
3. **Cross-Reference with Pay App**: Confirm line items match SOV
4. **Flag Overbilling**: If invoice > % complete, reject or request clarification
5. **Apply Retainage**: Hold back 10% (or contract rate) from payment
6. **Process Payment**: Pay sub after conditional lien waiver received
7. **Update Cost Tracking**: Record payment in cost-data.json

### Overbilling Detection

```
Maximum billable amount = Line item contract amount × % complete

Example:
  Division 03 contract: $185,000
  Division 03 % complete: 45%
  Maximum billable: $185,000 × 0.45 = $83,250

  If invoice shows: $87,000 → FLAG OVERBILLING
  Difference: $3,750 excess
  Action: Request clarification or deny until work verified
```

### Retainage Tracking by Sub

```json
{
  "sub_retainage_tracking": {
    "subcontractor": "W Principles (Concrete)",
    "contract_amount": 185000,
    "invoiced_to_date": 120000,
    "retainage_rate": 0.10,
    "retainage_held": 12000,
    "amount_paid": 108000,
    "percent_complete": 65,
    "retainage_policy": "W Principles flat 10% until substantial completion",
    "retainage_released_at_substantial_completion": true,
    "notes": "Flat 10% retainage per W Principles standard"
  }
}
```


## Project Intelligence Integration

When project intelligence is loaded, cross-reference cost data against extracted quantities, schedule progress, and procurement to identify cost risks early.

### Quantity Verification
Compare budgeted quantities against plan-extracted quantities:
- Read `plans-spatial.json` → `quantities` → for each CSI division, sum the relevant quantities (concrete CY, wall SF, flooring SF, fixture counts, etc.)
- Compare against budget line items in `cost-data.json` → `budget_by_division[]`
- Calculate: Plan quantity × estimated unit rate vs budget amount
- Flag divisions where plan quantities exceed budget quantities by >5% — this indicates the estimate may have missed scope
- Example: Division 03 budget assumes 38 CY total concrete, but plans-spatial.json quantities show 42.3 CY → flag 11% overage for review

### Schedule-Cost Alignment
Cross-check cost progress against schedule progress:
- Read `schedule.json` → `percent_complete` → overall project progress
- Compare with cost % complete per division: (invoiced_costs / current_amount) for each budget line
- Flag front-loading: If cost % complete significantly exceeds schedule % complete for a division, the sub may be overbilling
- Flag lagging: If cost % complete is far below schedule % complete, work may be unbilled or behind
- Example: Schedule 25% complete, Division 03 (Concrete) 40% billed → possible front-loading

### Change Order Linkage
Verify change order cost impacts are properly reflected in budget:
- Read `change-order-log.json` → for each CO with status "approved"
- Check that the CO's `cost_approved` amount appears in the correct budget division's `applied_cos[]` array
- Flag any approved COs not yet reflected in budget divisions
- Example: CO-005 approved for $17,800 affecting Division 26 → verify Division 26 `applied_cos` includes CO-005

### Procurement Cost Tracking
Compare committed material costs against budget line items:
- Read `procurement-log.json` → sum `total_cost` by spec section → map to CSI divisions
- Compare against budget division `committed_costs`
- Flag material cost overruns before they hit invoicing
- Example: Procurement for Division 05 (Steel) totals $88,500 committed, but budget shows $85,000 → flag $3,500 (4.1%) material cost overrun

---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
