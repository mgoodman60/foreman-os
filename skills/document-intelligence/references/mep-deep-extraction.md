# MEP Systems — Deep Extraction Guide

Comprehensive extraction reference for Mechanical, Electrical, and Plumbing (MEP) systems from construction documents. This guide covers all three MEP disciplines plus fire protection and specialty systems.

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

---

## MECHANICAL EXTRACTION

### HVAC Equipment Schedule

**EXTRACT EVERY UNIT** from mechanical schedules (M-300 series).

Per equipment item:
- **Tag**: RTU-1, AHU-2, EF-3, MAU-1, UH-1, FCU-1
- **Type**: Rooftop Unit, Air Handler, Exhaust Fan, Make-Up Air, Unit Heater, Fan Coil, Split System, Mini-Split, Heat Pump, ERV/HRV
- **Location**: Roof/mech room/ceiling space + grid ref or room
- **Cooling**: Tons or MBH, type (DX, chilled water)
- **Heating**: MBH or KW, type (gas, electric, heat pump, hydronic)
- **Airflow**: CFM, external static pressure (in. w.c.)
- **Efficiency**: SEER, EER, AFUE, COP, HSPF
- **Refrigerant**: R-410A, R-32, R-454B
- **Electrical**: Voltage/phase/Hz, MCA, MOCP, FLA, LRA
- **Physical**: Weight, dimensions, sound rating, gas connection size
- **Controls**: DDC/standalone, economizer type, VFD
- **Served areas**: Room numbers, zone name, main duct size
- **Manufacturer/model**: From submittals if available

### Exhaust Fan Schedule

Per fan: Tag, type (centrifugal/inline/roof/wall), CFM, static pressure, HP, voltage/phase, served rooms, speed control.

### Diffuser/Grille Schedule

Per device: Tag/type, size (neck or face), CFM, throw pattern (1/2/3/4-way), rooms, mounting (ceiling/wall/floor).

### Ductwork Sizes

Extract all duct sizes from M-100 plans:
- **Size format**: Rectangular=W×H, Round=diameter
- **Type**: Supply, return, exhaust, outside air
- **Material**: Galvanized, flex, lined, external wrap
- **Main trunk runs**: Trace from each air handler
- **Branch sizes**: At tees/takeoffs to rooms

---

## PLUMBING EXTRACTION

### Plumbing Fixture Schedule

**EXTRACT EVERY FIXTURE** from P-400 series:
- **Tag**: WC-1, LAV-1, SK-1, UR-1, MOP-1, DF-1, EW-1
- **Type**: Water Closet, Lavatory, Sink, Urinal, Drinking Fountain, Eye Wash, Floor Drain
- **Manufacturer/model**: Full catalog info
- **Mounting**: Floor/wall-hung/countertop/undermount
- **Connection sizes**: Hot, cold, waste
- **Faucet type**: Manual/sensor/metering
- **ADA compliance**: Yes/no
- **Flow rate**: GPM for faucets, GPF for flush
- **Quantity**: Total count

### Water Heater/Boiler Schedule

Per unit: Tag, type (tank/tankless/heat pump), capacity (gallons, GPH, BTU), efficiency, fuel, electrical, vent type, location, served areas.

### Pipe Sizing

From plans and riser diagrams:
- **System**: DCW, DHW, sanitary, vent, storm, gas, medical gas
- **Size**: Nominal diameter
- **Material**: Copper/CPVC/PEX/PVC/cast iron/HDPE/steel/SS
- **Main runs**: From source through building

---

## ELECTRICAL EXTRACTION

### Panel Schedules

**EXTRACT EVERY PANEL** — the most critical electrical data.

Panel header: Designation, location (room), voltage, phase, wires, main breaker amps, bus rating, fed from, mounting, AIC rating.

Per circuit: Number, breaker size, poles, load description, connected VA, phase (A/B/C).

Panel totals: Connected VA per phase, demand VA, spare breakers, space slots.

### Single-Line Diagram

Complete power hierarchy:
- Utility service: Voltage, phase, service size
- Main switchboard: Rating, main breaker
- Transformers: kVA, primary/secondary voltage
- Distribution panels: Fed-from tree
- ATS: Rating, transfer time
- Generator: KW, fuel, voltage, enclosure
- UPS: kVA, runtime

### Lighting Fixture Schedule

Per type: Mark, description, manufacturer, catalog number, wattage, lumens, color temp (K), CRI, mounting, lens type, voltage, dimming, emergency battery, controls, total quantity.

Count fixtures per room from E-200 lighting plans.

### Receptacle/Device Counts

Count per room from E-100 power plans:
- Duplex receptacles, GFCI, dedicated circuits, 240V outlets
- Data/telecom outlets
- Special devices (card readers, cameras, sensors)

---

## FIRE PROTECTION EXTRACTION

- **System type**: Wet/dry/pre-action/deluge/combined
- **Design standard**: NFPA 13/13R/13D
- **Hazard classification**: Light/Ordinary/Extra
- **Riser**: Location, size, FDC location/type
- **Head schedule**: Type (pendant/upright/sidewall/concealed), temp rating, K-factor, coverage, finish
- **Fire pump**: GPM, PSI, HP (if present)

---

## CROSS-REFERENCE RULES

| MEP Data | Cross-Reference Against | Validation |
|----------|------------------------|------------|
| Equipment MCA/MOCP | Panel circuits | Every equipment should have matching circuit |
| Equipment room locations | Room schedule | Rooms must exist |
| Diffuser CFM per room | Equipment total CFM | Room sums ≤ equipment total |
| Light fixture counts | Schedule totals | Room sums ≈ schedule total |
| Panel total VA | Service capacity | Panels ≤ upstream capacity |
| Generator kW | Emergency loads | Generator ≥ emergency total |
| Sprinkler coverage | Room areas | Every occupied room covered |

---

## OUTPUT STRUCTURE

### For plans-spatial.json → mep_systems

```json
{
  "mep_systems": {
    "mechanical": {
      "source_sheets": [],
      "equipment": [],
      "exhaust_fans": [],
      "diffusers_grilles": [],
      "duct_runs": []
    },
    "plumbing": {
      "source_sheets": [],
      "equipment": [],
      "fixtures": [],
      "pipe_runs": [],
      "risers": []
    },
    "electrical": {
      "source_sheets": [],
      "panel_schedules": [],
      "single_line_data": {},
      "circuit_assignments": [],
      "equipment": [],
      "lighting_fixtures": [],
      "device_counts_by_room": []
    },
    "fire_protection": {
      "system_type": "",
      "riser_location": "",
      "fdc_location": "",
      "equipment": [],
      "sprinkler_heads": []
    },
    "specialty": {},
    "conflicts": []
  }
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
      description: "10-Ton Rooftop Unit",
      location: { grid: "C-D/3-4", room: null, mounting: "Roof" },
      capacity: { cooling_tons: 10, heating_mbh: 250, airflow_cfm: 4000 },
      electrical: { voltage: 208, phase: 3, mca: 48, mocp: 60 },
      served_rooms: ["101","102","103"],
      manufacturer: null, model: null,
      spec_section: "23 81 26", source_sheet: "M-301"
    }
  ],
  panels: [],
  single_line: {},
  fixtures: { lighting: [], plumbing: [] },
  distribution: { duct_mains: [], pipe_mains: [] },
  fire_protection: {},
  device_counts: [],
  conflicts: [],
  extraction_coverage: {
    sheets_processed: [],
    total_equipment_count: 0,
    completeness_pct: 0
  }
}
```
