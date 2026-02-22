---
name: quality-management
description: >
  Formal Quality Management System (QMS) with three-phase inspection checklists (pre-installation, installation, post-installation) organized by CSI division and trade. Provides specification compliance verification, Inspection and Test Plans (ITP), corrective action tracking, and quality metrics reporting. Integrates with inspection-tracker, sub-performance, and daily reports. Triggers: "quality checklist", "QMS", "pre-install checklist", "three-phase inspection", "quality verification", "ITP", "inspection test plan", "quality control", "quality assurance", "QA/QC", "pre-install", "post-install", "quality report", "first-time quality", "rework tracking".
version: 1.0.0
---

# Quality Management System (QMS)

## Overview

The Quality Management System is a formal, three-phase construction quality framework organized by CSI division and trade. It ensures specification compliance, minimizes rework costs, and creates comprehensive, auditable quality records for every phase of construction.

**Primary Purpose**: Convert design intent and specifications into built reality with zero defects and full documentation.

**Scope**: Applies to all trades and materials from foundation through final punch-list closeout.

**Key Outcomes**:
- Reduction in rework cost (target: <2% of contract value)
- First-Pass Inspection Rate (FPIR) above 90%
- Zero code violations at final inspection
- Complete digital quality trail for O&M handoff

---

## QMS Philosophy: Three Pillars

### 1. Prevention (Pre-Installation)

Quality built in from the beginning. Before any work starts:
- Verify all materials meet specification
- Confirm crews understand acceptance criteria
- Complete prep work to documented standards
- Ensure MEP coordination is resolved
- Review and approve all submittals
- Identify and resolve clashes before installation

**Prevention Cost**: Investment in planning, verification, and coordination = lowest cost to quality.

### 2. Conformance (Installation Monitoring)

Real-time quality control during construction:
- Daily observation by field leadership and trade foremen
- In-progress measurements and testing
- Immediate corrective action when non-conformance detected
- Photo documentation of critical phases
- Hold points verified before proceeding
- Test data recorded and trended

**Conformance Cost**: Active supervision and testing = moderate cost, prevents rework.

### 3. Documentation (Post-Installation)

Permanent quality record:
- Final inspection checklists signed and filed
- Test reports and material certs retained
- Deficiencies resolved and verified
- As-built data verified
- Warranty and startup documentation complete
- O&M team trained on quality standards

**Documentation Cost**: Low (mostly administrative), enables warranty support and operations.

---

## Three-Phase Inspection Structure by Trade

Each major trade follows a standardized three-phase inspection protocol: Pre-Installation (setup), Installation (monitoring), and Post-Installation (verification).

### CONCRETE (CSI 03 30 00)

**Phase 1: Pre-Installation Inspection**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Formwork alignment | ±1/4" plumb/level (ACI 117) | Laser level / sight | 03 30 00 |
| Formwork bracing | Adequate for loads, no deflection | Visual / load calc review | 03 30 00 |
| Rebar spacing | Within ±1/4" of dimensions | Measurement / template | 03 20 00 |
| Rebar cover | Min cover per plans verified | Measurement at corners | 03 20 00 |
| Embedments | Location within 1" of plan | Measurement / photo | 03 20 00 |
| Mix design approval | Wells Concrete formula approved | Documentation review | 03 30 00 |
| Weather check | Min 40F rising, no rain forecast | Weather forecast / thermometer | 03 30 00 |
| Concrete source | Mill cert on file, slump range known | Documentation review | 03 30 00 |
| Reinforcing placement | Clear of formwork, secured | Visual / photo | 03 20 00 |
| Curing compound staged | Material on site, application plan ready | Visual | 03 30 00 |

**Phase 2: Installation Checklist**

| Item | Acceptance Criteria | Method | Frequency |
|------|-------------------|--------|-----------|
| Slump test | Within ±1" of target (typically 4-5") | Slump cone per ASTM C143 | Each truck |
| Air content | 4-6% per mix design ±1% | Pressure meter per ASTM C173 | Each truck |
| Temperature | Above 40F, below 90F | Thermometer in truck | Each truck |
| Vibration pattern | No segregation, full consolidation | Visual observation | Continuous |
| Surface leveling | No excessive settlement before set | Straightedge / laser | After placement |
| Curing initiation | Misting started or compound applied | Visual | Immediately |
| Test cylinder casting | 1 set per 50 CY (2 cylinders at 7d, 1 at 28d) | Per ASTM C31 | Each 50 CY |
| Honeycombing check | None visible, minor voids <0.5" | Visual inspection | Continuous |
| Formwork removal timing | No removal until strength verified | Test cylinder break schedule | Per ACI |
| Cure duration | Min 7 days moist cure (or as calculated) | Project calendar | Monitored |

**Phase 3: Post-Installation Verification**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Curing duration verified | 7-day cure complete per ACI 308 | Documentation / calendar | 03 30 00 |
| Surface finish | No honeycombing, texture per plans | Visual / photo | 03 30 00 |
| Tolerances verified | Flatness/levelness per ACI 117 | Straightedge / laser transit | 03 30 00 |
| Embedded items | All penetrations sealed, sleeves verified | Visual / checklist | 03 20 00 |
| Test results | 28-day cylinder strength ≥ spec (4000 PSI) | Break report review | 03 30 00 |
| Rebar exposure | None visible, no rust staining | Visual | 03 20 00 |
| Final acceptance | Superintendent and GC approval | Signature on checklist | — |

---

### STRUCTURAL STEEL / PEMB (CSI 05)

**Phase 1: Pre-Installation**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Anchor bolt survey | All bolts within 1/2" of template | Transit survey by surveyor | 05 12 00 |
| Material certs | Mill test reports for all structural steel | Review MMIS / certs | 05 12 00 |
| Connection detail approval | All details reviewed by architect | Document review | 05 12 00 |
| Lift plan approval | Lift plan stamped by PE, reviewed | Plan review | Safety |
| Bolt type / grade verification | F1554 Gr36 (anchor), A325/A490 (connections) | Cert review / tagging | 05 12 00 |
| Hoist equipment staged | Crane tested, certified, on site | Visual / cert review | Safety |
| Weather clearance | Wind forecast <25 mph, no rain | Weather service | Safety |
| Site access verified | Staging area clear, access established | Visual | Safety |
| Personnel training | Ironworkers and hoistmen briefed | Sign-in sheet | Safety |

**Phase 2: Installation**

| Item | Acceptance Criteria | Method | Frequency |
|------|-------------------|--------|-----------|
| Bolt torque | Wrench value per F1554 spec chart | Calibrated torque wrench | Each bolt |
| Connection alignment | ±1/4" plumb/level, within tolerance | Transit / laser level | Per frame |
| Bolt snugness | Hand-tight on all bolts before tension | Visual / torque check | Staged |
| Weld quality (if SJI deck) | Per AISC D1.1 / AWS D1.3 | Visual / UT if required | Per weld |
| Member plumbness | Columns within 1:500 | Transit/laser | Per frame |
| Connection tightness | No movement when tapped | Tap test / torque check | Per connection |
| Paint curing | No interference with bolting | Visual | If wet paint |
| Bracing sequence | Erected per lift plan sequence | Observation | Progressive |

**Phase 3: Post-Installation**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Final bolt inspection | All bolts tight, thread visible | Torque spot check (10%) | 05 12 00 |
| Plumbness verification | ±1/4" overall building plumb | Transit survey | 05 12 00 |
| Paint touch-up | All connections and damaged areas | Visual inspection | 05 12 00 |
| Fireproofing applied (if req'd) | Full coverage per spray plan | Visual / thickness probe | Division 07 |
| Hardware attachment | All trim, wind bracing secured | Visual checklist | 05 12 00 |
| Final acceptance | SE sign-off on structural completion | Plan review / letter | 05 12 00 |

---

### CFS FRAMING & GYPSUM BOARD (CSI 09)

**Phase 1: Pre-Installation**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Stud spacing layout | 16" OC verified per plans | Measurement / marking | 09 22 00 |
| Stud grade / gauge | 20-gauge minimum, 3-5/8" or 6" | Mill cert / label review | 09 22 00 |
| Board type verification | Type X fire-rated in required areas | Review purchase orders | 09 29 00 |
| Backing/blocking installed | All locations ready for MEP | Visual checklist | 09 22 00 |
| MEP rough-in clearance | All MEP complete or approved to proceed | Punch-out walk | Division 21-28 |
| Weather protection | No exposed board, site enclosed | Visual | 09 29 00 |
| Material staging | Board stored flat, elevated off deck | Visual | 09 29 00 |
| Moisture meter on hand | Baseline moisture readings documented | Meter calibration check | 09 29 00 |

**Phase 2: Installation**

| Item | Acceptance Criteria | Method | Frequency |
|------|-------------------|--------|-----------|
| Fastener spacing | Screws 16" OC walls / 12" OC ceilings | Measurement / visual | Per 500 SF |
| Joint tape placement | Centered, wrinkle-free | Visual | Per 1000 SF |
| Joint compound application | Smooth feather, consistent thickness | Visual / straightedge | Per joint |
| Corner bead | Straight, no lips, fastened every 12" | Straightedge check | Per 500 SF |
| Fire-stopping installed | Caulk at all penetrations, per detail | Visual checklist | Continuous |
| Control joints | Installed per spec (typically 30' max) | Measurement | Per wall |
| Drying time observed | Minimum 24 hr between coats | Time log / observation | Between coats |
| Moisture monitoring | Readings <12% during application | Moisture meter | Daily |
| Sanding schedule | Smooth finish, dust collected | Observation | Per coat |

**Phase 3: Post-Installation**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Finish level | L3 or L4 (project spec requirement) | Rake light / photo | 09 29 00 |
| Fire rating cert | Documentation for fire-rated areas | Certificate file review | Division 07 |
| Corner bead straight | Minimal lippage, no shadows | Rake light / visual | 09 29 00 |
| Surface smoothness | No ridges, uniform reflectance | Rake light | 09 29 00 |
| Penetration sealing | All outlets, pipes, ducts sealed | Visual | Division 07 |
| Final touch-up | All dings/gouges repaired | Paint coverage verification | 09 29 00 |
| Acceptance | GC and drywall sub sign-off | Checklist signature | — |

---

### ROOFING & BUILDING ENVELOPE (CSI 07)

**Phase 1: Pre-Installation**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Substrate condition | Clean, dry, structurally sound | Visual / moisture test | 07 15 00 |
| Moisture test | Calcium chloride <3 lbs/1000 SF | ASTM F1869 test | 07 15 00 |
| Insulation installed | Per plan, joints staggered, no compression | Visual inspection | 07 21 00 |
| Flashing substrate prep | Substrate clean, primer ready | Visual | 07 65 00 |
| Weather window | 3-day clear forecast, min 40F | Weather service | 07 31 00 |
| Manufacturer rep on hand | Inspection/warranty witness available | Sign-in | 07 31 00 |
| Membrane rolls staged | At room temp (>50F), labeled correctly | Visual staging check | 07 31 00 |
| SWPPP protection | Erosion control in place | Visual | — |

**Phase 2: Installation**

| Item | Acceptance Criteria | Method | Frequency |
|------|-------------------|--------|-----------|
| Membrane seam integrity | Seams sealed per mfr (hot mop / adhesive) | Visual / peel test | Per 500 SF |
| Flashing detail adherence | Detail drawings followed exactly | Visual / photo | Per detail |
| Expansion joint treatment | Flashing detail per drawing | Visual | Per joint |
| Fastener pattern | Pattern per mfr specification | Measurement | Per 1000 SF |
| Roof slope verification | Slope to drains per plan (1:12 typical) | Level check / observation | Continuous |
| Pipe boot installation | Sealed, no gaps, proper clearance | Visual | Per penetration |
| HVAC curb sealing | Flashing sealed, no voids | Visual / photo | Per curb |
| Weather protection | No rain on exposed membrane | Weather monitoring | Continuous |

**Phase 3: Post-Installation**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Flood test (if required) | Water retained for 24-48 hr, no leaks | Visual / inspection | 07 31 00 |
| Final walkdown | Mfr witness present, no punctures/damage | Visual / photo | 07 31 00 |
| Penetration sealing | All boots and flashing sealed | Visual checklist | 07 65 00 |
| Surface cleanliness | Debris removed, surface clean | Visual | 07 31 00 |
| Warranty documentation | Mfr warranty issued | Certificate file | 07 31 00 |
| Final acceptance | GC and mfr sign-off | Punch checklist | — |

---

### MEP SYSTEMS (CSI 21-28)

**Phase 1: Pre-Installation (Mechanical, Electrical, Plumbing)**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Routing per plans | 2D/3D routing review complete | Drawing review / walk-down | 21-28 |
| Hanger spacing calculated | Per code and load (typically 4-6' for pipes) | Calc sheet review | 21-28 |
| Code review complete | MEP plans reviewed against IBC / NEC | Plan review | 21-28 |
| Penetration layout approved | Locations verified on structure | Drawing review / mark-up | 21-28 |
| Material specs verified | Pipe grade, fittings, wire gauge on site | Purchase order review | 21-28 |
| Coordination with GWB | Rough-in sequence planned before board | MEP/drywall meeting notes | 09-21 |
| Equipment staging | Major equipment on site or scheduled | Delivery tracking | 21-28 |
| Support / fastening ready | Hangers staged, fasteners available | Visual | 21-28 |

**Phase 2: Installation**

| Item | Acceptance Criteria | Method | Frequency |
|------|-------------------|--------|-----------|
| Line sizing | Per plans, no undersizing | Observation | Per run |
| Slope verification | DWV slopes 1/4" per ft, hot water to load | Level check | Per 50 ft |
| Hanger spacing | Per code, supports secured | Measurement / visual | Per 6 feet |
| Pressure testing | Hydrostatic test per code, no leaks | Pressure gauge / timer | Per 500 SF |
| Sealing at penetrations | Caulk/firestopping installed immediately | Visual | Per penetration |
| Ductwork seal | Duct sealed per SMACNA, no leaks | Visual / duct seal verification | Per connection |
| Insulation thickness | R-value per plans verified | Measurement | Per 500 ft |
| Labeling | Pipe labels, duct ID per drawings | Visual checklist | Continuous |
| Electrical clearances | Proper separation from other trades | Visual | Per run |

**Phase 3: Post-Installation**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| System pressure test | Final pressure hold, documented | Test gauge / report | 21-28 |
| Functional testing | All systems operate per spec | Operation verification | 21-28 |
| Balancing report | HVAC balanced, airflow per plan | Balance contractor report | 21-28 |
| Start-up documentation | Equipment manuals, settings documented | O&M manual verification | 21-28 |
| Commissioning prep | Systems ready for handoff | Checklist completion | 21-28 |
| Final acceptance | Trade contractor and GC sign-off | Punch completion | — |

---

### FLOORING (CSI 09 65 00)

**Phase 1: Pre-Installation**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Substrate moisture test | Calcium chloride <3 lbs/1000 SF (wood), <4 (concrete) | ASTM F1869 | 09 65 00 |
| Levelness check | FF/FL per spec (typically 3/10" in 10 ft) | Self-leveling floor check | 09 65 00 |
| Acclimation period | Material at room temp (68-75F), 48+ hours | Observation / documentation | 09 65 00 |
| Adhesive compatibility | Confirmed with substrate and material | Mfr spec review | 09 65 00 |
| Subfloor prep | Clean, no dust, imperfections filled | Visual inspection | 09 65 00 |
| Pattern layout | Layout marked, seams planned | Mark-up / photo | 09 65 00 |
| Primer applied (if req'd) | Substrate primed per mfr spec | Visual | 09 65 00 |

**Phase 2: Installation**

| Item | Acceptance Criteria | Method | Frequency |
|------|-------------------|--------|-----------|
| Pattern layout | Seams placed per plan, cuts planned | Visual observation | Per 500 SF |
| Adhesive spread rate | Per mfr spec (typically 1/16" or 1/8" notch) | Trowel observation / documentation | Per 1000 SF |
| Seam placement | No bunching, pattern consistent | Visual / measurement | Per seam |
| Roller weight | Per mfr spec (typically 100-150 lbs) | Observation | Per 500 SF |
| Ambient conditions | Temperature 65-85F, humidity 30-60% | Thermometer / hygrometer | Continuous |
| Material temperature | At room temp, not cold | Touch check | Continuous |
| Walking time | Observed before foot traffic allowed | Observation / signage | As required |

**Phase 3: Post-Installation**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Seam integrity | Seams bonded, no lifting or curling | Pull test / visual | 09 65 00 |
| Transition strips | All transitions installed correctly | Visual / fit check | 09 65 00 |
| Cleaning protocol | Residual adhesive removed per mfr | Visual inspection | 09 65 00 |
| Protection plan | Material protected from traffic | Signage / observation | 09 65 00 |
| Color consistency | No shade variation | Visual / photo | 09 65 00 |
| Final acceptance | Flooring contractor and GC sign-off | Checklist signature | — |

---

### DOORS & HARDWARE (CSI 08)

**Phase 1: Pre-Installation**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Frame plumb/level/square | ±1/8" in height and width | 4-foot level / square | 08 11 00 |
| Hardware blocking installed | All blocking in place for hardware | Observation against blocking chart | 08 70 00 |
| Finish wall complete | Surrounding wall finished before door | Visual (drywall prime/paint complete) | 09 29 00 |
| Clearances verified | ADA clearances confirmed if required | Measurement per ADA guidelines | 08 11 00 |
| Frame material certs | Metal frame mill certs on file | Documentation review | 08 11 00 |
| Door slab certification | Fire rating certs for fire-rated doors | Certificate file | 08 14 00 |
| Hinges and closer staging | Correct type/function staged | Observation / count | 08 70 00 |

**Phase 2: Installation**

| Item | Acceptance Criteria | Method | Frequency |
|------|-------------------|--------|-----------|
| Frame installation | Plumb/level, shims tight, fastened every 16" | 4-foot level / observation | Per frame |
| Door slab hang | Aligned, hinges torqued correctly | Visual / swing test | Per door |
| Hardware template alignment | Drill holes per template, no deviation | Template use observation | Per opening |
| Closer adjustment | Closing speed and latching verified | Function test (close/latch/release) | Per closer |
| Lock function test | Keyless/key operation smooth | Operation test | Per lock |
| ADA compliance | Lever handles, no stiff hinges if required | Operational test per ADA | Per opening |
| Fire-rated assembly | Gaskets and seals installed | Visual / detail verification | Per fire-rated door |

**Phase 3: Post-Installation**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Operation smooth | Door swings freely, closes smoothly | Operation test | 08 11 00 |
| Fire-rated assembly complete | Gaskets, seals, closers all in place | Visual checklist | Division 07 |
| Keying schedule verified | All locks keyed per master key system | Key test / documentation | 08 70 00 |
| Hardware functional | All hardware operates per spec (openers, stops, holders) | Operation test | 08 70 00 |
| Finish unblemished | No scratches, dents, or damage | Visual inspection | 08 14 00 |
| Final acceptance | Door hardware contractor and GC sign-off | Checklist signature | — |

---

### PAINT & COATINGS (CSI 09 91 00)

**Phase 1: Pre-Installation**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Surface prep complete | Sanding, filling, sanding complete to L3/L4 | Visual / sand/fill verification | 09 91 00 |
| Primer compatibility | Primer type matches substrate and topcoat | Spec/mfr documentation review | 09 91 00 |
| Temperature check | Between 50-90F, ideally 60-75F | Thermometer | 09 91 00 |
| Humidity check | Between 30-85% RH | Hygrometer | 09 91 00 |
| Masking complete | All trim, glass, hardware protected | Visual inspection | 09 91 00 |
| Material temperature | Paint at room temp (>50F) | Observation | 09 91 00 |
| Surface wetness | Surface completely dry, no condensation | Touch / observation | 09 91 00 |

**Phase 2: Installation**

| Item | Acceptance Criteria | Method | Frequency |
|------|-------------------|--------|-----------|
| Mil thickness | Wet mil per plan, typically 3-4 mils | Wet mil gauge | Per 1000 SF |
| Coverage uniformity | No thin spots, consistent color | Visual observation | Per 500 SF |
| Cut lines | Straight lines, no bleed-through | Straightedge / visual | Per edge |
| Drying time observed | Minimum between coats per mfr (typically 4-8 hrs) | Time log / observation | Between coats |
| No runs/sags | Surface smooth, no sagging paint | Visual | Per 500 SF |
| No holidays | Complete coverage, no bare spots | Visual inspection under light | Per 500 SF |
| Brush marks minimal | Smooth finish per spec level | Visual / rake light | Per 500 SF |
| Ventilation adequate | Paint fumes evacuated, workspace safe | Observation / fan use | Continuous |

**Phase 3: Post-Installation**

| Item | Acceptance Criteria | Method | Spec Ref |
|------|-------------------|--------|----------|
| Touch-up complete | All dings from construction touchup done | Visual checklist | 09 91 00 |
| Color match verified | Final color matches approved samples | Side-by-side visual | 09 91 00 |
| Sheen consistent | Uniform gloss across all surfaces | Visual raking light | 09 91 00 |
| No runs/sags/holidays | Final surface uniform and complete | Final visual inspection | 09 91 00 |
| Surface cleanliness | Dust removed, surface clean | Visual | 09 91 00 |
| Final acceptance | Painter and GC sign-off | Checklist signature | — |

---


## Project Intelligence Integration

When project intelligence is loaded, auto-populate QMS checklists, hold points, and inspection requirements from extracted project data instead of requiring manual lookup.

### Spec-Based Checklist Generation
Generate trade-specific checklists from specifications:
- Read `specs-quality.json` → `spec_sections[]` → for each CSI division, pull testing requirements, acceptance criteria, and QC checkpoints
- Auto-populate Phase 1/2/3 checklist items with spec-specific tolerances and methods
- Example: Division 03 spec requires 4000 PSI 28-day strength → auto-set concrete Phase 3 acceptance criteria to "28-day cylinder strength >= 4000 PSI"

### Hold Point Awareness
Auto-populate pre-installation verification requirements:
- Read `specs-quality.json` → `hold_points[]` → identify mandatory hold points for the current work phase
- Flag upcoming hold points that require Building Official or third-party inspection sign-off before proceeding
- Cross-reference `inspection-log.json` → verify hold point inspection status (scheduled/pass/fail)
- Example: HP-007 (anchor bolt survey) must clear before PEMB erection → flag if not yet passed

### Location Mapping
Resolve inspection locations to structured references:
- Read `plans-spatial.json` → `room_schedule[]` + `building_areas[]` → resolve inspection area to grid references and floor levels
- Auto-populate the inspection location field with structured grid/area/room data
- Example: "Kitchen area" → Grid C-4, Level 1, Building Area: West Wing, Room 103

### Subcontractor QC Contact
Identify the responsible QC representative for each trade:
- Read `directory.json` → `subcontractors[]` → for the trade being inspected, pull the sub's QC contact and foreman information
- Auto-populate the "Responsible Party" field on inspection checklists
- Example: CFS framing inspection → EKD QC rep: contact info from directory.json

### Historical Quality Data
Pull trending data to inform current inspections:
- Read `quality-data.json` → `quality_metrics` → pull FPIR (First-Pass Inspection Rate) trends per trade
- Read `quality-data.json` → `corrective_actions[]` → surface recurring corrective actions for the current trade
- Flag trades with FPIR below 85% for increased inspection frequency
- Example: W Principles FPIR trending at 82% → recommend additional pre-pour inspection checkpoints

### Drawing Reference
Link QC inspections to relevant construction documents:
- Read `plans-spatial.json` → `sheet_cross_references[]` → match the inspection location and trade to relevant detail drawings
- Auto-populate "Reference Drawing" field on inspection checklists
- Example: Foundation rebar inspection at Grid X-2 → Reference Sheet S-1.1 (Foundation Plan), Detail 3/S-1.2

### Material Test Result Verification

```
Read quality-data.json → test_results[]
```

- Before approving any inspection involving concrete, steel, soil, or welding, check `quality-data.json → test_results[]` for the relevant material/trade
- **Concrete**: Verify 7-day and 28-day compressive strength results meet spec requirements from `specs-quality.json → acceptance_criteria[]`
- **Steel**: Verify mill test reports (MTRs) on file with correct grade and heat lot traceability
- **Soil**: Verify compaction test results meet specified percent compaction before proceeding with foundation work
- **Welding**: Verify NDT inspection results for structural connections before cover-up
- Cross-reference test specimen IDs against `procurement-log.json → delivery_tickets[]` to confirm material traceability
- Flag any test failures or pending results that could affect inspection approval

---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
