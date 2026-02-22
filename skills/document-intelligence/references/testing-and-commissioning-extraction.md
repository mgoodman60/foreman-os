# Testing & Commissioning Reports — Deep Extraction Guide

Extract structured data from building systems testing and commissioning documentation. These reports verify that installed systems perform to specification before the owner accepts the building. Covers HVAC TAB (Testing, Adjusting, and Balancing), fire protection testing, electrical testing, generator load testing, plumbing pressure testing, and building envelope testing.

---

## Extraction Priority Matrix

| Priority | Report Type | Use Case | Completeness Target |
|----------|-----------|----------|-------------------|
| **CRITICAL** | HVAC TAB reports | Comfort verification, energy performance, commissioning acceptance | 100% — every air/water device |
| **CRITICAL** | Fire protection test reports (hydrostatic, flow, alarm) | Code compliance, occupancy permit, life safety | 100% — all tests |
| **CRITICAL** | Electrical test reports (megger, ground fault, arc flash) | Safety compliance, insurance, permit closeout | 100% — all tested circuits |
| **HIGH** | Generator load test | Emergency power verification, code compliance | 100% — full test data |
| **HIGH** | Plumbing pressure tests | Code compliance, leak prevention, permit | 100% — all systems |
| **HIGH** | Building envelope tests (air/water) | Performance warranty, energy compliance | All tested areas |
| **MEDIUM** | Controls/BAS commissioning | Sequence verification, energy optimization | All sequences tested |
| **MEDIUM** | Elevator acceptance testing | Occupancy, safety, ADA compliance | All elevators |
| **LOW** | Low-voltage system tests (fire alarm, security, AV) | Functionality verification | System-level pass/fail |

---

## HVAC TAB REPORTS

### Document Identification

**Signals this is a TAB report**:
- TAB agency letterhead (AABC or NEBB certified)
- "Testing, Adjusting, and Balancing Report" heading
- Diffuser/grille CFM readings in tabular format
- Fan performance data (RPM, amps, static pressure)
- Instrument calibration certificates
- AABC or NEBB certification stamp
- Tolerance references (typically ±10% of design)

### Air Side — Diffuser/Register Readings

**EXTRACT EVERY DEVICE**:

| Data Point | Type | Example |
|-----------|------|---------|
| `device_tag` | string | "SD-101A" (Supply Diffuser, Room 101, device A) |
| `device_type` | string | "4-way supply diffuser" |
| `location` | string | "Room 101, ceiling" |
| `served_by` | string | "RTU-1, Branch B-3" |
| `design_cfm` | integer | 200 |
| `measured_cfm` | integer | 195 |
| `deviation_pct` | number | -2.5 |
| `within_tolerance` | boolean | true |
| `damper_position` | string | "75% open" |
| `throw_pattern` | string | "4-way, 8' throw" |
| `noise_observation` | string | "Acceptable" |
| `notes` | string | "" |

### Air Side — Fan Performance

| Data Point | Type | Example |
|-----------|------|---------|
| `equipment_tag` | string | "RTU-1" |
| `fan_type` | string | "Supply fan" |
| `design_cfm` | integer | 4000 |
| `measured_cfm` | integer | 3950 |
| `design_esp_inwc` | number | 1.5 |
| `measured_esp_inwc` | number | 1.45 |
| `fan_rpm` | integer | 850 |
| `motor_amps` | number | 12.4 |
| `motor_rated_amps` | number | 15.0 |
| `motor_hp` | number | 5.0 |
| `vfd_frequency_hz` | number | 55.2 |
| `belt_condition` | string | "New, proper tension" |
| `filter_dp_inwc` | number | 0.35 |
| `filter_type` | string | "MERV 13, 2\" pleated" |

### Air Side — Zone Balance Summary

| Data Point | Type | Example |
|-----------|------|---------|
| `zone_name` | string | "East Wing, Level 1" |
| `served_by` | string | "RTU-1" |
| `total_design_cfm` | integer | 4000 |
| `total_measured_cfm` | integer | 3950 |
| `supply_return_balance_pct` | number | 98.7 |
| `rooms_in_tolerance` | integer | 18 |
| `rooms_out_of_tolerance` | integer | 2 |
| `out_of_tolerance_rooms` | array | ["Room 107 (-15%, needs adjustment)", "Room 112 (+12%, damper too open)"] |

### Water Side (Hydronic Systems)

| Data Point | Type | Example |
|-----------|------|---------|
| `equipment_tag` | string | "CH-1" (Chiller) |
| `loop` | string | "Chilled water supply" |
| `design_gpm` | number | 120 |
| `measured_gpm` | number | 118 |
| `design_delta_t` | number | 10.0 |
| `measured_delta_t` | number | 9.5 |
| `supply_temp_f` | number | 44 |
| `return_temp_f` | number | 53.5 |
| `pump_head_ft` | number | 45 |
| `pump_amps` | number | 18.5 |

### TAB Acceptance Criteria

| Parameter | Tolerance | Action if Out |
|-----------|----------|---------------|
| Individual diffuser CFM | ±10% of design | Adjust damper, re-measure |
| Total system CFM | ±10% of design | Adjust fan speed or VFD |
| Supply/return balance | Within 5% | Adjust return grilles |
| Fan external static pressure | ±10% of design | Check duct system for restrictions |
| Motor amps | ≤ nameplate FLA | Investigate if over (overloaded) |
| Hydronic flow | ±10% of design | Adjust balance valves |
| Delta-T | ±2°F of design | Check coil performance |

### Red Flags

| Condition | Severity | Action |
|-----------|----------|--------|
| Device >15% below design CFM | **WARNING** | Duct obstruction or sizing issue — investigate |
| Motor amps > FLA | **CRITICAL** | Motor overloaded — reduce load or resize motor |
| Supply/return imbalance >10% | **WARNING** | Building pressurization issue |
| Fan at 100% speed, low CFM | **CRITICAL** | Major duct restriction or wrong fan |
| Noise complaints at diffuser | **FLAG** | Velocity too high — increase duct size or add damper |

---

## FIRE PROTECTION TEST REPORTS

### Hydrostatic Pressure Test

| Data Point | Type | Example |
|-----------|------|---------|
| `test_type` | string | "Hydrostatic pressure test" |
| `system` | string | "Wet sprinkler system, Zone 1" |
| `test_date` | string | "2026-06-15" |
| `test_pressure_psi` | integer | 200 |
| `duration_hours` | number | 2.0 |
| `pressure_drop_psi` | number | 0 |
| `result` | string | "PASS — no leaks, no pressure drop" |
| `witnessed_by` | string | "Fire Marshal, J. Williams" |
| `nfpa_reference` | string | "NFPA 13, Section 29.2" |
| `contractor` | string | "ABC Fire Protection, Inc." |

### Flow Test

| Data Point | Type | Example |
|-----------|------|---------|
| `test_type` | string | "Flow test at most remote head" |
| `system` | string | "Wet sprinkler system" |
| `static_pressure_psi` | integer | 85 |
| `residual_pressure_psi` | integer | 62 |
| `flow_gpm` | integer | 750 |
| `required_flow_gpm` | integer | 500 |
| `required_pressure_psi` | integer | 55 |
| `result` | string | "PASS — adequate pressure and flow" |
| `fire_pump_operated` | boolean | false |

### Fire Alarm Verification

| Data Point | Type | Example |
|-----------|------|---------|
| `test_type` | string | "Fire alarm acceptance test" |
| `panel_manufacturer` | string | "Honeywell Silent Knight" |
| `panel_model` | string | "SK-5820" |
| `total_devices` | integer | 142 |
| `devices_tested` | integer | 142 |
| `devices_passed` | integer | 140 |
| `devices_failed` | integer | 2 |
| `failed_devices` | array | ["SD-205 (smoke detector, Room 205 — sensitivity low)", "PULL-1 (pull station, stairwell — switch stuck)"] |
| `notification_devices_tested` | integer | 48 |
| `notification_all_pass` | boolean | true |
| `supervisory_signals_tested` | boolean | true |
| `monitoring_company` | string | "ADT" |
| `monitoring_verified` | boolean | true |

### FDC (Fire Department Connection) Inspection

| Data Point | Type | Example |
|-----------|------|---------|
| `fdc_location` | string | "East elevation, Grid E/1, 3' AFF" |
| `fdc_type` | string | "Storz connection, 5\"" |
| `fdc_accessible` | boolean | true |
| `signage_posted` | boolean | true |
| `caps_in_place` | boolean | true |
| `clapper_functional` | boolean | true |
| `fire_marshal_approved` | boolean | true |

---

## ELECTRICAL TEST REPORTS

### Megger / Insulation Resistance Testing

| Data Point | Type | Example |
|-----------|------|---------|
| `test_type` | string | "Insulation resistance (Megger)" |
| `circuit_id` | string | "MDP to Panel LP-1 feeder" |
| `conductor_size` | string | "4/0 AWG THWN" |
| `conduit` | string | "2\" EMT" |
| `test_voltage_vdc` | integer | 1000 |
| `phase_a_ground_mohm` | number | 850 |
| `phase_b_ground_mohm` | number | 920 |
| `phase_c_ground_mohm` | number | 880 |
| `phase_to_phase_mohm` | number | 1200 |
| `minimum_acceptable_mohm` | number | 100 |
| `result` | string | "PASS — all readings well above minimum" |
| `temperature_f` | integer | 72 |
| `humidity_pct` | integer | 45 |

### Ground Fault Testing

| Data Point | Type | Example |
|-----------|------|---------|
| `test_type` | string | "Ground fault protection trip test" |
| `device_location` | string | "Main switchboard GFP relay" |
| `rated_pickup_amps` | integer | 1200 |
| `test_current_amps` | integer | 1200 |
| `trip_time_seconds` | number | 0.18 |
| `required_trip_time` | string | "≤ 1.0 second per NEC 230.95" |
| `result` | string | "PASS" |
| `zones_tested` | integer | 3 |
| `all_zones_pass` | boolean | true |

### Arc Flash Labels

| Data Point | Type | Example |
|-----------|------|---------|
| `equipment` | string | "Main Distribution Panel MDP" |
| `incident_energy_cal_cm2` | number | 8.4 |
| `arc_flash_boundary_inches` | integer | 48 |
| `ppe_category` | integer | 2 |
| `ppe_required` | string | "Arc-rated face shield and clothing, minimum 8 cal/cm²" |
| `working_distance_inches` | integer | 18 |
| `label_posted` | boolean | true |
| `study_date` | string | "2026-05-20" |
| `study_by` | string | "PowerStudies, Inc." |

---

## GENERATOR LOAD TEST

### Extraction Targets

| Data Point | Type | Example |
|-----------|------|---------|
| `generator_tag` | string | "GEN-1" |
| `manufacturer` | string | "Generac" |
| `model` | string | "SD150" |
| `rated_kw` | integer | 150 |
| `fuel_type` | string | "Diesel" |
| `test_date` | string | "2026-07-10" |
| `test_type` | string | "4-hour load bank test per NFPA 110" |
| `ambient_temp_f` | integer | 85 |

#### Load Steps

| Load Step | % Load | kW | Voltage (A/B/C) | Amps (A/B/C) | Frequency Hz | Duration |
|-----------|--------|-----|-----------------|--------------|-------------|----------|
| 25% | 25 | 37.5 | 480/479/480 | 45/44/45 | 60.1 | 30 min |
| 50% | 50 | 75.0 | 479/478/479 | 90/89/90 | 60.0 | 30 min |
| 75% | 75 | 112.5 | 478/477/478 | 135/134/135 | 59.9 | 60 min |
| 100% | 100 | 150.0 | 477/476/477 | 180/179/180 | 59.8 | 120 min |

#### Additional Measurements

| Data Point | Type | Example |
|-----------|------|---------|
| `transfer_switch_time_seconds` | number | 8.5 |
| `required_transfer_time` | string | "≤ 10 seconds per NFPA 110" |
| `fuel_consumption_gph` | number | 10.8 |
| `fuel_tank_capacity_gal` | integer | 250 |
| `runtime_at_full_load_hours` | number | 23.1 |
| `coolant_temp_f` | integer | 195 |
| `oil_pressure_psi` | integer | 55 |
| `exhaust_temp_f` | integer | 850 |
| `battery_voltage` | number | 24.2 |
| `overall_result` | string | "PASS — all parameters within acceptable range" |

---

## PLUMBING PRESSURE TESTS

### Water System Test

| Data Point | Type | Example |
|-----------|------|---------|
| `system` | string | "Domestic cold water" |
| `test_pressure_psi` | integer | 150 |
| `working_pressure_psi` | integer | 65 |
| `test_duration_hours` | number | 2.0 |
| `pressure_loss_psi` | number | 0 |
| `result` | string | "PASS — no leaks, no pressure loss" |
| `test_medium` | string | "Water" |
| `inspector` | string | "Plumbing Inspector, City of Louisville" |
| `pipe_material` | string | "Type L copper, ProPress fittings" |

### DWV (Drain, Waste, Vent) Test

| Data Point | Type | Example |
|-----------|------|---------|
| `system` | string | "Sanitary DWV" |
| `test_type` | string | "Water test (10' head)" |
| `test_head_ft` | integer | 10 |
| `duration_minutes` | integer | 15 |
| `leaks_found` | integer | 0 |
| `result` | string | "PASS" |
| `pipe_material` | string | "Cast iron, no-hub couplings" |

### Backflow Preventer Test

| Data Point | Type | Example |
|-----------|------|---------|
| `device_tag` | string | "BFP-1" |
| `device_type` | string | "RPZ (Reduced Pressure Zone)" |
| `manufacturer` | string | "Watts" |
| `model` | string | "909RPDA" |
| `size` | string | "4\"" |
| `location` | string | "Mechanical room, Grid A/1" |
| `test_date` | string | "2026-06-20" |
| `check_valve_1_psid` | number | 12.5 |
| `check_valve_2_psid` | number | 3.2 |
| `relief_valve_opening_psid` | number | 2.0 |
| `result` | string | "PASS — all valves within range" |
| `certified_tester` | string | "Licensed Backflow Tester #BF-2345" |
| `next_test_due` | string | "2027-06-20" |

---

## BUILDING ENVELOPE TESTING

### Window/Curtain Wall Water Test (ASTM E1105)

| Data Point | Type | Example |
|-----------|------|---------|
| `test_type` | string | "ASTM E1105 field water test" |
| `location` | string | "East elevation, Grid E / 1-5, Level 1 windows" |
| `test_pressure_psf` | number | 6.24 |
| `spray_rate_gal_sf_hr` | number | 5.0 |
| `duration_minutes` | integer | 15 |
| `leaks_found` | integer | 0 |
| `result` | string | "PASS — no water penetration observed" |
| `weather_conditions` | string | "Calm, 72°F, no rain" |
| `warranty_requirement` | boolean | true |

### Air Infiltration Test (Blower Door)

| Data Point | Type | Example |
|-----------|------|---------|
| `test_type` | string | "Whole-building air leakage per ASTM E779" |
| `test_pressure_pa` | number | 75 |
| `cfm_at_test_pressure` | number | 4500 |
| `building_area_sf` | number | 15000 |
| `cfm_per_sf` | number | 0.30 |
| `spec_maximum_cfm_sf` | number | 0.40 |
| `result` | string | "PASS — 0.30 CFM/SF < 0.40 CFM/SF maximum" |
| `ach_50` | number | 3.2 |

---

## OUTPUT STRUCTURE

### For quality-data.json → system_tests

```json
{
  "system_tests": [
    {
      "id": "STEST-001",
      "test_type": "hvac_tab",
      "system": "RTU-1 air distribution",
      "test_date": "2026-07-01",
      "agency": "AABC Certified TAB Agency",
      "total_devices": 42,
      "devices_in_tolerance": 40,
      "devices_out_of_tolerance": 2,
      "overall_result": "CONDITIONAL — 2 devices require adjustment",
      "action_items": ["SD-107A: increase damper to 85%", "SD-112B: reduce damper to 60%"],
      "spec_section": "23 05 93"
    },
    {
      "id": "STEST-002",
      "test_type": "fire_protection_hydrostatic",
      "system": "Wet sprinkler, Zone 1",
      "test_date": "2026-06-15",
      "test_pressure_psi": 200,
      "duration_hours": 2,
      "result": "PASS",
      "witnessed_by": "Fire Marshal",
      "spec_section": "21 13 13",
      "nfpa_reference": "NFPA 13, Section 29.2"
    },
    {
      "id": "STEST-003",
      "test_type": "generator_load_test",
      "equipment": "GEN-1 (Generac SD150)",
      "test_date": "2026-07-10",
      "rated_kw": 150,
      "max_load_tested_kw": 150,
      "transfer_time_sec": 8.5,
      "result": "PASS",
      "runtime_hours": 4,
      "spec_section": "26 32 13",
      "nfpa_reference": "NFPA 110"
    }
  ]
}
```

---

## CROSS-REFERENCE RULES

| Test Type | Cross-Reference Against | Purpose |
|-----------|------------------------|---------|
| TAB readings | MEP equipment schedules (specs-quality.json) | Verify design CFM matches measured |
| TAB readings | Room schedule (plans-spatial.json) | Verify all rooms are balanced |
| Fire protection | Spec section 21 XX XX (specs-quality.json) | Verify test meets spec |
| Fire protection | Inspection-log.json | Link to required inspections |
| Electrical megger | Panel schedule (plans-spatial.json) | Verify all feeders tested |
| Generator | Emergency power spec (specs-quality.json) | Verify transfer time meets code |
| Plumbing pressure | Pipe schedule (plans-spatial.json) | Verify all systems tested |
| Backflow | Permit requirements | Annual re-test tracking |
| Envelope | Window specs (specs-quality.json) | Verify performance meets spec |

---

## COMMISSIONING CLOSEOUT INTEGRATION

### Commissioning Checklist Generation

From extracted test data, generate closeout status:

```
SYSTEMS TESTING & COMMISSIONING STATUS

HVAC:
- [x] RTU-1 TAB: PASS (40/42 devices, 2 adjusted)
- [x] RTU-2 TAB: PASS (38/38 devices)
- [ ] Exhaust fan verification: Pending
- [ ] Controls sequence testing: In progress (60%)

FIRE PROTECTION:
- [x] Hydrostatic test: PASS
- [x] Flow test: PASS
- [x] Alarm verification: CONDITIONAL (2 devices need repair)
- [x] FDC inspection: PASS

ELECTRICAL:
- [x] Megger testing: PASS (all feeders)
- [x] Ground fault testing: PASS (all zones)
- [x] Arc flash study: Complete, labels posted
- [x] Generator load test: PASS (4-hour test)

PLUMBING:
- [x] DCW pressure test: PASS
- [x] DHW pressure test: PASS
- [x] DWV test: PASS
- [x] Backflow preventer: PASS (annual test due 06/2027)

BUILDING ENVELOPE:
- [x] Window water test: PASS
- [ ] Roof water test: Scheduled 07/25
- [ ] Air infiltration: Scheduled 08/01

OVERALL: 16/20 tests complete (80%)
```

---

## SUMMARY CHECKLIST — TESTING & COMMISSIONING EXTRACTION

**On Receipt of Test Report**:

- [ ] **Identify test type** (TAB, fire, electrical, generator, plumbing, envelope)
- [ ] **Extract all data points** per the relevant section above
- [ ] **Compare against spec requirements** from `specs-quality.json`
- [ ] **Determine PASS/FAIL/CONDITIONAL** status
- [ ] **Extract action items** for any failing or conditional results
- [ ] **Store results** in `quality-data.json` → system_tests
- [ ] **Link to inspection-log** for code-required tests
- [ ] **Update closeout checklist** status
- [ ] **Track re-test dates** for conditional results
- [ ] **Verify witness signatures** for code-required tests (fire marshal, building official)
- [ ] **Cross-reference** equipment tags with MEP schedules
