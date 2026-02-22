# AI-Assisted Takeoff Methodology

## Overview
AI-powered quantity takeoff tools are transforming construction estimating by automating the measurement of plan elements. However, AI is a co-pilot, not a pilot — the machine counts, the human validates. This reference defines the methodology for integrating AI-assisted takeoffs with traditional estimating practices.

## The AI Co-Pilot Model

### What AI Does Well
- Counting repetitive elements (doors, windows, outlets, fixtures)
- Measuring areas (floor area, wall area, roof area, paving)
- Measuring linear elements (walls, pipes, conduit runs, curbs)
- Detecting and classifying plan symbols
- Comparing quantities across drawing revisions
- Processing multiple sheets simultaneously

### What AI Does Not Do Well
- Interpreting ambiguous details or design intent
- Reading heavily annotated or cluttered plan areas
- Understanding scope boundaries (what's in vs out of contract)
- Applying judgment about constructability or means/methods
- Handling non-standard symbols or firm-specific conventions
- Estimating items not explicitly shown on plans (temporary work, site logistics)

### The Human Role
- Define measurement scope and boundaries
- Review and validate AI-generated quantities
- Apply professional judgment on ambiguous items
- Add items not visible on plans (general conditions, temporary work)
- Adjust for field conditions and constructability
- Apply waste factors, productivity adjustments, and pricing

## Confidence Scoring Workflow

AI takeoff tools should generate confidence scores for each measurement. The verification level depends on the confidence score:

### High Confidence (>95%)
- **Action**: Auto-accept with spot-check sampling
- **Spot-check rate**: 5-10% of items (random sample)
- **Typical items**: Standard room areas, repetitive fixture counts, simple linear measurements
- **Verification method**: Compare AI count against manual count on 2-3 representative sheets

### Medium Confidence (85-95%)
- **Action**: Review all flagged items, verify against drawings
- **Review rate**: 100% of flagged items + 20% random sample of accepted items
- **Typical items**: Complex shapes, crowded plan areas, items near drawing edges, small-scale details
- **Verification method**: Manual measurement of flagged items, comparison with AI measurement

### Low Confidence (<85%)
- **Action**: Manual takeoff required — AI flags these for human attention
- **Typical items**: Items in heavily annotated areas, non-standard symbols, items requiring cross-sheet reference, scope boundary items
- **Verification method**: Full manual takeoff with AI measurement as reference only

## Verification Protocol by Dollar Threshold

The rigor of verification should match the financial impact:

| Line Item Value | Verification Level | Who Reviews |
|----------------|-------------------|-------------|
| <$10K | AI-only with sample audit | Estimator (spot check) |
| $10K-$50K | AI + Senior estimator review | Senior estimator |
| $50K-$200K | Full manual verification required | Chief estimator |
| >$200K | Independent dual takeoff (AI + manual) | Chief estimator + PM review |

## CSI MasterFormat Integration

AI tools should map detected elements to CSI division codes:

| Division | Example AI-Detected Elements |
|----------|---------------------------|
| 03 Concrete | Slab areas, footing dimensions, wall volumes |
| 04 Masonry | CMU wall lengths, block counts, bond beam LF |
| 05 Metals | Structural steel piece counts, connection counts, misc metals LF |
| 06 Wood/Plastics | Framing member counts, sheathing areas, blocking LF |
| 07 Thermal/Moisture | Insulation areas, roofing squares, waterproofing SF |
| 08 Openings | Door counts by type, window counts by size, hardware sets |
| 09 Finishes | Paint areas, flooring SF by type, ceiling grid SF, tile SF |
| 22 Plumbing | Fixture counts, pipe runs (LF by diameter), valve counts |
| 23 HVAC | Ductwork LF by size, diffuser counts, equipment counts |
| 26 Electrical | Device counts, conduit LF, wire LF, panel counts |

## Measurement Types and AI Accuracy

| Measurement Type | Units | Typical AI Accuracy | Common Errors |
|-----------------|-------|-------------------|---------------|
| Area | SF | 95-99% | Misses cutouts, wrong boundary |
| Linear | LF | 90-97% | Scale calibration, curved segments |
| Volume | CY | 85-95% | Depth assumption errors |
| Count | EA | 92-98% | Misses hidden/overlapping symbols |
| Weight | tons | 80-90% | Depends on size classification |

## Common AI Detection Errors

### Scale Calibration Errors
- AI reads the wrong scale from the title block
- Fix: Always verify scale calibration against a known dimension on the drawing

### Congested Area Misses
- Dense plan areas cause AI to miss or double-count items
- Fix: Zoom to congested areas and verify counts manually

### Symbol Misidentification
- Similar-looking symbols confused (outlet vs switch, FD vs SD)
- Fix: Review symbol legend and verify AI's symbol classification

### Cross-Sheet Items
- Items that span multiple sheets may be double-counted or missed
- Fix: Define sheet boundaries clearly and reconcile totals

### Scope Boundary Errors
- AI measures elements outside the contract scope boundary
- Fix: Define scope boundaries on plans before AI processing

## Best Practices

1. **Calibrate first**: Always verify the AI tool's scale calibration before accepting any measurements
2. **Start with high-confidence items**: Build trust by verifying AI accuracy on simple items first
3. **Document everything**: Record which quantities came from AI vs manual takeoff
4. **Track accuracy over time**: Keep a log of AI accuracy by measurement type to calibrate trust
5. **Never skip the dollar-threshold checks**: High-value items always get manual verification
6. **Use AI for revision comparison**: Where AI really shines is comparing rev to rev changes quickly
