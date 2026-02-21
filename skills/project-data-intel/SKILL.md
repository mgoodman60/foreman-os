---
name: project-data-intel
description: >
  Comprehensive Project Data Intelligence dashboard — the single source of truth for ALL
  extracted project data. Template-based architecture with 40+ sections covering building data,
  quantities, financials, specifications, project controls, spatial analysis, and AI rendering.
  Triggers: "/data", "show me all the data", "project intelligence", "room browser",
  "quantity dashboard", "material calculator", "bid comparison", "project brain dashboard",
  "show everything we know", "data dashboard", "what data do we have".
version: 3.0.0
---

# Project Data Intelligence (v3.0) — SKILL Documentation

## Overview

Comprehensive extraction and intelligence system for construction project documents.

## 1. Philosophy: "No Data Left Behind"

The project-data-intel skill is the **single source of truth** for all extracted construction project data. It operates on a universal principle: every piece of information captured during project setup, document processing, and field operations should be **searchable, viewable, and actionable** from a single, role-aware interface.

Key design principles:
- **Template-based architecture**: Static HTML template ships with the plugin, dynamic data is injected
- **Project-agnostic**: Works for any building type (senior care, office, industrial, healthcare, etc.)
- **Incremental updates**: Only changed data is re-serialized; unchanged sections remain cached
- **Role-aware rendering**: Superintendent, PM, Owner, and Architect each see customized views
- **AI-native**: Chatbot and rendering system leverage Anthropic API for context-aware insights
- **Offline-capable**: Keyword search fallback when API unavailable

---

## 2. Architecture: Template + Data Injection

The v3.0 dashboard uses a **separation of concerns** model:

### File Structure
```
AI - Project Brain/
├── {PROJECT_CODE}_Data_Intel.html        ← Static template (10,000+ lines, generated once)
├── {PROJECT_CODE}_data.js                ← Dynamic data payload (regenerated each run)
├── references/
│   └── data-intel-template.html           ← Master template in plugin (never regenerated)
└── logs/
    └── data-intel-generation.log          ← Audit trail
```

### Template Lifecycle
1. **First run**: Copy `data-intel-template.html` from plugin → `{PROJECT_CODE}_Data_Intel.html`
2. **Subsequent runs**: Never touch the HTML file; only regenerate `{PROJECT_CODE}_data.js`
3. **Rationale**: Template is stable (~10,000 lines), data evolves rapidly. Decoupled updates reduce file size and generation time.

### Data Payload Structure (data.js)
```javascript
const PROJECT_DATA = {
  // Core project metadata and configuration
  config: {
    projectCode, projectName, address, buildingType, occupancy,
    company, startDate, endDate, architect, pm, super, status
  },

  // Spatial & geometric data
  spatial: {
    gridLines: { x: [...], y: [...] },
    buildingAreas: { footprint, perimeter, floors, zones },
    rooms: [{id, name, area, type, occupancy, finishes, doors, equipment}],
    floorPlans: [{floor, gridRef, area, roomCount}]
  },

  // Building specifications and systems
  specs: {
    building: {structure, foundation, roof, exterior, interior},
    pemb: {supplier, model, dimensions, frames, reactions, design_loads},
    cfs: {profile, gauge, spacing, height},
    concrete: {bearing, sog_interior, sog_exterior, rebar, mixes, anchor_bolts, testing},
    mep: {
      equipment: [
        {
          id: "RTU-1", tag: "RTU-1", type: "Rooftop Unit",
          discipline: "mechanical",    // mechanical|plumbing|electrical|fire_protection
          system: "hvac",              // hvac|exhaust|plumbing|electrical_power|lighting|fire
          description: "10-Ton Rooftop Unit",
          location: { grid: "C-D/3-4", room: null, mounting: "Roof" },
          capacity: { cooling_tons: 10, heating_mbh: 250, airflow_cfm: 4000 },
          electrical: { voltage: 208, phase: 3, mca: 48, mocp: 60 },
          served_rooms: ["101","102","103"],
          manufacturer: null, model: null,
          spec_section: "23 81 26", source_sheet: "M-301"
        }
      ],
      panels: [{
        panel: "LP-1", location: "Electrical Room 110",
        voltage: "208/120V", phase: 3, wires: 4,
        main_breaker_amps: 225, bus_rating_amps: 225,
        fed_from: "MDP", mounting: "surface", aic_rating: 22000,
        circuits: [{number: 1, breaker_amps: 20, poles: 1, description: "Lighting 101-103", va: 1800, phase: "A"}],
        totals: {connected_va: 45000, demand_va: 31500, spare_breakers: 6, space_slots: 4}
      }],
      single_line: {
        utility_service: {voltage: 208, phase: 3, service_amps: 800},
        main_switchboard: {rating_amps: 800, main_breaker_amps: 800},
        transformers: [], distribution_tree: [],
        generator: null, ats: null, ups: null
      },
      fixtures: {
        lighting: [{mark: "A", description: "2x4 LED Troffer", wattage: 40, lumens: 5000, cct_k: 4000, mounting: "recessed", quantity: 48}],
        plumbing: [{tag: "WC-1", type: "water_closet", manufacturer: null, model: null, mounting: "wall-hung", flush_gpf: 1.28, ada: true, quantity: 12}]
      },
      distribution: {
        duct_mains: [{size: "24x12", type: "supply", from_equipment: "RTU-1", material: "galvanized"}],
        pipe_mains: [{system: "domestic_cold", size: "2\"", material: "copper"}]
      },
      fire_protection: {
        system_type: "wet", design_standard: "NFPA 13", hazard_class: "Light",
        riser: {location: "Mech Room 110", size: "6\""}, fdc: {location: "East exterior", type: "Siamese"},
        heads: [{type: "concealed_pendant", temp_rating: "155F", k_factor: 5.6, coverage_sqft: 225}],
        fire_pump: null
      },
      device_counts: [{room: "101", duplex: 6, gfci: 2, dedicated: 1, data_telecom: 3}],
      conflicts: [],
      extraction_coverage: {
        sheets_processed: [],
        total_equipment_count: 0,
        completeness_pct: 0
      }
    },
    finishes: {flooring, wall_finishes, ceiling, paint, acoustical},
    doors: [{opening, type, material, hardware, schedule, supplier}],
    windows: [{opening, type, material, schedule, supplier}],
    casework: [{id, location, type, material, supplier}]
  },

  // Schedules and timeline
  schedule: {
    baseline: [{task, duration, start, finish, preds, slack, critical}],
    milestones: [{event, plannedDate, actualDate, status}],
    critical_path: [],
    float_analysis: {},
    procurement_gantt: [{item, supplier, orderDate, deliveryDate, duration}]
  },

  // Project directory & contacts
  directory: {
    owner: [{name, role, phone, email, address}],
    gc: [{name, company, phone, email}],
    architect: [{name, company, phone, email}],
    engineers: [{discipline, name, company, phone, email}],
    subs: [{trade, company, name, phone, email, contract}],
    suppliers: [{category, name, contact, phone, email, terms}],
    inspectors: [{agency, contact, phone, email}],
    equipment_operators: [{equipment, name, phone, license}]
  },

  // Procurement & change control
  submittals: {
    status_summary: {pending, review, approved, rejected, deferred},
    pipeline: [{id, item, supplier, submitted, days_in_review, status, approver, notes}]
  },

  procurement: {
    po_log: [{po_number, supplier, item, quantity, unit_price, total, date, status}],
    material_tracking: [{item, po, location, delivery_date, received, notes}],
    vendor_quotes: [{item, vendors: [{name, price, delivery, lead_time}]}],
    alerts: [{priority, item, issue, action_required, due_date}]
  },

  // Hold points & inspections
  inspections: {
    hold_points: [{hp_id, description, trigger, responsible, status, date_completed}],
    test_results: [{test_id, type, location, result, pass_fail, engineer, date}],
    third_party: [{agency, type, scope, inspection_date, result, notes}],
    photo_log: [{id, location, date, category, photographer, notes}]
  },

  // Daily operations
  dailyReports: [{date, superintendent, weather, temp, crew_size, work_summary, issues, safety_events}],

  // Request for Information
  rfis: {
    log: [{rfi_id, date_submitted, question, submitted_by, assigned_to, days_open, response, date_resolved}],
    categories: {design, constructability, materials, coordination, other}
  },

  // Meetings & coordination
  meetings: [{date, type, attendees, agenda, decisions, action_items}],

  // Change management
  changeOrders: [{co_id, description, cost_impact, schedule_impact, status, date, approvals}],

  // Delays & impacts
  delays: [{id, event, cause, trade, duration_days, impact, mitigation, status}],

  // Pay applications & financials
  payApps: {
    summary: {total_contract, total_completed, percent_complete, total_invoiced, retainage},
    history: [{period, contractor, amount, completed_value, retainage, approved_date}]
  },

  // Punch list & closeout
  punchList: [{id, location, item, trade, priority, assigned_to, status, due_date}],

  // Visual context (optional)
  visualContext: {
    site_photos: [{date, location, category, photographer, file_reference}],
    progress_photos: [{date, phase, photographer, file_reference}],
    as_built_markup: [{drawing, date, marked_up_by, file_reference}]
  },

  // AI rendering requests (optional)
  renderings: [{prompt, type, model, generated_date, ai_image_reference}]
};

const API_KEYS = {
  anthropic: process.env.ANTHROPIC_API_KEY || '',
  gemini: process.env.GEMINI_API_KEY || '',
  flux2: process.env.FLUX2_API_KEY || ''
};

const ACTIVE_ROLE = 'superintendent'; // Changed dynamically in UI

const DATA_MANIFEST = {
  generated: '2026-02-19T14:30:00Z',
  template_version: '3.0.0',
  project_code: 'MOSC-825021',
  files: {
    'config.json': {md5: 'abc123', rows: 1, last_update: '...'},
    'spatial.json': {md5: 'def456', rows: 42, last_update: '...'},
    'specs.json': {md5: 'ghi789', rows: 156, last_update: '...'},
    // ... 14 more files
  },
  section_visibility: {
    mep_equipment: true,
    mep_panels: true,
    mep_single_line: true,
    mep_fixtures: true,
    mep_fire_protection: true,
    mep_data_gaps: true,
    doors_hardware: true,
    concrete_mix_designs: true,
    field_tolerances: true,
    // ... auto-populated based on data content
  }
};
```

---

## 3. Incremental Update System

The dashboard uses **smart regeneration** to minimize file I/O and improve performance:

### Update Algorithm
```
function updateProjectData(projectPath, sourceFiles) {
  // Step 1: Check if data.js exists
  if (NOT EXISTS data.js) {
    // Full generation path
    generateAllJSON(sourceFiles) → data.js
    copyTemplate(plugin/references/data-intel-template.html) → {PROJECT_CODE}_Data_Intel.html
    return "NEW_DASHBOARD_CREATED"
  }

  // Step 2: Load existing manifest
  manifest = parseManifest(data.js)

  // Step 3: Compute MD5 for each source
  for each sourceFile in [config, spatial, specs, schedule, directory, ...]:
    currentHash = MD5(sourceFile)
    storedHash = manifest.files[sourceFile.name].md5
    if (currentHash !== storedHash) {
      CHANGED_FILES.push(sourceFile)
    }

  // Step 4: Selective serialization
  if (CHANGED_FILES.length === 0) {
    return "NO_CHANGES_DETECTED"
  }

  // Step 5: Regenerate only changed sections
  for each changedFile in CHANGED_FILES:
    re_parse(changedFile) → update PROJECT_DATA[section]
    update manifest.files[changedFile.name].md5
    log("Updated: " + changedFile.name)

  // Step 6: Write data.js
  serializeToJS(PROJECT_DATA, API_KEYS, ACTIVE_ROLE, manifest) → data.js
  updateGenerationLog()
  return "UPDATED: " + CHANGED_FILES.length + " sections"
}
```

### Fallback: Corrupted Manifest
If `DATA_MANIFEST` is invalid, the system falls back to **full regeneration** with validation:
1. Parse all JSON source files fresh
2. Validate schema against PROJECT_DATA structure
3. Recompute all MD5 hashes
4. Regenerate data.js
5. Log warning in generation log

---


---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
