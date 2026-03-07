# Codebase Structure

**Analysis Date:** 2026-03-06

## Directory Layout

```
foreman-os/                              # Plugin marketplace root
├── .claude-plugin/
│   └── marketplace.json                 # Marketplace registry (7 plugins)
├── .claude/
│   └── settings.local.json              # Claude Code permissions
├── .planning/
│   └── codebase/                        # Architecture/analysis docs
├── foremanos-core/                      # Plugin: Project backbone (install first)
│   ├── .claude-plugin/plugin.json       # Plugin manifest v5.0.0
│   ├── commands/                        # 7 commands
│   ├── skills/                          # 6 skills (all canonical)
│   └── agents/                          # 4 agents (incl. superintendent-assistant)
├── foremanos-intel/                     # Plugin: Document extraction & intelligence
│   ├── .claude-plugin/plugin.json       # Plugin manifest
│   ├── commands/                        # 2 commands
│   ├── skills/                          # 4 full + 1 stub
│   ├── agents/                          # 3 agents
│   └── hooks/                           # 4 Node.js hooks (Claude Code only)
├── foremanos-field/                     # Plugin: Daily field operations
│   ├── .claude-plugin/plugin.json
│   ├── commands/                        # 8 commands
│   ├── skills/                          # 10 full + 1 stub
│   └── agents/                          # 2 agents
├── foremanos-planning/                  # Plugin: Scheduling & look-aheads
│   ├── .claude-plugin/plugin.json
│   ├── commands/                        # 6 commands
│   ├── skills/                          # 5 full + 4 stubs
│   └── agents/                          # 2 agents
├── foremanos-doccontrol/                # Plugin: RFIs, submittals, drawings
│   ├── .claude-plugin/plugin.json
│   ├── commands/                        # 5 commands
│   └── skills/                          # 5 full + 2 stubs
├── foremanos-cost/                      # Plugin: Budget, earned value, pay apps
│   ├── .claude-plugin/plugin.json
│   ├── commands/                        # 6 commands
│   └── skills/                          # 7 full + 2 stubs
├── foremanos-compliance/                # Plugin: Risk, environmental, closeout
│   ├── .claude-plugin/plugin.json
│   ├── commands/                        # 6 commands (incl. data-health)
│   └── skills/                          # 5 full + 3 stubs
├── plugins/                             # Dev plugins (Claude Code only, NOT in marketplace)
│   ├── foremanos-stack/                 # Prisma, NextAuth, Redis, SWR, Trigger.dev
│   │   ├── plugin.json
│   │   └── skills/                      # 5 skills
│   ├── foremanos-llm/                   # LLM orchestration, vision, RAG
│   │   ├── plugin.json
│   │   ├── skills/                      # 4 skills
│   │   └── agents/                      # 1 agent
│   ├── foremanos-testing/               # Vitest, API route testing
│   │   ├── plugin.json
│   │   ├── skills/                      # 2 skills
│   │   └── commands/                    # 1 command
│   └── foremanos-documents/             # PDF, Office, R2 file storage
│       ├── plugin.json
│       └── skills/                      # 3 skills
├── sync-stubs.sh                        # Stub synchronization script
├── CLAUDE.md                            # Project instructions for Claude
└── README.md                            # Repository documentation
```

## Directory Purposes

**foremanos-core/:**
- Purpose: Project backbone — setup, data browsing, dashboards, briefings, rendering
- Contains: 7 commands, 6 skills (all canonical — no stubs here), 4 agents, 11 reference docs
- Key files:
  - `commands/set-project.md`: Project initialization entry point
  - `commands/data.md`: HTML data dashboard generator
  - `commands/morning-brief.md`: Daily briefing command
  - `commands/foremanos.md`: System overview command
  - `skills/project-data/SKILL.md`: Central data backbone (360 lines) — canonical source for the most-used stub
  - `skills/project-data/references/json-schema-reference.md`: Complete schema for all 28 JSON files
  - `skills/project-data/references/data-flow-map.md`: Pipeline architecture with ASCII diagrams
  - `skills/project-data/references/cross-reference-patterns.md`: 12 cross-referencing patterns
  - `agents/superintendent-assistant.md`: Top-level meta-agent that routes all requests

**foremanos-intel/:**
- Purpose: Document intelligence, extraction pipelines, DWG parsing, quantity takeoffs
- Contains: 2 commands, 5 skills (4 full + 1 stub), 3 agents, 4 hooks, 30+ reference docs, Python scripts
- Key files:
  - `commands/process-docs.md`: Primary document extraction entry point
  - `commands/process-dwg.md`: DWG/DXF extraction entry point
  - `skills/document-intelligence/SKILL.md`: Core extraction engine (1084 lines)
  - `skills/document-intelligence/references/`: 30 extraction templates and reference docs
  - `skills/dwg-extraction/scripts/parse_dxf.py`: Executable DXF parser
  - `skills/dwg-extraction/scripts/compile_libredwg.sh`: LibreDWG compiler script
  - `hooks/data-loss-guard.js`: PreToolUse Write hook — warns on JSON array shrinkage
  - `hooks/extraction-checkpoint.js`: Extraction operation guard
  - `hooks/counter-reconciler.js`: Count consistency validator
  - `hooks/project-brain-validator.js`: Data integrity validator
  - `agents/doc-orchestrator.md`: Extraction pipeline coordinator
  - `agents/data-integrity-watchdog.md`: Cross-file consistency validator
  - `agents/conflict-detection-agent.md`: Cross-discipline conflict scanner

**foremanos-field/:**
- Purpose: Daily reporting, safety, quality, inspections, labor, punch lists
- Contains: 8 commands, 11 skills (10 full + 1 stub), 2 agents
- Key files:
  - `commands/log.md`: Primary field observation entry point
  - `commands/daily-report.md`: Report generation
  - `skills/intake-chatbot/SKILL.md`: Natural language field input classifier
  - `skills/field-reference/`: Contains 21 trade-specific field guides in `references/`
  - `skills/report-qa/SKILL.md`: Report quality auditing (canonical — stubbed to planning)

**foremanos-planning/:**
- Purpose: Scheduling, look-aheads, Last Planner System, weekly reports, material tracking
- Contains: 6 commands, 9 skills (5 full + 4 stubs), 2 agents
- Key files:
  - `commands/look-ahead.md`: 3-week lookahead generation
  - `commands/weekly-report.md`: Weekly report generation
  - `skills/last-planner/SKILL.md`: Last Planner System methodology
  - `agents/weekly-planning-coordinator.md`: Last Planner cycle coordinator
  - `agents/deadline-sentinel.md`: 6-tier deadline urgency monitor

**foremanos-doccontrol/:**
- Purpose: RFI preparation, submittal reviews, drawing control, annotations, BIM
- Contains: 5 commands, 7 skills (5 full + 2 stubs), no agents
- Key files:
  - `commands/prepare-rfi.md`: RFI creation workflow
  - `commands/submittal-review.md`: Submittal review workflow
  - `skills/submittal-intelligence/SKILL.md`: Submittal tracking (canonical — stubbed to planning)

**foremanos-cost/:**
- Purpose: Cost tracking, earned value management, pay applications, change orders, delays, claims
- Contains: 6 commands, 9 skills (7 full + 2 stubs), no agents
- Key files:
  - `commands/evm.md`: Earned value management
  - `commands/pay-app.md`: Payment application processing
  - `skills/delay-tracker/SKILL.md`: Delay event tracking (canonical — stubbed to compliance)

**foremanos-compliance/:**
- Purpose: Risk registers, environmental compliance, closeout, commissioning, sub scorecards
- Contains: 6 commands, 8 skills (5 full + 3 stubs), no agents
- Key files:
  - `commands/data-health.md`: Data integrity health check
  - `commands/closeout.md`: Project closeout workflow
  - `skills/closeout-commissioning/SKILL.md`: Closeout and commissioning methodology

**plugins/:**
- Purpose: Claude Code-only dev plugins for ForemanOS web app development patterns
- Contains: 4 sub-plugins with 14 skills, 1 agent, 1 command total
- Key files:
  - `foremanos-stack/skills/prisma-patterns/SKILL.md`: Prisma 6.7 patterns
  - `foremanos-stack/skills/nextauth-rbac/SKILL.md`: NextAuth v5 RBAC patterns
  - `foremanos-llm/skills/rag-system/SKILL.md`: RAG system patterns
  - `foremanos-testing/skills/vitest-patterns/SKILL.md`: Vitest testing patterns

## Key File Locations

**Entry Points:**
- `foremanos-core/commands/set-project.md`: First command to run on any project
- `foremanos-core/commands/foremanos.md`: System overview and help
- `foremanos-intel/commands/process-docs.md`: Document extraction pipeline
- `foremanos-core/agents/superintendent-assistant.md`: Natural language entry via meta-agent

**Configuration:**
- `.claude-plugin/marketplace.json`: Marketplace plugin registry
- `<plugin>/.claude-plugin/plugin.json`: Individual plugin manifests
- `.claude/settings.local.json`: Claude Code permissions
- `CLAUDE.md`: Project-level Claude instructions (26K lines — comprehensive)

**Core Logic:**
- `foremanos-core/skills/project-data/SKILL.md`: Data backbone (360 lines)
- `foremanos-intel/skills/document-intelligence/SKILL.md`: Extraction engine (1084 lines)
- `foremanos-core/skills/project-data/references/json-schema-reference.md`: All 28 JSON schemas
- `foremanos-core/skills/project-data/references/cross-reference-patterns.md`: 12 cross-ref patterns
- `foremanos-field/skills/intake-chatbot/SKILL.md`: Field input NLP classifier

**Safety & Hooks:**
- `foremanos-intel/hooks/data-loss-guard.js`: Array shrinkage warning
- `foremanos-intel/hooks/extraction-checkpoint.js`: Extraction guard
- `foremanos-intel/hooks/counter-reconciler.js`: Count consistency
- `foremanos-intel/hooks/project-brain-validator.js`: Data integrity

**Stub Sync:**
- `sync-stubs.sh`: Propagates canonical SKILL.md changes to all stub consumers

## Naming Conventions

**Files:**
- Commands: `kebab-case.md` (e.g., `set-project.md`, `daily-report.md`, `prepare-rfi.md`)
- Skills: Directory named `kebab-case/` containing `SKILL.md` (uppercase) (e.g., `project-data/SKILL.md`)
- Agents: `kebab-case.md` (e.g., `superintendent-assistant.md`, `doc-orchestrator.md`)
- Plugin manifests: Always `plugin.json`
- Hooks: `kebab-case.js` (e.g., `data-loss-guard.js`)
- Reference docs: `kebab-case.md` or `snake_case.py` (e.g., `cross-reference-patterns.md`, `visual_plan_analyzer.py`)

**Directories:**
- Plugins: `foremanos-<domain>` (e.g., `foremanos-core`, `foremanos-field`)
- Dev plugins: `foremanos-<concern>` under `plugins/` (e.g., `foremanos-stack`, `foremanos-llm`)
- Skills: `kebab-case` (e.g., `project-data`, `intake-chatbot`, `earned-value-management`)
- Standard directories: `commands/`, `skills/`, `agents/`, `hooks/`, `references/`

**YAML Frontmatter:**
- Commands: `description`, `allowed-tools`, `argument-hint`
- Skills: `name`, `description`, `version`
- Agents: `name`, `description`

## Where to Add New Code

**New Command:**
- Place in `<plugin>/commands/<command-name>.md`
- Must have YAML frontmatter with `description`, `allowed-tools`, `argument-hint`
- Reference skills via `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md`
- All skill references must resolve within the same plugin — use stubs for cross-plugin needs
- Auto-discovered from directory — no registration needed

**New Skill:**
- Create directory `<plugin>/skills/<skill-name>/`
- Create `SKILL.md` with YAML frontmatter (`name`, `description`, `version`)
- Optionally add `references/` subdirectory for supporting docs
- If consumed by commands in other plugins, add stub mapping to `sync-stubs.sh` and run it

**New Agent:**
- Place in `<plugin>/agents/<agent-name>.md`
- Must have YAML frontmatter with `name`, `description`
- Must have structured sections: Context, Methodology, Data Sources, Output Format, Constraints
- NEVER copy agents between plugins — use stubs, soft refs, or inlined methodology
- Auto-discovered from directory — no registration needed

**New Hook:**
- Place in `<plugin>/hooks/<hook-name>.js`
- Node.js script that reads from stdin, writes to stdout (pass-through), warnings to stderr
- Currently only `foremanos-intel/hooks/` has hooks
- Must be registered in Claude Code settings (not auto-discovered)

**New Reference Document:**
- Place in `<plugin>/skills/<skill-name>/references/<doc-name>.md`
- Referenced by the parent SKILL.md
- Not included in stubs (stubs copy SKILL.md only, not references/)

**New Marketplace Plugin:**
- Create `foremanos-<domain>/` directory at repo root
- Create `.claude-plugin/plugin.json` with name, version, description, author
- Create `commands/`, `skills/`, optionally `agents/` directories
- Add entry to `.claude-plugin/marketplace.json`
- For dev-only plugins: place under `plugins/` and do NOT add to marketplace.json

**New Cross-Plugin Dependency:**
1. Prefer adding a stub: update `sync-stubs.sh` with new mapping, run script
2. For optional deps: use soft ref text in the command ("If foremanos-intel is installed...")
3. For agent-like behavior: inline key methodology directly in the command markdown

## Special Directories

**`AI - Project Brain/` (external):**
- Purpose: Per-project JSON data store (28 files)
- Generated: Yes, by `/set-project` command
- Committed: No — lives in user's project folder, outside this repo
- Critical: All commands read/write here; path stored in `project-config.json` → `folder_mapping.ai_output`

**`.claude-plugin/` (root):**
- Purpose: Marketplace registry
- Generated: No
- Committed: Yes

**`<plugin>/.claude-plugin/`:**
- Purpose: Individual plugin manifest
- Generated: No
- Committed: Yes

**`<plugin>/skills/<skill>/references/`:**
- Purpose: Deep reference material for a skill (extraction templates, query patterns, Python scripts)
- Generated: No
- Committed: Yes
- Note: NOT included when creating stubs — stubs are SKILL.md only

**`foremanos-intel/skills/dwg-extraction/scripts/`:**
- Purpose: Executable scripts (Python, Bash) for DWG/DXF processing
- Generated: No (source code)
- Committed: Yes
- Note: These ARE run directly, unlike reference Python scripts which are read-only context

**`~/foreman-os-venv/` (external):**
- Purpose: Python virtual environment for executable scripts
- Generated: Yes, manually
- Committed: No — kept outside repo to avoid Cowork sandbox copier issues

## Totals

| Category | Count |
|----------|-------|
| Marketplace plugins | 7 |
| Dev plugins (Claude Code only) | 4 |
| Commands | 41 (marketplace) + 1 (dev) = 42 |
| Full skills | 43 (marketplace) + 14 (dev) = 57 |
| Stub skills | 13 |
| Agents | 11 (marketplace) + 1 (dev) = 12 |
| Hooks | 4 (all in foremanos-intel) |
| Reference docs | 40+ (intel: 30, core: 11, others: various) |
| JSON data files | 28 (per project, external) |

---

*Structure analysis: 2026-03-06*
