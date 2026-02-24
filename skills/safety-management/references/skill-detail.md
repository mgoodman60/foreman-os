# safety-management — Detailed Reference



Extended documentation, examples, templates, and detailed criteria for the safety-management skill.



## Toolbox Talks & Safety Meetings

### Toolbox Talk Program

**Definition**: Brief (5-15 minute) focused safety discussions with trades before work begins or weekly.

**Frequency Requirements**:
- **Minimum**: Weekly for all crews
- **High-risk activities**: Daily (steel erection, excavation, crane work, roofing, hot work, confined space)
- **Trigger-based**: Immediately after near-miss or incident (required corrective action discussion)
- **Pre-task**: Before new activity type or change in conditions

**Legal Basis**: OSHA 1926.500(a) and construction safety best practices; demonstrates management commitment to safety culture.

### Toolbox Talk Topic Library

Topics organized by **Trade** and **Hazard Type**:

#### Foundation & Concrete Trades

**Topic 1: Concrete Placement Safety**
- Hazards: Hot concrete (burns), flying concrete chips, slips/falls, noise
- Controls:
  - Protective clothing (long sleeves, gloves, boots)
  - Face protection when chipping
  - Slip prevention on wet surfaces
  - Hearing protection (>85 dB)
- Duration: 10 minutes
- Frequency: Before each concrete pour
- Spec Reference: ACI 306 (cold weather) / ACI 305 (hot weather)

**Topic 2: Reinforcing Steel Handling**
- Hazards: Sharp edges, eye injuries, crushed fingers, back strain
- Controls:
  - Leather gloves when handling rebar
  - Cut-resistant sleeves
  - Proper lifting technique (bend knees, straight back)
  - No throwing or dropping rebar near workers
  - Secure bundles to prevent tipping
- Duration: 8 minutes
- Frequency: Weekly during foundation

**Topic 3: Formwork Safety**
- Hazards: Strikes from falling forms, nail punctures, splinters, falls from height
- Controls:
  - Hard hats while removing/building forms
  - Proper removal sequence (no hanging on props)
  - Watch for exposed nails
  - Use proper ladder/scaffolding (not stacked material)
- Duration: 10 minutes
- Frequency: Before formwork erection and removal

#### Structural Steel & PEMB

**Topic 4: PEMB Erection Safety (High-Risk)**
- Hazards: Falls from height (36' eave), crushing (falling beams), struck-by (guy wires), pinch points
- Controls:
  - 100% fall protection (harness, lanyard, anchor points) for all workers at height
  - Guy-wire verification before each lift
  - Ground personnel clear of load path
  - Spotter communication with crane operator (radio)
  - No workers under suspended load
  - Hard hats mandatory
- Duration: 15 minutes
- Frequency: Daily during erection (pre-work safety briefing)
- OSHA Reference: 1926.500 (Fall Protection), 1926.752 (Cranes & Rigging)

**Topic 5: Crane Safety & Rigging**
- Hazards: Dropped load, moving boom, guy-wire failure, electrocution (power lines)
- Controls:
  - Certification requirements (operator, rigger, signal person)
  - Load calculations and documentation
  - Inspection of rigging hardware (slings, shackles, chains)
  - 100% inspection of load rigging before lift
  - Clear communication (radio signals defined)
  - No hovering over work area
  - Maintain 50-foot clearance from power lines (or de-energize)
- Duration: 15 minutes
- Frequency: Before first day of crane operations; daily safety briefing
- OSHA Reference: 1926.550 (Cranes, Derricks, Load-Handling Equipment)

**Topic 6: Steel Beam Handling & Assembly**
- Hazards: Falls from height, struck-by (beams pivoting), crushing (load shift)
- Controls:
  - Fall protection for heights > 6 feet
  - Hard hats at all times
  - Workers stay clear of suspended loads
  - Proper bolting sequence per plans
  - Temporary bracing until connection complete
  - Communication with crew before moving/shifting
- Duration: 10 minutes
- Frequency: Weekly during structural phase

#### MEP & Building Systems

**Topic 7: Confined Space Entry (if applicable)**
- Hazards: Asphyxiation, toxic atmospheres, engulfment, hazardous energy
- Controls:
  - Confined space permit required (atmospheric testing, entry procedure)
  - Ventilation before entry; continuous monitoring
  - Rescue equipment staged
  - Attendant present outside space
  - Communication (radio, rope signals) with entrant
  - SCBA or supplied air if needed
- Duration: 15 minutes (detailed review)
- Frequency: Before any confined space entry
- OSHA Reference: 1926.1202 (Confined Spaces)

**Topic 8: Hot Work Safety (Welding, Cutting, Torch)**
- Hazards: Fire, explosion, arc flash, burns, fumes
- Controls:
  - Hot work permit required
  - Fire watch for 30 minutes post-work
  - Clear combustibles within 35-foot radius
  - Welding screens to protect others
  - Proper PPE (welding helmet, gloves, apron)
  - Respiratory protection if poor ventilation
  - Gas cylinder secured upright
- Duration: 10 minutes
- Frequency: Before any hot work; daily if hot work ongoing
- OSHA Reference: 1926.252 (Welding, Cutting, Brazing); NFPA 51B

**Topic 9: Electrical Safety & Live Circuits**
- Hazards: Electrocution, arc flash, burns
- Controls:
  - De-energize circuits during work (lockout/tagout)
  - Use GFCI protection for temporary power
  - Inspect cords before use
  - Wet-location protection
  - Keep water/moisture away from electrical equipment
  - Call before digging (one-call system) for existing utilities
- Duration: 10 minutes
- Frequency: Weekly during MEP rough-in; before any electrical work
- OSHA Reference: 1926.300 (Electrical)

#### Excavation & Earthwork

**Topic 10: Excavation & Trenching Safety (Critical)**
- Hazards: Cave-in (crushing), struck-by (moving equipment), asphyxiation, engulfment
- Controls:
  - Competent person inspection (daily or after rain/change)
  - Proper sloping (angle per soil type) or shoring
  - Atmospheric testing (confined space hazards)
  - Equipment 2 feet from trench edge
  - No workers under raised buckets
  - Oxygen deficiency/toxic gas detection
  - Exit routes (ladder, ramp) within 25 feet
- Duration: 15 minutes (critical hazard)
- Frequency: Before excavation; daily safety briefing; after weather changes
- OSHA Reference: 1926.651 (Excavation Requirements); Geotechnical site-specific safety plan
- **Site-Specific** (read from project geotech data): Check `project-config.json` and `specs-quality.json` for soil conditions — frost-susceptible soils require modified sloping angles, expansive clay needs wider excavation, high water table requires dewatering plan, contaminated soils need hazmat protocols. Read fill depth from geotech report data to assess cave-in risk level.

**Topic 11: Compaction & Earthwork Equipment**
- Hazards: Struck-by (compactor, roller), dust inhalation, noise
- Controls:
  - Spotters for compaction equipment
  - Dust mask when compacting in dry conditions
  - Hearing protection (compactors >85 dB)
  - Load checking per geotech proofroll
  - No walking directly behind moving equipment
- Duration: 8 minutes
- Frequency: Weekly during site prep

#### Roofing & Fall Protection

**Topic 12: Roofing & Perimeter Safety (Weather-Sensitive)**
- Hazards: Falls (roof height 36 feet), slipping on wet/icy surfaces, weather exposure
- Controls:
  - 100% fall protection (harness + lanyard + anchor points)
  - Roof pitched ≥4:12 requires fall protection
  - Personal anchor lines; no horizontal lifelines (project-specific)
  - Buddy system (no solo roofing work)
  - Hard hats at all times
  - Non-slip footwear or roof boots
  - Weather monitoring (wind, rain, ice); work halts if conditions unsafe
- Duration: 15 minutes
- Frequency: Before roofing operations; daily briefing during roofing phase
- OSHA Reference: 1926.502 (Fall Protection)
- **Site-Specific** (read from project data): Check `plans-spatial.json → sections.building[].roof_slope` for actual slope — low-slope roofs (≤4:12) require different fall protection than steep-slope (>4:12). Read wind halt threshold from `specs-quality.json → weather_thresholds` for the roofing spec section.

**Topic 13: Scaffold Safety**
- Hazards: Falls from scaffold, collapse (overload), shifted/unstable
- Controls:
  - Competent person inspection (weekly or after damage)
  - Proper bracing and stabilization
  - Capacity limits clearly marked
  - Guard rails (top rail 42"+, mid-rail 21"+)
  - Toe boards for falling object protection
  - Proper access (stairs, ramps, ladders)
  - No makeshift repairs without engineer approval
- Duration: 10 minutes
- Frequency: Weekly; before any scaffold work
- OSHA Reference: 1926.501 (Scaffolding)

#### PPE & General Safety

**Topic 14: Personal Protective Equipment (PPE)**
- Hazards: Site hazards vary; PPE prevents/mitigates severity
- Controls:
  - Hard hats required at all times (no exceptions)
  - Safety glasses in work areas
  - Steel-toe boots
  - High-visibility vests
  - Gloves per task (cut-resistant, leather, nitrile)
  - Hearing protection if noise > 85 dB
  - Respiratory protection if dust/fumes
  - Sunscreen and hydration (heat stress)
- Duration: 10 minutes
- Frequency: Weekly orientation; before high-risk work
- OSHA Reference: 1926.95 (Fall Protection); 1926.102 (Eye/Face Protection)

**Topic 15: Housekeeping & Site Safety**
- Hazards: Trips/falls, struck-by, fire, poor visibility
- Controls:
  - Clean walkways and work areas daily
  - Proper waste management (containers, removal)
  - Secure materials to prevent tipping
  - Adequate lighting (especially pathways, stairs)
  - Emergency equipment accessible (first aid, AED, fire extinguishers)
  - Clear signage for hazards
- Duration: 8 minutes
- Frequency: Weekly; as-needed for housekeeping issues
- OSHA Reference: 1926.25 (Housekeeping)

#### Weather-Related Topics

**Topic 16: Heat Stress & Hydration**
- Hazards: Heat exhaustion, heat stroke, dehydration
- Conditions: During hot weather (>85°F) or high humidity
- Controls:
  - Water available on site (minimum 1 gallon per person per 4 hours)
  - Rest breaks in shade every 2 hours
  - Light-colored, light-weight clothing
  - Monitor crew for heat stress signs (dizziness, nausea, confusion)
  - Buddy system; crew watches for heat illness
  - Acclimatization during first week of hot weather
- Duration: 8 minutes
- Frequency: Daily during summer months

**Topic 17: Cold Weather & Frost Safety**
- Hazards: Frostbite, hypothermia, slipping on ice, frozen equipment
- Conditions: During cold weather (<40°F), frost, snow/ice
- Controls:
  - Warm clothing layers (thermal, gloves, hat)
  - Frequent breaks in heated areas
  - Monitor for cold stress signs
  - De-icing materials on walkways
  - Inspect equipment for ice accumulation
  - No concrete work below 40°F (ACI 306)
  - Proofroll inspection if frozen material present
- Duration: 8 minutes
- Frequency: Daily during cold months
- Spec Reference: ACI 306; Geotechnical safety plan (frost-susceptible soils)

### Toolbox Talk Attendance & Documentation

**Attendance Tracking**:
- Sign-in sheet (print or digital)
- Topic, date, attendees documented
- Supervisor/safety manager initials
- Linked to safety-log.json

**Sign-In Sheet Template**:
```
TOOLBOX TALK ATTENDANCE RECORD
Project: {project_name}
Date: _______________
Topic: _______________
Duration: _______________
Facilitator: _______________ (print name and sign)

Attendees (Print Name):
1. _______________
2. _______________
3. _______________
4. _______________
5. _______________

Topics Discussed:
_________________________________________________________________
_________________________________________________________________

Key Takeaways / Action Items:
_________________________________________________________________

Signature of Supervisor: _______________    Date: __________
```

**Data Storage**:
```json
{
  "id": "TOOLBOX-TALK-001",
  "date": "2026-02-18",
  "project": "{project_code}",
  "topic": "PEMB Erection Safety",
  "topic_id": "topic_4",
  "duration_minutes": 15,
  "facilitator": "Safety Manager",
  "attendance_count": 12,
  "attendees": ["Ironworker-1", "Ironworker-2", "Ironworker-3", "Crew-Foreman", "Supervisor"],
  "trades_present": ["ironworker", "crane_operator", "foreman"],
  "key_points_covered": [
    "100% fall protection harness requirement",
    "Guy-wire verification before lifts",
    "Ground personnel clear of load path",
    "Spotter radio communication"
  ],
  "action_items": [
    "Inspect all harnesses and lanyards before work",
    "Verify anchor points on PEMB columns"
  ],
  "linked_daily_report": "2026-02-18",
  "notes": "Held at 6:45 AM before erection day 1. All ironworkers attended. Questions addressed on harness attachment."
}
```

---



## JSA / JHA (Job Safety Analysis / Job Hazard Analysis)

### JSA Structure & Components

A JSA is a systematic method of identifying hazards and controls for a specific work task. The fundamental structure:

**Task Step → Hazard(s) → Control(s)**

**Template**:
```
JSA: [Task Name]
Project: {project_name}
Activity: [Specific work to be performed]
Location: [On-site location]
Date Prepared: [Date]
Prepared By: [Name, Title]
Reviewed By: [Supervisor/Safety Manager]

STEP-BY-STEP BREAKDOWN:

Step 1: [First task step]
  Hazard: [What can go wrong?]
  Control: [How to prevent it?]
  Responsible: [Who ensures it happens?]

Step 2: [Second task step]
  Hazard: [What can go wrong?]
  Control: [How to prevent it?]
  Responsible: [Who ensures it happens?]

...

APPROVAL:
Supervisor: _______________    Date: __________
Safety Manager: _______________    Date: __________
```

### Activity-Specific JSAs

#### JSA 1: Concrete Footings Pour (Foundation)

```
JSA: Concrete Footings Pour
Activity: Placing concrete in footings C1-C6, foundation phase
Location: Building perimeter, footings under columns
Date: 2026-02-18
Duration: 4 hours (estimated)
Crew: Concrete crew ({concrete_sub_name}), laborers, superintendent

PREREQUISITES:
- Forms inspected and approved
- Rebar placement verified
- Weather verified ≥40°F ambient (ACI 306)
- Concrete delivery confirmed

STEP 1: Setup & Preparation
  Hazard: Tripping/falls on muddy/uneven ground
  Control:
    - Mark walkways and clear debris
    - Install temporary walkways/planks
    - Non-slip boots required
  Responsible: Foreman

STEP 2: Concrete Delivery & Placement
  Hazard: Concrete splash causing burns
  Control:
    - Long sleeves, gloves, concrete boots required
    - Face protection optional but recommended
    - First aid kit staged at pour location
  Responsible: Concrete crew

  Hazard: Struck-by concrete pump hose (pressure hazard)
  Control:
    - Pump operator maintains clear zone around pump
    - Only trained operator manipulates hose
    - Hose pressure released before touching nozzle
  Responsible: Pump operator

  Hazard: Noise from concrete mixer and pump (>85 dB)
  Control:
    - Hearing protection required for all
    - Rotation of crew if extended exposure
  Responsible: Foreman

STEP 3: Finishing & Strike-Off
  Hazard: Reaching beyond form edges; fall potential
  Control:
    - Crew stays inside forms during finishing
    - Boards provided for crew to stand on (not forms)
    - No reaching more than arm's length
  Responsible: Finishing crew

  Hazard: Hand/finger injury from concrete tools or form contact
  Control:
    - Gloves worn during all finishing
    - Watch for concrete setting (hardens; crushing hazard)
    - Proper tool use; no makeshift implements
  Responsible: Finishing crew

STEP 4: Cleanup & Curing
  Hazard: Heavy concrete buckets; back strain
  Control:
    - Proper lifting technique (bend knees, straight back)
    - Buddy system for heavy items
    - Mechanical means (wheelbarrow) preferred
  Responsible: Laborers

  Hazard: Concrete washing; caustic burns from hydrated lime
  Control:
    - Wash residue into designated area (not storm drain)
    - Gloves/sleeves when handling wash-off
    - Rinse skin immediately if contact
  Responsible: Cleanup crew

SAFETY BRIEFING:
All pour participants attend 15-minute briefing day-of-pour covering:
- Weather verification (temperature check at start)
- Hazard review (above steps)
- Emergency procedures
- First aid kit location

WEATHER COMPLIANCE:
- Temperature ≥40°F (ACI 306 minimum)
- No rain during pour (protection added if needed)
- NOAA forecast reviewed morning-of

SIGN-OFF:
Superintendent: _______________    Date: __________
Concrete Supervisor: _______________    Date: __________
Safety Manager: _______________    Date: __________

UPDATES REQUIRED IF:
- Weather conditions change
- New work methods introduced
- Incident or near-miss occurs
- Regulatory change or new spec requirement
```

#### JSA 2: Structural Steel Erection (PEMB)

```
JSA: PEMB Column Erection & Connection
Project: {project_name}
Activity: Installing structural steel/PEMB columns, connections, and bracing (read eave height from plans-spatial.json)
Location: Multiple bays (Bays 1-6), structural system
Duration: 10 days (estimated)
Start Date: 2026-03-23
Crew: Ironworkers ({steel_sub_name}), crane operator, rigger, spotters, superintendent

CRITICAL HAZARDS:
- Fall from height (read from plans-spatial.json building height — fatality potential)
- Struck-by suspended load (fatality potential)
- Crushing (load shift during assembly)

PREREQUISITE REQUIREMENTS:
- All workers have fall protection training
- Harnesses, lanyards, and anchor points inspected
- Crane certification and load calculations verified
- Rigging plan and load testing documented
- Site-specific PEMB erection procedure approved by structural engineer
- Weather conditions verified (wind <25 MPH)

STEP 1: Site Preparation & Layout
  Hazard: Tripping on ground obstacles; falls on uneven terrain
  Control:
    - Clear site of debris and obstacles
    - Mark column locations and lifting areas
    - Establish exclusion zone around work area
  Responsible: Site crew

  Hazard: Crane stability on soft/uneven ground
  Control:
    - Soil bearing capacity verified
    - Matting provided under outriggers
    - Competent leveling of crane base
  Responsible: Crane operator & site supervisor

STEP 2: Rigging & Lift Planning
  Hazard: Improper load rigging; dropped load
  Control:
    - Rigging plan developed per AISC manual
    - Slings, shackles, chains inspected and certified
    - Load weight verified (nameplate + connection hardware)
    - Rigging inspection completed before each lift
    - Rigging hardware affixed per plan (no improvisation)
  Responsible: Certified rigger; verified by crane operator

  Hazard: Rigging attachment points damaged/weak
  Control:
    - Lifting lugs on beams verified intact
    - No lifting from welds or painted surfaces
    - Written lift plan specific to beam orientation
  Responsible: Rigger & PEMB manufacturer instructions

STEP 3: Crane Positioning & Communication
  Hazard: Loss of communication between operator and spotters; load movement unpredictable
  Control:
    - Radio communication system tested before work
    - Defined hand signals and radio protocol
    - Primary and backup spotters assigned
    - Spotter positioned to see operator at all times
    - No communication = no movement
  Responsible: Crane operator & spotters

  Hazard: Crane boom contact with existing structures or utilities
  Control:
    - Swing area cleared of workers and obstacles
    - Power lines marked (50-foot minimum clearance)
    - Boom path verified for interference
    - Spotter monitors swing path
  Responsible: Site supervisor & spotters

STEP 4: Load Positioning & Installation
  Hazard: Suspended load movement during positioning; worker struck
  Control:
    - All ground personnel clear of load path
    - Workers stay behind spotter/safety line
    - No workers under suspended load (100% rule)
    - Load movement slow and controlled
    - Crane operator stops movement if personnel move into zone
  Responsible: Crane operator, spotters, ironworker supervisor

  Hazard: Column drift during placement; guy-wire failure
  Control:
    - Guy wires attached per PEMB plan before column set
    - Guy-wire tension verified by both operator and ironworker
    - Tension equalization checked (diagonal guy wires)
    - No bolting begins until column stable
  Responsible: Ironworker foreman & rigger

STEP 5: Column Connection & Bolting
  Hazard: Pinching (crushing fingers in bolt connections)
  Control:
    - Bolt holes aligned with drift pins before bolting
    - Proper tools used (impact wrench, not hand tools)
    - Crew watches for pinch points
    - Hands clear of connection points during torquing
  Responsible: Ironworker crew

  Hazard: Falls while bolting at height (36 feet)
  Control:
    - 100% fall protection harness worn at all times
    - Lanyard attached to column perimeter cable (installed by rigging crew)
    - No moving between anchor points without prior attachment
    - Buddy system (workers work in pairs)
    - Shock-absorbing lanyards used for fall distances >6 feet
  Responsible: Each ironworker; verified by supervisor

  Hazard: Tool drops from height; struck-by objects
  Control:
    - All tools tethered (lanyard or magnetic clip)
    - No tools left on column edges or beams
    - Tools passed hand-to-hand at height (not tossed)
    - Hard hats required for all personnel below working height
  Responsible: Ironworker crew & spotters

STEP 6: Bracing & Stability
  Hazard: Column movement before final bolting; instability
  Control:
    - Temporary bracing installed per PEMB plan
    - Bracing attached to columns and ground anchors
    - Bracing inspection completed by superintendent
    - No removal of bracing until engineer approval
  Responsible: Ironworker foreman

STEP 7: Roof Beam Installation (Phase 2)
  Hazard: Same as column erection (falls, struck-by, crushing)
  Control:
    - Same fall protection, communication, and lifting protocols
    - Additional focus: roof height 36 feet; long span beams
    - Sag calculations monitored (beam deflection during install)
    - Lateral bracing required during assembly
  Responsible: All crew members; engineer oversight

WEATHER COMPLIANCE:
- Wind speed <25 MPH (OSHA 1926.752 requirement for crane work)
- No precipitation during lifts (wet rigging hazard)
- Temperature monitoring (extreme heat/cold impact on rigging)
- Daily weather briefing before erection

EMERGENCY PROCEDURES:
- If load becomes unstable during lift:
  → Operator lowers load to ground slowly
  → All personnel clear of landing zone
  → Investigation before next lift
  → Supervisor and safety manager briefed

TRAINING REQUIREMENTS:
- All crew: Fall protection, communication, lifting hazards (2 hours)
- Rigging crew: Rigging certification, load calculations (4 hours + AISC manual)
- Ironworker supervisor: OSHA 1926.500-550 (fall, crane, rigging standards)
- Crane operator: Certification + equipment-specific training

DAILY SAFETY BRIEFING:
6:45 AM before work start:
- Weather check
- Rigging inspection results
- Communication protocol review
- Previous day's issues
- Day's lift sequence

SIGN-OFF:
Project Superintendent: _______________    Date: __________
Ironworker Supervisor: _______________    Date: __________
Crane Operator: _______________    Date: __________
Safety Manager: _______________    Date: __________
Structural Engineer (approval): _______________    Date: __________

DOCUMENTATION:
- Lift plan (signed by engineer)
- Rigging inspection reports (daily)
- Daily safety briefing attendance
- Incident reports (if any)
- Photographic record

UPDATES REQUIRED IF:
- Weather conditions significantly change
- New crew members join (additional training)
- Equipment changes (different crane, rigging)
- Incident or near-miss occurs
- Structural engineer requires plan modification
```

#### JSA 3: Excavation & Fill Removal

```
JSA: Excavation & 3.5-Foot Fill Removal
Project: {project_name}
Activity: Removing undocumented fill and native excavation; 2,000 PSF bearing verification
Location: Building footprint area (approx. 10,000 SF)
Duration: 3-4 weeks
Crew: Earthwork crew (Walker Land Company), excavator operator, geotech inspector, compaction crew

CRITICAL HAZARD: CAVE-IN
- Building footprint has 3.5-foot undocumented fill in Bays B-1, B-2, B-4, B-5
- Frost-susceptible soils below fill (per geotech report)
- Risk: Improper excavation creates unstable slopes → crew injuries/fatalities

PREREQUISITE REQUIREMENTS:
- Geotechnical report reviewed and understood
- Site-specific excavation safety plan completed
- Competent person (geotech inspector) assigned
- Daily competent person inspections required
- Shoring or sloping plan finalized per soil type

STEP 1: Site Survey & Marking
  Hazard: Striking existing utilities (underground water, sewer, electric)
  Control:
    - One-call system activated (all utilities located and marked)
    - Marked areas observed and photographed
    - Excavation stopped immediately if utility discovered
    - Utility company contacted to verify marks
  Responsible: Site supervisor

STEP 2: Excavation Trenching
  Hazard: Trench cave-in; worker crushed under soil collapse
  Control:
    - Competent person inspects trench daily (before work, after rain, soil condition change)
    - Proper sloping per OSHA (angle varies by soil type):
      - Type A soil: 3.5:1 slope (not applicable; frost-susceptible)
      - Type B soil (typical): 1:1 slope
      - Type C soil (weak): vertical wall + shoring
    - Trench <5 feet depth: sloping acceptable
    - Trench >5 feet depth: shoring/bracing required
  Responsible: Competent person (geotech inspector); excavator operator

  Hazard: Striking underground utilities in trench; electrocution, gas explosion, water surge
  Control:
    - Utilities clearly marked and flagged
    - Excavate within 2 feet of marked utility: hand dig (no equipment)
    - Utility company on standby (contact listed on signs)
    - Stop work if utility encountered; do not attempt removal
  Responsible: Operator; verification by supervisor

  Hazard: Struck-by excavator bucket or moving equipment
  Control:
    - Exclusion zone established (radius = bucket reach + 10 feet)
    - Only essential personnel in zone
    - Spotter assigned for all bucket moves
    - Visual and radio contact maintained
    - Equipment movement announced ("Bucket moving left")
  Responsible: Excavator operator & spotters

STEP 3: Spoil Pile Management
  Hazard: Spoil pile collapse; worker crushed
  Control:
    - Spoil piles located outside trench walls (minimum 2-foot distance)
    - Pile slope not steeper than 2:1
    - No personnel standing on or walking along pile edges
    - Stockpile stabilized with barriers if near walkways
  Responsible: Excavation crew; site supervisor

STEP 4: Atmospheric Monitoring (if Fill Removal Extends >5 feet)
  Hazard: Oxygen deficiency or toxic gases in deeper excavation
  Control:
    - Atmospheric testing required if depth >5 feet or confined space conditions
    - Testing: oxygen (19.5-23.5%), LEL (<25%), H2S, CO, CO2
    - Testing performed daily at start of work
    - Continuous ventilation (blowers) if poor air quality
    - SCBA or supplied air if entry into poor-air zone
  Responsible: Geotech inspector or certified gas detection technician

STEP 5: Fill Removal Verification
  Hazard: Incomplete fill removal; inadequate bearing capacity; foundation failure risk
  Control:
    - Fill removal verified to design depth per geotech report (3.5 feet removal required)
    - Cross-sectional verification at multiple locations (grid pattern)
    - Verification photos documented with depth markers
    - Geotech inspector sign-off before next phase
    - Proofroll (loaded tandem-axle truck) testing per geotech observation
  Responsible: Geotech inspector; documented in daily reports

STEP 6: Subgrade Preparation & Compaction
  Hazard: Inadequate compaction; poor bearing; future settlement
  Control:
    - Compaction to 98% standard proctor per specifications
    - Moisture content within 2% of optimum (per geotech specs)
    - Compaction verified by density testing (nuclear gauge or sand cone)
    - Compaction areas marked and documented
    - Rework any areas not meeting specification
  Responsible: Compaction crew; geotech verification

STEP 7: Utility Trench Backfill
  Hazard: Improper backfill; trench collapse; utility damage
  Control:
    - Utility trenches backfilled within 5 feet of building with flowable fill (per geotech)
    - Non-frost-susceptible (NFS) material only under building
    - Compaction per plan; density verification
    - Backfill material tested (gradation, moisture)
  Responsible: Backfill crew; geotech verification

WEATHER COMPLIANCE:
- No excavation if frozen material present (thaw required)
- Moisture content within 2% of optimum (no wet or dry conditions)
- Proofroll testing suspended if unsafe (rain, mud, poor bearing)

EMERGENCY PROCEDURES:
- Trench collapse: Immediate evacuation; no rescue attempts without shoring
- Utility strike: Immediately stop all work; call utility company; assess damage
- Atmospheric hazard: Ventilate area; evacuate personnel; continuous monitoring before re-entry

COMPETENT PERSON QUALIFICATIONS:
- Geotech inspector (professional engineer or certified)
- OSHA 1926.650 excavation training
- Field experience with frost-susceptible soils
- Authority to stop work if unsafe conditions develop

DAILY INSPECTIONS:
Competent person daily report includes:
- Visual inspection of trench walls (sloping, stability)
- Shoring/bracing condition assessment
- Atmospheric test results (if applicable)
- Fill removal progress verification
- Compaction test results
- Photos of critical areas

SIGN-OFF:
Project Superintendent: _______________    Date: __________
Excavation Foreman: _______________    Date: __________
Geotech Inspector: _______________    Date: __________
Safety Manager: _______________    Date: __________

DOCUMENTATION:
- Daily competent person inspection reports (with photos)
- Proofroll testing results
- Compaction density test results
- Atmospheric test results (if applicable)
- Utility location marks (photographs)
- Incident reports (if any)

UPDATES REQUIRED IF:
- Soil conditions change from geotech assumptions
- Utilities discovered not previously marked
- Weather impacts work sequence
- Incident or near-miss occurs
- Compaction testing shows non-compliance
```

#### JSA 4: Roofing Panel Installation

```
JSA: PEMB Roof Panel Installation & Attachment
Project: {project_name}
Activity: Installing metal roof panels on PEMB structure; 1:12 slope
Location: Full roof (75' x 132'-8")
Duration: 10 days (estimated)
Crew: Roofing crew, panel installer, fastening crew, safety personnel

CRITICAL HAZARD: FALL FROM HEIGHT
- Roof height: 36 feet (eave)
- Roof slope: 1:12 (low slope; minimal edge protection)
- Fatality risk: Fall from height with inadequate fall protection

PREREQUISITE REQUIREMENTS:
- All roofers trained in fall protection (OSHA 1926.500-501)
- Harnesses, lanyards, anchor points inspected and certified
- Roof safety system installed per plan (cable lifeline or anchor points)
- Weather conditions verified before start (wind <25 MPH, dry conditions)

STEP 1: Roof Preparation & Safety System Installation
  Hazard: Harness attachment points not yet ready; workers at unprotected height
  Control:
    - Roof cable lifeline installed first (before any worker on roof)
    - Lifeline tested with 5,000-pound anchor load
    - Anchor points spaced per OSHA requirement (8-10 feet maximum apart)
    - Sign-off by structural engineer before use
    - Workers tethered to lifeline via shock-absorbing lanyard
  Responsible: Rigging crew; verified by structural engineer

  Hazard: Tripping/falling on roof surface during panel placement
  Control:
    - Roof surface cleaned of debris and water
    - Non-slip surface or walkways provided
    - Footwear with grip (not leather soles)
    - Buddy system (no solo roofing work)
  Responsible: Roofing crew

STEP 2: Panel Delivery & Staging
  Hazard: Panel stack collapse; worker struck by falling panels
  Control:
    - Panels delivered by crane (controlled placement)
    - Staging area established away from pedestrian traffic
    - Stacks stabilized and secured
    - Stack height limited (8 panels maximum per manufacturer)
    - Panels handled with proper equipment (panel lifter, not hands)
  Responsible: Roofing foreman

STEP 3: Panel Installation on Roof Structure
  Hazard: Falls from height during panel placement and fastening
  Control:
    - 100% fall protection harness worn at all times
    - Lanyard attached to roof lifeline (never to anything else)
    - Movement between lifeline anchor points:
      → Stop, unclip from current anchor
      → Re-clip to lifeline before stepping away
      → Never more than arm's length from attachment
    - Shock-absorbing lanyard (minimum 5 feet length)
    - Hard hats worn at all times
    - Buddy system: roofers work in pairs; visual contact maintained
  Responsible: Each roofer; supervised by roofing foreman

  Hazard: Panel contact with live electrical circuits (utilities in building)
  Control:
    - Electrical circuits de-energized during roofing (lockout/tagout)
    - Non-conductive roofing materials (unless grounded)
    - GFCI protection on temporary power for tool use
  Responsible: Electrical supervisor

STEP 4: Fastening & Sealing
  Hazard: Hand/finger injuries from power tools (impact wrench, bolt gun)
  Control:
    - Proper tool operation and maintenance (no defective tools)
    - Clear communication before tool use ("tool coming in")
    - Guards in place; safety features functional
    - Hands clear of fastening points
  Responsible: Fastening crew

  Hazard: Sealant fumes in enclosed roofing area
  Control:
    - Adequate ventilation during sealant application
    - Respiratory protection if ventilation poor
    - Sealant per spec (typically polyurethane or silicone)
    - Drying time observed before personnel traffic
  Responsible: Sealing crew; supervisor verification

STEP 5: Roof Edges & Drip Edge Completion
  Hazard: Fall from roof edge during drip edge installation
  Control:
    - Guardrails installed on roof edges (42" top rail, 21" mid-rail)
    - Personal fall protection for workers on roof edge
    - No reaching beyond rail without harness attachment
    - Fall protection verified before edge work
  Responsible: Roofing crew; safety manager verification

WEATHER COMPLIANCE:
- Wind speed <25 MPH (OSHA 1926.752 requirement; impacts fall protection)
- No rain or wet roof surface (slipping hazard)
- Temperature >40°F for sealant application (spec requirement for adhesion)
- Temperature monitoring: Stop work if <32°F (ice formation risk)
- Daily weather briefing before roof work

EMERGENCY PROCEDURES:
- Worker fall: Immediate stop work; rescue equipment staged; call 911
- High wind: All personnel off roof; work suspended until wind <25 MPH
- Sealant exposure: Rinse with water; medical evaluation if eyes/lungs affected

TRAINING REQUIREMENTS:
- All roofers: Fall protection certification (OSHA 1926.500)
- Harness inspection and use (hands-on training)
- Rescue procedures (in case of fall)
- Weather monitoring protocol

DAILY SAFETY BRIEFING:
6:30 AM before roof work:
- Weather check and forecast
- Wind speed verification
- Fall protection equipment inspection results
- Day's work sequence
- Communication protocol
- Previous day's issues

SIGN-OFF:
Project Superintendent: _______________    Date: __________
Roofing Supervisor: _______________    Date: __________
Safety Manager: _______________    Date: __________
Structural Engineer (lifeline approval): _______________    Date: __________

DOCUMENTATION:
- Roof lifeline installation and testing report
- Harness and lanyard inspection logs
- Daily weather documentation
- Daily safety briefing attendance
- Incident reports (if any)
- Photographic record of safety systems

UPDATES REQUIRED IF:
- Weather conditions exceed thresholds
- Worker injury or near-miss occurs
- New crew members join (additional training)
- Equipment changes (different harness, lifeline system)
- Roof damage discovered (re-inspection required)
```

### JSA Review & Update Triggers

JSAs must be reviewed and updated when:
1. **New Activity**: First time performing activity on this project
2. **After Incident/Near-Miss**: JSA modified to address root cause
3. **Significant Weather Change**: Extreme heat, cold, rain, wind affecting hazards
4. **Specification Change**: New material, method, or procedure requirement
5. **Regulatory Update**: New OSHA standard or requirement
6. **Lesson Learned**: Experience on project reveals new or underestimated hazard
7. **Annual Review**: JSA reviewed yearly (minimum)

**Update Procedure**:
- Safety manager initiates review
- Original JSA creator and current work supervisor involved
- Discussion with crew members (who perform work)
- Modifications documented with date and reason
- Updated JSA approved by supervisor and safety manager
- New sign-off obtained before work resumes
- Old version archived (version control)

---



## OSHA Recordkeeping

### OSHA 300 Log

The OSHA 300 Log is the official record of all **recordable** work-related injuries and illnesses. It must be maintained, posted, and retained per 29 CFR 1904.

**Recordable Incident Criteria** (recap):
- Work-related AND
- Involves medical treatment beyond first aid OR
- Restricted duty OR
- Days away from work (≥1) OR
- Loss of consciousness OR
- Significant injury/illness diagnosed by healthcare provider

**OSHA 300 Form Columns**:

```
Line | (A) Case Number | (B) Employee Name | (C) Job Title |
     | (D) Date Injury/Illness | (E) Date Reported | (F) Where Incident |
     | (G) Description | (H) Classification | (I) Days Away |
     | (J) Restricted Duty | (K) Other Outcome | (L-Q) Type of Injury

CLASSIFICATION (Column H):
  ☐ Injury          (acute trauma)
  ☐ Skin Disease    (contact dermatitis, etc.)
  ☐ Respiratory     (asthma, silicosis, etc.)
  ☐ Poisoning       (chemical exposure, etc.)
  ☐ Hearing Loss    (noise-induced)
  ☐ All Other       (misc. illnesses)

DAYS AWAY (Column I):
  Count calendar days employee unable to work
  Start date: first day unable to work
  End date: last day unable to work

RESTRICTED DUTY (Column J):
  Employee returns to work but on modified/light duty
  (e.g., cannot climb ladders; can only perform desk work)
```

**OSHA 300 Log Template**:
```
OSHA 300 LOG OF WORK-RELATED INJURIES AND ILLNESSES
Project: {project_name}
Year: 2026

Line | Case # | Employee | Job Title | Date | Reported | Where | Description | Classification | Days Away | Restricted | Other

1 | 2026-001 | [Name] | Ironworker | 02/16 | 02/18 | Structural Steel | Laceration to forehead during ladder work | Injury | 0 | 2 | X (medical treatment)

---

SUMMARY PAGE (OSHA 300A):
Total recordable cases: __
Total deaths: __
Total cases with days away: __
Total cases with restricted duty: __
Total other recordable cases: __
```

### OSHA 301 Incident Report Form

For each recordable incident, a detailed **OSHA 301 Incident Report** is completed.

**OSHA 301 Form Contents**:

```
OSHA 301 - INJURY AND ILLNESS INCIDENT REPORT

Employee Information:
  Name: _______________
  Address: _______________
  Phone: _______________
  Date of Birth: _______________
  Social Security #: _______________
  Sex: ☐ Male ☐ Female

Employment Information:
  Job Title: _______________
  Department: _______________
  Hire Date: _______________
  Usual Job: _______________

Incident Details:
  Date of Incident: _______________
  Time: _______________
  Location: _______________
  What was the employee doing? _______________
  What happened? _______________
  What caused the injury/illness? _______________

Injury/Illness Description:
  ☐ Injury ☐ Illness
  Body Part(s) Affected: _______________
  Type of Injury: _______________

Medical Treatment:
  Treated by: ☐ First Aid ☐ Urgent Care ☐ Emergency ☐ Hospital
  Facility Name: _______________
  Treatment Description: _______________

Work Status:
  ☐ Days Away from Work (start date: ___, end date: ___)
  ☐ Restricted Duty (start date: ___, duration: ___ days)
  ☐ Other (specify): _______________

Witnesses:
  Name: _______________
  Address: _______________
  Phone: _______________

Employee Signature: _______________ Date: _______________
Supervisor: _______________ Date: _______________
```

### OSHA 300A Annual Summary

At the end of each calendar year, an **OSHA 300A Annual Summary** is generated summarizing all recordable incidents and posted through March 15.

**300A Contents**:
```
OSHA 300A - ANNUAL SUMMARY

Injuries and Illnesses Summary for Year 2026

Total Recordable Cases: ___
  Days Away from Work: ___
  Job Transfer/Restricted Duty: ___
  Other Recordable Cases: ___

Total Deaths: ___

Total Employees: ___
Total Hours Worked: ___

Signature of Authorized Company Official: _______________
Title: _______________
Date: _______________
```

**Posting Requirement**:
- Posted from February 1 - March 15 (at minimum)
- Visible to all employees
- No modifications or corrections after posting begins
- Updated through March 15

---



## Safety Metrics & Reporting

### TRIR (Total Recordable Incident Rate)

**Definition**: Number of recordable incidents per 200,000 hours worked (standard industry metric representing 100 full-time employees working 1 year).

**Formula**:
```
TRIR = (Total Recordable Cases × 200,000) / Total Hours Worked

Example:
  Recordable Cases in 2026: 2
  Total Hours Worked: 50,000 hours
  TRIR = (2 × 200,000) / 50,000 = 8.0

  Interpretation: 8.0 TRIR means 8 recordable incidents per 200,000 hours
  Industry Average (Construction): 3.5-4.0 TRIR
  Project Rating: ABOVE AVERAGE INCIDENT RATE (needs improvement)
```

**Calculation Frequency**: Monthly, quarterly, annually

**Benchmark Comparison**:
- Construction Industry Average: 3.5-4.0 TRIR
- Excellent Safety Culture: <2.0 TRIR
- Poor Safety Performance: >6.0 TRIR

### DART Rate (Days Away, Restricted, Transferred)

**Definition**: Number of incidents with days away from work OR restricted duty OR job transfer per 200,000 hours worked.

**Formula**:
```
DART Rate = (Total DART Cases × 200,000) / Total Hours Worked

Total DART Cases = Cases with Days Away + Restricted Duty + Job Transfer

Example:
  Cases with Days Away: 1
  Cases with Restricted Duty: 1
  Cases with Job Transfer: 0
  Total DART Cases: 2
  Total Hours Worked: 50,000
  DART Rate = (2 × 200,000) / 50,000 = 8.0

  Interpretation: 8.0 DART rate
  Industry Average: 2.5-3.0 DART rate
  Project Rating: ABOVE AVERAGE SEVERITY
```

**Comparison to TRIR**:
- DART rates are subset of TRIR (only incidents with work impact)
- DART rate indicates severity (how many incidents caused lost time)
- High DART with low TRIR = few incidents, but severe
- High TRIR with low DART = many incidents, mostly minor

### EMR (Experience Modification Rate)

**Definition**: EMR is used by workers' compensation insurance to adjust premium rates based on company's safety history compared to industry average.

**EMR Calculation** (simplified):
```
EMR = Actual Loss Experience / Expected Loss Experience

EMR = 1.0: Company at average risk (standard rates)
EMR < 1.0: Company better than average (rate discount, e.g., 0.85 = 15% discount)
EMR > 1.0: Company worse than average (rate increase, e.g., 1.25 = 25% premium increase)

3-Year Experience Period: Most insurance carriers use trailing 3-year loss history
```

**Impact**: EMR directly affects company insurance costs:
- Better EMR (lower than 1.0) = lower premiums (financial incentive for safety)
- Worse EMR (higher than 1.0) = higher premiums (financial penalty)

**How to Improve EMR**:
1. Reduce recordable incident frequency (fewer claims)
2. Reduce severity (fewer/shorter days away from work)
3. Implement robust safety program (demonstrates commitment)
4. Return-to-work programs (reduce days away)
5. Incident investigation and corrective actions (prevent recurrence)

### Leading Indicators vs. Lagging Indicators

**Lagging Indicators** (after-the-fact; reactive):
- Recordable incidents
- TRIR rate
- DART rate
- Days away from work
- Medical costs
- Workers' compensation claims

**Leading Indicators** (proactive; preventive):
- Toolbox talks held
- JSAs completed/reviewed
- Safety inspections conducted
- Near-miss reports
- Corrective actions completed
- Training attendance
- Pre-task planning performed
- Safety violations identified and corrected

**Key Principle**: Focus on **leading indicators**. Improving leading indicators drives down lagging indicators.

**Example**:
- Leading: Increase toolbox talks from 1/week to 5/week (more safety communication)
- Expected Result: Fewer incidents (improved lagging indicator)

### Weekly/Monthly Safety Summary

**Weekly Safety Report** (every Friday):

```
WEEKLY SAFETY REPORT
Project: {project_name}
Week of: 2026-02-16

INCIDENTS & INJURIES:
  Recordable Incidents: 0
  Near-Misses: 2
  First Aid: 1
  Lost Time: 0 hours

TOOLBOX TALKS:
  Topics Held This Week: 3
    - PEMB Erection Safety (2/18, 12 attendees)
    - Concrete Placement (2/17, 8 attendees)
    - Excavation Safety (2/19, 6 attendees)
  Total Attendees: 26

JSA UPDATES:
  New JSAs Completed: 1 (Roofing Panel Installation)
  JSAs Reviewed: 2 (Concrete Pour, Excavation)

SAFETY INSPECTIONS:
  Formal Inspections: 2
  Deficiencies Found: 3
    - Missing guardrail on temporary platform (corrected same day)
    - Electrical cord damaged (replaced)
    - Scaffolding not properly braced (corrected within 24 hrs)
  Deficiencies Corrected: 3 (100% closure)

LEADING INDICATORS:
  Total Hours Worked: 1,250 hours
  TRIR (YTD): 0.0 (zero incidents)
  Incident-to-Near-Miss Ratio: 1:2 (good safety culture)
  Near-Misses Per Week: 2

WEATHER & SITE CONDITIONS:
  No weather delays this week
  Temperature range: 28°F - 42°F
  Conditions within spec thresholds

SAFETY ALERTS:
  None this week

NEXT WEEK FOCUS:
  - PEMB erection begins (high-risk phase)
  - Daily safety briefings (steel erection hazards)
  - Harness and lifeline inspection
  - Increase toolbox talks during erection phase

Submitted by: [Safety Manager Name]
Date: 2026-02-21
```

**Monthly Safety Metrics Dashboard**:

```
MONTHLY SAFETY REPORT
Project: {project_name}
Month: February 2026

MONTHLY STATISTICS:
  Recordable Incidents: 0
  Total Injuries/Illnesses: 3 (1 recordable, 2 first aid)
  Near-Misses: 4
  Lost Time (hours): 0
  Near-Miss to Incident Ratio: 4:1 (good; >1:1 indicates proactive culture)

TRIR CALCULATION (YTD):
  Total Recordable Cases: 1 (injury requiring medical treatment)
  Total Hours Worked YTD: 2,500 hours
  TRIR YTD = (1 × 200,000) / 2,500 = 80.0

  Note: TRIR will stabilize as hours accumulate. First month inflated due to low denominator.

DART RATE (YTD):
  Total DART Cases: 0 (incident did not involve days away or restricted duty)
  DART Rate YTD = 0.0

LEADING INDICATORS:
  Toolbox Talks: 8 (target: 4-5/month; on track)
  JSAs Completed: 3 (Concrete Pour, Excavation, Roofing Panel Installation)
  Safety Inspections: 5 formal inspections
  Near-Miss Reports: 4 (encouraging proactive reporting)
  Training Completed: All crew orientation (100%)
  Corrective Actions Completed: 100% (all deficiencies closed)

SAFETY FOCUS AREAS:
  ✓ Strong toolbox talk participation
  ✓ High near-miss reporting (proactive hazard identification)
  ✓ Rapid corrective action closure
  ✓ Low incident rate (0 recordable for first month)

  Risk Areas:
  - PEMB erection beginning (high-risk phase upcoming)
  - Weather variability (cold/frost in February impacted excavation)
  - New crew onboarding for steel phase

UPCOMING HIGH-RISK ACTIVITIES:
  - PEMB erection (3/23-4/3): Daily safety briefings, increased inspections
  - Roofing operations (4/6-4/17): Fall protection focus
  - MEP rough-in (4/27-5/15): Confined space training (if applicable)

EMR PROJECTION:
  Current EMR: Not yet available (insufficient historical data)
  Projection: If incident rate continues at <1 recordable incident/month, EMR should improve

RECOMMENDATIONS:
  1. Maintain current toolbox talk frequency during PEMB erection
  2. Increase daily safety briefings for high-risk steel phase
  3. Verify all fall protection equipment before roofing begins
  4. Continue near-miss reporting program (demonstrates safety culture)
  5. Post monthly metrics visibly (team transparency)

Submitted by: [Safety Manager Name]
Reviewed by: [Project Manager Name]
Date: 2026-03-01
```

---



## Site Safety Inspections

### Inspection Checklists by Category

#### Category 1: Fall Protection

```
FALL PROTECTION INSPECTION CHECKLIST
Project: {project_name}
Date: _______________
Inspector: _______________
Phase/Location: _______________

☐ HARNESSES & BODY BELTS
  ☐ Harnesses present and accessible
  ☐ Harnesses inspected for damage, tears, fraying
  ☐ Proper fit (snug, not twisted, chest D-ring centered)
  ☐ All attachment points intact
  ☐ No modifications or alterations
  ☐ Correct harness type for work (full-body, not positioning)

☐ LANYARDS & SHOCK ABSORBERS
  ☐ Lanyards present (minimum 6 feet, can be shorter with retractable)
  ☐ Shock absorbers present on lanyards >6 feet
  ☐ Shock absorbers not previously deployed
  ☐ Double lanyards for transitions (never unprotected gap)
  ☐ No fraying or damage to lanyards
  ☐ Proper attachment to anchor points

☐ ANCHOR POINTS
  ☐ Anchor points identified and marked
  ☐ Anchor point capacity verified (minimum 5,000 lbs per person)
  ☐ Structural steel columns or beams (not pipes, conduit, or temporary items)
  ☐ No sharp edges that could cut/abrade lanyard
  ☐ Adequate clearance below anchor point (22-foot free fall limit)
  ☐ Multiple anchor points spaced per OSHA (8-10 feet typical)

☐ ROOF LIFELINES (if installed)
  ☐ Lifeline installed per structural engineer plans
  ☐ Lifeline tested with 5,000-pound load verification
  ☐ Lifeline cable intact (no rust, corrosion, fraying)
  ☐ Lifeline tension appropriate (slack prevents excessive fall)
  ☐ Retractable lifeline track: no obstructions or damage
  ☐ Proper spacing of attachment points

☐ GUARDRAILS (if installed)
  ☐ Top rail height 42" ± 3"
  ☐ Mid-rail height 21" ± 3" (halfway between top and walking surface)
  ☐ Toe board height ≥3.5"
  ☐ No gaps in guardrail (prevent falls through)
  ☐ Robust construction (can withstand 200-pound force)
  ☐ Proper connections (not loose or wobbly)

☐ PERSONAL FALL ARREST SYSTEM (PFAS) USE
  ☐ Workers actively tethered to anchor points (not just wearing harness)
  ☐ Proper transitions between anchor points (continuous protection)
  ☐ Buddy system observed (no solo elevated work)
  ☐ Hard hats worn at all times
  ☐ Workers competent in fall protection system use
  ☐ No working at heights without required protection

☐ TRAINING & AWARENESS
  ☐ Workers demonstrate proper harness donning (inspection observed)
  ☐ Workers understand anchor point limitations
  ☐ Workers aware of clearance space below work (landing hazards)
  ☐ Supervisor present during elevated work
  ☐ No complacency observed (routine compliance with requirements)

DEFICIENCIES FOUND:
  ☐ None - full compliance
  ☐ Minor (corrected same day):
    _________________________________________________________________
  ☐ Major (requires corrective action plan):
    _________________________________________________________________

CORRECTIVE ACTIONS:
  Action: _________________________________________________________________
  Responsible: _______________    Deadline: _______________

Inspector Signature: _______________    Date: _______________
Supervisor Acknowledgment: _______________    Date: _______________
```

#### Category 2: Excavation & Trenching

```
EXCAVATION & TRENCHING SAFETY CHECKLIST
Project: {project_name}
Date: _______________
Inspector: _______________
Location/Trench: _______________
Depth: _______________

☐ COMPETENT PERSON DESIGNATION
  ☐ Qualified competent person assigned
  ☐ Competent person present on-site during inspection
  ☐ Documentation of competent person qualifications

☐ SLOPE ANALYSIS & SHORING
  ☐ Soil type identified (geotech report reviewed)
  ☐ Proper slope angle per soil type (1:1 for Type B, steeper for Type A)
  ☐ Shoring/bracing properly installed (depths >5 feet)
  ☐ Shoring daily inspection documented
  ☐ No signs of sloughing or cave-in risk
  ☐ Bracing not overloaded or damaged

☐ ATMOSPHERIC HAZARDS
  ☐ Testing equipment available (if depth >5 feet)
  ☐ Daily atmospheric testing (O2, LEL, H2S)
  ☐ Ventilation equipment present if poor air quality
  ☐ SCBA or supplied air available if confined space entry required
  ☐ No hazardous gas accumulation observed

☐ UTILITIES & UNDERGROUND HAZARDS
  ☐ One-call system contacted (utility marking completed)
  ☐ Utilities clearly marked and flagged at trench edge
  ☐ Hand excavation within 2 feet of marked utilities
  ☐ Utility company contact info posted (phone number visible)
  ☐ No utilities struck or damaged
  ☐ Excavation stopped immediately if utility encountered

☐ ACCESS & EGRESS
  ☐ Ladder access provided (within 25 feet of any worker)
  ☐ Ladder safety requirements met (rungs intact, angle 75°)
  ☐ Ramps provided for vehicle access (proper slope, cleats)
  ☐ Access/egress clearly marked and maintained
  ☐ Multiple exits available (if depth >4 feet)

☐ EQUIPMENT OPERATION
  ☐ Excavator properly positioned (away from trench edge)
  ☐ Spotter assigned and communicating with operator
  ☐ No workers under suspended excavator bucket
  ☐ Bucket swing radius clear of personnel
  ☐ Equipment not operated near slope edges

☐ SPOIL PILE MANAGEMENT
  ☐ Spoil piles located minimum 2 feet from trench edge
  ☐ Pile slope not steeper than 2:1
  ☐ Pile stabilized (no sliding risk)
  ☐ No personnel standing on pile edges
  ☐ Barriers installed if pile near walkways

☐ PERSONAL PROTECTIVE EQUIPMENT
  ☐ Hard hats worn at all times
  ☐ High-visibility vests
  ☐ Steel-toe boots
  ☐ Appropriate gloves for task
  ☐ Respiratory protection if dust/gases

☐ WEATHER & ENVIRONMENTAL
  ☐ Frozen material properly thawed before excavation
  ☐ Moisture content within specification
  ☐ No water accumulation (pumping/dewatering if needed)
  ☐ Weather monitoring (no work during heavy rain)
  ☐ Ice/frost cleared from surfaces

☐ DAILY COMPETENT PERSON REPORT
  ☐ Inspection documented in daily report
  ☐ Photos taken (slope condition, shoring, utilities)
  ☐ Any hazards identified and corrected
  ☐ Signature of competent person

DEFICIENCIES FOUND:
  ☐ None - full compliance
  ☐ Minor (corrected same day):
    _________________________________________________________________
  ☐ Major (work halted; corrective action required):
    _________________________________________________________________

CORRECTIVE ACTIONS:
  Action: _________________________________________________________________
  Responsible: _______________    Deadline: _______________

Inspector Signature: _______________    Date: _______________
Competent Person: _______________    Date: _______________
```

#### Category 3: Electrical Safety

```
ELECTRICAL SAFETY INSPECTION CHECKLIST
Project: {project_name}
Date: _______________
Inspector: _______________
Phase/Location: _______________

☐ TEMPORARY POWER DISTRIBUTION
  ☐ GFCI protection on all temporary power circuits
  ☐ Ground-fault protection verified (test function)
  ☐ Electrical service adequate (not overloaded)
  ☐ Temporary wiring properly sized and protected
  ☐ Main disconnect accessible and labeled

☐ POWER CORDS & EQUIPMENT
  ☐ All cords inspected (no damage, cuts, splices)
  ☐ Three-prong plugs on all equipment (proper grounding)
  ☐ Cords protected from foot traffic (covers or routing)
  ☐ No cords run through water
  ☐ Equipment maintained and functioning safely
  ☐ Extension cords rated for wet locations (if used outdoors)

☐ LOCKOUT / TAGOUT (LOTO)
  ☐ Energy source de-energized before work (lockout applied)
  ☐ Lockout devices installed and labeled
  ☐ Tags clearly stating hazard and responsible person
  ☐ All energy sources isolated (electrical, mechanical, hydraulic)
  ☐ Energy tested de-energized before work begins
  ☐ LOTO not removed until work complete

☐ HOT WORK PERMITS
  ☐ Hot work permit posted before welding/cutting
  ☐ Fire watch assigned and positioned
  ☐ Combustibles cleared within 35-foot radius
  ☐ Fire extinguisher accessible
  ☐ Area ventilated (fumes not accumulating)
  ☐ Arc flash hazard assessment complete

☐ LIVE CIRCUITS & ENERGIZED EQUIPMENT
  ☐ Electrical equipment properly guarded
  ☐ No live wires accessible to personnel
  ☐ Maintenance work performed de-energized (LOTO)
  ☐ Proper PPE for live-work situations (if unavoidable)
  ☐ Insulated tools used near live circuits

☐ UTILITY COORDINATION
  ☐ Existing utilities located and marked (one-call system)
  ☐ Trench work done with utility awareness
  ☐ Call-before-you-dig observed
  ☐ No overhead lines struck during equipment operation
  ☐ 50-foot clearance from power lines (or de-energized)

☐ PERSONNEL TRAINING
  ☐ Electrical personnel qualified/licensed
  ☐ Safety training completed (OSHA 1926.300)
  ☐ Hazard awareness demonstrated
  ☐ Proper tool use observed

DEFICIENCIES FOUND:
  ☐ None - full compliance
  ☐ Minor (corrected same day):
    _________________________________________________________________
  ☐ Major (work halted; corrective action required):
    _________________________________________________________________

CORRECTIVE ACTIONS:
  Action: _________________________________________________________________
  Responsible: _______________    Deadline: _______________

Inspector Signature: _______________    Date: _______________
Electrical Supervisor: _______________    Date: _______________
```

#### Category 4: Housekeeping & General Safety

```
HOUSEKEEPING & GENERAL SITE SAFETY CHECKLIST
Project: {project_name}
Date: _______________
Inspector: _______________
Phase/Location: _______________

☐ WALKWAYS & WORK AREAS
  ☐ Walkways clear of debris, trip hazards
  ☐ Materials stacked safely (not toppling)
  ☐ Spilled liquids cleaned up promptly
  ☐ Cable/hose routing clear of traffic paths
  ☐ Adequate lighting in work areas and pathways
  ☐ Slippery surfaces identified and treated (sand/salt)

☐ MATERIAL STORAGE & STACKING
  ☐ Materials stored in designated areas
  ☐ Stacks stable and secured (no tipping hazard)
  ☐ Heavy materials on bottom, light on top
  ☐ Load limits respected (no overloading)
  ☐ Material identification/labels visible
  ☐ Flammable materials stored per fire code

☐ WASTE MANAGEMENT
  ☐ Waste containers present and clearly marked
  ☐ Containers not overflowing
  ☐ Hazardous waste properly segregated
  ☐ Regular waste removal schedule observed
  ☐ No accumulation of loose materials

☐ EMERGENCY EQUIPMENT & EGRESS
  ☐ First aid kit accessible and stocked
  ☐ Emergency eye wash station available (if chemicals)
  ☐ AED (Automated External Defibrillator) on-site
  ☐ Fire extinguishers accessible (rated for fuels present)
  ☐ Emergency exits clearly marked and unobstructed
  ☐ Emergency contact numbers posted

☐ SIGNAGE & HAZARD COMMUNICATION
  ☐ Hazard signs posted (biological, chemical, radiation, noise)
  ☐ OSHA 300A summary posted (safety performance)
  ☐ Safety rules posted and visible
  ☐ Forklift/vehicle warning signs present
  ☐ "No Entry" or "Authorized Personnel Only" clearly marked
  ☐ Electrical hazard warnings where applicable

☐ PERSONAL PROTECTIVE EQUIPMENT
  ☐ PPE provided and accessible
  ☐ Hard hats worn at all times (observe compliance)
  ☐ Safety glasses in work areas
  ☐ Steel-toe boots observed
  ☐ High-visibility vests worn
  ☐ Gloves available and used appropriately

☐ ENVIRONMENTAL CONDITIONS
  ☐ Adequate ventilation in work areas
  ☐ Noise levels monitored (hearing protection if >85 dB)
  ☐ Dust suppression active (water spray, not visible dust)
  ☐ Temperature monitoring (heat/cold stress management)
  ☐ Humidity/moisture control (no slipping hazards)

☐ EQUIPMENT MAINTENANCE
  ☐ Equipment clean and functioning safely
  ☐ Maintenance documented
  ☐ Defective equipment removed from service
  ☐ Inspections completed on schedule (scaffolds, cranes, etc.)
  ☐ Repairs performed by qualified personnel

☐ VEHICLE & EQUIPMENT SAFETY
  ☐ Vehicle parking in designated areas (not obstructing)
  ☐ Reverse alarms functional on heavy equipment
  ☐ Spotters used for equipment movement
  ☐ Speed limits enforced on-site
  ☐ Operators properly licensed/certified

DEFICIENCIES FOUND:
  ☐ None - full compliance
  ☐ Minor (corrected same day):
    _________________________________________________________________
  ☐ Major (corrective action plan required):
    _________________________________________________________________

CORRECTIVE ACTIONS:
  Action: _________________________________________________________________
  Responsible: _______________    Deadline: _______________

Inspector Signature: _______________    Date: _______________
Supervisor: _______________    Date: _______________
```

### Deficiency Tracking & Corrective Actions

**Deficiency Classification**:

1. **Minor** (Corrected Same Day)
   - Low hazard severity
   - Quick/simple fix
   - Examples: PPE not worn, cable in walkway (moved), unsecured tool
   - Closed: Same day or within 24 hours

2. **Major** (Requires Formal Corrective Action Plan)
   - Higher hazard severity
   - Requires resources, planning, or engineering
   - Examples: Improper shoring, missing anchor points, equipment defect
   - Timeline: 3-7 days typical; depends on hazard severity

**Corrective Action Tracking**:
```json
{
  "id": "DEFICIENCY-001",
  "date_found": "2026-02-18",
  "inspection_type": "fall_protection",
  "location": "Structural steel erection area",
  "severity": "major",
  "description": "Missing mid-rail on temporary platform guardrail; workers at risk of fall",
  "root_cause": "Misunderstanding of OSHA guardrail requirements (21\" mid-rail requirement)",
  "corrective_action": "Install mid-rail on all temporary platforms per OSHA 1926.501; conduct toolbox talk on guardrail specifications",
  "responsible_party": "Ironworker Supervisor",
  "deadline": "2026-02-20",
  "status": "in_progress",
  "closure_date": "2026-02-20",
  "closure_notes": "Mid-rail installed; toolbox talk held 2/19; re-inspection completed same day",
  "verification": "Photos taken; supervisor signature"
}
```

---



## Data Store Integration

### safety-log.json Schema

```json
{
  "project": "{project_code}",
  "incidents": [
    {
      "id": "INC-001",
      "type": "recordable",
      "date": "2026-02-16",
      "time": "10:45",
      "location": "Mechanical room, north wall",
      "description": "Employee fall from 6-foot ladder while installing electrical fixture",
      "employee_id": "[redacted]",
      "craft": "carpenter",
      "injury_type": "laceration",
      "body_part": "head",
      "medical_treatment": "urgent_care",
      "facility": "{facility_name}",
      "severity": "moderate",
      "recordable": true,
      "days_away": 0,
      "restricted_duty_days": 2,
      "investigation_completed": true,
      "root_causes": ["Ladder not secured", "No second person", "No JSA completed"],
      "corrective_actions": ["JSA created for ladder work >4 ft", "Ladder stabilizers procured", "Safety training for supervisors"],
      "linked_daily_report": "2026-02-16",
      "linked_incident_investigation": "INC-001-INVESTIGATION",
      "photos": ["photo-1.jpg", "photo-2.jpg"],
      "date_logged": "2026-02-18"
    }
  ],
  "near_misses": [
    {
      "id": "NEAR-MISS-001",
      "date": "2026-02-16",
      "time": "14:30",
      "location": "Structural steel erection, Bay 3",
      "description": "Momentary loss of guy-wire tension during PEMB beam lift",
      "potential_severity": "critical",
      "craft_involved": ["ironworker", "crane_operator"],
      "root_causes": ["Guy-wire tension not verified by both parties"],
      "corrective_actions": ["Procedure updated: written sign-off required before lift"],
      "closed_date": "2026-02-18"
    }
  ],
  "first_aid_log": [
    {
      "id": "FIRST-AID-001",
      "date": "2026-02-15",
      "craft": "carpenter",
      "injury_type": "minor laceration",
      "body_part": "right hand",
      "description": "Cut on hand during formwork removal; cleaned and bandaged",
      "treatment": "First aid kit; bandage and antibiotic ointment",
      "provider": "On-site first aid staff",
      "linked_daily_report": "2026-02-15"
    }
  ],
  "toolbox_talks": [
    {
      "id": "TOOLBOX-001",
      "date": "2026-02-18",
      "topic": "PEMB Erection Safety",
      "duration_minutes": 15,
      "facilitator": "Safety Manager",
      "attendance_count": 12,
      "attendees": ["Ironworker-1", "Ironworker-2", "Crew-Foreman"],
      "key_points": ["100% fall protection", "Guy-wire verification", "Ground personnel safety"],
      "linked_daily_report": "2026-02-18"
    }
  ],
  "jsas": [
    {
      "id": "JSA-001",
      "title": "Concrete Footings Pour",
      "activity": "Placing concrete in footings C1-C6",
      "date_created": "2026-02-15",
      "last_reviewed": "2026-02-18",
      "status": "active",
      "hazards": 8,
      "controls_count": 8,
      "approvers": ["Superintendent", "Safety Manager"],
      "document_link": "jsa-001-concrete-pour.pdf"
    }
  ],
  "inspections": [
    {
      "id": "INS-001",
      "date": "2026-02-18",
      "type": "fall_protection",
      "location": "Structural steel erection area",
      "inspector": "Safety Manager",
      "findings": "Harnesses present and inspected; anchor points verified",
      "deficiencies": 0,
      "follow_up_date": "2026-02-25"
    }
  ],
  "metrics": {
    "year": 2026,
    "month": 2,
    "recordable_incidents": 1,
    "near_misses": 2,
    "first_aid_incidents": 1,
    "total_hours_worked": 2500,
    "trir": 80.0,
    "dart_rate": 16.0,
    "toolbox_talks_held": 8,
    "jsas_completed": 3,
    "safety_inspections": 5,
    "deficiencies_found": 4,
    "deficiencies_closed": 4,
    "closure_rate": "100%"
  }
}
```

---



## Integration with Daily Reports & Commands

### Auto-Capture in Daily Reports

Daily report `/morning-brief` includes safety section:
```
SAFETY ALERTS
- Incidents today? (y/n)
- Near-misses to report? (y/n)
- First aid treatments?
- Toolbox talk held? (topic)
- Safety concerns/observations?
```

If incident logged, auto-populates in `safety-log.json` and generates alert.

### Integration with Other Skills

**Inspection-Tracker**: Formal inspections logged separately; safety-management picks up deficiencies for tracking and closure

**Daily-Report**: Safety incidents captured; linked to safety-log

**Delay-Tracker**: If incident causes work stoppage, can be logged as safety delay

**Project-Dashboard**: Safety metrics displayed (TRIR, DART, leading indicators)

---



## Trigger Phrases

Use this skill when user says:
- "Record an incident" / "Log an injury"
- "Conduct a toolbox talk" / "Safety meeting"
- "Develop a JSA" / "Create a hazard analysis"
- "Safety inspection" / "Check fall protection"
- "OSHA recordkeeping" / "300 Log"
- "Safety metrics" / "TRIR calculation"
- "Near-miss report"
- "Confined space" / "Hot work permit"
- "Lockout/tagout"
- "Safety alert" / "Safety concern"
- "Incident investigation"
- "Site safety compliance"

---



## References

**OSHA Standards**:
- 29 CFR 1904 (OSHA Recordkeeping)
- 29 CFR 1926.500 (Fall Protection)
- 29 CFR 1926.550 (Cranes & Rigging)
- 29 CFR 1926.651 (Excavation)
- 29 CFR 1926.300 (Electrical)
- 29 CFR 1926.25 (Housekeeping)

**Industry Standards**:
- ACI 306 (Concrete in Cold Weather)
- ACI 305 (Concrete in Hot Weather)
- AISC Manual (Steel Detailing & Assembly)
- NFPA 51B (Hot Work)

**Project-Specific**:
- Project-specific Safety Plan (from project documents)
- Structural Steel Erection Procedure (per PEMB manufacturer)
- Geotechnical Report (frost-susceptible soils, fill removal requirements)

---

End of Safety Management Skill Documentation


