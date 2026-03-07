# Architecture

**Analysis Date:** 2026-03-06

## Pattern Overview

**Overall:** Modular Plugin Marketplace — a collection of 7 self-contained Cowork/Claude Code plugins (plus 4 Claude Code-only dev plugins), organized as a local plugin marketplace. No build system, no runtime application code, no package manager. The entire codebase is markdown files, JSON configs, shell scripts, and reference Python scripts.

**Key Characteristics:**
- Each of the 7 marketplace plugins is fully self-contained — all `${CLAUDE_PLUGIN_ROOT}` paths resolve within the plugin's own directory tree
- Cross-plugin dependencies are handled via stub SKILL.md files (copied by `sync-stubs.sh`), soft references, or inlined methodology — never hard cross-plugin paths
- The system is an AI-native architecture: commands (markdown) instruct AI agents to read skills (markdown) and operate on a shared JSON data store (28 files in the user's `AI - Project Brain/` folder)
- Zero executable application code — the "runtime" is the AI (Claude) interpreting markdown instructions

## Layers

**Layer 1 — Marketplace Registry:**
- Purpose: Registers plugins for installation in Cowork
- Location: `.claude-plugin/marketplace.json`
- Contains: Plugin name-to-source-path mappings for the 7 marketplace plugins
- Depends on: Nothing
- Used by: Cowork plugin installer

**Layer 2 — Plugin Manifests:**
- Purpose: Declare plugin identity, version, and metadata
- Location: `<plugin>/.claude-plugin/plugin.json` (marketplace plugins) or `plugins/<plugin>/plugin.json` (dev plugins)
- Contains: name, version, description, author; dev plugins also list skills explicitly
- Depends on: Nothing
- Used by: Cowork/Claude Code plugin loader

**Layer 3 — Commands (User-Facing Entry Points):**
- Purpose: Define user-invocable slash commands with step-by-step AI instructions
- Location: `<plugin>/commands/*.md` (41 total across all plugins)
- Contains: YAML frontmatter (description, allowed-tools, argument-hint) + markdown body with procedural steps
- Depends on: Skills (via `${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md` references), project data JSON files
- Used by: Users via `/command-name` invocation

**Layer 4 — Skills (Domain Knowledge):**
- Purpose: Encode deep domain logic, classification rules, extraction pipelines, data schemas, and cross-reference patterns
- Location: `<plugin>/skills/<skill-name>/SKILL.md` + optional `references/` folder (70 SKILL.md files: 43 full + 13 stubs + 14 dev plugin skills)
- Contains: YAML frontmatter (name, description, version) + methodology, rules, schemas, integration points
- Depends on: Reference documents in `references/` subdirectories; project data JSON files
- Used by: Commands (which tell the AI to read specific skills before executing)

**Layer 5 — Agents (Autonomous Specialists):**
- Purpose: Provide specialized autonomous behavior for complex, multi-step reasoning tasks
- Location: `<plugin>/agents/*.md` (13 agent files across 4 plugins: core, intel, field, planning)
- Contains: YAML frontmatter (name, description) + structured sections (Context, Methodology, Data Sources, Output Format, Constraints)
- Depends on: Skills, reference documents, project data JSON files
- Used by: Commands (via delegation), the superintendent-assistant meta-agent (via routing)

**Layer 6 — Hooks (Claude Code Runtime Guards):**
- Purpose: Provide runtime safety checks during AI tool use
- Location: `foremanos-intel/hooks/` (4 hooks)
- Contains: Node.js scripts that intercept PreToolUse events
- Depends on: Claude Code hook system, project data JSON files on disk
- Used by: Claude Code runtime (auto-triggered on Write operations to JSON files)

**Layer 7 — Reference Documents & Scripts:**
- Purpose: Provide deep reference material, extraction templates, calculation implementations
- Location: `<plugin>/skills/<skill-name>/references/` (30+ reference docs in intel alone, 11 in core project-data)
- Contains: Markdown extraction templates, Python reference implementations, validation checklists, query patterns
- Depends on: Nothing
- Used by: Skills and agents (read as context during AI execution)

**Layer 8 — Project Data Store (External):**
- Purpose: Persistent structured data for a specific construction project
- Location: User's `AI - Project Brain/` folder (outside this repo)
- Contains: 28 JSON files covering all project dimensions
- Depends on: Document extraction via `/process-docs` command
- Used by: Every command and agent reads/writes to this store

## Data Flow

**Document Extraction Pipeline:**

1. User runs `/set-project` (foremanos-core) → scans folder structure, creates empty JSON files in `AI - Project Brain/`
2. User runs `/process-docs` (foremanos-intel) → reads `document-intelligence` skill (1084 lines) → extracts structured data from PDFs/drawings
3. Extraction populates `plans-spatial.json`, `specs-quality.json`, `schedule.json`, `directory.json` with project intelligence
4. All downstream commands auto-populate from these files via "Project Intelligence Integration" sections in 20+ skills

**Daily Field Operations Flow:**

1. User runs `/log "Walker had 6 guys doing backfill"` (foremanos-field)
2. Command reads `intake-chatbot` skill + `project-data` skill (stub)
3. AI classifies input, enriches with sub names from `directory.json`, locations from `plans-spatial.json`, spec references from `specs-quality.json`
4. Structured entry appended to `daily-report-intake.json`
5. User runs `/daily-report` → aggregates intake entries into formal report → writes to `daily-report-data.json`

**Agent Routing Flow:**

1. User speaks naturally to the `superintendent-assistant` agent (foremanos-core)
2. Agent parses intent against routing table (core agents) and command table (other plugins)
3. Simple lookups (single field, single file) handled directly
4. Complex queries delegated to specialized agents: `project-data-navigator`, `dashboard-intelligence-analyst`, `project-health-monitor`
5. Cross-plugin needs generate command guidance: "Use `/daily-report` for field reporting — requires foremanos-field"

**Stub Sync Flow:**

1. Developer edits a canonical SKILL.md (e.g., `foremanos-core/skills/project-data/SKILL.md`)
2. Developer runs `./sync-stubs.sh` from repo root
3. Script copies SKILL.md (with stub header comment) to all consumer plugins
4. 7 canonical-to-consumer mappings propagate to 13 stub files total

**State Management:**
- All state lives in the 28 JSON files in the user's `AI - Project Brain/` folder
- No in-memory state between command invocations — every command re-reads from disk
- `project-config.json` is the master config with `version_history` tracking all changes
- A `CLAUDE.md` file is generated at the project root as session-start context for Claude

## Key Abstractions

**Command:**
- Purpose: User-facing entry point that orchestrates AI behavior via markdown instructions
- Examples: `foremanos-core/commands/set-project.md`, `foremanos-field/commands/log.md`, `foremanos-cost/commands/evm.md`
- Pattern: YAML frontmatter + step-by-step procedural instructions that reference skills and data files

**Skill:**
- Purpose: Encapsulates domain knowledge, classification rules, and data schemas
- Examples: `foremanos-core/skills/project-data/SKILL.md` (360 lines), `foremanos-intel/skills/document-intelligence/SKILL.md` (1084 lines)
- Pattern: YAML frontmatter + methodology sections, often with "Project Intelligence Integration" sections listing exact JSON file paths and field paths

**Stub:**
- Purpose: Read-only copy of a SKILL.md that lets commands in one plugin reference methodology from another
- Examples: `foremanos-field/skills/project-data/SKILL.md` (stub of core's project-data), `foremanos-cost/skills/estimating-intelligence/SKILL.md` (stub of intel's)
- Pattern: Header comment `<!-- STUB: Canonical source is ... -->` + full SKILL.md content, no `references/` folder

**Agent:**
- Purpose: Autonomous specialist for multi-step reasoning and decision-making
- Examples: `foremanos-core/agents/superintendent-assistant.md` (meta-router), `foremanos-intel/agents/doc-orchestrator.md` (extraction coordinator)
- Pattern: YAML frontmatter + Context, Methodology, Data Sources, Output Format, Constraints sections

**Reference Document:**
- Purpose: Deep supporting material for skills — extraction templates, query patterns, validation rules
- Examples: `foremanos-core/skills/project-data/references/cross-reference-patterns.md`, `foremanos-intel/skills/document-intelligence/references/plans-deep-extraction.md`
- Pattern: Detailed markdown with schemas, examples, and decision trees

## Entry Points

**User Entry (Slash Commands):**
- Location: `<plugin>/commands/*.md` (41 commands total)
- Triggers: User types `/command-name` in Cowork or Claude Code
- Responsibilities: Load context, read skills, execute steps, write to data store

**Meta-Agent Entry:**
- Location: `foremanos-core/agents/superintendent-assistant.md`
- Triggers: Natural language conversation (not a slash command)
- Responsibilities: Intent classification, routing to appropriate command or agent, direct lookup for simple queries

**Setup Entry:**
- Location: `foremanos-core/commands/set-project.md`
- Triggers: First use on a new project folder via `/set-project`
- Responsibilities: Folder scanning, project config creation, 28 JSON file initialization, CLAUDE.md generation

**Extraction Entry:**
- Location: `foremanos-intel/commands/process-docs.md`
- Triggers: `/process-docs` after project setup
- Responsibilities: Document ingestion, extraction pipeline execution, JSON data store population

## Error Handling

**Strategy:** Graceful degradation with user guidance

**Patterns:**
- Missing data files: Commands check for file existence, report what is missing, and name the command that creates the missing data (e.g., "No project is set up yet. Run `/set-project` first.")
- Missing plugins: Commands use soft references for cross-plugin needs ("If the foremanos-intel plugin is installed, the doc-orchestrator agent can validate extraction output.")
- Data loss prevention: `foremanos-intel/hooks/data-loss-guard.js` — PreToolUse hook on Write operations that warns (to stderr) when top-level arrays in `AI - Project Brain/` JSON files shrink or disappear. Never blocks writes.
- Extraction checkpoint: `foremanos-intel/hooks/extraction-checkpoint.js` — guards extraction operations
- Counter reconciliation: `foremanos-intel/hooks/counter-reconciler.js` — validates count consistency
- Project brain validation: `foremanos-intel/hooks/project-brain-validator.js` — validates data integrity

## Cross-Cutting Concerns

**Logging:** `project-config.json` → `version_history` array records timestamped changes from every command (`[TIMESTAMP] | command | action | details`)

**Validation:** Data integrity enforced by 4 hooks in `foremanos-intel/hooks/`, the `data-integrity-watchdog` agent, and extraction validation checklists in `foremanos-core/skills/project-data/references/extraction-validation-checklist.md`

**Authentication:** Not applicable — this is a plugin marketplace, not a web application. The Cowork/Claude Code runtime handles user identity.

**Cross-Referencing:** 12 codified cross-reference patterns in `foremanos-core/skills/project-data/references/cross-reference-patterns.md` define how data connects across the 28 JSON files (Sub->Scope->Spec->Inspection, Location->Grid->Area->Room, etc.)

**Claims Mode:** A `claims_mode` flag in `project-config.json` activates enhanced documentation rigor across all commands — extra timestamp precision, contemporaneous records emphasis, delay impact tracking

## Plugin Dependency Graph

```
foremanos-core (backbone — install first)
  └─ project-data skill ──stub──> intel, field, planning, doccontrol, cost, compliance

foremanos-intel (extraction engine)
  ├─ document-intelligence skill ──stub──> doccontrol, compliance
  ├─ estimating-intelligence skill ──stub──> cost
  └─ quantitative-intelligence skill ──stub──> planning

foremanos-field (daily operations)
  └─ report-qa skill ──stub──> planning

foremanos-doccontrol (document control)
  └─ submittal-intelligence skill ──stub──> planning

foremanos-cost (financial tracking)
  └─ delay-tracker skill ──stub──> compliance

foremanos-planning (scheduling) — receives 4 stubs, produces none
foremanos-compliance (risk/closeout) — receives 3 stubs, produces none
```

## Dev Plugins (Claude Code Only)

Four plugins under `plugins/` provide development patterns for the ForemanOS web application (Next.js 15.5 + Prisma 6.7). These are NOT part of the marketplace and must NOT be installed in Cowork.

- `plugins/foremanos-stack/` — Prisma, NextAuth RBAC, Redis, SWR, Trigger.dev patterns (5 skills)
- `plugins/foremanos-llm/` — LLM orchestration, vision, RAG, prompt patterns (4 skills + 1 agent)
- `plugins/foremanos-testing/` — Vitest, API route testing patterns (2 skills + 1 command)
- `plugins/foremanos-documents/` — PDF generation, Office docs, R2 file storage patterns (3 skills)

---

*Architecture analysis: 2026-03-06*
