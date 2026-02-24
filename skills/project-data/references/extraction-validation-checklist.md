---
name: extraction-validation-checklist
description: Post-extraction validation checklists for all three data pipelines (document-intelligence, dwg-extraction, manual entry). Defines completeness checks, accuracy spot-checks, cross-file consistency rules, and expected field population per document type.
version: 1.0.0
---

# Extraction Validation Checklist

Post-extraction validation framework for verifying that data extraction pipelines produced correct, complete output. Consumed by the `data-integrity-watchdog` agent and the `document-intelligence` skill after every extraction run.

---

## 1. Document-Intelligence Pipeline Validation

The document-intelligence skill processes documents through a multi-pass extraction system. Each pass has specific validation checks that must be run after extraction completes.

### 1.1 Pass 1 — Metadata and Structural Analysis

Run these checks immediately after Pass 1 completes:

| Check ID | Check | How to Verify | Fail Condition |
|----------|-------|---------------|----------------|
| P1-01 | Document type classified | `project-config.json` -> `documents_loaded[].type` is not null | Type is null or "unknown" |
| P1-02 | Discipline identified | `project-config.json` -> `documents_loaded[].discipline` is populated | Discipline is null for plans/specs |
| P1-03 | Page count recorded | `documents_loaded[].page_count` > 0 | Zero or missing page count |
| P1-04 | Section structure extracted | `documents_loaded[].sections_extracted` array is non-empty | Empty sections array for specs/schedules |
| P1-05 | TOC accuracy (specs) | Extracted section count matches TOC entry count within 10% | Divergence > 10% between TOC and extracted sections |
| P1-06 | Sheet index accuracy (plans) | Extracted sheet count matches sheet index count | Missing sheets vs. index |
| P1-07 | Creator application recorded | PDF metadata `creator` field captured | Missing for digital-origin documents (acceptable for scans) |
| P1-08 | Date metadata captured | `documents_loaded[].date_loaded` is valid ISO 8601 | Invalid or missing date |

**Pass 1 Validation Logic:**
```
FOR each document in extraction batch:
  IF type == null:
    FLAG "P1-01: Document type not classified — manual classification required"
    CONFIDENCE = low
  IF type IN ["plans", "specs", "schedule"] AND discipline == null:
    FLAG "P1-02: Discipline not identified for {type} document"
  IF type == "specs" AND len(sections_extracted) < 3:
    FLAG "P1-04: Unusually few sections extracted from specs ({count})"
  IF type == "plans" AND sheet_count_extracted != sheet_index_count:
    FLAG "P1-06: Sheet count mismatch — extracted {n}, index shows {m}"
```

### 1.2 Pass 2 — Data Extraction Checks

Run these checks after structured data extraction completes:

| Check ID | Check | How to Verify | Fail Condition |
|----------|-------|---------------|----------------|
| P2-01 | Target JSON files populated | Files listed in Expected Population Matrix (Section 2) exist and have new data | Expected files empty or unchanged |
| P2-02 | Key field population rate | Count of populated vs. expected fields per document type | Population rate < 60% for primary fields |
| P2-03 | Numeric values extracted | Quantities, dimensions, and monetary values are numeric (not descriptive text) | Values like "per spec" instead of "4000 PSI" |
| P2-04 | Array fields have entries | Array fields (e.g., `spec_sections[]`, `milestones[]`) contain at least one entry | Empty arrays where data was expected |
| P2-05 | No duplicate entries | New entries do not duplicate existing entries by ID or key fields | Duplicate IDs after merge |
| P2-06 | Enum values valid | Status fields, type fields match expected enums | Unknown enum values |
| P2-07 | Date formats consistent | All dates are ISO 8601 (YYYY-MM-DD) | Mixed date formats (MM/DD/YYYY, etc.) |
| P2-08 | Version history updated | `project-config.json` -> `version_history[]` has new entry for this extraction | No version history entry |

**Field Population Rate Calculation:**
```
FOR each document type processed:
  expected_fields = LOOKUP from Expected Population Matrix (Section 2)
  populated_fields = COUNT of non-null, non-empty fields in target JSON
  population_rate = populated_fields / expected_fields * 100

  IF population_rate >= 90%: result = "PASS"
  ELIF population_rate >= 60%: result = "WARN — review for missing data"
  ELSE: result = "FAIL — significant data gaps"
```

### 1.3 Pass 3 — Cross-Reference and Enrichment Checks

Run these checks after cross-referencing completes:

| Check ID | Check | How to Verify | Fail Condition |
|----------|-------|---------------|----------------|
| P3-01 | Spec references linked | `plans-spatial.json` -> `sheet_cross_references.spec_references[]` populated | No spec references extracted from drawing notes |
| P3-02 | Detail callouts linked | `sheet_cross_references.detail_callouts[]` have valid source and target sheets | Broken callout links (target sheet not in index) |
| P3-03 | Assembly chains built | `sheet_cross_references.assembly_chains[]` have >= 2 links per chain | Single-link chains (incomplete assembly trace) |
| P3-04 | Schedule references linked | `sheet_cross_references.schedule_references[]` connect marks to schedules | Door/window marks without schedule entries |
| P3-05 | Sub names resolved | New sub references match entries in `directory.json` -> `subcontractors[]` | Unresolved sub names (not in directory) |
| P3-06 | Location references resolved | Location mentions map to `plans-spatial.json` entries (rooms, areas, grids) | Orphan location references |
| P3-07 | RFI-submittal links valid | `rfi-log.json` -> `related_submittals` IDs exist in `submittal-log.json` | Broken cross-references |
| P3-08 | Enrichment coverage | Percentage of extracted entities that received cross-reference enrichment | Enrichment rate < 40% |

**Cross-Reference Chain Validation:**
```
FOR each assembly_chain in plans-spatial.json:
  IF len(chain.links) < 2:
    FLAG "P3-03: Incomplete assembly chain {chain.id} — only {n} link(s)"
  FOR each link in chain.links:
    IF link.sheet NOT IN drawing_index[].sheet_number:
      FLAG "P3-02: Assembly chain {chain.id} references missing sheet {link.sheet}"
  IF chain.linked_schedule_activities is empty:
    INFO "P3-03: Assembly chain {chain.id} has no schedule activity linkage"
```

### 1.4 Pass 4 — Visual / Graphical Analysis Checks (Plan Sheets Only)

| Check ID | Check | How to Verify | Fail Condition |
|----------|-------|---------------|----------------|
| P4-01 | Scale calibrated | At least one scale reference extracted per sheet | No scale data for dimensioned sheets |
| P4-02 | Grid lines detected | `plans-spatial.json` -> `grid_lines` has columns and rows | Empty grid data for structural/architectural plans |
| P4-03 | Room boundaries identified | `room_schedule[]` has entries matching visible rooms | Room count < 50% of visible rooms |
| P4-04 | Dimension strings captured | Numeric dimensions extracted (not just "see detail") | No dimensions for detail sheets |
| P4-05 | Title block data extracted | Sheet number, title, discipline, revision from title block | Missing title block data |
| P4-06 | Source attribution set | All visual-extracted data has `"source": "claude_vision"` or `"source": "dxf"` | Missing source attribution |
| P4-07 | Confidence level assigned | Each extracted value has confidence: high/medium/low | Missing confidence ratings |

---

## 2. Expected Field Population by Document Type

After processing each document type, verify that the corresponding JSON files and fields have been populated. Use this matrix as the authoritative reference.

### 2.1 Construction Plans

**Target Files:** `plans-spatial.json`, `project-config.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `plans-spatial.json` -> `grid_lines.columns` | Yes | Yes (structural/arch) | Column grid identifiers (A, B, C...) |
| `plans-spatial.json` -> `grid_lines.rows` | Yes | Yes (structural/arch) | Row grid identifiers (1, 2, 3...) |
| `plans-spatial.json` -> `grid_lines.spacing` | Yes | No | Typical bay spacing |
| `plans-spatial.json` -> `building_areas[]` | Yes | Yes | Zone names with grid ranges |
| `plans-spatial.json` -> `floor_levels[]` | Yes | Yes (multi-story) | Level names with elevations |
| `plans-spatial.json` -> `room_schedule[]` | Yes | Yes (architectural) | Room numbers, names, areas |
| `plans-spatial.json` -> `sheet_cross_references.drawing_index[]` | Yes | Yes | Every sheet in the set |
| `plans-spatial.json` -> `sheet_cross_references.detail_callouts[]` | Yes | Yes | Section cuts, detail references |
| `plans-spatial.json` -> `quantities` | Yes | No | Populated by quantitative-intelligence |
| `plans-spatial.json` -> `site_utilities[]` | Yes | Yes (civil/site) | Utility runs from plan notes |
| `project-config.json` -> `documents_loaded[]` | Yes | Yes | Extraction tracking entry |

### 2.2 Specifications

**Target Files:** `specs-quality.json`, `project-config.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `specs-quality.json` -> `spec_sections[]` | Yes | Yes | CSI sections with division, section, title, key_req |
| `specs-quality.json` -> `spec_sections[].weather_thresholds` | Yes | No | Only for weather-sensitive sections |
| `specs-quality.json` -> `spec_sections[].testing` | Yes | No | Testing frequency, type, agency |
| `specs-quality.json` -> `spec_sections[].hold_points` | Yes | No | Inspection hold points |
| `specs-quality.json` -> `key_materials[]` | Yes | Yes | Material, spec_section, specification, testing |
| `specs-quality.json` -> `weather_thresholds[]` | Yes | Yes | Work type limits (temp, wind, moisture) |
| `specs-quality.json` -> `hold_points[]` | Yes | Yes | Work type, inspection name, trigger, inspector |
| `specs-quality.json` -> `safety` | Yes | No | Fall protection, confined spaces, hot work, crane zones |
| `specs-quality.json` -> `contract` | Yes | No | NTP, completion, LDs, working hours |
| `specs-quality.json` -> `mix_designs[]` | Yes | No | Only if concrete specs present |
| `specs-quality.json` -> `geotechnical` | Yes | No | Only if geotech report processed |
| `project-config.json` -> `documents_loaded[]` | Yes | Yes | Extraction tracking entry |

### 2.3 Schedule (P6 / MS Project)

**Target Files:** `schedule.json`, `project-config.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `schedule.json` -> `milestones[]` | Yes | Yes | Key dates with name, date, status |
| `schedule.json` -> `critical_path[]` | Yes | Yes | Critical activities with float = 0 |
| `schedule.json` -> `near_critical[]` | Yes | No | Activities with float < 10 days |
| `schedule.json` -> `weather_sensitive_activities[]` | Yes | No | Outdoor/weather-dependent activities |
| `schedule.json` -> `long_lead_items[]` | Yes | No | Items with lead time > 8 weeks |
| `schedule.json` -> `substantial_completion` | Yes | Yes | Contract substantial completion date |
| `schedule.json` -> `final_completion` | Yes | No | Contract final completion date |
| `schedule.json` -> `material_requirements_by_activity[]` | Yes | No | Activity-material mapping |
| `project-config.json` -> `documents_loaded[]` | Yes | Yes | Extraction tracking entry |

### 2.4 Subcontract Documents

**Target Files:** `directory.json`, `project-config.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `directory.json` -> `subcontractors[].name` | Yes | Yes | Company name |
| `directory.json` -> `subcontractors[].trade` | Yes | Yes | Primary trade |
| `directory.json` -> `subcontractors[].scope` | Yes | Yes | Contracted scope of work |
| `directory.json` -> `subcontractors[].foreman` | Yes | No | Field foreman name |
| `directory.json` -> `subcontractors[].phone` | Yes | No | Contact phone |
| `directory.json` -> `subcontractors[].email` | Yes | No | Contact email |
| `directory.json` -> `subcontractors[].start_date` | Yes | No | Mobilization date |
| `directory.json` -> `subcontractors[].status` | Yes | Yes | active/mobilized/demobilized |
| `project-config.json` -> `documents_loaded[]` | Yes | Yes | Extraction tracking entry |

### 2.5 Meeting Minutes

**Target Files:** `meeting-log.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `meeting-log.json` -> `meeting_log[].id` | Yes | Yes | MTG-NNN identifier |
| `meeting-log.json` -> `meeting_log[].type` | Yes | Yes | OAC/progress/safety/pre_install/coordination |
| `meeting-log.json` -> `meeting_log[].date` | Yes | Yes | Meeting date |
| `meeting-log.json` -> `meeting_log[].attendees` | Yes | Yes | List of attendees |
| `meeting-log.json` -> `meeting_log[].action_items[]` | Yes | Yes | Assignee, due_date, status |
| `meeting-log.json` -> `meeting_log[].decisions` | Yes | No | Key decisions made |

### 2.6 Daily Reports (Imported)

**Target Files:** `daily-report-data.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `daily-report-data.json` -> `entries[].date` | Yes | Yes | Report date |
| `daily-report-data.json` -> `entries[].weather` | Yes | Yes | Temperature, conditions, precipitation |
| `daily-report-data.json` -> `entries[].crew` | Yes | Yes | Subs on site, headcounts |
| `daily-report-data.json` -> `entries[].work` | Yes | Yes | Work performed descriptions |
| `daily-report-data.json` -> `entries[].delays` | Yes | No | Delay events if any |

### 2.7 RFI Documents

**Target Files:** `rfi-log.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `rfi-log.json` -> `rfi_log[].id` | Yes | Yes | RFI-NNN identifier |
| `rfi-log.json` -> `rfi_log[].subject` | Yes | Yes | RFI topic |
| `rfi-log.json` -> `rfi_log[].status` | Yes | Yes | draft/issued/response_received/resolved/void |
| `rfi-log.json` -> `rfi_log[].date_issued` | Yes | Yes | Date RFI was issued |
| `rfi-log.json` -> `rfi_log[].spec_section` | Yes | No | Governing spec section |
| `rfi-log.json` -> `rfi_log[].schedule_impact` | Yes | No | none/minor/major |
| `rfi-log.json` -> `rfi_log[].related_submittals` | Yes | No | Linked submittal IDs |
| `rfi-log.json` -> `rfi_log[].location` | Yes | No | Grid/area/floor references |

### 2.8 Submittal Documents

**Target Files:** `submittal-log.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `submittal-log.json` -> `submittal_log[].id` | Yes | Yes | SUB-NNN identifier |
| `submittal-log.json` -> `submittal_log[].spec_section` | Yes | Yes | CSI section number |
| `submittal-log.json` -> `submittal_log[].status` | Yes | Yes | submitted/under_review/approved/revise_and_resubmit/rejected |
| `submittal-log.json` -> `submittal_log[].date_submitted` | Yes | Yes | Submittal date |
| `submittal-log.json` -> `submittal_log[].lead_time_weeks` | Yes | No | Supplier lead time |
| `submittal-log.json` -> `submittal_log[].related_rfis` | Yes | No | Linked RFI IDs |
| `submittal-log.json` -> `submittal_log[].schedule_impact` | Yes | No | none/critical_path_blocked/lead_time_risk |

### 2.9 Pay Applications

**Target Files:** `pay-app-log.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `pay-app-log.json` -> `pay_applications[].number` | Yes | Yes | Pay app number |
| `pay-app-log.json` -> `pay_applications[].period` | Yes | Yes | Billing period |
| `pay-app-log.json` -> `pay_applications[].amounts` | Yes | Yes | Scheduled, completed, stored, retainage |
| `pay-app-log.json` -> `pay_applications[].retainage` | Yes | No | Retainage held and released |
| `pay-app-log.json` -> `schedule_of_values` | Yes | No | SOV by trade, phase, total |

### 2.10 Change Orders

**Target Files:** `change-order-log.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `change-order-log.json` -> `change_order_log[].id` | Yes | Yes | CO-NNN identifier |
| `change-order-log.json` -> `change_order_log[].description` | Yes | Yes | Change description |
| `change-order-log.json` -> `change_order_log[].status` | Yes | Yes | draft/submitted/under_review/approved/rejected/void |
| `change-order-log.json` -> `change_order_log[].cost_estimate` | Yes | Yes | Estimated cost impact |
| `change-order-log.json` -> `change_order_log[].cost_approved` | Yes | No | Final approved amount (when approved) |
| `change-order-log.json` -> `change_order_log[].schedule_impact_days` | Yes | No | Calendar days impact |
| `change-order-log.json` -> `change_order_log[].affected_spec_sections` | Yes | No | Impacted spec sections |
| `change-order-log.json` -> `change_order_log[].affected_subs` | Yes | No | Impacted subcontractors |

### 2.11 Closeout Data

**Target Files:** `closeout-data.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `closeout-data.json` -> `systems[].system_name` | Yes | Yes | Building system identifier (HVAC, Plumbing, Electrical, etc.) |
| `closeout-data.json` -> `systems[].commissioning_status` | Yes | Yes | not_started/in_progress/complete |
| `closeout-data.json` -> `systems[].oam_manual_status` | Yes | Yes | not_submitted/submitted/approved |
| `closeout-data.json` -> `systems[].warranty_status` | Yes | Yes | not_received/received/filed |
| `closeout-data.json` -> `systems[].training_status` | Yes | No | not_scheduled/scheduled/complete |
| `closeout-data.json` -> `systems[].completion_pct` | Yes | Yes | 0-100 overall closeout completion for system |
| `closeout-data.json` -> `warranties[].item` | Yes | Yes | Warranted item description |
| `closeout-data.json` -> `warranties[].sub_name` | Yes | Yes | Responsible subcontractor |
| `closeout-data.json` -> `warranties[].start_date` | Yes | Yes | Warranty start date (ISO 8601) |
| `closeout-data.json` -> `warranties[].expiration_date` | Yes | Yes | Warranty end date (ISO 8601) |
| `closeout-data.json` -> `warranties[].warranty_type` | Yes | No | manufacturer/installer/extended |
| `closeout-data.json` -> `warranties[].duration_months` | Yes | No | Warranty period in months |

### 2.12 Risk Register

**Target Files:** `risk-register.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `risk-register.json` -> `risks[].risk_id` | Yes | Yes | RSK-NNN identifier |
| `risk-register.json` -> `risks[].description` | Yes | Yes | Risk description |
| `risk-register.json` -> `risks[].category` | Yes | Yes | schedule/cost/safety/quality/external |
| `risk-register.json` -> `risks[].probability` | Yes | Yes | 0.0-1.0 likelihood |
| `risk-register.json` -> `risks[].impact` | Yes | Yes | 1-10 impact score |
| `risk-register.json` -> `risks[].status` | Yes | Yes | active/mitigated/occurred/closed |
| `risk-register.json` -> `risks[].risk_owner` | Yes | Yes | Person responsible for mitigation |
| `risk-register.json` -> `risks[].mitigation_plan` | Yes | No | Planned response description |
| `risk-register.json` -> `risks[].mitigation_status` | Yes | No | not_started/in_progress/complete |
| `risk-register.json` -> `risks[].contingency_allocated` | Yes | No | Dollar amount reserved |
| `risk-register.json` -> `risks[].contingency_spent` | Yes | No | Dollar amount used |
| `risk-register.json` -> `risks[].linked_activity_id` | Yes | No | Schedule activity this risk threatens |
| `risk-register.json` -> `risks[].trigger_date` | Yes | No | Date by which risk must be addressed |

### 2.13 Claims Log

**Target Files:** `claims-log.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `claims-log.json` -> `claims[].claim_id` | Yes | Yes | CLM-NNN identifier |
| `claims-log.json` -> `claims[].description` | Yes | Yes | Claim description |
| `claims-log.json` -> `claims[].claim_type` | Yes | Yes | time_extension/cost/acceleration/differing_conditions |
| `claims-log.json` -> `claims[].status` | Yes | Yes | draft/notice_sent/filed/under_review/negotiation/resolved/denied |
| `claims-log.json` -> `claims[].claimed_amount` | Yes | Yes | Dollar amount claimed |
| `claims-log.json` -> `claims[].claimed_days` | Yes | No | Time extension days claimed |
| `claims-log.json` -> `claims[].date_filed` | Yes | Yes | Date claim was filed (ISO 8601) |
| `claims-log.json` -> `claims[].notice_required_by` | Yes | Yes | Contractual notice deadline |
| `claims-log.json` -> `claims[].notice_sent_date` | Yes | No | Date notice was actually sent |
| `claims-log.json` -> `claims[].formal_claim_deadline` | Yes | No | Deadline for formal claim submission |
| `claims-log.json` -> `claims[].contract_notice_period_days` | Yes | No | Required notice period per contract |
| `claims-log.json` -> `claims[].documentation_completeness_pct` | Yes | No | 0-100 evidence package completeness |
| `claims-log.json` -> `claims[].related_delay_ids` | Yes | No | Linked delay-log entries |
| `claims-log.json` -> `claims[].related_co_ids` | Yes | No | Linked change order numbers |
| `claims-log.json` -> `claims[].evidence_documents[]` | Yes | No | Supporting documentation references |

### 2.14 Environmental Log

**Target Files:** `environmental-log.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `environmental-log.json` -> `leed_credits[].credit_id` | Yes | No | LEED credit identifier |
| `environmental-log.json` -> `leed_credits[].status` | Yes | No | on_track/at_risk/achieved/not_applicable |
| `environmental-log.json` -> `leed_credits[].points_available` | Yes | No | Points available for this credit |
| `environmental-log.json` -> `leed_credits[].points_achieved` | Yes | No | Points earned to date |
| `environmental-log.json` -> `swppp.inspections[].date` | Yes | Yes (if SWPPP active) | Inspection date (ISO 8601) |
| `environmental-log.json` -> `swppp.inspections[].inspector` | Yes | No | Inspector name |
| `environmental-log.json` -> `swppp.inspections[].result` | Yes | Yes (if SWPPP active) | pass/fail/pass_with_findings |
| `environmental-log.json` -> `swppp.inspections[].findings[]` | Yes | No | Inspection findings |
| `environmental-log.json` -> `swppp.inspections[].corrective_actions[]` | Yes | No | Required corrective actions |
| `environmental-log.json` -> `swppp.permit_expiration` | Yes | Yes (if SWPPP active) | Permit expiration date |
| `environmental-log.json` -> `swppp.required_frequency` | Yes | Yes (if SWPPP active) | Required inspection frequency in days |
| `environmental-log.json` -> `waste_diversion.total_waste_tons` | Yes | No | Total waste generated |
| `environmental-log.json` -> `waste_diversion.diverted_tons` | Yes | No | Waste diverted from landfill |
| `environmental-log.json` -> `waste_diversion.diversion_rate` | Yes | No | Diversion percentage |
| `environmental-log.json` -> `hazmat.incidents[].date` | Yes | No | Incident date |
| `environmental-log.json` -> `hazmat.incidents[].type` | Yes | No | spill/release/exposure/storage_violation |
| `environmental-log.json` -> `hazmat.incidents[].status` | Yes | No | open/resolved/reported_to_agency |

### 2.15 Annotation Log

**Target Files:** `annotation-log.json`

| Field Path | Expected | Required | Notes |
|-----------|----------|----------|-------|
| `annotation-log.json` -> `annotations[].annotation_id` | Yes | Yes | ANN-NNN identifier |
| `annotation-log.json` -> `annotations[].document_id` | Yes | Yes | Sheet number or document reference |
| `annotation-log.json` -> `annotations[].document_type` | Yes | Yes | plans/specs/submittals/rfis |
| `annotation-log.json` -> `annotations[].annotation_type` | Yes | Yes | comment/markup/revision_cloud/dimension_override |
| `annotation-log.json` -> `annotations[].description` | Yes | Yes | Annotation content |
| `annotation-log.json` -> `annotations[].author` | Yes | Yes | Who created the annotation |
| `annotation-log.json` -> `annotations[].assigned_to` | Yes | No | Who needs to respond |
| `annotation-log.json` -> `annotations[].date_created` | Yes | Yes | Creation date (ISO 8601) |
| `annotation-log.json` -> `annotations[].status` | Yes | Yes | open/in_review/pending_response/resolved/closed |
| `annotation-log.json` -> `annotations[].priority` | Yes | No | low/medium/high/critical |
| `annotation-log.json` -> `annotations[].linked_rfi_id` | Yes | No | RFI generated from this annotation |
| `annotation-log.json` -> `annotations[].distribution[]` | Yes | No | List of parties who received the annotation |

---

## 3. DWG Extraction Pipeline Validation

The DWG -> DXF -> JSON pipeline has its own set of validation checks, focused on CAD entity accuracy and spatial data integrity.

### 3.1 Compilation and Conversion Checks

| Check ID | Check | How to Verify | Fail Condition |
|----------|-------|---------------|----------------|
| DWG-01 | dwg2dxf binary available | File exists at `/tmp/libredwg/dwg2dxf` and is executable | Binary missing or not executable |
| DWG-02 | DXF output generated | Output `.dxf` file exists and size > 0 | Empty or missing DXF file |
| DWG-03 | DXF file parseable | `parse_dxf.py` runs without fatal errors | Parser crashes or returns no entities |
| DWG-04 | Conversion warnings logged | Warning count recorded for audit | Warnings suppressed (acceptable but should be logged) |

### 3.2 Entity Extraction Checks

| Check ID | Check | How to Verify | Fail Condition |
|----------|-------|---------------|----------------|
| DWG-05 | Entity count reasonable | Total entities > 100 for typical civil/site plan | Entity count < 10 (likely failed parse) |
| DWG-06 | Layer names extracted | Distinct layer count > 1 | All entities on layer "0" (layer mapping failed) |
| DWG-07 | Layer mapping valid | DWG layers map to recognized JSON categories | > 30% of entities on unmapped layers |
| DWG-08 | Coordinate system consistent | All coordinates in same units (inches, feet, meters) | Mixed units detected |
| DWG-09 | Coordinate range plausible | Min/max coordinates within reasonable construction site bounds | Coordinates at origin or extreme values (> 10^6) |
| DWG-10 | XDATA extraction complete | Civil 3D XDATA entities extracted where present | XDATA headers detected but data not extracted |
| DWG-11 | INSERT+ATTRIB parsed | Block insertions have associated attribute data | INSERT entities without expected ATTRIBs |
| DWG-12 | Proximity grouping valid | Grouped structures have plausible spatial relationships | Groups contain entities > 100 ft apart |

**Entity Type Distribution Check:**
```
FOR each DXF file processed:
  entity_counts = COUNT entities BY type (LINE, POLYLINE, TEXT, INSERT, DIMENSION, etc.)

  IF entity_counts["TEXT"] == 0 AND entity_counts["MTEXT"] == 0:
    FLAG "DWG-05: No text entities — annotation data missing"
  IF entity_counts["INSERT"] == 0:
    FLAG "DWG-11: No INSERT entities — block/symbol data missing"
  IF entity_counts["DIMENSION"] > 0 AND entity_counts["TEXT"] == 0:
    FLAG "DWG-05: Dimensions without text — value extraction may fail"

  LOG entity_type_distribution for audit
```

### 3.3 Spatial Data Validation

| Check ID | Check | How to Verify | Fail Condition |
|----------|-------|---------------|----------------|
| DWG-13 | Grid lines match visual | DXF grid count matches plan sheet grid count (from Pass 4) | Mismatch > 2 grid lines |
| DWG-14 | Room boundaries closed | Polylines forming rooms are closed (start == end) | Open polylines used as room boundaries |
| DWG-15 | Pipe runs connected | Pipe segments share endpoints within tolerance (0.1 ft) | Disconnected pipe segments > 20% |
| DWG-16 | Utility system completeness | Each utility type has at least one run/segment | Expected utility systems missing entirely |

### 3.4 DWG-to-JSON Merge Validation

| Check ID | Check | How to Verify | Fail Condition |
|----------|-------|---------------|----------------|
| DWG-17 | Source attribution correct | DXF-sourced entries have `"source": "dxf"` | Missing or incorrect source tag |
| DWG-18 | Priority 1 applied | DXF values override visual estimates where both exist | Visual values persisted over DXF values |
| DWG-19 | Existing data preserved | Non-DXF data in plans-spatial.json unchanged after merge | Data loss during merge |
| DWG-20 | Dual-source conflicts flagged | Conflicts between DXF and drawing notes flagged per Pattern 7 | Conflicts silently resolved without logging |

---

## 4. Manual Entry Validation

Data entered via `/set-project` and `/log` commands must pass these validation checks.

### 4.1 `/set-project` Validation

| Check ID | Check | How to Verify | Fail Condition |
|----------|-------|---------------|----------------|
| ME-01 | Project name set | `project-config.json` -> `project_basics.project_name` is non-empty | Empty project name |
| ME-02 | Folder mapping valid | All paths in `folder_mapping` point to accessible directories | Invalid or inaccessible paths |
| ME-03 | AI output folder exists | `folder_mapping.ai_output` directory exists or can be created | Cannot create data store directory |
| ME-04 | Sub entries complete | Each sub in `directory.json` has name, trade, and status | Missing required sub fields |
| ME-05 | Schedule dates valid | Milestone dates are valid ISO 8601 and in logical order | Completion date before NTP date |
| ME-06 | No duplicate subs | `directory.json` -> `subcontractors[]` has no duplicate company names | Duplicate sub entries |

### 4.2 `/log` Entry Validation

| Check ID | Check | How to Verify | Fail Condition |
|----------|-------|---------------|----------------|
| ME-07 | Entry classified | `daily-report-intake.json` -> `entries[].category` is set | Unclassified entry |
| ME-08 | Date assigned | `entries[].date` is valid ISO 8601 | Missing or invalid date |
| ME-09 | Sub reference resolved | If sub mentioned, matches `directory.json` entry | Unknown sub reference |
| ME-10 | Location reference resolved | If location mentioned, maps to `plans-spatial.json` | Unknown location reference |
| ME-11 | Numeric values validated | Headcounts, hours, quantities are positive numbers | Negative or non-numeric values |
| ME-12 | Enum values valid | Status, category, priority fields use expected values | Invalid enum values |

### 4.3 Format Validation Rules

These rules apply to all manually entered data:

```
Date Format:
  VALID:   "2025-03-15" (ISO 8601)
  INVALID: "3/15/2025", "March 15, 2025", "03-15-25"
  ACTION:  Convert to ISO 8601 before storing

ID Format:
  RFI:        "RFI-NNN" (e.g., RFI-001, RFI-042)
  Submittal:  "SUB-X-NNN" (e.g., SUB-C-005, SUB-S-002)
  CO:         "CO-NNN" (e.g., CO-001)
  Punch:      "PUNCH-NNN" (e.g., PUNCH-001)
  Inspect:    "INSP-NNN" (e.g., INSP-001)
  Procure:    "PROC-NNN" (e.g., PROC-012)
  Meeting:    "MTG-NNN" (e.g., MTG-001)
  Risk:       "RSK-NNN" (e.g., RSK-001, RSK-015)
  Claim:      "CLM-NNN" (e.g., CLM-001, CLM-004)
  Annotation: "ANN-NNN" (e.g., ANN-001, ANN-045)
  ACTION:  Auto-increment from highest existing ID if not provided

Status Enums (by record type):
  RFI:           draft | issued | response_received | resolved | void
  Submittal:     submitted | under_review | approved | revise_and_resubmit | rejected
  CO:            draft | submitted | under_review | approved | rejected | void
  Punch:         open | in_progress | completed | back_charge | disputed
  Inspection:    scheduled | pass | fail | conditional | cancelled
  Procurement:   ordered | shipped | delivered | delayed
  Sub Status:    active | mobilized | demobilized
  Risk:          active | mitigated | occurred | closed
  Risk Mitigation: not_started | in_progress | complete
  Claim:         draft | notice_sent | filed | under_review | negotiation | resolved | denied
  Closeout System: not_started | in_progress | complete
  O&M Manual:   not_submitted | submitted | approved
  Warranty:      not_received | received | filed
  Training:      not_scheduled | scheduled | complete
  Environmental: pass | fail | pass_with_findings
  Hazmat:        open | resolved | reported_to_agency
  LEED Credit:   on_track | at_risk | achieved | not_applicable
  Annotation:    open | in_review | pending_response | resolved | closed
  ACTION:  Reject unknown enum values; prompt for correction

Currency Format:
  VALID:   12500.00, 1250000, 45.50
  INVALID: "$12,500.00", "12.5K", "twelve thousand"
  ACTION:  Strip currency symbols and commas; convert to numeric
```

---

## 5. Cross-File Consistency Checks (Post-Extraction)

After any extraction run (document-intelligence, dwg-extraction, or manual entry), verify that the entire data store remains internally consistent. These checks enforce the seven cross-reference patterns defined in `cross-reference-patterns.md`.

### 5.1 Entity Reference Integrity

| Check ID | Check | Files Involved | How to Verify |
|----------|-------|----------------|---------------|
| XF-01 | Sub names consistent | `directory.json`, all log files | Every sub name in log entries matches a `subcontractors[].name` exactly |
| XF-02 | Spec sections consistent | `specs-quality.json`, `rfi-log.json`, `submittal-log.json`, `change-order-log.json` | Every `spec_section` reference maps to a `spec_sections[].section` |
| XF-03 | Location references valid | `plans-spatial.json`, `punch-list.json`, `inspection-log.json`, `rfi-log.json` | Every `location.room_number` maps to `room_schedule[].room_number` |
| XF-04 | Grid references valid | `plans-spatial.json`, all location-bearing records | Every grid reference falls within `grid_lines.columns` and `grid_lines.rows` |
| XF-05 | Schedule activity IDs valid | `schedule.json`, `plans-spatial.json` -> `assembly_chains[].linked_schedule_activities[]` | Every `activity_id` maps to a schedule.json activity |
| XF-06 | RFI-Submittal cross-refs | `rfi-log.json`, `submittal-log.json` | Every `related_submittals` ID exists in submittal-log; every `related_rfis` ID exists in rfi-log |
| XF-07 | Procurement-Submittal links | `procurement-log.json`, `submittal-log.json` | Every `submittal_id` in procurement-log maps to a submittal-log entry |
| XF-08 | CO spec sections valid | `change-order-log.json`, `specs-quality.json` | Every `affected_spec_sections` entry maps to a `spec_sections[].section` |
| XF-09 | CO sub names valid | `change-order-log.json`, `directory.json` | Every `affected_subs` entry maps to a `subcontractors[].name` |
| XF-10a | Risk activity IDs valid | `risk-register.json`, `schedule.json` | Every `linked_activity_id` maps to an `activities[].activity_id` |
| XF-11a | Closeout sub names valid | `closeout-data.json`, `directory.json` | Every `warranties[].sub_name` maps to a `subcontractors[].name` |
| XF-12a | Claims delay IDs valid | `claims-log.json`, `delay-log.json` | Every `related_delay_ids[]` entry maps to a `delays[].delay_id` |
| XF-13a | Claims CO IDs valid | `claims-log.json`, `change-order-log.json` | Every `related_co_ids[]` entry maps to a `change_orders[].co_number` |
| XF-14a | Annotation document IDs valid | `annotation-log.json`, `drawing-log.json` | Every `document_id` for `document_type == "plans"` maps to a `drawings[].sheet_number` |
| XF-15a | Annotation RFI links valid | `annotation-log.json`, `rfi-log.json` | Every `linked_rfi_id` maps to an `rfis[].rfi_number` |
| XF-16a | Closeout system tests exist | `closeout-data.json`, `quality-data.json` | Each system in `systems[]` has corresponding `system_tests[]` entries |
| XF-17a | Environmental inspection cross-ref | `environmental-log.json`, `inspection-log.json` | SWPPP inspections correlate with environmental inspection entries |

### 5.2 Cross-Reference Pattern Integrity

These checks verify that the seven codified cross-reference patterns from `cross-reference-patterns.md` remain functional after data changes.

**Pattern 1: Sub -> Scope -> Spec -> Inspection**
```
FOR each sub in directory.json -> subcontractors[]:
  VERIFY sub.trade maps to at least one specs-quality.json -> spec_sections[].division
  VERIFY hold_points[] exists for sub.trade work types
  IF sub.status == "active":
    VERIFY at least one schedule.json activity references this trade
```

**Pattern 2: Location -> Grid -> Area -> Room**
```
FOR each room in plans-spatial.json -> room_schedule[]:
  VERIFY room.building_area matches a building_areas[].name
  VERIFY room.floor_level matches a floor_levels[].name
  VERIFY building_areas[match].grids falls within grid_lines range
```

**Pattern 3: Work Type -> Weather Threshold -> Today's Weather**
```
FOR each weather_threshold in specs-quality.json -> weather_thresholds[]:
  VERIFY weather_threshold.work_type maps to at least one schedule activity OR spec section
  VERIFY min_temp, max_temp, max_wind are numeric values (not descriptive text)
  VERIFY spec_reference maps to a valid spec_sections[].section
```

**Pattern 4: Element -> Assembly Chain -> Multi-Sheet Data**
```
FOR each chain in plans-spatial.json -> assembly_chains[]:
  VERIFY all chain.links[].sheet values exist in drawing_index[]
  VERIFY chain has at least 2 links (plan + detail minimum)
  IF chain.linked_schedule_activities exists:
    FOR each linked_activity:
      VERIFY linked_activity.activity_id exists in schedule.json
```

**Pattern 5: RFI -> Submittal -> Procurement Chain**
```
FOR each rfi in rfi-log.json with related_submittals:
  VERIFY each related submittal ID exists in submittal-log.json
  FOR each linked submittal:
    CHECK if procurement-log.json has entry with matching submittal_id
    IF procurement exists:
      VERIFY chain integrity: RFI -> Submittal -> Procurement
```

**Pattern 6: Assembly -> Schedule -> Earned Value**
```
FOR each chain with linked_schedule_activities:
  VERIFY activity_id maps to schedule.json activity
  IF cost-data.json -> sov_lines[] exists:
    CHECK that assembly elements map to SOV lines for EVM tracking
```

**Pattern 7: Dual-Source Utility Reconciliation**
```
IF both document-intelligence AND dwg-extraction have run:
  FOR each utility system (storm, sanitary, water, fire, gas, electric, telecom):
    CHECK for entries in both site_utilities[] and dwg_* arrays
    IF both exist:
      VERIFY source field is set ("dwg", "notes", or "reconciled")
      FLAG any unresolved conflicts (e.g., pipe size mismatch)
    IF only one source:
      INFO "Single-source utility data for {system} — no reconciliation needed"
```

**Pattern 8: Risk -> Schedule -> Cost**
```
FOR each risk in risk-register.json -> risks[] where status == "active":
  IF risk.linked_activity_id IS NOT NULL:
    VERIFY linked_activity_id exists in schedule.json -> activities[]
    CHECK if linked activity is on critical path
  IF risk.contingency_allocated > 0:
    VERIFY total risk contingency <= cost-data.json -> contingency.original_amount
  VERIFY probability is between 0.0 and 1.0
  VERIFY impact is between 1 and 10
```

**Pattern 9: Claims -> Delay -> CO**
```
FOR each claim in claims-log.json -> claims[]:
  FOR each delay_id in claim.related_delay_ids:
    VERIFY delay_id exists in delay-log.json -> delays[]
  FOR each co_id in claim.related_co_ids:
    VERIFY co_id exists in change-order-log.json -> change_orders[]
  IF claim.notice_required_by IS NOT NULL AND claim.notice_sent_date IS NOT NULL:
    VERIFY notice_sent_date <= notice_required_by (notice compliance)
  VERIFY claimed_amount is numeric and positive
  VERIFY date sequence: date_filed <= formal_claim_deadline (if both present)
```

**Pattern 10: Environmental -> Inspection -> Safety**
```
FOR each swppp_inspection in environmental-log.json -> swppp.inspections[]:
  IF swppp_inspection.result == "fail":
    CHECK for corresponding corrective_actions[] entries
    VERIFY each corrective action has due_date and status
  CHECK if inspection date aligns with required_frequency
FOR each hazmat_incident in environmental-log.json -> hazmat.incidents[]:
  CHECK for corresponding entry in safety-log.json -> incidents[] by date and location
  VERIFY incident status is valid enum value
```

**Pattern 11: Closeout -> Quality -> Drawing**
```
FOR each system in closeout-data.json -> systems[]:
  IF system.commissioning_status IN ("in_progress", "complete"):
    VERIFY quality-data.json -> system_tests[] has entries for this system
  CHECK drawing-log.json for as-built drawings matching this system's discipline
FOR each warranty in closeout-data.json -> warranties[]:
  VERIFY warranty.sub_name exists in directory.json -> subcontractors[]
  VERIFY warranty.start_date < warranty.expiration_date
  VERIFY warranty.expiration_date is valid ISO 8601
```

**Pattern 12: Annotation -> Drawing -> RFI**
```
FOR each annotation in annotation-log.json -> annotations[]:
  IF annotation.document_type == "plans":
    VERIFY annotation.document_id exists in drawing-log.json -> drawings[].sheet_number
  IF annotation.linked_rfi_id IS NOT NULL:
    VERIFY linked_rfi_id exists in rfi-log.json -> rfis[].rfi_number
  VERIFY date_created is valid ISO 8601
  VERIFY status is valid enum (open/in_review/pending_response/resolved/closed)
```

### 5.3 Temporal Consistency

| Check ID | Check | How to Verify | Fail Condition |
|----------|-------|---------------|----------------|
| XF-10 | NTP before milestones | `specs-quality.json` -> `contract.ntp_date` < all milestone dates | Milestone before NTP |
| XF-11 | Milestones before completion | All milestones < `schedule.json` -> `substantial_completion` | Milestone after substantial completion |
| XF-12 | RFI dates logical | `date_issued` <= `date_responded` <= `date_resolved` | Date sequence violations |
| XF-13 | Submittal dates logical | `date_submitted` <= `date_reviewed` <= `date_approved` | Date sequence violations |
| XF-14 | CO dates logical | `date_submitted` <= `date_approved` (if approved) | Approval before submission |
| XF-15 | Inspection dates in range | All inspection dates within NTP to completion window | Inspections outside project timeline |
| XF-16 | Daily reports sequential | No gaps > 5 business days in `daily-report-data.json` entries | Extended reporting gaps |

---

## 6. Confidence Scoring Framework

Every extracted data element receives a confidence score based on source quality, extraction method, and validation results. This framework standardizes scoring across all pipelines.

### 6.1 Confidence Tiers

| Tier | Score Range | Criteria | Auto-Accept | Human Review |
|------|------------|----------|-------------|--------------|
| **High** | > 90% | Clear structured source; all expected fields populated; passes all validation checks; source is digital-native (not scanned) | Yes | No |
| **Medium** | 60-90% | Most fields populated; some from inference or fuzzy matching; minor validation warnings; source has some quality issues | Yes (with flags) | Recommended for critical data |
| **Low** | < 60% | Missing critical fields; significant validation failures; source is poor quality (scanned, handwritten, damaged) | No | Required |

### 6.2 Per-Source Confidence Defaults

| Source | Default Confidence | Rationale |
|--------|-------------------|-----------|
| DXF extraction (`"source": "dxf"`) | High (95%) | CAD geometry is precise, machine-generated |
| Digital PDF text extraction | High (90%) | Structured text, no OCR errors |
| Claude Vision extraction (`"source": "claude_vision"`) | Medium (75%) | Good for layout and labels; may miss fine detail |
| OCR / Tesseract extraction | Medium (65%) | Prone to character substitution errors |
| Scanned document extraction | Low (55%) | Quality depends on scan resolution and document condition |
| Manual entry via `/set-project` | High (95%) | User-provided; assumed accurate |
| Manual entry via `/log` | Medium-High (85%) | User-provided but may be informal/incomplete |
| Inferred / fuzzy-matched data | Low (50%) | Requires verification |

### 6.3 Confidence Adjustment Rules

Apply these adjustments to the default confidence:

```
Positive Adjustments (increase confidence):
  +10%  Cross-file corroboration (same value in multiple files)
  +5%   Value matches expected format exactly
  +5%   Numeric value within expected range for field type
  +5%   DXF + visual both agree on value

Negative Adjustments (decrease confidence):
  -15%  Validation check failed (any P*, DWG-*, ME-*, XF-* check)
  -10%  Value extracted from poor-quality source region
  -10%  Fuzzy match used (Levenshtein distance > 2)
  -5%   Value conflicts with another source (unreconciled)
  -5%   Missing expected companion fields (e.g., dimension without units)

Floor: Confidence cannot drop below 10%
Ceiling: Confidence cannot exceed 99%
```

### 6.4 Human Review Trigger Rules

Flag for human review when ANY of the following conditions are true:

```
TRIGGER human_review WHEN:
  - Final confidence < 60% on any required field
  - Critical field is missing (field marked "Required" in Section 2)
  - Cross-file consistency check fails (any XF-* check)
  - Dual-source conflict unresolved (Pattern 7 conflict)
  - Quantity discrepancy > 10% between sources
  - New entity created by inference (sub name, location, spec section)
  - Assembly chain has broken links (P3-02 or P3-03 failure)
  - Financial values extracted (cost, contract amounts) — always flag
  - Schedule critical path modified — always flag
  - Safety data modified (fall protection zones, confined spaces) — always flag
```

### 6.5 Confidence Reporting Format

After each extraction run, generate a confidence summary:

```
EXTRACTION CONFIDENCE REPORT
==============================
Document: "Riverside Medical Center - Structural Plans S1-S12"
Type: Construction Plans | Discipline: Structural
Extraction Date: 2025-03-15

Overall Confidence: 82% (Medium)

By Section:
  grid_lines:              95% (High)   — DXF source, fully validated
  building_areas:          85% (Medium) — Claude Vision, 4/5 areas detected
  room_schedule:           70% (Medium) — Claude Vision, some rooms uncertain
  sheet_cross_references:  90% (High)   — Text extraction, all callouts linked
  quantities:              75% (Medium) — Mixed sources, 2 discrepancies flagged

Validation Results:
  Passed: 18/22 checks
  Warnings: 3 (P2-02, P4-03, P4-07)
  Failed: 1 (P3-03 — Assembly chain CHAIN-004 has single link)

Human Review Needed:
  - room_schedule: Rooms 201-205 uncertain boundaries (confidence 55%)
  - quantities.concrete[3]: Footing F4 volume discrepancy 12% between sources
  - assembly_chains[3]: CHAIN-004 incomplete — missing detail sheet link
```

---

## 7. Common Extraction Errors and Remediation

Documented patterns of extraction failures encountered in practice, organized by pipeline and frequency. Each error includes root cause, detection method, and remediation steps.

### 7.1 Document-Intelligence Errors

#### Error DI-001: Misclassified Document Type
**Frequency:** Common (especially for multi-section documents)
**Root Cause:** Document contains mixed content (e.g., specs with embedded schedules, plans with spec notes on cover sheet).
**Detection:** P1-01 check fails, or extracted data appears in wrong JSON file.
**Remediation:**
```
1. Check documents_loaded[].type against actual content
2. If misclassified, update type field manually
3. Re-run extraction with corrected classification
4. Verify target JSON files updated correctly
```

#### Error DI-002: Merged/Split Table Cells
**Frequency:** Common (specs with complex tables)
**Root Cause:** PDF table extraction misinterprets merged cells, causing data to shift columns or rows to merge.
**Detection:** P2-03 check — values appear in wrong fields; numeric values contain text from adjacent cells.
**Remediation:**
```
1. Identify affected table by reviewing extracted data for field misalignment
2. Compare extracted values against source PDF page visually
3. Manually correct misaligned values in target JSON
4. Add coverage_notes entry: "Table extraction corrected manually — merged cells on page {n}"
```

#### Error DI-003: OCR Errors in Scanned Documents
**Frequency:** Common (scanned specs, old drawings)
**Root Cause:** Low scan resolution, poor contrast, handwritten annotations, stamps overlapping text.
**Detection:** P2-03 check — numeric values have character substitution (0/O, 1/l, 5/S, 8/B).
**Common Substitutions:**
```
  "0" <-> "O" <-> "D"     (zero, letter O, letter D)
  "1" <-> "l" <-> "I"     (one, lowercase L, capital I)
  "5" <-> "S"              (five, letter S)
  "8" <-> "B"              (eight, letter B)
  "6" <-> "G"              (six, letter G)
  "#5" <-> "#S" <-> "45"   (rebar size — common in structural)
  "4000" <-> "40OO"        (PSI value — O instead of zero)
```
**Remediation:**
```
1. Flag all OCR-sourced numeric values with confidence < 70%
2. Cross-check critical values (PSI, rebar sizes, dimensions) against specs
3. Apply OCR correction rules for known substitution patterns
4. Set source = "ocr_corrected" and log corrections in version_history
```

#### Error DI-004: Multi-Sheet Assembly Chain Breaks
**Frequency:** Moderate (complex structural/MEP plan sets)
**Root Cause:** Detail callouts reference sheets not in the processed set, or callout text is partially obscured.
**Detection:** P3-02 and P3-03 checks — assembly chains with broken links or single links.
**Remediation:**
```
1. List all assembly chains with < 2 links
2. For each broken chain:
   a. Check drawing_index for the target sheet
   b. If sheet exists but link broken: re-extract callout data from source sheet
   c. If sheet missing from set: flag as "incomplete — sheet {n} not processed"
3. Mark affected chains with confidence = "low" until resolved
4. NOTE: Do not delete broken chains — they indicate work needed
```

#### Error DI-005: Specification Section Numbering Mismatch
**Frequency:** Moderate
**Root Cause:** Document uses non-standard CSI numbering, or old (5-digit) vs. new (6-digit) MasterFormat.
**Detection:** P2-06 check — spec section numbers don't match expected CSI format.
**Remediation:**
```
1. Identify numbering convention used in document
2. If old MasterFormat (5-digit): convert to 6-digit equivalent
   Example: "03300" -> "03 30 00"
3. If custom numbering: create mapping table in coverage_notes
4. Ensure all downstream references use the normalized format
```

### 7.2 DWG Extraction Errors

#### Error DWG-001: Civil 3D Proprietary Objects
**Frequency:** Common (Civil 3D files)
**Root Cause:** Civil 3D stores data in proprietary AEC objects that standard DXF parsers cannot read (corridors, surfaces, pipe networks stored as proxy entities).
**Detection:** DWG-05 check — low entity count despite large file size; DWG-10 — XDATA headers without data.
**Remediation:**
```
1. Check DXF output for ACAD_PROXY_ENTITY entries
2. If proxy entities found: extract available text/attribute data from associated blocks
3. Fall back to visual pipeline (Claude Vision) for spatial data
4. Log: "Civil 3D proprietary objects detected — visual fallback used"
5. Set source = "visual_fallback" for affected entries
```

#### Error DWG-002: Coordinate System Offset
**Frequency:** Moderate (survey-based drawings)
**Root Cause:** Drawing uses state plane or UTM coordinates with large offset values instead of project-relative coordinates.
**Detection:** DWG-09 check — coordinate values in millions (state plane) or coordinates all near origin with tiny differences.
**Remediation:**
```
1. Detect coordinate range: if min_x or min_y > 100000, likely state plane
2. Identify base point or origin offset from DXF header or title block
3. Apply offset to normalize coordinates to project-relative system
4. Document transformation in plans-spatial.json metadata
5. Flag: "Coordinate system transformed from state plane — verify accuracy"
```

#### Error DWG-003: Missing Layer Mapping
**Frequency:** Moderate
**Root Cause:** Non-standard layer naming conventions; layers named in language other than English; custom company standards.
**Detection:** DWG-07 check — high percentage of entities on unmapped layers.
**Remediation:**
```
1. Export unique layer name list
2. Attempt pattern matching:
   - "*STORM*", "*STM*", "*SD*" -> storm drainage
   - "*WATER*", "*WTR*", "*W-*" -> water
   - "*SEWER*", "*SAN*", "*SS*" -> sanitary
   - "*GAS*", "*G-*" -> gas
   - "*ELEC*", "*E-*", "*POWER*" -> electrical
   - "*TELE*", "*COMM*", "*T-*" -> telecom
3. For unmapped layers: prompt superintendent for classification
4. Store custom mapping in project-config.json for reuse
```

#### Error DWG-004: INSERT Blocks Without Attributes
**Frequency:** Moderate
**Root Cause:** Blocks defined without ATTDEF (attribute definitions); data stored in nested entities or XDATA instead.
**Detection:** DWG-11 check — INSERT entities found but ATTRIB count is zero.
**Remediation:**
```
1. Check if block data is in XDATA instead of ATTRIBs
2. Check for nested TEXT/MTEXT entities within block boundary
3. Use proximity-based grouping to associate nearby text with block insertion point
4. Log: "Block attributes extracted via proximity grouping — verify accuracy"
```

### 7.3 Cross-Pipeline Errors

#### Error XP-001: Date Format Inconsistency
**Frequency:** Very Common
**Root Cause:** Different source documents use different date formats; extraction preserves source format instead of normalizing.
**Detection:** ME-08 and XF-12/13/14 checks — date comparison failures due to format mismatch.
**Common Formats Encountered:**
```
  "2025-03-15"     ISO 8601 (correct format)
  "3/15/2025"      US format (MM/DD/YYYY)
  "15/3/2025"      European format (DD/MM/YYYY)
  "March 15, 2025" Long format
  "03-15-25"       Short format (ambiguous century)
  "15-Mar-2025"    Mixed format
```
**Remediation:**
```
1. Detect format by pattern matching
2. Convert ALL dates to ISO 8601 (YYYY-MM-DD) before storing
3. For ambiguous dates (e.g., "03/04/2025" — March 4 or April 3?):
   Flag for human review with both interpretations
4. Add format detection to extraction pipeline pre-processing
```

#### Error XP-002: Currency and Number Format Issues
**Frequency:** Common
**Root Cause:** Source documents include currency symbols, commas, parentheses (for negatives), or text descriptions instead of numeric values.
**Detection:** P2-03 check — numeric fields contain non-numeric characters.
**Remediation:**
```
1. Strip: "$", ",", " " from currency values
2. Convert: "(1,234.56)" -> -1234.56 (accounting negative notation)
3. Convert: "12.5K" -> 12500, "1.2M" -> 1200000
4. Reject: "per spec", "see contract", "TBD" — set value to null and flag
5. Store all monetary values as plain numbers (no formatting)
```

#### Error XP-003: Duplicate Entity Creation
**Frequency:** Moderate (especially during re-extraction)
**Root Cause:** Re-processing a document creates new entries instead of updating existing ones; ID generation doesn't check for existing entries.
**Detection:** P2-05 check — duplicate IDs or duplicate key field combinations.
**Remediation:**
```
1. Before inserting: check if entry with same ID or key fields exists
2. If duplicate found:
   a. Compare field values
   b. If identical: skip insertion (true duplicate)
   c. If different: merge (prefer newer values) and log changes in version_history
3. For array fields: use set-based merge (no duplicate items)
4. Add extraction_run_id to all entries to track which run produced them
```

#### Error XP-004: Orphan References After Partial Extraction
**Frequency:** Moderate
**Root Cause:** Processing one document creates references to entities in another document that hasn't been processed yet (e.g., specs reference sub names not yet in directory).
**Detection:** XF-01 through XF-09 checks — references to non-existent entities.
**Remediation:**
```
1. Do NOT treat orphan references as errors during initial setup
2. Track orphans in a separate validation queue
3. After each new document processed: re-check orphan queue
4. After all known documents processed: remaining orphans are true errors
5. Report orphan age (how long since reference was created)
```

---

## 8. Validation Execution Protocol

### 8.1 When to Run Validations

| Trigger | Checks to Run | Priority |
|---------|---------------|----------|
| After `/process-docs` | Pass 1-4 checks, Section 2 matrix, Section 5 cross-file | High |
| After `/process-dwg` | Section 3 DWG checks, DWG merge checks, Pattern 7 | High |
| After `/set-project` | Section 4.1 manual entry checks, Section 5.1 entity refs | Medium |
| After `/log` entry | Section 4.2 log entry checks | Low |
| After any `/rfis`, `/submittals`, `/change-order` | Section 5.1 entity refs, Section 5.2 pattern checks | Medium |
| Weekly integrity scan | Full Section 5 cross-file checks, Section 5.3 temporal | Medium |
| Before `/daily-report` generation | Quick check: intake data complete, sub refs valid | High |
| Before `/weekly-report` generation | Full cross-file consistency, confidence summary | High |

### 8.2 Validation Output Format

Every validation run produces a structured report:

```
VALIDATION REPORT
==================
Run ID: VAL-2025-03-15-001
Trigger: /process-docs (Structural Plans S1-S12)
Timestamp: 2025-03-15T14:30:00Z

SUMMARY
  Total Checks: 45
  Passed: 38 (84%)
  Warnings: 5 (11%)
  Failed: 2 (4%)

FAILURES (require action)
  [P3-03] Assembly chain CHAIN-004 has only 1 link (expected >= 2)
    File: plans-spatial.json -> sheet_cross_references.assembly_chains[3]
    Action: Process detail sheet S5.2 to complete chain

  [XF-01] Sub "Martinez Plumbing" referenced in extraction but not in directory
    File: directory.json -> subcontractors[]
    Action: Add sub via /set-project or verify name spelling

WARNINGS (review recommended)
  [P2-02] Field population rate 72% for plans-spatial.json (threshold: 60%)
  [P4-03] Room count 15 detected vs 22 expected (68% coverage)
  [P4-07] 3 quantity values missing confidence ratings
  [DWG-20] Pipe size conflict: drawing notes "8-inch PVC" vs DXF ATTRIB "6-inch PVC"
    Location: Storm drain run SD-03, Grid C-5
  [XF-16] Daily report gap: no reports from 2025-03-10 to 2025-03-14

PASSED (sample)
  [P1-01] Document type classified: Construction Plans
  [P1-02] Discipline identified: Structural
  [P2-07] All dates in ISO 8601 format
  [XF-05] All schedule activity IDs valid
  ...

CONFIDENCE SUMMARY
  Overall extraction confidence: 82% (Medium)
  Human review items: 3
```

### 8.3 Validation Check Priority

When time-constrained (e.g., superintendent needs report NOW), run checks in this priority order:

1. **Critical** (always run): P1-01, P1-02, P2-01, P2-05, ME-01, XF-01, XF-06
2. **High** (run if time permits): P2-02 through P2-08, P3-01 through P3-04, DWG-05 through DWG-12
3. **Medium** (run during scheduled scans): Full Section 5 cross-file checks, Section 5.3 temporal
4. **Low** (run weekly): P4 visual checks, DWG spatial validation, confidence recalculation

---

## Consuming Skills

This reference document is consumed by:
- `data-integrity-watchdog` agent — runs validation checks automatically after extraction events
- `document-intelligence` skill — self-validates after each extraction pass
- `project-data` skill — validates on read/write operations
- `report-qa` skill — validates data completeness before report generation
- `dwg-extraction` skill — validates DWG pipeline output
