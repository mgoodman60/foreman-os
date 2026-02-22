# Data Flow Map — Foreman OS Extraction Pipeline

Architectural documentation of the full data extraction and consumption pipeline.

---

## Pipeline Overview

```
                          ┌─────────────────────────────────┐
                          │      SOURCE DOCUMENTS            │
                          │  Plans  Specs  Schedules  Misc   │
                          └──────────────┬──────────────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                     │
                    ▼                    ▼                     ▼
          ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐
          │  document-       │  │  dwg-extraction  │  │  /set-project    │
          │  intelligence    │  │                  │  │  (manual entry)  │
          │  (3-pass + visual│  │  DWG → DXF → JSON│  │                  │
          │   extraction)    │  │                  │  │                  │
          └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
                   │                     │                      │
                   ▼                     ▼                      ▼
          ┌──────────────────────────────────────────────────────────┐
          │                   JSON DATA STORE                        │
          │  AI - Project Brain/                                     │
          │                                                          │
          │  project-config.json    plans-spatial.json                │
          │  specs-quality.json     schedule.json                    │
          │  directory.json         rfi-log.json                     │
          │  submittal-log.json     procurement-log.json             │
          │  change-order-log.json  inspection-log.json              │
          │  meeting-log.json       punch-list.json                  │
          │  pay-app-log.json       delay-log.json                   │
          │  labor-tracking.json    quality-data.json                │
          │  safety-log.json        daily-report-data.json           │
          │  daily-report-intake.json  cost-data.json                │
          └───────────────────────────┬──────────────────────────────┘
                                      │
            ┌──────────┬──────────┬───┴────┬──────────┬──────────┐
            ▼          ▼          ▼        ▼          ▼          ▼
      ┌──────────┐ ┌────────┐ ┌───────┐ ┌──────┐ ┌────────┐ ┌───────┐
      │ /daily-  │ │/weekly-│ │/look- │ │/morn-│ │/project│ │Skill  │
      │ report   │ │report  │ │ahead  │ │ing-  │ │-dash-  │ │Queries│
      │          │ │        │ │       │ │brief │ │board   │ │       │
      └──────────┘ └────────┘ └───────┘ └──────┘ └────────┘ └───────┘
```

---

## Extraction Pipelines

### Document Intelligence Pipeline

The `document-intelligence` skill processes uploaded documents through a multi-pass extraction system:

```
Document Upload
    │
    ▼
Pass 1 — PDF Text Extraction
    │  Extract raw text, identify document type, discipline, sections
    │
    ▼
Pass 2 — Structured Data Extraction
    │  Parse tables, schedules, specification sections, notes
    │  Output: spec_sections, key_materials, contract, safety
    │
    ▼
Pass 3 — Cross-Reference Extraction
    │  Parse drawing references, RFI/submittal mentions, spec callouts
    │  Output: sheet_cross_references, spec_references
    │
    ▼
Pass 4+ — Visual Pipeline (plan sheets only)
    │  Claude Vision analysis of plan sheet images
    │  Detects: grid lines, room boundaries, symbols, dimensions,
    │  material hatches, keynotes, equipment, scale bars
    │  Output: grid_lines, building_areas, room_schedule, quantities
    │
    ▼
Merge & Store
    │  Merge new data with existing store (incremental update)
    │  Flag discrepancies, update version_history
    │
    ▼
JSON Data Files Updated
```

**Files populated:** `project-config.json` (documents_loaded), `plans-spatial.json` (all sections), `specs-quality.json` (all sections), `schedule.json` (milestones, critical_path), `directory.json` (from contract docs)

### DWG Extraction Pipeline

The `dwg-extraction` skill converts AutoCAD DWG files to structured data:

```
DWG File
    │
    ▼
compile_libredwg.sh
    │  Compile libredwg C library (cached at /tmp/libredwg/dwg2dxf)
    │
    ▼
dwg2dxf (C binary)
    │  Convert DWG → DXF (text-based CAD format)
    │
    ▼
parse_dxf.py
    │  Custom parser: Civil 3D XDATA, INSERT+ATTRIB, proximity grouping
    │  Extract: polylines, dimensions, text, blocks, layers, attributes
    │
    ▼
plans-spatial.json
    │  DXF data merged with Priority 1 (highest accuracy)
    │  Grid lines (exact), room boundaries (exact), pipe runs (exact)
```

**Files populated:** `plans-spatial.json` (grid_lines, room_schedule, quantities with `source: "dxf"`)

### Quantitative Intelligence Pipeline

The `quantitative-intelligence` skill builds on extracted data to calculate derived quantities:

```
plans-spatial.json (raw extracted data)
    │
    ▼
Build Sheet Cross-Reference Index
    │  Map all detail callouts, section cuts, schedule references
    │
    ▼
Create Assembly Chains
    │  Link elements across multiple sheets
    │  Footing F1: plan view (S2.1) → detail (S5.1) → notes (S1.0)
    │
    ▼
calc_bridge.py (10 calculator classes)
    │  ConcreteVolumeCalc  → CY per element
    │  WallAreaCalc        → SF per wall type
    │  RoomAreaCalc        → SF per room
    │  PipeRunCalc         → LF per system/size
    │  FootingCalc         → volume, rebar, formwork
    │  SlabCalc            → SOG area, volume, vapor barrier
    │  RoofCalc            → area (flat + sloped), insulation
    │  PEMBCalc            → bay areas, panels, gutter
    │  SymbolCountCalc     → fixture/device counts
    │  AggregateCalc       → CSI division totals
    │
    ▼
Multi-Source Validation
    │  Compare DXF vs visual vs takeoff vs text values
    │  Flag discrepancies >10%
    │
    ▼
plans-spatial.json → quantities, sheet_cross_references
```

**Files populated:** `plans-spatial.json` (quantities, sheet_cross_references.assembly_chains)

---

## Command-Driven Data Flow

### Setup Phase

```
/set-project
    │  User provides: project name, client, team, building type, folder paths
    │  Writes: project-config.json (project_basics, folder_mapping)
    │  Optionally reads: SC/PO Log spreadsheet → procurement-log.json
    │
    ▼
/process-docs  (one or more documents)
    │  Triggers: document-intelligence extraction pipeline
    │  Reads: uploaded PDF/images
    │  Writes: project-config.json (documents_loaded)
    │          plans-spatial.json, specs-quality.json, schedule.json, directory.json
    │
    ▼
/process-dwg  (optional — if DWG files available)
    │  Triggers: dwg-extraction pipeline
    │  Reads: uploaded .dwg files
    │  Writes: plans-spatial.json (DXF-sourced quantities at Priority 1)
    │
    ▼
/cost  (budget initialization)
    │  Triggers: cost-tracking skill → Budget Initialization
    │  User provides: contract value, CSI division budget breakdown,
    │                 contingency amount, allowances, SOV line items
    │  Reads: change-order-log.json (approved CO linkage),
    │         pay-app-log.json (SOV structure)
    │  Writes: cost-data.json (original_contract_value, budget_by_division[],
    │          contingency, allowances[])
    │  NOTE: This is the ONLY documented entry path for establishing
    │        the cost baseline that EVM, risk-management, and cost-tracking consume
```

### Daily Operations Phase

```
/log  (throughout the day — multiple entries)
    │  Triggers: intake-chatbot classification
    │  Reads: directory.json (sub resolution), plans-spatial.json (location resolution),
    │         specs-quality.json (material enrichment)
    │  Writes: daily-report-intake.json (classified entries)
    │
    ▼
/daily-report  (end of day)
    │  Reads: daily-report-intake.json (all entries for today)
    │         project-config.json (headers, report numbering)
    │         plans-spatial.json (quantities for progress %)
    │         specs-quality.json (weather thresholds, hold points)
    │         schedule.json (current phase, milestones)
    │         directory.json (sub details for crew section)
    │  Writes: daily-report-data.json (structured report record)
    │          .docx/.pdf report file to folder_mapping.daily_reports
    │          delay-log.json (if delays classified)
    │          project-config.json (report_tracking.last_report_number++)
```

### Weekly/Periodic Phase

```
/weekly-report
    │  Reads: daily-report-data.json (all reports for the week)
    │         schedule.json, change-order-log.json, rfi-log.json
    │         submittal-log.json, safety-log.json, inspection-log.json
    │         delay-log.json, pay-app-log.json
    │  Writes: directory.json (owner_reports), .docx/.pdf report

/look-ahead
    │  Reads: schedule.json, directory.json, procurement-log.json
    │         specs-quality.json, rfi-log.json, submittal-log.json
    │         daily-report-data.json (crew trends)
    │  Writes: schedule.json (lookahead_history), .docx/.xlsx schedule

/morning-brief
    │  Reads: schedule.json, inspection-log.json, rfi-log.json
    │         submittal-log.json, change-order-log.json, meeting-log.json
    │         procurement-log.json, safety-log.json, daily-report-data.json
    │         plans-spatial.json (quantities for today's work areas)
    │  Output: Morning briefing summary (not stored)
```

### Log Commands (write to individual log files)

```
/rfis          → rfi-log.json
/submittals    → submittal-log.json
/change-order  → change-order-log.json
/meeting-notes → meeting-log.json
/punch         → punch-list.json
/inspection    → inspection-log.json
/safety        → safety-log.json
/labor         → labor-tracking.json
```

---

## Consumer Map — Which Files Feed Which Skills

| Skill / Command | Reads From |
|-----------------|------------|
| `intake-chatbot` | `directory.json`, `plans-spatial.json`, `specs-quality.json`, `schedule.json` |
| `punch-list` | `plans-spatial.json`, `directory.json`, `specs-quality.json`, `schedule.json` |
| `inspection-tracker` | `specs-quality.json`, `schedule.json`, `plans-spatial.json` |
| `safety-management` | `specs-quality.json`, `plans-spatial.json`, `directory.json` |
| `cost-tracking` | `plans-spatial.json`, `schedule.json`, `change-order-log.json`, `procurement-log.json`, `pay-app-log.json` |
| `labor-tracking` | `plans-spatial.json`, `directory.json`, `daily-report-intake.json`, `specs-quality.json` |
| `meeting-minutes` | `schedule.json`, `rfi-log.json`, `submittal-log.json`, `change-order-log.json`, `meeting-log.json`, `daily-report-data.json`, `safety-log.json` |
| `change-order-tracker` | `schedule.json`, `cost-data.json`, `specs-quality.json`, `plans-spatial.json`, `directory.json` |
| `quantitative-intelligence` | `plans-spatial.json` (reads + writes) |
| `/daily-report` | `daily-report-intake.json`, `project-config.json`, `plans-spatial.json`, `specs-quality.json`, `schedule.json`, `directory.json` |
| `/weekly-report` | `daily-report-data.json`, `schedule.json`, `change-order-log.json`, `rfi-log.json`, `submittal-log.json`, `safety-log.json`, `inspection-log.json`, `delay-log.json`, `pay-app-log.json` |
| `/morning-brief` | `schedule.json`, `inspection-log.json`, `rfi-log.json`, `submittal-log.json`, `change-order-log.json`, `meeting-log.json`, `procurement-log.json`, `safety-log.json`, `plans-spatial.json` |
| `/look-ahead` | `schedule.json`, `directory.json`, `procurement-log.json`, `specs-quality.json`, `rfi-log.json`, `submittal-log.json`, `daily-report-data.json` |

---

## Update Triggers — When Data Gets Refreshed

| Trigger Event | Files Updated | Downstream Impact |
|---------------|---------------|-------------------|
| `/set-project` | `project-config.json`, `schedule.json`, `directory.json` | All commands can now reference project basics |
| `/process-docs` (new document) | `plans-spatial.json`, `specs-quality.json`, `schedule.json`, `directory.json`, `project-config.json` | Quantities recalculated, assembly chains rebuilt |
| `/process-dwg` (new DWG) | `plans-spatial.json` | DXF quantities override visual estimates |
| `/cost` (budget initialization) | `cost-data.json` | Establishes cost baseline for EVM, risk-management, cost-tracking |
| `/log` (field entry) | `daily-report-intake.json` | Data accumulates for `/daily-report` |
| `/daily-report` generated | `daily-report-data.json`, `delay-log.json`, `project-config.json` | Weekly report gets new source data |
| `/rfis` (new/updated RFI) | `rfi-log.json` | Morning brief, look-ahead, meeting minutes |
| `/submittals` (new/updated) | `submittal-log.json` | Morning brief, look-ahead, procurement |
| `/change-order` (new/updated CO) | `change-order-log.json` | Cost tracking, schedule impact, weekly report |
| `/meeting-notes` (meeting recorded) | `meeting-log.json` | Action item carry-forward, morning brief |
| `/punch` (new item) | `punch-list.json` | Dashboard completion %, daily report |
| `/inspection` (result logged) | `inspection-log.json` | Morning brief, daily report |
| `/safety` (incident logged) | `safety-log.json` | Morning brief, TRIR calc, meeting minutes |
| `/labor` (hours logged) | `labor-tracking.json` | EVM actual cost, daily report cross-validation |
| ASI received | `project-config.json` (asi_log) | Assembly chains marked needs_verification |
