# Material Testing Reports — Deep Extraction Guide

Extract structured, field-actionable data from material testing reports including concrete compression tests, steel mill certificates, soil compaction reports, and third-party inspection certifications. These documents verify that installed materials meet specification requirements and are critical for quality assurance, closeout documentation, and claims support.

---

## Extraction Priority Matrix

| Priority | Document Type | Use Case | Completeness Target |
|----------|--------------|----------|-------------------|
| **CRITICAL** | Concrete compression test reports (7/28-day) | Strength acceptance, form removal decisions, spec compliance | 100% — every test set |
| **CRITICAL** | Soil compaction test reports | Subgrade acceptance, backfill verification, foundation bearing | 100% — every test |
| **CRITICAL** | Steel mill certificates (MTRs) | Structural steel verification, welding compatibility, traceability | 100% — every heat lot |
| **HIGH** | Third-party inspection certificates | Code compliance, special inspection sign-off, permit closeout | 100% — every inspection |
| **HIGH** | Welding inspection reports | Structural connection quality, certified welder verification | 100% — all CJP/PJP welds |
| **HIGH** | Concrete batch/delivery tickets | Load verification, placement tracking, QC chain-of-custody | All tickets for flagged loads |
| **MEDIUM** | Aggregate gradation reports | Concrete mix constituent verification | Per source change |
| **MEDIUM** | Fireproofing thickness reports | UL assembly compliance, fire rating verification | Per area |
| **MEDIUM** | Masonry prism/mortar test reports | Masonry strength verification, f'm compliance | Per test series |
| **LOW** | Paint/coating thickness reports | Finish quality verification | Per area |

---

## CONCRETE COMPRESSION TEST REPORTS

### Document Identification

**Signals this is a concrete test report**:
- Testing laboratory letterhead (typically ACI-certified lab)
- "Compressive Strength Test Report" or "Concrete Cylinder Test Report" heading
- ASTM C39 reference (standard test for compressive strength)
- Cylinder specimen data: date cast, date tested, age at test, break strength
- Project name and mix design reference
- Batch/ticket numbers cross-referencing delivery tickets

### Extraction Targets — Per Test Set

| Data Point | Type | Example | Notes |
|-----------|------|---------|-------|
| `lab_name` | string | "Smith Testing Lab, ACI Certified" | Verify lab is accredited |
| `lab_report_number` | string | "CTR-2026-0142" | Unique traceability ID |
| `project_name` | string | "One Senior Care" | Cross-reference project-config |
| `mix_id` | string | "4000-1" | Must match specs-quality.json mix_designs |
| `spec_section` | string | "03 30 00" | CSI section governing concrete |
| `placement_date` | string | "2026-02-15" | When concrete was placed |
| `placement_location` | string | "Footings, Grid C-D / 3-4" | Cross-reference plans-spatial |
| `batch_ticket_number` | string | "RTM-002841" | Delivery ticket for traceability |
| `supplier` | string | "Ready Mix Company" | Cross-reference directory |
| `volume_cy` | number | 8.5 | Cubic yards for this placement |

#### Cylinder Data (per specimen)

| Data Point | Type | Example |
|-----------|------|---------|
| `specimen_id` | string | "TB-4000-F15-01a" |
| `date_cast` | string | "2026-02-15" |
| `date_tested` | string | "2026-02-22" (7-day) or "2026-03-15" (28-day) |
| `age_days` | integer | 7 or 28 |
| `cure_method` | string | "Standard (72°F moist room)" or "Field cure" |
| `diameter_inches` | number | 4.0 |
| `height_inches` | number | 8.0 |
| `break_load_lbs` | number | 35,800 |
| `compressive_strength_psi` | integer | 2850 |
| `fracture_type` | string | "Type 3 (columnar)" |
| `notes` | string | "Normal fracture pattern" |

#### Calculated/Derived Fields

| Data Point | Calculation | Example |
|-----------|------------|---------|
| `set_average_psi` | Average of all cylinders at same age | 2850 |
| `design_fc_psi` | From mix design (specs-quality.json) | 4000 |
| `percent_of_design` | (set_average / design_fc) × 100 | 71.3% |
| `spec_compliance` | set_average >= design_fc at 28 days | true/false |
| `predicted_28day` | 7-day result / 0.65 (Type I) or / 0.75 (Type III) | ~4385 PSI |
| `strength_trend` | Compared to previous same-mix tests | "consistent" / "declining" / "improving" |

### Acceptance Criteria

**28-Day Acceptance (ACI 318)**:
- Average of any 3 consecutive tests >= f'c
- No individual test < f'c - 500 PSI
- If either fails → investigate: core testing, load testing, or structural analysis

**7-Day Indicators**:
- Type I cement: 7-day ≈ 60-70% of 28-day
- Type III cement: 7-day ≈ 70-80% of 28-day
- If 7-day is below 55% of design f'c → flag for early warning

### Red Flags

| Condition | Severity | Action |
|-----------|----------|--------|
| 28-day strength < design f'c | **CRITICAL** | Notify engineer, potential structural concern |
| 28-day strength < f'c - 500 PSI | **CRITICAL** | Core testing required per ACI 318 |
| 7-day < 55% of design f'c | **WARNING** | Early warning — monitor closely, consider heating |
| Strength declining over sequential tests | **WARNING** | Investigate: batch plant issue, aggregate change |
| Fracture type abnormal (Type 5/6) | **FLAG** | Specimen preparation issue — may not represent actual concrete |
| Test age > 35 days for "28-day" test | **FLAG** | Late testing — results may be higher than actual 28-day |
| Cure method mismatch (field vs standard) | **NOTE** | Field cure results will be lower — compare to standard cure |

### Output Mapping

Results are stored in two locations:

**`quality-data.json` → test records**:
```json
{
  "test_type": "concrete_compression",
  "lab_report_number": "CTR-2026-0142",
  "mix_id": "4000-1",
  "placement_date": "2026-02-15",
  "placement_location": "Footings, Grid C-D / 3-4",
  "batch_ticket": "RTM-002841",
  "age_days": 28,
  "set_average_psi": 4120,
  "design_fc_psi": 4000,
  "spec_compliance": true,
  "specimens": [
    {"id": "TB-4000-F15-01a", "strength_psi": 4180, "fracture_type": "Type 3"},
    {"id": "TB-4000-F15-01b", "strength_psi": 4060, "fracture_type": "Type 3"}
  ],
  "notes": "Exceeds design f'c by 120 PSI. Normal fracture patterns."
}
```

**Cross-reference to `procurement-log.json`**: Update `cert_status` for the concrete supplier from "pending" to "verified" once 28-day tests pass.

---

## STEEL MILL CERTIFICATES (MTRs)

### Document Identification

**Signals this is a mill certificate / Material Test Report**:
- Steel mill or distributor letterhead (Nucor, ArcelorMittal, SSAB, Gerdau)
- "Certified Mill Test Report" or "Certificate of Compliance" heading
- ASTM standard references (A36, A572, A992, A500, A615)
- Heat lot / heat number identification
- Chemical composition analysis table
- Mechanical property test results (yield, tensile, elongation)

### Extraction Targets — Per Heat Lot

| Data Point | Type | Example | Notes |
|-----------|------|---------|-------|
| `mill_name` | string | "Nucor Steel Birmingham" | Steel producer |
| `certificate_number` | string | "MTR-2026-N-45892" | Unique certificate ID |
| `heat_number` | string | "H-283945" | Heat lot traceability (critical) |
| `product_form` | string | "Wide Flange" | Shape category |
| `size` | string | "W12×26" | Specific member size |
| `grade` | string | "ASTM A992 Grade 50" | Steel grade specification |
| `length` | string | "40'-0\"" | As-rolled or cut length |
| `quantity` | string | "12 pieces" | Number of pieces in this heat |
| `weight_lbs` | number | 12480 | Total weight shipped |
| `date_rolled` | string | "2026-01-05" | Mill production date |
| `date_shipped` | string | "2026-01-12" | Ship date from mill |

#### Chemical Composition (Weight Percent)

| Element | Symbol | Typical Limit (A992) | Example Value |
|---------|--------|---------------------|---------------|
| Carbon | C | ≤ 0.23% | 0.08% |
| Manganese | Mn | 0.50-1.60% | 1.22% |
| Phosphorus | P | ≤ 0.035% | 0.012% |
| Sulfur | S | ≤ 0.045% | 0.008% |
| Silicon | Si | 0.15-0.40% | 0.22% |
| Copper | Cu | ≤ 0.60% | 0.25% |
| Nickel | Ni | ≤ 0.45% | 0.08% |
| Chromium | Cr | ≤ 0.35% | 0.05% |
| Molybdenum | Mo | ≤ 0.15% | 0.03% |
| Vanadium | V | ≤ 0.15% | 0.04% |
| Carbon Equivalent | CE | ≤ 0.47% | 0.38% |

**Carbon Equivalent (CE)** is critical for weldability:
- CE ≤ 0.40% = excellent weldability, no preheat needed
- CE 0.40-0.47% = good weldability, preheat may be needed for thick sections
- CE > 0.47% = poor weldability, preheat required, special procedures needed

#### Mechanical Properties

| Property | Unit | A992 Requirement | Example |
|----------|------|-----------------|---------|
| Yield strength (Fy) | ksi | 50-65 ksi | 54.5 ksi |
| Tensile strength (Fu) | ksi | ≥ 65 ksi | 71.0 ksi |
| Yield/Tensile ratio | ratio | ≤ 0.85 | 0.77 |
| Elongation (8") | % | ≥ 18% | 24% |
| Elongation (2") | % | ≥ 21% | 31% |

### Red Flags

| Condition | Severity | Action |
|-----------|----------|--------|
| Yield strength outside spec range | **CRITICAL** | Reject — engineer review required |
| Carbon equivalent > 0.47% | **WARNING** | Weldability concern — special welding procedures |
| Elongation below minimum | **CRITICAL** | Ductility concern — engineer review |
| Yield/tensile ratio > 0.85 | **WARNING** | Seismic concern — limited strain hardening |
| Missing heat number | **CRITICAL** | No traceability — unacceptable |
| Chemical composition out of range | **WARNING** | Review against spec; may require waiver |

### Rebar Mill Certificates (ASTM A615)

Additional fields for reinforcing steel:
- **Bar size**: #3 through #11 (and #14, #18)
- **Grade**: Grade 60 (Fy = 60 ksi) or Grade 80
- **Deformation pattern**: Confirm meets ASTM requirements
- **Bend test**: Pass/fail for specified bar size
- **Bundle tag number**: For field traceability

### Output Mapping

```json
{
  "test_type": "mill_certificate",
  "certificate_number": "MTR-2026-N-45892",
  "heat_number": "H-283945",
  "mill": "Nucor Steel Birmingham",
  "product": "W12×26",
  "grade": "A992 Grade 50",
  "yield_ksi": 54.5,
  "tensile_ksi": 71.0,
  "elongation_pct": 24,
  "carbon_equivalent": 0.38,
  "weldability": "excellent",
  "spec_compliance": true,
  "quantity_pieces": 12,
  "weight_lbs": 12480,
  "date_rolled": "2026-01-05"
}
```

Store in `quality-data.json` → test records. Update `procurement-log.json` → `cert_status` = "verified" for associated steel delivery.

---

## SOIL COMPACTION TEST REPORTS

### Document Identification

**Signals this is a compaction report**:
- Geotechnical testing lab letterhead
- "Compaction Test Report" or "Field Density Test Report" heading
- ASTM D1556 (sand cone), D6938 (nuclear gauge), or D2922 references
- Proctor reference (standard or modified)
- Percent compaction values
- Test location descriptions with station/offset or grid references

### Extraction Targets — Per Test

| Data Point | Type | Example | Notes |
|-----------|------|---------|-------|
| `lab_name` | string | "Terracon Consultants" | Testing agency |
| `report_number` | string | "FDT-2026-089" | Unique report ID |
| `test_date` | string | "2026-02-18" | Date of field test |
| `test_method` | string | "ASTM D6938 (Nuclear Gauge)" | Or D1556 (Sand Cone) |
| `test_location` | string | "Building pad, Grid B-C / 2-3" | Cross-reference plans-spatial |
| `elevation_or_depth` | string | "6\" below FFE" or "Lift 3 of 5" | Vertical position |
| `material_type` | string | "Structural fill (crushed limestone)" | Fill material description |
| `proctor_reference` | string | "Modified Proctor (ASTM D1557)" | Basis for percent compaction |
| `max_dry_density_pcf` | number | 132.5 | Lab-determined maximum density |
| `optimum_moisture_pct` | number | 10.2 | Lab-determined optimal moisture |
| `field_dry_density_pcf` | number | 128.8 | Measured in-situ density |
| `field_moisture_pct` | number | 9.8 | Measured in-situ moisture |
| `percent_compaction` | number | 97.2 | (field_dry / max_dry) × 100 |
| `spec_requirement_pct` | number | 95.0 | Specification minimum |
| `result` | string | "PASS" | PASS or FAIL |
| `tested_by` | string | "J. Martinez, NICET III" | Technician name/cert |

### Acceptance Criteria

| Area Type | Typical Spec | Notes |
|-----------|-------------|-------|
| Building pad / under slab | 95% modified proctor | Most common requirement |
| Under footings | 95-98% modified proctor | Higher for structural bearing |
| Parking lot / roads | 95% modified proctor | Subgrade and base |
| Trench backfill | 90-95% standard proctor | May be lower for non-structural |
| Landscape areas | 85-90% standard proctor | Least critical |

### Red Flags

| Condition | Severity | Action |
|-----------|----------|--------|
| Percent compaction < spec | **FAIL** | Remove and replace or re-compact and re-test |
| Moisture > optimum + 3% | **WARNING** | Soil too wet — may need to dry or add stabilizer |
| Moisture < optimum - 3% | **WARNING** | Soil too dry — add moisture and re-compact |
| Test location gaps | **FLAG** | Ensure all areas are tested per spec frequency |
| Different material than approved | **CRITICAL** | Unapproved fill source — stop work, get approval |
| Lift thickness > spec maximum | **WARNING** | May not achieve compaction — re-evaluate |

### Output Mapping

```json
{
  "test_type": "soil_compaction",
  "report_number": "FDT-2026-089",
  "test_date": "2026-02-18",
  "test_method": "ASTM D6938 (Nuclear Gauge)",
  "location": "Building pad, Grid B-C / 2-3",
  "depth_or_lift": "Lift 3 of 5",
  "material": "Structural fill (crushed limestone)",
  "percent_compaction": 97.2,
  "spec_requirement": 95.0,
  "moisture_pct": 9.8,
  "optimum_moisture": 10.2,
  "result": "PASS",
  "tested_by": "J. Martinez, NICET III"
}
```

Store in `quality-data.json` → test records. Cross-reference with `specs-quality.json` → `geotechnical.fill_requirements` for spec compliance.

---

## THIRD-PARTY INSPECTION CERTIFICATES

### Document Identification

**Signals this is a third-party inspection certificate**:
- Special inspection agency letterhead
- IBC Chapter 17 references (Special Inspections)
- Inspector certification references (ICC, AWS, ACI)
- Inspection type and scope identification
- Pass/fail/conditional determination
- Signed by certified inspector with credential numbers

### Extraction Targets — Per Inspection

| Data Point | Type | Example |
|-----------|------|---------|
| `agency_name` | string | "Quality Assurance Inspections, Inc." |
| `inspector_name` | string | "Robert Chen, ICC SI" |
| `inspector_cert_number` | string | "ICC-8892341" |
| `inspector_cert_type` | string | "ICC Structural Steel and Bolting" |
| `report_number` | string | "SI-2026-0234" |
| `inspection_date` | string | "2026-02-20" |
| `inspection_type` | string | "Structural Steel Bolting" |
| `ibc_reference` | string | "IBC 1705.2.1" |
| `location` | string | "Level 1, Grid A-D / 1-5" |
| `scope` | string | "Verify bolt pretension, snug-tight connections" |
| `result` | string | "PASS" / "FAIL" / "CONDITIONAL" |
| `conditions` | string | "3 connections require re-torque, see notes" |
| `linked_hold_point` | string | "HP-012" |
| `linked_spec_section` | string | "05 12 23" |
| `associated_po` | string | "PO-2026-045" |
| `associated_delivery` | string | "PROC-023" |

### Common Inspection Types

| Inspection Type | Standard | Typical Frequency |
|----------------|----------|-------------------|
| Concrete placement | ACI 318 | Per placement (hold point) |
| Structural steel bolting | AISC 360 | Per connection type |
| Structural welding | AWS D1.1 | Per CJP/PJP weld |
| High-strength bolting | RCSC Spec | Per connection |
| Masonry | TMS 402/602 | Per lift/grout pour |
| Fireproofing | UL assembly | Per area |
| Spray foam | IBC 2603 | Per application |
| Pile installation | Per geotech | Per pile |
| Concrete reinforcement | ACI 318 | Pre-pour (hold point) |
| Post-tensioning | PTI specs | Pre-stress/post-stress |
| Special soil/fill | Per geotech | Per spec frequency |

### Red Flags

| Condition | Severity | Action |
|-----------|----------|--------|
| FAIL result | **CRITICAL** | Stop work in affected area until corrected and re-inspected |
| CONDITIONAL with open items | **WARNING** | Track conditions to closure before covering work |
| Inspector cert expired | **CRITICAL** | Inspection may be invalid — verify with jurisdiction |
| Missing inspection for hold point | **CRITICAL** | Work cannot proceed — schedule inspection |
| Scope doesn't match hold point | **FLAG** | Ensure inspection covers all required items |

### Output Mapping

```json
{
  "test_type": "third_party_inspection",
  "report_number": "SI-2026-0234",
  "inspection_type": "Structural Steel Bolting",
  "inspector": "Robert Chen, ICC SI",
  "cert_number": "ICC-8892341",
  "date": "2026-02-20",
  "location": "Level 1, Grid A-D / 1-5",
  "result": "PASS",
  "linked_hold_point": "HP-012",
  "linked_spec_section": "05 12 23"
}
```

Store in `quality-data.json` → inspections array. Update `inspection-log.json` → link to hold point status.

---

## WELDING INSPECTION REPORTS

### Extraction Targets

| Data Point | Type | Example |
|-----------|------|---------|
| `inspector_name` | string | "Maria Lopez, CWI" |
| `aws_cert_number` | string | "AWS-CWI-19089445" |
| `wps_number` | string | "WPS-001" (Welding Procedure Specification) |
| `welder_id` | string | "W-12" (certified welder identification) |
| `joint_type` | string | "CJP (Complete Joint Penetration)" |
| `weld_location` | string | "Beam-to-column moment connection, Grid C/3" |
| `base_metal_grade` | string | "A992 Grade 50" |
| `filler_metal` | string | "E70XX" |
| `preheat_temp_f` | integer | 150 |
| `interpass_temp_f` | integer | 550 |
| `visual_inspection` | string | "PASS" |
| `ndt_method` | string | "UT (Ultrasonic Testing)" |
| `ndt_result` | string | "PASS — no rejectable indications" |
| `date` | string | "2026-02-19" |

### NDT Method Reference

| Method | Abbreviation | Use Case |
|--------|-------------|----------|
| Visual (VT) | VT | All welds — mandatory first inspection |
| Ultrasonic (UT) | UT | CJP welds, thick sections — most common NDT |
| Magnetic Particle (MT) | MT | Surface/near-surface cracks — fillet welds |
| Radiographic (RT) | RT | CJP welds, critical connections — less common on-site |
| Penetrant (PT) | PT | Surface cracks on non-ferromagnetic materials |

---

## BATCH/DELIVERY TICKET EXTRACTION

### When to Extract

Extract concrete delivery (batch) tickets when:
- A concrete test fails and traceability is needed
- Claims documentation requires detailed load records
- QC audit requires verification of mix ID vs. placement location

### Extraction Targets

| Data Point | Type | Example |
|-----------|------|---------|
| `ticket_number` | string | "RTM-002841" |
| `date` | string | "2026-02-15" |
| `time_batched` | string | "07:45 AM" |
| `time_arrived` | string | "08:15 AM" |
| `transit_minutes` | integer | 30 |
| `truck_number` | string | "T-14" |
| `mix_id` | string | "4000-1" |
| `volume_cy` | number | 8.5 |
| `water_added_site_gal` | number | 0 |
| `slump_at_plant` | number | 5.5 |
| `slump_at_site` | number | 5.0 |
| `air_content` | number | 5.5 |
| `concrete_temp_f` | integer | 72 |
| `ambient_temp_f` | integer | 65 |
| `revolutions_at_discharge` | integer | 78 |
| `total_revolutions` | integer | 210 |

**Red Flag**: If `water_added_site_gal` > 0, the w/c ratio has changed. Verify with supplier and flag for engineer if above maximum.

**Red Flag**: If `total_revolutions` > 300, concrete may be over-mixed. ASTM C94 limit.

---

## CROSS-REFERENCE RULES

| Test Report Type | Cross-Reference Against | Validation |
|-----------------|------------------------|------------|
| Concrete 28-day break | `specs-quality.json` mix_designs → design_fc | strength >= design_fc |
| Concrete 28-day break | `procurement-log.json` → supplier cert_status | Update to "verified" on pass |
| Soil compaction | `specs-quality.json` geotechnical → fill_requirements | % compaction >= spec |
| Mill certificate | `specs-quality.json` spec_sections → steel grade requirements | Grade matches spec |
| Mill certificate | `procurement-log.json` → steel delivery cert_status | Update on verification |
| Third-party inspection | `inspection-log.json` → hold point status | Update result |
| Third-party inspection | `specs-quality.json` → hold_points | Verify scope matches |
| Welding inspection | Shop drawing connection details | Verify WPS matches joint type |
| Batch ticket | `daily-report-data.json` → concrete placements | Cross-reference load data |

---

## OUTPUT STRUCTURE

### For quality-data.json → test_results

```json
{
  "test_results": [
    {
      "id": "TEST-001",
      "test_type": "concrete_compression",
      "lab_report_number": "CTR-2026-0142",
      "test_date": "2026-03-15",
      "mix_id": "4000-1",
      "spec_section": "03 30 00",
      "placement_date": "2026-02-15",
      "placement_location": "Footings, Grid C-D / 3-4",
      "age_days": 28,
      "result_value": 4120,
      "result_unit": "PSI",
      "spec_requirement": 4000,
      "spec_compliance": true,
      "specimens": [],
      "notes": ""
    },
    {
      "id": "TEST-002",
      "test_type": "soil_compaction",
      "lab_report_number": "FDT-2026-089",
      "test_date": "2026-02-18",
      "test_method": "ASTM D6938",
      "location": "Building pad, Grid B-C / 2-3",
      "result_value": 97.2,
      "result_unit": "percent_compaction",
      "spec_requirement": 95.0,
      "spec_compliance": true,
      "material": "Structural fill",
      "notes": ""
    },
    {
      "id": "TEST-003",
      "test_type": "mill_certificate",
      "certificate_number": "MTR-2026-N-45892",
      "heat_number": "H-283945",
      "product": "W12×26",
      "grade": "A992 Grade 50",
      "yield_ksi": 54.5,
      "tensile_ksi": 71.0,
      "elongation_pct": 24,
      "carbon_equivalent": 0.38,
      "spec_compliance": true,
      "notes": ""
    }
  ]
}
```

---

## SUMMARY CHECKLIST — MATERIAL TEST REPORT EXTRACTION

**On Receipt of Any Test Report**:

- [ ] **Identify report type** (concrete, soil, steel, third-party, welding)
- [ ] **Extract all data points** per the relevant section above
- [ ] **Cross-reference spec requirements** from `specs-quality.json`
- [ ] **Determine PASS/FAIL** against specification criteria
- [ ] **Flag any red conditions** per the red flags tables
- [ ] **Store results** in `quality-data.json` test records
- [ ] **Update procurement status** in `procurement-log.json` cert_status
- [ ] **Link to inspections** in `inspection-log.json` if hold point related
- [ ] **Alert superintendent** if any FAIL or CRITICAL condition detected
- [ ] **Track trends** — compare against previous tests for same mix/material

**For Closeout**:

- [ ] All concrete 28-day tests pass
- [ ] All steel MTRs on file and verified
- [ ] All compaction tests pass in all areas
- [ ] All special inspections signed off
- [ ] All hold point inspections have passing results
- [ ] Test report binder organized by CSI division
