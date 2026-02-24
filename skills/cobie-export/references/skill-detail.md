# cobie-export — Detailed Reference



Extended documentation, examples, templates, and detailed criteria for the cobie-export skill.



## 2. COBie Standard Reference

### Standards and Versions

- **Primary Reference**: NBIMS-US v3.0 / COBie v2.4 (publicly available via buildingSMART)
- **Secondary Reference**: BS 1192-4:2014 (UK BIM protocol including COBie)
- **Healthcare Supplement**: AACN guidelines and CMS documentation requirements
- **Data Quality Targets**: Level 2-3 (see data completeness section)

### 18 Standard Worksheets

The COBie export workbook contains exactly 18 worksheets (tabs) in this order:

| # | Worksheet | Purpose | Primary Data Source |
|---|-----------|---------|---------------------|
| 1 | Contact | Project team contact directory | directory.json |
| 2 | Facility | Building identification and metadata | project-config.json |
| 3 | Floor | Floor/level definitions and area data | plans-spatial.json |
| 4 | Space | Room and space inventory with area/finishes | plans-spatial.json + room schedule |
| 5 | Zone | Functional groupings (HVAC, fire, departments) | plans-spatial.json + specs-quality.json |
| 6 | Type | Asset type catalog with specs and make/model | specs-quality.json + submittals |
| 7 | Component | Individual asset instances with serial numbers | specs-quality.json + closeout data |
| 8 | System | Building systems and their scope | specs-quality.json |
| 9 | Assembly | Asset assemblies and sub-system groupings | specs-quality.json |
| 10 | Connection | System connections and relationships | specs-quality.json + coordination |
| 11 | Spare | Spare parts inventory and specifications | submittal O&M data |
| 12 | Resource | Maintenance materials and tools | submittal product data sheets |
| 13 | Job | Maintenance tasks and schedules | specs-quality.json + manuals |
| 14 | Impact | Environmental and economic impact data | specs-quality.json + sustainability |
| 15 | Document | References to submittals, O&M manuals, warranties | document-intelligence + submittal log |
| 16 | Attribute | Extended properties and custom fields | all data sources |
| 17 | Coordinate | Location coordinates (grid references) | plans-spatial.json (X/Y/Z grids) |
| 18 | Issue | Known issues, punch list items, deficiencies | punch-list.json + RFI log |

### Data Integrity Requirements

- **Primary Key Uniqueness**: Each worksheet has a unique identifier (e.g., Contact-Email, Facility-ProjectID, Component-Name)
- **Referential Integrity**: Foreign key references must exist (e.g., Component.Space references Space.Name)
- **Field Format**: All fields follow COBie data type specifications (text, date, URL, number, boolean)
- **Null Handling**: Missing data marked as "n/a" or left blank per field requirements
- **Encoding**: All text UTF-8, all dates ISO 8601 format (YYYY-MM-DD)

---



## 3. All 18 COBie Worksheets: Detailed Field Mappings

### 3.1 Contact Worksheet

**Purpose**: Directory of all project participants including GC, subcontractors, suppliers, architects, engineers, and facility operators.

**Source Data**: directory.json (extracted from project org chart)

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| Email | Y (PK) | directory.contact-email | Email address | andrew.eberle@wprinciples.com |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Category | Y | directory.role-category | Enum: GC / Sub / Supplier / Architect / Engineer / Owner / Consultant / Facility | GC |
| Company | Y | directory.company-name | Text | {gc_company} |
| Phone | N | directory.phone | Phone number | +1-859-555-0142 |
| Department | N | directory.department | Text | Construction Management |
| OrganizationCode | N | directory.org-code | Text | WP-{building_code} |
| GivenName | Y | directory.first-name | Text | Andrew |
| FamilyName | Y | directory.last-name | Text | Eberle |
| MiddleInitials | N | directory.middle-initials | Text (max 3) | J |
| ContactType | Y | directory.contact-type | Enum: Individual / Company | Individual |

**Mapping Logic**:

```json
{
  "Email": "directory[].contact-email",
  "Company": "directory[].company-name",
  "GivenName": "directory[].first-name",
  "FamilyName": "directory[].last-name",
  "Phone": "directory[].phone || 'n/a'",
  "Category": "directory[].role-category",
  "Department": "directory[].department || 'n/a'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

**Example Rows**:
- **{superintendent_name}** (Super, {gc_company}) | GC | {phone}
- **{pm_name}** (PM, {gc_company}) | GC | {phone}
- **{earthwork_sub}** (Earthwork/Excavation) | Sub | {phone}
- **{structural_sub}** (Structural Steel/Erection) | Sub | {phone}
- **{hvac_sub}** (HVAC/Mechanical) | Sub | {phone}
- **{framing_sub}** (Drywall/CFS Framing) | Sub | {phone}
- **{door_supplier}** (Doors/Hardware) | Supplier | {phone}
- **{plumbing_supplier}** (Plumbing/Utilities) | Supplier | {phone}
- **{steel_supplier}** (Structural Steel) | Supplier | {phone}
- **{concrete_supplier}** (Mix designs, concrete supply) | Supplier | {phone}

*Populate from directory.json — read all contacts, companies, and roles from the project's extracted data.*

---

### 3.2 Facility Worksheet

**Purpose**: Master building identification, classification, and site metadata.

**Source Data**: project-config.json (building basics), plans-spatial.json (area/dimensions)

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| ProjectName | Y (PK) | project-config.project-name | Text | {project_name} |
| ProjectCode | Y | project-config.project-number | Text | {job_number} |
| BuildingName | Y | project-config.building-name | Text | {building_name} |
| BuildingCode | Y | project-config.building-code | Text | {building_code} |
| SiteName | N | project-config.site-name | Text | {site_name} |
| LinearUnits | Y | project-config.units | Enum: Feet / Meters | Feet |
| AreaUnits | Y | project-config.units | Enum: SF / SM | SF |
| VolumeUnits | Y | project-config.units | Enum: CF / CM | CF |
| AreaGrossBuilding | Y | plans-spatial.gross-building-area | Numeric (SF) | 9980 |
| BuildingDescription | N | project-config.description | Text | 1-story healthcare facility, E occupancy, 149 occupant load |
| BuildingCategory | Y | project-config.occupancy-type | Enum: Healthcare / Educational / Office / Residential / Industrial / Retail / Mixed / Other | Healthcare |
| BuildingLocation | N | project-config.site-address | Address | {project_location} |
| Longitude | N | site-survey.longitude | Decimal degrees | -83.4256 |
| Latitude | N | site-survey.latitude | Decimal degrees | 38.1842 |
| Elevation | N | site-survey.elevation | Feet MSL | 762 |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |

**Mapping Logic**:

```json
{
  "ProjectName": "project-config.project-name",
  "ProjectCode": "project-config.project-number",
  "BuildingName": "project-config.building-name",
  "BuildingCode": "project-config.building-code || project-config.project-number",
  "SiteName": "project-config.site-name || 'n/a'",
  "BuildingCategory": "project-config.occupancy-type",
  "BuildingDescription": "project-config.description",
  "BuildingLocation": "project-config.site-address",
  "AreaGrossBuilding": "plans-spatial.gross-building-area",
  "LinearUnits": "Feet",
  "AreaUnits": "SF",
  "VolumeUnits": "CF",
  "Longitude": "site-survey.longitude || 'n/a'",
  "Latitude": "site-survey.latitude || 'n/a'",
  "Elevation": "site-survey.elevation || 'n/a'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

**Example Data**:
- ProjectName: {project_name}
- ProjectCode: {job_number}
- BuildingName: {building_name}
- BuildingCode: {building_code}
- BuildingCategory: Healthcare
- AreaGrossBuilding: 9,980 SF
- BuildingDescription: 1-story Type IIB healthcare facility, E occupancy, 149 occupants, 16 bedrooms, 5 common areas
- Location: {project_location}

---

### 3.3 Floor Worksheet

**Purpose**: Define all floors/levels in the building with area and elevation data.

**Source Data**: plans-spatial.json (floor schedule)

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| FloorName | Y (PK) | plans-spatial.floor-name | Text | Level 1 / Ground Floor |
| BuildingName | Y | project-config.building-name | Text (FK to Facility) | {building_name} |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| FloorDescription | N | plans-spatial.floor-description | Text | Single-story floor, includes all occupied spaces |
| Elevation | N | plans-spatial.floor-elevation | Feet above datum | 0.0 (baseline) |
| AreaGrossFloor | Y | plans-spatial.floor-gross-area | Numeric (SF) | 9980 |
| AreaNetFloor | N | plans-spatial.floor-net-usable-area | Numeric (SF) | 9100 (approx) |

**Mapping Logic**:

```json
{
  "FloorName": "plans-spatial.floor-name || 'Level 1'",
  "BuildingName": "project-config.building-name",
  "FloorDescription": "plans-spatial.floor-description || 'n/a'",
  "Elevation": "plans-spatial.floor-elevation || 0.0",
  "AreaGrossFloor": "plans-spatial.floor-gross-area",
  "AreaNetFloor": "plans-spatial.floor-net-usable-area || 'n/a'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

**Example Floor Data**:
- Single floor (1-story building)
- FloorName: "Ground Floor" or "Level 1"
- AreaGrossFloor: 9,980 SF
- Elevation: 0.0 ft (building baseline)

---

### 3.4 Space Worksheet

**Purpose**: Inventory of all rooms, spaces, and areas with finishes, function, and occupancy data. This is critical for facility navigation ("What equipment is in Bedroom 5?").

**Source Data**: plans-spatial.json (room schedule), room finish schedules, specs-quality.json (space types)

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| SpaceName | Y (PK) | plans-spatial.room-name | Text | Bedroom 1 / Common Room A / Nurse Station |
| FloorName | Y | plans-spatial.floor-assignment | Text (FK to Floor) | Ground Floor |
| RoomTag | Y | plans-spatial.room-id | Text (from plans) | A-101 / B-205 |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Description | N | plans-spatial.room-description | Text | Private patient bedroom, dual occupancy capable |
| RoomCategory | Y | plans-spatial.room-type | Enum: Bedroom / Bath / Common / Support / Circulation / Mechanical / Storage | Bedroom |
| AreaGrossRoom | N | plans-spatial.room-gross-area | Numeric (SF) | 245 |
| AreaNetRoom | N | plans-spatial.room-usable-area | Numeric (SF) | 220 |
| FloorFinish | N | room-finish-schedule.floor-material | Text | Vinyl composite tile, slip-resistant |
| WallFinish | N | room-finish-schedule.wall-material | Text | Paint, wipeable, eggshell |
| CeilingFinish | N | room-finish-schedule.ceiling-material | Text | Suspended acoustic tile, cleanroom-rated |
| Department | N | space-assignment.department | Text | Patient Care / Administrative / Dietary / Maintenance |
| Occupancy | N | occupancy-schedule.occupancy-type | Enum: Occupant / Staff / Equipment / Circulation | Occupant |
| OccupancyCount | N | occupancy-schedule.person-count | Numeric | 2 |

**Mapping Logic**:

```json
{
  "SpaceName": "plans-spatial.room-name",
  "FloorName": "plans-spatial.floor-assignment",
  "RoomTag": "plans-spatial.room-id || 'TBD'",
  "Description": "plans-spatial.room-description || 'n/a'",
  "RoomCategory": "plans-spatial.room-type",
  "AreaGrossRoom": "plans-spatial.room-gross-area || 'n/a'",
  "AreaNetRoom": "plans-spatial.room-usable-area || 'n/a'",
  "FloorFinish": "room-finish-schedule.floor-material || 'n/a'",
  "WallFinish": "room-finish-schedule.wall-material || 'n/a'",
  "CeilingFinish": "room-finish-schedule.ceiling-material || 'n/a'",
  "Department": "space-assignment.department || 'n/a'",
  "Occupancy": "occupancy-schedule.occupancy-type || 'n/a'",
  "OccupancyCount": "occupancy-schedule.person-count || 'n/a'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

**Example Space Inventory** (from project data):
- 16 Bedrooms (275 SF each approx) | Department: Patient Care | Occupancy: Occupant, 2 persons
- 5 Common Areas (dining, activity, living, etc.) | Department: Patient Care
- 8 Support Spaces (offices, med room, supply, laundry) | Department: Administrative/Support
- 4 Restroom Groups | Department: Common
- Nurse Station | Department: Administrative | Occupancy: Staff, 4-6 persons
- Corridors & Circulation | RoomCategory: Circulation
- Mechanical Room | RoomCategory: Mechanical | Equipment: HVAC, plumbing, electrical

---

### 3.5 Zone Worksheet

**Purpose**: Functional groupings of spaces for HVAC, fire/life safety, accessibility, and departmental zones.

**Source Data**: plans-spatial.json (zone assignments), specs-quality.json (HVAC/fire zones), building code analysis

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| ZoneName | Y (PK) | plans-spatial.zone-name OR system-generated | Text | HVAC Zone 1 / Fire Zone A / Dept: Patient Care |
| BuildingName | Y | project-config.building-name | Text (FK to Facility) | {building_name} |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Description | N | zone-assignment.description | Text | HVAC zone serving patient bedrooms 1-8 and west corridor |
| ZoneCategory | Y | zone-assignment.zone-type | Enum: HVAC / Plumbing / Electrical / Fire / Accessibility / Departmental / Security | HVAC |
| Spaces | N | zone-assignment.space-members | Comma-delimited list | Bedroom 1, Bedroom 2, Bedroom 3, Bedroom 4, Bedroom 5, Bedroom 6, Bedroom 7, Bedroom 8, Corridor West |

**Mapping Logic**:

```json
{
  "ZoneName": "zone-assignment.zone-name",
  "BuildingName": "project-config.building-name",
  "ZoneCategory": "zone-assignment.zone-type",
  "Description": "zone-assignment.description || 'n/a'",
  "Spaces": "zone-assignment.space-members.join(', ')",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

**Example Zones** (inferred from project data):
- **HVAC Zones** (from Carrier AHU-1/2/3): AHU-1 zone (east wing bedrooms), AHU-2 zone (common areas), AHU-3 zone (west wing + support)
- **Fire Zones** (IBC compliance): Zone A (patient bedrooms west), Zone B (patient bedrooms east), Zone C (common/support areas)
- **Plumbing Zones** (from GWH-1 water heater): Domestic hot water distribution main zone
- **Electrical Zones** (from Panel A/B/C): Panel A zone (west), Panel B zone (central), Panel C zone (east)
- **Departmental Zones**: Patient Care, Support Services, Administration

---

### 3.6 Type Worksheet

**Purpose**: Asset type catalog with specifications, make, model, manufacturer, and warranty information. This is the "menu" of all equipment types in the building.

**Source Data**: specs-quality.json (equipment schedules), submittal data (manufacturer specs, data sheets)

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| TypeName | Y (PK) | specs-quality.equipment-type | Text | Carrier AHU (AHU-1) / Lochinvar Water Heater / Greenheck Exhaust Fan |
| Category | Y | specs-quality.equipment-category | Enum: HVAC / Plumbing / Electrical / Fire / Structural / Doors / Hardware | HVAC |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Description | N | specs-quality.equipment-description | Text | Air handling unit, 3-ton capacity, variable speed |
| Manufacturer | Y | submittal-data.manufacturer-name | Text | Carrier Corporation |
| ModelNumber | Y | submittal-data.model-number | Text | 25HCH036S0A0C0 |
| WarrantyGuarantorParts | N | submittal-data.warranty-parts-years | Numeric (years) | 5 |
| WarrantyGuarantorLabor | N | submittal-data.warranty-labor-years | Numeric (years) | 1 |
| WarrantyDurationParts | N | submittal-data.warranty-parts-duration | Text | 5 years from startup |
| WarrantyDurationLabor | N | submittal-data.warranty-labor-duration | Text | 1 year from startup |
| Specification | N | specs-quality.specification-reference | Text (URL or file path) | /submittals/Carrier-AHU-spec-sheet.pdf |
| AssetType | N | specs-quality.asset-classification | Enum: Equipment / System / Fixture / Component | Equipment |
| ExpectedLife | N | specs-quality.expected-life-years | Numeric | 15 |
| DurationYears | N | specs-quality.design-life | Numeric (years) | 15 |

**Mapping Logic**:

```json
{
  "TypeName": "specs-quality.equipment-type || specs-quality.equipment-name",
  "Category": "specs-quality.equipment-category",
  "Description": "specs-quality.equipment-description || 'n/a'",
  "Manufacturer": "submittal-data.manufacturer-name || 'Unknown'",
  "ModelNumber": "submittal-data.model-number || 'n/a'",
  "WarrantyGuarantorParts": "submittal-data.warranty-parts-years || 'n/a'",
  "WarrantyGuarantorLabor": "submittal-data.warranty-labor-years || 'n/a'",
  "WarrantyDurationParts": "submittal-data.warranty-parts-duration || 'n/a'",
  "WarrantyDurationLabor": "submittal-data.warranty-labor-duration || 'n/a'",
  "Specification": "submittal-data.spec-url || 'n/a'",
  "AssetType": "Equipment",
  "ExpectedLife": "specs-quality.expected-life-years || 'n/a'",
  "DurationYears": "specs-quality.design-life || 'n/a'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

**Example Type Entries**:

| TypeName | Manufacturer | ModelNumber | Category | WarrantyParts | ExpectedLife |
|----------|--------------|-------------|----------|---------------|--------------|
| Carrier AHU-1 | Carrier | 25HCH036S0A0C0 | HVAC | 5 years | 15 years |
| Carrier AHU-2 | Carrier | 25HCH036S0A0C0 | HVAC | 5 years | 15 years |
| Carrier AHU-3 | Carrier | 25HCH036S0A0C0 | HVAC | 5 years | 15 years |
| Carrier Split AC-1 | Carrier | 25HNH054S01A0 | HVAC | 5 years | 12 years |
| Carrier Split AC-2 | Carrier | 25HNH054S01A0 | HVAC | 5 years | 12 years |
| Carrier Split AC-3 | Carrier | 25HNH054S01A0 | HVAC | 5 years | 12 years |
| Lochinvar Water Heater GWH-1 | Lochinvar | GWH-50-N | Plumbing | 6 years | 15 years |
| RenewAire ERV-1 | RenewAire | E180 Smart | HVAC | 3 years | 20 years |
| Greenheck EF-1 | Greenheck | ® | Plumbing | 3 years | 20 years |
| Greenheck EF-2 | Greenheck | ® | Plumbing | 3 years | 20 years |
| Hollow Metal Door | {door_manufacturer} | Per Spec | Doors | 5 years | 25 years |
| Wood Door | {door_manufacturer} | Per Spec | Doors | 5 years | 25 years |
| Toilet Accessories | {accessory_manufacturer} | Various | Fixtures | 5 years | 10 years |

---

### 3.7 Component Worksheet

**Purpose**: Individual asset instances with serial numbers, locations, installation dates, and current status. This is where equipment gets assigned to specific spaces.

**Source Data**: specs-quality.json + closeout data (as-built, commissioning, startup), submittals

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| Name | Y (PK) | component-registry.component-name | Text | AHU-1 Unit (West Wing) |
| TypeName | Y | component-registry.type-reference | Text (FK to Type) | Carrier AHU-1 |
| Space | Y | component-registry.space-location | Text (FK to Space) | Mechanical Room |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Description | N | component-registry.description | Text | Air handling unit installed in mechanical room serving west patient wing |
| SerialNumber | N | commissioning-data.serial-number OR closeout-tag.serial | Text | 987654321 |
| InstallationDate | N | commissioning-data.startup-date OR closeout-inspection.date-complete | Date (YYYY-MM-DD) | 2026-04-15 |
| TagNumber | N | component-registry.asset-tag OR closeout-tag.tag-number | Text | {project_code}-AHU-001 |
| BarCode | N | component-registry.barcode OR RFID-tag.identifier | Text (barcode data) | 7722448811223344 |
| AssetIdentifier | N | component-registry.asset-id | Text | AC-HVA-0001 |
| Status | Y | component-registry.operational-status | Enum: New / Existing / Planned / Obsolete / Unknown | New |
| Location | Y | component-registry.gps-location OR grid-reference | Text (grid ref) | X-3, Y-C (building grid) |

**Mapping Logic**:

```json
{
  "Name": "component-registry.component-name",
  "TypeName": "component-registry.type-reference",
  "Space": "component-registry.space-location",
  "Description": "component-registry.description || 'n/a'",
  "SerialNumber": "commissioning-data.serial-number || closeout-tag.serial || 'Unknown'",
  "InstallationDate": "commissioning-data.startup-date || closeout-inspection.date-complete || 'n/a'",
  "TagNumber": "component-registry.asset-tag || 'n/a'",
  "BarCode": "component-registry.barcode || 'n/a'",
  "AssetIdentifier": "component-registry.asset-id || 'n/a'",
  "Status": "component-registry.operational-status || 'Unknown'",
  "Location": "component-registry.grid-reference || 'n/a'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

**Example Component Entries** (populated at closeout):
- AHU-1 Unit | Type: Carrier AHU-1 | Space: Mechanical Room | SerialNumber: 987654321 | Location: X-3, Y-D | Status: New
- AC-1 Split | Type: Carrier Split AC-1 | Space: Bedroom 1 | SerialNumber: 654321987 | Status: New
- AC-2 Split | Type: Carrier Split AC-2 | Space: Bedroom 2 | SerialNumber: 654321988 | Status: New
- GWH-1 | Type: Lochinvar Water Heater | Space: Mechanical Room | SerialNumber: 123456789 | Status: New
- ERV-1 | Type: RenewAire ERV-1 | Space: Mechanical Room | SerialNumber: 456789123 | Status: New

---

### 3.8 System Worksheet

**Purpose**: Building systems (HVAC, plumbing, electrical, fire protection) and their functional scope.

**Source Data**: specs-quality.json (system schedules), plans-spatial.json (system service areas)

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| Name | Y (PK) | specs-quality.system-name | Text | HVAC System / Domestic Hot Water / Fire Alarm / Emergency Power |
| Category | Y | specs-quality.system-category | Enum: HVAC / Plumbing / Electrical / Fire / Structural / Security / IT / Vertical Transport | HVAC |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Description | N | specs-quality.system-description | Text | Central HVAC system with 3 air handlers, distributed ductwork, variable air volume dampers |
| Location | N | plans-spatial.system-location | Text | Throughout building |
| AssetType | N | specs-quality.system-asset-type | Enum: Equipment / System | System |

**Mapping Logic**:

```json
{
  "Name": "specs-quality.system-name",
  "Category": "specs-quality.system-category",
  "Description": "specs-quality.system-description || 'n/a'",
  "Location": "plans-spatial.system-location || 'Throughout building'",
  "AssetType": "System",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

**Example Systems**:
- HVAC System (central with 3 AHUs + distributed ductwork + terminal units + ERV)
- Domestic Hot Water System (Lochinvar GWH-1 water heater + piping + fixtures)
- Cold Water System (supply lines + backflow prevention)
- Sanitary Drainage System (DWV piping + traps + venting)
- Storm Drainage System (exterior roof drains + site piping)
- Electrical Power Distribution (main panel + sub-panels A/B/C + branch circuits)
- Lighting System (120+ LED fixtures + controls + emergency lighting)
- Fire Alarm System (addressable, manual pull stations, horns, strobes)
- Fire Suppression (if applicable — sprinkler system or halon)
- Nurse Call System (audio/visual, emergency call buttons)
- Access Control System (card readers, electronic locks)
- Security Monitoring System (cameras, sensors)
- Emergency Power System (generator, transfer switch if required)

---

### 3.9 Assembly Worksheet

**Purpose**: Asset assemblies and groupings (e.g., "HVAC AHU package" includes fan motor, filters, dampers, controls).

**Source Data**: specs-quality.json (assembly definitions), equipment groupings

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| Name | Y (PK) | specs-quality.assembly-name | Text | AHU-1 Package / Filter Bank / Control Panel |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Description | N | specs-quality.assembly-description | Text | Complete air handler unit assembly including supply fan, return fan, filters, dampers, controls |
| ComponentNames | N | assembly-definition.component-members | Comma-delimited | AHU-1 Fan Motor, AHU-1 Return Filter, AHU-1 Supply Filter, AHU-1 Mix Damper |
| Quantity | N | specs-quality.assembly-quantity | Numeric | 1 |

**Mapping Logic**:

```json
{
  "Name": "specs-quality.assembly-name",
  "Description": "specs-quality.assembly-description || 'n/a'",
  "ComponentNames": "assembly-definition.component-members.join(', ')",
  "Quantity": "specs-quality.assembly-quantity || 1",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

**Example Assemblies**:
- AHU-1 Complete Unit (fan, motor, filters, dampers, controls)
- Water Heater Hot Water Distribution (heater + pump + controls + mixing valve)
- Fire Alarm System Package (control panel + sensors + manual stations + horns)
- Nurse Call System (base station + call buttons + speakers + displays)

---

### 3.10 Connection Worksheet

**Purpose**: Relationships between systems and components (e.g., "AHU-1 feeds Ductwork Zone 1" or "Panel A controls Circuit 1-4").

**Source Data**: specs-quality.json (coordination notes), system diagrams, equipment schedules

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| ConnectionName | Y (PK) | connection-registry.connection-id | Text (auto-generated) | HVAC-001-to-HVAC-002 / Electrical-Panel-A-to-Circuit-1 |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| PortOne | Y | connection-registry.source-component | Text | AHU-1 (discharge) |
| PortTwo | Y | connection-registry.target-component | Text | Ductwork to AHU-1 Zone 1 |
| FlowDirection | N | connection-registry.flow-direction | Enum: Forward / Reverse / Bidirectional | Forward |
| RealizationModule | N | connection-registry.media-type | Text (pipe/duct/wire size) | 8" diameter ductwork / 1" copper tubing |

**Mapping Logic**:

```json
{
  "ConnectionName": "connection-registry.connection-id",
  "PortOne": "connection-registry.source-component",
  "PortTwo": "connection-registry.target-component",
  "FlowDirection": "connection-registry.flow-direction || 'Forward'",
  "RealizationModule": "connection-registry.media-type || 'n/a'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

---

### 3.11 Spare Worksheet

**Purpose**: Spare parts inventory and specifications required for maintenance.

**Source Data**: submittal O&M manuals (manufacturer spare parts lists), commissioning data

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| SpareType | Y (PK) | spare-parts-list.part-name | Text | HVAC Filter Element / Water Heater Control Module |
| TypeName | Y | spare-parts-list.equipment-type | Text (FK to Type) | Carrier AHU-1 |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Description | N | spare-parts-list.description | Text | MERV-13 pleated filter, 16x25x4 inches |
| PartNumber | Y | spare-parts-list.manufacturer-part-number | Text | CAR-16x25x4-M13 |
| StorageLocation | N | spare-parts-list.storage-location | Text | Maintenance Room Shelf 3 |
| QuantityOnHand | N | spare-parts-inventory.current-quantity | Numeric | 4 |
| QuantityRequired | N | spare-parts-list.recommended-inventory | Numeric | 6 |
| Cost | N | spare-parts-list.unit-cost | Currency (USD) | 45.00 |
| LeadTime | N | spare-parts-list.supplier-lead-time | Text (days) | 3-5 business days |
| Supplier | N | spare-parts-list.supplier-name | Text | {plumbing_supplier} |

**Mapping Logic**:

```json
{
  "SpareType": "spare-parts-list.part-name",
  "TypeName": "spare-parts-list.equipment-type",
  "Description": "spare-parts-list.description || 'n/a'",
  "PartNumber": "spare-parts-list.manufacturer-part-number",
  "StorageLocation": "spare-parts-list.storage-location || 'n/a'",
  "QuantityOnHand": "spare-parts-inventory.current-quantity || 0",
  "QuantityRequired": "spare-parts-list.recommended-inventory || 'n/a'",
  "Cost": "spare-parts-list.unit-cost || 'n/a'",
  "LeadTime": "spare-parts-list.supplier-lead-time || 'n/a'",
  "Supplier": "spare-parts-list.supplier-name || 'n/a'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

---

### 3.12 Resource Worksheet

**Purpose**: Maintenance materials and tools (beyond spare parts), including product data sheets and disposal requirements.

**Source Data**: submittal product data sheets, maintenance plan documentation

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| Name | Y (PK) | resource-registry.resource-name | Text | Compressor Oil / Refrigerant R-410A / Test Gauges |
| Category | Y | resource-registry.resource-type | Enum: Maintenance / Cleaning / Safety / Test / Consumable | Maintenance |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Description | N | resource-registry.description | Text | Synthetic compressor oil for Carrier units, ISO VG 32 |
| URL | N | resource-registry.product-sheet-url | Text (hyperlink) | /submittals/Carrier-Oil-SDS.pdf |
| Quantity | N | resource-inventory.quantity | Numeric | 6 |
| Unit | N | resource-registry.unit-type | Text | quarts / gallons / sets |

**Mapping Logic**:

```json
{
  "Name": "resource-registry.resource-name",
  "Category": "resource-registry.resource-type",
  "Description": "resource-registry.description || 'n/a'",
  "URL": "resource-registry.product-sheet-url || 'n/a'",
  "Quantity": "resource-inventory.quantity || 'n/a'",
  "Unit": "resource-registry.unit-type || 'ea'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

---

### 3.13 Job Worksheet

**Purpose**: Maintenance tasks and schedules (recurring and one-time) derived from manufacturer specifications and building code requirements.

**Source Data**: submittal O&M manuals (maintenance matrices), building code, energy code

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| Name | Y (PK) | maintenance-schedule.job-name | Text | HVAC Filter Replacement / Water Heater Flushing / Fire Alarm Test |
| Category | Y | maintenance-schedule.job-type | Enum: Preventive / Corrective / Cleaning / Inspection / Testing | Preventive |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Description | N | maintenance-schedule.description | Text | Replace MERV-13 filters in AHU-1, AHU-2, AHU-3 per manufacturer schedule |
| Frequency | Y | maintenance-schedule.frequency | Text | Monthly / Quarterly / Semi-Annual / Annual / Biennial / As-Needed |
| Duration | N | maintenance-schedule.estimated-duration | Text | 2 hours per unit |
| Location | N | maintenance-schedule.location | Text | Mechanical Room |
| TaskStartDate | N | maintenance-schedule.first-occurrence-date | Date (YYYY-MM-DD) | 2026-05-19 |
| TaskStopDate | N | maintenance-schedule.last-scheduled-date | Date (YYYY-MM-DD) | 2035-05-19 |
| Instruction | N | maintenance-schedule.procedure-url | Text (hyperlink) | /manuals/Carrier-AHU-Maintenance.pdf |
| Performer | N | maintenance-schedule.assigned-technician | Text | Facilities Maintenance Team |
| Resource | N | maintenance-schedule.required-resources | Text (comma-delimited) | MERV-13 Filters, Test Gauges, Compressor Oil |

**Mapping Logic**:

```json
{
  "Name": "maintenance-schedule.job-name",
  "Category": "maintenance-schedule.job-type",
  "Description": "maintenance-schedule.description || 'n/a'",
  "Frequency": "maintenance-schedule.frequency",
  "Duration": "maintenance-schedule.estimated-duration || 'n/a'",
  "Location": "maintenance-schedule.location || 'n/a'",
  "TaskStartDate": "maintenance-schedule.first-occurrence-date || '2026-05-19'",
  "TaskStopDate": "maintenance-schedule.last-scheduled-date || 'n/a'",
  "Instruction": "maintenance-schedule.procedure-url || 'n/a'",
  "Performer": "maintenance-schedule.assigned-technician || 'Facilities Maintenance'",
  "Resource": "maintenance-schedule.required-resources.join(', ')",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

**Example Maintenance Jobs** (from manufacturer manuals):
- HVAC Filter Replacement | Frequency: Monthly | Performer: HVAC Technician
- Water Heater Flushing & Scale Removal | Frequency: Annual | Performer: HVAC Technician
- AC Unit Refrigerant Charge Verification | Frequency: Semi-Annual | Performer: EPA-Certified Technician
- Fire Alarm System Monthly Test | Frequency: Monthly | Performer: Fire Alarm Service
- Fire Alarm Annual Inspection | Frequency: Annual | Performer: Licensed Fire Alarm Inspector
- Nurse Call System Functional Test | Frequency: Quarterly | Performer: Biomedical Technician
- Emergency Lighting Battery Test | Frequency: Monthly | Performer: Facilities Staff
- Backflow Prevention Device Testing | Frequency: Annual | Performer: Certified Backflow Tester
- Door Hardware Lubrication & Adjustment | Frequency: Semi-Annual | Performer: Maintenance Staff

---

### 3.14 Impact Worksheet

**Purpose**: Environmental and economic impact data (energy consumption, sustainability, carbon footprint).

**Source Data**: specs-quality.json (equipment efficiency ratings), building energy code analysis, environmental impact assessment

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| Name | Y (PK) | impact-registry.impact-name | Text | HVAC Energy Efficiency / Water Conservation / Carbon Footprint |
| Category | Y | impact-registry.impact-type | Enum: Environmental / Energy / Water / Waste / Emissions | Energy |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Description | N | impact-registry.description | Text | HVAC system designed to 2021 IECC, estimated annual consumption 145 kWh/SF |
| Value | N | impact-registry.calculated-value | Numeric | 145 |
| Unit | N | impact-registry.unit | Text | kWh/SF/yr / GPM / lbs CO2/yr |
| ImpactType | N | impact-registry.impact-direction | Enum: Positive / Negative / Neutral | Positive |

**Mapping Logic**:

```json
{
  "Name": "impact-registry.impact-name",
  "Category": "impact-registry.impact-type",
  "Description": "impact-registry.description || 'n/a'",
  "Value": "impact-registry.calculated-value || 'n/a'",
  "Unit": "impact-registry.unit || 'n/a'",
  "ImpactType": "impact-registry.impact-direction || 'Neutral'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

---

### 3.15 Document Worksheet

**Purpose**: References to submittals, O&M manuals, warranties, shop drawings, commissioning reports, and other project documentation.

**Source Data**: document-intelligence (extracted metadata), submittal log, commissioning reports, warranty documentation

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| Name | Y (PK) | document-registry.document-name | Text | Carrier AHU Spec Sheet / Lochinvar Water Heater Manual / Fire Alarm Commissioning Report |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Category | Y | document-registry.document-type | Enum: Specification / Manual / Warranty / Commissioning / Drawing / Certificate / Report / SDS | Specification |
| ApprovedBy | N | document-registry.approver | Text | {pm_name} / Project Manager |
| Stage | Y | document-registry.project-phase | Enum: Design / Construction / Closeout / Operation | Closeout |
| Description | N | document-registry.description | Text | Manufacturer product data sheet with performance curves and maintenance schedule |
| Location | Y | document-registry.file-path-or-url | Text (hyperlink/path) | /submittals/Carrier-AHU-25HCH036S0A0C0-spec.pdf |
| Issued | N | document-registry.issue-date | Date (YYYY-MM-DD) | 2025-12-15 |
| Available | N | document-registry.expiration-date OR lifecycle-date | Date (YYYY-MM-DD) | 2035-12-15 (warranty expiration) |

**Mapping Logic**:

```json
{
  "Name": "document-registry.document-name",
  "Category": "document-registry.document-type",
  "Description": "document-registry.description || 'n/a'",
  "ApprovedBy": "document-registry.approver || 'n/a'",
  "Stage": "document-registry.project-phase || 'Closeout'",
  "Location": "document-registry.file-path-or-url",
  "Issued": "document-registry.issue-date || 'n/a'",
  "Available": "document-registry.expiration-date || 'n/a'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

**Example Documents** (expected at closeout):
- Carrier AHU-1 Product Data Sheet (Specification, /submittals/Carrier-AHU-*.pdf)
- Carrier AHU-2 Product Data Sheet (Specification, /submittals/Carrier-AHU-*.pdf)
- Carrier AHU-3 Product Data Sheet (Specification, /submittals/Carrier-AHU-*.pdf)
- Carrier Split AC Equipment Spec Sheets (Specification)
- Lochinvar Water Heater O&M Manual (Manual, /submittals/Lochinvar-GWH-*.pdf)
- RenewAire ERV Product Data Sheet (Specification)
- Greenheck Exhaust Fan Spec Sheets (Specification)
- Fire Alarm System Shop Drawings (Drawing, MMI approval)
- Fire Alarm Commissioning Report (Commissioning, test results)
- Nurse Call System Training Manual (Manual)
- Electrical Panel Schedule (Drawing, IFC approval)
- Electrical Commissioning Report (Commissioning)
- HVAC Commissioning Report (Commissioning, TAB data)
- Plumbing System Pressure Test Report (Commissioning)
- Fire Suppression System Acceptance Test (Commissioning, if applicable)
- {door_supplier} Door and Hardware Warranty Certificates (Warranty, 5-year coverage)
- All Major Equipment Warranties (Warranty)

---

### 3.16 Attribute Worksheet

**Purpose**: Extended properties and custom fields not covered in standard COBie fields. This captures project-specific metadata.

**Source Data**: all extracted data, project-specific attributes stored in cobie-export-config.json

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| Name | Y (PK) | attribute-registry.attribute-name | Text | Asset Purchase Date / Installation Technician / Maintenance Vendor Contact |
| Category | Y | attribute-registry.parent-entity | Enum: Contact / Facility / Floor / Space / Zone / Type / Component / System / Assembly / Connection / Spare / Resource / Job / Impact / Document | Component |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| DataType | Y | attribute-registry.data-type | Enum: Text / Number / Date / Boolean / URL / Email | Date |
| Value | N | attribute-registry.value | Mixed | 2026-04-15 |
| TargetEntity | N | attribute-registry.entity-reference | Text (PK reference) | AHU-1 Unit (West Wing) |

**Mapping Logic**:

```json
{
  "Name": "attribute-registry.attribute-name",
  "Category": "attribute-registry.parent-entity",
  "DataType": "attribute-registry.data-type",
  "Value": "attribute-registry.value || 'n/a'",
  "TargetEntity": "attribute-registry.entity-reference || 'n/a'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

---

### 3.17 Coordinate Worksheet

**Purpose**: Location coordinates using building grid system (X/Y/Z references) and actual GPS coordinates.

**Source Data**: plans-spatial.json (grid definitions), site survey data

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| Name | Y (PK) | coordinate-registry.coordinate-name | Text | AHU-1 Location / Bedroom 1 Center / Mech Room Door |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Longitude | N | site-survey.longitude OR coordinate-registry.gps-longitude | Decimal degrees | -83.4256 |
| Latitude | N | site-survey.latitude OR coordinate-registry.gps-latitude | Decimal degrees | 38.1842 |
| Elevation | N | site-survey.elevation OR coordinate-registry.z-coordinate | Feet MSL | 762.50 |
| X Axis | N | plans-spatial.grid-x-reference | Grid code (text/numeric) | 3 |
| Y Axis | N | plans-spatial.grid-y-reference | Grid code (text/numeric) | C |
| Z Axis | N | plans-spatial.grid-z-reference | Grid code (text/numeric) | 1 |

**Mapping Logic**:

```json
{
  "Name": "coordinate-registry.coordinate-name",
  "Longitude": "site-survey.longitude || 'n/a'",
  "Latitude": "site-survey.latitude || 'n/a'",
  "Elevation": "site-survey.elevation || 'n/a'",
  "X Axis": "plans-spatial.grid-x-reference || 'n/a'",
  "Y Axis": "plans-spatial.grid-y-reference || 'n/a'",
  "Z Axis": "plans-spatial.grid-z-reference || '1'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

**Example Grid System** (from project memory):
- X-Grids: 1, 2, 3, 4, 5 (spaced 26'-8" apart, total 75'-0")
- Y-Grids: A, B, C, D, E, F, G, H (spaced ~16'-8" apart, total 132'-8")
- Z-Axis: 1 (single floor)

**Example Coordinates**:
- AHU-1 Location: X-3, Y-D (mechanical room center)
- Bedroom 1: X-1, Y-A to X-2, Y-B
- Nurse Station: X-3, Y-B
- Main Entry: X-3, Y-A

---

### 3.18 Issue Worksheet

**Purpose**: Known deficiencies, punch list items, RFIs, and outstanding project items for handover phase resolution.

**Source Data**: punch-list.json, rfi-log.json, deficiency-tracking.json, inspection reports

**Key Fields and Mappings**:

| COBie Field | Required | Data Source | Format | Example |
|-------------|----------|-------------|--------|---------|
| Name | Y (PK) | issue-registry.issue-name | Text (auto-generated ID) | Issue-PL-0001 / RFI-0042 / Deficiency-Electrical-001 |
| CreatedBy | Y | document-intelligence.extractor | Email | system@foreman-os.local |
| CreatedOn | Y | audit-trail.current-timestamp | ISO 8601 | 2026-02-19T10:30:00Z |
| Category | Y | issue-registry.issue-type | Enum: Deficiency / Discrepancy / Request for Information / Incomplete / Damage / Safety | Deficiency |
| Description | Y | issue-registry.description | Text | AHU-1 supply duct not properly sealed at penetration |
| Status | Y | issue-registry.status | Enum: Open / In Progress / Resolved / Deferred / Closed / On Hold | Open |
| Assigned | N | issue-registry.assigned-to | Text (email or name) | {structural_sub} / HVAC Sub |
| DueDate | N | issue-registry.due-date | Date (YYYY-MM-DD) | 2026-05-15 |
| Priority | N | issue-registry.priority | Enum: Critical / High / Medium / Low | Medium |
| Component | N | issue-registry.affected-component | Text (FK reference) | AHU-1 Unit (West Wing) |
| Comment | N | issue-registry.resolution-notes | Text | n/a (pending repair) |

**Mapping Logic**:

```json
{
  "Name": "issue-registry.issue-name || issue-registry.issue-id",
  "Category": "issue-registry.issue-type",
  "Description": "issue-registry.description",
  "Status": "issue-registry.status",
  "Assigned": "issue-registry.assigned-to || 'n/a'",
  "DueDate": "issue-registry.due-date || 'n/a'",
  "Priority": "issue-registry.priority || 'Medium'",
  "Component": "issue-registry.affected-component || 'n/a'",
  "Comment": "issue-registry.resolution-notes || 'n/a'",
  "CreatedBy": "system@foreman-os.local",
  "CreatedOn": "audit-trail.current-timestamp"
}
```

---



## 8. Healthcare Facility Specifics

**Facility-Type Extension: Healthcare** — Healthcare, senior care, and medical facilities are subject to additional regulatory requirements beyond standard building codes. Activate this extension when `project-config.json` occupancy type includes healthcare, medical, senior care, or assisted living.

### Healthcare-Specific COBie Fields

The COBie export includes these healthcare-critical data extensions:

**Contact Worksheet Additions**:
- Medical Director contact (responsible for clinical equipment specifications)
- Infection Control Officer contact (for disinfection protocols, finishes)
- Biomedical Engineering contact (for medical equipment maintenance)

**Space Worksheet Additions**:
- Isolation rooms (if applicable)
- Infection control zones (surfaces, HVAC isolation)
- Accessibility classifications (ADA compliance per room)
- Life safety zone assignments

**Type Worksheet Additions** (Medical Equipment):
- FDA classification (Class I/II/III for applicable equipment)
- Medical device UDI (Unique Device Identifier) if applicable
- Sterilization/disinfection requirements (if applicable)
- Reprocessing instructions (if applicable)

**Component Worksheet Additions**:
- Installation date (critical for warranty/service)
- Biomedical asset tag (separate from general assets)
- Equipment status (operational, scheduled for replacement, on hold)
- Last service date (from biomedical tracking system)

**Job Worksheet Additions** (Healthcare-Specific Maintenance):
- Infection prevention maintenance tasks (surface cleaning protocols, air handling verification)
- Equipment decontamination procedures
- Staff training requirements
- Regulatory inspection schedules (Joint Commission, CMS, state survey)
- Isolation room pressure testing (quarterly for independent HVAC systems)

**Document Worksheet Additions**:
- Joint Commission equipment records (required for accreditation)
- CMS compliance certifications (Medicare/Medicaid eligibility)
- State licensing inspection reports
- Biomedical equipment manuals (distinct from standard O&M)
- Disinfection/sterilization protocols
- Infection control documentation

### Medical Equipment Tracking

For healthcare/medical facilities, the following systems require enhanced COBie documentation:

**Nurse Call System**:
- Manufacturer: [TBD in project memory]
- Scope: Audio/visual communication system, emergency call buttons in bedrooms + common areas
- COBie tracking:
  - Type: Nurse Call System
  - Component: Individual call buttons + base stations + displays
  - System: Nurse Call System
  - Job: Monthly functional testing, annual maintenance
  - Document: System manual, training records, compliance certificate

**Isolation/Infection Control**:
- Space designation: 2-4 isolation rooms (if applicable) marked in Space worksheet
- Zone designation: Dedicated HVAC zone (separate supply/return)
- Job: Isolation room pressure testing quarterly (≥2.5 Pa negative)
- Document: HVAC test reports, infection control protocols

**Emergency Power**:
- If applicable: Generator + transfer switch
- Type: Emergency Power System
- Component: Generator, fuel tank, transfer switch, testing
- Job: Monthly load testing, annual inspection, fuel integrity testing
- Document: Equipment manual, testing logs, compliance certification

**Fire/Life Safety Systems**:
- Sprinkler system (if applicable): Full system documentation
- Fire alarm: Enhanced documentation for healthcare (longer notification times, manual pull stations)
- Exit signage & emergency lighting: Full inventory with battery testing schedules
- Document: System commissioning reports, annual inspection certificates, fire marshal approvals

### Joint Commission & CMS Compliance

The COBie export can be cross-referenced with healthcare compliance checklists:

**Equipment Management**:
- All medical equipment documented in Type/Component worksheets
- Warranty tracking in Document worksheet
- Maintenance schedules in Job worksheet
- Joint Commission verification: Export confirms all equipment accounted for

**Life Safety**:
- Fire alarm system fully documented
- Emergency power system documented (if applicable)
- Isolation room specifications documented
- Exit/egress routes documented in Space worksheet

**Environment of Care**:
- HVAC systems documented with maintenance schedules
- Room finish specifications documented (infection control compliance)
- Plumbing system documentation (water quality, legionella prevention)

---



## 9. Integration Points

### project-data Skill

Primary integration: The cobie-export skill depends entirely on project-data for all JSON source files.

```
cobie-export
├─ project-data.project-config (facility metadata)
├─ project-data.directory (contacts)
├─ project-data.plans-spatial (spaces, zones, grids)
├─ project-data.specs-quality (equipment, systems, maintenance)
├─ project-data.audit-trail (timestamps, creators)
└─ project-data.closeout-inspection (serial numbers, installation dates)
```

### closeout-commissioning Skill

Data flow: Commissioning results populate Component, Job, and Document worksheets.

```
closeout-commissioning
├─ Startup dates → Component.InstallationDate
├─ Commissioning reports → Document worksheet (category: Commissioning)
├─ Maintenance procedures verified → Job worksheet (updates to manufacturer recommendations)
└─ Seasonal balancing data → Job worksheet (HVAC-specific schedules)
```

### submittal-intelligence Skill

Data extraction: Approved submittals provide Type, Spare, Resource, and Document data.

```
submittal-intelligence
├─ Manufacturer specs → Type worksheet (make, model, warranty info)
├─ Product data sheets → Document worksheet
├─ O&M manual extraction → Spare, Resource, Job worksheets
├─ Warranty extraction → Type.WarrantyGuarantor* fields
└─ Approved document dates → Document.Issued field
```

### xlsx Skill

Workbook generation: cobie-export delegates Excel file creation to xlsx skill.

```
cobie-export
└─ xlsx.create-workbook
    ├─ Sheet: Contact (12 rows)
    ├─ Sheet: Facility (1 row)
    ├─ Sheet: Floor (1 row)
    ├─ Sheet: Space (29 rows)
    ├─ Sheet: Zone (14 rows)
    ├─ Sheet: Type (48 rows)
    ├─ Sheet: Component (31 rows)
    ├─ Sheet: System (14 rows)
    ├─ Sheet: Assembly (8 rows)
    ├─ Sheet: Connection (12 rows)
    ├─ Sheet: Spare (15 rows)
    ├─ Sheet: Resource (8 rows)
    ├─ Sheet: Job (22 rows)
    ├─ Sheet: Impact (6 rows)
    ├─ Sheet: Document (18 rows)
    ├─ Sheet: Attribute (45 rows)
    ├─ Sheet: Coordinate (8 rows)
    └─ Sheet: Issue (6 rows)
```

### document-intelligence Skill

Data extraction: Metadata and content analysis supports Document, Spare, Resource, and Job worksheets.

```
document-intelligence
├─ Extract document type (spec sheet, manual, warranty) → Document.Category
├─ Extract manufacturer info → Type, Spare worksheets
├─ Extract maintenance requirements → Job worksheet
├─ Extract warnings/cautions → Job worksheet (safety notes)
├─ Extract part numbers → Spare.PartNumber field
└─ Extract supplier info → Spare.Supplier, Resource.Supplier fields
```

### quality-management Skill

Data flow: Inspection records and test reports populate Document and Issue worksheets.

```
quality-management
├─ Commissioning test results → Document (category: Commissioning)
├─ Final inspection checklist → Issue (status: Resolved/Closed)
├─ Punch list items → Issue worksheet (status: Open/In Progress/Resolved)
├─ Deficiency tracking → Issue worksheet (category: Deficiency)
└─ Inspection sign-offs → Document (category: Certificate/Report)
```

### drawing-control Skill

Data flow: Shop drawings and revisions support Document and Coordinate worksheets.

```
drawing-control
├─ PEMB shop drawings → Document (drawing references, approval dates)
├─ MMI anchor bolt shop drawings → Document, Component (installation verification)
├─ MEP coordination drawings → Connection worksheet (system routing)
├─ As-built plans → Coordinate worksheet (updated grid references)
└─ Equipment location drawings → Component.Location field updates
```

---



## 10. COBie Validation Rules

The export must pass these mandatory validation checks:

### Primary Key Uniqueness (Per Worksheet)

| Worksheet | Primary Key | Rule |
|-----------|-------------|------|
| Contact | Email | No duplicate email addresses |
| Facility | ProjectCode | One entry per building project |
| Floor | FloorName | Unique within facility |
| Space | SpaceName | Unique within floor |
| Zone | ZoneName | Unique within facility |
| Type | TypeName | Unique type definition |
| Component | Name | Unique component instance |
| System | Name | Unique system identifier |
| Assembly | Name | Unique assembly identifier |
| Connection | ConnectionName | Unique connection identifier |
| Spare | SpareType | Unique spare part type |
| Resource | Name | Unique resource type |
| Job | Name | Unique maintenance job |
| Impact | Name | Unique impact metric |
| Document | Name | Unique document reference |
| Attribute | Name (within Category) | Unique attribute per parent entity |
| Coordinate | Name | Unique coordinate location |
| Issue | Name | Unique issue identifier |

### Foreign Key Integrity (References Must Exist)

- Component.TypeName → Type.TypeName (required)
- Component.Space → Space.SpaceName (required)
- Component.FloorName → Floor.FloorName (required)
- Zone.Spaces → Space.SpaceName (comma-delimited; all must exist)
- Zone.BuildingName → Facility.BuildingName (required)
- Floor.BuildingName → Facility.BuildingName (required)
- Job.Location → Space.SpaceName (required if location specified)
- Document.ApprovedBy → Contact.Email (optional but if present, must exist)
- Spare.TypeName → Type.TypeName (required)
- Assembly components → Component.Name (comma-delimited; all must exist)
- Connection.PortOne → Component.Name or System.Name
- Connection.PortTwo → Component.Name or System.Name
- Attribute.TargetEntity → Primary key of parent entity

### Enum Value Validation

All enumerated fields must match allowed values per COBie v2.4 spec:

- Status: New / Existing / Planned / Obsolete / Unknown
- Category (Contact): GC / Sub / Supplier / Architect / Engineer / Owner / Consultant / Facility
- RoomCategory: Bedroom / Bath / Common / Support / Circulation / Mechanical / Storage / Other
- ZoneCategory: HVAC / Plumbing / Electrical / Fire / Accessibility / Departmental / Security / Other
- Category (Type/System): HVAC / Plumbing / Electrical / Fire / Structural / Doors / Hardware / IT / Security / Vertical / Other
- Category (Job): Preventive / Corrective / Cleaning / Inspection / Testing / Safety / Other
- Category (Issue): Deficiency / Discrepancy / Request for Information / Incomplete / Damage / Safety / Other
- Frequency: Daily / Weekly / Monthly / Quarterly / Semi-Annual / Annual / Biennial / As-Needed / Unknown
- FlowDirection: Forward / Reverse / Bidirectional / Unknown
- DataType (Attribute): Text / Number / Date / Boolean / URL / Email / Other

### Data Type Conformance

- Email fields: Must match regex `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Date fields: ISO 8601 format `YYYY-MM-DD` (no time, UTC assumed)
- Numeric fields: No currency symbols; negative numbers allowed where applicable
- Phone: Minimum 10 digits; optional international format
- URLs: Must start with `http://` or `https://` or be a file path
- Boolean: "Yes"/"No" or 1/0 (standardized to Yes/No in output)

### Required Field Completion

**All worksheets require**:
- CreatedBy (email address of person/system that created the row)
- CreatedOn (timestamp ISO 8601)

**Per-worksheet requirements** (sample):
- Contact: Email, Category, Company, GivenName, FamilyName, ContactType
- Facility: ProjectName, ProjectCode, BuildingName, BuildingCode, BuildingCategory, LinearUnits, AreaUnits, VolumeUnits, AreaGrossBuilding
- Component: Name, TypeName, Space
- Type: TypeName, Category, Manufacturer
- System: Name, Category
- Issue: Name, Category, Description, Status

---



## 11. Data Store: cobie-export-config.json

Project-specific COBie configuration and field mapping overrides.

**Location**: `/project-data/cobie-export-config.json`

**Purpose**: Allow project teams to customize field mappings, add custom attributes, and define healthcare-specific data requirements.

**Example Structure**:

```json
{
  "project_number": "{job_number}",
  "cobie_version": "2.4",
  "custom_attributes": [
    {
      "name": "Asset Purchase Date",
      "category": "Component",
      "data_type": "Date",
      "description": "Date equipment purchased/delivered to site"
    },
    {
      "name": "Installation Technician",
      "category": "Component",
      "data_type": "Text",
      "description": "Name/contact of technician who installed component"
    },
    {
      "name": "Annual Service Cost",
      "category": "Type",
      "data_type": "Number",
      "description": "Estimated annual maintenance/service cost"
    },
    {
      "name": "Critical Equipment",
      "category": "Component",
      "data_type": "Boolean",
      "description": "Flag for equipment critical to operations (yes/no)"
    },
    {
      "name": "Isolation Room Designation",
      "category": "Space",
      "data_type": "Boolean",
      "description": "Space functions as infection control isolation room"
    }
  ],
  "field_mapping_overrides": [
    {
      "worksheet": "Type",
      "field": "Category",
      "source_path": "specs-quality.equipment-category",
      "transform": "uppercase",
      "fallback": "Unknown"
    }
  ],
  "healthcare_requirements": {
    "enabled": true,
    "occupancy_type": "Senior Care Facility",
    "medical_equipment_tracking": true,
    "isolation_room_verification": true,
    "joint_commission_compliance": true,
    "cms_certification_required": true
  },
  "delivery_phase": "construction",
  "expected_completion_date": "2026-07-29",
  "last_updated": "2026-02-19T10:30:00Z"
}
```

---



## 12. Best Practices: COBie Data Collection During Construction

### Pre-Construction (Design Phase)

**Target COBie Readiness: 45-50%**

- Establish Contact directory (all GC, subs, suppliers, design team)
- Define Facility metadata (project name, code, location, gross area)
- Create Floor/Space inventory from design plans
- Define Zone assignments (HVAC, fire, electrical)
- Extract Type information from specifications
- Create skeleton System definitions
- Log initial Document references (spec sheets, code analysis)
- Establish Issue tracking (RFIs for data clarifications)

**Action Items**:
- PM: Assign COBie Data Coordinator (submittals coordinator recommended)
- PM: Include COBie data requirements in all subcontract RFQs
- PM: Create directory.json and plans-spatial.json from design deliverables
- Architect/Engineers: Provide equipment schedules (specs-quality.json) in standard format
- Suppliers: Commit to delivering O&M manuals with COBie data points identified

### Early Construction (Foundation & Excavation, Jan-Mar)

**Target COBie Readiness: 50-60%**

- Confirm all Contact information (update email/phone as needed)
- Verify Floor/Space definitions against actual site conditions
- Receive and log initial submittals ({door_supplier} doors, {concrete_supplier} concrete)
- Begin assembly of Type/Component definitions from approved submittals
- Document any Site changes/deviations (ASI, RFI log) in Issue worksheet
- Maintain daily reports with equipment delivery/receipt notes

**Action Items**:
- Super: Log equipment delivery dates and serial numbers as items arrive
- Super: Photograph and document serial plates for major equipment
- Sub Coordinators: Submit equipment data sheets with deliveries
- GC: Update Issue worksheet with submittal status weekly
- PM: Escalate overdue submittals (as of 2/19/26: {door_supplier} 24 days overdue, {concrete_supplier} 17 days overdue)

### Mid-Construction (PEMB Erection through Rough-In, Mar-May)

**Target COBie Readiness: 65-75%**

- PEMB erection: Log PEMB structure into Component worksheet ({steel_supplier} model S25R0990A, serial/details)
- Electrical rough-in: Award electrical sub (SC-{job_number}-08 still pending); log electrical components
- Mechanical rough-in: Log ductwork, piping, electrical conduit connections (Connection worksheet)
- Commissioning prep: Coordinate with Commissioning Agent to ensure COBie-compatible data delivery
- Document collection: Compile approved submittals, shop drawings, test reports

**Action Items**:
- Super: Assign asset tags to all equipment upon installation (photo serial plates)
- Sub Foremen: Log start/completion dates for major system installations
- Commissioning Agent: Request integration of COBie data requirements into commissioning scope
- PM: Schedule final submittal review to ensure all O&M manuals are approved by 6/1/26

### Late Construction (Finishes & Closeout, May-Jul)

**Target COBie Readiness: 90-95%**

- Capture final room finishes (verify against spec, update Space worksheet)
- Commissioning results: Receive and incorporate system test reports (Document worksheet)
- Punch list resolution: Close Issues as items are remedied
- Equipment startup: Log installation dates, startup dates, serial numbers (Component worksheet)
- Warranty collection: Compile all equipment warranties and attach to Document worksheet
- Final walkthrough: Verify all components documented, all systems tested

**Action Items**:
- Architect: Provide as-built finishes verification (update Space.FloorFinish, WallFinish, CeilingFinish)
- Commissioning Agent: Deliver final TAB report and equipment startup certificates
- All Subs: Deliver final O&M manuals, warranties, training materials
- Super: Complete asset inventory (all serial numbers, installation photos, startup dates)
- PM: Final COBie QA review; validate all required fields; resolve any gaps

### Substantial Completion (Punch List & Final COBie Export, Jul-Aug)

**Target COBie Readiness: 98%+**

- Generate final COBie export (all 18 worksheets populated)
- Validate against schema (primary keys, foreign keys, enums, required fields)
- Deliver to Facility Manager for system import and staff training
- Establish maintenance baseline (all equipment documented, all schedules defined)

**Action Items**:
- PM: Run `/cobie export` command; validate output
- Owner/Facility Manager: Review COBie export; request clarifications if needed
- Facility Operations: Import into CMMS system; train staff on asset lookup
- PM: Archive all source documents (submittals, O&M manuals, commissioning reports) as backing for COBie data
- PM: Schedule post-handover audit (30/60/90 days post-occupancy) to verify data accuracy

---



## Key Files & Documentation

**COBie Specification**:
- NBIMS-US v3.0 (publicly available at: http://buildingsmartalliance.org/cobie/)
- BS 1192-4:2014 (UK standard; subset of NBIMS)

**Foreman OS Integration**:
- /v31-build/skills/cobie-export/SKILL.md (this file)
- /project-data/cobie-export-config.json (project-specific configuration)
- /project-data/ (all data sources: *.json files)

**Project References**:
- Read from `project-config.json` for project memory, contacts, and status
- /project-data/plans-spatial.json (space/zone definitions from architectural plans)
- /project-data/specs-quality.json (equipment schedules from MEP specifications)
- /project-data/submittal-log.json (submitted equipment data sheets, O&M manuals)

---

**End of cobie-export SKILL.md**

This comprehensive documentation provides construction teams and facility managers with a complete guide for implementing COBie data export in the Foreman OS construction management system. Healthcare-specific extensions are available under the Facility-Type Extension section and activate automatically when the project's occupancy type includes healthcare, medical, or senior care.

## 7. Commands

### /cobie status

Display current COBie data readiness and completeness across all worksheets. Does not modify data.

**Example Output**:
```
COBie Status — Project: {project_name} (Job #{job_number})
Generated: 2026-02-19 10:30 AM

Data Completeness by Worksheet:
  Contact .............. 95% (11/12 contacts complete)
  Facility ............. 90% (building metadata ~ready)
  Floor ................ 100% (single floor complete)
  Space ................ 85% (16 bedrooms + common areas scheduled)
  Zone ................. 70% (HVAC zones ~ready; fire zones pending)
  Type ................. 65% (major equipment types 80%; secondary 50%)
  Component ............ 20% (will populate at closeout; 7 serialized so far)
  System ............... 70% (primary systems defined)
  Assembly ............. 50% (HVAC assembly 100%; others pending)
  Connection ........... 30% (HVAC coordination complete; other systems pending)
  Spare ................ 40% (pending O&M manual approvals)
  Resource ............. 35% (pending product data sheets)
  Job .................. 45% (standard maintenance schedule; customizations pending)
  Impact ............... 60% (energy model complete; environmental data pending)
  Document ............. 55% (3/5 major equipment submittals under review; expect 95% by 3/1/26)
  Attribute ............ 50% (standard data populated)
  Coordinate ........... 90% (grid system complete; GPS pending survey)
  Issue ................ 85% (6 submittals overdue; 7 daily reports logged; expect closure by 3/15/26)

Overall COBie Readiness: 58% (CONSTRUCTION PHASE)
Target Readiness: 85% @ Foundation Complete (03/20/26)
Full Readiness: 98% @ Substantial Completion (07/29/26)

Data Gaps & Recommendations:
  → Component serial numbers: Action required at equipment closeout — ensure commissioning team captures asset tags
  → O&M Manuals: {door_supplier}, Ferguson, {steel_supplier} packages overdue — escalate to PM for recovery
  → Commissioning reports: Expected May 2026 — ensure TAB consultant delivers in COBie-compatible format
  → GPS coordinates: Pending site survey by [Surveyor name] — follow up by 3/1/26
  → Fire system documentation: Contingent on design finalization — DUE by 2/28/26

Next Action: Run '/cobie export' when ready, or '/cobie gaps' to see detailed missing items.
```

### /cobie export

Generate the multi-tab COBie Excel workbook. Output: `{project_code}-COBie-Export-[timestamp].xlsx`

**Inputs**:
- Optional: `--phase design|construction|closeout` (default: based on current project status)
- Optional: `--filename custom-name.xlsx`
- Optional: `--include-notes` (append data source citations to each cell)

**Output**:
```
COBie Export Complete — 2026-02-19 10:35 AM

Workbook: /project-data/{project_code}-COBie-Export-2026-02-19.xlsx
File size: 2.4 MB
Worksheets: 18 tabs (all standard COBie v2.4)

Rows Generated:
  Contact .............. 12 contacts (GC, 8 subs, 4 suppliers, Architect TBD, Engineers TBD)
  Facility ............. 1 facility
  Floor ................ 1 floor (ground/level 1)
  Space ................ 29 spaces (16 bedrooms, 5 common areas, 8 support/mech, 4 restrooms, corridors)
  Zone ................. 14 zones (5 HVAC, 4 fire, 2 electrical, 1 plumbing, 2 departmental)
  Type ................. 48 equipment types (HVAC, plumbing, electrical, fire, doors, hardware, fixtures)
  Component ............ 31 component instances (7 with serial numbers; 24 pending closeout)
  System ............... 14 building systems
  Assembly ............. 8 assemblies (AHU package, water heater, fire alarm, nurse call, etc.)
  Connection ........... 12 system connections
  Spare ................ 15 spare parts (filters, oils, refrigerant, controls)
  Resource ............. 8 maintenance resources (test gauges, cleaning supplies, safety gear)
  Job .................. 22 maintenance jobs (with frequencies)
  Impact ............... 6 environmental metrics
  Document ............. 18 document references (spec sheets, manuals, commissioning reports)
  Attribute ............ 45 extended properties (custom data, project-specific fields)
  Coordinate ........... 8 location coordinates (grid system + key equipment locations)
  Issue ................ 6 open issues (submittals overdue, pending commissioning)

Validation Results:
  ✓ Primary key uniqueness: PASS (no duplicates detected)
  ✓ Foreign key integrity: PASS (all references valid)
  ✓ Data type conformance: PASS
  ⚠ Completeness warnings: 23 optional fields marked "n/a" (expected in construction phase)

Export ready for facility management system import.
Next: Review with Owner/Facility Manager for approval.
```

### /cobie validate [path-to-existing-export]

Validate an existing COBie export against the schema. Used to QA previous exports or validate exports from other sources.

**Example**:
```
/cobie validate /project-data/{project_code}-COBie-Export-2026-02-19.xlsx

Validation Report — 2026-02-19 10:40 AM

Worksheet Validation:
  ✓ Contact (12 rows) — Primary key unique, all required fields present
  ✓ Facility (1 row) — Complete
  ✓ Floor (1 row) — Complete
  ⚠ Space (29 rows) — 4 spaces missing finish specifications (optional field)
  ✓ Zone (14 rows) — All zones properly referenced to Space
  ⚠ Type (48 rows) — 12 equipment types missing warranty information (optional)
  ⚠ Component (31 rows) — 24 components lack serial numbers (expected, pending closeout)
  ✓ System (14 rows) — All systems defined
  ⚠ Assembly (8 rows) — 3 assemblies with incomplete component lists
  ✓ Connection (12 rows) — All connections valid
  ✓ Spare (15 rows) — All spare parts defined
  ⚠ Resource (8 rows) — 2 resources missing lead time (optional)
  ✓ Job (22 rows) — All maintenance jobs scheduled
  ✓ Impact (6 rows) — Environmental metrics complete
  ⚠ Document (18 rows) — 5 documents pending delivery (Issue worksheet notes these)
  ⚠ Attribute (45 rows) — 12 custom attributes not yet populated (design pending)
  ✓ Coordinate (8 rows) — Grid system complete, GPS data optional
  ✓ Issue (6 rows) — 6 open issues logged

Overall Validation: 89% PASS
  — 5 required fields missing (actionable)
  — 23 optional fields "n/a" (acceptable per COBie standard)
  — No broken references

Issues Requiring Action:
  1. Component serialization (24 items) — Due at closeout (07/29/26)
  2. Document delivery (5 items) — Due from suppliers by 03/15/26
  3. Custom attributes (12 items) — Due from Design team by 02/28/26

Recommended Action: Address open items; re-validate at next milestone (03/20/26).
```

### /cobie gaps

Identify all missing data with recommended collection sources and responsible parties.

**Example Output**:
```
COBie Data Gaps Report — 2026-02-19

Missing Data by Source (Actionable Items):

1. SUPPLIER DOCUMENTS (Contact: Submittals Coordinator)

   {door_supplier} Doors & Hardware Package (SUB-002 to SUB-005)
   ├─ Status: OVERDUE (24 days in review)
   ├─ Required for: Type, Spare, Document worksheets
   ├─ Action: Expedite submittal approval or issue RFI to {door_supplier}
   ├─ Owner: {pm_name} (PM)
   └─ Due: ASAP (critical path: door frames for rough-in start 04/21/26)

   {concrete_supplier} Concrete Mix Designs (SUB-001)
   ├─ Status: OVERDUE (17 days in review)
   ├─ Required for: Document worksheet (test reports)
   ├─ Action: Approve mix designs and initiate concrete testing
   ├─ Owner: Structural Engineer [TBD]
   └─ Due: ASAP (concrete work in progress)

   Ferguson Plumbing/Utilities (Quote pending)
   ├─ Status: Quote received, PO pending
   ├─ Required for: Type, Component, Spare worksheets
   ├─ Action: Issue PO for materials; request O&M manual with submittal
   ├─ Owner: {pm_name} (PM)
   └─ Due: By 02/28/26

   ICast Precast Structures (Quote pending)
   ├─ Status: Quote received, PO pending
   ├─ Required for: Component, Coordinate worksheets
   ├─ Action: Issue PO; request as-built data with delivery
   ├─ Owner: {pm_name} (PM)
   └─ Due: By 02/28/26

2. COMMISSIONING DATA (Contact: Commissioning Agent [TBD])

   HVAC System Commissioning & TAB
   ├─ Status: Pending (expected May 2026)
   ├─ Required for: Component (serial numbers), Job (maintenance), Document worksheets
   ├─ Action: Incorporate COBie data requirements into commissioning scope
   ├─ Owner: Project Manager + Commissioning Agent
   └─ Due: By 06/15/26 (before substantial completion)

   Fire Alarm System Commissioning
   ├─ Status: Pending (expected April 2026)
   ├─ Required for: Type, Component, Document worksheets
   ├─ Action: Ensure fire alarm contractor provides equipment schedule + test report
   ├─ Owner: Fire Alarm Inspector + System Provider
   └─ Due: By 04/30/26

   Electrical System Testing & Certification
   ├─ Status: Pending (expected June 2026)
   ├─ Required for: Component, Connection, Document worksheets
   ├─ Action: Request electrical test reports in COBie format
   ├─ Owner: Electrical Contractor + Licensed Electrician
   └─ Due: By 07/15/26

   Plumbing System Pressure & Flow Testing
   ├─ Status: Pending (expected April 2026)
   ├─ Required for: Component, Document worksheets
   ├─ Action: Capture test results and include in document references
   ├─ Owner: Plumbing Contractor + Inspector
   └─ Due: By 04/30/26

3. SITE SURVEY DATA (Contact: Land Surveyor [TBD])

   GPS Coordinates & Topography
   ├─ Status: Pending (design survey available; final survey pending)
   ├─ Required for: Facility, Coordinate worksheets
   ├─ Action: Request final survey with building and major equipment coordinates
   ├─ Owner: Project Surveyor
   └─ Due: By 03/01/26

4. DESIGN TEAM DELIVERABLES (Contact: Architect [TBD], Engineers [TBD])

   Architectural Room Finish Schedule (as-built)
   ├─ Status: Design available; as-built pending closeout
   ├─ Required for: Space worksheet (FloorFinish, WallFinish, CeilingFinish)
   ├─ Action: Architect to verify finishes at final inspection; provide as-built updates
   ├─ Owner: Architect + {framing_sub} Framing/Drywall Sub
   └─ Due: By 07/15/26

   MEP Equipment Cut Sheets (All)
   ├─ Status: Partial (HVAC partial; plumbing/electrical pending)
   ├─ Required for: Type, Spare, Document worksheets
   ├─ Action: Collect approved submittals and attach to COBie export
   ├─ Owner: Design Engineers + Submittals Coordinator
   └─ Due: By 06/01/26

   Fire Protection System Design (if applicable)
   ├─ Status: Under review per project memory ("Contingent on design decisions")
   ├─ Required for: Type, Component, System, Job, Document worksheets
   ├─ Action: Clarify fire protection scope (sprinkler, halon, etc.); request design & manuals
   ├─ Owner: Architect + Fire Protection Engineer
   └─ Due: By 02/28/26

5. PROJECT TEAM CONTACTS (Contact: PM {pm_name})

   Architect Information
   ├─ Status: "TBD" in project data
   ├─ Required for: Contact worksheet
   ├─ Action: Confirm architect name, contact info, role
   ├─ Owner: {pm_name} (PM)
   └─ Due: By 02/20/26

   Structural Engineer Information
   ├─ Status: "Yeiser (referenced on MMI shop drawings)" — role/contact TBD
   ├─ Required for: Contact worksheet
   ├─ Action: Clarify Yeiser role; add to contact list with email/phone
   ├─ Owner: {pm_name} (PM)
   └─ Due: By 02/20/26

   Electrical Contractor
   ├─ Status: "SC-{job_number}-08 PENDING" (not yet awarded)
   ├─ Required for: Contact, Type, Component worksheets
   ├─ Action: Award electrical sub contract ASAP (critical path for rough-in 04/21/26)
   ├─ Owner: {pm_name} (PM)
   └─ Due: By 02/28/26 (3 weeks until PEMB Erection 03/23/26)

6. FIELD CLOSEOUT DATA (Contact: Super {superintendent_name})

   Equipment Serial Numbers & Asset Tags
   ├─ Status: 7/31 components serialized; 24 pending
   ├─ Required for: Component worksheet (required field)
   ├─ Action: Assign asset tags at equipment delivery/installation; photograph serial plates
   ├─ Owner: Super + Receiving Coordinator
   └─ Due: By 07/15/26 (before substantial completion)

   Installation Dates & Commissioning Records
   ├─ Status: Pending (expect entries from 04/15/26 onward)
   ├─ Required for: Component, Job, Document worksheets
   ├─ Action: Log installation/startup dates in project daily reports + commissioning data
   ├─ Owner: Super + Trade Contractors + Commissioning Agent
   └─ Due: Ongoing (by 07/29/26 substantial completion)

   O&M Manuals & Warranties
   ├─ Status: Pending supplier delivery (expected with final payment invoices)
   ├─ Required for: Spare, Resource, Job, Document worksheets
   ├─ Action: Collect all O&M manuals at closeout; scan and attach to COBie export
   ├─ Owner: Super + Submittals Coordinator + GC Office Manager
   └─ Due: By 07/20/26 (before final walkthrough)

Summary of Actions:
  Immediate (by 02/28/26):
    • Expedite {door_supplier} door submittal approval
    • Approve {concrete_supplier} concrete mix designs
    • Issue POs for Ferguson & ICast
    • Confirm architect & engineers contact info
    • Award electrical sub contract
    • Clarify fire protection scope

  Near-term (by 03/15/26):
    • Receive all supplem O&M manual submittals
    • Incorporate COBie requirements into commissioning scope
    • Conduct site survey with equipment coordinates

  Ongoing (through 07/29/26):
    • Capture equipment serial numbers at delivery
    • Log installation/startup dates
    • Collect commissioning reports
    • Verify room finish specifications
    • Close all punch list issues

Current COBie Gap Score: 42% of required data missing (CONSTRUCTION PHASE EXPECTED)
Target Gap Score: 5% by substantial completion (07/29/26)
```

---


---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.


