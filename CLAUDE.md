> See `~/.claude/CLAUDE.md` for universal workflow, agent teams, security, ecosystem, and key commands.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

This is **foreman-os-marketplace**, a Cowork plugin marketplace containing **7 self-contained ForemanOS plugins** (v6.0.0) for construction superintendents. The monolith has been split so each plugin can be installed independently. The marketplace also includes 4 Claude Code-only dev plugins (not listed in the marketplace).

There is no build system, no tests, no package manager. The entire codebase is markdown files, JSON configs, a stub sync script, and a few Python reference scripts.

## Repository Structure

```
.claude-plugin/
  marketplace.json              -- Lists 7 plugins (no monolith, no dev plugins)

foremanos-core/                 -- Project setup, data, dashboards, briefings, rendering
  .claude-plugin/plugin.json
  commands/                     -- 7: set-project, data, morning-brief, dashboard, render, site-context, foremanos
  skills/                       -- 6: project-data, project-data-intel, project-dashboard, rendering-generator, image-generation-mcp, project-visual-context
  agents/                       -- 4: superintendent-assistant, project-data-navigator, dashboard-intelligence-analyst, project-health-monitor

foremanos-intel/                -- Document extraction, DWG parsing, takeoffs, estimating
  .claude-plugin/plugin.json
  commands/                     -- 2: process-docs, process-dwg
  skills/                       -- 4 full + 1 stub: document-intelligence, dwg-extraction, quantitative-intelligence, estimating-intelligence + project-data (stub)
  agents/                       -- 3: doc-orchestrator, data-integrity-watchdog, conflict-detection-agent

foremanos-field/                -- Daily reporting, safety, quality, inspections, labor, punch lists
  .claude-plugin/plugin.json
  commands/                     -- 8: log, daily-report, amend-report, safety, quality, inspections, labor, punch-list
  skills/                       -- 10 full + 1 stub: intake-chatbot, daily-report-format, report-qa, safety-management, quality-management, inspection-tracker, labor-tracking, punch-list, photo-documentation, field-reference (21 trade guides) + project-data (stub)
  agents/                       -- 2: field-intelligence-advisor, report-quality-auditor

foremanos-planning/             -- Scheduling, look-aheads, Last Planner, weekly reports, materials
  .claude-plugin/plugin.json
  commands/                     -- 6: plan, schedules, look-ahead, weekly-report, meeting-notes, material-tracker
  skills/                       -- 5 full + 4 stubs: last-planner, look-ahead-planner, weekly-report-format, meeting-minutes, material-tracker + project-data (stub), report-qa (stub), quantitative-intelligence (stub), submittal-intelligence (stub)
  agents/                       -- 2: weekly-planning-coordinator, deadline-sentinel

foremanos-doccontrol/           -- RFIs, submittals, drawings, annotations, BIM
  .claude-plugin/plugin.json
  commands/                     -- 5: prepare-rfi, submittal-review, drawings, annotate, bim
  skills/                       -- 5 full + 2 stubs: rfi-preparer, submittal-intelligence, drawing-control, document-annotation, bim-coordination + project-data (stub), document-intelligence (stub)
  agents/                       -- (none)

foremanos-cost/                 -- Cost tracking, earned value, pay apps, change orders, delays, claims
  .claude-plugin/plugin.json
  commands/                     -- 6: cost, evm, pay-app, change-order, delay, claims
  skills/                       -- 7 full + 2 stubs: cost-tracking, earned-value-management, pay-application, change-order-tracker, delay-tracker, claims-documentation, contract-administration + project-data (stub), estimating-intelligence (stub)
  agents/                       -- (none)

foremanos-compliance/           -- Risk, environmental, closeout, commissioning, sub scorecards
  .claude-plugin/plugin.json
  commands/                     -- 5: risk, environmental, closeout, sub-scorecard, conflicts
  skills/                       -- 5 full + 3 stubs: risk-management, environmental-compliance, closeout-commissioning, cobie-export, sub-performance + project-data (stub), document-intelligence (stub), delay-tracker (stub)
  agents/                       -- (none)

plugins/                        -- 4 Claude Code-only dev plugins (NOT in marketplace)
  foremanos-stack/              -- Prisma, NextAuth, Redis, SWR, Trigger.dev patterns + hooks
  foremanos-llm/                -- LLM orchestration, vision, RAG, prompt patterns + agent
  foremanos-testing/            -- Vitest, API route testing patterns + /test-coverage-report command
  foremanos-documents/          -- PDF gen, Office docs, R2 file storage patterns

sync-stubs.sh                   -- Syncs stub SKILL.md files from canonical sources
```

**Totals across the 7 marketplace plugins:** 40 commands, 43 full skills, 13 stubs, 11 agents.

## Architecture

### Self-Contained Plugins

Each of the 7 plugins is fully self-contained. All `${CLAUDE_PLUGIN_ROOT}` references in commands resolve within that plugin's own directory tree. A command in `foremanos-field/commands/log.md` references `${CLAUDE_PLUGIN_ROOT}/skills/intake-chatbot/SKILL.md` and that resolves to `foremanos-field/skills/intake-chatbot/SKILL.md`. There are no cross-plugin `${CLAUDE_PLUGIN_ROOT}` paths.

### Zero Agent Copies

There are 11 agents in 11 unique locations across 4 plugins. Agents are never copied or stubbed. Cross-plugin agent needs are handled by three mechanisms:

1. **Skill stubs** -- A SKILL.md-only copy (no references/ folder) lets commands in other plugins read the skill methodology without needing the full skill.
2. **Soft refs** -- Commands include graceful text guidance like "If the foremanos-intel plugin is installed, the doc-orchestrator agent can validate extraction output." No hard path dependency.
3. **Inlined methodology** -- Key logic from agents is embedded directly into command markdown when a command needs agent-like behavior but the agent lives in another plugin.

### Plugin System

- `marketplace.json` at the repo root registers the 7 plugins by name and source path
- Each plugin has its own `.claude-plugin/plugin.json` with name, version, description, author
- Commands are markdown files with YAML frontmatter (`description`, `allowed-tools`, `argument-hint`)
- Skills are directories containing a `SKILL.md` and an optional `references/` folder
- Agents are markdown files with YAML frontmatter (`name`, `description`) and structured sections (Context, Methodology, Data Sources, Output Format, Constraints)
- Commands, skills, and agents are auto-discovered from their respective directories -- no registration in plugin.json needed

### Command to Skill Relationship

Commands (in `<plugin>/commands/`) are the user-facing entry points (invoked as `/log`, `/daily-report`, etc.). Each command's markdown body tells the AI which skill(s) to read before executing. Skills (in `<plugin>/skills/`) contain the deep logic, classification rules, extraction pipelines, and data schemas.

Example chain: `/log` command (foremanos-field) reads `intake-chatbot` skill + `project-data` skill (stub) -> classifies input -> enriches with project intelligence -> writes to `daily-report-intake.json`.

### Agent System

Eleven agents across 4 plugins. No agents in doccontrol, cost, or compliance.

| Plugin | Agent | Role |
|--------|-------|------|
| core | superintendent-assistant | Top-level router to the 10 specialized agents |
| core | project-data-navigator | Translates natural language questions to data queries |
| core | dashboard-intelligence-analyst | Generates dashboard views and executive briefings |
| core | project-health-monitor | Evaluates 11 KPIs and 5 anomaly detection rules |
| intel | doc-orchestrator | Coordinates extraction pipelines and validates output |
| intel | data-integrity-watchdog | Validates consistency across all 28 JSON files |
| intel | conflict-detection-agent | Scans for cross-discipline conflicts across plans, specs, schedules, and field data |
| field | field-intelligence-advisor | Contextual briefings for field situations |
| field | report-quality-auditor | 10 daily + 6 weekly QA checks on reports |
| planning | weekly-planning-coordinator | Last Planner System cycle with constraint analysis |
| planning | deadline-sentinel | Monitors all deadline sources with 6-tier urgency |

Agents are read-only -- they query the 28-file data store but never modify data without user approval. They consume reference docs from `foremanos-core/skills/project-data/references/` for thresholds, query patterns, and validation rules.

### Cowork vs Claude Code

- The 7 marketplace plugins (foremanos-core through foremanos-compliance) work in both Cowork and Claude Code
- The 4 dev plugins under `plugins/` are Claude Code-only -- they contain hooks that require Claude Code's execution environment
- Do NOT install dev plugins in Cowork -- they cause sandbox mount errors
- The dev plugins are intentionally excluded from `marketplace.json`

### Key Conventions

- Commands reference skills via `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` -- this variable resolves to the plugin's own root directory at runtime
- Commands also reference Cowork platform skills (e.g., `docx`, `pdf`, `construction-takeoff`) for output formatting
- All project data files are JSON, stored in the user's `AI - Project Brain/` folder (or working directory root as fallback)
- The `project-data` skill (`foremanos-core/skills/project-data/SKILL.md`) is the central data backbone -- nearly every command reads it (via the canonical copy or a stub)

## Stub Policy

Stubs let commands in one plugin reference skill methodology from another plugin without duplicating the full skill (references/, scripts/, etc.). A stub is a SKILL.md-only copy with a header comment marking it as a stub.

### Rules

1. Stubs contain ONLY a `SKILL.md` file -- no `references/` folder, no scripts
2. Every stub has a header comment: `<!-- STUB: Canonical source is <plugin>/skills/<name>/SKILL.md. Run sync-stubs.sh to update. Do NOT edit directly. -->`
3. After editing any canonical SKILL.md, run `sync-stubs.sh` from the repo root to propagate changes
4. NEVER edit a stub directly -- always edit the canonical source and sync

### Canonical Source Mappings

| Skill | Canonical Plugin | Stub Consumers |
|-------|-----------------|----------------|
| project-data | foremanos-core | intel, field, planning, doccontrol, cost, compliance |
| report-qa | foremanos-field | planning |
| document-intelligence | foremanos-intel | doccontrol, compliance |
| estimating-intelligence | foremanos-intel | cost |
| delay-tracker | foremanos-cost | compliance |
| quantitative-intelligence | foremanos-intel | planning |
| submittal-intelligence | foremanos-doccontrol | planning |

There are 13 stub files total across the 7 plugins.

## Marketplace

`marketplace.json` lists exactly 7 plugins:

| # | Plugin | Description |
|---|--------|-------------|
| 1 | foremanos-core | Project setup, data, dashboards, briefings, rendering. Install first. |
| 2 | foremanos-intel | Document intelligence, DWG extraction, quantitative takeoffs. |
| 3 | foremanos-field | Daily reporting, safety, quality, inspections, labor, punch lists. 21 field guides. |
| 4 | foremanos-planning | Scheduling, look-aheads, Last Planner, weekly reports, material tracking. |
| 5 | foremanos-doccontrol | RFI preparation, submittal reviews, drawing control, annotations, BIM. |
| 6 | foremanos-cost | Cost tracking, earned value, pay apps, change orders, delays, claims. |
| 7 | foremanos-compliance | Risk registers, environmental, closeout, commissioning, sub scorecards, conflicts. |

There is no monolith entry. There are no dev plugin entries. The dev plugins in `plugins/` are Claude Code-only and never appear in the marketplace.

## Data Flow

Documents -> `document-intelligence` skill (5-phase adaptive extraction) in foremanos-intel -> structured JSON files -> consumed by commands/skills across all 7 plugins.

### The 28-File Data Store

All project data files are JSON, stored in the user's `AI - Project Brain/` folder:

| File | Purpose |
|------|---------|
| `project-config.json` | Master config, folder mapping, document tracking, claims_mode flag |
| `plans-spatial.json` | Grid lines, rooms, quantities, site layout, as-built overlay |
| `specs-quality.json` | Spec sections, materials, thresholds, tolerances, hold points, safety zones |
| `schedule.json` | Milestones, critical path, float, lookahead history, weather-sensitive activities |
| `directory.json` | Subs, vendors, contacts, assignments, trade mapping |
| `daily-report-intake.json` | Today's field log entries (append here) |
| `daily-report-data.json` | Historical report data |
| `safety-log.json` | Safety observations and incidents |
| `inspection-log.json` | Inspection schedule and results |
| `rfi-log.json` | RFI tracking |
| `submittal-log.json` | Submittal status |
| `cost-data.json` | Budget, earned value, contingency, CPI/SPI |
| `labor-tracking.json` | Worker hours, crew productivity, certified payroll |
| `procurement-log.json` | Material procurement and delivery tracking |
| `quality-data.json` | Inspection results, material tests, warranties, system tests, equipment data |
| `change-order-log.json` | Change orders with cost/schedule impact |
| `delay-log.json` | Delay events, weather days, claims documentation |
| `visual-context.json` | Site photo context and visual references |
| `rendering-log.json` | Rendering generation history |
| `drawing-log.json` | Drawing register and as-built markup status |
| `closeout-data.json` | Closeout checklists, commissioning, O&M status |
| `risk-register.json` | Risk events, probability, impact, mitigation |
| `claims-log.json` | Claims documentation and tracking |
| `environmental-log.json` | Environmental compliance records |
| `annotation-log.json` | Document annotation records |
| `punch-list.json` | Punch list items with status tracking |
| `meeting-log.json` | Meeting minutes and action items |
| `material-test-log.json` | Material test results and specimen tracking |

### Pipeline Reference Documentation

The canonical `project-data` skill in foremanos-core has 11 reference documents in `foremanos-core/skills/project-data/references/`:

**Pipeline architecture (3):**
- **`json-schema-reference.md`** -- Complete schema for all 28 JSON files with producer/consumer mapping per field
- **`data-flow-map.md`** -- Pipeline architecture with ASCII diagrams: Documents -> document-intelligence -> JSON store -> downstream skills
- **`cross-reference-patterns.md`** -- Twelve codified cross-referencing patterns (Sub->Scope->Spec->Inspection, Location->Grid->Area->Room, WorkType->Weather->Threshold, Element->AssemblyChain->MultiSheet, RFI->Submittal->Procurement, Assembly->Schedule->EarnedValue, DualSource->UtilityReconciliation, Risk->Schedule->Cost, Claims->Delay->CO, Environmental->Inspection->Safety, Closeout->Quality->Drawing, Annotation->Drawing->RFI)

**Agent-supporting (4 -- consumed by agents for thresholds, queries, and validation):**
- **`alert-thresholds.md`** -- KPI thresholds, anomaly detection rules, and severity scoring for project-health-monitor and dashboard-intelligence-analyst agents
- **`data-query-patterns.md`** -- 20+ cross-file query patterns (QP-MAT-*, QP-SUB-*, QP-SCH-*, QP-LOC-*, QP-COST-*) with join logic for project-data-navigator
- **`natural-language-query-guide.md`** -- Maps superintendent questions to data queries with intent detection and entity recognition
- **`extraction-validation-checklist.md`** -- Post-extraction validation checklists for all 3 pipelines, consumed by doc-orchestrator

**Other (4):**
- **`config-schema.md`** -- Project configuration schema and field definitions
- **`report-history-schema.md`** -- Daily report data structure and history format
- **`skill-detail.md`** -- Detailed skill capability mapping
- **`masterformat-reference.md`** -- CSI MasterFormat division reference

### Downstream Skill Auto-Population

Twenty downstream skills have explicit "Project Intelligence Integration" (or "Auto-Population" / "Auto-Linking") sections that tell the AI exactly which JSON files and field paths to read for auto-populating data. This eliminates guesswork -- each skill names its data sources:

**foremanos-field:**
- `punch-list` -- location from plans-spatial, sub from directory, spec cross-ref, drawing ref, schedule impact
- `inspection-tracker` -- hold points from specs-quality, weather check, spec deep-link, schedule activity, drawing ref
- `safety-management` -- weather alerts from specs-quality, safety zones, utility locations, sub safety performance
- `labor-tracking` -- location from plans-spatial, employer from directory, productivity benchmarking, daily report cross-validation, cost code mapping
- `intake-chatbot` -- spec enrichment, schedule awareness, weather-work cross-check, quantity context, inspection reminders
- `report-qa` -- punch list cross-check, cost authorization, procurement verification, quality correlation, safety incident cross-check, schedule milestone validation, weather threshold verification

**foremanos-planning:**
- `meeting-minutes` -- schedule update, RFI/submittal status, CO status, action item carry-forward, weather + safety summaries
- `last-planner` -- activity pool from schedule.json, sub availability from directory + labor-tracking, location constraints from plans-spatial, weather from specs-quality thresholds, material readiness from procurement-log, prerequisite inspections from specs-quality hold points + inspection-log
- `look-ahead-planner` -- activity extraction from schedule.json, predecessor tracking, sub mobilization from directory, material delivery from procurement-log, inspection prerequisites from specs-quality hold points + inspection-log, weather restrictions from specs-quality thresholds

**foremanos-doccontrol:**
- `rfi-preparer` -- location from plans-spatial, drawing refs from sheet_cross_references, spec section from specs-quality, team routing from directory, numbering from rfi-log, related items cross-ref
- `submittal-intelligence` -- procurement lead time from procurement-log, sub contact from directory, hold point linking from specs-quality, cost impact from cost-data, quality test correlation from quality-data, installation verification from daily-report-data
- `drawing-control` -- as-built markup status per sheet in drawing-log, deviation cross-reference against rfi-log and change-order-log, closeout completeness flagging, links to as-built-extraction.md

**foremanos-cost:**
- `cost-tracking` -- quantity verification from plans-spatial, schedule-cost alignment, CO linkage, procurement tracking
- `earned-value-management` -- budget baseline from cost-data, schedule baseline from schedule.json, actual costs from labor-tracking + procurement-log, earned value from cost-data percent complete, CO adjustments, forecast validation against delay-log
- `change-order-tracker` -- schedule impact from schedule.json, cost context from cost-data, spec linking, drawing ref, sub identification
- `delay-tracker` -- critical path impact from schedule.json, weather verification from specs-quality thresholds + daily-report-data, cost impact from cost-data + labor-tracking, related delays from delay-log, float analysis from schedule.json

**foremanos-compliance:**
- `risk-management` -- schedule risks from schedule.json critical path/float, weather thresholds from specs-quality, sub performance from directory + quality-data, contingency context from cost-data, delay patterns from delay-log, procurement risks from procurement-log
- `sub-performance` -- sub roster from directory, schedule adherence from daily-report-data + schedule.json + labor-tracking, quality from inspection-log + quality-data + punch-list, safety from safety-log, responsiveness from rfi-log + submittal-log, productivity from labor-tracking
- `closeout-commissioning` -- warranty tracking from quality-data warranties, commissioning test results from quality-data system_tests, O&M manual completeness from quality-data equipment_data, as-built drawing status from plans-spatial as_built_overlay
- `quality-management` (field) -- spec-based checklists from specs-quality, hold points, location from plans-spatial, sub QC contact from directory, FPIR trends from quality-data, drawing refs, material test result verification, specimen traceability against procurement-log delivery_tickets

### Extraction Templates

The `document-intelligence` skill in foremanos-intel has 28 reference documents in `foremanos-intel/skills/document-intelligence/references/`, including extraction templates for plans, specs, schedules, MEP, fire protection, civil, PEMB, submittals, RFIs, ASIs, concrete mix designs, compliance, material testing, warranty documentation, as-builts, testing and commissioning, and O&M manuals.

The `quantitative-intelligence` skill has a `calculation-workflow.md` documenting how downstream skills should request calculations from the 10 calculator classes (ConcreteVolumeCalc, WallAreaCalc, RoomAreaCalc, PipeRunCalc, FootingCalc, SlabCalc, RoofCalc, PEMBCalc, SymbolCountCalc, AggregateCalc), including source priority levels and confidence scoring.

## Python Reference Scripts and Executable Scripts

Python files exist under `foremanos-intel/skills/document-intelligence/references/` and `foremanos-intel/skills/quantitative-intelligence/references/` -- these are reference implementations for visual plan analysis, sheet cross-referencing, and calculation bridging. They are not executed directly by the plugin but serve as reference code for the AI.

- `foremanos-intel/skills/document-intelligence/references/visual_plan_analyzer.py` -- Visual plan analysis
- `foremanos-intel/skills/document-intelligence/references/parse_dxf.py` -- DXF entity parser reference
- `foremanos-intel/skills/document-intelligence/references/convert_dwg.py` -- DWG to DXF conversion reference
- `foremanos-intel/skills/quantitative-intelligence/references/calc_bridge.py` -- Calculation bridge
- `foremanos-intel/skills/quantitative-intelligence/references/sheet_xref.py` -- Sheet cross-referencing
- `foremanos-core/skills/image-generation-mcp/references/server.py` -- MCP image generation server

The `foremanos-intel/skills/dwg-extraction/scripts/` directory contains executable scripts that ARE run directly:
- `compile_libredwg.sh` -- Compiles the libredwg C library from GitHub source (cached at `/tmp/libredwg/dwg2dxf`)
- `parse_dxf.py` -- Custom DXF entity parser that handles Civil 3D XDATA patterns, INSERT+ATTRIB sequences, and proximity-based structure grouping

**Important for local development**: The Python virtual environment lives at `~/foreman-os-venv/` (outside the repo). The MCP server config is at `~/.claude/.mcp.json` (user-level). These are kept outside the repo because the local directory marketplace copier does not respect `.gitignore` -- anything in the repo root gets copied to the plugin cache, which breaks the Cowork sandbox.

## Editing Patterns

### Adding a Command

Create a markdown file in `<plugin>/commands/` with YAML frontmatter (`description`, `allowed-tools`, `argument-hint`) and step-by-step instructions that reference the relevant skills using `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md`. All skill references must resolve within the same plugin. If the command needs a skill from another plugin, add a stub (see Stub Policy) or use a soft ref.

### Adding a Skill

Create a directory under `<plugin>/skills/<skill-name>/` with a `SKILL.md` (YAML frontmatter with `name`, `description`, `version`) and optionally a `references/` folder for supporting docs or scripts. If this skill needs to be consumed by commands in other plugins, add it to the stub mappings in `sync-stubs.sh` and run the script.

### Adding an Agent

Create a markdown file in `<plugin>/agents/` with YAML frontmatter (`name`, `description`) and structured sections (Context, Methodology, Data Sources, Output Format, Constraints). Agents are auto-discovered from the directory. NEVER copy an agent to another plugin -- use inlined methodology or soft refs instead.

### Creating Cross-Plugin References

When a command in one plugin needs methodology from another plugin:

1. **Prefer stubs** -- If a SKILL.md stub already exists (check the mapping table above), reference it via `${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md`.
2. **Add a new stub** -- If no stub exists and the need is strong, add the canonical-to-consumer mapping in `sync-stubs.sh`, run the script, and reference the stub.
3. **Use soft refs** -- For optional/advisory cross-plugin dependencies, include text guidance: "If the foremanos-intel plugin is installed, see its doc-orchestrator agent for extraction validation."
4. **Inline methodology** -- For agent-like behavior needed by a command in a different plugin, embed the key logic directly in the command markdown.

### Modifying the Plugin Manifest

- To update a plugin's metadata, edit its `.claude-plugin/plugin.json`
- To add or remove a marketplace plugin, edit `.claude-plugin/marketplace.json` at the repo root
- NEVER add dev plugins (from `plugins/`) to the marketplace

### Updating Stubs

After editing any canonical SKILL.md, run from the repo root:

```bash
./sync-stubs.sh
```

This propagates changes to all stub consumers. The script reports which stubs were created or updated.
