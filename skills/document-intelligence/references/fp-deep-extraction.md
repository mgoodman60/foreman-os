# Fire Protection Systems — Deep Extraction Guide

Extract detailed fire protection intelligence from FP drawings, riser diagrams, fire alarm plans, fire rated assembly schedules, and specification sections (Division 21). These documents define the life-safety systems protecting every occupancy in the building and are critical for code compliance verification, inspection coordination, and commissioning.

---

## Extraction Priority Matrix

| Priority | Data Type | Use Case | Completeness Target |
|----------|-----------|----------|---------------------|
| **CRITICAL** | System type (wet/dry/pre-action/deluge) | Code compliance, inspection scheduling, winterization | 100% per system |
| **CRITICAL** | Sprinkler head schedule (type, temp, K-factor) | Procurement, installation verification, inspection | 100% per head type |
| **CRITICAL** | Riser locations and sizes | Coordination, rough-in, inspection | 100% per riser |
| **CRITICAL** | Fire department connection (FDC) location and type | Fire department access, signage, inspection | 100% |
| **CRITICAL** | Fire alarm control panel (FACP) location and model | Commissioning, inspection, monitoring | 100% |
| **CRITICAL** | Fire rated assembly schedule (wall/floor ratings) | Penetration management, inspection, code compliance | 100% per rated assembly |
| **HIGH** | Sprinkler pipe sizes by run (mains, cross-mains, branches) | Coordination, rough-in, hydraulic verification | All main runs |
| **HIGH** | Floor control valve assembly (FCA) locations | Inspection, maintenance, shutdown coordination | 100% per floor |
| **HIGH** | Initiating device counts (smoke, heat, pull stations, flow/tamper) | Procurement, installation tracking, acceptance test | 100% per type per floor |
| **HIGH** | Notification appliance counts (horns, strobes, speakers) | Procurement, installation tracking, acceptance test | 100% per type per floor |
| **HIGH** | Hydraulic design area and density | Code compliance verification | 100% per system |
| **HIGH** | Firestopping details (UL system numbers) | Penetration tracking, inspection | 100% per penetration type |
| **MEDIUM** | Hanger spacing and types | Installation verification | Per spec requirement |
| **MEDIUM** | Fire damper and smoke damper locations | Coordination, inspection | 100% if shown |
| **MEDIUM** | Addressable device addressing/zone layout | Programming, commissioning | 100% if addressable |
| **MEDIUM** | Fire pump data (GPM, PSI, HP) | Commissioning, inspection | 100% if present |

---

## DOCUMENT IDENTIFICATION

### Signals That This Is a Fire Protection Document

**Drawing Sheet Prefixes**:
- **FP** prefix: FP-100, FP-101, FP-200, FP-201 (dedicated fire protection sheets)
- **P** prefix with sprinkler content: Some projects include fire protection under plumbing discipline
- **FA** prefix: Fire alarm plans (FA-100, FA-200)
- **LS** prefix: Life safety plans (may include fire protection layout)

**Content Signals** (any of these confirm fire protection):
- "NFPA 13", "NFPA 13R", "NFPA 13D", "NFPA 72"
- "sprinkler", "fire sprinkler", "automatic sprinkler system"
- "fire alarm", "fire alarm control panel", "FACP"
- "fire protection", "fire suppression"
- "fire rated", "fire resistance rating", "fire barrier"
- "FDC", "fire department connection"
- "riser diagram", "sprinkler riser", "standpipe riser"
- "fire damper", "smoke damper", "combination fire/smoke damper"
- "hydrostatic test", "main drain test", "flow test"
- "fire pump", "jockey pump"
- "OS&Y valve", "alarm check valve", "dry pipe valve"
- "inspector's test connection"
- "horn/strobe", "pull station", "duct detector", "flow switch", "tamper switch"

**Specification Section Signals**:
- Division 21 (Fire Suppression): 21 05 00, 21 10 00, 21 13 13, 21 13 16
- Division 28 (Electronic Safety and Security): 28 31 00 (Fire Detection and Alarm)
- Section 07 84 00 (Firestopping)
- Section 07 84 13 (Penetration Firestopping)

**Typical Sheet Organization**:
```
FP-001   Fire Protection General Notes, Symbols, Abbreviations
FP-100   Fire Protection First Floor Plan
FP-101   Fire Protection First Floor Enlarged Plans
FP-200   Fire Protection Second Floor Plan
FP-300   Fire Protection Riser Diagram
FP-301   Fire Protection Details
FP-400   Fire Alarm First Floor Plan
FP-401   Fire Alarm Second Floor Plan
FP-500   Fire Alarm Riser Diagram
FP-501   Fire Alarm Details and Schedules
```

---

## SPRINKLER SYSTEM EXTRACTION

### System Type Identification

Identify the system type for every sprinkler zone. A building may have multiple system types.

| System Type | Description | Where Used | Key Characteristics |
|-------------|-------------|------------|---------------------|
| **Wet** | Pipes charged with water at all times | Heated spaces (>40 deg F) | Fastest response, simplest maintenance |
| **Dry** | Pipes charged with air/nitrogen; water held at valve | Unheated spaces (parking, loading docks, attics) | 60-second max water delivery time |
| **Pre-Action (Single Interlock)** | Dry until detection triggers valve | Data centers, museums, archives | Requires both detection and head activation |
| **Pre-Action (Double Interlock)** | Dry until BOTH detection AND head activate | High-value areas needing extra protection | Two independent triggers required |
| **Deluge** | Open heads; entire system discharges on activation | High-hazard (flammable liquid, aircraft hangars) | All heads open simultaneously |

**EXTRACT**:
```
System 1: Wet pipe sprinkler system
  Served areas: First floor, second floor (heated spaces)
  Design standard: NFPA 13
  Hazard classification: Ordinary Hazard Group 1
  Riser: R-1, located in Mechanical Room 105

System 2: Dry pipe sprinkler system
  Served areas: Unheated loading dock, attic space
  Design standard: NFPA 13
  Hazard classification: Ordinary Hazard Group 1
  Riser: R-2, located in Mechanical Room 105
  Air compressor: Required (maintain 20 PSI minimum air pressure)
```

### Sprinkler Head Schedule

**EXTRACT EVERY HEAD TYPE** from the sprinkler head schedule or general notes.

Per head type:
- **Type**: Pendant, upright, sidewall, concealed, ESFR (Early Suppression Fast Response), residential, dry pendant, dry sidewall
- **Temperature Rating**: Ordinary (135 deg F / 57 deg C), Intermediate (175 deg F / 79 deg C), High (286 deg F / 141 deg C), Extra High (360 deg F / 182 deg C)
- **K-Factor**: K5.6 (standard), K8.0 (large orifice), K11.2, K14.0, K16.8, K25.2 (ESFR)
- **Coverage Area**: Standard 130 SF max per head (15 ft max spacing), extended coverage per listing, residential per NFPA 13R
- **Response Type**: Standard response, quick response (QR), extended coverage (EC)
- **Finish**: Chrome, white, brass, custom RAL
- **Manufacturer/Model**: From submittal if available
- **Quantity**: Total count per type, count per floor

**EXAMPLE HEAD SCHEDULE EXTRACT**:
```
Sprinkler Head Schedule:

Type A — Standard Spray Pendant (SSP)
  Response: Quick Response
  Temp rating: 155 deg F (68 deg C) — Ordinary (white bulb)
  K-factor: K5.6
  Coverage: 130 SF max (15' x 15' max spacing per NFPA 13)
  Thread: 1/2" NPT
  Finish: White polyester
  Use: Standard heated spaces, offices, corridors
  Qty: 342 heads (Floor 1: 178, Floor 2: 164)

Type B — Standard Spray Upright (SSU)
  Response: Standard Response
  Temp rating: 155 deg F — Ordinary
  K-factor: K5.6
  Coverage: 130 SF max
  Thread: 1/2" NPT
  Finish: Brass
  Use: Mechanical rooms, storage, exposed ceiling areas
  Qty: 28 heads

Type C — Concealed Pendant
  Response: Quick Response
  Temp rating: 155 deg F — Ordinary
  K-factor: K5.6
  Coverage: 130 SF max (per listing, check manufacturer data)
  Thread: 1/2" NPT
  Finish: White cover plate (RAL 9003)
  Activation: Cover plate drops at 135 deg F, head activates at 155 deg F
  Use: Lobbies, conference rooms, finished ceilings
  Qty: 45 heads

Type D — Dry Pendant
  Response: Standard Response
  Temp rating: 155 deg F — Ordinary
  K-factor: K5.6
  Drop length: Per field measurement (specify at order)
  Thread: 1" NPT inlet
  Finish: Chrome
  Use: Unheated loading dock (dry system)
  Qty: 18 heads

Type E — Sidewall
  Response: Quick Response
  Temp rating: 175 deg F — Intermediate (green bulb)
  K-factor: K5.6
  Coverage: Per listing (typically 12' x 12' to 16' x 20')
  Thread: 1/2" NPT
  Finish: White
  Use: Near heat sources, kitchens, areas requiring intermediate temp
  Qty: 12 heads
```

**TEMPERATURE RATING COLOR CODE** (glass bulb):
| Color | Temperature | Classification |
|-------|-------------|---------------|
| Orange | 135 deg F (57 deg C) | Ordinary |
| Red | 155 deg F (68 deg C) | Ordinary |
| Yellow | 175 deg F (79 deg C) | Intermediate |
| Green | 200 deg F (93 deg C) | Intermediate |
| Blue | 286 deg F (141 deg C) | High |
| Purple | 360 deg F (182 deg C) | Extra High |
| Black | 440-500 deg F (227-260 deg C) | Very Extra High |

### Pipe Sizing and Material

Extract pipe sizes for all runs visible on plans and riser diagrams.

- **Mains** (horizontal trunk lines from riser): Typically 4" to 8"
- **Cross-mains** (secondary horizontal distribution): Typically 2-1/2" to 4"
- **Branch lines** (feed individual heads): Typically 1" to 1-1/2"
- **Risers** (vertical supply): Typically 4" to 6"
- **Drops/sprigs** (short vertical to head): 1/2" to 1"

**Pipe Material**:
| Material | Use Case | Joining |
|----------|----------|---------|
| Black steel (Schedule 10/40) | Standard above-ground wet/dry | Grooved (Victaulic), threaded, welded |
| CPVC (BlazeMaster) | Light hazard, residential, concealed spaces | Solvent cement (one-step) |
| Thin-wall steel (Schedule 5/7) | Grooved systems, cost savings | Grooved couplings only |
| Copper (Type L/M) | Exposed finished areas (per code) | Brazed or soldered |
| Ductile iron | Underground, yard mains | Mechanical joint, restrained joint |

**EXAMPLE PIPE EXTRACT**:
```
Riser R-1 (Wet System):
  Riser pipe: 6" Schedule 40 black steel, grooved
  Underground to riser: 6" ductile iron, mechanical joint
  Main (horizontal trunk): 4" Schedule 10 black steel, grooved
  Cross-mains: 2-1/2" Schedule 10, grooved
  Branch lines: 1-1/4" Schedule 10, threaded
  Drops to heads: 1" x close nipple, threaded
  Arm-overs: 1" Schedule 40, threaded
```

### Hanger Spacing and Types

Extract from general notes or details:
- **Main and cross-main hangers**: Max 12 ft spacing (NFPA 13)
- **Branch line hangers**: Max 12 ft (8 ft with CPVC)
- **Hanger types**: Ring, clevis, trapeze, seismic bracing
- **Seismic bracing**: Lateral and longitudinal braces per NFPA 13 Chapter 18

---

## RISER AND VALVE EXTRACTION

### Riser Diagram Data

**EXTRACT FROM RISER DIAGRAM** (typically FP-300 series):

Per riser:
- **Riser designation**: R-1, R-2, etc.
- **Location**: Grid reference, room number
- **Riser pipe size**: Diameter
- **System type**: Wet/dry/pre-action/deluge
- **Floors served**: Which levels
- **Supply source**: Underground main size and connection point

### Floor Control Valve Assembly (FCA)

Per floor (required on each floor in multi-story buildings):
- **Location**: Grid reference, room/closet
- **Components**: OS&Y gate valve (or butterfly), flow switch, drain, pressure gauge, test connection
- **Size**: Matches riser or branch takeoff size
- **Floor served**: Identify which floor each FCA controls

**EXAMPLE FCA EXTRACT**:
```
Floor Control Valve Assemblies:

FCA-1 (First Floor)
  Location: Stairwell B, Grid D/4
  Size: 4"
  Components: 4" OS&Y gate valve, 4" flow switch, 2" drain with sight glass, pressure gauge
  System: Wet (R-1)

FCA-2 (Second Floor)
  Location: Stairwell B, Grid D/4
  Size: 4"
  Components: Same as FCA-1
  System: Wet (R-1)
```

### Key Valve Locations

Extract all valve locations with grid references:
- **OS&Y (Outside Screw and Yoke) gate valves**: Main shutoff, sectional, floor control
- **Alarm check valve**: Base of wet riser (signals water flow)
- **Dry pipe valve**: Base of dry riser (holds air, releases water on drop)
- **Pre-action valve**: Controlled by detection system
- **Check valves**: Backflow prevention at FDC, meter connections
- **Inspector's test connection**: Remote end of each system (simulates head flow)

---

## FIRE DEPARTMENT CONNECTION (FDC)

### FDC Data Points

- **Location**: Grid reference, building face (north, south, etc.), distance from building entrance
- **Access**: Within 100 ft of fire hydrant, clear access path for fire apparatus
- **Type**: Siamese (two 2-1/2" inlets) or Storz (single 5" quick-connect)
- **Size**: Typically 4" to 6" supply pipe behind FDC
- **System(s) served**: Which sprinkler/standpipe system(s)
- **Signage**: Required signage per NFPA (system type, coverage area)
- **Clapper/check valve**: Internal check valve to prevent backflow
- **Finish**: Chrome, brass, painted (specify color)
- **Mounting**: Wall-mounted, freestanding post, recessed

**EXAMPLE FDC EXTRACT**:
```
Fire Department Connection:
  Type: Storz (5" quick-connect)
  Location: South face of building, Grid B/1, 8 ft from main entrance
  Mounting: Wall-mounted, 36" AFF to center
  System served: Sprinkler system (wet + dry)
  Pipe to riser: 6" Schedule 40 black steel
  Check valve: Inline check valve to prevent backflow
  Signage: "AUTO SPKR" brass plate
  Nearest hydrant: 65 ft south (public hydrant on Main Street)
```

---

## FIRE RATED ASSEMBLY SCHEDULES

### Wall Rating Schedule

Extract from architectural life safety plans (often A-series or LS-series sheets):

Per rated wall type:
- **Designation**: W-1, W-2, etc. (or UL design number)
- **Rating**: 1-hour, 2-hour, 3-hour, 4-hour
- **Construction**: Gypsum board layers, stud type/gauge/spacing, insulation
- **UL Design Number**: e.g., UL U305, UL U411, UL W412
- **Use**: Corridor, demising, occupancy separation, shaft, stairwell

**EXAMPLE WALL SCHEDULE EXTRACT**:
```
Fire Rated Wall Schedule:

Type W-1 — 1-Hour Fire Barrier
  UL Design: U305
  Construction: (1) layer 5/8" Type X each side on 3-5/8" 20 ga studs @ 16" o.c.
  Use: Corridor walls, tenant separation
  STC rating: 45

Type W-2 — 2-Hour Fire Barrier
  UL Design: U411
  Construction: (2) layers 5/8" Type X each side on 3-5/8" 20 ga studs @ 16" o.c.
  Use: Occupancy separation, exit enclosure
  STC rating: 54

Type W-3 — 2-Hour Shaft Wall
  UL Design: U418
  Construction: 1" shaft liner + (1) layer 5/8" Type X on 2-1/2" C-H studs @ 24" o.c.
  Use: Elevator shafts, mechanical shafts, stairwell shafts
```

### Floor/Ceiling Assembly Schedule

Per assembly:
- **Designation**: FC-1, FC-2, etc.
- **Rating**: 1-hour, 2-hour, 3-hour
- **UL Design Number**: e.g., UL D501, UL G512
- **Construction**: Deck type, insulation, ceiling board layers, grid system

### Penetration Firestopping

Extract firestopping details for all penetrations through rated assemblies:
- **UL System Number**: e.g., UL W-L-7079, CJ-1234
- **Penetration type**: Pipe (metallic/plastic), conduit, cable tray, HVAC duct, mixed
- **Through-penetration or membrane penetration**
- **Sealant/device**: Intumescent caulk, mineral wool, firestop pillows, collar, wrap strip
- **Annular space**: Maximum gap allowed around penetrant
- **Manufacturer**: Hilti, 3M, STI, Specified Technologies

**EXAMPLE FIRESTOPPING EXTRACT**:
```
Firestopping Schedule:

FS-1 — Metallic Pipe through Gypsum Wall (W-1, 1-hr)
  UL System: W-L-7079
  Penetrant: Steel pipe up to 4" diameter
  Fill: Hilti CFS-S SIL silicone sealant, min 5/8" depth
  Packing: Mineral wool backing, min 3" depth
  Annular space: Max 2" around pipe

FS-2 — Plastic Pipe (CPVC) through Gypsum Wall (W-2, 2-hr)
  UL System: W-L-8137
  Penetrant: CPVC pipe up to 3" diameter
  Device: Hilti CP 653 firestop collar
  Installation: Both sides of wall
  Note: CPVC melts and collar closes opening
```

### Fire Damper and Smoke Damper Locations

Extract from FP plans and HVAC coordination drawings:
- **Fire dampers**: Required where ducts penetrate fire-rated walls/floors
  - Rating: 1-1/2 hr (1-hr wall) or 3 hr (2-hr wall)
  - Type: Curtain type (gravity close), spring type
  - Fusible link temperature: 165 deg F standard
- **Smoke dampers**: Required where ducts penetrate smoke barriers
  - Actuator: Electric (fail-safe close on loss of power)
  - Control: Tied to fire alarm system or smoke detector
- **Combination fire/smoke dampers**: Both functions in one unit
  - Fusible link + electric actuator

---

## FIRE ALARM SYSTEM

### Fire Alarm Control Panel (FACP)

- **Location**: Grid reference, room number (typically at main entrance or security office)
- **Manufacturer/Model**: Notifier, Simplex, Edwards, Honeywell, Fire-Lite, Silent Knight
- **Type**: Addressable or conventional
- **Capacity**: Number of loops/zones, maximum devices per loop
- **Monitoring**: Central station connection type (IP, cellular, POTS)
- **Annunciation**: Remote annunciator location(s) if any
- **Power**: Primary (120V), secondary (batteries — 24hr standby + 5 min alarm)
- **DACT**: Digital Alarm Communicator Transmitter (for monitoring)
- **Software version**: If noted on plans

### Initiating Devices

Extract device counts by type and floor:

| Device Type | Abbreviation | Function | Location Pattern |
|-------------|--------------|----------|------------------|
| Smoke detector | SD | Detect smoke (photoelectric/ionization) | Corridors, rooms, plenums |
| Heat detector | HD | Detect temperature rise (fixed temp/rate-of-rise) | Kitchens, garages, dusty areas |
| Duct smoke detector | DSD | Detect smoke in HVAC ducts | At AHU return, supply over 2000 CFM |
| Manual pull station | MPS | Manual alarm activation | At each exit, 5 ft travel max |
| Waterflow switch | WFS | Detect water flow in sprinkler pipe | At each riser and FCA |
| Tamper switch | TS | Detect valve closure | At each OS&Y, FCA, PIV |
| Beam detector | BD | Detect smoke across large open space | High-ceiling areas (warehouses, atriums) |

**EXAMPLE DEVICE COUNT EXTRACT**:
```
Initiating Device Summary:

                        Floor 1   Floor 2   Total
Smoke Detectors (SD)       42        38       80
Heat Detectors (HD)         6         4       10
Duct Detectors (DSD)        4         3        7
Pull Stations (MPS)         8         6       14
Flow Switches (WFS)         2         2        4
Tamper Switches (TS)        4         4        8
                        ─────     ─────    ─────
Total Initiating:          66        57      123
```

### Notification Appliances

Extract counts by type and floor:

| Device Type | Abbreviation | Function | Mounting |
|-------------|--------------|----------|----------|
| Horn/strobe | H/S | Audible + visible alarm | Wall (typically 80" AFF) |
| Strobe only | S | Visible alarm (ADA) | Wall/ceiling |
| Horn only | H | Audible alarm | Wall/ceiling |
| Speaker/strobe | SP/S | Voice evacuation + visible | Wall (voice alarm systems) |
| Speaker only | SP | Voice evacuation | Wall/ceiling |
| Chime/strobe | CH/S | Coded signal + visible | Healthcare (code blue, etc.) |

**EXAMPLE NOTIFICATION COUNT EXTRACT**:
```
Notification Appliance Summary:

                        Floor 1   Floor 2   Total
Horn/Strobes (H/S)        24        20       44
Strobes only (S)           8         6       14
Speaker/Strobes (SP/S)     0         0        0
                        ─────     ─────    ─────
Total Notification:        32        26       58
```

### Addressable vs. Conventional

- **Addressable**: Each device has unique address; FACP identifies exact device in alarm. Modern standard. Extract loop assignments and device addressing scheme.
- **Conventional**: Devices grouped into zones; FACP identifies zone only. Older systems. Extract zone map.

---

## NFPA 13 SPACING COMPLIANCE CHECKS

### Standard Spray Sprinkler Spacing Rules

Use these rules to verify sprinkler layout compliance on plans:

**Light Hazard Occupancies** (offices, churches, educational, residential):
- Maximum spacing: 15 ft between heads
- Maximum coverage: 200 SF per head (225 SF for QR)
- Maximum distance from wall: 7.5 ft (half the head-to-head spacing)
- Minimum distance from wall: 4 inches

**Ordinary Hazard Occupancies** (restaurants, retail, parking garages, manufacturing):
- Maximum spacing: 15 ft between heads
- Maximum coverage: 130 SF per head
- Maximum distance from wall: 7.5 ft
- Minimum distance from wall: 4 inches

**Extra Hazard Occupancies** (flammable liquid storage, woodworking, plastics):
- Maximum spacing: 12 ft between heads
- Maximum coverage: 90-100 SF per head
- Maximum distance from wall: 6 ft
- Minimum distance from wall: 4 inches

### Extended Coverage Heads

- Spacing and coverage per manufacturer listing (UL/FM)
- Must verify listed spacing matches installation on plans
- Typical extended coverage: up to 20 ft x 20 ft (400 SF) for light hazard

### Obstruction Rules (NFPA 13 Section 8.6)

**Three Times Rule**: Sprinkler deflector must be a minimum of 3 times the maximum dimension of the obstruction away from the obstruction, measured horizontally.

- Continuous obstructions (beams, soffits, ducts): Add heads below if obstruction is > 4 ft wide
- Isolated obstructions (columns, lights): 3x rule applies
- Pendant clearance below smooth ceiling: 1" to 12" (typical, per listing)
- Upright clearance above deflector: Minimum 18" to ceiling/roof deck (to prevent skipping)

### Storage Area Requirements (NFPA 13 Chapters 12-20)

If the building has storage areas, extract commodity classification and storage arrangement:
- **Commodity Class I**: Non-combustible products on pallets (metal parts, glass)
- **Commodity Class II**: Class I in combustible packaging (cardboard boxes)
- **Commodity Class III**: Wood, paper, natural fiber products
- **Commodity Class IV**: Class I-III with plastic (expanded polystyrene, group A plastics)
- **Storage height**: Maximum storage height vs. ceiling height
- **Arrangement**: Rack storage, palletized, solid pile, bin box
- **Required density**: Higher density or ESFR heads for higher commodity classes

---

## TESTING AND INSPECTION HOLD POINTS

### Required Tests — Fire Protection

| Test | Standard | Requirements | Hold Point |
|------|----------|-------------|------------|
| **Hydrostatic test** | NFPA 13 Section 29.2 | 200 PSI for 2 hours (or 50 PSI above static, whichever is greater); no leaks | Inspector witness required |
| **Underground flush test** | NFPA 13 Section 29.1 | Flush underground mains before connecting to riser; document flow rate and color | Contractor to document |
| **Main drain test** | NFPA 13 Section 29.2.6 | Full flow from main drain; record static and residual pressure | Inspector witness |
| **Alarm verification test** | NFPA 72 | Trip alarm check valve waterflow switch; verify alarm signal at FACP and monitoring station | Inspector + central station |
| **Trip test (dry systems)** | NFPA 13 Section 29.2.5 | Open inspector's test; time from trip to water delivery at inspector's test (max 60 seconds) | Inspector witness required |
| **Final acceptance test** | NFPA 13 Section 29 | Complete system walkthrough: head placement, signage, clearances, accessibility, spare heads | AHJ final inspection |

### Fire Alarm Acceptance Testing

| Test | Standard | Requirements | Hold Point |
|------|----------|-------------|------------|
| **Individual device test** | NFPA 72 Section 14.4 | Every initiating and notification device tested individually | Inspector witness |
| **Alarm signal verification** | NFPA 72 Section 14.4 | Verify alarm signals received at FACP and central monitoring station | Inspector + monitoring company |
| **Supervisory signal test** | NFPA 72 Section 14.4 | Close each tamper switch; verify supervisory signal at FACP | Inspector witness |
| **Audibility test** | NFPA 72 Section 18.4 | Sound level readings in all occupied spaces (min 15 dBA above ambient or 75 dBA) | Inspector witness |
| **Visual coverage test** | NFPA 72 Section 18.5 | Verify strobe visible from all required locations, candela per room size | Inspector witness |
| **Battery calculation test** | NFPA 72 Section 10.6.7 | Verify 24-hour standby + 5-minute alarm (or 15 min for voice) | Documentation review |
| **Emergency voice test** | NFPA 72 | Intelligibility test per NFPA 72 (STI measurement) | Inspector witness if voice system |

### Inspector Coordination Points

- **Rough-in inspection**: Before concealing pipes behind walls/ceilings — verify pipe sizes, hanger spacing, head locations
- **Underground inspection**: Before backfilling — verify pipe, bedding, thrust blocks
- **Hydrostatic test**: Must be witnessed by AHJ inspector
- **Firestopping inspection**: Before concealing — verify UL system match, material, installation
- **Above-ceiling inspection**: Before installing ceiling tiles — verify head clearances, branch line routing
- **Final inspection**: Complete system walkthrough by AHJ before certificate of occupancy
- **Fire alarm acceptance test**: All devices tested with AHJ inspector present
- **Fire pump test**: Flow test witnessed by AHJ (if fire pump is present)

---

## OUTPUT MAPPING

### For quality-data.json (FP inspections and test results)

```json
{
  "fire_protection_inspections": [
    {
      "inspection_type": "hydrostatic_test",
      "system": "wet_sprinkler_R1",
      "date": "2026-03-15",
      "test_pressure_psi": 200,
      "duration_hours": 2,
      "result": "pass",
      "inspector": "J. Martinez, AHJ",
      "notes": "No leaks observed. System held 200 PSI for 2 hours.",
      "spec_reference": "NFPA 13 Section 29.2"
    },
    {
      "inspection_type": "fire_alarm_acceptance",
      "date": "2026-04-01",
      "devices_tested": 181,
      "devices_passed": 181,
      "devices_failed": 0,
      "result": "pass",
      "inspector": "J. Martinez, AHJ",
      "monitoring_verified": true,
      "spec_reference": "NFPA 72 Section 14.4"
    }
  ],
  "fire_protection_deficiencies": [
    {
      "deficiency_id": "FP-001",
      "description": "Head spacing exceeds 15 ft at Grid C-3 corridor",
      "location": "First Floor, Grid C/3",
      "severity": "code_violation",
      "status": "open",
      "corrective_action": "Add one pendant head between C-2 and C-4",
      "date_identified": "2026-03-10"
    }
  ]
}
```

### For plans-spatial.json (FP system layout)

```json
{
  "fire_protection": {
    "source_sheets": ["FP-100", "FP-200", "FP-300", "FP-400", "FP-500"],
    "systems": [
      {
        "system_id": "wet_R1",
        "type": "wet",
        "design_standard": "NFPA 13",
        "hazard_class": "Ordinary Hazard Group 1",
        "riser": {
          "designation": "R-1",
          "location_grid": "D/4",
          "location_room": "Mechanical Room 105",
          "size": "6 inch"
        },
        "floors_served": ["1", "2"],
        "fdc": {
          "type": "Storz",
          "location": "South face, Grid B/1",
          "systems_served": ["wet_R1", "dry_R2"]
        },
        "hydraulic_design": {
          "area_sf": 1500,
          "density_gpm_sf": 0.15,
          "demand_gpm": 225,
          "hose_allowance_gpm": 250,
          "total_demand_gpm": 475
        }
      }
    ],
    "sprinkler_heads": [
      {
        "type_code": "A",
        "description": "Standard Spray Pendant QR",
        "temp_rating_f": 155,
        "k_factor": 5.6,
        "coverage_sf": 130,
        "finish": "White",
        "quantity": 342,
        "by_floor": {"1": 178, "2": 164}
      }
    ],
    "fire_alarm": {
      "facp_location_grid": "A/1",
      "facp_location_room": "Lobby 100",
      "facp_manufacturer": "Notifier",
      "facp_model": "NFS2-3030",
      "system_type": "addressable",
      "initiating_devices": {
        "smoke_detectors": 80,
        "heat_detectors": 10,
        "duct_detectors": 7,
        "pull_stations": 14,
        "flow_switches": 4,
        "tamper_switches": 8
      },
      "notification_appliances": {
        "horn_strobes": 44,
        "strobes": 14,
        "speakers": 0
      },
      "total_devices": 181
    },
    "fire_rated_assemblies": [
      {
        "designation": "W-1",
        "rating_hours": 1,
        "ul_design": "U305",
        "type": "wall",
        "construction": "(1) layer 5/8 Type X each side, 3-5/8 20ga studs at 16 o.c."
      }
    ],
    "firestopping": [
      {
        "designation": "FS-1",
        "ul_system": "W-L-7079",
        "penetrant": "Steel pipe up to 4 inch",
        "through_assembly": "W-1",
        "sealant": "Hilti CFS-S SIL",
        "manufacturer": "Hilti"
      }
    ]
  }
}
```

### For specs-quality.json (FP hold points and thresholds)

```json
{
  "fire_protection_specs": {
    "spec_sections": ["21 13 13", "21 13 16", "28 31 00", "07 84 00"],
    "hold_points": [
      {
        "test": "Hydrostatic test",
        "threshold": "200 PSI for 2 hours",
        "witness_required": true,
        "reference": "NFPA 13 Section 29.2"
      },
      {
        "test": "Dry system trip test",
        "threshold": "Water at inspector's test within 60 seconds",
        "witness_required": true,
        "reference": "NFPA 13 Section 29.2.5"
      },
      {
        "test": "Fire alarm device test",
        "threshold": "100% of devices individually tested",
        "witness_required": true,
        "reference": "NFPA 72 Section 14.4"
      },
      {
        "test": "Audibility test",
        "threshold": "15 dBA above ambient or 75 dBA minimum",
        "witness_required": true,
        "reference": "NFPA 72 Section 18.4"
      },
      {
        "test": "Rough-in inspection",
        "threshold": "Before concealing — pipe sizes, hangers, head locations verified",
        "witness_required": true,
        "reference": "NFPA 13"
      },
      {
        "test": "Firestopping inspection",
        "threshold": "UL system match, correct materials, proper installation",
        "witness_required": true,
        "reference": "IBC 714, ASTM E814"
      }
    ],
    "spacing_requirements": {
      "light_hazard_max_spacing_ft": 15,
      "light_hazard_max_coverage_sf": 200,
      "ordinary_hazard_max_spacing_ft": 15,
      "ordinary_hazard_max_coverage_sf": 130,
      "extra_hazard_max_spacing_ft": 12,
      "extra_hazard_max_coverage_sf": 100,
      "max_distance_from_wall_ft": 7.5,
      "min_distance_from_wall_in": 4
    }
  }
}
```

---

## CROSS-REFERENCE RULES

| FP Data | Cross-Reference Against | Validation |
|---------|------------------------|------------|
| Sprinkler head count per room | Room areas in plans-spatial.json | Verify coverage (area / heads <= max coverage per head) |
| Riser locations (grid ref) | Grid system in plans-spatial.json | Grid reference must exist |
| FDC location | Site plan / civil drawings | Verify hydrant within 100 ft and clear apparatus access |
| Fire rated wall designations | Architectural life safety plans | Wall types must match between arch and FP sheets |
| Firestopping UL systems | Rated assembly penetrations | Every penetration through rated assembly needs firestop |
| Fire alarm device locations | Reflected ceiling plans | Devices must not conflict with HVAC, lighting |
| Flow switch / tamper switch count | Valve and FCA count | Every OS&Y and FCA should have tamper switch; every FCA should have flow switch |
| Equipment electrical (fire pump MCA/MOCP) | Panel schedules in electrical | Fire pump circuit must be on dedicated panel/feeder |
| Sprinkler pipe routing | Structural framing / MEP coordination | Verify clearances, no conflicts with steel, duct, conduit |
| Fire damper locations | HVAC duct routing through rated walls | Every duct penetration through rated wall needs fire damper |
| Notification appliance candela | Room dimensions in plans-spatial.json | Candela must match room size per NFPA 72 Table 18.5.5.4.1(a) |
| Hydraulic design demand (GPM) | Water supply flow test data | Available supply must exceed system demand at required pressure |

---

## SUMMARY CHECKLIST — FIRE PROTECTION DOCUMENT REVIEW

### On Receipt of FP Drawings

- [ ] **System identification**: All sprinkler system types identified (wet, dry, pre-action, deluge)
- [ ] **Hazard classification**: Occupancy hazard per NFPA 13 documented for each area
- [ ] **Head schedule**: Every head type extracted (type, temp, K-factor, coverage, finish, quantity)
- [ ] **Head count by floor**: Total heads per floor tallied and cross-checked against coverage areas
- [ ] **Pipe sizing**: Main, cross-main, branch, and riser sizes extracted from riser diagram
- [ ] **Pipe material**: Material and joining method identified for each pipe type
- [ ] **Riser diagram**: All risers located with grid references, sizes, system types
- [ ] **FCA locations**: Floor control valve assembly location per floor documented
- [ ] **Valve schedule**: All OS&Y, alarm check, dry pipe, and control valves located
- [ ] **FDC**: Location, type (Siamese/Storz), systems served, signage, nearest hydrant distance
- [ ] **Fire rated assemblies**: All rated walls and floor/ceiling assemblies with UL design numbers
- [ ] **Firestopping**: UL systems for each penetration type through rated assemblies
- [ ] **Fire damper / smoke damper locations**: Extracted where ducts penetrate rated assemblies
- [ ] **Hydraulic design**: Design area (SF), density (GPM/SF), total demand (GPM) documented

### On Receipt of Fire Alarm Plans

- [ ] **FACP**: Location, manufacturer, model, type (addressable/conventional), capacity
- [ ] **Initiating devices**: Count by type per floor (smoke, heat, duct, pull station, flow, tamper)
- [ ] **Notification appliances**: Count by type per floor (horn/strobe, strobe, speaker)
- [ ] **Addressable layout**: Loop assignments and addressing scheme (if addressable)
- [ ] **Zone map**: Zone boundaries (if conventional)
- [ ] **Monitoring**: Central station connection type and provider
- [ ] **Power**: Primary and secondary (battery) power confirmed

### On Receipt of Fire Protection Specifications

- [ ] **Spec sections**: Division 21 and 28 section numbers identified
- [ ] **Design standard**: NFPA 13/13R/13D edition year confirmed
- [ ] **Approved manufacturers**: Listed by component (heads, pipe, valves, FACP)
- [ ] **Testing requirements**: All required tests with acceptance criteria extracted
- [ ] **Inspection requirements**: All hold points and witness requirements documented
- [ ] **Spare head cabinet**: Minimum spare head quantities per NFPA 13 (6-24 heads depending on total)
- [ ] **Hydraulic calculation submittal**: Required from contractor before installation

---

## NOTES

- Fire protection is a life-safety system. Extraction accuracy directly affects code compliance and occupant safety.
- NFPA 13 edition year matters — verify which edition is referenced on the drawings (2013, 2016, 2019, 2022). Spacing rules and requirements change between editions.
- Sprinkler head temperature rating must match the environment. Heads near heat sources (kitchens, mechanical rooms, skylights) may need intermediate or high temperature ratings — verify against general notes.
- The AHJ (Authority Having Jurisdiction) — typically the local fire marshal — has final authority on acceptance. Their interpretations may be stricter than NFPA minimum.
- Fire alarm device counts are critical for procurement and progress tracking. Accurate floor-by-floor counts enable installation tracking in daily reports.
- Firestopping is one of the most common inspection failures. Extract UL system numbers early and track every penetration.
- Dry systems require an air compressor and have a 60-second maximum water delivery time — this is a testable and inspectable requirement.
- Fire pump systems (if present) add significant complexity — extract pump curve data, controller information, and test requirements.
- Combination fire/smoke dampers require both a fusible link and an electric actuator tied to the fire alarm — verify both are specified.
