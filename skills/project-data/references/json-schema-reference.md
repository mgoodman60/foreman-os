# JSON Schema Reference — All Project Intelligence Files

Complete schema documentation for all project intelligence data files. Each section lists every field, its type, description, which skills/commands **produce** it, and which skills/commands **consume** it.

All files are stored in `folder_mapping.ai_output` (typically `AI - Project Brain/`).

---

## 1. project-config.json

Master configuration — project identity, folder paths, document tracking, and change history.

### `project_basics`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `project_name` | string | Official project name | `/set-project` | All report commands, all skills |
| `project_code` | string | Short project code | `/set-project` | Report headers |
| `project_number` | string | Contract/job number | `/set-project` | Report headers, pay-app |
| `client` | string | Owner/client name | `/set-project` | `/weekly-report`, `/meeting-notes` |
| `superintendent` | string | GC superintendent name | `/set-project` | Report signatures, morning brief |
| `architect` | string | Architect of record | `/set-project`, `/process-docs` | RFI routing, submittal routing |
| `project_manager` | string | PM name | `/set-project` | Report distribution |
| `engineers` | object | Structural, MEP, civil engineers | `/set-project`, `/process-docs` | RFI routing |
| `address` | string | Project address | `/set-project` | Report headers |
| `building_type` | string | Building use classification | `/set-project`, `/process-docs` | Inspection types, code requirements |
| `gross_sf` | string | Total building SF | `/set-project`, `/process-docs` | Cost per SF calculations |
| `stories` | string | Number of stories | `/set-project`, `/process-docs` | Vertical logistics planning |
| `logo_path` | string | Path to project/company logo | `/set-project` | Report headers |
| `claims_mode` | boolean | Enhanced detail capture for claims | `/set-project` | `intake-chatbot`, `daily-report` |

### `report_tracking`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `last_report_number` | integer | Sequential report counter | `/daily-report` | `/daily-report` (next number) |

### `folder_mapping`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `daily_reports` | string | Path for daily report output | `/set-project` | `/daily-report` |
| `weekly_reports` | string | Path for weekly report output | `/set-project` | `/weekly-report` |
| `submittals` | string | Path for submittal docs | `/set-project` | `/submittals` |
| `rfis` | string | Path for RFI docs | `/set-project` | `/rfis` |
| `photos` | string | Path for site photos | `/set-project` | `/daily-report`, `photo-analyst` |
| `schedules` | string | Path for schedule output | `/set-project` | `/look-ahead` |
| `safety` | string | Path for safety docs | `/set-project` | `safety-management` |
| `subcontractors` | string | Path for sub docs | `/set-project` | `punch-list` |
| `suppliers` | string | Path for supplier docs | `/set-project` | `procurement-log` |
| `oac_reports` | string | Path for OAC reports | `/set-project` | `/meeting-notes`, `/weekly-report` |
| `change_orders` | string | Path for CO docs | `/set-project` | `change-order-tracker` |
| `ai_output` | string | Path for AI data store | `/set-project` | All skills (data read/write) |
| `spreadsheets` | string | Path for spreadsheets | `/set-project` | `material-tracker` |
| `bidding` | string | Path for bid docs | `/set-project` | — |
| `contracts` | string | Path for contract docs | `/set-project` | — |
| `sc_po_log` | string | Full path to SC/PO Log spreadsheet | `/set-project` | `material-tracker` |

### `documents_loaded`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `filename` | string | Document file name | `/process-docs` | — |
| `type` | string | Document type (plans, specs, etc.) | `/process-docs` | — |
| `discipline` | string | A/S/M/E/P/C discipline code | `/process-docs` | — |
| `date_loaded` | string | ISO 8601 date of extraction | `/process-docs` | — |
| `sections_extracted` | array | Which data sections were populated | `/process-docs` | — |
| `coverage_notes` | string | Extraction quality notes | `/process-docs` | — |
| `confidence` | string | high/medium/low | `/process-docs` | — |

### `version_history`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `date` | string | ISO 8601 timestamp | All write operations | Audit trail |
| `source` | string | What triggered the change | All write operations | Audit trail |
| `changes[]` | array | Field-level change records | All write operations | Audit trail |

### `asi_log`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | ASI-NNN identifier | `/asis` | `/asis`, `change-order-tracker` |
| `date` | string | ASI date issued | `/asis` | `/morning-brief`, `/daily-report` |
| `description` | string | Change description | `/asis` | `/daily-report`, `/weekly-report` |
| `affected_sheets` | array | Drawing sheets impacted | `/asis` | `quantitative-intelligence` |

---

## 2. plans-spatial.json

Everything derived from plan sheets — spatial layout, quantities, drawing cross-references, and site utilities.

### `grid_lines`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `columns` | array | Column grid identifiers (A, B, C...) | `document-intelligence`, `/process-docs` | All location resolution |
| `rows` | array | Row grid identifiers (1, 2, 3...) | `document-intelligence`, `/process-docs` | All location resolution |
| `spacing` | string | Typical bay spacing | `document-intelligence` | `quantitative-intelligence` |
| `notes` | string | Grid system notes | `document-intelligence` | — |

### `building_areas`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `name` | string | Zone name (East Wing, etc.) | `document-intelligence` | `intake-chatbot`, `punch-list`, `labor-tracking`, `safety-management` |
| `grids` | string | Grid range (E-G / 3-5) | `document-intelligence` | Location resolution |
| `floors` | string | Floor range | `document-intelligence` | Location resolution |
| `use` | string | Zone purpose | `document-intelligence` | — |

### `floor_levels`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `name` | string | Level name (Level 1, etc.) | `document-intelligence` | `intake-chatbot`, `punch-list`, `labor-tracking` |
| `elevation` | string | Elevation value | `document-intelligence` | `quantitative-intelligence` |
| `description` | string | Level description | `document-intelligence` | — |

### `room_schedule`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `room_number` | string | Room identifier | `document-intelligence` | `punch-list`, `intake-chatbot`, `labor-tracking` |
| `room_name` | string | Room name/function | `document-intelligence` | `punch-list`, `/daily-report` |
| `floor_level` | string | Which floor | `document-intelligence` | Location resolution |
| `building_area` | string | Which zone | `document-intelligence` | Location resolution |
| `department` | string | Department (healthcare) | `document-intelligence` | — |

### `sheet_cross_references`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `drawing_index[]` | array | Every sheet: number, title, discipline, type, revision | `document-intelligence`, `quantitative-intelligence` | `punch-list`, `inspection-tracker`, `change-order-tracker`, `cost-tracking` |
| `detail_callouts[]` | array | Section cuts, details linking source→target sheets | `document-intelligence`, `quantitative-intelligence` | `quantitative-intelligence` (assembly chains) |
| `schedule_references[]` | array | Door/window/equipment marks linking plans→schedules | `document-intelligence` | `quantitative-intelligence` |
| `spec_references[]` | array | Spec section callouts from drawing notes | `document-intelligence` | `inspection-tracker`, `cost-tracking` |
| `assembly_chains[]` | array | Pre-built multi-sheet element chains | `quantitative-intelligence` | `/morning-brief`, `/daily-report`, `cost-tracking` |
| `assembly_chains[].linked_schedule_activities[]` | array | Schedule activities tied to assembly steps | `quantitative-intelligence` | `earned-value-management`, `look-ahead-planner`, `delay-tracker` |
| `assembly_chains[].linked_schedule_activities[].activity_id` | string | Reference to schedule.json activity | `quantitative-intelligence` | `earned-value-management` |
| `assembly_chains[].linked_schedule_activities[].assembly_step` | string | Which assembly this activity maps to | `quantitative-intelligence` | `earned-value-management` |

### `discrepancy_log`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `discrepancy_log[]` | array | Resolved quantity discrepancies | `quantitative-intelligence` | `cost-tracking`, `labor-tracking`, `procurement` |
| `discrepancy_log[].discrepancy_id` | string | Tracking ID | `quantitative-intelligence` | `cost-tracking` |
| `discrepancy_log[].element` | string | Element with discrepancy | `quantitative-intelligence` | `cost-tracking` |
| `discrepancy_log[].resolved_value` | string | Superintendent-approved quantity | `quantitative-intelligence` | `cost-tracking`, `labor-tracking` |
| `discrepancy_log[].resolution_date` | string | Date resolved | `quantitative-intelligence` | `cost-tracking` |

### `quantities`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `rooms[]` | array | Room areas, perimeters, wall/ceiling SF | `quantitative-intelligence`, `document-intelligence` | `punch-list`, `/daily-report`, `cost-tracking`, `labor-tracking` |
| `walls[]` | array | Wall types with total LF, SF, fire rating | `quantitative-intelligence` | `cost-tracking`, `/daily-report` |
| `concrete[]` | array | Concrete elements with volumes, rebar, source sheets | `quantitative-intelligence` | `cost-tracking`, `/daily-report`, `labor-tracking` |
| `flooring[]` | array | Flooring materials with total SF by type | `quantitative-intelligence` | `cost-tracking`, `/daily-report` |
| `piping[]` | array | Pipe runs by system, material, size | `quantitative-intelligence` | `cost-tracking` |
| `counts[]` | array | Fixture/device counts (outlets, switches, etc.) | `quantitative-intelligence` | `cost-tracking`, `/daily-report` |
| `aggregates[]` | array | CSI division totals | `quantitative-intelligence` | `cost-tracking` |
| `pemb` | object | PEMB-specific quantities (bays, panels, gutter) | `quantitative-intelligence` | `cost-tracking`, `inspection-tracker` |
| `data_sources` | object | Source tracking and discrepancy log | `quantitative-intelligence` | — |

### `site_utilities`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `storm` | array | Storm drain runs | `document-intelligence` | `safety-management` (utility strike context) |
| `sanitary` | array | Sanitary sewer runs | `document-intelligence` | `safety-management` |
| `water` | array | Water line runs | `document-intelligence` | `safety-management` |
| `fire` | array | Fire protection mains | `document-intelligence` | `safety-management` |
| `gas` | array | Gas line runs | `document-intelligence` | `safety-management` |
| `electrical_ductbank` | array | Electrical duct banks | `document-intelligence` | `safety-management` |
| `telecom` | array | Telecom conduit runs | `document-intelligence` | `safety-management` |
| `site_utilities[].source` | string | Data source: "dwg" / "notes" / "reconciled" | `project-data` | `quantitative-intelligence`, `safety-management` |

### `as_built_overlay`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `as_built_date` | string | Date of as-built compilation | `document-intelligence` | `closeout-commissioning`, `drawing-control` |
| `deviations[]` | array | Each with deviation_id, sheet, discipline, location, design_value, actual_value, type, cause | `document-intelligence` | `closeout-commissioning`, `drawing-control` |
| `routing_updates[]` | array | Actual vs. designed utility/MEP routing | `document-intelligence` | `closeout-commissioning` |
| `concealed_conditions[]` | array | Hidden/buried conditions | `document-intelligence` | `closeout-commissioning` |

---

## 3. specs-quality.json

Everything from specs and quality documents — requirements, thresholds, testing, safety, contract, and mix designs.

### `spec_sections[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `division` | string | CSI division number | `document-intelligence` | `cost-tracking`, `inspection-tracker`, `change-order-tracker` |
| `section` | string | Full section number | `document-intelligence` | `inspection-tracker`, `intake-chatbot`, `punch-list` |
| `title` | string | Section title | `document-intelligence` | — |
| `key_req` | string | Primary requirement summary | `document-intelligence` | `inspection-tracker` |
| `weather_thresholds` | object | Temp/wind/moisture limits | `document-intelligence` | `safety-management`, `inspection-tracker`, `intake-chatbot` |
| `testing` | object | Testing frequency, type, agency | `document-intelligence` | `inspection-tracker` |
| `hold_points` | array | Inspection hold points | `document-intelligence` | `inspection-tracker`, `intake-chatbot`, `submittal-intelligence` |
| `submittal_required` | boolean | Whether submittal is needed | `document-intelligence` | `/submittals` |

### `key_materials[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `material` | string | Material name | `document-intelligence` | `intake-chatbot` |
| `spec_section` | string | Governing spec | `document-intelligence` | `procurement-log` |
| `specification` | string | ASTM/standard reference | `document-intelligence` | `intake-chatbot` |
| `testing_required` | string | Testing requirements | `document-intelligence` | `inspection-tracker` |

### `weather_thresholds[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `work_type` | string | Activity type (Concrete, Roofing, etc.) | `document-intelligence` | `safety-management`, `inspection-tracker`, `intake-chatbot`, `/daily-report` |
| `min_temp` | string | Minimum temperature for work | `document-intelligence` | `safety-management`, `intake-chatbot` |
| `max_temp` | string | Maximum temperature | `document-intelligence` | `safety-management` |
| `max_wind` | string | Maximum wind speed | `document-intelligence` | `safety-management` |
| `spec_reference` | string | Source spec section | `document-intelligence` | — |
| `mitigation_measures` | string | Cold/hot weather measures | `document-intelligence` | `/daily-report` |

### `hold_points[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `work_type` | string | Activity requiring hold | `document-intelligence` | `inspection-tracker`, `intake-chatbot` |
| `inspection_name` | string | Required inspection name | `document-intelligence` | `inspection-tracker` |
| `trigger` | string | When inspection is required | `document-intelligence` | `inspection-tracker` |
| `inspector` | string | Who performs it | `document-intelligence` | `inspection-tracker` |
| `spec_reference` | string | Source spec section | `document-intelligence` | — |

### `safety`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `fall_protection_zones[]` | array | Fall protection areas | `document-intelligence` | `safety-management` |
| `confined_spaces[]` | array | Confined space locations | `document-intelligence` | `safety-management` |
| `hot_work_areas[]` | array | Hot work areas | `document-intelligence` | `safety-management` |
| `crane_exclusion_zones[]` | array | Crane exclusion areas | `document-intelligence` | `safety-management` |
| `overhead_power_lines[]` | array | Overhead power line locations | `document-intelligence` | `safety-management` |
| `emergency_assembly_point` | string | Assembly point location | `document-intelligence` | `safety-management` |

### `contract`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `ntp_date` | string | Notice to Proceed date | `document-intelligence` | `schedule`, `/morning-brief` |
| `completion_date` | string | Substantial completion date | `document-intelligence` | `schedule`, `/weekly-report` |
| `liquidated_damages` | string | LD rate per day | `document-intelligence` | `change-order-tracker`, `delay-log` |
| `working_hours` | object | Start, end, days | `document-intelligence` | `labor-tracking`, `/daily-report` |
| `documentation_requirements` | object | Reporting requirements, distribution list | `document-intelligence` | `/daily-report`, `/weekly-report` |

### `mix_designs[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `mix_id` | string | Mix design identifier | `document-intelligence` | `intake-chatbot`, `/daily-report` |
| `design_fc` | integer | Design strength (PSI) | `document-intelligence` | `quantitative-intelligence`, `inspection-tracker` |
| `assigned_elements` | array | Which concrete elements use this mix | `document-intelligence` | `quantitative-intelligence` |
| `cold_weather_modification` | string | Cold weather adjustments | `document-intelligence` | `safety-management`, `intake-chatbot` |
| `hot_weather_modification` | string | Hot weather adjustments | `document-intelligence` | `safety-management`, `intake-chatbot` |

### `geotechnical`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `bearing_capacity` | string | Allowable bearing pressure | `document-intelligence` | `inspection-tracker` |
| `water_table_depth` | string | Depth to water table | `document-intelligence` | `safety-management` |
| `fill_requirements` | object | Compaction, lift thickness, testing | `document-intelligence` | `inspection-tracker`, `intake-chatbot` |

---

## 4. schedule.json

Schedule data, lookahead history, and activity-to-material mapping.

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `current_phase` | string | Active construction phase | `/set-project`, manual update | `/morning-brief`, `/daily-report`, `meeting-minutes` |
| `percent_complete` | string | Overall project progress % | manual update | `cost-tracking` (EVM), `/weekly-report`, `meeting-minutes` |
| `milestones[]` | array | Key dates with status | `/set-project`, `/process-docs` | `/morning-brief`, `/look-ahead`, `meeting-minutes`, `change-order-tracker`, `report-qa` |
| `critical_path[]` | array | Critical path activities | `/set-project`, `/process-docs` | `inspection-tracker`, `change-order-tracker`, `punch-list` |
| `near_critical[]` | array | Near-critical activities | `/set-project` | `/look-ahead` |
| `weather_sensitive_activities[]` | array | Weather-affected activities | `/set-project`, `/process-docs` | `safety-management`, `/daily-report` |
| `long_lead_items[]` | array | Long-lead material items | `/process-docs` | `procurement-log`, `/look-ahead` |
| `substantial_completion` | string | Substantial completion date | `/set-project` | `delay-log`, `cost-tracking` |
| `final_completion` | string | Final completion date | `/set-project` | `punch-list` |
| `material_requirements_by_activity[]` | array | Activity-to-material mapping | `/process-docs` | `/look-ahead`, `procurement-log` |
| `lookahead_history[]` | array | Generated lookahead records | `/look-ahead` | `/weekly-report` |

---

## 5. directory.json

People, companies, and owner report archive.

### `subcontractors[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `name` | string | Company name | `/set-project`, `/process-docs` | `intake-chatbot`, `punch-list`, `labor-tracking`, `meeting-minutes`, `change-order-tracker`, `safety-management`, `submittal-intelligence` |
| `trade` | string | Primary trade | `/set-project` | `intake-chatbot` (entity resolution), `punch-list` |
| `scope` | string | Contracted scope of work | `/set-project` | `change-order-tracker`, `cost-tracking` |
| `foreman` | string | Field foreman name | `/set-project` | `punch-list`, `/daily-report`, `submittal-intelligence` |
| `phone` | string | Contact phone | `/set-project` | `/daily-report`, `meeting-minutes`, `submittal-intelligence` |
| `email` | string | Contact email | `/set-project` | `/daily-report` |
| `start_date` | string | Mobilization date | `/set-project` | `/look-ahead` |
| `status` | string | active/mobilized/demobilized | `/set-project` | `intake-chatbot` (absence detection) |

### `vendor_database[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `company_name` | string | Supplier name | `/set-project`, `/process-docs` | `procurement-log` |
| `capabilities` | array | What they supply | `/set-project` | `procurement-log` |
| `materials_supplied` | array | Material categories | `/set-project` | `procurement-log` |
| `past_quotes[]` | array | Historical pricing | `procurement-log` | `cost-tracking` |

### `owner_reports[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | WR-NNN identifier | `/weekly-report` | — |
| `week_ending` | string | Report period end | `/weekly-report` | — |
| `executive_summary` | string | Week summary | `/weekly-report` | — |
| `schedule_status` | string | on_track/at_risk/behind/ahead | `/weekly-report` | — |

---

## 6. rfi-log.json

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | RFI-NNN identifier | `/rfis` | `meeting-minutes`, `change-order-tracker` |
| `date_issued` | string | Date RFI was issued | `/rfis` | `/morning-brief` |
| `subject` | string | RFI topic | `/rfis` | `meeting-minutes`, `/morning-brief` |
| `status` | string | draft/issued/response_received/resolved/void | `/rfis` | `/morning-brief`, `meeting-minutes`, `/look-ahead` |
| `schedule_impact` | string | none/minor/major | `/rfis` | `change-order-tracker`, `/look-ahead` |
| `related_submittals` | array | Linked submittal IDs | `/rfis` | `project-data` cross-ref |
| `location` | object | Grid/area/floor references | `/rfis` | `change-order-tracker` |

---

## 7. submittal-log.json

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | SUB-NNN identifier | `/submittals` | `meeting-minutes`, `procurement-log` |
| `spec_section` | string | CSI section number | `/submittals` | `inspection-tracker` |
| `status` | string | submitted/under_review/approved/revise_and_resubmit/rejected | `/submittals` | `meeting-minutes`, `/morning-brief`, `/look-ahead` |
| `schedule_impact` | string | none/critical_path_blocked/lead_time_risk | `/submittals` | `/look-ahead` |
| `related_rfis` | array | Linked RFI IDs | `/submittals` | `project-data` cross-ref |
| `lead_time_weeks` | integer | Supplier lead time | `/submittals` | `procurement-log`, `/look-ahead` |

---

## 8. procurement-log.json

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | PROC-NNN identifier | `material-tracker` | `cost-tracking`, `/look-ahead` |
| `item` | string | Material item name | `material-tracker` | `/morning-brief` |
| `category` | string | long_lead/standard/critical_path | `material-tracker` | `/look-ahead` |
| `expected_delivery` | string | Expected delivery date | `material-tracker` | `/look-ahead`, `/morning-brief`, `submittal-intelligence` |
| `delivery_status` | string | ordered/shipped/delivered/delayed | `material-tracker` | `/morning-brief`, `cost-tracking`, `report-qa`, `submittal-intelligence` |
| `total_cost` | string | PO total cost | `material-tracker` | `cost-tracking` |
| `submittal_id` | string | Linked submittal | `material-tracker` | `project-data` cross-ref, `submittal-intelligence` |
| `cert_status` | string | pending/partial/verified/waived | `material-tracker` | `inspection-tracker` |
| `waste_factor` | number | Applied waste percentage for ordered quantity | `estimating-intelligence`, `quantitative-intelligence` | `cost-tracking` |
| `waste_factor_source` | string | "project_config" / "estimating_default" / "conservative_default" | `quantitative-intelligence` | `cost-tracking` |

---

## 9. change-order-log.json

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | CO-NNN identifier | `change-order-tracker` | `cost-tracking`, `meeting-minutes` |
| `description` | string | Change description | `change-order-tracker` | `meeting-minutes`, `/morning-brief` |
| `status` | string | draft/submitted/under_review/approved/rejected/void | `change-order-tracker` | `meeting-minutes`, `/morning-brief`, `cost-tracking`, `report-qa` |
| `cost_estimate` | string | Estimated cost impact | `change-order-tracker` | `cost-tracking` |
| `cost_approved` | string | Final approved amount | `change-order-tracker` | `cost-tracking` |
| `schedule_impact_days` | integer | Calendar days impact | `change-order-tracker` | `schedule`, `/weekly-report` |
| `affected_spec_sections` | array | Impacted spec sections | `change-order-tracker` | `cost-tracking` |
| `affected_subs` | array | Impacted subcontractors | `change-order-tracker` | `cost-tracking` |

---

## 10. inspection-log.json

### `inspection_log[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | INSP-NNN identifier | `inspection-tracker` | `/morning-brief`, `/daily-report` |
| `type` | string | Inspection type | `inspection-tracker` | `/morning-brief` |
| `result` | string | scheduled/pass/fail/conditional/cancelled | `inspection-tracker` | `/daily-report`, `/morning-brief` |
| `linked_hold_point` | string | HP-NN reference | `inspection-tracker` | — |
| `linked_spec_section` | string | CSI section | `inspection-tracker` | — |
| `location` | object | Grid/area/floor/room | `inspection-tracker` | — |

### `permit_log[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `permit_id` | string | PERMIT-NNN identifier | `inspection-tracker` | `/morning-brief` |
| `expiration_date` | string | Permit expiration | `inspection-tracker` | `/morning-brief` (alerts) |
| `status` | string | applied/issued/active/expired/renewed | `inspection-tracker` | `/morning-brief` |

---

## 11. meeting-log.json

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | MTG-NNN identifier | `meeting-minutes` | — |
| `type` | string | OAC/progress/safety/pre_install/coordination | `meeting-minutes` | `/weekly-report` |
| `action_items[]` | array | Action items with assignee, due_date, status | `meeting-minutes` | `/morning-brief` (overdue items), `meeting-minutes` (carry-forward) |

---

## 12. punch-list.json

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | PUNCH-NNN identifier | `punch-list` | `/project-dashboard`, `/daily-report` |
| `location` | object | room_number, building_area, grid_reference, floor_level | `punch-list` | `report-qa` |
| `trade` | string | Responsible trade | `punch-list` | `/project-dashboard` (by-trade chart) |
| `responsible_sub` | string | Sub company name | `punch-list` | — |
| `status` | string | open/in_progress/completed/back_charge/disputed | `punch-list` | `/project-dashboard`, `/daily-report`, `report-qa` |
| `priority` | string | A/B/C | `punch-list` | `/project-dashboard` |

---

## 13. pay-app-log.json

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `pay_applications[]` | array | Pay app records (amount, retainage, approval) | `pay-applications` | `cost-tracking`, `/weekly-report` |
| `schedule_of_values` | object | SOV by trade, phase, total | `pay-applications` | `cost-tracking` |
| `lien_waivers[]` | array | Lien waiver status by contractor | `pay-applications` | `/morning-brief`, `/weekly-report` |

---

## 14. delay-log.json

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `delay_events[]` | array | Delay records with type, duration, impact | `intake-chatbot`, `/daily-report` | `/weekly-report`, `claims-documentation`, `risk-management`, `earned-value-management`, `delay-tracker` |
| `weather_delays[]` | array | Weather-specific delay records | `intake-chatbot`, `/daily-report` | `/weekly-report`, `delay-tracker` |
| `concurrent_delays[]` | array | Overlapping delay analysis | `claims-documentation` | `/weekly-report` |

---

## 15. labor-tracking.json

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `labor_entries[]` | array | Per-worker daily labor records | `labor-tracking` | `cost-tracking` (EVM actual cost), `/daily-report` cross-validation, `earned-value-management`, `delay-tracker` |
| `crew_summaries[]` | array | Crew-level aggregation with productivity | `labor-tracking` | `/daily-report`, `/weekly-report`, `earned-value-management`, `sub-performance`, `last-planner` |
| `productivity_ratios[]` | array | Output-per-labor-hour by trade | `labor-tracking` | `/project-dashboard`, `sub-performance`, `risk-management` |
| `classifications[]` | array | Worker classifications (Davis-Bacon) | `labor-tracking` | Certified payroll |

---

## 16. quality-data.json

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `inspections[]` | array | Quality inspection results | `inspection-tracker` | `/daily-report`, `/weekly-report`, `sub-performance`, `report-qa`, `submittal-intelligence` |
| `deficiencies[]` | array | Quality deficiency records | `inspection-tracker` | `punch-list` |
| `corrective_actions[]` | array | Corrective action tracking | `inspection-tracker` | `/morning-brief`, `quality-management` |
| `quality_metrics` | object | Quality KPIs (first-pass yield, etc.) | `inspection-tracker` | `/project-dashboard`, `quality-management`, `sub-performance`, `risk-management` |

### `warranties[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `warranty_id` | string | Internal tracking ID | `document-intelligence` | `closeout-commissioning`, `cost-tracking` |
| `product_or_system` | string | Equipment tag or product name | `document-intelligence` | `closeout-commissioning` |
| `warranty_type` | string | manufacturer_equipment / manufacturer_material / workmanship / roofing_system / waterproofing_system / performance_guarantee / extended | `document-intelligence` | `closeout-commissioning` |
| `manufacturer` | string | Warranty issuer | `document-intelligence` | `closeout-commissioning` |
| `duration` | object | Component-level durations | `document-intelligence` | `closeout-commissioning` |
| `start_trigger` | string | substantial_completion / installation_date / commissioning_date | `document-intelligence` | `closeout-commissioning` |
| `registration` | object | required, deadline_days, method, status | `document-intelligence` | `closeout-commissioning`, `report-qa` |
| `exclusions` | array | Warranty exclusion categories | `document-intelligence` | `closeout-commissioning` |
| `maintenance_requirements` | array | Required maintenance to keep warranty valid | `document-intelligence` | `closeout-commissioning` |
| `claim_contact` | object | phone, email, portal | `document-intelligence` | `closeout-commissioning` |

### `system_tests[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `test_id` | string | Internal tracking ID | `document-intelligence` | `closeout-commissioning`, `quality-management` |
| `system` | string | System tested (HVAC, fire protection, electrical, plumbing, envelope) | `document-intelligence` | `closeout-commissioning` |
| `test_type` | string | TAB/hydrostatic/megger/load_bank/pressure/envelope | `document-intelligence` | `closeout-commissioning`, `quality-management` |
| `result` | string | pass/fail/conditional_pass | `document-intelligence` | `closeout-commissioning`, `quality-management` |
| `witnessed_by` | string | Third-party witness name and cert | `document-intelligence` | `closeout-commissioning` |

### `test_results[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `test_id` | string | Internal tracking ID | `document-intelligence` | `quality-management` |
| `test_type` | string | concrete_compression/steel_mtr/soil_compaction/welding_ndt/special_inspection | `document-intelligence` | `quality-management` |
| `result` | string | pass/fail | `document-intelligence` | `quality-management` |
| `spec_requirement` | string | Required value per spec | `document-intelligence` | `quality-management` |
| `actual_value` | string | Measured/tested value | `document-intelligence` | `quality-management` |

---

## 17. safety-log.json

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `recordable_incidents[]` | array | OSHA 300 recordable incidents | `safety-management` | `/morning-brief`, `meeting-minutes`, `sub-performance`, `report-qa` |
| `near_misses[]` | array | Near-miss reports | `safety-management` | `/morning-brief`, `meeting-minutes`, `sub-performance`, `report-qa` |
| `first_aid_log[]` | array | First aid only incidents | `safety-management` | — |
| `osha_300_log` | object | OSHA 300 log data (TRIR, DART) | `safety-management` | `meeting-minutes`, `/project-dashboard` |
| `toolbox_talks[]` | array | Toolbox talk records | `safety-management` | `/daily-report`, `sub-performance` |

---

## 18. daily-report-data.json

The running record of all generated daily reports. Each entry represents one day's report data.

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| (entries) | array | Structured data from every daily report | `/daily-report` | `/weekly-report`, `/project-dashboard`, `meeting-minutes`, `labor-tracking` (cross-validation), `sub-performance`, `delay-tracker`, `submittal-intelligence` |
| `weather` | object | Temperature, conditions, precipitation | `/daily-report` | `meeting-minutes` (weather summary), `delay-tracker` (weather verification) |
| `crew` | object | Subs on site, headcounts | `/daily-report` | `labor-tracking` (cross-validation), `sub-performance` |
| `schedule` | object | Delays, progress notes | `/daily-report` | `/weekly-report` |

---

## 19. daily-report-intake.json

Temporary intake buffer — raw classified field observations awaiting report generation.

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `date` | string | Intake date | `intake-chatbot` via `/log` | `/daily-report` |
| `entries[]` | array | Classified field observations | `intake-chatbot` via `/log` | `/daily-report`, `labor-tracking` (cross-validation) |

---

## Additional Data Files

### 20. cost-data.json
Budget structure, cost performance, contingency tracking. Produced by `cost-tracking`, consumed by `/project-dashboard`, `/weekly-report`, `earned-value-management`, `risk-management`, `delay-tracker`, `submittal-intelligence`.

#### Budget Initialization Fields

| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `original_contract_value` | number | Total contract amount from executed contract | `cost-tracking` (via `/cost`) | `earned-value-management`, `risk-management`, `report-qa` |
| `budget_by_division[]` | array | CSI division budget line items | `cost-tracking` (via `/cost`) | `earned-value-management`, `cost-tracking`, `risk-management` |
| `budget_by_division[].division` | string | CSI division code (e.g., "03", "05") | `cost-tracking` | `earned-value-management`, `cost-tracking` |
| `budget_by_division[].original_amount` | number | Original budget for division | `cost-tracking` | `earned-value-management` |
| `budget_by_division[].current_amount` | number | Current budget (original + approved COs) | `cost-tracking`, `change-order-tracker` | `earned-value-management`, `risk-management` |
| `budget_by_division[].committed_costs` | number | Subcontract + PO amounts | `cost-tracking` | `earned-value-management`, `risk-management` |
| `budget_by_division[].applied_cos[]` | array | Change orders applied to division | `change-order-tracker` | `cost-tracking`, `earned-value-management` |
| `contingency` | object | Contingency tracking | `cost-tracking` | `risk-management`, `earned-value-management` |
| `contingency.original_amount` | number | Starting contingency amount | `cost-tracking` | `risk-management` |
| `contingency.current_amount` | number | Remaining after draws | `cost-tracking` | `risk-management`, `earned-value-management` |
| `contingency.draws[]` | array | Each draw with date, amount, description, CO ref | `cost-tracking` | `risk-management` |
| `allowances[]` | array | Contract allowances with original vs. spent | `cost-tracking` | `cost-tracking`, `change-order-tracker` |
| `sov_lines[]` | array | Schedule of Values line items | `cost-tracking` | `earned-value-management`, `pay-app` |
| `sov_lines[].sov_line_number` | string | SOV line reference | `cost-tracking` | `earned-value-management` |
| `sov_lines[].scheduled_value` | number | Original SOV amount | `cost-tracking` | `earned-value-management` |
| `sov_lines[].percent_complete` | number | Current completion percentage | `cost-tracking` | `earned-value-management` |

### 21. visual-context.json
Photo analysis results and visual documentation metadata. Produced by `photo-analyst`, consumed by `/daily-report`.

### 22. rendering-log.json
Document rendering and extraction tracking. Produced by `document-intelligence`, consumed internally.

### 23. drawing-log.json
DWG processing tracking. Produced by `dwg-extraction`, consumed by `quantitative-intelligence`.

---

## 24. closeout-data.json

Closeout status tracking, commissioning workflow, and retainage management for project completion.

### `closeout_status`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `phase` | string | Current closeout phase: pre_substantial / substantial_punch / final_closeout / complete | `closeout-commissioning` | `/morning-brief`, `/project-dashboard`, `/weekly-report` |
| `substantial_completion_date` | string | ISO 8601 date of substantial completion | `closeout-commissioning` | `project-config` (warranty start trigger), `punch-list`, `/weekly-report` |
| `final_completion_date` | string | ISO 8601 date of final completion | `closeout-commissioning` | `/weekly-report`, `cost-tracking` |

### `closeout_status.items[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | CLO-NNN identifier | `closeout-commissioning` | `/morning-brief`, `/project-dashboard` |
| `category` | string | contract / om_manual / asbuilt / warranty / training / spare_parts / keys / certificate / testing | `closeout-commissioning` | `/project-dashboard` (by-category chart) |
| `description` | string | Closeout item description | `closeout-commissioning` | — |
| `responsible_party` | string | Subcontractor or team responsible | `closeout-commissioning` | `punch-list`, `meeting-minutes` |
| `status` | string | not_started / in_progress / submitted / approved / na | `closeout-commissioning` | `/morning-brief`, `/project-dashboard` |
| `due_date` | string | ISO 8601 due date | `closeout-commissioning` | `/morning-brief` (deadline alerts) |
| `date_submitted` | string | ISO 8601 date item was submitted | `closeout-commissioning` | — |
| `date_approved` | string | ISO 8601 date item was approved | `closeout-commissioning` | — |
| `notes` | string | Additional notes | `closeout-commissioning` | — |
| `spec_section` | string | CSI spec section reference | `closeout-commissioning` | `inspection-tracker` |

### `closeout_status.retainage`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `total_held` | number | Total retainage amount held | `closeout-commissioning`, `cost-tracking` | `/project-dashboard`, `/weekly-report` |
| `released` | number | Retainage amount released | `closeout-commissioning` | `cost-tracking`, `pay-applications` |
| `remaining` | number | Retainage still held | `closeout-commissioning` | `/project-dashboard` |
| `conditions_for_release` | array | Conditions that must be met for retainage release | `closeout-commissioning` | `/morning-brief` |

### `commissioning`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `commissioning_agent` | string | CxA name or firm | `closeout-commissioning` | `/weekly-report`, `meeting-minutes` |

### `commissioning.systems[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | CX-NNN identifier | `closeout-commissioning` | `/morning-brief`, `/project-dashboard` |
| `system` | string | System description (e.g., HVAC — RTU-1) | `closeout-commissioning` | `/project-dashboard` |
| `phase` | string | pre_functional / functional_testing / integrated_testing / seasonal_testing / complete | `closeout-commissioning` | `/morning-brief`, `/project-dashboard` |
| `pre_functional_date` | string | ISO 8601 date of pre-functional test | `closeout-commissioning` | `quality-data` cross-ref |
| `pre_functional_result` | string | pass / fail / conditional | `closeout-commissioning` | `/morning-brief` |
| `fpt_date` | string | ISO 8601 date of functional performance test | `closeout-commissioning` | `quality-data` cross-ref |
| `fpt_result` | string | pass / fail / conditional | `closeout-commissioning` | `/morning-brief`, `/project-dashboard` |
| `deficiencies` | array | List of commissioning deficiencies | `closeout-commissioning` | `punch-list` |
| `retesting_required` | boolean | Whether retesting is needed | `closeout-commissioning` | `/morning-brief` |
| `training_complete` | boolean | Whether owner training is complete | `closeout-commissioning` | — |
| `documentation_complete` | boolean | Whether documentation is complete | `closeout-commissioning` | — |
| `notes` | string | Additional notes | `closeout-commissioning` | — |

---

## 25. risk-register.json

Project risk register with identification, assessment, mitigation, contingency tracking, and version history.

### Top-level fields
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `project_id` | string | Project identifier | `risk-management` | — |
| `last_updated` | string | ISO 8601 timestamp of last update | `risk-management` | `/morning-brief` |
| `next_review_date` | string | ISO 8601 date of next scheduled review | `risk-management` | `/morning-brief` (upcoming review alert) |

### `contingency_budget`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `original_allocation` | number | Starting contingency amount (dollars) | `risk-management` | `cost-tracking`, `earned-value-management` |
| `current_remaining` | number | Remaining contingency after drawdowns | `risk-management` | `cost-tracking`, `/project-dashboard`, `/weekly-report` |
| `drawdowns[]` | array | Contingency drawdown records | `risk-management` | `cost-tracking` |
| `drawdowns[].date` | string | ISO 8601 date of drawdown | `risk-management` | `cost-tracking` |
| `drawdowns[].amount` | number | Drawdown amount (dollars) | `risk-management` | `cost-tracking` |
| `drawdowns[].risk_id` | string | R-NNN reference to triggering risk | `risk-management` | — |
| `drawdowns[].description` | string | Description of contingency use | `risk-management` | — |
| `drawdowns[].approved_by` | string | Approver name/role | `risk-management` | — |

### `risks[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | R-NNN identifier | `risk-management` | `delay-tracker`, `cost-tracking`, `/morning-brief` |
| `date_identified` | string | ISO 8601 date risk was first identified | `risk-management` | — |
| `identified_by` | string | Role or name of person who identified the risk | `risk-management` | — |
| `identification_method` | string | brainstorming / checklist / site_walkthrough / historical_review / swot / field_observation / sub_report / rfi_trend | `risk-management` | — |
| `category` | string | site_conditions / weather / labor / supply_chain / regulatory / design / subcontractor / financial / force_majeure / safety | `risk-management` | `/project-dashboard` (by-category chart) |
| `subcategory` | string | Specific risk type within category | `risk-management` | — |
| `description` | string | Clear description of the risk event | `risk-management` | `/morning-brief`, `/weekly-report` |
| `root_cause` | string | Underlying cause or driver | `risk-management` | — |
| `probability` | integer | 1-5 rating per probability scale | `risk-management` | `/project-dashboard` (heat map) |
| `impact` | integer | 1-5 rating per impact scale | `risk-management` | `/project-dashboard` (heat map) |
| `score` | integer | Calculated as probability x impact | `risk-management` | `/morning-brief`, `/project-dashboard` |
| `priority` | string | low / medium / high / critical (derived from score) | `risk-management` | `/morning-brief`, `/weekly-report` |
| `owner` | string | Person responsible for monitoring | `risk-management` | `meeting-minutes` |
| `mitigation_strategy` | string | avoidance / transfer / reduction / acceptance | `risk-management` | — |
| `mitigation_actions` | array | Specific actions being taken | `risk-management` | `meeting-minutes` |
| `contingency_plan` | string | What to do if risk materializes | `risk-management` | — |
| `trigger_conditions` | array | Observable conditions indicating materialization | `risk-management` | `/morning-brief` |
| `cost_exposure` | number | Estimated cost impact (dollars) | `risk-management` | `cost-tracking`, `earned-value-management` |
| `schedule_exposure_days` | integer | Estimated schedule impact (calendar days) | `risk-management` | `delay-tracker`, `look-ahead-planner` |
| `status` | string | identified / active / mitigating / monitoring / materialized / closed | `risk-management` | `/morning-brief`, `/project-dashboard` |
| `status_history[]` | array | Chronological status changes with date, status, notes | `risk-management` | — |
| `related_activities` | array | Schedule activities affected if risk materializes | `risk-management` | `delay-tracker`, `look-ahead-planner` |
| `related_risks` | array | Other risk IDs that are related or interdependent | `risk-management` | — |
| `linked_rfis` | array | RFI IDs related to this risk | `risk-management` | `project-data` cross-ref |
| `linked_change_orders` | array | Change order IDs related to this risk | `risk-management` | `project-data` cross-ref |
| `last_reviewed` | string | ISO 8601 date of most recent review | `risk-management` | — |
| `review_notes` | string | Notes from most recent review | `risk-management` | — |
| `probability_trend` | string | increasing / stable / decreasing | `risk-management` | `/project-dashboard` |
| `resolution_date` | string | ISO 8601 date risk was closed (null if active) | `risk-management` | — |
| `resolution_notes` | string | How the risk was resolved | `risk-management` | — |

### `closed_risks[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| (same schema as `risks[]`) | — | Resolved/retired risks moved from active register | `risk-management` | Audit trail, `/weekly-report` |

### `version_history[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `timestamp` | string | ISO 8601 timestamp | `risk-management` | Audit trail |
| `action` | string | risk-add / risk-update / risk-close / risk-review / contingency-drawdown | `risk-management` | Audit trail |
| `risk_id` | string | R-NNN reference | `risk-management` | — |
| `summary` | string | Summary of change | `risk-management` | — |

---

## 26. claims-log.json

Construction claims management — claim records, notice tracking, evidence inventory, and timeline events.

### `claims[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | CLAIM-NNN identifier | `claims-documentation` | `/morning-brief`, `/weekly-report`, `meeting-minutes` |
| `status` | string | active / pending_review / settled / denied / withdrawn / arbitration | `claims-documentation` | `/morning-brief`, `/project-dashboard` |
| `title` | string | Claim title | `claims-documentation` | `/weekly-report` |
| `type` | string | delay / cost / delay_and_cost / differing_site_conditions / constructive_change / acceleration | `claims-documentation` | — |
| `date_initiated` | string | ISO 8601 date claim was initiated | `claims-documentation` | — |
| `notice_date` | string | ISO 8601 date formal notice was sent | `claims-documentation` | — |
| `notice_deadline` | string | ISO 8601 deadline for contractual notice | `claims-documentation` | `/morning-brief` (deadline alert) |
| `notice_compliant` | boolean | Whether notice was timely per contract | `claims-documentation` | — |
| `contract_provision` | string | Contract section supporting the claim | `claims-documentation` | — |
| `description` | string | Detailed claim description | `claims-documentation` | `/weekly-report` |

### `claims[].events[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `event_id` | string | EVT-NNN identifier | `claims-documentation` | — |
| `date` | string | ISO 8601 date of event | `claims-documentation` | — |
| `description` | string | Event description | `claims-documentation` | — |
| `type` | string | trigger / impact / resolution | `claims-documentation` | — |
| `evidence` | array | Evidence references (RFI IDs, DR IDs, photo IDs) | `claims-documentation` | — |

### `claims[].schedule_impact`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `delay_days` | integer | Total delay days | `claims-documentation` | `delay-tracker` cross-ref |
| `float_consumed` | integer | Float days consumed | `claims-documentation` | — |
| `critical_path_extension` | integer | Critical path extension days | `claims-documentation` | `delay-tracker` |
| `acceleration_days` | integer | Days recovered through acceleration | `claims-documentation` | — |
| `net_schedule_impact` | integer | Net schedule impact after acceleration | `claims-documentation` | `/weekly-report` |
| `linked_delays` | array | DELAY-NNN references | `claims-documentation` | `delay-tracker` cross-ref |
| `tia_performed` | boolean | Whether time impact analysis was performed | `claims-documentation` | — |
| `fragnet_id` | string | Schedule fragnet identifier | `claims-documentation` | — |

### `claims[].damages`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `extended_general_conditions` | number | Extended GC cost (dollars) | `claims-documentation` | `cost-tracking` |
| `loss_of_productivity` | number | Productivity loss cost (dollars) | `claims-documentation` | `cost-tracking` |
| `acceleration_costs` | number | Acceleration cost (dollars) | `claims-documentation` | `cost-tracking` |
| `home_office_overhead` | number | Eichleay HOH cost (dollars) | `claims-documentation` | `cost-tracking` |
| `subcontractor_impacts` | number | Sub impact passthrough (dollars) | `claims-documentation` | `cost-tracking` |
| `equipment_costs` | number | Equipment standby/rental cost (dollars) | `claims-documentation` | `cost-tracking` |
| `material_escalation` | number | Material price escalation (dollars) | `claims-documentation` | `cost-tracking` |
| `total_claimed` | number | Total claim amount (dollars) | `claims-documentation` | `/project-dashboard`, `/weekly-report` |
| `calculation_method` | string | actual_cost / measured_mile / industry_study / eichleay | `claims-documentation` | — |
| `supporting_docs` | array | Invoice/payroll/equipment record references | `claims-documentation` | — |

### `claims[].resolution`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `status` | string | pending / negotiating / settled / denied / arbitration / litigation | `claims-documentation` | `/project-dashboard` |
| `method` | string | direct_negotiation / mediation / arbitration / litigation | `claims-documentation` | — |
| `settlement_amount` | number | Final settlement amount (dollars) | `claims-documentation` | `cost-tracking` |
| `settlement_date` | string | ISO 8601 date of settlement | `claims-documentation` | — |
| `notes` | string | Resolution notes | `claims-documentation` | — |

### `notice_log[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | NOTICE-NNN identifier | `claims-documentation` | — |
| `type` | string | delay / change / differing_site / constructive_change / acceleration | `claims-documentation` | — |
| `claim_id` | string | CLAIM-NNN reference | `claims-documentation` | — |
| `date_sent` | string | ISO 8601 date notice was sent | `claims-documentation` | `/morning-brief` |
| `deadline_date` | string | ISO 8601 contractual deadline | `claims-documentation` | `/morning-brief` (deadline alert) |
| `contract_provision` | string | Contract section requiring notice | `claims-documentation` | — |
| `sent_via` | array | Delivery methods (certified_mail, email, hand_delivery) | `claims-documentation` | — |
| `delivery_confirmed` | boolean | Whether delivery was confirmed | `claims-documentation` | — |
| `response_received` | boolean | Whether response was received | `claims-documentation` | — |
| `content_summary` | string | Summary of notice content | `claims-documentation` | — |

### `evidence_inventory[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | EVID-NNN identifier | `claims-documentation` | — |
| `type` | string | daily_report / photo / rfi / correspondence / invoice / schedule / inspection | `claims-documentation` | — |
| `date` | string | ISO 8601 date of evidence | `claims-documentation` | — |
| `description` | string | Evidence description | `claims-documentation` | — |
| `file_path` | string | Path or reference to evidence file | `claims-documentation` | — |
| `linked_claims` | array | CLAIM-NNN references | `claims-documentation` | — |
| `quality_rating` | string | tier_1 / tier_2 / tier_3 | `claims-documentation` | — |
| `verified` | boolean | Whether evidence has been verified | `claims-documentation` | — |

### `summary`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `total_active_claims` | integer | Count of active claims | `claims-documentation` | `/project-dashboard` |
| `total_claimed_amount` | number | Sum of all active claim amounts | `claims-documentation` | `/project-dashboard`, `cost-tracking` |
| `total_recovered_amount` | number | Sum of all settled/recovered amounts | `claims-documentation` | `cost-tracking` |
| `pending_notices` | integer | Count of notices awaiting response | `claims-documentation` | `/morning-brief` |
| `overdue_notices` | integer | Count of overdue notices | `claims-documentation` | `/morning-brief` |
| `next_deadline` | string | ISO 8601 date of next notice/claim deadline | `claims-documentation` | `/morning-brief` |
| `last_updated` | string | ISO 8601 timestamp | `claims-documentation` | — |

---

## 27. environmental-log.json

Environmental compliance tracking — LEED credits, SWPPP inspections, waste management, hazmat, dust/noise monitoring, and incidents.

### Top-level fields
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `project` | string | Project code identifier | `environmental-compliance` | — |
| `last_updated` | string | ISO 8601 timestamp of last update | `environmental-compliance` | — |

### `leed`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `certification_target` | string | LEED certification level (Certified / Silver / Gold / Platinum) | `environmental-compliance` | `/project-dashboard`, `closeout-commissioning` |

### `leed.credits[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | LEED credit identifier (e.g., SS-C1, MR-P1, EQ-C3) | `environmental-compliance` | `/project-dashboard` |
| `name` | string | Credit name | `environmental-compliance` | — |
| `status` | string | not_started / in_progress / documented / submitted / achieved / not_achieved | `environmental-compliance` | `/project-dashboard`, `closeout-commissioning` |
| `target_points` | integer | Points targeted for this credit | `environmental-compliance` | — |
| `current_diversion_rate` | number | Current waste diversion percentage (MR credits) | `environmental-compliance` | `/project-dashboard` |
| `documentation_complete` | boolean | Whether credit documentation is complete | `environmental-compliance` | `closeout-commissioning` |
| `notes` | string | Credit tracking notes | `environmental-compliance` | — |
| `last_review` | string | ISO 8601 date of last review | `environmental-compliance` | — |

### `leed.product_tracking[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `product_name` | string | Product name | `environmental-compliance` | — |
| `manufacturer` | string | Manufacturer name | `environmental-compliance` | — |
| `voc_content_gL` | number | VOC content in grams per liter | `environmental-compliance` | — |
| `voc_limit_gL` | number | Applicable VOC limit in grams per liter | `environmental-compliance` | — |
| `compliant` | boolean | Whether product meets VOC limit | `environmental-compliance` | `/project-dashboard` |
| `area_installed` | string | Installation location | `environmental-compliance` | — |
| `date_installed` | string | ISO 8601 date installed | `environmental-compliance` | — |
| `epd` | boolean | Has Environmental Product Declaration | `environmental-compliance` | `closeout-commissioning` |
| `hpd` | boolean | Has Health Product Declaration | `environmental-compliance` | `closeout-commissioning` |
| `data_sheet_filed` | boolean | Whether data sheet is on file | `environmental-compliance` | — |

### `swppp`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `permit_number` | string | CGP permit number | `environmental-compliance` | — |
| `noi_filed` | string | ISO 8601 date Notice of Intent filed | `environmental-compliance` | — |
| `permit_effective` | string | ISO 8601 date permit became effective | `environmental-compliance` | — |
| `not_filed` | string | ISO 8601 date Notice of Termination filed | `environmental-compliance` | `closeout-commissioning` |
| `status` | string | active / terminated | `environmental-compliance` | `/morning-brief` |

### `swppp.inspections[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | SWPPP-INS-NNN identifier | `environmental-compliance` | `inspection-log` cross-ref |
| `date` | string | ISO 8601 inspection date | `environmental-compliance` | `/daily-report` |
| `type` | string | routine_weekly / post_storm / pre_storm / quarterly | `environmental-compliance` | — |
| `inspector` | string | Inspector name | `environmental-compliance` | — |
| `findings` | string | Inspection findings summary | `environmental-compliance` | `/daily-report` |
| `deficiencies` | array | List of deficiency descriptions | `environmental-compliance` | `/morning-brief` |
| `corrective_actions` | array | Corrective action records with action, responsible, deadline, status | `environmental-compliance` | `/morning-brief` |
| `rainfall_24hr` | number | 24-hour rainfall in inches | `environmental-compliance` | `/daily-report` |
| `photos` | array | Photo file references | `environmental-compliance` | — |

### `waste_management`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `plan_in_place` | boolean | Whether waste management plan exists | `environmental-compliance` | — |
| `diversion_target` | number | Target diversion rate percentage | `environmental-compliance` | `/project-dashboard` |
| `cumulative_recycled` | number | Total tons recycled to date | `environmental-compliance` | `/project-dashboard`, `/weekly-report` |
| `cumulative_landfilled` | number | Total tons landfilled to date | `environmental-compliance` | `/project-dashboard` |
| `cumulative_diversion_rate` | number | Running diversion rate percentage | `environmental-compliance` | `/project-dashboard`, `/weekly-report`, `closeout-commissioning` |

### `waste_management.monthly_tracking[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `month` | string | YYYY-MM month identifier | `environmental-compliance` | — |
| `streams` | object | Tonnage by waste stream (concrete, wood, metal, drywall, cardboard, other_recycled, landfilled) | `environmental-compliance` | `/project-dashboard` |
| `total_recycled` | number | Total tons recycled for month | `environmental-compliance` | — |
| `total_landfilled` | number | Total tons landfilled for month | `environmental-compliance` | — |
| `diversion_rate` | number | Monthly diversion rate percentage | `environmental-compliance` | — |

### `hazmat`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `events[]` | array | Hazmat events (surveys, discoveries, abatement) with id, date, type, description, status | `environmental-compliance` | `safety-management`, `/morning-brief` |
| `active_hazards` | array | Currently active environmental hazards | `environmental-compliance` | `safety-management` |
| `training_records[]` | array | Hazmat training records with topic, date, attendees, trainer | `environmental-compliance` | `safety-management` |

### `dust_noise`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `dust_monitoring[]` | array | PM10/PM2.5 readings with date, location, reading, limit, compliant flag | `environmental-compliance` | `/daily-report`, `safety-management` |
| `noise_monitoring[]` | array | Noise readings with date, location, dBA reading, limit, compliant flag, mitigation applied | `environmental-compliance` | `/daily-report`, `safety-management` |
| `noise_variances[]` | array | Noise variance permits with conditions | `environmental-compliance` | — |
| `complaints[]` | array | Environmental complaints received with date, type, resolution | `environmental-compliance` | `/morning-brief` |

### `incidents[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `id` | string | ENV-INC-NNN identifier | `environmental-compliance` | `safety-management`, `/morning-brief` |
| `date` | string | ISO 8601 incident date | `environmental-compliance` | `/daily-report` |
| `type` | string | spill / release / contamination / violation | `environmental-compliance` | `safety-management` |
| `material` | string | Material involved | `environmental-compliance` | — |
| `quantity_estimate` | string | Estimated quantity released | `environmental-compliance` | — |
| `location` | string | Incident location description | `environmental-compliance` | — |
| `cause` | string | Root cause description | `environmental-compliance` | — |
| `environmental_media_affected` | array | Affected media (soil, water, air) | `environmental-compliance` | `safety-management` |
| `response_actions` | array | Response actions taken | `environmental-compliance` | — |
| `reportable` | boolean | Whether incident met reportable thresholds | `environmental-compliance` | `/morning-brief` |
| `agencies_notified` | array | Agencies notified (NRC, state, EPA) | `environmental-compliance` | — |
| `cleanup_verified` | boolean | Whether cleanup was verified | `environmental-compliance` | — |
| `corrective_actions` | array | Corrective actions to prevent recurrence | `environmental-compliance` | — |
| `status` | string | open / in_progress / closed | `environmental-compliance` | `/morning-brief` |
| `photos` | array | Photo file references | `environmental-compliance` | — |

---

## 28. annotation-log.json

Document annotation tracking — annotation records, annotation sets, symbol library, and layer definitions.

### `annotations[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `annotation_id` | string | ANN-NNN identifier | `document-annotation` | `drawing-control`, `rfi-preparer`, `punch-list` |
| `document_ref` | string | Sheet number or document identifier | `document-annotation` | `drawing-control` |
| `document_path` | string | File path to source document | `document-annotation` | — |
| `sheet_number` | string | Drawing sheet number (e.g., A-101, M-201) | `document-annotation` | `drawing-control` |
| `sheet_title` | string | Drawing sheet title | `document-annotation` | — |
| `annotation_type` | string | revision_cloud / text_note / comment / label / callout / symbol / dimension / zone_boundary / photo_markup / redline | `document-annotation` | — |

### `annotations[].location`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `page` | integer | PDF page number | `document-annotation` | — |
| `x` | number | X coordinate in PDF points | `document-annotation` | — |
| `y` | number | Y coordinate in PDF points | `document-annotation` | — |
| `width` | number | Annotation width in PDF points | `document-annotation` | — |
| `height` | number | Annotation height in PDF points | `document-annotation` | — |
| `grid_ref` | string | Grid reference (e.g., C-4) | `document-annotation` | `punch-list`, `inspection-tracker` |
| `level` | string | Building level | `document-annotation` | — |
| `room` | string | Room identifier | `document-annotation` | `punch-list` |
| `description` | string | Location description | `document-annotation` | — |

### `annotations[].content`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `text` | string | Annotation text content | `document-annotation` | — |
| `symbols` | array | Symbol references from symbol library | `document-annotation` | — |
| `revision_number` | string | Revision identifier (e.g., R3) | `document-annotation` | `drawing-control` |
| `markup_elements[]` | array | Markup elements: type, points/position, value, font_size, arc_radius, from/to | `document-annotation` | — |

### `annotations[]` (continued)
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `discipline` | string | architectural / structural / mechanical / electrical / plumbing / fire_protection / civil / safety / general | `document-annotation` | — |
| `color` | string | Hex color code | `document-annotation` | — |
| `line_weight` | string | heavy / medium / light | `document-annotation` | — |
| `layer` | string | Annotation layer name (RFI_REFERENCES, FIELD_NOTES, QC_MARKS, etc.) | `document-annotation` | — |
| `created_by` | string | Creator name and role | `document-annotation` | — |
| `created_date` | string | ISO 8601 creation date | `document-annotation` | — |
| `modified_date` | string | ISO 8601 last modification date | `document-annotation` | — |
| `linked_items` | object | Cross-references: rfi, asi, clash_id, punch_item, daily_report, spec_section | `document-annotation` | `rfi-preparer`, `punch-list`, `drawing-control` |
| `status` | string | active / superseded / voided / archived | `document-annotation` | `drawing-control` |
| `version_history[]` | array | Version records: version, date, action, by, notes | `document-annotation` | — |

### `annotation_sets[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `set_id` | string | ASET-NNN identifier | `document-annotation` | — |
| `name` | string | Annotation set name | `document-annotation` | — |
| `description` | string | Set description | `document-annotation` | — |
| `created_date` | string | ISO 8601 creation date | `document-annotation` | — |
| `created_by` | string | Creator name and role | `document-annotation` | — |
| `source_documents` | array | Source document references | `document-annotation` | `drawing-control` |
| `annotation_ids` | array | ANN-NNN references included in this set | `document-annotation` | — |
| `output_format` | string | annotated_pdf / annotated_image / html_view | `document-annotation` | — |
| `output_path` | string | File path to generated output | `document-annotation` | — |
| `distribution` | array | Recipient list | `document-annotation` | — |
| `status` | string | draft / generated / distributed / archived | `document-annotation` | — |

### `symbol_library`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| (keyed by symbol name) | object | Symbol definitions with type, size, fill, fill_color, label_position, border_color, head_style, dash_pattern, line_weight, reference_position | `document-annotation` | — |

### `layer_definitions[]`
| Field | Type | Description | Producers | Consumers |
|-------|------|-------------|-----------|-----------|
| `layer_name` | string | Internal layer name (e.g., RFI_REFERENCES, FIELD_NOTES) | `document-annotation` | — |
| `display_name` | string | Human-readable layer name | `document-annotation` | — |
| `default_color` | string | Hex default color for annotations on this layer | `document-annotation` | — |
| `default_visibility` | boolean | Whether layer is visible by default | `document-annotation` | — |
| `description` | string | Layer purpose description | `document-annotation` | — |

---

## Cross-File Relationship Summary

```
project-config.json ←→ (all files reference folder_mapping and project_basics)
plans-spatial.json  ←→ specs-quality.json  (location → spec requirements)
plans-spatial.json  ←→ directory.json      (location → sub scope)
schedule.json       ←→ change-order-log    (activity → CO impact)
rfi-log.json        ←→ submittal-log.json  (RFI → submittal chain)
submittal-log.json  ←→ procurement-log     (approval → procurement)
procurement-log     ←→ rfi-log.json        (delay → alternate request)
daily-report-data   ←→ labor-tracking      (headcount cross-validation)
inspection-log      ←→ specs-quality       (hold points → inspection requirements)
closeout-data.json  ←→ punch-list.json     (closeout items reference punch list completion)
closeout-data.json  ←→ quality-data.json   (commissioning test results feed closeout status)
closeout-data.json  ←→ drawing-log.json    (as-built drawing status tracked through closeout)
risk-register.json  ←→ schedule.json       (schedule risk impacts and activity exposure)
risk-register.json  ←→ cost-data.json      (cost contingency drawdowns and budget risk)
risk-register.json  ←→ delay-log.json      (materialized risks become delay events)
claims-log.json     ←→ delay-log.json      (delay events feed claims documentation)
claims-log.json     ←→ change-order-log    (disputed COs escalate to claims)
environmental-log   ←→ inspection-log      (SWPPP and environmental inspections)
environmental-log   ←→ safety-log.json     (environmental incidents cross-ref safety)
annotation-log.json ←→ drawing-log.json    (annotations reference controlled drawings)
annotation-log.json ←→ rfi-log.json        (RFI markup annotations linked to RFIs)
```
