# MEP Systems — Deep Extraction Guide

Comprehensive extraction reference for Mechanical, Electrical, and Plumbing (MEP) systems from construction documents. This guide covers all three MEP disciplines plus fire protection and specialty systems. MEP extraction feeds equipment schedules, coordination data, and commissioning records into the project data store for daily reporting, procurement tracking, and closeout.

---

## Extraction Priority Matrix

| Priority | Data Type | Use Case | Target |
|----------|-----------|----------|--------|
| **CRITICAL** | Equipment schedules (HVAC, plumbing, electrical) | Startup, commissioning, daily reporting | 100% |
| **CRITICAL** | Panel schedules | Circuit assignments, load tracking | 100% |
| **CRITICAL** | Equipment tags on plans | Location tracking | 100% |
| **HIGH** | Duct sizes and routing | Coordination, rough-in | All main trunks |
| **HIGH** | Pipe sizes and materials | Coordination, rough-in | All main runs |
| **HIGH** | Lighting fixture schedule | Procurement, install tracking | 100% |
| **HIGH** | Plumbing fixture schedule | Procurement, ADA | 100% |
| **HIGH** | Fire protection system data | Code compliance | System type + riser |
| **HIGH** | Single-line diagram | Power distribution | Full hierarchy |
| **MEDIUM** | Diffuser/grille schedules | Balancing, commissioning | All scheduled |
| **MEDIUM** | Controls/BAS points | Commissioning | All DDC points |
| **MEDIUM** | Receptacle counts by room | Progress tracking | All rooms |
| **MEDIUM** | MEP coordination conflicts | Clash resolution | All flagged |
| **MEDIUM** | Roof/floor penetration schedule | Waterproofing, fire-stop | All penetrations |

---

## DOCUMENT IDENTIFICATION

MEP drawings follow standard sheet-number conventions. Identify and catalog every sheet before extraction begins.

| Prefix | Discipline | Typical Range | Content |
|--------|-----------|---------------|---------|
| **M** | Mechanical | M-001 to M-999 | HVAC plans, schedules, details |
| **P** | Plumbing | P-001 to P-999 | Plumbing plans, risers, schedules |
| **E** | Electrical | E-001 to E-999 | Power, lighting, panels, single-line |
| **FP** | Fire Protection | FP-001 to FP-999 | Sprinkler plans, risers, details |

**Common Sheet Organization**:
- **x-001 to x-099**: Legends, abbreviations, general notes, symbols
- **x-100 to x-199**: Floor plans (power plans for E, piping plans for P)
- **x-200 to x-299**: Floor plans continued (lighting for E, fixture plans for P)
- **x-300 to x-399**: Schedules (equipment, panels, fixtures)
- **x-400 to x-499**: Details, sections, enlarged plans
- **x-500 to x-599**: Risers, single-line diagrams, control diagrams

---

## MECHANICAL EXTRACTION

### HVAC Equipment Schedule — Detailed Specification Extraction

**EXTRACT EVERY UNIT** from mechanical schedules (M-300 series). For each equipment item, capture the full specification record:

#### Rooftop Units (RTUs)

Per unit extract:
- **Tag**: RTU-1, RTU-2, etc.
- **Manufacturer/model**: From schedule or submittal (e.g., "Carrier 48TC, Trane Voyager")
- **Capacity**: Cooling tons, heating MBH, airflow CFM
- **Static pressure**: External static pressure (in. w.c.) — critical for duct design
- **Heating type**: Gas-fired (input/output MBH, AFUE), electric (kW), heat pump (COP, HSPF)
- **Economizer**: Yes/No, type (barometric/motorized/enthalpy), minimum OA CFM
- **VFD**: Yes/No, if yes note motor HP and VFD manufacturer
- **Refrigerant**: R-410A, R-32, R-454B (affects service equipment needed)
- **Electrical**: Voltage/phase/Hz, FLA, MCA, MOCP, LRA
- **Physical**: L x W x H (inches), operating weight (lbs), curb size
- **Clearances**: Front service (36" typical), rear (24"), sides (varies), top (open)
- **Connection sizes**: Supply duct (W x H or diameter), return duct, condensate drain, gas pipe
- **Controls**: DDC/standalone, BACnet/Modbus/0-10V, thermostat type
- **Sound**: NC rating at 5 ft, dBA at distance
- **Efficiency**: SEER2, EER2, IEER, AFUE (heating)
- **Served areas**: Room numbers, zone name

**EXAMPLE RTU EXTRACT**:
```
RTU-1: Carrier 48TC-D16
  Cooling: 15 tons DX, EER 11.0, IEER 14.2
  Heating: 300 MBH gas input, 240 MBH output, AFUE 80%
  Airflow: 5,400 CFM @ 1.5" w.c. external static
  Economizer: Motorized, enthalpy control, 1,200 CFM min OA
  VFD: Yes, 7.5 HP supply fan
  Refrigerant: R-410A, 2 circuits
  Electrical: 460V/3ph/60Hz, FLA 28.5, MCA 35.6, MOCP 45A
  Physical: 100" L x 56" W x 42" H, 1,850 lbs operating
  Curb: 96" x 52" (Carrier P/N CRB-48-15)
  Clearances: Front 36", rear 24", sides 24", top open
  Connections: Supply 24"x16", return 24"x16", condensate ¾" PVC, gas 1¼" NPT
  Controls: BACnet MS/TP, DDC controller by Tridium/Niagara
  Sound: NC-40 at 5 ft from unit
  Served: Rooms 101-108, Zone "East Wing Ground Floor"
  Spec section: 23 81 26
  Source sheet: M-301
```

#### Air Handling Units (AHUs)

Per unit extract:
- **Tag**: AHU-1, AHU-2
- **CFM**: Supply and return/relief
- **Coils**: Cooling rows, heating rows, face velocity, entering/leaving temps
- **Filter**: Type (pleated/bag/HEPA), MERV rating, quantity and size
- **Fan**: HP, type (FC/BI/AF), quantity, VFD
- **Static pressure**: External and total
- **Humidifier**: Type (steam/evaporative), lbs/hr if present
- **Sound**: Supply and return NC levels
- **Physical**: L x W x H, weight, configuration (vertical/horizontal)
- **Clearances**: Service access doors, filter pull side, coil pull side
- **Controls**: BACnet, sequence of operation reference

#### Split Systems

Per system extract:
- **Indoor unit**: Tag, type (fan coil/air handler), CFM, coil capacity
- **Outdoor unit**: Tag, type (condensing unit/heat pump), tons, refrigerant
- **Pairing**: Indoor tag → outdoor tag mapping (critical for commissioning)
- **Line set**: Suction size, liquid size, maximum run length, maximum elevation change
- **Electrical**: Each unit separately — indoor MCA/MOCP, outdoor MCA/MOCP

#### VRF Systems

Per system extract:
- **Outdoor unit**: Tag, total capacity (tons/MBH), heat recovery capability
- **Indoor units**: Count, types (wall mount/ceiling cassette/ducted/floor console), individual capacity
- **Piping layout**: Branch selector box locations, total piping length, maximum piping run
- **Controls**: Central controller model, individual remote controllers
- **Electrical**: Outdoor unit MCA/MOCP, branch circuit for indoor units

#### Exhaust Fan Schedule

Per fan: Tag, type (centrifugal/inline/roof upblast/wall mount/ceiling), CFM, static pressure (in. w.c.), HP, voltage/phase, served rooms, speed control (single/multi/VFD), duct connection size, sound rating, spark-resistant construction (Yes/No for kitchen/lab/flammable).

**EXAMPLE EXHAUST FAN EXTRACT**:
```
EF-1: Kitchen Hood Exhaust
  Type: Roof upblast centrifugal, spark-resistant Class I
  CFM: 3,500 @ 1.0" w.c.
  HP: 2, voltage 208V/3ph
  Served: Kitchen (Room 120) — Type I grease hood
  Speed: VFD, interlocked with makeup air
  Duct: 20" x 14" welded black steel
  Sound: 72 dBA at 5 ft (on roof)
  Source: M-302

EF-2: Restroom Exhaust
  Type: Inline centrifugal
  CFM: 450 @ 0.5" w.c.
  HP: ¼, voltage 120V/1ph
  Served: Restrooms 105, 106, 107
  Speed: Single speed, on/off by occupancy sensor
  Duct: 10" round galvanized
  Sound: NC-30 at ceiling grille
  Source: M-302
```

#### Unit Heaters

Per unit: Tag, type (gas-fired/electric/hydronic/steam), BTU input/output or kW, fuel type, vent type (direct vent/power vent/unvented), mounting height (ft AFF), served area, thermostat type, electrical, gas connection size.

#### Pumps (HVAC)

Per pump: Tag, type (chilled water/hot water/condenser water), GPM, head (ft), HP, impeller size, suction/discharge pipe sizes, voltage/phase, VFD (Yes/No), redundancy (lead/lag/standby).

### Diffuser/Grille Schedule

Per device: Tag/type, size (neck or face), CFM, throw pattern (1/2/3/4-way), rooms, mounting (ceiling/wall/floor).

### Ductwork Sizes

Extract all duct sizes from M-100 plans:
- **Size format**: Rectangular = W x H, Round = diameter
- **Type**: Supply, return, exhaust, outside air
- **Material**: Galvanized, flex, lined, external wrap
- **Main trunk runs**: Trace from each air handler
- **Branch sizes**: At tees/takeoffs to rooms
- **Insulation**: Internal liner (thermal + acoustic) vs external wrap vs none
- **Fire/smoke dampers**: Location, type, size, fusible link temp or actuator

---

## PLUMBING EXTRACTION

### Plumbing Fixture Schedule — Detailed Extraction

**EXTRACT EVERY FIXTURE** from P-400 series:

| Data Point | Extract For Every Fixture |
|-----------|---------------------------|
| **Tag** | WC-1, LAV-1, SK-1, UR-1, MOP-1, DF-1, EW-1, SHR-1 |
| **Type** | Water Closet, Lavatory, Sink, Urinal, Mop Sink, Drinking Fountain, Eye Wash, Shower, Floor Drain |
| **Manufacturer/model** | Full catalog number (e.g., "Kohler K-4325-0") |
| **Mounting** | Floor/wall-hung/countertop/undermount/surface |
| **Connection sizes** | Hot (½" or ¾"), cold (½" or ¾"), waste (1½" or 2" or 3" or 4") |
| **Faucet type** | Manual/sensor/metering/push-button |
| **ADA compliance** | Yes/No — affects mounting height, clear floor space, insulation kit |
| **Flow rate** | GPM for faucets and showers, GPF for flush valves and tanks |
| **Flush type** | Flushometer (manual/sensor) or tank (gravity/pressure-assist) |
| **Quantity** | Total count across all rooms |
| **Carrier/support** | Wall carrier type for wall-hung fixtures (affects rough-in) |

**Fixture Count Summary Table** — build this from plans for procurement and ADA verification:

```
FIXTURE SUMMARY — PROJECT TOTAL

Type       | Tag  | Count | ADA Count | Flush/Flow  | Waste Size | Notes
-----------|------|-------|-----------|-------------|------------|------
Water Closet| WC-1 | 12   | 4         | 1.28 GPF    | 4"         | Wall-hung, sensor flush
Water Closet| WC-2 | 6    | 2         | 1.28 GPF    | 4"         | Floor-mount, tank type
Lavatory   | LAV-1| 14    | 4         | 0.5 GPM     | 1½"        | Countertop, sensor faucet
Urinal     | UR-1 | 6     | 2         | 0.125 GPF   | 2"         | Wall-hung, sensor flush
Mop Sink   | MOP-1| 3     | 0         | Hose bibb   | 3"         | Floor-mount, hot/cold
Drinking Ftn| DF-1 | 4    | 2         | Filtered    | 1½"        | Hi-lo ADA, bottle filler
Eye Wash   | EW-1 | 2     | 0         | Tempered    | 2"         | Pedestal, ANSI Z358.1
Shower     | SHR-1| 4     | 1         | 2.0 GPM     | 2"         | ADA roll-in with seat
Floor Drain| FD-1 | 18    | —         | —           | 2"         | 6" round nickel bronze
```

### Plumbing Equipment Schedule — Detailed Extraction

#### Water Heaters

Per unit:
- **Tag**: WH-1, WH-2
- **Type**: Storage tank / tankless (instantaneous) / heat pump / indirect (boiler-fed)
- **Capacity**: Gallons (storage), GPH recovery at 100°F rise
- **Input**: BTU/hr (gas) or kW (electric)
- **Recovery rate**: GPH at specified temperature rise
- **Fuel type**: Natural gas / propane / electric
- **Vent type**: Direct vent / power vent / atmospheric / none (electric)
- **Efficiency**: UEF (Uniform Energy Factor), thermal efficiency %
- **Electrical**: Voltage/phase for electric or ignition/controls
- **Connections**: Cold inlet, hot outlet, T&P relief, recirculation return, gas, vent
- **Location**: Mechanical room, ceiling space, exterior
- **Served areas**: Domestic hot water zones

**EXAMPLE WATER HEATER EXTRACT**:
```
WH-1: A.O. Smith BTH-400A
  Type: Commercial gas storage
  Capacity: 100 gallons, 400 MBH input
  Recovery: 409 GPH @ 100°F rise
  Fuel: Natural gas, ¾" gas connection
  Vent: Power vent, 6" diameter
  Efficiency: 96% thermal
  Electrical: 120V/1ph for ignition and controls
  Connections: 2" cold inlet, 2" hot outlet, ¾" T&P relief, 1" recirc return
  Location: Mechanical Room 015
  Served: All domestic hot water zones
  Source: P-301
```

#### Pumps (Plumbing)

Per pump:
- **Tag**: P-1, DRP-1, SWP-1
- **Type**: Domestic booster / recirculation / sump / sewage ejector / condensate return
- **GPM**: Flow rate at design point
- **Head**: Total dynamic head (ft)
- **HP**: Motor horsepower
- **Suction/discharge**: Pipe sizes
- **Voltage/phase**: Electrical requirements
- **Duplex**: Lead/lag or simplex — affects electrical circuit count

#### Backflow Preventers

Per device:
- **Tag**: BFP-1
- **Size**: Pipe size (¾" to 6")
- **Type**: RPBP (Reduced Pressure Backflow Preventer), DCVA (Double Check Valve Assembly), PVB (Pressure Vacuum Breaker)
- **Location**: Interior vault / exterior pit / above grade
- **Application**: Domestic, irrigation, fire service, boiler fill
- **Annual test required**: Yes (all RPBPs and DCVAs)

#### Grease Interceptors

Per unit:
- **Flow rate**: GPM rating
- **Capacity**: Gallons
- **Location**: Interior (under sink or floor) / exterior (buried)
- **Served fixtures**: Which sinks, dishwashers, floor drains connect
- **Sizing basis**: Per PDI-G101 or local code

#### Roof Drains

Per drain:
- **Type**: Primary (to storm system) / overflow (secondary) / controlled-flow
- **Size**: Body size and leader size (e.g., "4" body, 4" leader")
- **Strainer**: Dome type, flat grate, or combination
- **Insulation**: Insulated underdeck clamp (for condensation prevention)
- **Overflow**: Scupper or secondary drain — note elevation difference from primary

### Pipe Sizing

From plans and riser diagrams:
- **System**: DCW, DHW, DHW-R (recirc), sanitary, vent, storm, gas, medical gas, compressed air
- **Size**: Nominal diameter
- **Material**: Copper Type L / CPVC / PEX / PVC (DWV) / cast iron / HDPE / carbon steel / stainless steel
- **Main runs**: From source through building, noting size transitions
- **Insulation**: Type, thickness, jacket — required for DHW, chilled water, condensate
- **Valves**: Isolation valves at branches, balancing valves, check valves, PRVs

---

## ELECTRICAL EXTRACTION

### Panel Schedules — Detailed Extraction

**EXTRACT EVERY PANEL** — the most critical electrical data.

Panel header: Designation, location (room), voltage, phase, wires, main breaker amps, bus rating, fed from, mounting (surface/flush/NEMA rating), AIC rating.

Per circuit: Number, breaker size (amps), poles (1/2/3), load description, connected VA, phase assignment (A/B/C).

Panel totals: Connected VA per phase, demand VA, spare breakers (count), space slots (count).

**EXAMPLE PANEL EXTRACT**:
```
Panel LP-1A: Lighting Panel — First Floor East
  Location: Electrical Room 014
  Voltage: 120/208V, 3-phase, 4-wire
  Main breaker: 100A
  Bus rating: 225A
  Fed from: DP-1, Ckt 3 (3-pole 100A)
  Mounting: Surface, NEMA 1
  AIC rating: 22,000 AIC
  Circuits used: 30 of 42 spaces
  Spare breakers: 4
  Space slots: 8
  Connected load: Phase A=12,450 VA, B=11,880 VA, C=12,200 VA
  Demand load: 29,224 VA (80% demand factor applied)
```

### Electrical Equipment Schedule — Detailed Extraction

#### Switchboards / Switchgear

Per unit:
- **Tag**: MSB, SB-1
- **Type**: Switchboard / switchgear / MCC (motor control center)
- **Main bus rating**: Amps (e.g., 2000A, 4000A)
- **Main breaker/switch**: Size, type (circuit breaker / fusible switch / non-fused)
- **Voltage**: 480Y/277V, 208Y/120V, etc.
- **AIC rating**: Available fault current (e.g., 65,000 AIC)
- **Sections**: Number of sections, distribution sections vs feeder sections
- **Metering**: Revenue meter, sub-meter, digital power monitor
- **Surge protection**: SPD type, kA rating
- **Physical**: Dimensions, weight, front/rear access clearances (NEC 110.26)

#### Panelboards

Per panel:
- **Designation**: LP-1A, PP-2B, EP-1
- **Type**: Lighting / power / emergency / equipment
- **Bus rating**: 100A, 225A, 400A
- **Main breaker**: Size, or MLO (main lugs only)
- **Voltage**: 120/208V or 277/480V, phase, wires
- **Circuits**: Total spaces, used, spare, space
- **Mounting**: Surface / flush, NEMA rating (1/3R/4/4X/12)
- **AIC**: Interrupting rating
- **Fed from**: Upstream panel/switchboard and circuit

#### Transformers

Per transformer:
- **Tag**: T-1, XFMR-1
- **kVA**: Rating (e.g., 75 kVA, 150 kVA)
- **Primary voltage**: 480V, 277V
- **Secondary voltage**: 208Y/120V, 240V
- **Impedance**: % impedance (affects fault current)
- **Type**: Dry / liquid-filled
- **Location**: Indoor / outdoor, room or pad
- **K-factor**: If serving non-linear loads (K-4, K-13, K-20)
- **Sound level**: dB at 5 ft (for occupied areas)
- **Taps**: Primary taps (e.g., ±2.5%, ±5%)

#### Disconnect Switches

Per disconnect:
- **Amperage**: Size
- **Type**: Fused / non-fused
- **NEMA rating**: 1, 3R, 4, 4X, 12
- **Location**: Adjacent to served equipment (within sight)
- **Serves**: Equipment tag (RTU-1, AHU-2, etc.)

#### Generators

Per generator:
- **Tag**: GEN-1
- **kW rating**: Standby and prime power
- **Fuel type**: Diesel / natural gas / propane / bi-fuel
- **Tank**: Sub-base tank size (gallons), runtime at full load (hours)
- **Voltage**: Output voltage/phase
- **Transfer switch**: ATS or MTS, amperage, number of poles, transfer time (seconds)
- **Enclosure**: Level 1/2/3 sound-attenuated (for outdoor)
- **Sound**: dBA at 7 meters (23 ft)
- **Emissions**: EPA Tier rating
- **Electrical**: MCA, MOCP for battery charger and block heater

#### UPS Systems

Per UPS:
- **Tag**: UPS-1
- **kVA / kW**: Rating
- **Topology**: Online double-conversion / line-interactive / standby
- **Runtime**: Minutes at full load on battery
- **Battery type**: VRLA / lithium-ion, quantity, expected life
- **Input/output voltage**: Phase configuration
- **Bypass**: Internal static bypass, external maintenance bypass switch
- **PDU**: Associated power distribution units

### Single-Line Diagram

Complete power hierarchy — trace the full electrical distribution tree:
- Utility service: Voltage, phase, service size, meter location
- Main switchboard: Rating, main breaker, AIC
- Transformers: kVA, primary/secondary voltage
- Distribution panels: Fed-from tree, all feeder sizes
- ATS: Rating, transfer time, load classification (life safety, legally required standby, optional standby)
- Generator: kW, fuel, voltage, enclosure
- UPS: kVA, runtime, served panels

### Lighting Fixture Schedule

Per type: Mark (A, B, C, etc.), description, manufacturer, catalog number, wattage, lumens, color temp (K), CRI, mounting (recessed/surface/pendant/track/wall), lens type, voltage, dimming (0-10V/DALI/phase), emergency battery (Yes/No, 90-min), controls (occupancy/daylight/dimmer), total quantity.

Count fixtures per room from E-200 lighting plans.

### Receptacle/Device Counts

Count per room from E-100 power plans:
- Duplex receptacles (standard 120V)
- GFCI receptacles (wet locations per NEC 210.8)
- Dedicated circuits (refrigerator, microwave, copier, etc.)
- 240V outlets (welding, compressor, EV charger)
- Data/telecom outlets
- Special devices (card readers, cameras, motion sensors, AV connections)

---

## FIRE PROTECTION EXTRACTION

- **System type**: Wet / dry / pre-action / deluge / combined
- **Design standard**: NFPA 13 / 13R / 13D
- **Hazard classification**: Light Hazard / Ordinary Hazard Group 1 or 2 / Extra Hazard
- **Riser**: Location, size, FDC location/type, inspector test connection
- **Head schedule**: Type (pendant/upright/sidewall/concealed), temp rating (°F), K-factor, coverage area, finish (chrome/white/brass)
- **Fire pump**: GPM, PSI, HP, driver (electric/diesel), controller, jockey pump (if present)
- **Standpipes**: Class I/II/III, locations, hose connections per floor

---

## MEP COORDINATION DATA

### Ceiling Cavity Conflicts

For every floor, verify ceiling height vs. MEP routing:
- **Ceiling height**: Finish ceiling (e.g., 9'-0" AFF) from architectural reflected ceiling plan
- **Structure depth**: Beam/joist depth below deck (e.g., 18" W-beam at 10'-6" AFF)
- **Available MEP zone**: Structure bottom to ceiling top (e.g., 10'-6" minus 9'-0" = 18" clear)
- **Duct size**: Largest duct in that zone (e.g., 24"x14" = 14" vertical)
- **Pipe runs**: Largest pipe crossing (e.g., 4" DWV with pitch = ~5" vertical with hangers)
- **Conflict**: If duct + pipe + light fixture + ceiling grid > available zone → flag for coordination

**EXAMPLE COORDINATION LOG**:
```
CEILING COORDINATION — FIRST FLOOR CORRIDOR (GRID C-D / 3-7)

Available zone: 18" (structure at 10'-6", ceiling at 9'-0")
Items in zone:
  - Supply duct 24"x14" (main trunk from RTU-1) = 14" + 2" hanger = 16"
  - 4" sanitary waste (pitched ¼"/ft over 20') = 5" + hanger = 6"
  - Sprinkler main 2" = 3" with fitting
  - 2x4 recessed troffer (Type A fixture) = 4" above ceiling

⚠ CONFLICT: Duct at 16" + pipe crossing at 6" cannot stack in 18" zone.
  Resolution options:
  1. Reduce duct to 30"x10" (same CFM, wider but shorter)
  2. Route sanitary below duct (requires coordination with structural)
  3. Lower ceiling to 8'-8" (verify code minimum and ADA clearance)
  Flag for MEP coordination meeting.
```

### Beam/Slab Penetration Schedule

Extract from structural/MEP coordination drawings:
- **Location**: Grid intersection or room reference
- **Size**: Penetration diameter or dimensions
- **Sleeve**: Required? Type (pipe sleeve, link seal, fire-stop collar)
- **Fire rating**: Through fire-rated assembly? If yes, firestop system required
- **Structural approval**: P.E. stamp required for penetrations through beams

### Shaft Sizing and Vertical Routing

Per shaft:
- **Shaft ID**: From architectural plans (e.g., "Mech Shaft A", "Plumbing Chase 2")
- **Shaft dimensions**: Clear interior size
- **Systems routed**: Duct risers, pipe risers, conduit risers
- **Fire rating**: Shaft wall rating (1-hr, 2-hr)
- **Access**: Access doors per floor (size, fire-rated)

### Equipment Pads and Curbs

Per equipment item requiring a pad or curb:
- **Equipment tag**: RTU-1, AHU-2, GEN-1, etc.
- **Pad/curb dimensions**: L x W x H
- **Material**: Concrete housekeeping pad, prefab roof curb, steel dunnage
- **Weight capacity**: Equipment operating weight + safety factor
- **Vibration isolation**: Spring isolators, neoprene pads, inertia base
- **Drain**: Floor drain or roof drain near pad for condensate/washdown
- **Electrical**: Disconnect switch location relative to pad

### Roof Penetration Schedule

Per penetration:
- **Equipment/system**: RTU curb, exhaust fan curb, plumbing vent, conduit stub
- **Size**: Opening dimensions
- **Curb height**: Minimum 8" above finished roof (or per roofing warranty)
- **Flashing method**: Pitch pocket, boot, prefab curb with counter-flashing
- **Roofing warranty**: Penetrations must comply with roofing manufacturer requirements
- **Structural**: Verify roof framing can support concentrated load at penetration

---

## CROSS-REFERENCE RULES

| MEP Data | Cross-Reference Against | Validation |
|----------|------------------------|------------|
| Equipment MCA/MOCP | Panel circuits | Every equipment should have matching circuit |
| Equipment room locations | Room schedule | Rooms must exist in plans-spatial.json |
| Diffuser CFM per room | Equipment total CFM | Room sums ≤ equipment total |
| Light fixture counts | Schedule totals | Room sums = schedule total |
| Panel total VA | Service capacity | Panels ≤ upstream capacity |
| Generator kW | Emergency loads | Generator ≥ emergency total |
| Sprinkler coverage | Room areas | Every occupied room covered |
| Equipment weight | Structural pad capacity | Weight ≤ pad design capacity |
| Duct size | Ceiling zone clearance | Duct fits in available MEP zone |
| Pipe pitch | Available slope distance | Gravity drain achieves minimum ¼"/ft |
| Equipment submittal | Submittal log status | Every equipment item has approved submittal |
| Equipment lead time | Procurement log delivery | Lead times align with construction schedule |
| Equipment spec section | Specs-quality requirements | Equipment meets specified performance |

### Cross-Reference to Project Records

| MEP Extraction Data | Target JSON File | Field Path | Purpose |
|---------------------|------------------|------------|---------|
| Equipment tags + locations | `plans-spatial.json` | `mep_systems.*.equipment[]` | Location tracking on plans |
| Equipment spec compliance | `specs-quality.json` | `spec_sections[].hold_points[]` | Inspection acceptance criteria |
| Equipment submittals | `submittal-log.json` | `id`, `status`, `lead_time_weeks` | Approval status tracking |
| Equipment procurement | `procurement-log.json` | `item`, `delivery_status`, `expected_delivery` | Delivery and cost tracking |
| Commissioning test results | `quality-data.json` | `system_tests[]` | TAB, hydrostatic, megger results |
| Equipment warranties | `quality-data.json` | `warranties[]` | Warranty tracking for closeout |
| Inspection records | `inspection-log.json` | `inspection_log[]` | MEP rough-in and final inspections |

---

## OUTPUT STRUCTURE

### For plans-spatial.json → mep_systems

```json
{
  "mep_systems": {
    "mechanical": {
      "source_sheets": ["M-101", "M-102", "M-301", "M-302"],
      "equipment": [
        {
          "tag": "RTU-1",
          "type": "Rooftop Unit",
          "manufacturer": "Carrier",
          "model": "48TC-D16",
          "location": { "grid": "C-D/3-4", "room": null, "floor": "Roof", "mounting": "Roof curb" },
          "capacity": {
            "cooling_tons": 15,
            "heating_mbh": 300,
            "airflow_cfm": 5400,
            "static_pressure_inwc": 1.5
          },
          "electrical": {
            "voltage": 460, "phase": 3, "hz": 60,
            "fla": 28.5, "mca": 35.6, "mocp": 45, "lra": 142
          },
          "physical": {
            "length_in": 100, "width_in": 56, "height_in": 42,
            "weight_lbs": 1850,
            "curb_size": "96x52"
          },
          "clearances": {
            "front_in": 36, "rear_in": 24, "sides_in": 24, "top": "open"
          },
          "connections": {
            "supply_duct": "24x16", "return_duct": "24x16",
            "condensate": "3/4 PVC", "gas": "1-1/4 NPT"
          },
          "controls": { "protocol": "BACnet MS/TP", "controller": "Tridium Niagara" },
          "efficiency": { "seer2": null, "eer": 11.0, "ieer": 14.2, "afue": 0.80 },
          "sound": { "nc_rating": 40, "dba_at_5ft": null },
          "refrigerant": "R-410A",
          "served_rooms": ["101", "102", "103", "104", "105", "106", "107", "108"],
          "spec_section": "23 81 26",
          "source_sheet": "M-301"
        }
      ],
      "exhaust_fans": [],
      "diffusers_grilles": [],
      "duct_runs": []
    },
    "plumbing": {
      "source_sheets": ["P-101", "P-201", "P-301"],
      "equipment": [],
      "fixtures": [
        {
          "tag": "WC-1",
          "type": "Water Closet",
          "manufacturer": "Kohler",
          "model": "K-4325-0",
          "mounting": "Wall-hung",
          "connections": { "cold": "1/2", "waste": "4" },
          "flow_rate": "1.28 GPF",
          "ada_compliant": true,
          "count_total": 12,
          "count_ada": 4,
          "rooms": ["105", "106", "205", "206"],
          "spec_section": "22 42 13",
          "source_sheet": "P-301"
        }
      ],
      "pipe_runs": [],
      "risers": []
    },
    "electrical": {
      "source_sheets": ["E-101", "E-201", "E-301", "E-501"],
      "panel_schedules": [
        {
          "designation": "LP-1A",
          "type": "Lighting",
          "location": "Electrical Room 014",
          "voltage": "120/208V",
          "phase": 3,
          "main_breaker_amps": 100,
          "bus_rating_amps": 225,
          "fed_from": "DP-1 Ckt 3",
          "aic_rating": 22000,
          "total_spaces": 42,
          "circuits_used": 30,
          "spare_breakers": 4,
          "space_slots": 8,
          "connected_va": { "phase_a": 12450, "phase_b": 11880, "phase_c": 12200 },
          "demand_va": 29224
        }
      ],
      "single_line_data": {
        "utility_service": { "voltage": "480Y/277V", "phase": 3, "service_amps": 2000 },
        "main_switchboard": { "tag": "MSB", "rating_amps": 2000, "main_breaker": 2000, "aic": 65000 },
        "transformers": [],
        "distribution_tree": [],
        "generator": {},
        "ats": {},
        "ups": {}
      },
      "circuit_assignments": [],
      "equipment": [],
      "lighting_fixtures": [],
      "device_counts_by_room": []
    },
    "fire_protection": {
      "system_type": "wet",
      "design_standard": "NFPA 13",
      "hazard_class": "Light Hazard",
      "riser_location": "Fire Riser Room 010",
      "fdc_location": "North wall, Grid A/5",
      "equipment": [],
      "sprinkler_heads": []
    },
    "coordination": {
      "ceiling_conflicts": [],
      "penetration_schedule": [],
      "shaft_routing": [],
      "equipment_pads": [],
      "roof_penetrations": []
    },
    "conflicts": []
  }
}
```

### For quality-data.json → system_tests (commissioning records)

```json
{
  "system_tests": [
    {
      "test_id": "ST-001",
      "system": "HVAC",
      "test_type": "TAB",
      "description": "RTU-1 air balance — supply CFM per diffuser vs. schedule",
      "equipment_tag": "RTU-1",
      "spec_section": "23 05 93",
      "result": "pass",
      "tested_date": "2026-04-15",
      "tested_by": "ABC Balancing, Inc.",
      "witnessed_by": "John Smith, P.E.",
      "notes": "All diffusers within ±10% of scheduled CFM"
    },
    {
      "test_id": "ST-002",
      "system": "plumbing",
      "test_type": "hydrostatic",
      "description": "Domestic water pressure test — 150 PSI for 2 hours",
      "equipment_tag": null,
      "spec_section": "22 05 23",
      "result": "pass",
      "tested_date": "2026-03-20",
      "tested_by": "XYZ Plumbing Contractor",
      "witnessed_by": "City Inspector #1234",
      "notes": "No pressure drop observed"
    },
    {
      "test_id": "ST-003",
      "system": "electrical",
      "test_type": "megger",
      "description": "Feeder insulation resistance — MSB to DP-1",
      "equipment_tag": "DP-1",
      "spec_section": "26 05 73",
      "result": "pass",
      "tested_date": "2026-03-10",
      "tested_by": "DEF Electrical Contractor",
      "witnessed_by": "Engineer of Record",
      "notes": "All feeders > 100 megohms at 1000V DC"
    }
  ]
}
```

### For procurement-log.json → equipment submittals and lead times

```json
{
  "id": "PROC-015",
  "item": "RTU-1: Carrier 48TC-D16, 15-Ton Rooftop Unit",
  "category": "long_lead",
  "expected_delivery": "2026-05-01",
  "delivery_status": "ordered",
  "total_cost": "$18,500",
  "submittal_id": "SUB-042",
  "cert_status": "pending",
  "equipment_tag": "RTU-1",
  "spec_section": "23 81 26",
  "lead_time_weeks": 12,
  "notes": "Factory-built, 12-week lead time. Submittal approved 2026-02-01."
}
```

### For dashboard data.js → mep section

```javascript
mep: {
  equipment: [
    // ALL equipment across disciplines with full detail
    {
      id: "RTU-1", tag: "RTU-1", type: "Rooftop Unit",
      discipline: "mechanical",    // mechanical|plumbing|electrical|fire_protection
      system: "hvac",              // hvac|exhaust|plumbing|electrical_power|lighting|fire
      description: "15-Ton Rooftop Unit with gas heat",
      location: { grid: "C-D/3-4", room: null, mounting: "Roof" },
      capacity: { cooling_tons: 15, heating_mbh: 300, airflow_cfm: 5400 },
      electrical: { voltage: 460, phase: 3, fla: 28.5, mca: 35.6, mocp: 45 },
      physical: { length_in: 100, width_in: 56, height_in: 42, weight_lbs: 1850 },
      connections: { supply_duct: "24x16", return_duct: "24x16", gas: "1-1/4 NPT" },
      efficiency: { eer: 11.0, ieer: 14.2, afue: 0.80 },
      controls: { protocol: "BACnet MS/TP" },
      served_rooms: ["101","102","103","104","105","106","107","108"],
      manufacturer: "Carrier", model: "48TC-D16",
      spec_section: "23 81 26", source_sheet: "M-301",
      procurement: { submittal_id: "SUB-042", status: "ordered", lead_weeks: 12 }
    }
  ],
  panels: [],
  single_line: {},
  fixtures: { lighting: [], plumbing: [] },
  distribution: { duct_mains: [], pipe_mains: [] },
  fire_protection: {},
  coordination: { ceiling_conflicts: [], penetrations: [], shaft_routing: [] },
  device_counts: [],
  conflicts: [],
  extraction_coverage: {
    sheets_processed: [],
    total_equipment_count: 0,
    completeness_pct: 0
  }
}
```

---

## SUMMARY CHECKLIST — MEP EXTRACTION REVIEW

**BEFORE ROUGH-IN**:

- [ ] **Equipment schedules**: Every HVAC, plumbing, and electrical equipment item extracted with full specs
- [ ] **Panel schedules**: All panels extracted with circuit assignments and load calculations
- [ ] **Single-line diagram**: Complete power hierarchy traced from utility to branch panels
- [ ] **Fixture schedules**: Lighting and plumbing fixtures with counts, types, ADA compliance
- [ ] **Pipe/duct sizing**: All main runs extracted with sizes, materials, insulation
- [ ] **Fire protection**: System type, riser location, head schedule, hazard classification
- [ ] **Coordination data**: Ceiling conflicts identified, penetrations cataloged, shaft routing verified
- [ ] **Equipment pads/curbs**: Dimensions, weight capacity, vibration isolation confirmed
- [ ] **Submittals**: Every equipment item has a submittal in submittal-log.json
- [ ] **Procurement**: Long-lead items flagged in procurement-log.json with lead times

**DURING INSTALLATION**:

- [ ] **Equipment tags match**: Installed equipment tags match extraction records
- [ ] **Electrical connections**: MCA/MOCP on panels match equipment requirements
- [ ] **Duct/pipe routing**: Field routing matches coordination drawings (or as-built deviations logged)
- [ ] **Penetrations**: Firestop at all rated assemblies, structural approval for beam penetrations
- [ ] **Controls wiring**: BAS points connected per sequence of operations

**AT COMMISSIONING**:

- [ ] **TAB report**: Air and water balance results recorded in quality-data.json system_tests
- [ ] **Hydrostatic tests**: Plumbing pressure tests documented
- [ ] **Electrical testing**: Megger, load bank, ground fault tests documented
- [ ] **Fire protection**: Flow test, trip test, alarm test documented
- [ ] **Warranties**: All equipment warranties extracted to quality-data.json warranties
- [ ] **O&M manuals**: Equipment data cross-referenced for closeout package
