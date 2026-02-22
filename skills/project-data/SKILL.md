---
name: project-data
description: >
  Use this skill when reading from or writing to the project intelligence data store.
  Manages a multi-file data store (project-config.json, plans-spatial.json, specs-quality.json,
  schedule.json, directory.json, individual log files, and daily-report-data.json).
  Handles storage, cross-referencing, versioning, validation, and smart retrieval of
  project intelligence, report history, RFI/submittal logs, procurement tracking,
  vendor database, and lookahead schedules.
version: 2.0.0
---

# Project Data Management

## Overview

The data backbone for Foreman_OS. This skill owns the project intelligence store, the report history log, and all operational data. Every other skill reads from and writes to the data layer through the patterns defined here.

## Data Files

All JSON files are stored in `folder_mapping.ai_output` (typically `AI - Project Brain/`). If folder_mapping is not yet set up, fall back to the user's working directory root.

**IMPORTANT — File Location Rule:** When searching for these files, always check `AI - Project Brain/` first, then fall back to the project root. When saving, always save to `folder_mapping.ai_output` if available.

### File Structure

| File | Purpose | Key Contents |
|---|---|---|
| `project-config.json` | Master config — project identity, folder paths, document tracking, change history | project_basics, report_tracking, folder_mapping, documents_loaded, version_history, asi_log |
| `plans-spatial.json` | Everything derived from plan sheets — spatial layout, quantities, drawing cross-references | grid_lines, building_areas, floor_levels, room_schedule, site_layout, sheet_cross_references, quantities, site_utilities |
| `specs-quality.json` | Everything from specs and quality documents — requirements, thresholds, testing, safety | spec_sections, key_materials, weather_thresholds, hold_points, tolerances, contract, safety, swppp, geotechnical, mix_designs |
| `schedule.json` | Schedule data and lookahead history | milestones, critical_path, near_critical, weather_sensitive_activities, long_lead_items, material_requirements_by_activity, lookahead_history |
| `directory.json` | People and companies | subcontractors, subcontractor_assignments, vendor_database, owner_reports |
| `rfi-log.json` | RFI tracking | rfi_log array |
| `submittal-log.json` | Submittal tracking | submittal_log array |
| `procurement-log.json` | Material procurement tracking (includes cert tracking) | procurement_log array |
| `change-order-log.json` | Change order tracking | change_order_log array |
| `inspection-log.json` | Inspection and permit tracking | inspection_log array, permit_log array |
| `meeting-log.json` | Meeting minutes and action items | meeting_log array |
| `punch-list.json` | Punch list items | punch_list array |
| `pay-app-log.json` | Pay application tracking | pay_applications array, lien_waivers, retainage tracking, schedule_of_values |
| `delay-log.json` | Delay event tracking | delay_events array, weather_delays, owner_delays, claims documentation |
| `labor-tracking.json` | Labor hours and crew productivity | labor_entries array, crew_summaries, productivity_ratios, classifications |
| `quality-data.json` | Quality inspections and deficiency tracking | inspections array, deficiencies, corrective_actions, quality_metrics |
| `daily-report-data.json` | Report history — the running record that feeds dashboard and weekly reports | Structured data from every generated daily report |

### File Lookup Table

When a skill or command needs specific data, use this table to know which file to read:

| You need... | Read from |
|---|---|
| Project name, address, team, logo | `project-config.json` → project_basics |
| Report numbering | `project-config.json` → report_tracking |
| Where to save files | `project-config.json` → folder_mapping |
| What documents have been processed | `project-config.json` → documents_loaded |
| Change history for any data | `project-config.json` → version_history |
| Architect's Supplemental Instructions (ASIs) | `project-config.json` → asi_log |
| Grid lines, building areas, floor levels | `plans-spatial.json` |
| Room schedule, site layout | `plans-spatial.json` |
| Drawing index, detail callouts, assembly chains | `plans-spatial.json` → sheet_cross_references |
| Quantities (rooms, walls, concrete, flooring, piping, counts, PEMB) | `plans-spatial.json` → quantities |
| Site utilities (storm, sanitary, water, fire, gas, telecom) | `plans-spatial.json` → site_utilities |
| Spec sections, CSI requirements | `specs-quality.json` → spec_sections |
| Key materials, testing requirements | `specs-quality.json` → key_materials |
| Weather thresholds (temp/wind limits) | `specs-quality.json` → weather_thresholds |
| Hold points, witness points, tolerances | `specs-quality.json` |
| Concrete mix designs | `specs-quality.json` → mix_designs |
| Contract dates, LDs, working hours | `specs-quality.json` → contract |
| Safety zones, SWPPP, geotechnical | `specs-quality.json` |
| Schedule milestones, critical path | `schedule.json` |
| Long-lead items, weather-sensitive activities | `schedule.json` |
| Lookahead history | `schedule.json` → lookahead_history |
| Subcontractor directory | `directory.json` → subcontractors |
| Vendor database | `directory.json` → vendor_database |
| Weekly owner report archive | `directory.json` → owner_reports |
| RFI entries | `rfi-log.json` |
| Submittal entries | `submittal-log.json` |
| Procurement / material tracking | `procurement-log.json` |
| Change orders | `change-order-log.json` |
| Inspections and permits | `inspection-log.json` |
| Meeting minutes and action items | `meeting-log.json` |
| Punch list items | `punch-list.json` |
| Pay application data | `pay-app-log.json` |
| SOV / schedule of values | `pay-app-log.json` → schedule_of_values |
| Lien waivers | `pay-app-log.json` → lien_waivers |
| Delay events | `delay-log.json` → delay_events |
| Weather days / contract extensions | `delay-log.json` → weather_delays, delay_events |
| Labor hours, crew counts, overtime | `labor-tracking.json` → labor_entries |
| Crew productivity ratios | `labor-tracking.json` → productivity_ratios |
| Worker classifications (Davis-Bacon) | `labor-tracking.json` → classifications |
| Quality inspection results | `quality-data.json` → inspections |
| Quality deficiencies / corrective actions | `quality-data.json` → deficiencies, corrective_actions |
| Concurrent delays | `delay-log.json` → concurrent_delays |
| Past daily reports | `daily-report-data.json` |

## Project Intelligence Schema

See `references/json-schema-reference.md` for the full schema with producer/consumer mapping. Also see `references/data-flow-map.md` for pipeline architecture and `references/cross-reference-patterns.md` for reusable cross-referencing patterns. Quick reference:

```
project-config.json
  ├── project_basics       → Header info, auto-fills every report
  ├── report_tracking      → Last report number, sequential numbering
  ├── folder_mapping       → Where to save each output type
  ├── documents_loaded     → Extraction history with dates and coverage
  ├── version_history      → Change log for key data points
  └── asi_log              → Architect's Supplemental Instructions tracking

plans-spatial.json
  ├── grid_lines           → Column/row identifiers, spacing, orientation notes
  ├── building_areas       → Named zones with grid references and floor ranges
  ├── floor_levels         → Level names, elevations, descriptions
  ├── room_schedule        → Room numbers, names, locations
  ├── site_layout          → North arrow, access points, laydown, trailers
  ├── sheet_cross_references → Drawing index, detail callouts, assembly chains
  ├── quantities           → Measured quantities (rooms, walls, concrete, flooring, piping, counts, PEMB)
  └── site_utilities       → Storm, sanitary, water, fire, gas, telecom utility runs

specs-quality.json
  ├── spec_sections        → CSI sections with requirements and thresholds
  ├── key_materials        → Material specs with testing requirements
  ├── weather_thresholds   → Temperature/wind limits by work type
  ├── hold_points          → Inspection hold points by work type
  ├── tolerances           → Quality tolerances by material/system
  ├── contract             → Dates, LDs, hours, restrictions, documentation reqs
  ├── safety               → Fall protection zones, confined spaces, hot work areas
  ├── swppp               → BMP locations, inspection triggers, requirements
  ├── geotechnical         → Bearing capacity, water table, compaction reqs
  └── mix_designs          → Concrete mix design specifications

schedule.json
  ├── current_phase        → Active construction phase
  ├── percent_complete     → Overall project progress
  ├── milestones           → Key dates with status tracking
  ├── critical_path        → Critical path activities
  ├── near_critical        → Near-critical activities
  ├── weather_sensitive    → Activities affected by weather
  ├── long_lead_items      → Long-lead material items
  ├── material_requirements_by_activity → Activity-to-material mapping
  └── lookahead_history    → Generated lookahead schedule records

directory.json
  ├── subcontractors       → Directory with names, trades, contacts, scopes
  ├── vendor_database      → Supplier directory with capabilities and history
  └── owner_reports        → Weekly owner report archive

Individual log files (rfi-log.json, submittal-log.json, procurement-log.json,
change-order-log.json, inspection-log.json, meeting-log.json, punch-list.json,
pay-app-log.json, delay-log.json)
  ├── rfi-log.json         → RFI log array
  ├── submittal-log.json   → Submittal log array
  ├── procurement-log.json → Procurement log array
  ├── change-order-log.json → Change order log array
  ├── inspection-log.json  → Inspection/permit log array
  ├── meeting-log.json     → Meeting minutes and action items array
  ├── punch-list.json      → Punch list items array
  ├── pay-app-log.json     → Pay applications, SOV, lien waivers, retainage tracking
  └── delay-log.json       → Delay events, weather delays, concurrent delays, claims

daily-report-data.json
  └── Report history — the running record that feeds dashboard and weekly reports
```

## Smart Retrieval

When a skill needs project data, it should only load the specific files it needs — never all 13 files at once.

### Retrieval by Work Type

When the user describes work being performed, pull the relevant cross-section:

| User mentions | Files to read | Retrieve |
|---|---|---|
| Concrete work | specs-quality.json, plans-spatial.json, schedule.json | Concrete spec sections, mix designs, testing frequency, cold/hot weather thresholds, hold points, compaction reqs if SOG |
| Steel erection | specs-quality.json, plans-spatial.json, schedule.json | Steel spec sections, connection types, special inspection reqs, crane locations from site layout, wind speed limits |
| Excavation/earthwork | specs-quality.json, plans-spatial.json | Geotechnical data, compaction requirements, utility locations, dewatering triggers, SWPPP BMPs |
| Roofing | specs-quality.json | Roofing spec section, weather thresholds (wind, temperature, moisture), manufacturer requirements |
| MEP rough-in | specs-quality.json, plans-spatial.json | Relevant M/E/P spec sections, inspection requirements, coordination notes |
| Framing | specs-quality.json | Structural specs, connection details, inspection hold points |
| Waterproofing | specs-quality.json | Waterproofing spec section, temperature requirements, surface prep tolerances |

### Retrieval by Location

When the user mentions a location, resolve it from `plans-spatial.json`:

| User says | Resolve to |
|---|---|
| "east side" | Building area with "east" in name → grid lines → floor levels for that area |
| "second floor" | Floor level "Level 2" → rooms on that level → building areas at that level |
| "by the elevator" | Central core area → grid lines for core → floor level |
| "at Grid C" | All building areas that include Grid C → activities at that location |

### Retrieval by Subcontractor

When the user mentions a sub (even casually), match from `directory.json`:

| User says | Match to |
|---|---|
| "Walker" | Walker Construction → Excavation/Sitework → scope details → schedule dates |
| "the electrician" | Sub with trade = "Electrical" → company name → foreman → scope |
| "HVAC guys" | Sub with trade containing "HVAC" or "Mechanical" → full record |

## Cross-Referencing

The power of the data layer is connecting related information across files. When serving data, always include cross-references:

### Sub → Schedule → Spec
A subcontractor is linked to their scope, which maps to spec sections, which have testing and inspection requirements. When "Walker Construction" is on site doing excavation:
- Pull their scope from `directory.json`
- Pull the earthwork spec sections from `specs-quality.json`
- Pull compaction testing requirements from `specs-quality.json`
- Pull geotechnical requirements from `specs-quality.json`
- Check schedule from `schedule.json` for earthwork milestones

### Location → Grid → Area → Room
A location mention cascades through spatial data in `plans-spatial.json`:
- "Room 205" → Room schedule → Level 2 → East Wing → Grid E-G / 3-5
- "East wing foundation" → East Wing → Grid E-G → Level 1 / Below grade → Foundation spec sections (from `specs-quality.json`)

### Work Type → Weather Threshold → Today's Weather
When documenting work, check if today's weather affects that work:
- Concrete placement + today's temp < cold weather threshold (from `specs-quality.json`) → Flag in report
- Crane operations + today's wind > wind speed limit (from `specs-quality.json`) → Flag in report

### Retrieval by Quantity

When the user asks about quantities, measurements, or progress percentages — read from `plans-spatial.json`:

| User asks | Retrieve |
|---|---|
| "how much concrete" | quantities.concrete → total CY by element type, assembly chains with source sheets |
| "room areas" | quantities.rooms → all rooms with area SF, perimeter LF, source attribution |
| "flooring progress" | quantities.flooring → total SF by type, cross-ref with rooms completed in `daily-report-data.json` |
| "how many outlets" | quantities.counts → symbol counts with schedule comparison, discrepancy flags |
| "total drywall" | quantities.walls → wall SF by type, calculate GWB from wall assemblies |
| "which sheets for footing F1" | sheet_cross_references.assembly_chains → all linked sheets for that element |

### Element → Assembly Chain → Multi-Sheet Data
When a specific construction element is referenced, trace its assembly chain in `plans-spatial.json`:
- "Footing F1" → sheet_cross_references.assembly_chains → S2.1 (plan) + S5.1 (detail) + S1.0 (notes)
- Pull dimensions from each linked sheet, calculate volume, note concrete spec
- Include source priority (DXF exact data > visual estimate > text-parsed value)

### Retrieval by RFI/Submittal

When working with RFIs or submittals, pull the full context chain across files:

| Query | Files to read | Retrieve |
|---|---|---|
| RFI by subject/topic | rfi-log.json, specs-quality.json, plans-spatial.json | Matching RFI entries → linked drawing refs → linked spec sections → related submittals |
| RFI by status | rfi-log.json, schedule.json | All RFIs with status "issued" or "pending" → schedule impact |
| Submittal by spec section | submittal-log.json, specs-quality.json | Matching submittal entries → spec requirements → compliance matrix |
| Submittal by status | submittal-log.json, schedule.json | All submittals "under_review" or "revise_and_resubmit" → lead times → schedule impact |
| Submittal by sub | submittal-log.json, directory.json | All submittals from that sub → their scope → related spec sections |
| Overdue RFIs | rfi-log.json | All RFIs issued > 14 days ago with status != "resolved" |
| Overdue submittals | submittal-log.json | All submittals with review pending > 10 business days |

### Retrieval by Procurement

Read from `procurement-log.json`, cross-reference with other files as needed:

| Query | Retrieve |
|---|---|
| Long-lead items | All procurement with category "long_lead" → expected delivery → schedule activity linked (cross-ref `schedule.json`) |
| Upcoming deliveries | All procurement with expected_delivery in next 14 days → spec requirements (cross-ref `specs-quality.json`) → storage location |
| Delayed materials | All procurement with delivery_status "delayed" → schedule impact → alternative vendors (cross-ref `directory.json`) |
| Unverified deliveries | All procurement with actual_delivery set but verified_against_spec = false |
| Missing certs | All procurement with certs_required but certs_received incomplete |
| Material by spec section | All procurement matching a spec section → supplier → delivery status |

### Retrieval by Pay Application

Read from `pay-app-log.json`, cross-reference with subcontractor and change order tracking:

| Query | Retrieve |
|---|---|
| Current pay application status | Latest pay_application entry → current amount, retainage, approval status |
| Schedule of values | pay-app-log.json → schedule_of_values (sum by trade, by phase, total contract value) |
| Retainage tracking | pay-app-log.json → retainage_held, retainage_released, remaining_retainage (by contractor, by pay period) |
| Lien waivers pending | All lien_waivers with status "pending" → contractor name, deadline for receipt |
| Lien waivers received | All lien_waivers with status "received" → storage location, date received, percentage release authorized |
| Payment by contractor | All pay_applications entries filtered by contractor → total paid, percentage complete, retainage |
| Change order impact on payment | pay-app-log.json cross-ref with `change-order-log.json` → which COs have been incorporated into pay app |
| Cost variance | pay-app-log.json → contract_value vs sum(all pay applications) → budget impact trend |

### Retrieval by Delay Event

Read from `delay-log.json`, cross-reference with schedule and daily report data:

| Query | Retrieve |
|---|---|
| Weather delays | All delay_events with type "weather" → date, duration, affected activities, weather thresholds exceeded |
| Owner delays | All delay_events with type "owner_delay" → date, reason (permit, decision, document approval), duration |
| Concurrent delays | All concurrent_delays entries → which delays happened at same time, impact on schedule impact calculation |
| Delay documentation | delay_events → daily_report_references, photos, weather data, contractor notification log |
| Schedule extension claims | All delay_events with claims_filed = true → claim date, contractor, damages requested, supporting documents |
| Recovery actions | delay_events → recovery_measures_taken, accelerated_activities, cost of acceleration |
| Total delay impact | Sum all approved_delay_days across all delay_events → net schedule impact vs original substantial completion date |
| Concurrent delay disputes | All concurrent_delays where responsibility is disputed → document contractor vs owner claims separately |

### Retrieval for Lookahead

When generating a look-ahead schedule, pull a composite view:

| Data needed | Source file |
|---|---|
| Activities for next 3 weeks | `schedule.json` → milestones + critical_path + near_critical filtered by date range |
| Subs for each activity | `directory.json` → subcontractors matched by trade/scope |
| Materials needed | `procurement-log.json` → expected_delivery in lookahead window, plus long_lead items |
| Weather constraints | `specs-quality.json` → weather_thresholds matched to activity work types |
| Pending RFIs that block work | `rfi-log.json` → status != "resolved" and schedule_impact != "none" |
| Pending submittals that block work | `submittal-log.json` → status = "under_review" and schedule_impact = "critical_path_blocked" |
| Recent crew trends | `daily-report-data.json` → Last 5 daily reports → crew.subs_on_site → headcount trends |

### Retrieval for Weekly Owner Report

| Data needed | Source file |
|---|---|
| All daily reports for the week | `daily-report-data.json` filtered by date range |
| Current schedule status | `schedule.json` → current_phase, percent_complete, milestones_approaching |
| Active delays | `delay-log.json` → delay_events; also `daily-report-data.json` → Latest report's schedule.delays |
| Delay summary (weather, owner, concurrent) | `delay-log.json` → weather_delays, concurrent_delays, claims_documentation |
| Open items | `daily-report-data.json` → Latest report's open_items |
| Weather summary for week | `daily-report-data.json` → All reports' weather sections |
| Inspection summary | `daily-report-data.json` → All reports' inspections sections |
| Photo highlights | `daily-report-data.json` → All reports' photos (select representative) |
| Pay application status | `pay-app-log.json` → Latest pay application, retainage tracking |
| Lien waiver status | `pay-app-log.json` → lien_waivers (pending vs received) |
| ASI status | `project-config.json` → asi_log (active ASIs, change order impacts) |
| Distribution list | `specs-quality.json` → contract.documentation_requirements.distribution_list |

### Cross-Referencing: RFI → Submittal → Procurement

These three log files are interconnected:

- An **RFI** (`rfi-log.json`) may trigger a **submittal** (architect clarifies, resulting in a product change)
- A **submittal** (`submittal-log.json`) approval may trigger **procurement** (approved product can now be ordered)
- A **procurement** (`procurement-log.json`) delay may trigger an **RFI** (need alternate product approval)

When serving data from any of these logs, always check for cross-references:
- RFI's `related_submittals[]` → pull linked entries from `submittal-log.json`
- Submittal's `related_rfis[]` → pull linked entries from `rfi-log.json`
- Procurement's `submittal_id` → pull linked submittal status from `submittal-log.json` (can't order until approved)


---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
