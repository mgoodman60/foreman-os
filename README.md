# ForemanOS v5.0

The superintendent's operating system. 7 modular plugins for construction field management, powered by deep document intelligence.

Built for superintendents, not software engineers.

## Plugin Architecture

ForemanOS v5.0 splits the former monolith into 7 self-contained Cowork plugins. Each plugin has its own commands, skills, and agents. Install only what you need.

| Plugin | Cmds | Skills | Agents | Description |
|--------|------|--------|--------|-------------|
| **foremanos-core** | 7 | 6 | 4 | Project setup, data, dashboards, briefings, rendering. Install first. |
| **foremanos-intel** | 2 | 4+1 stub | 3 | Document intelligence, DWG extraction, quantitative takeoffs. |
| **foremanos-field** | 8 | 10+1 stub | 2 | Daily reporting, safety, quality, inspections, labor, punch lists. |
| **foremanos-planning** | 6 | 5+4 stubs | 2 | Scheduling, look-aheads, weekly reports, material tracking. |
| **foremanos-doccontrol** | 5 | 5+2 stubs | 0 | RFI prep, submittals, drawings, annotations, BIM. |
| **foremanos-cost** | 6 | 7+2 stubs | 0 | Cost tracking, EVM, pay apps, change orders, delays, claims. |
| **foremanos-compliance** | 5 | 5+3 stubs | 0 | Risk, environmental, closeout, sub scorecards, conflicts. |

**Totals:** 39 commands, 42 full skills + 13 stubs, 11 agents across 7 plugins.

## Installation

All plugins live in the **foreman-os-marketplace**. Install via Cowork:

```
claude plugin install foremanos-core@foreman-os-marketplace
```

**foremanos-core is required** -- every other plugin depends on it for project data, entity resolution, and the data store backbone.

### Recommended Install Sets

| Use Case | Plugins | Commands |
|----------|---------|----------|
| **Core only** | `foremanos-core` | `/set-project`, `/data`, `/dashboard`, `/morning-brief`, `/render`, `/site-context`, `/foremanos` |
| **Core + Field** | + `foremanos-field` | Add `/log`, `/daily-report`, `/amend-report`, `/safety`, `/quality`, `/inspections`, `/labor`, `/punch-list` |
| **Core + Field + Planning** | + `foremanos-planning` | Add `/look-ahead`, `/plan`, `/weekly-report`, `/schedules`, `/material-tracker`, `/meeting-notes` |
| **All 7** | All plugins | Full 39-command suite |

Install plugins one at a time, in any order after core:

```
claude plugin install foremanos-core@foreman-os-marketplace
claude plugin install foremanos-field@foreman-os-marketplace
claude plugin install foremanos-planning@foreman-os-marketplace
claude plugin install foremanos-intel@foreman-os-marketplace
claude plugin install foremanos-doccontrol@foreman-os-marketplace
claude plugin install foremanos-cost@foreman-os-marketplace
claude plugin install foremanos-compliance@foreman-os-marketplace
```

## A Day with ForemanOS

**6:15 AM** -- Run `/morning-brief` from the truck. Weather is 38F with rain clearing by 10 AM. The system flags 38F is below the 40F minimum for concrete placement per Section 03 30 00. Two deliveries today: structural steel at 7:30, waterproofing membrane at noon. Foundation inspection at 2 PM.

**7:00 AM** -- Steel arrives. Type `/log Walker delivered W12x26 beams to east wing, 14 pieces, good condition`. The system resolves "Walker" to Walker Construction from the sub directory, maps "east wing" to Grid E-G / Level 1, links steel to spec section 05 12 00, and logs quantity as 14 of 47 total beams (30%).

**11:30 AM** -- Walk the foundation forms. Type `/log rebar spacing looks tight in the north footing, grid B-2`. Classified as a quality observation, linked to Section 03 20 00 (ASTM A615 Grade 60), with a hold point inspection flagged before pour.

**3:00 PM** -- Run `/daily-report`. It pulls everything from the morning brief, both log entries, and any photos. Narratives standardized to third person past tense. Photos auto-captioned. Spec references, grid lines, and weather data woven in. Out comes a .docx matching your company template.

**Friday** -- `/weekly-report` rolls up all five daily reports into a polished owner summary. `/look-ahead` generates the 3-week schedule. `/dashboard` shows crew trends, inspection pass rates, and the S-curve.

## Command Map

Every command and which plugin provides it.

### foremanos-core (7 commands)

| Command | Description |
|---------|-------------|
| `/set-project [name]` | Initialize a new project. Collects basics, accepts document uploads, generates project memory (CLAUDE.md) |
| `/data [section]` | Project Data Intelligence dashboard. Browse and query all extracted intelligence across 40+ sections |
| `/dashboard [weekly\|project]` | Interactive HTML dashboard with Weekly/Project tabs and built-in data chat |
| `/morning-brief` | Daily briefing: weather, schedule, deliveries, alerts, pending RFIs, overdue submittals |
| `/render [type]` | Generate AI architectural renderings from project intelligence and visual context |
| `/site-context [gather\|review]` | Gather visual context for AI rendering -- site photos, design intent, material selections |
| `/foremanos` | Plugin help and command reference |

### foremanos-intel (2 commands)

| Command | Description |
|---------|-------------|
| `/process-docs [filename, type, or "scan"]` | Process documents for intelligence extraction. Auto-classifies, extracts, and merges with project data |
| `/process-dwg [filename.dwg]` | Extract intelligence from AutoCAD DWG files (including Civil 3D) via libredwg/DXF pipeline |

### foremanos-field (8 commands)

| Command | Description |
|---------|-------------|
| `/log [observation \| clear]` | Log field observations. Natural language with classification, entity resolution, and enrichment |
| `/daily-report [date]` | Generate daily report .docx with language standardization, photo captioning, and spec enrichment |
| `/amend-report [number or date]` | Corrections or additions to a previously generated report |
| `/safety [log\|incident\|toolbox\|jsa\|metrics\|inspect\|report]` | Safety management: incidents, toolbox talks, JSAs, OSHA 300/301/300A, TRIR/DART/EMR metrics |
| `/quality [checklist\|itp\|deficiency\|metrics\|report]` | QMS: three-phase inspection checklists, ITP management, deficiency tracking, FPIR metrics |
| `/inspections [schedule\|log\|status\|permits]` | Schedule inspections, log results, track permits, view status |
| `/labor [log\|summary\|productivity\|validate\|payroll\|cost]` | Per-worker and crew labor tracking, productivity metrics, certified payroll, EV cost integration |
| `/punch-list [add\|status\|generate]` | Punch list items from identification through completion with back-charge management |

### foremanos-planning (6 commands)

| Command | Description |
|---------|-------------|
| `/look-ahead [weeks]` | 3-week lookahead schedule with sub assignments, materials, weather constraints, and blockers |
| `/plan [weekly\|status\|constraints\|commitments\|report]` | Last Planner System: weekly work plans, PPC tracking, constraint analysis, variance |
| `/weekly-report [week-ending date]` | Aggregate daily reports into a polished weekly owner/PM summary |
| `/schedules [type]` | Generate formatted construction schedules: door, hardware, fixture, finish, plumbing, equipment, room |
| `/material-tracker [add\|status\|delivery\|verify\|find]` | Full-lifecycle material management with delivery verification and vendor search |
| `/meeting-notes [type]` | Meeting minutes for OAC, progress, safety, and pre-installation meetings. Action item carry-forward |

### foremanos-doccontrol (5 commands)

| Command | Description |
|---------|-------------|
| `/prepare-rfi [topic]` | Draft RFIs with auto-filled drawing references, spec sections, grid lines. Also handles transmittals |
| `/submittal-review [ID]` | Review submittals against spec requirements. Compliance matrix and professional review comments |
| `/drawings [status\|add\|revise\|asi\|audit\|search\|distribute]` | Drawing revision control: ASIs, superseded sheets, field audits, distribution |
| `/annotate [plan\|spec\|photo\|rfi] [reference]` | Document markup: plan redlines, spec highlighting, photo callouts, as-built annotations |
| `/bim [status\|clash\|model\|scan]` | BIM coordination: clash detection, model-to-field verification, 4D scheduling, digital twin |

### foremanos-cost (6 commands)

| Command | Description |
|---------|-------------|
| `/cost [status\|forecast\|variance\|invoice\|report]` | Budget structure, CPI/EAC/variance analysis, cash flow projections |
| `/evm [status\|calculate\|curve\|forecast\|report]` | Earned Value Management with S-curve, SPI/CPI, EAC/ETC forecasting |
| `/pay-app [add\|status\|generate]` | AIA G702/G703 pay applications: schedule of values, retainage, lien waivers |
| `/change-order [add\|status\|log]` | Change order tracking with T&M tags, field sign-off workflow, CO integration |
| `/delay [add\|status\|log]` | Delay tracking: excusable/compensable classification, critical path analysis, TIA |
| `/claims [document\|notice\|package\|status]` | Claims documentation: contemporaneous records, notice letters, claims package assembly |

### foremanos-compliance (5 commands)

| Command | Description |
|---------|-------------|
| `/risk [add\|review\|report\|matrix]` | 5x5 probability/impact matrix, risk register, mitigation tracking, contingency management |
| `/environmental [leed\|swppp\|hazmat\|waste\|report]` | LEED credits, SWPPP, hazmat, waste diversion, dust/noise monitoring, incident response |
| `/closeout [status\|add\|checklist\|commission\|warranty\|generate]` | Closeout tracking, ASHRAE Guideline 0 commissioning, warranty management |
| `/sub-scorecard [sub name\|all\|report\|compare]` | Sub performance scorecards: schedule, quality, safety, responsiveness, professionalism |
| `/conflicts [scan\|status\|resolve\|history]` | Cross-discipline conflict detection across plans, specs, schedules, and field data |

## Agent Roster

11 autonomous agents across 4 plugins. Agents monitor, analyze, and advise across the project intelligence store. They are read-only -- they never modify data without user approval.

| Agent | Plugin | Role |
|-------|--------|------|
| **superintendent-assistant** | core | Top-level router to specialized agents. Handles general project questions |
| **project-data-navigator** | core | Translates natural language questions to structured data queries across the 28-file store |
| **dashboard-intelligence-analyst** | core | Generates dashboard summaries, executive briefings, and narrative health reports |
| **project-health-monitor** | core | Evaluates 11 KPIs and 5 anomaly detection rules for health alerts and trends |
| **doc-orchestrator** | intel | Coordinates multi-document extraction runs and validates output |
| **data-integrity-watchdog** | intel | Validates consistency across all 28 JSON files -- orphans, conflicts, schema gaps |
| **deadline-sentinel** | planning | Monitors all deadline sources with 6-tier urgency across schedule, submittals, RFIs, procurement |
| **report-quality-auditor** | field | 10 daily + 6 weekly QA checks on generated reports |
| **field-intelligence-advisor** | field | Contextual field intelligence for real-time superintendent decisions |
| **weekly-planning-coordinator** | planning | Orchestrates the weekly lookahead cycle using Last Planner System principles |
| **conflict-detection-agent** | intel | 25 detection rules across 8 conflict categories for cross-discipline discrepancies |

## Skills Architecture

### Full Skills vs. Stubs

Each plugin carries its own **full skills** (SKILL.md plus references/ and scripts/ directories). When a command in one plugin needs methodology from a skill owned by a different plugin, it uses a **stub** -- a SKILL.md-only copy of the canonical source, without the references/ directory.

Stubs are kept in sync by running `sync-stubs.sh` from the repo root after editing any canonical SKILL.md. The script prepends a header comment identifying the canonical source.

**Current stub map:**

| Stub Skill | Canonical Owner | Consumed By |
|------------|-----------------|-------------|
| project-data | foremanos-core | intel, field, planning, doccontrol, cost, compliance |
| report-qa | foremanos-field | planning |
| document-intelligence | foremanos-intel | doccontrol, compliance |
| estimating-intelligence | foremanos-intel | cost |
| quantitative-intelligence | foremanos-intel | planning |
| submittal-intelligence | foremanos-doccontrol | planning |
| delay-tracker | foremanos-cost | compliance |

### Cross-Plugin Reference Strategy

Plugins reference each other using three mechanisms, in order of preference:

1. **Stubs** -- SKILL.md methodology synced via `sync-stubs.sh`. The command reads the stub like any local skill. Used for foundational skills needed by many plugins (e.g., project-data).
2. **Soft references** -- A command mentions a skill by name and describes what it provides, without requiring the file to be present. The AI resolves these if the other plugin is installed; gracefully degrades if not.
3. **Inlined methodology** -- For agent-level knowledge, the relevant methodology is written directly into the agent definition. Agents are never copied between plugins.

Zero agent copies across the entire system. Zero hard cross-plugin file path references.

## Data Flow

The intelligence pipeline is unchanged from v4.x:

```
Documents (plans, specs, schedule, contracts, sub list, geotech, safety plan...)
    |
    v
/process-docs or /process-dwg  [foremanos-intel]
    |
    v
Three-pass extraction pipeline (metadata -> structural analysis -> targeted content)
    |
    v
28-file JSON intelligence store (in project's AI - Project Brain/ directory)
    |
    v
All downstream commands and agents consume the store
```

### Intelligence Store (28 JSON files)

**Project Core:**
`project-config.json`, `plans-spatial.json`, `specs-quality.json`, `schedule.json`, `directory.json`

**Document & Issue Tracking:**
`rfi-log.json`, `submittal-log.json`, `procurement-log.json`, `change-order-log.json`, `inspection-log.json`, `meeting-log.json`, `punch-list.json`, `delay-log.json`, `drawing-log.json`

**Financial & Labor:**
`cost-data.json`, `pay-app-log.json`, `labor-tracking.json`

**Quality:**
`quality-data.json`

**Safety, Risk & Closeout:**
`safety-log.json`, `risk-register.json`, `claims-log.json`, `environmental-log.json`, `closeout-data.json`, `annotation-log.json`

**Visualization:**
`visual-context.json`, `rendering-log.json`

**Report History:**
`daily-report-data.json`, `daily-report-intake.json`

Every command that reads project data uses entity resolution (sub names, grid locations, spec sections, schedule activities) to enrich raw input with intelligence from the store.

## Supported Document Types

| Document | What Gets Extracted |
|----------|-------------------|
| Plans / Drawings | Grid lines, building areas, floor levels, room schedules, site layout, door/hardware/finish/fixture schedules |
| Specifications | CSI divisions, material specs, weather thresholds, hold points, tolerances, testing requirements |
| CPM Schedule | Milestones, critical path, near-critical, weather-sensitive activities, long-lead items |
| Contract | Key dates, LDs, working hours, documentation requirements |
| Sub List / Bid Tab | Subcontractor directory with trades, scopes, contacts |
| Geotechnical Report | Bearing capacity, water table, compaction requirements, unsuitable soils |
| Safety Plan | Fall protection zones, confined spaces, hot work areas, crane exclusion zones |
| SWPPP | BMP inventory, inspection triggers, documentation requirements |
| RFI / Submittal Logs | Entries with status, references, responses, lead times |
| Vendor Quotes / Product Data | Supplier capabilities, contact info, pricing, certifications |
| AutoCAD DWG / Civil 3D | Survey points, utility structures, contours, property boundaries, grading data (via libredwg) |

## Migration from v4.2

The v4.2 monolith (single `foreman-os` plugin with top-level `commands/`, `skills/`, `agents/` directories) has been replaced by 7 self-contained plugins. Key changes:

- **Monolith removed.** The old single-plugin structure (`commands/`, `skills/`, `agents/` at repo root) no longer exists. All content is now inside the 7 `foremanos-*` plugin directories.
- **marketplace.json updated.** Lists 7 plugins instead of 1. Each plugin has its own `commands/`, `skills/`, and `agents/` directories.
- **No command changes.** All 39 commands work exactly as before. Same names, same arguments, same behavior. The only difference is which plugin provides them.
- **Stubs replace cross-references.** Where the monolith had direct file path references between skills, the split uses stubs and soft refs. Run `sync-stubs.sh` after editing canonical skills.
- **Project data is unchanged.** The 28-file JSON store, extraction pipeline, and project memory (CLAUDE.md) are identical. No data migration needed.

### What Stayed Local

The `plugins/` directory still contains 4 **Claude Code-only dev plugins** that are NOT part of the marketplace and NOT for Cowork:

| Plugin | Purpose |
|--------|---------|
| foremanos-stack | Prisma 6.7, NextAuth RBAC, Redis caching, SWR fetching, Trigger.dev task patterns |
| foremanos-llm | Multi-provider LLM orchestration, vision pipeline, RAG system, prompt patterns |
| foremanos-testing | Vitest patterns, API route testing, `/test-coverage-report` command |
| foremanos-documents | PDF generation (react-pdf/pdf-lib/pdfkit), Office docs, R2 file storage |

These are development-time skills for the ForemanOS Next.js application codebase. They require Claude Code's execution environment and will cause sandbox mount errors if installed in Cowork.

## Repository Structure

```
foreman-os/
  .claude-plugin/
    marketplace.json           -- Marketplace manifest (lists all 7 plugins)
  foremanos-core/              -- Core plugin (install first)
    commands/
    skills/
    agents/
  foremanos-intel/             -- Document intelligence plugin
    commands/
    skills/
    agents/
  foremanos-field/             -- Field operations plugin
    commands/
    skills/
    agents/
  foremanos-planning/          -- Planning & scheduling plugin
    commands/
    skills/
    agents/
  foremanos-doccontrol/        -- Document control plugin
    commands/
    skills/
    agents/
  foremanos-cost/              -- Cost & financial plugin
    commands/
    skills/
    agents/
  foremanos-compliance/        -- Risk & compliance plugin
    commands/
    skills/
    agents/
  plugins/                     -- 4 Claude Code-only dev plugins (not in marketplace)
  sync-stubs.sh                -- Sync stub SKILL.md files across plugins
  CLAUDE.md                    -- Repository-level developer guide
  README.md                    -- This file
```
