---
name: closeout-commissioning
description: >
  Skill for tracking project closeout and building commissioning activities. Manages closeout checklists, commissioning workflows, warranty tracking, and substantial/final completion documentation. Integrates with punch-list and inspection systems.
version: 1.0.0
---

# Closeout & Commissioning Skill

## Overview

This skill provides comprehensive tracking for project closeout activities and building systems commissioning, from substantial completion through final closeout and warranty management.

## Closeout Tracking

### Master Closeout Checklist

All items required for project closeout, organized by category:

#### 1. Contract Closeout Documents
- Final Application for Payment (AIA G702/G703 or equivalent)
- Consent of Surety (if bonded)
- Final Lien Waivers (conditional and unconditional)
- Certificate of Substantial Completion
- Certificate of Final Completion

#### 2. O&M Manuals
Organized by system with complete documentation:
- HVAC systems (RTUs, chillers, boilers, split systems, ductless mini-splits)
- Electrical systems (switchgear, panels, motors, lighting controls)
- Plumbing systems (water heaters, pumps, fixtures, backflow preventer)
- Fire Protection (sprinkler, suppression, fire alarm)
- Elevators and hoists
- Roofing and waterproofing
- Specialty systems (kitchen equipment, lab equipment, security, audio/visual)

Each O&M manual must include: equipment specifications, operation procedures, maintenance schedules, parts lists, wiring diagrams, control sequences, troubleshooting guides.

#### 3. As-Built Drawings
- Marked-up field drawings showing actual conditions as installed
- All deviations from design documented
- System riser diagrams updated with actual routing
- Floor plans updated with final fixture locations
- Electrical one-line diagrams with actual panel schedules
- Plumbing and HVAC isometric routing
- Labeled with "FINAL AS-BUILT" stamp and signed by responsible parties

#### 4. Warranty Documentation
- Manufacturer warranties by product/system (equipment warranties with dates and coverage limits)
- Workmanship warranty from contractor (typically 1 year from substantial completion)
- Extended warranties for roofing, waterproofing, windows, specialty systems
- Warranty registration documents
- Contact information for warranty claims by manufacturer and system

#### 5. Training Documentation
- Owner training sessions conducted by system
- Video recording of training sessions (where required)
- Attendance sign-in sheets with owner staff present
- Training materials provided to owner
- Certificates of completion provided to trained personnel

#### 6. Spare Parts and Attic Stock
- Air filters (HVAC)
- Ceiling tiles (match installed type)
- Paint touch-up kits (match all interior finishes)
- Light bulbs/tubes (all types used in building)
- Hardware (hinges, handles, locks, fasteners)
- Quantities per specification requirements
- Organized and stored in designated location with inventory list

#### 7. Keys and Keying Schedule
- Master keys and restricted keys provided per schedule
- Complete key log documenting all keys issued
- Access cards/fobs programmed and issued
- Key storage security procedures documented
- Keying schedule map provided to owner

#### 8. Certificates
- Certificate of Occupancy (from local building authority)
- Fire Marshal approval certificate
- Elevator inspection certificate (from state/local inspector)
- Health Department approval (for healthcare facilities)
- Any other authority having jurisdiction (AHJ) certifications

#### 9. Testing and Balancing Reports
- TAB report for HVAC systems (supply, return, and exhaust flow rates)
- Fire pump test report (performance verification)
- Emergency generator load test report
- Fire suppression hydrostatic and flow test reports
- Electrical system tests (Megger, relay calibration, coordination)
- Plumbing pressure and flow tests

### Closeout Status Tracking Data Model

```json
{
  "closeout_status": {
    "phase": "pre_substantial | substantial_punch | final_closeout | complete",
    "substantial_completion_date": null,
    "final_completion_date": null,
    "items": [
      {
        "id": "CLO-001",
        "category": "contract | om_manual | asbuilt | warranty | training | spare_parts | keys | certificate | testing",
        "description": "HVAC O&M Manual — RTU-1 through RTU-4",
        "responsible_party": "ABC Mechanical",
        "status": "not_started | in_progress | submitted | approved | na",
        "due_date": "2026-04-15",
        "date_submitted": null,
        "date_approved": null,
        "notes": "",
        "spec_section": "23 05 00"
      }
    ],
    "retainage": {
      "total_held": 0,
      "released": 0,
      "remaining": 0,
      "conditions_for_release": []
    }
  }
}
```

### Substantial Completion vs Final Completion

**Substantial Completion:**
- Work sufficiently complete for owner to occupy and use for intended purpose
- Triggers: warranty start date begins, liquidated damages cease accruing, owner takes possession, retainage released (W Principles holds flat 10% until SC, then full release)
- Owner may use space while contractor completes punch list items
- Owner responsible for property insurance and utilities
- Contractor maintains security and incomplete work protection

**Punch List Period:**
- Period between substantial and final completion (typically 30-60 days)
- Contractor completes all punch list items identified at substantial completion inspection
- May include re-testing and re-commissioning of affected systems
- Back-charges assessed for incomplete items or owner-caused damage

**Final Completion:**
- ALL work complete including punch list items
- ALL closeout documents submitted and approved by owner/PM
- ALL retainage released after final inspection
- Project formally closed in accounting systems
- Warranty period documented and starts (if not already from substantial)

**Timeline:**
- Typically 30-60 days from substantial to final completion
- Some extended systems (roofing warranty testing) may extend closure
- Final inspection required before certification

## Commissioning Tracking

### Systems Commissioning Workflow

**Pre-Functional Testing (PFT):**
- Verify equipment installed correctly according to manufacturer specifications
- Verify all controls wired per design documents
- Verify all utilities (power, water, gas, drainage) connected and operational
- Visual inspection complete before energizing or starting equipment
- Documentation: checklist signed off by contractor and commissioning agent

**Functional Performance Testing (FPT):**
- System operates through all operational modes (normal, startup, shutdown, economy, emergency, seasonal)
- System meets performance criteria specified in design documents
- Response to setpoint changes verified
- Alarm and alert functions tested
- Safety interlocks and shutdown sequences tested
- Documentation: test results recorded with data logging where applicable

**Integrated Systems Testing:**
- Systems work together as designed (fire alarm triggers HVAC shutdown, elevator recalls, pressurization sequences, etc.)
- Building automation system sequences tested through actual conditions or simulation
- Emergency procedures tested (generator auto-start, load transfer, fuel supply)
- Documentation: system interaction matrix with test results

**Seasonal Testing:**
- May require summer/winter testing for HVAC systems to verify control response in both seasons
- Chiller operation versus boiler operation transition
- Economizer function in summer and winter modes
- Humidity control verification across seasons

### Commissioning Data Model

```json
{
  "commissioning": {
    "commissioning_agent": "CxA name / firm",
    "systems": [
      {
        "id": "CX-001",
        "system": "HVAC — RTU-1",
        "phase": "pre_functional | functional_testing | integrated_testing | seasonal_testing | complete",
        "pre_functional_date": null,
        "pre_functional_result": "pass | fail | conditional",
        "fpt_date": null,
        "fpt_result": "pass | fail | conditional",
        "deficiencies": [],
        "retesting_required": false,
        "training_complete": false,
        "documentation_complete": false,
        "notes": ""
      }
    ]
  }
}
```

### System Startup Sequences

#### HVAC (Rooftop Units, Chillers, Boilers, Split Systems)
1. Pre-start checklist: verify equipment installed, all connections made, filters installed, ductwork sealed, thermostat wired
2. Startup by manufacturer's representative (may be contractual requirement)
3. Testing & Balancing (TAB): measure supply, return, exhaust flows; adjust dampers/vanes to design airflow
4. Controls verification: setpoints, schedules, occupancy sensors, economizer function
5. Functional Performance Testing: normal mode, startup sequence, shutdown sequence, emergency modes
6. Owner training: operation, filter replacement, emergency shutdown

#### Fire Alarm System
1. Device verification: all initiating devices (detectors, pull stations, manual call points) installed and accessible
2. Programming: verify all device addresses, circuit programming, notification routes
3. Acceptance testing with Fire Marshal: system activation, alarm signals, emergency voice/alarm communications
4. Final certification: Fire Marshal approval certificate issued

#### Fire Suppression (Sprinkler System)
1. Hydrostatic test: system pressure tested per NFPA 13 requirements
2. Flow test: verify adequate water supply and pressure at all elevations
3. Trip test: activate zone valve and verify system response (may be performed during final inspection)
4. Fire Marshal review and acceptance: final approval certificate issued

#### Elevators
1. Installation complete: all equipment installed, mechanical work complete, electrical connections made
2. Inspection by State/Local Inspector: full inspection of safety devices, operation, load capacity
3. Load test: elevator loaded to 125% rated capacity and operated through full range
4. Final acceptance: State Inspector certificate issued; elevator ready for service

#### Emergency Generator
1. Fuel system test: verify fuel supply, filtration, automatic transfer from main to day tank
2. Load bank test: generator loaded to 75-100% rated capacity, engine temperature and voltage verified
3. Transfer switch test: verify automatic switchover to generator and back to utility power
4. Integrated test with fire alarm: verify fuel pump starts, loads generator, transfers building loads
5. Maintenance schedule and fuel sampling protocol established

#### Building Automation System (BAS)
1. Point-to-point verification: each input and output point verified to correct equipment
2. Sequence programming: verify control logic for each system and interaction between systems
3. Trending: historical data collection enabled for critical points
4. Functional Performance Testing: all control scenarios tested; response times verified; alarms tested

#### Plumbing
1. Pressure test: cold water system tested to 1.5 times max operating pressure; verify no leaks
2. Flow test: verify adequate flow and pressure at all fixtures for intended use
3. Water quality test: hot water temperature, pH, chlorine level verification; fixture flushing complete
4. Healthcare facilities: Legionella testing of hot water system

#### Electrical Switchgear and Distribution
1. Megger testing: insulation resistance testing of all cables and equipment
2. Relay calibration: verify protective relay settings and coordination
3. Coordination study verification: confirm protection device coordination matches design calculations
4. Energization sequence: controlled energization with monitoring for any issues
5. Load testing: progressively apply electrical loads; verify voltage drop and power quality


## Project Intelligence Integration

On every `/closeout` invocation, automatically read the following project data to enrich closeout tracking:

### Warranty Tracking from Extracted Data

```
Read quality-data.json → warranties[]
```

- Pull all extracted warranty records and build the **Warranty Closeout Checklist** automatically
- For each warranty, check `registration.status` — flag any with status `pending` where `registration.deadline_date` is within 30 days
- Cross-reference `warranties[].installer` against `directory.json → subcontractors[]` for contact info on missing warranty documents
- Cross-reference `warranties[].spec_section` against `specs-quality.json → spec_sections[]` to verify warranty duration meets specification requirements
- Track warranty start date triggers — if `start_trigger` = "substantial_completion", auto-populate `start_date` when `project-config.json → substantial_completion_date` is set

### Commissioning Test Results

```
Read quality-data.json → system_tests[]
```

- Pull all system test results (TAB, fire protection, electrical, plumbing, envelope) to auto-populate commissioning checklist status
- For each system in the closeout checklist, check if corresponding test records exist with `result` = "pass"
- Flag systems with no test records or with `result` = "fail" / "conditional_pass" that still need re-test
- Cross-reference `system_tests[].witnessed_by` to verify third-party witness requirements are met

### O&M Manual Completeness

```
Read quality-data.json → equipment_data[]
```

- For each equipment item, verify O&M manual has been extracted and structured data exists
- Check for required sections: operation procedures, PM schedules, parts lists, emergency procedures
- Cross-reference equipment tags against `procurement-log.json` to verify all procured equipment has corresponding O&M data
- Flag equipment with missing or incomplete O&M documentation

### As-Built Drawing Status

```
Read plans-spatial.json → as_built_overlay
```

- Pull as-built completion status by discipline from `as_built_overlay.as_built_status[]`
- Calculate overall as-built completion percentage
- Flag disciplines below 100% completion — list specific sheets still needing markup
- Cross-reference deviations against `change-order-log.json` to verify all field changes are documented

---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
