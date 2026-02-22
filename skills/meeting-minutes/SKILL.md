---
name: meeting-minutes
description: >
  Record and generate professional meeting minutes for OAC meetings, progress meetings, safety meetings, and pre-installation conferences. Tracks action items across meetings with automatic carry-forward. Generates .docx minutes documents with status indicators. Integrates with morning brief (overdue action items), weekly report (meeting summary), and daily report (action item references). Surfaces critical action items in handoff reports. Triggers: "meeting notes", "meeting minutes", "OAC meeting", "OAC notes", "progress meeting", "safety meeting", "toolbox talk", "pre-install meeting", "pre-installation conference", "action items", "carry forward", "action item status".
version: 1.0.0
---

# Meeting Minutes Skill

## Overview
Provides structured meeting recording, action item tracking, and professional .docx generation for construction project meetings. Supports multiple meeting types with specialized content for pre-installation conferences. Automatically carries forward open action items between meetings and surfaces critical items in daily operations.

## Meeting Types

### OAC Meeting (Owner-Architect-Contractor)
- Typically weekly or bi-weekly
- Attendees: Owner, Architect, General Contractor, Key Subcontractors
- Focus: Overall project status, design decisions, issues, schedule
- Content: RFI tracking, change order discussions, coordination
- Action items: Design clarifications, schedule updates, specification reviews

### Progress Meeting
- Weekly or bi-weekly project status
- Attendees: General Contractor, Subcontractor Foremen, Key Consultants
- Focus: Construction progress, safety, quality, schedule adherence
- Content: Daily/weekly progress metrics, upcoming work, resource needs
- Action items: Schedule adjustments, material coordination, quality issues

### Safety Meeting
- Toolbox talks (daily or weekly 15-min safety briefs)
- Weekly or monthly formal safety meetings
- Attendees: Job site personnel, safety manager, subcontractor leads
- Focus: Hazard identification, OSHA compliance, near-miss incidents, safety training
- Content: Hazards present, PPE requirements, incident review, corrective actions
- Action items: Hazard corrections, training assignments, equipment upgrades

### Pre-Installation Conference (Pre-Install)
- Held before major trades begin (concrete, MEP, structural, etc.)
- Attendees: Trade contractor, General Contractor, Architect, Inspector
- Focus: Spec compliance, material quality, installation procedures, QC checkpoints
- Content: Spec section review, submittal status, delivery schedules, QC requirements, hold points
- Action items: Material ordering, submittal finalization, equipment staging, coordination tasks
- Special fields: spec_sections_reviewed[], submittal_status[], material_delivery_dates[], qc_requirements[], weather_restrictions, hold_points[]

### Coordination Meeting
- Trades coordination, safety coordination, logistics
- Attendees: Multiple subcontractors, General Contractor, Scheduler
- Focus: Trade sequencing, spatial coordination, utility routing, equipment staging
- Content: Weekly work plans, interface coordination, access requirements, phasing
- Action items: Coordination requirements, schedule adjustments, equipment staging

## Core Data Structures

### Meeting Object
```
{
  id: "MTG-001",                           # Auto-assigned, sequential, never reset
  type: "OAC" | "progress" | "safety" | "pre-install" | "coordination",
  date: "2025-02-17",                      # ISO 8601 format
  time: "09:00 AM",                        # 12-hour format with AM/PM
  location: "Project Trailer" | "Site Office",
  attendees: [
    {
      name: "John Smith",
      company: "ABC Construction",
      role: "Project Manager",
      phone: "555-0101",
      email: "john@abcconstruction.com"
    },
    ...
  ],
  discussion_items: [
    {
      topic: "Schedule Updates",
      discussion_summary: "Team reviewed current critical path...",
      decisions_made: ["Adjust concrete pour by 3 days", "Expedite rebar delivery"],
      linked_action_items: ["AI-0001", "AI-0002"]
    },
    ...
  ],
  action_items: ["AI-0001", "AI-0002", ...],        # References to action item IDs
  carry_forward_items: ["AI-0045", "AI-0046", ...], # From previous meetings
  previous_meeting_id: "MTG-015" | null,
  prepared_by: "Jane Doe",
  prepared_date: "2025-02-17",
  general_notes: "Weather delay expected next week"
}
```

### Action Item Object
```
{
  id: "AI-0001",                           # Auto-assigned, sequential, never reset
  description: "Review final mechanical submittal and approve",
  assignee: "Tom Jones",
  assignee_company: "XYZ MEP",
  due_date: "2025-02-24",
  status: "open" | "in_progress" | "closed" | "deferred",
  linked_rfi: "RFI-018" | null,
  linked_co: "CO-005" | null,
  linked_submittal: "SUB-M-042" | null,
  created_meeting: "MTG-001",
  closed_meeting: null,
  notes: "Client awaiting architect review",
  created_date: "2025-02-17"
}
```

### Meeting Log (Project-Level)
```
{
  project_id: "PRJ-2024-001",
  meetings: [
    { Meeting Object },
    { Meeting Object },
    ...
  ],
  last_meeting_date: "2025-02-17"
}
```

### Action Item Log (Project-Level)
```
{
  project_id: "PRJ-2024-001",
  items: [
    { Action Item Object },
    { Action Item Object },
    ...
  ],
  open_count: 23,
  overdue_count: 3,
  closed_count: 145
}
```

## Carry-Forward Logic

### Automatic Carry-Forward
When creating a new meeting:
1. Load all action items with status in ["open", "in_progress"]
2. Filter by created_meeting <= previous_meeting_id
3. Present to user with context: due date, assignee, description
4. For each item, ask: "Still open? (yes/no/deferred/completed)"
5. If completed: update status = "closed", closed_meeting = current meeting_id
6. If deferred: capture new due date and notes
7. If still open: capture status update in notes
8. Store updated items in action_item_log
9. Link carry-forward items to current meeting via carry_forward_items[]

### Overdue Item Highlighting
- Any action item with due_date < today AND status in ["open", "in_progress"]
- Flagged with visual indicator (red, bold)
- Surfaced in morning brief automatically
- Requires status update or new due date during meeting

## .docx Generation

### Document Header
- Project name and code (top-left)
- Meeting type and ID centered, prominent
- Date, time, location (top-right aligned)
- Prepared by and date prepared (footer)

### Attendees Section
- Professional table: Name | Company | Role | Contact
- All attendees listed in attendance order

### Discussion Items Section
- For each discussion_item:
  - Large bold topic heading (navy color)
  - Discussion summary paragraph
  - "Decisions" subheading (blue)
  - Bullet list of decisions_made
  - Action items from this topic linked by ID

### Action Items Table
- Columns: ID | Description | Assignee | Due Date | Status
- Rows sorted by due date (soonest first)
- Status color coding:
  - Open: Red background, white text
  - In Progress: Yellow background, black text
  - Closed: Green background, white text
  - Deferred: Gray background, white text
- Bold action items overdue (due_date < today)
- Carry-forward items marked with "CF" badge

### Carry-Forward Summary (if applicable)
- Heading: "Items Carried From Previous Meeting"
- Count of carried items, count closed, count still open
- Summary line: "3 of 5 carry-forward items closed this meeting"

### Pre-Installation Conference Special Content
If meeting type == "pre-install":
  - Spec Sections Reviewed: bulleted list
  - Submittal Status Table: Submittal ID | Item | Status | Due Date
  - Material Delivery Schedule: Item | Supplier | Expected Date
  - QC Requirements: bullet list of quality checkpoints
  - Weather Restrictions: paragraph on weather-dependent work
  - Hold Points: numbered list of inspection hold points

### General Notes Section
- Any additional meeting notes
- Attendee absences or late arrivals
- Next meeting schedule

### Styling
- Font: Calibri 11pt (body), 14pt bold (section headings)
- Header color: Navy (#001a4d)
- Accent color: Blue (#0047ab)
- Zebra striping on tables (alternating light gray rows)
- Page breaks between major sections
- Footer with page numbers and "Confidential - Project Document"

## Integration Points

### Morning Brief Integration
```
/morning-brief surfaces:
  - Overdue action items (due_date < today AND status in [open, in_progress])
  - High-priority open items from most recent OAC meeting
  - Any deferred items with new due dates
  - Display format: "2 overdue action items require status update"
```

### Weekly Report Integration
```
/weekly-report includes:
  - Count of meetings held that week
  - Summary of meeting types
  - New action items created
  - Action items closed
  - Overdue count at week end
  - Critical decisions made (from OAC meetings)
  - Format: Executive summary section, detailed table
```

### Daily Report Integration
```
/daily-report can reference:
  - Due today action items
  - Upcoming critical milestones
  - Links to related meeting minutes
  - Format: "Action items due today" section
```

### Project Handoff Integration
```
Transition reports include:
  - All open action items (sorted by due date)
  - Deferred items with rationale
  - Critical carry-forward items for next phase
  - Meeting schedule cadence established
```

## Storage Locations

### Document Output
```
folder_mapping.oac_reports / "meeting_minutes" / "meeting_minutes_MTG-001_2025-02-17_OAC.docx"
```

### Structured Data (Project Config)
```
config.meeting_log           → All meetings, indexed by meeting_id
config.action_item_log       → All action items, indexed by action_id
config.last_meeting_date     → Date of most recent meeting
```

## Workflow Summary

1. **Meeting recorded** via /meeting-notes command
2. **Carry-forward items** automatically surface from previous meeting
3. **Action items** created with ID, assignee, due date
4. **.docx minutes** generated with professional formatting
5. **Morning brief** surfaces overdue items daily
6. **Weekly report** summarizes meeting activity and action items
7. **Daily report** calls out items due today
8. **Status updates** during next meeting (carry-forward logic)
9. **Items closed** when completed, tracked in closed_meeting field

## Key Fields Explained

- **meeting_id (MTG-001)**: Sequential, auto-assigned, never reset. Provides unique identifier for all meetings across project lifecycle.
- **action_id (AI-0001)**: Sequential, auto-assigned, never reset. Provides unique identifier for all action items. Used for cross-referencing in RFIs, COs, etc.
- **status**: Tracks action item lifecycle. "open" = assigned but not started, "in_progress" = actively being worked, "closed" = completed, "deferred" = pushed to future date.
- **created_meeting / closed_meeting**: Tracks which meeting created/closed the item. Enables historical reporting.
- **carry_forward_items[]**: Explicit list of items carried from previous meeting. Differentiates carry-forward from newly created items.
- **linked_rfi / linked_co / linked_submittal**: Cross-references to related project documents. Enables quick navigation from meeting minutes to RFI/CO/submittal tracking.

## Project Intelligence Auto-Population

When project intelligence is loaded, auto-populate meeting agenda sections with current project data to save time and ensure accuracy.

### Schedule Update Section
Before or during progress/OAC meetings:
- Read `schedule.json` → `current_phase`, `percent_complete`, `milestones[]`
- Auto-populate schedule status: current phase, overall % complete, upcoming milestones (next 30 days), any milestones at risk
- Read `schedule.json` → `critical_path[]` → list critical path activities and their status
- Example: "Schedule Status: Foundation phase, 22% complete. Upcoming: Steel delivery 3/1, PEMB erection start 3/8."

### RFI/Submittal Status Tables
For OAC and progress meetings:
- Read `rfi-log.json` → count RFIs by status (open, overdue >14 days, resolved this week)
- Read `submittal-log.json` → count submittals by status (pending review, overdue >10 days, approved this week)
- Auto-populate status tables with counts and highlight overdue items
- Example: "RFIs: 3 open (1 overdue >14 days), 2 resolved this week. Submittals: 5 under review (1 overdue), 3 approved."

### Change Order Status
For OAC meetings:
- Read `change-order-log.json` → group COs by status (draft, submitted, under_review, approved)
- Auto-populate CO section with pending CO count, total pending cost exposure, recently approved COs
- Example: "Change Orders: 2 pending review ($23,500 exposure), 1 approved this week (CO-005, $17,800)."

### Action Item Carry-Forward
For all meeting types:
- Read `meeting-log.json` → pull all action items where `status` != "closed" from previous meetings
- Auto-populate carry-forward section with item ID, description, assignee, due date, and days overdue
- Calculate aging: items open >14 days highlighted, items open >30 days flagged critical
- Example: "5 carry-forward items (2 overdue): AI-0045 — Review MEP coordination (Tom Jones, 8 days overdue)"

### Weather Summary
For progress meetings:
- Read `daily-report-data.json` → pull weather data from all reports in the meeting period
- Summarize: average temp range, precipitation days, any weather delays
- Example: "Weather this week: Highs 42-55°F, lows 28-35°F. 1 rain day (Tuesday). No weather delays."

### Safety Summary
For all meeting types (safety moment section):
- Read `safety-log.json` → pull incident count, near-miss count for the period
- Calculate TRIR from `osha_300_log` if available
- Read `safety-log.json` → `toolbox_talks[]` → count talks held this period
- Example: "Safety: 0 recordable incidents, 3 near-misses reported, 5 toolbox talks held. TRIR: 0.0 YTD."

## Trigger Phrases
The skill activates on phrases like:
- "Take meeting minutes"
- "Record meeting notes"
- "OAC meeting notes"
- "What are our open action items?"
- "Follow up on this action item"
- "Carry forward items from last meeting"
- "Generate meeting report"
- "Pre-install conference"
- "Safety toolbox talk"
