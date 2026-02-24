---
description: Interactive project analytics dashboard
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [weekly|project]
---

Generate an interactive HTML dashboard showing project status from daily report history data.

Read the project-dashboard skill at `${CLAUDE_PLUGIN_ROOT}/skills/project-dashboard/SKILL.md` before proceeding. Also read `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md` for project data retrieval patterns. Read the dashboard-intelligence-analyst agent at `${CLAUDE_PLUGIN_ROOT}/agents/dashboard-intelligence-analyst.md` for narrative health reporting and executive briefing methodology. If available, also read the `web-artifacts-builder` Cowork skill for building rich interactive HTML dashboards with React and Tailwind CSS.

## Step 1: Load Data

Search for project-data files in the user's working directory (check `AI - Project Brain/` first, then root):
- `daily-report-data.json` (report history)
- `project-config.json` (project_basics)
- `schedule.json` (milestones, percent_complete)
- `plans-spatial.json` (quantities, site_layout)
- `procurement-log.json` (deliveries, material status)
- `rfi-log.json` (open RFIs, aging)
- `submittal-log.json` (submittal status)
- `change-order-log.json` (CO status, cost impact)
- `inspection-log.json` (inspection results, permits)
- `meeting-log.json` (action items, meetings)
- `punch-list.json` (punch list completion)
- `delay-log.json` (delay events, critical path impact)
- `labor-tracking.json` (man-hours, productivity)
- `safety-log.json` (incidents, TRIR/DART, toolbox talks)
- `cost-data.json` (budget vs. actual, CPI, EAC)
- `drawing-log.json` (revision status, distribution)
- `quality-data.json` (FPIR, corrective actions)
- `pay-app-log.json` (billing progress, retainage)
- `closeout-data.json` (closeout status, commissioning, warranties)

If `daily-report-data.json` doesn't exist or has no reports:
- Tell the user: "No daily reports have been generated yet. Run /daily-report to create your first report, then come back for the dashboard."

If `project-config.json` doesn't exist:
- Tell the user: "No project is set up yet. Run /set-project first."

## Step 2: Determine Focus

If the user provided an argument ($ARGUMENTS):
- "weekly" → Open the dashboard with the Weekly tab active
- "project" → Open the dashboard with the Project tab active
- No argument → Default to Weekly tab

## Step 3: Generate Dashboard

Build a single self-contained HTML file following the project-dashboard skill spec:

1. Embed all report data and project config as JavaScript objects in the HTML
2. Build the Weekly tab with:
   - Summary cards (reports this week, avg headcount, weather delays, inspections)
   - Weather strip (7-day conditions with threshold alerts)
   - Daily headcount bar chart (stacked by sub)
   - Sub attendance table
   - Active delays and open items
   - Recent inspections table
   - QA summary
   - Cost vs. budget card (weekly spend, variance by division)
   - Safety KPI card (incidents, near-misses, TRIR/DART)
   - Labor productivity card (man-hours by trade, overtime)
   - Delay impact card (calendar days lost this week, cumulative)
   - Quality metrics card (FPIR %, corrective actions open)
   - Drawing status card (revisions issued, distribution pending)
   - RFI/Submittal aging card (items over 7/10 days)
3. Build the Project tab with:
   - Project summary cards
   - Headcount over time line chart
   - Milestone tracker timeline
   - Weather impact charts (cumulative delays + conditions breakdown)
   - Sub mobilization timeline
   - Inspection performance charts
   - Percent complete curve
   - Delivery log table
   - Cumulative cost curve (actual spend vs. budget baseline over time)
   - Cost Performance Index (CPI) trend line
   - Safety trend chart (TRIR/DART over project duration, incidents by month)
   - Labor hours curve (man-hours by trade over time)
   - Quality trend chart (FPIR % weekly, rework cost trend)
   - Delay impact timeline (cumulative calendar days, contract extension progress)
   - Drawing revision timeline (revisions received, ASI processing)
   - Punch list completion chart (% by area and trade — if in closeout)
   - Pay application progress (billing % vs. schedule % — S-curve)
4. Include tab switching, responsive layout, and Chart.js charts
5. Include the project data chat interface (see project-dashboard skill)

## Step 4: Save and Present

Save as `{PROJECT_CODE}_Dashboard.html` in `folder_mapping.ai_output` (e.g., AI - Project Brain/). Fall back to the user's output folder if folder_mapping is not populated.

Present to user: "Here's your project dashboard. The Weekly tab shows this week's activity and the Project tab shows lifetime trends. You can also ask questions about your project data using the chat at the bottom."
