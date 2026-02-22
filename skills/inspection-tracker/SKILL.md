---
name: inspection-tracker
description: >
  Track inspections and permits through the construction lifecycle. Handles scheduling, result logging, re-inspection tracking, permit management, and status reporting. Healthcare-specific: state health dept inspections, life safety, ADA compliance. PEMB-specific: anchor bolt, high-strength bolt, moment connection special inspections. Integrates with morning brief and look-ahead. Triggers: "inspection", "schedule inspection", "log inspection", "inspection status", "permit", "failed inspection", "re-inspect", "upcoming inspections", "special inspection".
version: 1.0.0
---

# Inspection Tracker Skill

## Overview

The Inspection Tracker skill manages all construction inspections and permits throughout the project lifecycle. It provides real-time scheduling, result logging, re-inspection workflows, permit tracking, and comprehensive status reporting with integration into daily project management routines.

## Data Model

### Inspection Object

```json
{
  "id": "INSP-001",
  "type": "Concrete Pre-placement",
  "date_scheduled": "2025-03-15T09:00:00Z",
  "date_completed": null,
  "inspector": "John Smith",
  "result": null,
  "notes": "",
  "deficiencies": [],
  "re_inspection_required": false,
  "re_inspection_id": null,
  "linked_schedule_activity": "SAC-042",
  "linked_hold_point": "HP-08",
  "linked_spec_section": "3.2.1",
  "location": "Building A, Level 2",
  "photos": [],
  "status": "scheduled"
}
```

**Fields:**
- `id`: Unique identifier (INSP-001, INSP-002, etc.)
- `type`: Inspection classification (see Standard & Special Inspection Types)
- `date_scheduled`: ISO 8601 timestamp
- `date_completed`: Completion timestamp; null if not yet completed
- `inspector`: Name of inspector; external if not in approved list
- `result`: `pass`, `fail`, `conditional`, `cancelled`, or `null` if pending
- `notes`: Detailed observations, findings, or cancellation reason
- `deficiencies`: Array of identified issues requiring correction (if result = fail)
- `re_inspection_required`: Boolean; true if result = fail
- `re_inspection_id`: Reference to linked re-inspection (INSP-NNN)
- `linked_schedule_activity`: Schedule activity ID for smart linking (e.g., SAC-042)
- `linked_hold_point`: Spec hold point reference (e.g., HP-08)
- `linked_spec_section`: CSI specification section (e.g., 3.2.1)
- `location`: Physical location (room, area, grid reference)
- `photos`: Array of photo file paths or URLs for evidence
- `status`: `scheduled`, `completed`, `cancelled`, `hold` (awaiting prerequisites)

### Permit Object

```json
{
  "id": "PERMIT-001",
  "type": "Building Permit",
  "number": "BP-2025-4521",
  "date_applied": "2025-02-01",
  "date_issued": "2025-02-20",
  "expiration": "2026-02-20",
  "jurisdiction": "City Building Department",
  "status": "active",
  "conditions": ["Final inspection before occupancy", "Weekly inspection during excavation"],
  "inspections_required": ["INSP-001", "INSP-003"],
  "notes": ""
}
```

**Fields:**
- `id`: Unique identifier (PERMIT-001, PERMIT-002, etc.)
- `type`: Permit classification
- `number`: Official permit number
- `date_applied`: Application submission date
- `date_issued`: Date permit was issued; null if pending
- `expiration`: Expiration date for renewal tracking
- `jurisdiction`: Issuing authority
- `status`: `applied`, `issued`, `active`, `expired`, `renewed`
- `conditions`: Array of permit conditions or special requirements
- `inspections_required`: Array of inspection IDs required per permit
- `notes`: Additional remarks or tracking notes

## Standard Inspection Types

| ID | Type | Typical Spec Section | Hold Point | Notes |
|----|------|----------------------|------------|-------|
| 01 | Foundation | 3.1.1 | HP-01 | Before concrete placement |
| 02 | Concrete Pre-placement | 3.2.1 | HP-02 | Rebar, formwork, reinforcement |
| 03 | Rebar | 3.2.2 | HP-03 | Size, spacing, cover verification |
| 04 | Formwork | 3.2.3 | HP-04 | Structural adequacy, bracing |
| 05 | Structural Steel | 5.1.1 | HP-05 | Connections, bolt torque, straightness |
| 06 | Underground Utilities | 2.2.1 | HP-06 | Location, depth, protection |
| 07 | Electrical | 16.0.0 | HP-07 | Rough-in, panel installation, grounding |
| 08 | Plumbing | 22.0.0 | HP-08 | Rough-in, pressure test, slope |
| 09 | Mechanical | 23.0.0 | HP-09 | Equipment installation, ductwork |
| 10 | Fire Protection | 21.0.0 | HP-10 | Sprinkler lines, device placement |
| 11 | Insulation | 7.2.1 | HP-11 | R-value verification, continuity |
| 12 | Fireproofing | 7.1.1 | HP-12 | Applied thickness, coverage |
| 13 | Final | 01.7000 | HP-13 | Walk-through, punch list generation |

## Healthcare-Specific Inspections

| Type | Trigger | Requirement | Notes |
|------|---------|-------------|-------|
| Life Safety | Continuous | Code compliance | ADA accessibility, egress paths, alarm systems |
| ADA Compliance | Pre-occupancy | Americans with Disabilities Act | Ramps, doors, restrooms, signage |
| State Health Dept | Final | Health Dept approval | Medical gas outlets, emergency systems, infection control |
| Infection Control | Pre-occupancy | Special protocols | HVAC testing, surface finishes, hand hygiene stations |

## PEMB-Specific Special Inspections

Pre-Engineered Metal Building (PEMB) requires specialized inspections per AWS D1.1 and manufacturer specs:

| Type | Tolerance | Requirement | Notes |
|------|-----------|-------------|-------|
| Anchor Bolt | ±1/8" | Location & elevation | Grid reference, hold-down torque verification |
| High-Strength Bolt | ±1/32" | Proper tension | Calibrated wrench, bolt grade certification |
| Moment Connection | ±1/4" | Beam-to-column welds | 100% visual + UT inspection required |

**Special Inspection IDs:** INSP-PEMB-001, INSP-PEMB-002, etc.

## Auto-Linking Intelligence

The inspection-tracker skill automatically links inspections to project intelligence:

### Schedule Activity Linking
Query project intelligence for schedule activities matching inspection date and type:
- "Concrete Pour Day" → auto-link to concrete pre-placement inspection
- "Steel Erection Week 3" → auto-link to structural steel inspection
- "Electrical Rough-In Phase" → auto-link to electrical inspection

### Hold Point Linking
Cross-reference spec hold points from project spec database:
- Inspection type matched to standard hold point (HP-02, HP-05, etc.)
- Override if project-specific hold point defined
- Display linked hold point ID to superintendent

### Specification Section Linking
Auto-populate CSI specification section reference:
- Foundation → 3.1.1
- Concrete → 3.2.1
- Structural Steel → 5.1.1
- Electrical → 16.0.0

### Hold Point Auto-Population
Read `specs-quality.json` → `hold_points[]` → match inspection type to hold point by `work_type`:
- Pull the hold point's `inspection_name`, `trigger` condition, `inspector`, and `spec_reference`
- Auto-populate the inspection's `linked_hold_point` and `linked_spec_section` fields
- Example: Scheduling "Concrete Pre-placement" → match hold_points where work_type contains "Concrete" → auto-link HP-02 with trigger "Before concrete placement" and spec reference

### Weather Threshold Check
Before scheduling outdoor inspections:
- Read `specs-quality.json` → `weather_thresholds[]` → match by the inspection's work type
- Cross-check forecasted weather against `min_temp`, `max_temp`, `max_wind`, and `moisture_ok`
- Flag if weather conditions may prevent the inspection or the underlying work (e.g., concrete pour inspection + temp < 40°F cold weather threshold)
- Include mitigation measures from the spec when flagging

### Spec Section Deep-Link
When an inspection type is identified:
- Read `specs-quality.json` → `spec_sections[]` → find the matching CSI section
- Pull specific `testing` requirements (frequency, type, agency), acceptance criteria from `key_req`, and required documentation
- Auto-populate inspection notes with testing protocol and acceptance criteria
- Example: Compaction inspection → pull "95% modified Proctor, testing every 500 CY" from spec section

### Schedule Activity Linking (Enhanced)
- Read `schedule.json` → `critical_path[]` and `milestones[]` → match inspection date/type to schedule activities
- Auto-link inspection to schedule activity and flag if the activity is on the critical path
- If critical path: add note "Critical path activity — inspection delay will impact project completion"

### Drawing Reference
When inspection location is identified:
- Read `plans-spatial.json` → `sheet_cross_references.drawing_index[]` → find relevant structural/MEP drawings for the inspection location and discipline
- Include referenced sheet numbers in inspection record for field use
- Example: Foundation inspection at Grid C-3 → reference sheets S2.1, S5.1

## Re-Inspection Workflow

When inspection result = `fail`:

1. **Create Re-Inspection Entry:**
   - Auto-generate new INSP ID (sequential)
   - Set type as "{Original Type} (Re-inspection)"
   - Set `related_to` field to original inspection ID
   - Suggest date 48 hours after deficiency notification

2. **Track Deficiencies:**
   - Collect detailed deficiency descriptions
   - Log which contractor responsible for correction
   - Reference section of spec violated
   - Attach photos of deficiency

3. **Notification:**
   - Alert responsible trade contractor
   - Flag in morning brief
   - Include in daily report until re-inspection passed

4. **Closure:**
   - Log re-inspection result
   - Document corrective action taken
   - Release hold if pass
   - Create additional re-inspection if still fail

## Permit Tracking & Expiration Alerts

**Auto-Alert Thresholds:**
- **30 days to expiration:** Yellow flag in status report; suggest renewal inquiry
- **7 days to expiration:** Red flag; escalate to project manager
- **Expired:** Red flag; mark status as `expired`; notify responsible party

**Renewal Workflow:**
- Track date application submitted for renewal
- Update status to `renewed` upon reissuance
- Maintain continuous permit coverage throughout project

## Integration Points

### Morning Brief (`/morning-brief`)
Display under "Inspections & Permits" section:
- Upcoming inspections (next 24 hours) — show type, time, location, inspector
- Overdue inspections (no result logged) — Red flag with days overdue
- Permits expiring within 30 days — Yellow alert with days remaining

### Look-Ahead Schedule (`/look-ahead`)
Include scheduled inspections in weekly look-ahead:
- Inspections integrated by date into weekly view
- Show impact on critical path if hold point inspection
- Cross-reference with material delivery/contractor schedule
- Highlight PEMB special inspections with bold/asterisk

### Daily Report (`/daily-report`)
Section: "Inspections Today"
- Scheduled inspections for the day (time, type, location, inspector)
- Completed inspections from previous day (result, notes summary)
- Pending re-inspections affecting schedule
- Permit status reminder (expiring within 14 days)

## Error Handling & Validation

- **Duplicate Re-inspection:** Warn if re-inspection already exists for same deficiency
- **Invalid Inspector:** Log "External Inspector" if not in approved list; alert PM
- **Missing Linked Activity:** Alert if schedule activity cannot be found; allow manual entry
- **Permit Conflict:** Warn if inspection scheduled outside permit scope
- **Date Validation:** Reject inspection scheduled before permit issued
- **Status Consistency:** Prevent result logging if status ≠ `scheduled`

## Triggers & Voice Commands

- "Schedule an inspection"
- "Log inspection INSP-042"
- "Show inspection status"
- "What inspections are overdue?"
- "Upcoming inspections?"
- "Schedule a rebar inspection for Monday"
- "Inspection failed — need re-inspection"
- "Track permits"
- "When does the building permit expire?"
- "Special inspection — anchor bolts"
- "Healthcare inspection — state health dept"

## Safety Incident Tracking & Investigation

The safety incident tracking system captures all project injuries, near-misses, property damage, and environmental incidents. This module integrates incident documentation, root cause analysis, corrective action tracking, and OSHA compliance management.

### Incident Data Model

```json
{
  "incidents": [
    {
      "id": "INC-001",
      "date": "2026-02-18",
      "time": "10:30",
      "type": "injury | near_miss | property_damage | environmental | fire | utility_strike",
      "severity": "first_aid | medical_treatment | lost_time | fatality | near_miss",
      "location": "Grid C-3, Foundation Level",
      "description": "Worker stepped on unsecured rebar cap, punctured boot sole",
      "injured_party": { "name": "John Smith", "company": "ABC Concrete", "trade": "Ironworker" },
      "witnesses": ["Jane Doe — GC Superintendent"],
      "immediate_action": "First aid administered on site, worker returned to work",
      "root_cause_analysis": {
        "method": "5_why | fishbone | both",
        "findings": "Rebar caps not secured after formwork adjustment. No re-inspection after modification.",
        "contributing_factors": ["Housekeeping", "Incomplete re-inspection"]
      },
      "corrective_actions": [
        {
          "action": "Re-inspect all rebar caps in active pour areas daily",
          "responsible": "GC Superintendent",
          "due_date": "2026-02-19",
          "status": "open | in_progress | complete | verified"
        }
      ],
      "osha_recordable": false,
      "reported_to": ["Safety Director", "Project Manager"],
      "photos": [],
      "status": "open | under_investigation | corrective_actions_pending | closed"
    }
  ]
}
```

**Incident Fields:**
- `id`: Unique incident identifier (INC-NNN format)
- `date`: Date incident occurred (ISO 8601)
- `time`: Time of incident (HH:MM format)
- `type`: Incident classification (injury, near_miss, property_damage, environmental, fire, utility_strike)
- `severity`: Severity level for OSHA classification (first_aid, medical_treatment, lost_time, fatality, near_miss)
- `location`: Specific job site location (grid reference, room, building area)
- `description`: Detailed narrative of what happened (sequence of events, conditions, outcome)
- `injured_party`: Object with worker info (name, company, trade) — null if near-miss or no injury
- `witnesses`: Array of witness names and roles (e.g., "Jane Doe — GC Superintendent")
- `immediate_action`: Actions taken immediately after incident (first aid, emergency response, work stop)
- `root_cause_analysis`: Object with method, findings, and contributing factors
- `corrective_actions`: Array of corrective action items with responsible party, due date, and status
- `osha_recordable`: Boolean; true if meets OSHA recordable criteria (determined per OSHA 300 rules)
- `reported_to`: Array of parties notified (Safety Director, Project Manager, OSHA if required, owner)
- `photos`: Array of incident scene photos (time-stamped)
- `status`: Current incident status (open, under_investigation, corrective_actions_pending, closed)

### Near-Miss Tracking

Near-misses use the same data model as injuries but with severity = "near_miss" and no injured_party required.

**Critical for Prevention**: Near-misses are leading indicators of systemic safety issues. Organizations with strong near-miss reporting programs typically have 10 near-misses reported for every 1 recordable incident.

**Near-Miss Attributes:**
- `description`: What could have happened if luck hadn't intervened (potential injury severity)
- `corrective_actions`: Even though no injury occurred, implement controls to prevent future occurrence
- `reporting`: Actively solicit near-miss reports in toolbox talks and safety briefings
- `trending`: Monthly summary of near-miss reports by category (dropped objects, electrical hazards, etc.)

**Reporting Encouragement:**
- Make near-miss reporting easy (no blame culture)
- Publicly acknowledge and implement near-miss suggestions
- Track and report near-miss statistics in safety meetings
- Use near-misses to guide safety priorities

### Root Cause Analysis Methods

#### 5-Why Analysis

Ask "why" repeatedly (minimum 3 levels, typically 5) to drill down from symptom to root cause:

```
Incident: Worker stepped on unsecured rebar cap

Why 1: Why did worker step on the rebar cap?
Answer: Worker was unfamiliar with the work area layout after formwork was adjusted

Why 2: Why was worker unfamiliar with the area?
Answer: Area was re-inspected and cleaned, but no re-briefing conducted after change

Why 3: Why was no re-briefing conducted?
Answer: Work crew wasn't notified that formwork was adjusted and area hazards changed

Why 4: Why wasn't crew notified?
Answer: GC superintendent adjusted formwork during shift change; communication breakdown

Why 5: Why did communication breakdown occur?
Answer: No formal change notification protocol in place for mid-shift modifications
```

**Root Cause (Why 5)**: Lack of formal change notification protocol for formwork modifications.

#### Fishbone (Ishikawa) Analysis

Categorize contributing factors into six major categories:

```
                               Incident (Rebar Cap Injury)
                                      |
        ┌─────────────┬─────────────┬─┴──────────┬─────────────┬──────────────┐
        │             │             │            │             │              │
     PEOPLE      EQUIPMENT      MATERIALS     METHODS      ENVIRONMENT    MANAGEMENT
        │             │             │            │             │              │
   • Unfamiliar  • No warning   • Caps not    • No re-brief  • Layout       • No protocol
     with layout   devices        secured       after change   changed         for changes
   • Distracted  • Formwork        after work  • No inspection • Lighting     • Poor comms
   • Lack of      damaged          modification  after modification           • No hazard
     PPE check

FINDINGS:
- People: Worker lacked area briefing
- Equipment: Warning devices insufficient
- Materials: Rebar cap security inadequate
- Methods: No re-inspection after modification
- Environment: Changed physical layout not communicated
- Management: No protocol for mid-shift changes
```

**Root Cause Clusters**: Methods + Management (no protocol, no re-inspection, no communication)

### OSHA Recordkeeping Rules

#### OSHA 300 Recordable Criteria

**NOT RECORDABLE (First Aid Only):**
- Band-aids, bandaging, gauze wrapping
- Cleaning wound with soap and water
- Ice pack application
- Non-prescription medication (aspirin, ibuprofen)
- Rest, immobilization without treatment

**RECORDABLE (Medical Treatment):**
- Stitches (sutures)
- Prescription medication
- Fractures (including hairline, stress)
- Hospitalization (even observation)
- Permanent/temporary disfigurement
- Loss of consciousness
- Any medical professional treatment beyond first aid

**LOST TIME RECORDABLE:**
- Incident results in worker unable to perform normal job duties
- Worker assigned modified/light duty work
- Worker sent home (even same day)
- Days away from work counted starting next calendar day

#### OSHA 300 Log Maintenance

Required for all U.S.-based construction projects:

```json
{
  "osha_300_log": {
    "project_name": "Morehead Construction Project",
    "project_year": 2026,
    "total_hours_worked": 0,  // Updated daily
    "recordable_incidents": 0,
    "lost_time_incidents": 0,
    "logs": [
      {
        "case_number": "1",
        "employee_name": "John Smith",
        "job_title": "Ironworker",
        "incident_date": "2026-02-18",
        "incident_description": "Stepped on unsecured rebar cap, foot puncture",
        "outcome": "medical_treatment",
        "days_away": 0,
        "days_restricted": 0,
        "days_transferred": 0,
        "osha_recordable": true,
        "injury_type": "puncture_wound",
        "body_part": "foot",
        "source": "rebar_cap"
      }
    ]
  }
}
```

**Annual OSHA 300A Summary:**
- Posted February 1 - April 30 each year
- Summary of prior calendar year incidents
- Must display at job site
- Certification by company officer required

**Key Metrics for OSHA 300:**
- **Total Recordable Incident Rate (TRIR)**: (Recordable incidents × 200,000) / Total hours worked
- **Days Away, Restricted, or Transferred (DART) Rate**: (DART cases × 200,000) / Total hours worked
- **Lost Workday Case Rate**: (Lost time cases × 200,000) / Total hours worked

### Corrective Action Tracking

Each incident generates corrective actions to prevent recurrence:

**Corrective Action Object:**
```json
{
  "action": "Re-inspect all rebar caps in active pour areas daily",
  "responsible": "GC Superintendent",
  "due_date": "2026-02-19",
  "status": "open | in_progress | complete | verified",
  "notes": "Implemented during morning toolbox talk. All crews briefed.",
  "verification_date": "2026-02-19",
  "verified_by": "Safety Director"
}
```

**Tracking Workflow:**
1. **Open**: Action created; responsible party notified
2. **In Progress**: Party begins implementing the action
3. **Complete**: Action completed; documented in status record
4. **Verified**: Safety director confirms action was actually implemented and effective

**Leading Indicators (Safety Leading Indicators):**
- % of corrective actions completed on schedule
- Avg. time from incident to corrective action completion
- Repeat incidents (same type, same location) indicate ineffective corrective actions

### Safety Metrics for Dashboard

#### Primary Safety Metrics

**Total Recordable Incident Rate (TRIR)**
```
TRIR = (Recordable incidents × 200,000) / Total hours worked

Example: 2 recordable incidents, 100,000 hours worked
TRIR = (2 × 200,000) / 100,000 = 4.0 per 200,000 hours
Industry benchmark (construction): 3.0 - 4.5
```

**Days Away, Restricted, or Transfer (DART) Rate**
```
DART Rate = (DART cases × 200,000) / Total hours worked

Measures: Incidents resulting in lost time, restricted duty, or job transfer
More severe than TRIR (subset of recordables)
```

#### Leading Indicators (Predictive)

- **Safety Observations Completed**: # of daily safety observation rounds (target: 1/day/superintendent)
- **Toolbox Talks Held**: # of daily safety briefings (target: 1/day)
- **Hazard Reports Filed**: # of near-misses, safety concerns reported (target: 10:1 ratio with recordables)
- **Corrective Actions Completed On Time**: % of corrective actions meeting due date
- **Safety Training Completed**: % of workers with required certifications current
- **PPE Compliance**: % of workers observed wearing required PPE

#### Near-Miss Trending

**Target Ratio**: 10 near-misses reported for every 1 recordable incident (10:1 ratio)

```
This week:
- Near-misses filed: 8
- Recordable incidents: 1
- Ratio: 8:1 (below target)

Action: Increase hazard reporting awareness; conduct near-miss training
```

### Integration with Project Daily Systems

#### Storage Location

Incidents stored in `{{folder_mapping.config}}/inspection-log.json` under new `incidents` array:

```json
{
  "inspection_log": [...],
  "incidents": [...]  // New array for incident records
}
```

#### Morning Brief Integration

**Incidents & Safety Section:**
- **Open Incidents**: List INC IDs with status, type, date
- **Pending Corrective Actions**: Show overdue actions (due_date < today)
- **Yesterday's Incidents**: Summary of new incidents reported in past 24 hours
- **Near-Miss Summary**: Count of near-misses filed in past 7 days
- **OSHA Recordables YTD**: Running count with TRIR calculation

Example morning brief snippet:
```
INCIDENTS & SAFETY
[Red] INC-001: Rebar cap puncture wound (2026-02-18) — Corrective actions due 2026-02-19
[Yellow] Pending corrective actions: 2 (1 overdue)
Last 24h: 1 near-miss filed (electrical hazard, near-miss ratio 8:1)
OSHA Recordables YTD: 2 incidents, TRIR = 4.0
```

#### Daily Report Integration

**Incident Tracking Section:**
- Note any incidents that occurred during the report period
- Reference corrective actions underway
- Safety observations conducted during day
- Hazard reports or concerns raised by crews

### Compliance & Legal Considerations

**OSHA Compliance Checklist:**
- ✓ 300 Log maintained and updated timely (by employer)
- ✓ 300A Summary posted Feb 1 - Apr 30 (if 10+ employees)
- ✓ Employee access to logs (current/former employees)
- ✓ Privacy case list maintained (if required)
- ✓ Annual OSHA 301 forms completed (if recordable)
- ✓ Reporting to OSHA within 24 hours of serious incidents
- ✓ No retaliation for incident reporting

**Best Practices:**
- Investigate ALL incidents, not just recordables
- Document investigation thoroughly (photos, witness statements, RCA findings)
- Keep incident records confidential unless subject employee requests
- Maintain corrective action audit trail
- Report OSHA-recordables accurately and timely
- Use incidents to drive continuous safety improvement


---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
