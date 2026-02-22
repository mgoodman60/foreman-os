---
name: delay-tracker
description: >
  Track construction delays systematically for contract extension requests and delay claims documentation. Classify delay type, track critical path impact vs. float absorption, calculate contract extension earned, and manage weather delay verification. Integrates with daily reports, RFIs, and change orders. Triggers: "delay", "schedule delay", "weather delay", "delay event", "time impact", "contract extension", "delay claim", "log a delay", "delay status", "delay report".
version: 1.0.0
---

# Delay Tracker Skill

## Overview

The **delay-tracker** skill provides systematic construction delay management for superintendents and project managers. It enables tracking delays from field observation through documentation, contract extension request, or delay claims preparation—ensuring contemporaneous records, proper classification, and defensible delay calculations per construction contract standards.

## Delay Classification Taxonomy

Delays are classified by **type** to enable proper allocation of responsibility and contractual remedies. Each type carries different excusability and compensability implications per standard AIA and AGC contract documents.

### Delay Type Categories

#### 1. **Weather Delays**
**Definition**: Delays caused by weather conditions exceeding contract thresholds; typically defined by specs/ACI standards.

**Examples**:
- Concrete placement delayed by ambient temperature below 40°F (ACI 306)
- Roofing operations halted due to wind exceeding 25 MPH (OSHA 1926.752)
- Asphalt paving delayed by ambient temp below 50°F and surface below 40°F
- Earthwork suspended due to precipitation or frozen material
- Temporary erosion control required due to heavy rain
- High winds causing crane work restrictions

**Typical Classification**:
- **Excusable**: YES (standard in all contracts)
- **Compensable**: NO (owner not responsible for acts of nature)
- **Duration Tracking**: Compare actual weather vs. NOAA 30-year average baseline
- **Documentation**: Daily weather observations (temperature, precipitation, wind) + NOAA data

**Threshold Source**: `specs-quality.json` `weather_thresholds` (project-specific maximums/minimums)

#### 2. **Owner-Directed Delays**
**Definition**: Delays caused by owner-initiated changes, decisions, or directives.

**Examples**:
- Owner requests scope modification or additional work not in original contract
- Owner delays decision on material selections, finishes, or procurement
- Owner suspends work on portion of site for extended period
- Owner changes project phasing or sequencing from original schedule
- Owner delays approval of submittals beyond architect's review period
- Owner changes design or plans affecting already-fabricated materials
- Owner requires rework of completed areas due to owner dissatisfaction (non-defect)

**Typical Classification**:
- **Excusable**: YES (owner responsibility)
- **Compensable**: YES (contractor entitled to recover costs + overhead + profit)
- **Duration Tracking**: Calendar days from owner directive to work resumption
- **Documentation**: Owner emails/directives, change order requests, meeting notes, photos of pause conditions

**Claims Basis**: These delays typically support time + cost claims (T&M documentation + daily report support)

#### 3. **Design/Specification Issues**
**Definition**: Delays caused by design errors, incomplete plans, specification conflicts, or architect decisions.

**Examples**:
- Architect issues addendum/clarification requiring rework or re-procurement
- Plans show conflicting dimensions or conflicting spec requirements
- Specification requires unavailable material or proprietary item with long lead time
- Architect rejects submittal and requires re-design/re-submittal cycle
- Structural engineer requires field modifications to accommodate existing conditions
- Design does not account for site conditions shown on survey (differing site conditions borderline)
- MEP conflicts discovered in field require architect resolution

**Typical Classification**:
- **Excusable**: YES (architect responsibility)
- **Compensable**: Typically YES (contractor not responsible for design adequacy)
- **Duration Tracking**: Days from issue identification to architect resolution
- **Documentation**: RFIs, architect responses, addenda, revised submittals, daily reports documenting pause

**Claims Basis**: Strong basis for time + cost recovery (design delay = architect liability)

#### 4. **Material/Supply Chain Delays**
**Definition**: Delays caused by unavailability, late delivery, or quality issues with materials or equipment.

**Examples**:
- Supplier delivery delayed beyond promised date (steel, PEMB, windows, doors, equipment)
- Material arrives damaged and requires replacement
- Material fails quality inspection and supplier provides replacement with additional lead time
- Supplier production capacity issues cause extended lead time
- Procurement lead time underestimated during planning phase
- Manufacturer backlog due to market demand
- Shipping/logistics delays (trucking, rail, port congestion)

**Typical Classification**:
- **Excusable**: DEPENDS on contract (typically only if supplier is "beyond contractor's control")
- **Compensable**: DEPENDS on contract language
- **Duration Tracking**: Days from original promised delivery to actual delivery
- **Documentation**: POs, supplier correspondences, delivery confirmations, photos of unopened materials

**Key Distinction**: If contractor selected the supplier and accepted delivery terms, contractor typically bears risk. If owner-specified supplier or owner approved extended lead time, contractor may have excusable delay argument.

**Claims Basis**: Limited — best if owner approved the supplier or extended lead time was owner-directed

#### 5. **Subcontractor Performance Delays**
**Definition**: Delays caused by subcontractor inability to perform (staffing, equipment failure, rework, poor productivity).

**Examples**:
- Sub cannot mobilize sufficient crew despite multiple requests
- Sub's equipment breaks down and replacement delayed
- Sub's work quality deficient, requiring extensive rework
- Sub abandons project or fails to perform, requiring replacement
- Sub's work is out of sequence and blocks subsequent trades
- Sub prioritizes other projects over contracted timeline
- Sub files for bankruptcy or insolvency affecting project continuity
- Sub injury/fatality causes work suspension and investigation

**Typical Classification**:
- **Excusable**: NO (contractor liable for sub performance)
- **Compensable**: NO (contractor cannot claim damages from own sub)
- **Duration Tracking**: Calendar days from performance issue to resolution/replacement
- **Documentation**: Correspondence with sub, notices to perform, replacement crew documentation, daily reports

**Remedy**: Contract allows GC to require sub replacement, accelerated work, or payment for cost of remediation

**Claims Basis**: No time extension. GC absorbs cost and seeks cost recovery from sub surety or direct payment.

#### 6. **Force Majeure/Act of God**
**Definition**: Unforeseeable, uncontrollable events beyond any party's responsibility.

**Examples**:
- Earthquake, tsunami, or other natural disaster
- Pandemic/epidemic (COVID-19, etc.) with site closure mandate
- War, terrorism, civil unrest
- Extreme weather beyond normal forecasting (F5 tornado, unprecedented flooding, extreme heat wave)
- Utility failure/blackout affecting site operations for extended period
- Fire or explosion not caused by contractor actions
- Extraordinary strike or labor actions beyond contractor control

**Typical Classification**:
- **Excusable**: YES (beyond any party control)
- **Compensable**: TYPICALLY YES (mutual relief from obligations; may include cost recovery depending on contract)
- **Duration Tracking**: Days from event occurrence to operations resumption
- **Documentation**: News reports, government declarations, insurance reports, photos, daily weather data, government mandates

**Contract Clauses**: "Acts of God", "Force Majeure", "Suspension of Work" clauses apply

**Claims Basis**: Time extension clear; cost recovery depends on specific contract language

#### 7. **Permit/Regulatory Delays**
**Definition**: Delays caused by regulatory authority actions, permit issuance delays, or required inspections.

**Examples**:
- Building permit delayed due to plan review backlog
- Permit contingent on public hearing or neighbor notification
- Inspections scheduled far in advance; contractor cannot work until inspection
- Inspector rejects work and requires rework/re-inspection
- Regulatory agency (health department, environmental, etc.) issues stop-work order
- Zoning variance or conditional use permit delayed
- Federal/state environmental review requirement (NEPA, EIS) required before work
- Historic preservation review required

**Typical Classification**:
- **Excusable**: Typically YES (authority action beyond contractor control)
- **Compensable**: Typically YES (contractor not responsible for regulatory process)
- **Duration Tracking**: Days from permit request to issuance/inspection completion
- **Documentation**: Permit applications, correspondence with agencies, inspection reports, stop-work orders

**Claims Basis**: Strong basis for time extension; cost claims depend on whether contractor must bear costs of remedial measures

#### 8. **Differing Site Conditions**
**Definition**: Subsurface or site conditions materially different from those indicated in contract documents.

**Examples**:
- Excavation encounters rock (common in geotechnical contexts) when plans showed native soil
- Fill material 2-3 feet deeper than indicated on survey
- Existing utility discovered in field not shown on utility locates
- Soil bearing capacity inadequate; foundation design must be modified
- Groundwater/wet conditions worse than indicated; drainage/dewatering required
- Contaminated material encountered requiring EPA/environmental agency approval
- Existing building conditions worse than indicated (asbestos, mold, structural issues)

**Typical Classification**:
- **Excusable**: YES (differing from contract documents)
- **Compensable**: YES (contractor is entitled to cost recovery + time for the difference)
- **Duration Tracking**: Days from discovery to remediation completion
- **Documentation**: Original survey/geotechnical report + daily reports documenting actual conditions; photos; scope comparison

**Contract Clause**: "Changed Conditions" or "Differing Site Conditions" (DSC)

**Claims Basis**: Strongest basis for time + cost claims if properly documented with contemporaneous daily reports

---

## Excusable vs. Non-Excusable Classification Matrix

Excusability determines eligibility for time extension (not cost recovery). This matrix applies standard AIA/AGC contract interpretation:

| Delay Type | Excusable | Reason |
|------------|-----------|--------|
| Weather | YES | Beyond contractor control; standard in all contracts |
| Owner-Directed | YES | Owner responsibility; owner controls project decisions |
| Design/Spec Issues | YES | Architect responsibility; contractor not responsible for design adequacy |
| Material Delays | CONDITIONAL | Excusable if beyond contractor's control (owner-specified supplier, approved extended lead time); non-excusable if contractor selected supplier and accepted delivery terms |
| Sub Performance | NO | Contractor responsible for sub performance; contractor must manage/replace subs |
| Force Majeure | YES | Explicitly uncontrollable; standard force majeure clause |
| Permit/Regulatory | YES | Government authority action beyond contractor control |
| Differing Site Conditions | YES | Expressly provided in "Changed Conditions" clause |
| Concurrent Delays (Contractor + Owner) | PARTIAL | Time extension limited to excusable portion; non-excusable delays don't extend schedule |

## Compensable vs. Non-Compensable Classification Matrix

Compensability determines eligibility for cost recovery (in addition to time extension):

| Delay Type | Compensable | Cost Recovery Basis |
|------------|-------------|-------------------|
| Weather | NO | Standard risk allocation; contractor must budget for normal weather |
| Owner-Directed | YES | Cost + overhead + profit + extended general conditions |
| Design/Spec Issues | YES | Cost + overhead + profit; architect/owner liability |
| Material Delays | CONDITIONAL | YES if owner-specified supplier or approved extended lead time; NO if contractor's supply chain risk |
| Sub Performance | NO | Contractor absorbs cost; liability against sub surety |
| Force Majeure | CONDITIONAL | YES for cost to suspend/resume; may include cost of remediation depending on contract language |
| Permit/Regulatory | YES | Contractor entitled to cost recovery for remedial measures/compliance |
| Differing Site Conditions | YES | Cost recovery explicitly provided in "Changed Conditions" clause |

**Key Principle**: Time extensions and cost recovery are separate. A delay can be:
- Excusable + Non-compensable (weather) = get time extension, not cost recovery
- Excusable + Compensable (owner-directed) = get time extension AND cost recovery
- Non-excusable (sub performance) = no extension, no recovery

---

## Critical Path Analysis Methodology

Delay impact on project completion depends on whether the delay consumed project float or directly extended the critical path. This analysis is essential for contract extension calculations.

### Critical Path Definition

**Critical Path** = longest sequence of activities from project start to finish; any delay on this path extends overall project completion. Activities on the critical path have zero float.

**Float** (or slack) = amount of time an activity can slip without delaying project completion. Off-critical-path activities have positive float.

### Delay Impact Assessment

#### Scenario 1: Delay Consumes Float (No Extension)
```
Situation: Activity on non-critical path is delayed
Critical Path Duration: 150 days (unchanged)
Project Completion Impact: No change

Example:
- Interior finish trim work (non-critical) delayed 5 days
- Critical path: structural → MEP rough-in → MEP finish → paint → flooring
- Trim work has 8 days of float; 5-day delay consumes 3 days of available float
- Result: NO time extension earned (float absorbed the delay)

Delay Log Entry:
  "calendar_days": 5,
  "float_consumed_days": 5,
  "extension_days_earned": 0,
  "critical_path_impact": "absorbed_float"
```

#### Scenario 2: Delay Extends Critical Path (Full Extension)
```
Situation: Activity on critical path is delayed
Critical Path Duration: 150 → 157 days (extended 7 days)
Project Completion Impact: 7-day extension earned

Example:
- Weather delays concrete pour (critical activity) 7 days
- Critical path: structural → MEP rough-in → MEP finish → paint → flooring
- Concrete is critical; no float available
- Result: 7-day time extension earned; project completion moves from 150 to 157 days

Delay Log Entry:
  "calendar_days": 7,
  "float_consumed_days": 0,
  "extension_days_earned": 7,
  "critical_path_impact": "extended_completion"
```

#### Scenario 3: Partial Impact (Delay Consumes Float + Extends Path)
```
Situation: Activity delays beyond available float
Critical Path Duration: 150 → 154 days (extended 4 days)
Project Completion Impact: 4-day extension (out of 8-day delay)

Example:
- Sub performance issue delays MEP rough-in 8 days
- MEP rough-in has 4 days of float (scheduled 15 days, critical path needs 11)
- Delay consumes 4 days float, extends critical path 4 days
- Result: 4-day time extension earned; 4 days absorbed by float cushion

Delay Log Entry:
  "calendar_days": 8,
  "float_consumed_days": 4,
  "extension_days_earned": 4,
  "critical_path_impact": "partial"
```

### Critical Path Analysis Process

**Step 1: Load Baseline Schedule**
- Retrieve `schedule.json` baseline schedule with activities, durations, dependencies, and float values
- Identify activities marked as critical path (zero float)
- Note any schedule modifications or updates post-baseline

**Step 2: Determine Delay Impact on Activities**
For each delayed activity:
- Activity ID and name
- Original baseline duration
- Available float (slack) from baseline schedule
- Original scheduled start/finish dates
- Actual start/finish dates (from daily reports or field observation)

**Step 3: Calculate Float Consumption**
```
Float Consumed = MIN(Delay Days, Available Float)
```

If delay is 5 days and activity has 8 days of float:
- Float Consumed = MIN(5, 8) = 5 days
- Extension Days = 5 - 5 = 0 (no extension earned)

If delay is 12 days and activity has 4 days of float:
- Float Consumed = MIN(12, 4) = 4 days
- Extension Days = 12 - 4 = 8 days extension earned

**Step 4: Determine Critical Path Impact**
Update baseline schedule with actual activity dates and recalculate critical path:
- Recalculate project completion date with delayed activity dates
- Identify if original critical path is affected or if secondary path became critical
- Determine cumulative impact on all downstream activities

**Step 5: Concurrent Delay Identification**
**Critical**: If multiple delays overlap, assess whether they are on the same path:

```
Scenario A: Sequential Delays (different paths)
  Path 1: Weather delays concrete 5 days (has 2 days float) → 3-day extension
  Path 2: Sub delay on MEP 4 days (has 6 days float) → 0-day extension
  Total Extension: 3 days (weather delay alone extends project)

Scenario B: Concurrent Delays (same critical path)
  Delay 1: Owner decision delays MEP start 7 days (critical path)
  Delay 2: Supply delay affects MEP scope 5 days (overlaps owner delay)
  Result: Delays overlap; total extension is MAX(7, 5) = 7 days, NOT 12 days
  (Concurrent delays don't stack; use longest delay impact)

Delay Log Entry for Concurrent Scenario:
  "concurrent_delays": ["DELAY-001", "DELAY-002"],
  "extension_days_earned": 7  (not 12)
  "notes": "Delays overlap 2026-02-20 to 2026-02-25. Total extension is 7 days (maximum of concurrent impacts)."
```

**Key Rule**: When delays overlap on the same critical path, the extension is the **maximum** delay impact, not the sum. Contract extension only extends once, not multiple times for concurrent delays.

### Documenting Critical Path Impact in Delay Log

Required fields for critical path analysis:
```json
{
  "critical_path_impact": "[extended_completion|absorbed_float|partial]",
  "float_consumed_days": "[number]",
  "extension_days_earned": "[number]",
  "concurrent_delays": ["[DELAY-NNN if overlapping]"],
  "original_completion_date": "2026-07-29",
  "revised_completion_date": "[recalculated from schedule]",
  "schedule_analysis_performed": true,
  "notes": "[description of critical path analysis, including which activities affected]"
}
```

---


## Project Intelligence Integration

When project intelligence is loaded, auto-enrich delay entries with schedule impact analysis, weather verification, cost calculations, and historical context from project data files.

### Critical Path Impact
Automatically assess whether a delay extends the critical path or absorbs float:
- Read `schedule.json` → `critical_path[]` → when a delay affects an activity, check if it is on the critical path (zero float) vs. has float to absorb
- Calculate: `extension_days_earned` = MAX(0, delay_days - available_float)
- Auto-populate delay log entry with `critical_path_impact`, `float_consumed_days`, and `extension_days_earned`
- Example: 5-day delay on activity with 3 days float → float_consumed=3, extension_earned=2, impact="partial"

### Weather Delay Verification
Verify reported weather delays against contractual thresholds:
- Read `specs-quality.json` → `weather_thresholds[]` → for the affected work type, pull the specific temperature/wind/rain threshold
- Compare against actual weather conditions from `daily-report-data.json` → `weather` records for the delay period
- Auto-classify as "excusable" if actual conditions exceeded contractual thresholds
- Example: Concrete pour delayed, threshold is min 40F → daily report shows 33F high → excusable weather delay confirmed

### Contemporaneous Weather Records
Build defensible weather documentation from daily reports:
- Read `daily-report-data.json` → filter by date range of the delay → extract weather observations (temperature, precipitation, wind)
- Cross-reference with NOAA 30-year baseline data for the project location
- Auto-populate delay log with contemporaneous weather records for claims support
- Example: Feb 10-14 delay → daily reports show: 10th=28F/snow, 11th=31F/ice, 12th=35F/rain, 13th=38F/clear, 14th=42F/clear → 3 weather days documented

### Cost Impact Calculation
Calculate the financial impact of each delay:
- Read `cost-data.json` → pull general conditions daily rate (site supervision, equipment rental, temporary facilities)
- Calculate: delay_days × daily_GC_rate = delay cost (crew standby, equipment idle, extended general conditions)
- Read `labor-tracking.json` → identify crews on standby during delay → add standby labor cost
- Example: 3-day weather delay × $2,800/day GC rate + $1,200 standby labor = $9,600 delay cost

### Related Delays
Surface prior delays with same cause type for cumulative impact:
- Read `delay-log.json` → `delay_events[]` → filter by matching delay type → surface prior delays with same cause
- Calculate cumulative delay days by type for pattern analysis and cumulative impact claims
- Flag when cumulative delays of one type exceed 10 days → recommend formal delay claim preparation
- Example: 3rd weather delay this month → cumulative 11 weather days → flag for formal extension request

### Schedule Float Analysis
Show remaining float context for the affected activity:
- Read `schedule.json` → for the affected activity, pull total float, free float, and predecessor/successor relationships
- Show whether the delay pushes the activity onto the critical path or merely reduces float cushion
- Auto-update float values after recording the delay
- Example: Activity had 8 days total float before this 5-day delay → remaining float = 3 days → activity now near-critical

---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
