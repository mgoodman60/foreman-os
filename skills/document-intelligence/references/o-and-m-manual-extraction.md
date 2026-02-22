# O&M Manual — Deep Extraction Guide

Extract structured, maintenance-actionable data from Operation and Maintenance manuals. O&M manuals are the primary reference for building owners and facility managers after project turnover. This guide covers equipment operation procedures, preventive maintenance schedules, parts lists, troubleshooting guides, emergency procedures, and control sequences. Thorough extraction enables automated maintenance scheduling, equipment tracking, and facility management integration.

---

## Extraction Priority Matrix

| Priority | Data Type | Use Case | Completeness Target |
|----------|-----------|----------|-------------------|
| **CRITICAL** | Preventive maintenance schedules (PM intervals, procedures) | Owner maintenance planning, warranty compliance, lifecycle cost | 100% — every equipment item |
| **CRITICAL** | Equipment operation procedures (start/stop, setpoints) | Facility staff training, emergency response | 100% — all major systems |
| **CRITICAL** | Emergency shutdown procedures | Life safety, property protection | 100% — all systems with emergency stops |
| **HIGH** | Parts lists (part numbers, suppliers, lead times) | Spare parts inventory, replacement procurement | All wear items + critical parts |
| **HIGH** | Control sequences of operation | BMS programming, commissioning verification, troubleshooting | All HVAC sequences |
| **HIGH** | Warranty information cross-reference | Maintenance required to maintain warranty | 100% — see warranty-extraction.md |
| **MEDIUM** | Troubleshooting guides (symptom-cause-remedy) | Facility staff reference, service call reduction | All major equipment |
| **MEDIUM** | BMS/DDC points list | Controls integration, alarm management | All monitored points |
| **MEDIUM** | Nameplate data and specifications | Equipment identification, replacement specification | 100% — all equipment |
| **LOW** | General product literature | Reference only | As provided |

---

## DOCUMENT IDENTIFICATION

### Signals this is an O&M manual

- "Operation and Maintenance Manual" or "O&M Manual" on cover/spine
- Tab dividers organized by CSI division or building system
- Manufacturer product literature and cut sheets
- Maintenance schedule tables with intervals (daily/weekly/monthly/quarterly/annual)
- Parts lists with part numbers, descriptions, and supplier information
- Wiring diagrams and control schematics
- Start-up and commissioning checklists (completed)
- Warranty documentation (see warranty-extraction.md for deep extraction)
- Training sign-off sheets
- Emergency contact lists

### O&M Manual Organization

| Section | Typical Contents | Extraction Priority |
|---------|-----------------|-------------------|
| Division 01 | General requirements, emergency contacts, training records | HIGH |
| Division 03 | Concrete maintenance (joint sealing, crack repair) | LOW |
| Division 07 | Roofing maintenance, sealant schedules | MEDIUM |
| Division 08 | Door hardware maintenance, overhead door PM | MEDIUM |
| Division 09 | Finish maintenance (flooring care, paint touch-up) | LOW |
| Division 21 | Fire protection maintenance (head inspection, valve exercise) | HIGH |
| Division 22 | Plumbing maintenance (backflow testing, water heater PM) | HIGH |
| Division 23 | HVAC maintenance (filter changes, coil cleaning, belt replacement) | CRITICAL |
| Division 25 | Building automation (BAS maintenance, sensor calibration) | HIGH |
| Division 26 | Electrical maintenance (breaker exercise, transformer inspection) | HIGH |
| Division 27 | Communications (network maintenance, fire alarm) | MEDIUM |
| Division 28 | Electronic safety/security (CCTV, access control) | MEDIUM |
| Division 14 | Elevator (maintenance contract, emergency procedures) | HIGH |

---

## EQUIPMENT OPERATION PROCEDURES

### Extraction Targets — Per Equipment Item

| Data Point | Type | Example |
|-----------|------|---------|
| `equipment_tag` | string | "RTU-1" |
| `equipment_name` | string | "Rooftop Unit 1" |
| `manufacturer` | string | "Carrier" |
| `model` | string | "48XC-N14090" |
| `serial_number` | string | "3216F45892" |
| `location` | string | "Roof, Grid C-D/3-4" |
| `serves` | string | "East Wing, Level 1 (Rooms 101-112)" |
| `spec_section` | string | "23 81 26" |

#### Start-Up Procedure

Extract step-by-step start-up sequence:

```
RTU-1 START-UP PROCEDURE

Pre-Start Checklist:
1. Verify electrical disconnect is OFF
2. Check filter condition — replace if dirty (MERV 13, 20×25×2)
3. Verify condensate drain is clear and trapped
4. Check belt tension (1/2" deflection at midpoint)
5. Verify all access panels secured
6. Check refrigerant sight glass (clear = proper charge)

Start-Up Sequence:
1. Close electrical disconnect
2. Set thermostat/BAS to call for heating or cooling
3. Verify supply fan starts within 30 seconds
4. Verify compressor starts on cooling call (wait 5-minute anti-short-cycle delay)
5. Verify gas valve opens on heating call (verify flame through sight glass)
6. Check supply air temperature (cooling: 52-55°F, heating: 90-110°F)
7. Verify economizer operates (dampers modulate with outdoor temp)
8. Monitor for 15 minutes — check for unusual noise, vibration, odor

Normal Operating Parameters:
- Supply fan: 850 RPM, 12.4 amps
- Cooling: Supply air 52-55°F
- Heating: Supply air 90-110°F
- Economizer changeover: 55°F outdoor temp
- Filter DP: 0.2-0.8 in. w.c. (replace at 1.0)
```

#### Shutdown Procedure

```
RTU-1 SHUTDOWN PROCEDURE

Normal Shutdown:
1. Set thermostat/BAS to OFF or Unoccupied
2. Supply fan runs for 3 minutes (purge cycle)
3. Compressor stops, fan continues
4. Fan stops after purge cycle
5. System enters standby mode

Emergency Shutdown:
1. Open electrical disconnect (red handle on unit)
2. If gas leak suspected: close gas valve (yellow handle, quarter-turn)
3. If refrigerant leak: evacuate roof area, call service technician
4. Do NOT re-energize until inspected by qualified technician

Seasonal Shutdown (Extended):
1. Normal shutdown sequence
2. Close gas supply valve
3. Clean or replace filters
4. Clean condensate pan and drain
5. Cover outdoor air intake (if extended winter shutdown)
6. Disconnect power at breaker if unit will be off >30 days
```

---

## PREVENTIVE MAINTENANCE SCHEDULES

### Extraction Targets — PM Schedule Table

**EXTRACT EVERY PM TASK** for every equipment item:

| Data Point | Type | Example |
|-----------|------|---------|
| `equipment_tag` | string | "RTU-1" |
| `pm_task` | string | "Replace air filters" |
| `interval` | string | "quarterly" |
| `interval_code` | string | "Q" (D=daily, W=weekly, M=monthly, Q=quarterly, SA=semi-annual, A=annual) |
| `procedure` | string | "Remove access panel, slide out filters, install new MERV 13 20×25×2" |
| `required_parts` | array | [{"part": "Air filter", "spec": "MERV 13, 20×25×2", "qty": 4}] |
| `estimated_time_minutes` | integer | 15 |
| `skill_level` | string | "basic" / "intermediate" / "technician" / "specialist" |
| `tools_required` | array | ["Screwdriver (panel access)", "Flashlight"] |
| `warranty_critical` | boolean | true |
| `warranty_note` | string | "Quarterly filter changes required to maintain Carrier warranty" |

### Standard PM Schedule Template

#### HVAC Equipment

| Task | Daily | Weekly | Monthly | Quarterly | Semi-Annual | Annual |
|------|-------|--------|---------|-----------|-------------|--------|
| Check thermostat operation | | X | | | | |
| Check filter DP (visual or gauge) | | | X | | | |
| Replace filters | | | | X | | |
| Clean condensate pan and drain | | | | X | | |
| Check belt tension and condition | | | | X | | |
| Lubricate fan bearings | | | | | X | |
| Clean evaporator and condenser coils | | | | | | X |
| Check refrigerant charge | | | | | | X |
| Test safety controls | | | | | | X |
| Inspect ductwork and dampers | | | | | | X |
| Full operational test | | | | | | X |

#### Electrical Equipment

| Task | Monthly | Quarterly | Semi-Annual | Annual |
|------|---------|-----------|-------------|--------|
| Visual inspection (heat, corrosion, connections) | X | | | |
| Check breaker operation (exercise) | | | X | |
| Thermal scan (IR camera) | | | | X |
| Test GFP relay | | | | X |
| Test transfer switch | | | X | |
| Generator exercise (no-load) | X | | | |
| Generator load test (full) | | | | X |
| Battery inspection and test | | X | | |

#### Plumbing Equipment

| Task | Monthly | Quarterly | Semi-Annual | Annual |
|------|---------|-----------|-------------|--------|
| Check water heater temperature | X | | | |
| Flush water heater (sediment) | | | X | |
| Test T&P relief valve | | | | X |
| Backflow preventer test | | | | X |
| Clean floor drains | | X | | |
| Exercise shutoff valves | | | | X |
| Inspect expansion tank pressure | | | | X |

#### Fire Protection

| Task | Weekly | Monthly | Quarterly | Semi-Annual | Annual | 5-Year |
|------|--------|---------|-----------|-------------|--------|--------|
| Visual sprinkler head check | | | | | X | |
| Test fire alarm panel | | | | | X | |
| Exercise control valves | | | X | | | |
| Test tamper switches | | | | | X | |
| Test flow switches | | | | | X | |
| Fire pump test (if applicable) | X | | | | | |
| Internal pipe inspection | | | | | | X |
| Hydrostatic re-test | | | | | | X |

---

## PARTS LISTS

### Extraction Targets — Per Equipment Item

| Data Point | Type | Example |
|-----------|------|---------|
| `equipment_tag` | string | "RTU-1" |
| `part_category` | string | "wear_item" / "critical_spare" / "consumable" / "structural" |
| `part_description` | string | "Supply fan belt" |
| `part_number` | string | "Carrier P/N 50XC500012" |
| `oem_part_number` | string | "Gates A68" |
| `compatible_substitutes` | array | ["Dayton 6L267", "Browning A68"] |
| `supplier` | string | "Grainger, Stock #6L267" |
| `estimated_cost` | string | "$12.50" |
| `lead_time` | string | "In stock (standard)" |
| `quantity_per_unit` | integer | 1 |
| `recommended_spares_on_hand` | integer | 2 |
| `replacement_interval` | string | "Annual or when worn" |

### Recommended Spare Parts Inventory

Generate from extracted parts lists:

```
RECOMMENDED SPARE PARTS INVENTORY

HVAC:
- Air filters (MERV 13, 20×25×2): 16 ea (4 per RTU × 4 changes/year)
- Fan belts (Gates A68): 4 ea (1 per RTU spare)
- Thermostat batteries (AA): 24 ea
- Condensate pump (Little Giant EC-1): 1 ea (emergency spare)

ELECTRICAL:
- Panel breakers (Square D QO120): 6 ea (assorted spares)
- Fuses (Class RK5, 30A): 6 ea
- Lamp ballasts (GE UltraMax): 4 ea (matching installed)
- Exit sign batteries: 6 ea

PLUMBING:
- Backflow preventer repair kit (Watts 009-RK): 1 ea
- Water heater anode rod: 1 ea (Rheem P/N SP11526)
- Toilet repair kits (Sloan Regal): 6 ea
- Faucet cartridges (Moen 1222): 4 ea

FIRE PROTECTION:
- Sprinkler heads (spare box per NFPA 13): 6 ea (matching installed)
- Sprinkler wrench: 1 ea (matches head type)
- Head guard cages: 2 ea (for exposed heads)
```

---

## TROUBLESHOOTING GUIDES

### Extraction Format — Symptom → Cause → Remedy

| Data Point | Type | Example |
|-----------|------|---------|
| `equipment_tag` | string | "RTU-1" |
| `symptom` | string | "No cooling" |
| `possible_causes` | array | See table below |
| `diagnostic_steps` | array | Ordered troubleshooting sequence |

### Example Troubleshooting Table

```
RTU-1 TROUBLESHOOTING

SYMPTOM: No cooling output
┌─────────────────────────┬─────────────────────────────────────┬────────────────────────────────┐
│ Possible Cause          │ Diagnostic Check                    │ Remedy                         │
├─────────────────────────┼─────────────────────────────────────┼────────────────────────────────┤
│ Thermostat not calling  │ Check thermostat setting and mode   │ Set to COOL, temp below setpt  │
│ Tripped breaker         │ Check electrical disconnect and     │ Reset breaker; if trips again,  │
│                         │ panel breaker                       │ call service technician          │
│ Dirty filters           │ Check filter DP (>1.0 in.w.c.)     │ Replace filters                │
│ Frozen coil             │ Visual: ice on evaporator coil      │ Turn off cooling, run fan only  │
│                         │                                     │ to thaw; check charge           │
│ Low refrigerant         │ Check sight glass (bubbles = low)   │ Call service tech for charge    │
│ Compressor locked out   │ Check compressor contactor          │ Reset lockout; if repeats, call │
│ Failed capacitor        │ Compressor hums but won't start     │ Replace run/start capacitor    │
│ Economizer stuck open   │ Check outdoor air damper position   │ Manual override, call controls │
└─────────────────────────┴─────────────────────────────────────┴────────────────────────────────┘

SYMPTOM: High energy bills
┌─────────────────────────┬─────────────────────────────────────┬────────────────────────────────┐
│ Dirty coils             │ Visual: dust/debris on coils        │ Clean coils (annual PM)        │
│ Dirty filters           │ Check filter DP                     │ Replace filters                │
│ Incorrect setpoints     │ Check BAS schedule/setpoints        │ Verify occupied/unoccupied     │
│ Economizer not working  │ Damper stuck, sensor failed         │ Test economizer controls       │
│ Refrigerant overcharge  │ High head pressure                  │ Service tech to verify charge  │
└─────────────────────────┴─────────────────────────────────────┴────────────────────────────────┘
```

---

## EMERGENCY PROCEDURES

### Extraction Targets

| Data Point | Type | Example |
|-----------|------|---------|
| `system` | string | "Natural gas" |
| `emergency_type` | string | "Gas leak" |
| `immediate_actions` | array | ["Evacuate area", "Do NOT operate electrical switches", "Close main gas valve (yellow handle, Building NW corner)"] |
| `notification_sequence` | array | ["Call 911", "Call gas company: 1-800-XXX-XXXX", "Call building manager: (555) 123-4567"] |
| `gas_valve_location` | string | "Building NW corner, exterior, yellow handle" |
| `assembly_point` | string | "Parking lot, east side of building" |
| `re_entry_authority` | string | "Fire department clearance required" |

### Emergency Procedures to Extract

| System | Emergency Type | Key Extraction Points |
|--------|---------------|----------------------|
| **Gas** | Leak/odor | Main shutoff location, evacuation route, utility contact |
| **Electrical** | Fire/shock/outage | Main disconnect location, generator auto-start, ATS location |
| **Fire protection** | System activation | Sprinkler shutoff location, FDC location, fire panel location |
| **Plumbing** | Major leak/flood | Main water shutoff, floor drain locations, wet vacuum location |
| **HVAC** | Refrigerant release | Ventilation procedures, evacuation threshold (per ASHRAE 15) |
| **Elevator** | Entrapment | Emergency phone, manual lowering procedure, contact numbers |
| **Generator** | Failure during outage | Manual start procedure, fuel level check, load shedding priority |

---

## CONTROL SEQUENCES OF OPERATION

### Extraction Targets

| Data Point | Type | Example |
|-----------|------|---------|
| `system` | string | "RTU-1 HVAC" |
| `sequence_name` | string | "Occupied cooling sequence" |
| `trigger` | string | "Zone temp > cooling setpoint (74°F) AND occupied schedule" |
| `stages` | array | See below |
| `setpoints` | object | See below |
| `interlocks` | array | ["Supply fan must run before compressor", "Low temp cutout at 38°F supply air"] |

#### Setpoints Table

```
RTU-1 SETPOINTS

| Parameter | Occupied | Unoccupied | Override |
|-----------|----------|------------|---------|
| Cooling setpoint | 74°F | 82°F | 72°F (2hr max) |
| Heating setpoint | 70°F | 60°F | 72°F (2hr max) |
| Economizer enable | 55°F OAT | 55°F OAT | N/A |
| Economizer disable | 75°F OAT | 75°F OAT | N/A |
| Min outdoor air % | 20% | 0% | N/A |
| Supply air low limit | 52°F | 52°F | 52°F |
| Filter alarm DP | 1.0 in.w.c. | 1.0 in.w.c. | N/A |
| Occupied schedule | 6:00 AM | 9:00 PM | — |
```

### BMS/DDC Points List

| Point Name | Type | Range | Description |
|-----------|------|-------|-------------|
| RTU1_SAT | AI | 40-120°F | Supply air temperature |
| RTU1_RAT | AI | 50-100°F | Return air temperature |
| RTU1_OAT | AI | -20-120°F | Outdoor air temperature |
| RTU1_FDP | AI | 0-2.0 in.w.c. | Filter differential pressure |
| RTU1_SF_STS | DI | ON/OFF | Supply fan status |
| RTU1_CLG1 | DO | ON/OFF | Stage 1 cooling command |
| RTU1_CLG2 | DO | ON/OFF | Stage 2 cooling command |
| RTU1_HTG | DO | ON/OFF | Heating command |
| RTU1_ECON | AO | 0-100% | Economizer damper position |
| RTU1_OCC | DI | OCC/UNOCC | Occupancy mode |
| RTU1_ALARM | DI | NORMAL/ALARM | General alarm |

---

## OUTPUT MAPPING

### For equipment-data.json (or extend closeout tracking)

```json
{
  "equipment_inventory": [
    {
      "tag": "RTU-1",
      "name": "Rooftop Unit 1",
      "manufacturer": "Carrier",
      "model": "48XC-N14090",
      "serial_number": "3216F45892",
      "location": "Roof, Grid C-D/3-4",
      "serves": "East Wing, Level 1",
      "spec_section": "23 81 26",
      "install_date": "2026-05-15",
      "startup_date": "2026-06-20",
      "warranty": {
        "compressor": "5 years",
        "parts": "1 year",
        "labor": "1 year"
      },
      "operation": {
        "normal_setpoints": {
          "cooling": "74°F occupied / 82°F unoccupied",
          "heating": "70°F occupied / 60°F unoccupied"
        },
        "emergency_shutdown": "Disconnect at unit (red handle) + gas valve (yellow handle)"
      },
      "maintenance_schedule": [
        {"task": "Replace air filters", "interval": "quarterly", "parts": ["MERV 13 20×25×2 (qty 4)"]},
        {"task": "Check belt tension", "interval": "quarterly", "parts": []},
        {"task": "Clean condensate drain", "interval": "quarterly", "parts": []},
        {"task": "Lubricate bearings", "interval": "semi-annual", "parts": ["Mobilgrease XHP 222"]},
        {"task": "Clean coils", "interval": "annual", "parts": []},
        {"task": "Check refrigerant", "interval": "annual", "parts": []},
        {"task": "Full operational test", "interval": "annual", "parts": []}
      ],
      "critical_spare_parts": [
        {"part": "Fan belt", "pn": "Gates A68", "supplier": "Grainger", "qty_on_hand": 2},
        {"part": "Contactor", "pn": "Carrier P/N 50XC500089", "supplier": "Carrier dealer", "qty_on_hand": 1},
        {"part": "Capacitor", "pn": "45/5 MFD 440V", "supplier": "Grainger", "qty_on_hand": 1}
      ],
      "bms_points": [
        {"name": "RTU1_SAT", "type": "AI", "description": "Supply air temp"},
        {"name": "RTU1_RAT", "type": "AI", "description": "Return air temp"},
        {"name": "RTU1_SF_STS", "type": "DI", "description": "Supply fan status"}
      ]
    }
  ],
  "emergency_procedures": [
    {
      "system": "Natural gas",
      "type": "Gas leak",
      "actions": ["Evacuate", "Close main gas valve (NW corner)", "Call 911"],
      "shutoff_location": "Building NW corner, exterior, yellow handle"
    }
  ],
  "maintenance_calendar": {
    "quarterly": ["Replace RTU filters (all units)", "Clean condensate drains", "Exercise fire protection valves"],
    "semi_annual": ["Lubricate fan bearings", "Test transfer switch", "Flush water heaters"],
    "annual": ["Clean coils", "Generator load test", "Backflow preventer test", "Full electrical inspection"]
  }
}
```

---

## CROSS-REFERENCE RULES

| O&M Data | Cross-Reference Against | Purpose |
|----------|------------------------|---------|
| Equipment list | MEP equipment schedules in plans-spatial.json | Verify all equipment has O&M data |
| PM schedule | Warranty requirements (warranty-extraction.md) | Ensure PM meets warranty conditions |
| Parts list | Procurement-log.json | Source for replacement parts |
| Control sequences | TAB report (testing-commissioning) | Verify operating parameters match |
| Emergency procedures | Safety-log.json emergency plan | Align with site safety plan |
| BMS points | Controls commissioning data | Verify all points are functional |

---

## SUMMARY CHECKLIST — O&M EXTRACTION

**On Receipt of O&M Manual**:

- [ ] **Inventory all equipment** covered in the manual (tag, manufacturer, model, serial, location)
- [ ] **Extract operation procedures** for all major systems (start-up, shutdown, emergency)
- [ ] **Build PM schedule** table (interval, task, parts, time, skill level)
- [ ] **Extract parts lists** with part numbers, suppliers, substitutes, lead times
- [ ] **Build troubleshooting tables** (symptom → cause → remedy)
- [ ] **Extract emergency procedures** for all systems (gas, electrical, fire, plumbing, HVAC)
- [ ] **Extract control sequences** with setpoints and interlocks
- [ ] **Extract BMS points list** with types and descriptions
- [ ] **Cross-reference warranties** — verify PM requirements maintain warranty coverage
- [ ] **Generate spare parts inventory** recommendation
- [ ] **Generate maintenance calendar** from aggregated PM schedules
- [ ] **Store results** in equipment-data.json or closeout tracking
- [ ] **Verify completeness** — every specified equipment item has O&M documentation
