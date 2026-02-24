---
description: Cross-discipline conflict detection and resolution tracking
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [scan|status|resolve|history]
---

# Conflict Detection Command

## Overview

Detect, track, and resolve cross-discipline conflicts across your project's extracted document data. Compares plans vs. specs, specs vs. schedule, drawing vs. drawing, cost vs. scope, and dual-source data to catch discrepancies before they become expensive field problems.

## Skills Referenced
- `${CLAUDE_PLUGIN_ROOT}/skills/document-intelligence/references/conflict-detection-rules.md` — 25 codified detection rules (CDR-01 through CDR-25) with field paths, tolerances, and severity classifications
- `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md` — Project data access and JSON file locations
- `${CLAUDE_PLUGIN_ROOT}/skills/project-data/references/cross-reference-patterns.md` — 7 cross-reference patterns for data chain validation

## Agent Delegation

This command delegates its core detection logic to the **conflict-detection-agent** (defined in `${CLAUDE_PLUGIN_ROOT}/agents/conflict-detection-agent.md`). Read the agent definition to understand its 7-step methodology, data sources, and output format before executing.

## Execution Steps

### Step 1: Load Project Configuration

Search for project-data files in the user's working directory (check `AI - Project Brain/` first, then root):
- `project-config.json` (documents_loaded, version_history, conflict_log)
- `plans-spatial.json` (dimensions, material zones, MEP systems, quantities)
- `specs-quality.json` (spec sections, tolerances, weather thresholds, hold points)
- `schedule.json` (activities, durations, critical path, float)
- `cost-data.json` (budget lines, earned value, contingency)
- `directory.json` (sub scopes, assignments)
- `procurement-log.json` (lead times, delivery dates)
- `change-order-log.json` (scope, cost, schedule impact)
- `drawing-log.json` (revisions, ASIs)
- `rfi-log.json` (open RFIs that may address known conflicts)

If no project config: "No project set up yet. Run `/set-project` first."

If fewer than 2 document types have been processed (check `documents_loaded`): "Need at least 2 document types processed to detect conflicts. Run `/process-docs` with plans and specs first."

### Step 2: Parse Arguments for Sub-Action

Examine `$ARGUMENTS` to determine which operation:
- **"scan"** or no argument — Run full conflict detection scan
- **"status"** — Show current conflict inventory
- **"resolve [ID]"** — Mark a conflict as resolved
- **"history"** — Show resolved conflicts

If no sub-action provided, default to **scan**.

### Step 3: Execute Sub-Action

#### `/conflicts scan` (default)

Invoke the **conflict-detection-agent** with access to all loaded project data files. The agent runs its 7-step methodology:

1. Plan vs. Specification conflicts (CDR-05 through CDR-10)
2. Specification vs. Schedule conflicts (CDR-14 through CDR-17)
3. Drawing vs. Drawing conflicts (CDR-01 through CDR-04, CDR-21 through CDR-23)
4. Cost vs. Scope conflicts (CDR-18 through CDR-20)
5. Dual-Source conflicts (CDR-24, CDR-25)
6. Temporal/Revision conflicts
7. Categorize and prioritize

**After the agent returns**, present the conflict report to the user and:
- Save any **new** conflicts to `project-config.json → conflict_log[]`
- Skip conflicts that already exist in the log (match by category + source fields)
- Note which conflicts are new vs. previously identified

**Conflict log entry schema**:
```json
{
  "id": "CONF-001",
  "rule_id": "CDR-08",
  "category": "Equipment Capacity",
  "severity": "MAJOR",
  "source_a": "plans-spatial.json → mep_systems.mechanical.equipment[RTU-1].cooling.tons = 5",
  "source_b": "specs-quality.json → spec_sections[23 81 00].equipment_requirements.minimum_tons = 7.5",
  "description": "RTU-1 capacity on plan (5 ton) is below spec minimum (7.5 ton)",
  "detected_date": "2026-02-24",
  "status": "open",
  "resolution": null,
  "resolved_date": null,
  "resolved_by": null,
  "related_rfi": null
}
```

#### `/conflicts status`

Read `project-config.json → conflict_log[]` and display:

```
Conflict Status — {project_name}

Open: X conflicts (C critical, M major, N minor)
Resolved: Y conflicts
Accepted: Z conflicts (superintendent accepted risk)

OPEN CONFLICTS:
| ID | Severity | Category | Description | Age |
|----|----------|----------|-------------|-----|
| CONF-001 | CRITICAL | Pipe Sizing | 8" storm vs 6" PVC | 3 days |
| CONF-002 | MAJOR | Equipment | RTU-1 undersized | 5 days |
| ... | ... | ... | ... | ... |

Aging alerts:
- X critical conflicts open > 2 days
- Y major conflicts open > 5 days
```

#### `/conflicts resolve [ID]`

Prompt the user for resolution details:

1. **Resolution method**: RFI issued, ASI received, field-verified correct, superintendent decision, design team clarification, addendum supersedes
2. **Resolution notes**: Free text describing the resolution
3. **Resolved by**: Name or role

Update the conflict entry in `project-config.json → conflict_log[]`:
```json
{
  "status": "resolved",
  "resolution": "ASI-003 issued Feb 24 — spec corrected to match plan. 5-ton RTU confirmed adequate for space cooling load.",
  "resolved_date": "2026-02-24",
  "resolved_by": "Superintendent"
}
```

Also log the resolution to `project-config.json → version_history[]` for audit trail.

#### `/conflicts history`

Read `project-config.json → conflict_log[]` where status is "resolved" or "accepted" and display:

```
Conflict Resolution History — {project_name}

| ID | Category | Resolution | Method | Resolved | By |
|----|----------|-----------|--------|----------|-----|
| CONF-003 | Dimensional | RFI-012 clarified | RFI | Feb 20 | PM |
| CONF-001 | Pipe Sizing | ASI-003 corrected | ASI | Feb 24 | Super |
| ... | ... | ... | ... | ... | ... |

Summary:
- Total resolved: X
- By RFI: Y
- By ASI: Z
- By field verification: W
- Average resolution time: N days
```

### Step 4: Summary and Next Steps

After any sub-action, suggest relevant follow-up actions:
- After **scan**: "Use `/conflicts resolve CONF-XXX` to mark resolved conflicts. Critical conflicts should be addressed before today's work proceeds."
- After **status**: "Run `/conflicts scan` to check for new conflicts, or `/conflicts resolve [ID]` to update resolutions."
- After **resolve**: "Conflict resolved. Run `/conflicts status` to see remaining open items."
- After **history**: "Run `/conflicts scan` to check for any new conflicts since the last scan."
