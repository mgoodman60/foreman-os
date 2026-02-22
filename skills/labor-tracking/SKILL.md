---
name: labor-tracking
description: >
  Track per-worker and per-crew labor hours by trade, calculate labor productivity ratios (output per labor-hour), support certified payroll compliance, and feed EVM actual cost calculations. Provides daily headcount validation against daily report crew counts and weekly labor summaries. Triggers: "time card", "timecard", "labor hours", "crew hours", "headcount", "man-hours", "labor productivity", "certified payroll", "labor tracking", "labor report", "overtime", "labor cost", "crew size", "work hours", "time tracking".
version: 1.0.0
---

# Labor Tracking Skill for Foreman OS

## Overview

The **labor-tracking** skill provides comprehensive labor hour management and productivity analysis for construction projects. It enables daily labor data entry, crew-level summary tracking, worker classification management, and automated cross-validation against daily reports. The skill calculates labor productivity ratios, supports Davis-Bacon certified payroll compliance, and integrates with earned-value management (EVM) for actual cost (AC) calculations.

### Core Functions

- **Daily Labor Entry**: Log worker hours by trade, classification, and cost code
- **Crew Management**: Track crew composition, headcount, and work accomplished
- **Productivity Metrics**: Calculate output-per-labor-hour ratios and efficiency factors
- **Weekly Summaries**: Aggregate hours, costs, and trends by trade
- **Daily Report Validation**: Cross-check labor entries against crew counts in daily reports
- **Certified Payroll**: Generate Davis-Bacon WH-347 form data and prevailing wage tracking
- **Cost Integration**: Feed actual labor costs into EVM and project dashboard

---

## 1. Labor Entry Data Model

### Primary Labor Entry Schema (JSON)

```json
{
  "entry_id": "LAB-2026-02-19-001",
  "date": "2026-02-19",
  "worker_name": "John Smith",
  "trade": "Concrete",
  "employer": "W Principles",
  "classification": "journeyman",
  "hours_regular": 8.0,
  "hours_overtime": 2.0,
  "hours_double_time": 0.0,
  "work_description": "Footing excavation and prep, rebar layout",
  "location_grid": "X2-Y3",
  "cost_code": "03-1000-02",
  "cost_code_description": "Concrete Foundations - Labor",
  "prevailing_wage_classification": "Concrete Worker - Journeyman",
  "hourly_rate_base": 52.50,
  "hourly_rate_burdened": 78.75,
  "weather": "Clear, 42F",
  "notes": "Overtime for footing critical path acceleration",
  "certified_payroll_flag": true,
  "fringe_benefits_included": true,
  "timestamp": "2026-02-19T16:45:00Z"
}
```

### Field Definitions

| Field | Type | Notes |
|-------|------|-------|
| entry_id | String | Unique identifier (format: LAB-YYYY-MM-DD-###) |
| date | Date | Labor date (YYYY-MM-DD) |
| worker_name | String | Full name (required for payroll) |
| trade | String | Primary trade (Concrete, Steel, Framing, MEP, Finishes, Sitework, etc.) |
| employer | String | Subcontractor name or "Self-Perform" |
| classification | Enum | journeyman, apprentice, foreman, superintendent, laborer, operator, inspector |
| hours_regular | Decimal | Standard hours (40-hr base week) |
| hours_overtime | Decimal | Overtime hours (1.5x multiplier) |
| hours_double_time | Decimal | Double-time hours (2x multiplier, typically premium OT or holidays) |
| work_description | String | Detailed work performed (ties to daily report) |
| location_grid | String | Building location (X1-Y2, etc.) |
| cost_code | String | CSI division code (e.g., 03-1000-02 for concrete labor) |
| prevailing_wage_classification | String | Davis-Bacon classification (if applicable) |
| hourly_rate_base | Decimal | Base hourly rate (before burdened costs) |
| hourly_rate_burdened | Decimal | Fully loaded rate (base + fringe + overhead) |
| fringe_benefits_included | Boolean | Davis-Bacon fringe flag |
| certified_payroll_flag | Boolean | Include in WH-347 report |
| timestamp | ISO 8601 | System-generated entry time |

---

## 2. Crew Summary Model

### Crew-Level Aggregation (JSON)

```json
{
  "crew_id": "CRW-2026-02-19-CONCRETE-01",
  "date": "2026-02-19",
  "trade": "Concrete",
  "employer": "W Principles",
  "crew_size": 6,
  "foreman_name": "Mike Johnson",
  "foreman_classification": "foreman",
  "total_hours": 48.5,
  "total_hours_regular": 46.0,
  "total_hours_overtime": 2.5,
  "total_hours_double_time": 0.0,
  "labor_cost_base": 2541.00,
  "labor_cost_burdened": 3817.50,
  "work_accomplished": {
    "description": "Footing rebar layout and tie, stem wall formwork setup",
    "quantity": 145.0,
    "unit": "linear feet of footing rebar"
  },
  "productivity_ratio": {
    "output": 145.0,
    "labor_hours": 48.5,
    "ratio": 2.99,
    "ratio_unit": "LF rebar per labor-hour"
  },
  "benchmark_ratio": 3.25,
  "efficiency_factor": 0.92,
  "performance_rating": "Good",
  "weather_impacts": "None",
  "equipment_used": ["Excavator", "Compressor", "Circular saw"],
  "daily_report_reference": "DR-2026-02-19",
  "notes": "Crew ahead of schedule on footing prep",
  "timestamp": "2026-02-19T17:30:00Z"
}
```

### Crew Summary Fields

| Field | Type | Notes |
|-------|------|-------|
| crew_id | String | Unique crew identifier |
| trade | String | Primary trade discipline |
| crew_size | Integer | Number of workers on site today |
| foreman_name | String | Crew foreman/lead |
| total_hours | Decimal | Sum of all worker hours (including OT multipliers) |
| labor_cost_burdened | Decimal | Total crew cost (hours × burdened rate) |
| work_accomplished | Object | What was produced (description, quantity, unit) |
| productivity_ratio | Object | Output per labor-hour calculation |
| benchmark_ratio | Decimal | Target/standard for this trade |
| efficiency_factor | Decimal | Actual ÷ Benchmark (100% = on track) |
| daily_report_reference | String | Cross-link to daily report document |

---

## 3. Productivity Metrics

### Labor Productivity Ratio Calculation

**Formula:**
```
Productivity Ratio = Units of Output ÷ Total Labor-Hours

Labor Efficiency Factor = Actual Productivity Ratio ÷ Benchmark Ratio
```

### Benchmark Standards by Trade

| Trade | Output Unit | Benchmark Ratio | Basis | Notes |
|-------|------------|-----------------|-------|-------|
| Concrete (Footings) | Linear feet of footing | 3.25 LF/hr | Industry standard | Excavation, rebar, formwork, pour |
| Concrete (SOG) | Square feet poured | 120 SF/hr | Structural slab | Finishing included |
| Steel Erection | Tons hoisted | 2.5 T/hr | PEMB assembly | Includes bolting |
| CFS Framing | Studs installed | 15 studs/hr | Metal framing @ 16" OC | Interior partitions |
| Drywall | Square feet hung | 85 SF/hr | Hanging only | Finishing separate |
| MEP Rough-In | Linear feet of pipe/ductwork | 45 LF/hr | Combined MEP | Average across trades |
| Roofing | Square feet installed | 35 SF/hr | Panel install + fastening | Metal standing seam |
| Finishes | Square feet finished | 120 SF/hr | Paint + trim | Both walls and trim |

### Weekly Productivity Tracking

```json
{
  "week": "2026-02-17 to 2026-02-23",
  "trade": "Concrete",
  "entries": 5,
  "productivity_data": [
    {
      "date": "2026-02-19",
      "crew": "CRW-2026-02-19-CONCRETE-01",
      "ratio": 2.99,
      "benchmark": 3.25,
      "efficiency": 0.92
    },
    {
      "date": "2026-02-20",
      "crew": "CRW-2026-02-20-CONCRETE-01",
      "ratio": 3.18,
      "benchmark": 3.25,
      "efficiency": 0.98
    }
  ],
  "weekly_average_efficiency": 0.95,
  "trend": "steady",
  "forecast": "On track for weekly target"
}
```

### Earned Hours vs Actual Hours (Labor Efficiency)

```
Earned Hours = Standard Hours × Efficiency Factor
Labor Cost Variance = (Actual Hours - Earned Hours) × Burdened Rate

If Crew 1: 50 actual hours, 3.0 ratio actual vs 3.25 benchmark
  Earned Hours = 50 × (3.0 ÷ 3.25) = 46.15 hours
  Over-run = 3.85 labor-hours
  Cost Variance = 3.85 × $78.75 = $303.19 unfavorable
```

---

## 4. Weekly Labor Summary

### Labor Summary Report (JSON)

```json
{
  "report_id": "LAB-WEEKLY-2026-W08",
  "week": "2026-02-17 to 2026-02-23",
  "project": "MOSC",
  "phase": "Foundation / Sitework",
  "generated_date": "2026-02-23",
  "summary_by_trade": [
    {
      "trade": "Concrete",
      "total_workers": 8,
      "total_hours_regular": 280.0,
      "total_hours_overtime": 12.0,
      "total_hours_double_time": 0.0,
      "total_labor_hours": 292.0,
      "ot_percentage": 4.1,
      "labor_cost_base": 14560.00,
      "labor_cost_burdened": 21840.00,
      "budget_labor_hours": 300.0,
      "variance_hours": -8.0,
      "variance_cost": -630.00,
      "status": "Favorable"
    },
    {
      "trade": "Sitework / Excavation",
      "total_workers": 4,
      "total_hours_regular": 152.0,
      "total_hours_overtime": 8.0,
      "total_hours_double_time": 0.0,
      "total_labor_hours": 160.0,
      "ot_percentage": 5.0,
      "labor_cost_burdened": 12600.00,
      "budget_labor_hours": 160.0,
      "variance_hours": 0.0,
      "status": "On Budget"
    }
  ],
  "weekly_totals": {
    "total_workers_active": 12,
    "total_labor_hours": 452.0,
    "total_overtime_hours": 20.0,
    "total_ot_percentage": 4.4,
    "total_labor_cost_burdened": 34440.00,
    "budget_total_hours": 460.0,
    "budget_total_cost": 36225.00,
    "variance_hours": -8.0,
    "variance_cost": -1785.00,
    "variance_percentage": -4.9
  },
  "headcount_trend": {
    "monday": 12,
    "tuesday": 12,
    "wednesday": 11,
    "thursday": 12,
    "friday": 12,
    "average": 11.8,
    "previous_week_average": 9.5,
    "change_percentage": 24.2
  },
  "top_overtime_contributors": [
    {
      "worker_name": "Mike Johnson",
      "trade": "Concrete",
      "ot_hours": 8.0,
      "reason": "Critical path footing acceleration"
    },
    {
      "worker_name": "Jim Wilson",
      "trade": "Concrete",
      "ot_hours": 4.0,
      "reason": "Rebar tie-off completion"
    }
  ],
  "alerts": [
    {
      "level": "info",
      "message": "OT at 4.4% - within acceptable range"
    },
    {
      "level": "success",
      "message": "Headcount increased 24.2% - good mobilization progress"
    }
  ]
}
```

---

## 5. Daily Report Cross-Validation

### Validation Workflow

The labor-tracking skill automatically compares daily labor entries against crew counts reported in daily reports. This ensures consistency and flags discrepancies for investigation.

#### Validation Rules

```json
{
  "validation_rules": [
    {
      "rule_id": "VR-001",
      "name": "Crew Size Match",
      "logic": "Count of unique workers logged in labor entries == reported crew size in daily report",
      "tolerance": 0,
      "action": "Flag if mismatch"
    },
    {
      "rule_id": "VR-002",
      "name": "Trade Completeness",
      "logic": "All active trades in daily report must have labor entries",
      "tolerance": 0,
      "action": "Alert if trade missing"
    },
    {
      "rule_id": "VR-003",
      "name": "Overtime Reporting",
      "logic": "Overtime hours logged must match overtime note in daily report",
      "tolerance": 0.5,
      "action": "Flag for reconciliation if >0.5 hr difference"
    },
    {
      "rule_id": "VR-004",
      "name": "Headcount Trend",
      "logic": "Crew size drop >30% from previous week triggers alert",
      "tolerance": 30.0,
      "action": "Alert - verify reason for reduction"
    }
  ]
}
```

#### Daily Validation Report

```json
{
  "validation_report_id": "VAL-2026-02-19",
  "date": "2026-02-19",
  "daily_report_id": "DR-2026-02-19",
  "validation_status": "PASS_WITH_NOTES",
  "checks_performed": {
    "crew_size_match": {
      "status": "PASS",
      "daily_report_count": 6,
      "labor_entry_count": 6,
      "discrepancy": 0
    },
    "trade_completeness": {
      "status": "PASS",
      "trades_in_daily_report": ["Concrete", "Sitework"],
      "trades_with_labor_entries": ["Concrete", "Sitework"],
      "missing_trades": []
    },
    "overtime_verification": {
      "status": "PASS",
      "ot_hours_in_daily_report": 2.5,
      "ot_hours_in_labor_entries": 2.5,
      "discrepancy": 0.0
    },
    "cost_code_alignment": {
      "status": "PASS",
      "work_description_match": true
    }
  },
  "discrepancies": [],
  "notes": "All labor entries align with daily report. Foreman signed off on accuracy.",
  "reconciliation_status": "COMPLETE",
  "timestamp": "2026-02-19T18:00:00Z"
}
```

---


## Project Intelligence Integration

When project intelligence is loaded, auto-resolve locations, validate employers, benchmark productivity against plan quantities, and cross-validate against daily reports.

### Location Auto-Resolution
When the user provides a casual location for labor entries:
- Read `plans-spatial.json` → `building_areas[]` and `room_schedule[]` → resolve to grid reference, building area, and floor level
- Auto-fill the `location_grid` field with the resolved grid reference
- Example: User says "east wing second floor" → resolve to Grid E-G / 3-5, Level 2

### Employer Validation
When a labor entry's `employer` field is provided:
- Read `directory.json` → `subcontractors[]` → match by name (exact or fuzzy partial match)
- If match found: auto-correct to official company name from directory
- If no match found: flag `employer_matched: false` for review — the sub may not be in the directory yet
- Example: User enters "Walker" → resolve to "Walker Construction"

### Productivity Benchmarking
When a crew summary includes `work_accomplished` with measurable output:
- Read `plans-spatial.json` → `quantities` → find the total plan quantity for the work type
- Calculate output-per-labor-hour and compare against benchmark ratios
- For concrete work: Calculate CY placed per labor-hour vs 0.040 CY/hr benchmark
- For framing: Calculate studs installed per labor-hour vs 15 studs/hr benchmark
- For drywall: Calculate SF hung per labor-hour vs 85 SF/hr benchmark
- Include plan total as context: "12 CY poured today of 42.3 CY total footings (28%)"

### Daily Report Cross-Validation
When labor entries exist for a date that also has a daily report:
- Read `daily-report-intake.json` or `daily-report-data.json` → crew section
- Compare logged crew headcounts per trade against labor tracking entries per trade
- Flag mismatches: "Daily report shows 6 concrete workers, labor tracking has 5 entries for concrete"
- Compare overtime hours reported in daily report against overtime in labor entries

### Cost Code Mapping
When a labor entry has trade and work description but no cost code:
- Read `specs-quality.json` → `spec_sections[]` → match work description to CSI section
- Suggest the appropriate cost code based on trade → CSI division mapping
- Example: trade="Concrete", work="Footing rebar layout" → suggest cost code 03-2000 (Concrete Reinforcement)

---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
