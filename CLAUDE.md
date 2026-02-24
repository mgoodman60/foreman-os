# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

This is **foreman-os-marketplace**, a cowork plugin marketplace repository containing the **Foreman_OS** plugin (v4.2.0) — a construction superintendent operating system with 42 skills, 37 commands, 10 agents, and 21 field-reference documents. It runs as a plugin inside the cowork platform.

## Repository Structure

```
.claude-plugin/
  marketplace.json                 — Marketplace manifest (lists plugins)
  plugin.json                      — Plugin metadata (name, version, description)
README.md                          — Full documentation of commands, skills, agents, and data files
agents/                            — 10 autonomous agents (monitoring, analysis, advisory)
commands/                          — 37 slash-command definitions (markdown files)
skills/                            — 42 skill directories, each with SKILL.md + references/ or scripts/
plugins/                           — 4 Claude Code dev plugins (not used by Cowork)
  foremanos-stack/                 — Prisma, NextAuth, Redis, SWR, Trigger.dev patterns + hooks
  foremanos-llm/                   — LLM orchestration, vision, RAG, prompt patterns + agent
  foremanos-testing/               — Vitest, API route testing patterns + /test-coverage-report command
  foremanos-documents/             — PDF gen, Office docs, R2 file storage patterns
```

There is no build system, no tests, no package manager. The entire codebase is markdown files, JSON configs, and a few Python reference scripts.

## Architecture

### Plugin System
- `marketplace.json` at root registers plugins by name and source path
- Each plugin has a `plugin.json` with name, version, description, author
- Commands are markdown files with YAML frontmatter (`description`, `allowed-tools`, `argument-hint`)
- Skills are directories containing a `SKILL.md` and an optional `references/` folder

### Command → Skill Relationship
Commands (in `commands/`) are the user-facing entry points (invoked as `/log`, `/daily-report`, etc.). Each command's markdown body tells the AI which skill(s) to read before executing. Skills (in `skills/`) contain the deep logic, classification rules, extraction pipelines, and data schemas.

Example chain: `/log` command → reads `intake-chatbot` skill + `project-data` skill → classifies input → enriches with project intelligence → writes to `daily-report-intake.json`.

### Agent System
Agents are autonomous definitions in `agents/` with YAML frontmatter (`name`, `description`) and structured sections (Context, Methodology, Data Sources, Output Format, Constraints). They are auto-discovered from the directory — like commands and skills, no plugin.json registration needed.

| Agent | Role |
|-------|------|
| superintendent-assistant | Top-level router to the 9 specialized agents below |
| data-integrity-watchdog | Validates consistency across all 28 JSON files |
| project-health-monitor | Evaluates 8 KPIs and 5 anomaly detection rules |
| dashboard-intelligence-analyst | Generates dashboard views and executive briefings |
| project-data-navigator | Translates natural language questions to data queries |
| deadline-sentinel | Monitors all deadline sources with 6-tier urgency |
| report-quality-auditor | 10 daily + 6 weekly QA checks on reports |
| field-intelligence-advisor | Contextual briefings for field situations |
| weekly-planning-coordinator | Last Planner System cycle with constraint analysis |
| doc-orchestrator | Coordinates extraction pipelines and validates output |

Agents are read-only — they query the 28-file data store but never modify data without user approval. They consume reference docs from `skills/project-data/references/` for thresholds, query patterns, and validation rules.

### Cowork vs Claude Code Plugins
- The main `foreman-os` plugin (defined in `.claude-plugin/`) works in both Cowork and Claude Code — this includes all skills, commands, and agents
- The 4 dev plugins under `plugins/` are Claude Code-only — they contain hooks that require Claude Code's execution environment
- Do NOT install dev plugins in Cowork — they cause sandbox mount errors

### Key Conventions
- Commands reference skills via `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` — this variable resolves to the repository root at runtime
- Commands also reference cowork platform skills (e.g., `docx`, `pdf`, `construction-takeoff`) for output formatting
- All project data files are JSON, stored in the user's `AI - Project Brain/` folder (or working directory root as fallback)
- The `project-data` skill (`skills/project-data/SKILL.md`) is the central data backbone — nearly every command reads it first

### Data Flow
Documents → `document-intelligence` skill (three-pass extraction) → structured JSON files → consumed by all other commands/skills. The multi-file data store includes 28 JSON files:
- `project-config.json` — master config, folder mapping, document tracking
- `plans-spatial.json` — grid lines, rooms, quantities, site layout
- `specs-quality.json` — spec sections, materials, thresholds, tolerances
- `schedule.json` — milestones, critical path, lookahead history
- `directory.json` — subs, vendors, assignments
- Various `*-log.json` files for RFIs, submittals, procurement, delays, etc.
- `cost-data.json`, `safety-log.json`, `labor-tracking.json`, `quality-data.json`, `daily-report-data.json`, `daily-report-intake.json`, `visual-context.json`, `rendering-log.json`, `drawing-log.json`
- `closeout-data.json`, `risk-register.json`, `claims-log.json`, `environmental-log.json`, `annotation-log.json`

#### Pipeline Reference Documentation
The `project-data` skill has ten reference documents in `skills/project-data/references/`:

**Pipeline architecture (3):**
- **`json-schema-reference.md`** — Complete schema for all 28 JSON files with producer/consumer mapping per field
- **`data-flow-map.md`** — Pipeline architecture with ASCII diagrams: Documents → document-intelligence → JSON store → downstream skills
- **`cross-reference-patterns.md`** — Twelve codified cross-referencing patterns (Sub→Scope→Spec→Inspection, Location→Grid→Area→Room, WorkType→Weather→Threshold, Element→AssemblyChain→MultiSheet, RFI→Submittal→Procurement, Assembly→Schedule→EarnedValue, DualSource→UtilityReconciliation, Risk→Schedule→Cost, Claims→Delay→CO, Environmental→Inspection→Safety, Closeout→Quality→Drawing, Annotation→Drawing→RFI)

**Agent-supporting (4 — consumed by agents for thresholds, queries, and validation):**
- **`alert-thresholds.md`** — KPI thresholds, anomaly detection rules, and severity scoring for project-health-monitor and dashboard-intelligence-analyst agents
- **`data-query-patterns.md`** — 20+ cross-file query patterns (QP-MAT-*, QP-SUB-*, QP-SCH-*, QP-LOC-*, QP-COST-*) with join logic for project-data-navigator
- **`natural-language-query-guide.md`** — Maps superintendent questions to data queries with intent detection and entity recognition
- **`extraction-validation-checklist.md`** — Post-extraction validation checklists for all 3 pipelines, consumed by doc-orchestrator

**Other (3):**
- **`config-schema.md`** — Project configuration schema and field definitions
- **`report-history-schema.md`** — Daily report data structure and history format
- **`skill-detail.md`** — Detailed skill capability mapping

#### Downstream Skill Auto-Population
Eighteen downstream skills have explicit "Project Intelligence Integration" (or "Auto-Population" / "Auto-Linking") sections that tell the AI exactly which JSON files and field paths to read for auto-populating data. This eliminates guesswork — each skill names its data sources:
- `punch-list` — location from plans-spatial, sub from directory, spec cross-ref, drawing ref, schedule impact
- `inspection-tracker` — hold points from specs-quality, weather check, spec deep-link, schedule activity, drawing ref
- `safety-management` — weather alerts from specs-quality, safety zones, utility locations, sub safety performance
- `cost-tracking` — quantity verification from plans-spatial, schedule-cost alignment, CO linkage, procurement tracking
- `labor-tracking` — location from plans-spatial, employer from directory, productivity benchmarking, daily report cross-validation, cost code mapping
- `meeting-minutes` — schedule update, RFI/submittal status, CO status, action item carry-forward, weather + safety summaries
- `change-order-tracker` — schedule impact from schedule.json, cost context from cost-data, spec linking, drawing ref, sub identification
- `intake-chatbot` — spec enrichment, schedule awareness, weather-work cross-check, quantity context, inspection reminders
- `earned-value-management` — budget baseline from cost-data, schedule baseline from schedule.json, actual costs from labor-tracking + procurement-log, earned value from cost-data percent complete, CO adjustments, forecast validation against delay-log
- `rfi-preparer` — location from plans-spatial, drawing refs from sheet_cross_references, spec section from specs-quality, team routing from directory, numbering from rfi-log, related items cross-ref
- `quality-management` — spec-based checklists from specs-quality, hold points, location from plans-spatial, sub QC contact from directory, FPIR trends from quality-data, drawing refs
- `risk-management` — schedule risks from schedule.json critical path/float, weather thresholds from specs-quality, sub performance from directory + quality-data, contingency context from cost-data, delay patterns from delay-log, procurement risks from procurement-log
- `last-planner` — activity pool from schedule.json, sub availability from directory + labor-tracking, location constraints from plans-spatial, weather from specs-quality thresholds, material readiness from procurement-log, prerequisite inspections from specs-quality hold points + inspection-log
- `sub-performance` — sub roster from directory, schedule adherence from daily-report-data + schedule.json + labor-tracking, quality from inspection-log + quality-data + punch-list, safety from safety-log, responsiveness from rfi-log + submittal-log, productivity from labor-tracking
- `delay-tracker` — critical path impact from schedule.json, weather verification from specs-quality thresholds + daily-report-data, cost impact from cost-data + labor-tracking, related delays from delay-log, float analysis from schedule.json
- `look-ahead-planner` — activity extraction from schedule.json, predecessor tracking, sub mobilization from directory, material delivery from procurement-log, inspection prerequisites from specs-quality hold points + inspection-log, weather restrictions from specs-quality thresholds
- `report-qa` — punch list cross-check from punch-list.json, cost authorization from change-order-log, procurement verification from procurement-log, quality correlation from quality-data, safety incident cross-check from safety-log, schedule milestone validation from schedule.json, weather threshold verification from specs-quality
- `submittal-intelligence` — procurement lead time from procurement-log, sub contact from directory, hold point linking from specs-quality, cost impact from cost-data, quality test correlation from quality-data, installation verification from daily-report-data
- `closeout-commissioning` — warranty tracking from quality-data warranties, commissioning test results from quality-data system_tests, O&M manual completeness from quality-data equipment_data, as-built drawing status from plans-spatial as_built_overlay
- `drawing-control` — as-built markup status per sheet in drawing-log, deviation cross-reference against rfi-log and change-order-log, closeout completeness flagging, links to as-built-extraction.md
- `quality-management` — material test result verification from quality-data test_results (concrete, steel, soil, welding), specimen traceability against procurement-log delivery_tickets

### Python Reference Scripts and Executable Scripts
Five Python files exist under `skills/document-intelligence/references/` and `skills/quantitative-intelligence/references/` — these are reference implementations for visual plan analysis, sheet cross-referencing, and calculation bridging. They are not executed directly by the plugin but serve as reference code for the AI.

The `skills/quantitative-intelligence/references/calculation-workflow.md` documents how downstream skills should request calculations from the 10 calculator classes (ConcreteVolumeCalc, WallAreaCalc, RoomAreaCalc, PipeRunCalc, FootingCalc, SlabCalc, RoofCalc, PEMBCalc, SymbolCountCalc, AggregateCalc), including source priority levels and confidence scoring.

The `skills/dwg-extraction/scripts/` directory contains executable scripts that ARE run directly:
- `compile_libredwg.sh` — Compiles the libredwg C library from GitHub source (cached at `/tmp/libredwg/dwg2dxf`)
- `parse_dxf.py` — Custom DXF entity parser that handles Civil 3D XDATA patterns, INSERT+ATTRIB sequences, and proximity-based structure grouping

## Editing Patterns

When adding a **new command**: create a markdown file in `commands/` with YAML frontmatter (`description`, `allowed-tools`, `argument-hint`) and step-by-step instructions that reference the relevant skills.

When adding a **new skill**: create a directory under `skills/<skill-name>/` with a `SKILL.md` (YAML frontmatter with `name`, `description`, `version`) and optionally a `references/` folder for supporting docs or scripts.

When adding a **new agent**: create a markdown file in `agents/` with YAML frontmatter (`name`, `description`) and structured sections (Context, Methodology, Data Sources, Output Format, Constraints). Agents are auto-discovered from the directory — no plugin.json registration needed.

When modifying the **plugin manifest**: update both `marketplace.json` and `plugin.json` (both in `.claude-plugin/`) if the description or metadata changes.
