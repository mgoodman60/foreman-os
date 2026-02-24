---
description: Record meeting minutes and action items
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [OAC/progress/safety/pre-install/coordination] [date]
---

# Meeting Minutes & OAC Reports Command

## Overview
Records meeting minutes, captures action items, tracks carry-forward items from previous meetings, and generates professional .docx meeting reports. Integrates with morning brief (overdue items), weekly reports, and project tracking.

**Output Skills**: See the `docx` Cowork skill for .docx generation best practices.

## Skills Referenced
- `${CLAUDE_PLUGIN_ROOT}/skills/meeting-minutes/SKILL.md` — Meeting types, action item tracking, carry-forward logic
- `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md` — Project configuration and data context

## Execution Flow

### Step 1: Load Project Configuration
```
Load project config from $PROJECT_CONFIG
If not found:
  → Tell user: "Project not configured. Run /set-project first."
  → Exit
Extract: project_name, project_code, folder_mapping, team_contacts, subcontractor_directory
```

### Step 2: Load Meeting Minutes Skill
```
Read: ${CLAUDE_PLUGIN_ROOT}/skills/meeting-minutes/SKILL.md
Load skill metadata, meeting type definitions, and integration points
Confirm skill is available
```

### Step 3: Determine Meeting Type
```
Extract meeting_type from $ARGUMENTS[0]
If not specified:
  → Ask user conversationally:
     "What type of meeting is this?
      - OAC (Owner-Architect-Contractor)
      - Progress (Weekly/Bi-weekly status)
      - Safety (Toolbox talk or weekly safety)
      - Pre-Install (Pre-installation conference)
      - Coordination (Subcontractor/trade coordination)"
  → Wait for selection, store in meeting_type

Validate meeting_type against skill definitions
```

### Step 4: Auto-Assign Meeting Number & Date
```
Load meeting_log from config.meeting_log
Count existing meetings: count = length(meeting_log.meetings)
Auto-assign: meeting_id = "MTG-" + zero_padded(count + 1, 3)
  Example: MTG-001, MTG-002, MTG-003

Extract date from $ARGUMENTS[1] or use today()
  If date invalid or not provided → use today's date
Store: meeting_date = YYYY-MM-DD
Store: meeting_time = ask user conversationally
```

### Step 5: Collect Attendees Conversationally
```
Ask: "Who attended this meeting? (Enter names, separate by comma)"
For each name:
  → Resolve against subcontractor_directory and project team contacts
  → Confirm: "Is this [Full Name] from [Company]? (yes/no)"
  → If match found, add to attendees with company
  → If no match, ask for company and contact info
  → Store: attendee = {name, company, role, phone, email}

Ask: "Anyone else? (or type 'done')"
Continue until user enters 'done'
Store: attendees[] array
```

### Step 6: Collect Discussion Items Conversationally
```
Ask: "What was discussed? (Enter topic, or 'done' to finish)"

For each discussion item:
  → Store: topic (subject of discussion)
  → Ask: "What was discussed on this topic?"
  → Store: discussion_summary (narrative of conversation)
  → Ask: "Any decisions made? (or press enter for none)"
  → Store: decisions_made (list of decisions)
  → Ask: "Any action items from this? (or press enter for none)"
  → If yes:
      For each action item:
        - Ask: "What's the action? (description)"
        - Ask: "Who's assigned? (name or type 'unassigned')"
        - Resolve assignee against contacts
        - Ask: "Due date? (YYYY-MM-DD or 'TBD')"
        - Ask: "Any linked RFI, CO, or submittal? (or press enter)"
        - Store action item (see Step 7)
  → Ask: "Next discussion topic? (or type 'done')"

Continue until 'done'
Store: discussion_items[] array
```

### Step 7: Process Action Items
```
For each new action item from Step 6:
  → Load action_item_log from config
  → Count existing action items: ai_count = length(action_item_log.items)
  → Auto-assign: action_id = "AI-" + zero_padded(ai_count + 1, 4)
  → Store action item:
     {
       id: "AI-0001",
       description: <user input>,
       assignee: <resolved name>,
       assignee_company: <resolved company>,
       due_date: <date or TBD>,
       status: "open",
       linked_rfi: <RFI number if applicable>,
       linked_co: <CO number if applicable>,
       linked_submittal: <submittal ID if applicable>,
       created_meeting: "MTG-001",
       closed_meeting: null,
       notes: <user notes if any>
     }
  → Append to action_item_log.items
```

### Step 8: Carry-Forward Logic
```
If count(meeting_log.meetings) > 0:
  → Load previous_meeting = meeting_log.meetings[-1]
  → Load open_items from action_item_log where:
     - status in ["open", "in_progress"]
     - created_meeting <= previous_meeting.id

  → Present to user:
     "=== CARRY-FORWARD ITEMS FROM PREVIOUS MEETINGS ===
      [Table of open action items with due date, assignee, description]"

  → For each carry-forward item:
     Ask: "Is [action item description] now closed? (yes/no/deferred)"
     If yes:
       - Update: status = "closed", closed_meeting = current meeting_id
       - Ask: "Any closing notes?"
       - Store: notes
     If no:
       - Ask: "Any update? (or press enter)"
       - Store update in notes
     If deferred:
       - Ask: "New due date?"
       - Update due_date

  → Summarize carry-forward count and status changes
Else:
  → No previous meeting, skip carry-forward
```

### Step 9: Generate .docx Meeting Minutes Document
```
Use docx generation pattern (similar to daily-report, weekly-report)

Document structure:
  - Header section:
    * Project name, code, address
    * Meeting type, ID (MTG-001)
    * Date, time, location
    * Prepared by, date prepared

  - Attendees section:
    * Table: Name | Company | Role | Contact
    * All attendees listed

  - Discussion items section:
    * For each discussion_item:
      - Heading: Topic
      - Paragraph: Discussion summary
      - Subheading: Decisions
      - Bullet list: decisions_made
      - Subheading: Action items from this topic
      - Linked action items with IDs

  - Action items table:
    * Columns: ID | Description | Assignee | Company | Due Date | Status
    * Status color coding: Open=Red, In Progress=Yellow, Closed=Green, Deferred=Gray
    * All action items (new + carry-forward)

  - Carry-forward summary (if applicable):
    * Count of items carried from previous meeting
    * Status changes summary

  - General notes section (if any)

Styling:
  - Navy headers (#001a4d), blue accents (#0047ab)
  - Professional W Principles style
  - Tables with zebra striping
  - Status indicator colors
```

### Step 10: Save Outputs
```
Generate filename: meeting_minutes_MTG-001_[date]_[type].docx
Save .docx to: folder_mapping.oac_reports + "/meeting_minutes/"

Update meeting_log:
  - Add new meeting entry with all data
  - Store: id, type, date, time, location, attendees[], discussion_items[], action_items[], previous_meeting_id

Update action_item_log:
  - Add all new and modified action items

Update config:
  - Save meeting_log
  - Save action_item_log
  - Save last_meeting_date = today

Update project-config.json version_history:
  [TIMESTAMP] | meeting-notes | [meeting_type] | [MTG-NNN, X action items]

Output summary to user:
  "✓ Meeting minutes saved: [filename]
   ✓ Meeting ID: MTG-001
   ✓ New action items: [count]
   ✓ Carry-forward items: [count] (updated: [count])
   ✓ Document location: [path]"

Trigger integrations:
  - Check /morning-brief for overdue action items display
  - Check /weekly-report for meeting summary inclusion
If project data changed significantly, regenerate CLAUDE.md
```

## Integration Points
- **Morning Brief**: Surfaces action items with past due date and open status
- **Weekly Report**: Includes summary of all meetings held that week
- **Daily Report**: Can reference action items and upcoming meeting dates
- **Project Config**: Stores meeting log and action item log
- **Subcontractor Directory**: Resolves attendees and assignees

## Notes
- Meeting numbers persist across project lifecycle (never reset)
- Action item IDs persist across project lifecycle
- Carry-forward automatically loads previous meeting's open items
- All dates stored as ISO 8601 (YYYY-MM-DD)
- Contact information resolved from project team and subcontractors
- .docx documents generated with professional formatting and status indicators
