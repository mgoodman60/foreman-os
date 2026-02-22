# Warranty Documentation — Deep Extraction Guide

Extract structured data from warranty documents, certificates, and registration forms. Warranty documentation is critical for project closeout, owner turnover, and long-term building maintenance. This guide covers all warranty types encountered in construction: manufacturer equipment warranties, material warranties, workmanship warranties, roofing/waterproofing system warranties, and specialty performance guarantees.

---

## Extraction Priority Matrix

| Priority | Document Type | Use Case | Completeness Target |
|----------|--------------|----------|-------------------|
| **CRITICAL** | Roofing/waterproofing system warranties | Owner protection, long-duration coverage, maintenance requirements | 100% — all systems |
| **CRITICAL** | Major equipment warranties (HVAC, elevator, generator) | O&M planning, service scheduling, parts sourcing | 100% — all major equipment |
| **HIGH** | Manufacturer product warranties | Closeout documentation, defect claims | 100% — all specified products |
| **HIGH** | Workmanship/contractor warranties | GC obligation, defect coverage period | 100% — all trades |
| **HIGH** | Warranty registration deadlines | Time-sensitive — missing deadlines voids coverage | 100% |
| **MEDIUM** | Extended warranty options | Owner decision — cost vs. coverage | If provided |
| **MEDIUM** | Performance guarantees (energy, sound, leak-free) | Commissioning verification, performance testing | If specified |
| **LOW** | Implied warranties (statutory) | Legal reference | Note existence only |

---

## WARRANTY TERMS EXTRACTION

### Document Identification

**Signals this is a warranty document**:
- "WARRANTY", "GUARANTEE", or "CERTIFICATE OF WARRANTY" heading
- Duration language ("for a period of", "commencing on", "expiring on")
- Exclusions section ("This warranty does not cover...")
- Claim procedures or contact information
- Manufacturer or contractor signature/seal
- Registration forms or online portal references
- Bond or surety references (for performance warranties)

### Core Fields — Per Warranty

| Data Point | Type | Example | Notes |
|-----------|------|---------|-------|
| `warranty_id` | string | "WAR-001" | Internal tracking ID |
| `product_or_system` | string | "RTU-1 (Carrier 48XC-N14090)" | Equipment tag or product |
| `warranty_type` | string | "manufacturer_equipment" | See types below |
| `manufacturer` | string | "Carrier Corporation" | Warranty issuer |
| `installer` | string | "ABC Mechanical, Inc." | Installing contractor |
| `spec_section` | string | "23 81 26" | CSI section reference |
| `duration_years` | number | 5 | Warranty period |
| `duration_description` | string | "5-year compressor, 1-year parts and labor" | Full duration detail |
| `start_date_trigger` | string | "substantial_completion" | When warranty clock starts |
| `start_date` | string | "2026-08-15" | Actual start date (when known) |
| `expiration_date` | string | "2031-08-15" | Calculated end date |
| `coverage_scope` | string | "Compressor replacement due to manufacturing defect" | What's covered |
| `coverage_type` | string | "parts_only" / "parts_and_labor" / "full_replacement" | Level of coverage |
| `submittal_id` | string | "SUB-015" | Link to approved submittal |
| `procurement_id` | string | "PROC-023" | Link to procurement record |

### Warranty Types

| Type | Description | Typical Duration | Start Trigger |
|------|-------------|-----------------|---------------|
| `manufacturer_equipment` | Equipment manufacturer coverage | 1-10 years (varies by component) | Date of substantial completion |
| `manufacturer_material` | Material/product manufacturer | 1-25 years | Date of installation or substantial completion |
| `workmanship` | Contractor installation quality | 1-2 years | Substantial completion |
| `roofing_system` | Full roofing system (manufacturer + installer) | 10-30 years | Substantial completion |
| `waterproofing_system` | Below-grade or envelope waterproofing | 5-15 years | Substantial completion |
| `performance_guarantee` | Specific performance metric | 1-5 years | Commissioning completion |
| `extended` | Optional extended coverage (purchased) | Varies | End of standard warranty |

### Start Date Triggers

| Trigger | Definition | Notes |
|---------|-----------|-------|
| `substantial_completion` | Date of Certificate of Substantial Completion | Most common for building warranties |
| `installation_date` | Date product was installed | Some equipment warranties start on install |
| `commissioning_date` | Date system was commissioned and accepted | HVAC, controls, specialty systems |
| `occupancy_date` | Date building is occupied | Some owner-favorable warranties |
| `purchase_date` | Date product was purchased/shipped | Applies to some off-the-shelf products |
| `registration_date` | Date warranty was registered | Some warranties require registration to activate |

---

## EXCLUSIONS AND LIMITATIONS

### Extraction Targets

For each warranty, extract ALL exclusions — these define what the owner CANNOT claim under warranty.

| Data Point | Type | Example |
|-----------|------|---------|
| `exclusion_category` | string | "improper_maintenance" |
| `exclusion_description` | string | "Damage caused by failure to perform recommended maintenance per O&M manual" |
| `maintenance_requirement` | string | "Quarterly filter changes, annual coil cleaning" |
| `voiding_conditions` | array | ["Unauthorized modifications", "Use of non-approved parts", "Failure to register within 90 days"] |

### Common Exclusion Categories

| Category | Typical Language | Superintendent Action |
|----------|-----------------|----------------------|
| **Improper maintenance** | "Warranty void if maintenance schedule not followed" | Ensure O&M manual is delivered to owner with maintenance calendar |
| **Unauthorized modification** | "Warranty void if product is modified without written approval" | Document any field modifications with manufacturer approval |
| **Misuse or abuse** | "Warranty does not cover damage from misuse" | Document condition at turnover with photos |
| **Normal wear and tear** | "Normal wear items not covered" | List wear items (filters, belts, gaskets) separately |
| **Acts of God** | "Warranty excludes damage from natural disasters" | Note: owner's property insurance covers this |
| **Consequential damages** | "Manufacturer not liable for consequential damages" | Important limitation for owner to understand |
| **Failure to register** | "Warranty must be registered within 30/60/90 days" | **TRACK DEADLINE** — flag for immediate action |

---

## CLAIM PROCEDURES

### Extraction Targets

| Data Point | Type | Example |
|-----------|------|---------|
| `claim_contact_name` | string | "Carrier Warranty Claims Department" |
| `claim_phone` | string | "1-800-227-7437" |
| `claim_email` | string | "warranty@carrier.com" |
| `claim_portal_url` | string | "https://carrier.com/warranty-claims" |
| `required_documentation` | array | ["Serial number", "Date of installation", "Description of defect", "Photos", "Proof of maintenance"] |
| `response_timeframe` | string | "Within 10 business days of claim submission" |
| `dispute_resolution` | string | "Binding arbitration per AAA rules" |
| `authorized_service` | string | "Only authorized Carrier dealers may perform warranty repairs" |
| `owner_obligations` | string | "Owner must provide reasonable access for inspection" |

---

## REGISTRATION REQUIREMENTS

**This is time-critical — missing a registration deadline can void the warranty.**

### Extraction Targets

| Data Point | Type | Example |
|-----------|------|---------|
| `registration_required` | boolean | true |
| `registration_deadline` | string | "Within 30 days of substantial completion" |
| `registration_deadline_date` | string | "2026-09-14" | Calculated from start date |
| `registration_method` | string | "online" / "mail" / "email" |
| `registration_url` | string | "https://carrier.com/register" |
| `registration_form` | string | "Included in submittal package, Form WR-100" |
| `required_info` | array | ["Serial number", "Install date", "Installer name", "Owner name and address"] |
| `registration_status` | string | "pending" / "submitted" / "confirmed" |
| `confirmation_number` | string | "REG-2026-45892" |

### Registration Tracking Table

Generate this table from all extracted warranty registrations:

```
WARRANTY REGISTRATION TRACKER

| Item | Registration Deadline | Method | Status | Confirmation |
|------|---------------------|--------|--------|-------------|
| RTU-1 Carrier | 09/14/2026 | Online | Pending | — |
| RTU-2 Carrier | 09/14/2026 | Online | Pending | — |
| Roofing System (GAF) | 10/15/2026 | Mail | Pending | — |
| Generator (Generac) | 09/14/2026 | Online | Submitted | REG-89234 |
| Elevator (ThyssenKrupp) | 11/01/2026 | Email | Pending | — |
```

---

## PERFORMANCE GUARANTEES

### Extraction Targets

| Data Point | Type | Example |
|-----------|------|---------|
| `guarantee_type` | string | "leak_free" / "energy_performance" / "sound_rating" / "air_tightness" |
| `metric` | string | "No leaks for 5 years" |
| `measurement_method` | string | "Visual inspection after 1\" rainfall event" |
| `testing_protocol` | string | "ASTM E1105 field water test" |
| `threshold_value` | string | "EUI ≤ 45 kBTU/SF/year" |
| `verification_period` | string | "12 months of operational data" |
| `remedy_if_failed` | string | "Manufacturer repairs at no cost until metric is achieved" |
| `bond_amount` | string | "$50,000 performance bond" |

### Common Performance Guarantees in Construction

| System | Guarantee Type | Typical Metric | Duration |
|--------|---------------|----------------|----------|
| Roofing | Leak-free | No water penetration | 10-20 years |
| HVAC | Energy performance | EUI target | 1-3 years |
| Windows | Air infiltration | ≤ 0.06 CFM/SF at 1.57 PSF | Per spec |
| Acoustics | Sound rating | STC ≥ 50 between units | Per spec |
| Waterproofing | Leak-free below grade | No water intrusion | 5-15 years |
| Paving | Surface condition | No alligator cracking | 2-5 years |
| Concrete floors | Flatness/levelness | FF/FL per ACI 117 | At installation |

---

## ROOFING WARRANTY DEEP EXTRACTION

Roofing warranties are the most complex and valuable warranty documents on most projects. They involve both the manufacturer and the installer.

### Extraction Targets

| Data Point | Type | Example |
|-----------|------|---------|
| `roof_system` | string | "GAF TPO, 60 mil, fully adhered" |
| `manufacturer` | string | "GAF" |
| `warranty_type` | string | "NDL (No Dollar Limit)" / "Standard" / "System Plus" |
| `duration_years` | integer | 20 |
| `coverage_wind_speed_mph` | integer | 110 |
| `coverage_includes_labor` | boolean | true |
| `annual_inspection_required` | boolean | true |
| `inspection_by` | string | "GAF-certified inspector" |
| `maintenance_requirements` | array | ["Annual inspection", "Clear drains quarterly", "Remove ponding water within 48 hours"] |
| `installer_qualifications` | string | "GAF Master Elite contractor" |
| `warranty_number` | string | "GAF-WTY-2026-78234" |
| `prorated_after_year` | integer | 15 |
| `transferable` | boolean | true |
| `transfer_fee` | string | "$500" |

### Roofing Warranty Voiding Conditions

These are the most common reasons roofing warranties are voided — extract and flag:

1. **Unauthorized roof penetrations** — Any penetration not sealed by approved contractor
2. **Foot traffic damage** — Excessive or improper foot traffic without walk pads
3. **Failure to maintain drains** — Clogged roof drains causing ponding water
4. **Skipped annual inspections** — Manufacturer requires documented annual inspections
5. **Unauthorized repairs** — Repairs by non-certified contractors
6. **Alterations to rooftop equipment** — Adding or moving equipment without re-sealing
7. **Chemical exposure** — Kitchen exhaust grease, industrial chemicals
8. **Exceeding wind speed rating** — Damage during events exceeding rated wind speed

---

## OUTPUT MAPPING

### Primary Storage: quality-data.json → warranties

```json
{
  "warranties": [
    {
      "warranty_id": "WAR-001",
      "product_or_system": "RTU-1 (Carrier 48XC-N14090)",
      "warranty_type": "manufacturer_equipment",
      "manufacturer": "Carrier Corporation",
      "installer": "ABC Mechanical, Inc.",
      "spec_section": "23 81 26",
      "duration": {
        "compressor": "5 years",
        "parts": "1 year",
        "labor": "1 year"
      },
      "start_trigger": "substantial_completion",
      "start_date": null,
      "expiration_dates": {
        "compressor": null,
        "parts": null,
        "labor": null
      },
      "registration": {
        "required": true,
        "deadline_days": 30,
        "method": "online",
        "url": "https://carrier.com/register",
        "status": "pending"
      },
      "exclusions": ["improper_maintenance", "unauthorized_modification", "normal_wear"],
      "maintenance_requirements": ["Quarterly filter changes", "Annual coil cleaning", "Bi-annual refrigerant check"],
      "claim_contact": {
        "phone": "1-800-227-7437",
        "email": "warranty@carrier.com"
      },
      "linked_submittal": "SUB-015",
      "linked_procurement": "PROC-023"
    }
  ]
}
```

### Cross-References

| Warranty Data | Cross-Reference To | Purpose |
|--------------|-------------------|---------|
| Product/system | `procurement-log.json` → item | Link warranty to procurement record |
| Spec section | `specs-quality.json` → spec_sections | Verify warranty meets spec requirements |
| Installer | `directory.json` → subcontractors | Contact info for warranty service |
| Start date | `project-config.json` → substantial_completion | Calculate warranty expiration |
| Registration deadline | Morning brief alerts | Time-sensitive reminder |
| Maintenance requirements | O&M manual extraction | Cross-check maintenance schedule |

---

## CLOSEOUT INTEGRATION

### Warranty Closeout Checklist

Generate from extracted warranty data:

```
WARRANTY CLOSEOUT CHECKLIST

EQUIPMENT WARRANTIES:
- [ ] RTU-1 (Carrier): 5yr compressor / 1yr parts — Registered? ___
- [ ] RTU-2 (Carrier): 5yr compressor / 1yr parts — Registered? ___
- [ ] Generator (Generac): 5yr engine / 2yr controls — Registered? ___
- [ ] Elevator (ThyssenKrupp): 1yr full service — Registration N/A

SYSTEM WARRANTIES:
- [ ] Roofing (GAF TPO): 20yr NDL — Registration submitted? ___
- [ ] Waterproofing (Carlisle): 10yr — Registration submitted? ___
- [ ] Fire alarm (Honeywell): 3yr — Registration submitted? ___

MATERIAL WARRANTIES:
- [ ] Flooring (Armstrong LVT): 10yr commercial — On file? ___
- [ ] Paint (Sherwin-Williams): 5yr exterior / 1yr interior — On file? ___
- [ ] Windows (Andersen): 10yr glass / 20yr frame — Registered? ___

CONTRACTOR WARRANTIES:
- [ ] GC 1-year workmanship: Signed? ___
- [ ] Electrical sub: Signed? ___
- [ ] Mechanical sub: Signed? ___
- [ ] Plumbing sub: Signed? ___

TOTAL WARRANTIES: ___
REGISTERED: ___
PENDING: ___
MISSING: ___
```

---

## SUMMARY CHECKLIST — WARRANTY EXTRACTION

**On Receipt of Warranty Document**:

- [ ] **Identify warranty type** (equipment, material, workmanship, system, performance)
- [ ] **Extract all core fields** per tables above
- [ ] **Extract ALL exclusions** — these define claim boundaries
- [ ] **Extract registration requirements** — flag deadlines immediately
- [ ] **Extract maintenance requirements** — cross-reference with O&M manuals
- [ ] **Extract claim procedures** — contact info, required documentation
- [ ] **Calculate expiration dates** from start trigger + duration
- [ ] **Link to procurement** record in `procurement-log.json`
- [ ] **Link to submittal** record in `submittal-log.json`
- [ ] **Store in** `quality-data.json` → warranties array
- [ ] **Add registration deadline** to morning brief alerts
- [ ] **Generate closeout checklist** entry
