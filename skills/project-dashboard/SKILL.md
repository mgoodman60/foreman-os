---
name: project-dashboard
description: >
  Generate interactive HTML project dashboards from daily report history and project intelligence
  data. Provides Weekly (operational pulse) and Project (lifetime trends) tabs with charts, tables,
  and an embedded project data chat interface. Integrates data from daily reports, schedule, directory,
  inspections, procurement, RFIs, submittals, change orders, pay applications, labor tracking, and
  quality management. Triggers: "dashboard", "project status", "show project status", "how's the
  project going", "project overview", "project metrics", "project trends", "see the dashboard",
  "generate dashboard", "weekly summary chart", "headcount chart", "milestone tracker".
version: 1.0.0
---

# Project Dashboard

## Overview

Generate an interactive HTML dashboard from daily report history data. Two tabs: **Weekly** (recent activity and operational pulse) and **Project** (lifetime trends and status tracking).

## Data Source

Read from multiple files in the user's working directory:
- `daily-report-data.json` — structured report history
- `project-config.json` — project basics, folder mapping, documents loaded
- `schedule.json` — milestone targets and schedule data
- `directory.json` — subcontractor directory
- `plans-spatial.json` — quantities
- `inspection-log.json` — inspection records
- `procurement-log.json` — procurement/delivery tracking
- `rfi-log.json` — open/closed RFI counts, aging, response times
- `submittal-log.json` — submittal status breakdown, lead time tracking, critical-path submittals
- `change-order-log.json` — CO count, approved/pending/rejected, cost impact totals
- `pay-app-log.json` — billing progress, retainage tracking, SOV percent complete
- `labor-tracking.json` — crew hours, headcount trends, productivity ratios
- `quality-data.json` — quality inspection pass/fail rates, open deficiencies

If no report history exists, tell the user: "No daily reports have been generated yet. Run /daily-report to create your first report, then come back for the dashboard."

## Dashboard Command

The dashboard is generated via a `/dashboard` command or when the user asks for project status. Output is a single self-contained HTML file.

## Technology Stack

- **Single HTML file** — no external dependencies, opens in any browser
- **Chart.js** via CDN — for all charts (line, bar, doughnut, timeline)
- **Vanilla CSS** — clean, professional styling with the report color palette
- **Vanilla JS** — tab switching, data rendering, responsive layout

## Advanced Dashboard Enhancement

For richer dashboard components beyond vanilla HTML/CSS/JS, use the `web-artifacts-builder` Cowork skill. This skill provides advanced React, Tailwind CSS, and shadcn/ui patterns for interactive widgets, responsive layouts, and professional data visualization. Integrate with this dashboard by generating enhanced components that layer atop or replace the vanilla implementation.

## Color Palette

Match the daily report visual identity:

| Element | Color |
|---|---|
| Primary (headers, active tab) | #1B2A4A (Navy) |
| Accent (charts, highlights) | #2E5EAA (Blue) |
| Background (cards) | #F8F9FB (Light gray) |
| Section backgrounds | #EDF2F9 (Light blue) |
| Warning/flag | #E8A838 (Amber) |
| Success/positive | #2D8F4E (Green) |
| Danger/negative | #C0392B (Red) |
| Text primary | #1B2A4A |
| Text secondary | #666666 |
| Borders | #CCCCCC |

## Tab 1: Weekly

The operational pulse. Shows the last 7 days (or however many reports exist if fewer than 7).

### Layout

Top row — Summary cards (4 across):

| Card | Content |
|---|---|
| **Reports This Week** | Count of reports generated / expected workdays |
| **Avg. Headcount** | Average total headcount across the week |
| **Weather Delays** | Total hours lost to weather this week |
| **Inspections** | Pass / Fail / Pending count |

### Weather Row

Full-width weather strip showing all 7 days side by side:

| Day | Weather |
|---|---|
| Each day | Date, high/low temp, conditions icon (☀️ 🌤️ ☁️ 🌧️ ❄️ 💨), impact level (none/minor/major), delay hours if any |

Use color coding: green background for no impact, amber for minor, red for major.

If any weather thresholds were triggered, show them below the strip:
"⚠️ Cold weather concrete protocol triggered on Mon, Wed (below 40°F)"

### Crew Section

**Daily headcount bar chart** — X-axis: days of the week. Y-axis: total headcount. Each bar stacked or grouped by sub.

**Sub attendance table** — Rows: each sub. Columns: each day of the week. Cells: headcount (or "—" if absent). Highlight cells where a sub was expected but missing (based on schedule dates).

### Active Delays & Open Items

Two-column layout:

**Active Delays** (left):
- List of current delays from the most recent report
- Each showing: description, cause category, duration so far, critical path impact

**Open Items** (right):
- List of unresolved items from the most recent report
- Each showing: item, date opened, expected resolution

### Recent Inspections

Table of all inspections from the past week:
- Date, type, inspector, area, result (with color: green=pass, red=fail, amber=conditional)

### QA Summary (if data exists)

Small card showing: "Report quality this week: X flags raised, Y resolved, Z skipped"

## Tab 2: Project

The 30,000-foot view. Shows data across the entire project lifetime.

### Layout

Top row — Project summary cards (4 across):

| Card | Content |
|---|---|
| **Project** | Project name + code |
| **Reports Generated** | Total count, date range (first report → latest) |
| **Days Since Start** | Calendar days from first report |
| **Current Phase** | From latest report's schedule section |

### Headcount Over Time

**Line chart** — X-axis: report dates. Y-axis: total headcount.
- Main line: total headcount per day
- Optional toggle: show individual sub lines
- Reference line: moving 5-day average (smooths out daily variation)

### Milestone Tracker

**Horizontal timeline / Gantt-style view:**
- Each milestone as a row
- Planned date shown as a marker
- Actual date shown as a marker (if complete)
- Current date shown as a vertical line
- Color coding: green (complete), blue (on track), amber (approaching within 7 days), red (overdue)

If milestone dates have been revised (from version_history), show original vs. current as drift:
"Substantial Completion: Originally 06/15, now 07/15 (+30 days)"

### Weather Impact Summary

**Two charts side by side:**

Left — **Cumulative weather delay days** (line chart):
- Running total of weather delay hours converted to days
- X-axis: project timeline
- Shows acceleration in delay accumulation

Right — **Weather conditions breakdown** (doughnut chart):
- Percentage of days by impact level: No Impact, Minor Impact, Major Impact
- With total days count in center

### Sub Mobilization Timeline

**Horizontal bar/timeline chart:**
- Each sub as a row
- Bar spans from first appearance to last appearance (or "present" if still active)
- Color indicates current status: active (blue), demobilized (gray)
- Shows the ebb and flow of trades on the project

### Inspection Performance

**Two visualizations:**

Left — **Pass/Fail/Conditional doughnut chart:**
- Total inspections by result
- Counts in center

Right — **Inspection timeline:**
- Dots on a timeline, colored by result
- Clusters of red dots = problem periods worth noting

### Percent Complete Curve

**Line chart** (if data exists):
- X-axis: project timeline
- Y-axis: 0-100%
- Actual percent complete from reports
- Planned S-curve (if schedule data supports it)
- Visual gap between planned and actual = schedule position

### Delivery Log

**Table** of all material deliveries across all reports:
- Date, material, supplier, quantity, condition
- Sortable by date (default) or material
- Highlight any deliveries with condition issues

## HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Project Name} — Dashboard</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
  <style>
    /* All styles inline — single file, no dependencies */
  </style>
</head>
<body>
  <header>
    <h1>{Project Name}</h1>
    <p>{Project Code} — Dashboard generated {date}</p>
  </header>

  <nav class="tabs">
    <button class="tab active" data-tab="weekly">Weekly</button>
    <button class="tab" data-tab="project">Project</button>
  </nav>

  <main>
    <section id="weekly" class="tab-content active">
      <!-- Weekly tab content -->
    </section>
    <section id="project" class="tab-content">
      <!-- Project tab content -->
    </section>
  </main>

  <script>
    // Embedded report data as JSON
    const reportData = {/* injected from daily-report-data.json */};
    const projectConfig = {/* injected from project-config.json, schedule.json, directory.json, etc. */};

    // Tab switching
    // Chart rendering
    // Table population
  </script>
</body>
</html>
```

## Data Embedding

The report data and project intelligence are embedded directly in the HTML as JavaScript objects. This makes the dashboard fully self-contained — no server, no API calls, no external files needed. The user can open it, email it, or present it.

When embedding:
```javascript
const reportData = {/* injected from daily-report-data.json */};
const projectConfig = {/* injected from project-config.json, schedule.json, directory.json, etc. */};
```

## Responsive Behavior

- Cards wrap from 4-across to 2-across on tablets, 1-across on phones
- Charts resize to container width
- Tables become horizontally scrollable on small screens
- Tab bar remains fixed at top on scroll

## Output

Save as `{PROJECT_CODE}_Dashboard.html` in the user's output folder.

Example: `MOSC_Dashboard.html`

Present to user: "Here's your project dashboard. Open it in any browser — the Weekly tab shows this week's activity, and the Project tab shows lifetime trends."

## Project Data Chat

The dashboard includes a persistent chat interface at the bottom of the page, available on both tabs. This lets the user ask natural-language questions about their project data and daily report history without leaving the dashboard.

### Chat Interface Design

Fixed-position chat bar at the bottom of the viewport:
- Collapsed by default: thin bar with "Ask about your project data..." placeholder and an expand button
- Expanded: chat panel slides up (40% of viewport height), pushes dashboard content up
- Input field + send button at bottom of panel
- Chat history scrolls within the panel
- Close/minimize button to collapse back

### How It Works

The chat is powered entirely by client-side JavaScript — no API calls, no server, no external services. It works by querying the embedded report data and project config using predefined query patterns.

When the user types a question, the chat engine:
1. Parses the question for keywords and intent
2. Matches against query patterns (see below)
3. Searches the embedded data
4. Formats and displays the answer

### Query Patterns

The chat supports these categories of questions:

**Crew / Sub queries:**
- "Who was on site [date]?" → Look up `reports[date].crew.subs_on_site`
- "How many workers [date/this week]?" → Sum headcounts
- "When was [sub name] last on site?" → Search all reports for sub
- "How many days has [sub] been on site?" → Count appearances
- "Which subs were missing this week?" → Check `expected_subs_missing`

**Weather queries:**
- "What was the weather on [date]?" → Look up weather readings
- "How many weather delay days?" → Sum delay hours, convert to days
- "Any cold weather days this month?" → Filter by temperature
- "When did we last have rain?" → Search conditions for precipitation

**Schedule queries:**
- "When is [milestone] due?" → Look up milestone date
- "Are we on track?" → Compare percent complete trend
- "What milestones are coming up?" → Filter upcoming milestones
- "How much has substantial completion slipped?" → Check version history

**Inspection queries:**
- "Did we pass the [type] inspection?" → Search inspection results
- "How many inspections this month?" → Count inspections in date range
- "Any failed inspections?" → Filter by result = "Fail"

**Material queries:**
- "When did the [material] get delivered?" → Search deliveries
- "Any delivery issues?" → Filter deliveries with condition != "Good"

**General queries:**
- "What happened on [date]?" → Full report summary for that date
- "Show me the last 3 reports" → Summary of recent reports
- "Any open items?" → List current open items
- "What's the current phase?" → Latest schedule.current_phase

### Query Engine Implementation

```javascript
class ProjectChat {
  constructor(reportData, projectConfig) {
    this.reports = reportData.reports;
    this.config = projectConfig;
  }

  processQuestion(question) {
    const q = question.toLowerCase();

    // Date extraction
    const dateMatch = this.extractDate(q);

    // Intent matching (ordered by specificity)
    if (q.includes('who') && q.includes('on site')) return this.crewQuery(dateMatch);
    if (q.includes('how many') && q.includes('worker')) return this.headcountQuery(dateMatch);
    if (q.includes('weather')) return this.weatherQuery(dateMatch);
    if (q.includes('milestone') || q.includes('due') || q.includes('on track')) return this.scheduleQuery(q);
    if (q.includes('inspection')) return this.inspectionQuery(q, dateMatch);
    if (q.includes('deliver')) return this.deliveryQuery(q, dateMatch);
    if (q.includes('what happened')) return this.daySummary(dateMatch);
    if (q.includes('open item')) return this.openItemsQuery();

    // Fallback: search all text fields
    return this.fullTextSearch(q);
  }

  // ... query methods that search embedded data and return formatted results
}
```

### Chat Response Format

Responses are displayed as formatted HTML within the chat panel:
- Text answers in paragraph form
- Data tables when returning lists (crew, inspections, deliveries)
- Simple inline charts for trend questions (sparklines)
- Links to jump to the relevant dashboard section when applicable

### Example Interactions

```
User: "Who was on site last Tuesday?"
Chat: "On Tuesday 2/10, 6 subs were on site with 42 total workers:
       • Walker Construction — 6 workers (backfill)
       • Metro Concrete — 8 workers (formwork)
       • ABC Mechanical — 4 workers (underground rough-in)
       • Smith Electric — 5 workers (conduit)
       • Delta Plumbing — 3 workers (underground)
       • Iron Workers Inc. — 16 workers (rebar)"

User: "Any weather delays this month?"
Chat: "2 weather delays in February so far:
       • 2/3 — 4 hours lost (heavy rain, exterior work suspended)
       • 2/7 — Full day lost (ice storm, site closed)
       Total: 12 hours (1.5 work days)"

User: "When is foundation complete due?"
Chat: "Foundation Complete milestone is scheduled for 03/15/2026 (31 days away).
       Status: On track. No revisions from original date."
```

### Limitations

The chat works with whatever data exists in the embedded JSON. If no reports have been generated, the chat will respond: "No report data available yet. Generate some daily reports first and the chat will have data to work with."

For questions the query engine can't parse, it responds: "I'm not sure how to answer that from the report data. Try asking about crew, weather, schedule, inspections, or materials — or ask 'what happened on [date]' for a full day summary."

## Regeneration

The dashboard is regenerated fresh each time it's requested. It always reflects the latest data in `daily-report-data.json`. There's no persistent dashboard state — it's a snapshot.

If the user wants to keep a snapshot (e.g., for a monthly report), suggest they save a copy with a date suffix: `MOSC_Dashboard_Feb2026.html`.
