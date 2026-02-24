---
description: Generate construction lookahead schedule
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch
argument-hint: [optional: number of weeks, default 3]
---

## Overview
Generate a construction lookahead schedule from project intelligence. This command reads critical project data including schedule, subs, procurement, RFIs, and submittals to create a forward-looking view of upcoming work.

**Skills Referenced:**
- `${CLAUDE_PLUGIN_ROOT}/skills/look-ahead-planner/SKILL.md` - Lookahead scheduling methodology
- `${CLAUDE_PLUGIN_ROOT}/skills/look-ahead-planner/references/w-principles-4wla-template-spec.md` - **W Principles 4WLA Excel template specification** (MUST READ before generating .xlsx)
- `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md` - Project data extraction and management
- `${CLAUDE_PLUGIN_ROOT}/skills/field-reference/SKILL.md` - Field reference knowledge for trade sequencing (mep-coordination-guide.md), site logistics (site-logistics-guide.md), and activity-specific constraints
- `${CLAUDE_PLUGIN_ROOT}/agents/weekly-planning-coordinator.md` - Last Planner System cycle with constraint analysis
- `${CLAUDE_PLUGIN_ROOT}/agents/deadline-sentinel.md` - Comprehensive deadline monitoring for lookahead period

## Execution Steps

### 1. Load Project Configuration
- Read project data files to retrieve:
  - Schedule data from `schedule.json` (activities, durations, dependencies, critical path)
  - Subcontractor roster from `directory.json` (subcontractors and scopes)
  - Procurement log from `procurement-log.json` (long-lead items, delivery dates)
  - RFI log from `rfi-log.json` (open items, resolution impact)
  - Submittal log from `submittal-log.json` (pending reviews)
  - Project location from `project-config.json` (for weather forecasting)
  - Weather thresholds from `specs-quality.json` (weather_thresholds)
- **Load the W Principles 4WLA template** from `AI - Project Brain/Templates/3WLA TEMPLATE.xlsx`
  - If the template file cannot be read (e.g., OneDrive placeholder not synced), generate from the template spec in `references/w-principles-4wla-template-spec.md`
  - Preserve the company logo, colors, and formatting exactly

### 2. Determine Lookahead Window
- Default: Current week + 3 weeks ahead (4 total weeks displayed) per W Principles 4WLA template
- Week 1 = current work week (Mon–Fri), Weeks 2–4 = next 3 weeks ahead
- Check `$ARGUMENTS` for custom week count (1-12 weeks)
- Calculate date range from today

### 3. Extract Activities in Window
- Filter schedule for activities starting or ongoing within the window
- Include all critical path activities
- Note dependencies extending beyond the window

### 4. Map Each Activity to Resources
For each activity, gather:
- **Subcontractor**: Who is responsible
- **Location**: Grid reference, area, room number
- **Materials**: Required materials and their delivery status
- **Equipment**: Needed equipment and availability
- **Weather Constraints**: Temperature, humidity, precipitation requirements
- **Prerequisite Blockers**: Inspections, permits, approvals

### 5. Check for Blockers
Identify blocking items:
- Pending RFIs that affect the scope
- Pending submittals affecting procurement
- Delayed material deliveries
- Open permit requests
- Scheduled inspections

### 6. Fetch Weather Forecast
- Use WebSearch to fetch weather forecast for project location
- Extract 7-day and 14-day forecasts
- Note any weather-critical activities

### 7. Build Daily Breakdown
- Create day-by-day view for the window
- Show which subcontractors and crews are scheduled
- Highlight milestones and deliverables
- Flag critical dates

### 8. Generate Output (Gantt-Style 4WLA)

**CRITICAL**: Read the template spec (`references/w-principles-4wla-template-spec.md`) before generating.

- **Primary output**: `.xlsx` Gantt-style bar chart matching the **W Principles 4WLA TEMPLATE** format exactly
  - **File**: `{PROJECT_CODE}_4WLA_{YYYY-MM-DD}.xlsx`
  - **Save location priority** (use first available):
    1. `folder_mapping.schedules` folder (e.g., `09 - Schedule/`)
    2. `folder_mapping.ai_output` folder (e.g., `AI - Project Brain/`)
    3. Working directory root as fallback
  - Match the W Principles template layout:
    - Rows 1-3: Company header with logo, project name, dates, PM/Super info
    - Row 10: Title "4WLA" + project code
    - Row 13: Column headers (Description of Work | Dates | Notes)
    - Row 14: Day abbreviations (M T W TH F Sa Su) x 4 weeks, Sa/Su shaded
    - 4 gantt sections with date header rows (rows 15, 20, 28, 33) + activity rows below each
    - Row 40+: Action Items section (Action Items | Project | Responsible | Complete By | Status)
    - Rows 53+: Extended activity rows
    - Column AL (col 38): Notes column, width ~48
  - Activity bars span across day columns showing planned duration
  - Color-code: critical path (red), near-critical (amber), normal (blue), completed (green)
  - Friday columns have thick right border (week separator)
  - Sa/Su columns are shaded (weekend)
  - Include milestone diamonds for key dates
  - Footer section: blockers, weather alerts, key deliveries
- **Secondary output**: Also generate `{PROJECT_CODE}_Lookahead_{date}.html` — interactive HTML version
  - Save to same location as the .xlsx
  - Daily schedule view with weather forecast
  - Subcontractor schedule by crew
  - Material delivery timeline
  - Critical path highlighted, blockers flagged
  - Interactive toggles for detail levels

### 9. Update Project Configuration
- Save lookahead summary to `schedule.json` lookahead_history array
- Include: window dates, critical activities, blockers identified, date generated

### 10. Present to User
Display:
- Summary: "X activities scheduled for [date range], Y blockers identified, Z weather impacts"
- Key deliverables and milestones
- Top blockers and recommended actions
- Link to both .xlsx and .html files
- Suggestion: "Run /submittal-review to clear blocking submittals"
