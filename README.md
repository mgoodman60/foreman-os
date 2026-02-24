# Foreman_OS

The superintendent's operating system. A complete construction field management toolkit powered by deep document intelligence.

## What it does

Foreman_OS extracts comprehensive intelligence from your project documents — plans, specs, schedules, contracts, sub lists, geotech reports, safety plans, and more — then puts that intelligence to work across every part of your daily workflow: daily reports, 3-week look-aheads, RFI/submittal management, weekly owner reports, material tracking, vendor sourcing, and construction schedule generation.

Upload your documents once. Everything gets smarter from there.

### Core Capabilities

- **Deep document intelligence** — Three-pass extraction pipeline (metadata → structure → targeted content) pulls grid lines, room schedules, spec requirements, weather thresholds, hold points, tolerances, schedule milestones, sub directories, safety zones, SWPPP requirements, and geotechnical data
- **Conversational field intake** — Log observations throughout the day in plain language. The chatbot classifies your input, resolves sub names and locations against project intelligence, and stores everything for report generation
- **Daily reports** — Professional PDFs with AI-powered language standardization, photo captioning, smart placement, spec enrichment, and automated QA
- **3-week look-ahead** — Auto-generated lookahead schedules populated with subs, activities, materials, weather forecasts, and blocker alerts
- **RFI preparation** — Draft RFIs with auto-filled drawing references, spec sections, grid lines, and project team info
- **Submittal review** — Cross-reference submittals against spec requirements with line-by-line compliance checking and professional review comments
- **Weekly owner reports** — Aggregate daily reports into polished weekly summaries for the owner/PM
- **Material & procurement tracking** — Full lifecycle from PO through delivery through spec verification and cert tracking
- **Vendor sourcing** — Find suppliers, maintain a vendor database, track quotes and capabilities
- **Construction schedules** — Generate formatted door, hardware, fixture, finish, plumbing, and equipment schedules from extracted plan data
- **Interactive dashboards** — Weekly and project-lifetime views with charts, milestone tracking, and a built-in data chat
- **Morning briefings** — Daily context with weather, schedule, carry-forward items, delivery alerts, and pending action items
- **Project memory** — Auto-generated CLAUDE.md file that keeps Claude current on your project across sessions

## Commands

### Project Setup

#### `/set-project [name]`
Initialize a new project. Collects project basics and accepts document uploads for deep intelligence extraction. Generates the project memory file (CLAUDE.md) for session continuity.

#### `/process-docs [filename, type, or "scan"]`
Process specific documents to extract intelligence. Point it at a file, a document type, or drag a file into the chat. Classifies automatically, extracts intelligence, and merges with existing project data. Use `/process-docs scan` to see what's new or changed in your project folders before processing.

#### `/process-dwg [filename.dwg]`
Extract intelligence from AutoCAD DWG files (including Civil 3D). Compiles libredwg from source, converts DWG to DXF, and parses all entity types — survey points, utility structures, contours, property boundaries, construction keynotes, grading data — into structured project data in plans-spatial.json.

### Daily Workflow

#### `/morning-brief`
Start each day with weather, schedule context, approaching milestones, carry-forward items, delivery alerts, pending RFIs, and overdue submittals.

#### `/log [observation | clear]`
Log field observations throughout the day. Talk naturally — the chatbot handles classification, entity resolution, and enrichment. Use `/log clear` to archive today's entries and start fresh.

#### `/daily-report [date]`
Generate a daily report .docx (matching the W Principles template) with optional PDF export. Pulls from the intake log plus any additional input. Runs QA against project intelligence. Pass a past date to backfill.

#### `/amend-report [number or date]`
Make corrections or additions to a previously generated report.

### Planning & Scheduling

#### `/look-ahead [weeks]`
Generate a 3-week (or custom) lookahead schedule. Maps activities to subs, locations, materials, and weather. Flags blockers from pending RFIs, submittals, and materials.

#### `/plan [weekly|status|constraints|commitments|report]`
Last Planner System — create weekly work plans with trade foreman commitments, perform constraint analysis, track Percent Plan Complete (PPC), categorize variances, and generate weekly planning reports.

#### `/schedules [type]`
Generate formatted construction schedules from plan data: door, hardware, fixture, finish, plumbing, equipment, room, or all.

### Document Management

#### `/prepare-rfi [topic]`
Draft an RFI with auto-filled project intelligence — drawing references, spec sections, grid lines, project team. Pass "transmittal" to create a submittal transmittal instead.

#### `/submittal-review [ID]`
Review a submittal against spec requirements. Generates a compliance matrix and professional review comments. Upload a submittal PDF or reference an existing log entry.

#### `/drawings [status|add|revise|asi|audit|search|distribute]`
Drawing revision control — track current sets, process ASIs, manage superseded sheets, run field audits, and distribute updated drawings to trades.

### Reporting & Analytics

#### `/weekly-report [week-ending date]`
Aggregate daily reports into a polished weekly owner/PM summary with executive narrative, schedule status, photos, and issue tracking.

#### `/dashboard [weekly|project]`
Interactive HTML dashboard with Weekly (crew trends, weather, inspections) and Project (lifetime metrics, milestones, S-curve) tabs. Includes a built-in data chat.

### Procurement & Sourcing

#### `/material-tracker [add|status|delivery|verify|find]`
Track materials through the full procurement lifecycle. Add items, check status, log deliveries, verify against specs, track certifications. Use `/material-tracker find [material]` to search for vendors and suppliers.

### Project Closeout

#### `/closeout [status|add|checklist|commission|warranty|generate]`
Track project closeout, commissioning, and warranty items. View closeout status, initialize the master checklist, track system commissioning (pre-functional through FPT), manage warranties with expiration alerts, and generate closeout status reports for the owner/PM.

### Safety & Quality

#### `/safety [log|incident|toolbox|jsa|metrics|inspect|report]`
Comprehensive safety management — log incidents and near-misses, run toolbox talks, create JSAs, calculate TRIR/DART/EMR metrics, run safety inspections, and generate OSHA 300/301/300A logs.

#### `/quality [checklist|itp|deficiency|metrics|report]`
Quality Management System with three-phase inspection checklists by trade, ITP management, deficiency and corrective action tracking, FPIR metrics, and quality reports.

#### `/inspections [schedule|log|status|permits]`
Schedule inspections, log results, track permits, and view inspection status. Includes safety incident tracking with root cause analysis (5-Why, Fishbone), OSHA recordkeeping, and corrective action management.

#### `/change-order [add|status|log]`
Track change orders from initiation through resolution. Includes T&M tag tracking with field sign-off workflow, photo documentation, and automatic CO integration.

### Risk, Claims & Compliance

#### `/risk [add|review|report|matrix]`
Proactive risk management with 5x5 probability/impact matrix, risk register, mitigation tracking, contingency management, and monthly risk review reports.

#### `/environmental [leed|swppp|hazmat|waste|report]`
Environmental compliance management — LEED construction credits, SWPPP administration, hazardous materials procedures, waste diversion tracking, dust/noise monitoring, and environmental incident response.

#### `/claims [document|notice|package|status]`
Claims documentation system — contemporaneous record standards, photo/video evidence management, notice letter generation, schedule/cost impact documentation, and claims package assembly.

### BIM & Coordination

#### `/bim [status|clash|model|scan]`
BIM coordination for field operations — clash detection review, model-to-field verification, 4D schedule visualization, laser scanning/point cloud management, and digital twin handoff.

#### `/annotate [plan|spec|photo|rfi] [reference]`
Document annotation and markup — plan redlines, spec highlighting, photo callouts, RFI markup packages, and as-built annotations with discipline color coding.

### Field Documentation

#### `/meeting-notes [type]`
Record meeting minutes for OAC, progress, safety, and pre-installation meetings. Tracks action items with automatic carry-forward and generates .docx minutes.

#### `/punch-list [add|status|generate]`
Manage punch list items from identification through completion. Track deficiencies by area and trade, manage back-charges, and generate professional closeout reports.

#### `/delay [add|status|log]`
Track construction delays with excusable/compensable classification, critical path analysis, and time impact analysis. Supports weather methodology and contract extension documentation.

#### `/pay-app [add|status|generate]`
Manage pay applications using AIA G702/G703 format. Track schedule of values, retainage, lien waivers, and overbilling detection.

#### `/labor [log|summary|productivity|validate|payroll|cost]`
Per-worker and crew labor tracking with productivity metrics, certified payroll generation, and earned value cost integration.

#### `/sub-scorecard [sub name|all|report|compare]`
Subcontractor performance scorecards across 5 weighted dimensions — schedule adherence, quality, safety, responsiveness, and professionalism.

### Cost & Financial

#### `/cost [status|forecast|variance|invoice|report]`
Project cost management with budget structure, CPI/EAC/variance analysis, cash flow projections, and cost-loaded schedule integration.

#### `/evm [status|calculate|curve|forecast|report]`
Earned Value Management with S-curve visualization, SPI/CPI calculation, EAC/ETC forecasting, and project performance trending.

### Visualization & Intelligence

#### `/data [section]`
Project Data Intelligence dashboard. Browse and query all extracted project intelligence across 40+ sections covering spatial data, specifications, financials, and project controls.

#### `/render [type]`
Generate AI architectural renderings from project intelligence and visual context. Produces photorealistic progress renders, exterior/interior visualizations, and site context images.

#### `/site-context [gather|review]`
Gather visual context for AI rendering generation. Collects site photos, design intent, material selections, and environmental context to produce accurate renderings.

## Getting Started

1. Install the plugin
2. Run `/set-project` to configure your project and upload key documents
3. Run `/morning-brief` each morning for your daily context
4. Use `/log` throughout the day as things happen on site
5. Run `/daily-report` to generate your report (it'll show a log summary first so you can fill gaps)
6. Run `/look-ahead` to plan the next 3 weeks
7. Run `/process-docs` any time new project docs come in (use `/process-docs scan` to check for changes)
8. Run `/dashboard` to see how the project is trending
9. Run `/weekly-report` at the end of each week for the owner

## How Project Intelligence Works

When you upload project documents during `/set-project` or `/process-docs`, the plugin runs a three-pass extraction pipeline:

1. **Metadata extraction** — Reads PDF properties (creator app, title, dates) to auto-classify the document type
2. **Structural analysis** — Scans for sheet indices, tables of contents, and table headers to confirm type and guide extraction
3. **Targeted content extraction** — Pulls specific intelligence based on document type, exhaustively — every schedule, every note, every detail

This intelligence is used by every command in the system:

- `/log` resolves sub names, fills in grid lines, adds spec references
- `/daily-report` enriches narratives with locations, thresholds, hold points
- `/look-ahead` maps activities to subs, materials, and weather constraints
- `/prepare-rfi` auto-fills drawing and spec references
- `/submittal-review` pulls spec requirements for compliance checking
- `/material-tracker` verifies deliveries against spec requirements
- `/schedules` generates formatted trade schedules from extracted data
- `/morning-brief` checks weather against thresholds, flags upcoming deliveries

The more documents you upload, the smarter everything gets.

## Project Memory (CLAUDE.md)

Foreman_OS generates a `CLAUDE.md` file in your project directory that serves as working memory across sessions. It contains a snapshot of your project basics, current status, key intelligence, active issues, and available commands. This file is auto-updated whenever project data changes, so Claude always knows where things stand when you start a new conversation.

## Skills

The plugin includes forty-two specialized skills:

### Document & Data Skills
- **document-intelligence** — Three-pass document classification and extraction pipeline with exhaustive content capture, document register, transmittal tracking, RCP extraction, specification conflict detection, quantity validation workflows, and schedule-to-field automation
- **document-annotation** — PDF markup and annotated document production — plan redlines, spec highlighting, photo callouts, RFI markup packages, as-built annotations with discipline color coding and standard construction markup conventions
- **project-data** — Data backbone for storage, cross-referencing, versioning, validation, and smart retrieval across the multi-file data store
- **project-data-intel** — Project data intelligence dashboard with 40+ browsable sections covering spatial, financial, and specification data
- **quantitative-intelligence** — Bridges measurement sources (DXF, visual analysis, takeoff, text) with the project data store for quantities, assembly chains, sheet cross-references, estimate-to-field reconciliation, and assembly chain cost awareness

### Report Generation Skills
- **daily-report-format** — Core report generation with language standardization, photo intelligence, and template formatting
- **weekly-report-format** — Daily report aggregation into professional owner/PM weekly summaries
- **report-qa** — Post-generation quality check against project intelligence (daily and weekly QA checks)
- **photo-documentation** — AI-powered photo classification via Gemini Vision with auto-categorization, metadata tagging, and progress tracking

### Field Operations Skills
- **intake-chatbot** — Conversational field data classification, entity resolution, and proactive prompting
- **field-reference** — Construction field knowledge base with 21 reference documents covering equipment selection, concrete (standard and advanced), structural steel, earthwork, BMPs, MEP coordination, fire protection, building envelope, site logistics, formwork/shoring, scaffolding, masonry, waterproofing, underground utilities, paving/flatwork, crane lift planning, surveying, temporary facilities, multi-story coordination, and cross-trade coordination
- **closeout-commissioning** — Project closeout tracking, ASHRAE Guideline 0 commissioning, functional performance testing, BAS commissioning, TAB procedures, system startup sequences, and warranty management
- **safety-management** — Safety management system with incident tracking, OSHA 300/300A/301 reporting, toolbox talks, JSA/JHA creation, and safety KPIs

### Planning & Tracking Skills
- **look-ahead-planner** — Schedule-to-daily-breakdown mapping with sub, location, material, and weather resolution
- **last-planner** — Last Planner System (LPS) with weekly commitments, PPC tracking, constraint analysis, variance tracking, schedule recovery/compression, forensic schedule analysis, and DCMA 14-point assessment
- **project-dashboard** — Interactive HTML dashboard with Weekly/Project tabs and data chat
- **inspection-tracker** — Inspection scheduling, result logging, permit tracking, and safety incident investigation with OSHA recordkeeping
- **punch-list** — Punch list item tracking from identification through completion with back-charge management
- **delay-tracker** — Delay tracking with excusable/compensable classification, critical path analysis, time impact analysis, forensic documentation, concurrent delay identification, and contract extension documentation
- **sub-performance** — Subcontractor performance scorecards across 5 weighted dimensions (schedule, quality, safety, responsiveness, professionalism) with pre-qualification criteria and bid evaluation

### Procurement & Document Skills
- **material-tracker** — Full-lifecycle material management with delivery verification, cert tracking, and vendor database
- **change-order-tracker** — Change order tracking with T&M tag management, field sign-off workflow, and cost/schedule impact analysis
- **submittal-intelligence** — Spec requirement extraction, compliance matrix generation, and review comment drafting
- **rfi-preparer** — Auto-populated RFI and transmittal templates with intelligent drawing/spec reference resolution
- **meeting-minutes** — Meeting recording, action item tracking, and .docx generation for OAC and coordination meetings
- **drawing-control** — Drawing revision control with ASI processing, current set verification, and field audit tracking

### Contract, Risk & Claims Skills
- **contract-administration** — AIA/ConsensusDocs contract field guide, bond types, insurance (OCIP/CCIP/GL/builder's risk), mechanics lien law, indemnification, COI verification, dispute resolution, and subcontractor default procedures
- **risk-management** — Proactive risk identification with 5x5 probability/impact matrix, risk register, construction-specific risk categories, mitigation strategies, contingency management, weather/force majeure documentation, and monthly risk reviews
- **claims-documentation** — Contemporaneous record standards, photo/video evidence protocols, schedule/cost impact documentation, notice letter generation, Eichleay formula, concurrent delay analysis, claims package assembly, and mediation/arbitration preparation
- **environmental-compliance** — LEED v4.1 construction credits, SWPPP administration, hazardous materials (asbestos/lead/mold), waste diversion tracking, dust/air quality management, noise ordinance compliance, and environmental incident response

### Cost & Financial Skills
- **cost-tracking** — Project cost management with budget structure, CPI/EAC/variance analysis, and cash flow projections
- **earned-value-management** — EVM with S-curve visualization, SPI/CPI calculation, and project performance forecasting
- **pay-application** — AIA G702/G703 pay application management with schedule of values, retainage, four lien waiver types, and overbilling detection
- **labor-tracking** — Per-worker and crew labor tracking with productivity metrics, certified payroll, and EVM cost integration
- **estimating-intelligence** — Deep estimating knowledge base with unit cost structure, assembly-based estimating, CSI MasterFormat cost coding, quantity takeoff methods, productivity rate tables, T&M pricing verification, bid review/leveling, and value engineering

### Quality & Compliance Skills
- **quality-management** — Quality Management System (QMS) with three-phase inspection checklists (pre-install, install, post-install) organized by CSI division
- **cobie-export** — COBie v2.4 facility handover export with 18 standard worksheets mapped from project intelligence

### BIM & Coordination Skills
- **bim-coordination** — BIM execution plan, clash detection workflows, model-to-field verification, 4D scheduling, laser scanning/point clouds, drone surveys, digital twin concepts, and LOD specifications

### Visualization Skills
- **rendering-generator** — AI architectural rendering generation with comprehensive prompt engineering from project data and visual context
- **project-visual-context** — Visual context gathering for AI renderings including site context, design intent, and material selections
- **image-generation-mcp** — MCP server implementation for AI image generation using Flux 2, Google Gemini, and SVG tools

### CAD & DWG Skills
- **dwg-extraction** — AutoCAD DWG file extraction pipeline: compiles libredwg from source, converts DWG to DXF, and parses all entity types (survey points, utility structures, contours, property boundaries, construction keynotes, grading data) into structured project intelligence in plans-spatial.json

## Agents

The plugin includes eleven autonomous agents that monitor, analyze, and advise across the project intelligence data store. Agents are auto-discovered from the `agents/` directory.

### Orchestration
- **superintendent-assistant** — Top-level assistant that routes requests to the appropriate specialized agent, coordinates multi-agent workflows, and handles general project questions

### Data & Monitoring
- **data-integrity-watchdog** — Validates consistency across all 28 project intelligence JSON files — detects orphans, cross-file conflicts, schema gaps, staleness, and broken reference chains
- **project-health-monitor** — Evaluates 8 project KPIs and 5 anomaly detection rules to generate health alerts and trend analysis
- **dashboard-intelligence-analyst** — Generates project dashboard summaries, executive briefings, and narrative health reports by querying across all 28 JSON files
- **project-data-navigator** — Translates natural language questions from superintendents into structured data queries across the 28-file project intelligence store
- **deadline-sentinel** — Monitors all project deadlines across schedule milestones, submittal due dates, RFI response windows, procurement lead times, inspection prerequisites, and contract notice periods

### Field & Workflow
- **report-quality-auditor** — Automatically reviews daily and weekly reports for completeness, consistency, and accuracy against the full project data store
- **field-intelligence-advisor** — Provides contextual field intelligence by pulling together relevant data from across the project store to support real-time superintendent decisions
- **weekly-planning-coordinator** — Orchestrates the weekly lookahead planning cycle using Last Planner System principles — constraint analysis, PPC tracking, and weekly work plan generation
- **doc-orchestrator** — Coordinates multi-document extraction runs, validates extraction output, and ensures data quality after processing
- **conflict-detection-agent** — Scans for cross-discipline discrepancies across plans, specs, schedules, and field data using 25 detection rules across 8 conflict categories

## Files

The plugin creates these files in your working directory:

**Project Intelligence (Multi-File Data Store):**
- `project-config.json` — Project basics, report tracking, folder mapping, documents loaded, version history
- `plans-spatial.json` — Grid lines, building areas, floor levels, room schedule, site layout, sheet cross-references, quantities, site utilities
- `specs-quality.json` — Spec sections, key materials, weather thresholds, hold points, tolerances, contract, safety, SWPPP, geotechnical, mix designs
- `schedule.json` — Milestones, critical path, near-critical, weather-sensitive activities, long-lead items, material requirements by activity, lookahead history
- `directory.json` — Subcontractors, subcontractor assignments, vendor database, owner reports

**Document & Issue Tracking:**
- `rfi-log.json` — RFI entries with status, references, responses, schedule impact
- `submittal-log.json` — Submittal entries with review status, compliance, lead times
- `procurement-log.json` — Procurement tracking and delivery records
- `change-order-log.json` — Change order entries with cost/schedule impacts
- `inspection-log.json` — Inspection records, permit tracking, and re-inspection management (inspection_log and permit_log arrays)
- `meeting-log.json` — Meeting notes and action items
- `punch-list.json` — Punch list items with status, priority, and back-charge tracking
- `delay-log.json` — Delay records with classification, critical path analysis, and claims documentation
- `drawing-log.json` — Drawing revision control, ASI tracking, and current set status

**Financial & Labor:**
- `pay-app-log.json` — Pay application history with schedule of values and retainage
- `cost-data.json` — Budget structure, cost tracking, variance analysis, and cash flow
- `labor-tracking.json` — Worker/crew time tracking, productivity metrics, and certified payroll

**Quality:**
- `quality-data.json` — First-pass inspection results, material test records, equipment data, warranty tracking, and system test results

**Safety, Risk & Closeout:**
- `closeout-data.json` — Closeout tracking, commissioning status, and warranty management
- `safety-log.json` — Safety incidents, OSHA records, toolbox talks, and corrective actions
- `risk-register.json` — Risk entries with probability/impact scoring, mitigation plans, and contingency tracking
- `claims-log.json` — Claims documentation, notice records, evidence tracking, and claims packages
- `environmental-log.json` — LEED credits, SWPPP compliance, waste diversion, hazmat incidents
- `annotation-log.json` — Document annotations, markup history, and distribution tracking

**Visualization:**
- `visual-context.json` — Site context, design intent, and material selections for AI rendering
- `rendering-log.json` — Generated rendering history and prompt records

**Report History & Context:**
- `daily-report-data.json` — Structured report history (the "project memory")
- `daily-report-intake.json` — Running intake log for the current day
- `CLAUDE.md` — Project working memory for session continuity

## Document Types Supported

| Document | What Gets Extracted |
|----------|-------------------|
| Plans / Drawings | Grid lines, building areas, floor levels, room schedules, site layout, compass, door/hardware/finish/fixture schedules |
| Specifications | CSI divisions, material specs, weather thresholds, hold points, tolerances, testing requirements, submittal requirements |
| CPM Schedule | Milestones, critical path, near-critical, weather-sensitive activities, long-lead items, predecessors/successors |
| Contract | Key dates, LDs, working hours, documentation requirements, special requirements |
| Sub List / Bid Tab | Subcontractor directory with trades, scopes, contacts |
| Geotechnical Report | Bearing capacity, water table, compaction requirements, unsuitable soils, dewatering |
| Safety Plan | Fall protection zones, confined spaces, hot work areas, crane exclusion zones |
| SWPPP | BMP inventory, inspection triggers, documentation requirements |
| RFI Log | RFI entries with status, references, responses, schedule impact |
| Submittal Log | Submittal entries with review status, compliance, lead times |
| Vendor Quotes / Catalogs | Supplier capabilities, contact info, pricing, certifications |
| Product Data Sheets | Product specs, manufacturer data, certifications for submittal review |
