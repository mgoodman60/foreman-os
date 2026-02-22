---
name: look-ahead-planner
description: >
  Generates multi-week lookahead schedules from project intelligence. Trigger phrases include "look ahead", "lookahead", "3 week schedule", "upcoming work", "what's coming up", "plan the next few weeks".
version: 1.0.0
---

# Look-Ahead Planner Skill

## Overview

The Look-Ahead Planner generates 3-week (configurable) lookahead schedules by synthesizing project intelligence into interactive, actionable documents. It maps schedule activities to subcontractors, locations (grid lines, building areas), material requirements, equipment needs, and weather constraints. 

The skill reads historical schedule data, integrates pending items (RFIs, submittals), and cross-references material procurement status. It fetches weather forecasts for the project location and renders the result as an interactive HTML or PDF document—a forward-looking view of exactly what work, by whom, where, using what materials and equipment, under what conditions.

### Key Outputs
- **W Principles 4WLA Excel Spreadsheet** (.xlsx) — Gantt-style bar chart matching the company template exactly. See `references/w-principles-4wla-template-spec.md` for the full template specification.
- **Interactive HTML Lookahead** with color-coded activities, milestone markers, and weather alerts
- **Structured daily breakdown** showing crew requirements, material deliveries, and blockers
- **Searchable, self-contained document** for field distribution
- **Archive-friendly format** stored in project config's lookahead_history

### Template Loading
The skill uses the W Principles 4WLA template (`AI - Project Brain/Templates/3WLA TEMPLATE.xlsx`). If this file cannot be read (common when files are stored in OneDrive and not yet synced locally), the skill should generate the .xlsx from the template specification at `references/w-principles-4wla-template-spec.md`.

---

## Data Sources

The skill reads from and cross-references the following project data structures:

### Schedule Data
- **milestones**: Key project dates and gates
- **critical_path**: Activities on the critical path (red-coded in output)
- **near_critical**: Activities with limited float (amber-coded)
- **weather_sensitive_activities**: Activities blocked by rain, extreme temps, wind
- **long_lead_items**: Activities dependent on prior procurements

### Subcontractor & Crew Data
- **subcontractors**: List of all subs with trades, contact info, crew capacity
- **subcontractor_assignments**: Which sub is responsible for which scope/activity

### Procurement & RFI Data
- **procurement_log**: Material delivery schedules, outstanding orders
- **rfi_log**: Pending RFIs and their status (blocks work if not resolved by activity date)
- **submittal_log**: Pending submittals that may delay activities
- **material_requirements_by_activity**: Maps activity type to material needs (e.g., concrete pour → ready-mix delivery)

### Site & Environmental Data
- **site_layout**: Building areas, zones, access points
- **grid_lines**: Coordinate reference system (northing, easting, grid naming)
- **weather_thresholds**: Project constraints (e.g., no concrete pour below 40°F, no exterior painting in rain)
- **project_location**: GPS coordinates and nearest weather station for forecast

---

## Workflow

### 1. Load Project Configuration
- Read schedule from project-data (milestones, critical path, activity durations)
- Load subcontractor roster and assignments
- Load procurement log, RFI log, submittal log status
- Read site layout, grid lines, weather constraints

### 2. Define Lookahead Window
- Default: Current week + 3 weeks ahead (4 total weeks) per W Principles 3WLA template
- Week 1 = current work week (Mon–Fri), Weeks 2–4 = next 3 weeks
- Configurable: User can request different week counts
- Calculate calendar weeks with proper Monday–Friday boundaries (work days only)

### 3. Extract Activities in Window
- Query schedule for all activities starting or in-progress during lookahead window
- Include milestones and key deliverables
- Exclude completed activities (date in past)
- Sort chronologically by planned start date

### 4. Resolve Activity Details
For each activity in the window:
- **Subcontractor**: Match activity scope to assigned sub; determine crew headcount based on activity type and duration
- **Location**: Resolve to specific building area(s) and grid lines from site layout; note access routes if applicable
- **Materials**: Look up activity type in material_requirements_by_activity table; cross-reference procurement_log for delivery dates
- **Material Certification Readiness**: When resolving materials for each activity:
  1. For each material in the activity's material requirements, find the matching entry in `procurement-log.json`
  2. Check three conditions:
     - **Delivery status**: Is the material delivered or scheduled to arrive before the activity start date?
     - **Spec verification**: Has the material been verified against specs (`verification_status` = "approved" or "conditional")?
     - **Certifications**: Are all required certs received and verified (`cert_status` = "verified")?
  3. Color coding in the lookahead:
     - Material delivered + verified + certs complete → GREEN (ready to install)
     - Material delivered but certs missing → AMBER with note: "Material on site but certs pending — cannot install until verified"
     - Material not yet delivered → RED if delivery date is after activity start
     - Material delivered but rejected → RED with note: "Material rejected — replacement needed"
  4. Add a "Material Readiness" column or section to the lookahead output that shows cert status alongside delivery status
- **Equipment**: Determine equipment needs (cranes, scaffolding, lifts, etc.) and reservation status
- **Weather Sensitivity**: Check weather_sensitive_activities list; flag if activity is weather-dependent

### 5. Check for Blockers
- Pending RFIs: For each activity, check if there are open RFIs that block it; escalate if RFI due date is before activity start
- Pending Submittals: Check submittal_log for items required before activity can proceed
- Material Delays: Compare material delivery dates (from procurement_log) to activity start dates; flag shortfalls

### 6. Fetch Weather Forecast
- Use project location GPS coordinates
- Query external weather service (e.g., OpenWeather, NOAA) for 21-day forecast
- Extract daily high/low temps, precipitation probability, wind speed
- Flag days where weather violates activity thresholds

### 7. Build Daily Breakdown
- For each day in lookahead window:
  - List all scheduled activities (split multi-week activities into daily chunks)
  - Show assigned subcontractor and crew headcount
  - List material deliveries scheduled that day
  - Show weather forecast and any alerts
  - Note blockers or delays
  - Mark milestone completions

### 8. Render Interactive HTML
- Apply color coding: Red (critical path), Amber (near-critical), Green (on-track), Gray (weather-blocked)
- Add milestone markers as colored flags
- Highlight material deliveries with bold callouts
- Include weather forecast strip at top of each week
- Show blocker alerts as warning banners
- Make responsive for mobile field use
- Use embedded data and Chart.js (via CDN) for any visualizations
- Ensure single self-contained HTML file for easy distribution

### 9. Save to Lookahead History
- Store rendered HTML and structured daily breakdown in project config's lookahead_history
- Include metadata: date generated, lookahead window, summary statistics
- Maintain rolling history for trend analysis and accountability

---

## Output Format

### Primary Output: Excel 4WLA
**File Naming**: `{PROJECT_CODE}_4WLA_{YYYY-MM-DD}.xlsx`
**Example**: `MOSC_4WLA_2026-02-20.xlsx`
**Template Spec**: `references/w-principles-4wla-template-spec.md`

### Secondary Output: Interactive HTML
**File Naming**: `{PROJECT_CODE}_Lookahead_{YYYY-MM-DD}.html`
**Example**: `MOSC_Lookahead_2026-02-20.html`

### File Save Location (priority order)
1. `folder_mapping.schedules` (e.g., `09 - Schedule/`) — keeps it with baseline schedules
2. `folder_mapping.ai_output` (e.g., `AI - Project Brain/`) — fallback
3. Working directory root — last resort

This priority order ensures files are saved directly to the local project folder, avoiding dependency on cloud sync services like OneDrive.

**Contents**:
- Self-contained HTML with embedded CSS, JavaScript, and data
- Interactive tables and collapsible sections
- Responsive design for desktop and mobile
- No external file dependencies (except CDN for Chart.js)
- Print-friendly styling

---

## Project Intelligence Integration

When project intelligence is loaded, auto-populate lookahead activities with schedule data, sub assignments, material status, and constraint information from project data files.

### Activity Extraction
Pull activities scheduled within the lookahead window:
- Read `schedule.json` → filter activities with start date within the lookahead window (next 2-6 weeks from today)
- Include `critical_path[]` activities (red-coded) and near-critical activities (amber-coded)
- Auto-populate activity name, baseline duration, planned start/finish, and float available
- Example: 4-week window from 03/03 → pull "PEMB erection", "CFS framing start", "MEP rough-in prep"

### Predecessor Tracking
Flag activities with incomplete predecessors:
- Read `schedule.json` → for each activity in the window, pull predecessor relationships and their completion status
- Flag if any predecessor is incomplete or behind schedule → mark activity as "at risk" in the lookahead
- Auto-populate a "Prerequisites" column showing predecessor status (complete/in-progress/not-started)
- Example: "MEP rough-in" requires "CFS framing complete" as predecessor → framing 75% complete → flag as "prerequisite in progress"

### Sub Mobilization
Identify subs that need notification for upcoming work:
- Read `directory.json` → `subcontractors[]` → for each activity in the window, identify the assigned sub and their current mobilization status
- Flag subs not yet mobilized that have activities starting within 2 weeks → add "Mobilization Required" alert
- Auto-populate crew headcount expectations from sub contract scope
- Example: Alexander Construction (PEMB) not yet on site, erection starts 03/23 → flag: "Alexander mobilization needed by 03/16"

### Material Delivery Check
Cross-check material availability against planned activities:
- Read `procurement-log.json` → for each activity, match required materials → compare `expected_delivery` date against activity start date
- Flag activities where material delivery is scheduled after activity start → RED alert in lookahead
- Check `cert_status` → flag materials delivered but with pending certifications as AMBER
- Example: Door hardware needed 04/01, procurement-log shows Schiller delivery expected 04/15 → RED: "Material delayed 14 days"

### Inspection Prerequisites
Flag activities requiring inspection sign-off:
- Read `specs-quality.json` → `hold_points[]` → for each activity in the window, check if a hold point inspection is required before the next phase
- Cross-reference `inspection-log.json` → verify inspection status (scheduled/pass/fail)
- Add "Hold Point" markers to the lookahead for activities that cannot proceed without inspection
- Example: PEMB erection requires HP-007 (anchor bolt survey) → inspection-log shows scheduled 03/16 → add hold point marker

### Weather Restrictions
Flag weather-sensitive activities in the lookahead window:
- Read `specs-quality.json` → `weather_thresholds[]` → identify activities with temperature, wind, or precipitation restrictions
- Flag all weather-sensitive activities with their specific threshold requirements
- When weather forecast is available, cross-reference and color-code: GREEN (clear), AMBER (marginal), RED (restricted)
- Example: Concrete pour Week 2 → threshold min 40F → forecast shows 38F on planned day → AMBER: "Marginal weather, monitor forecast"

---

## Cross-References

This skill reads project intelligence from the **project-data** skill:

- Reference: `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md`
- Depends on: schedule milestones, critical path, activity definitions, subcontractor roster, procurement log, RFI log, submittal log, site layout, grid lines

---

## Configuration & Customization

### Lookahead Window
- **Default**: 3 weeks (21 days)
- **User-configurable**: Pass `lookahead_weeks: 2|3|4|6` as parameter
- **Rolling start**: Always "today" (can be overridden with `start_date` parameter)

### Color Palette
- **Navy (Critical Path)**: `#1B2A4A`
- **Blue Accent (Near-Critical)**: `#2E5EAA`
- **Light Blue (Background)**: `#EDF2F9`
- **Green (On-Track)**: `#28A745`
- **Amber (At-Risk)**: `#FFC107`
- **Red (Blocked)**: `#DC3545`
- **Gray (Weather-Blocked)**: `#6C757D`

### Material Delivery Highlighting
- Bold text with background color highlight
- Specific color for pending vs. confirmed deliveries

### Weather Thresholds
- Project-specific constraints read from config (e.g., concrete: min 40°F, no rain)
- Activities flagged if forecast violates constraints

---

## Example Use Cases

1. **Daily Standup**: "What's coming up this week?" → Generates 1-week lookahead with daily crew assignments and material needs
2. **Preconstruction Planning**: "Look ahead 6 weeks" → Full lookahead with critical path and long-lead item tracking
3. **Material Coordinator**: "Show me what materials we need next 3 weeks" → Highlights all material deliveries and cross-references procurement log
4. **Subcontractor Coordination**: "Plan the next few weeks" → Assigns subs to activities, shows crew headcount, notes any blockers or RFI delays
5. **Project Manager**: "Generate lookahead schedule" → Creates archive-ready HTML for distribution to team, owner, lender

---

## See Also

- **W Principles 4WLA Template Spec**: `/skills/look-ahead-planner/references/w-principles-4wla-template-spec.md` — Excel template layout and formatting rules
- **Activity Mapping Reference**: `/skills/look-ahead-planner/references/activity-mapping.md`
- **Lookahead HTML Template Reference**: `/skills/look-ahead-planner/references/lookahead-template.md`
- **Project Data Skill**: `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md`

