# QUIPU-DECODE Framework v1.0 - Data and Datasets

## Cornell University Quipu Database

The Cornell University maintains a comprehensive database of quipus available at:
**https://courses.cit.cornell.edu/quipu/contents.htm**

### Database Overview

This dataset represents one of the most extensive collections of quipu data available for research, containing detailed information about:

- **Physical Characteristics**: Materials, colors, dimensions, knot types
- **Structural Data**: Hierarchical organization, cord arrangements
- **Archaeological Context**: Provenance, dating, excavation information
- **Visual Documentation**: High-resolution images and 3D scans (where available)

### Dataset Structure

The Cornell database includes:

1. **Quipu Catalog**: Systematic numbering and classification system
2. **Visual Documentation**: Photographic records of each quipu
3. **Measurement Data**: Precise physical measurements
4. **Contextual Information**: Archaeological and cultural context
5. **Interpretation Notes**: Existing scholarly interpretations

### Data Format Compatibility

The Cornell dataset can be integrated with the QUIPU-DECODE framework by converting the data to our standardized JSON format:

```python
# Example conversion structure
cornell_quipu = {
    "quipu_id": "CORNELL_001",  # Cornell catalog number
    "collection_info": {
        "source": "Cornell University",
        "catalog_number": "K001",
        "url": "https://courses.cit.cornell.edu/quipu/k001.htm"
    },
    "primary_cord": {
        "material": "cotton",
        "color": "natural",
        "length": 45.5
    },
    "pendant_cords": [...],  # Converted from Cornell data
    "materials": ["cotton", "wool"],
    "colors": ["natural", "red", "blue"],
    "hierarchy_levels": 3,
    "total_knots": 25,
    "archaeological_context": {
        "site": "Pachacamac",
        "period": "Late Horizon",
        "culture": "Inca"
    }
}
```

### Integration with Framework

To use Cornell data with QUIPU-DECODE:

1. **Download Data**: Access the Cornell database online
2. **Convert Format**: Transform to QUIPU-DECODE JSON format
3. **Load into Framework**: Use standard analysis pipeline
4. **Validate Results**: Compare with existing interpretations

### Research Applications

The Cornell dataset enables:

- **Pattern Analysis**: Identification of recurring motifs across collections
- **Comparative Studies**: Analysis of quipus from different regions and periods
- **Statistical Validation**: Large-scale quantitative analysis
- **Cognitive Modeling**: Testing cognitive scaffolding hypotheses
- **Classification Studies**: Automated functional classification

### Data Quality and Completeness

The Cornell database provides:

- **High Completeness**: Most entries include comprehensive data
- **Standardized Measurements**: Consistent measurement protocols
- **Visual Verification**: Photographic documentation for validation
- **Scholarly Context**: Interpretations by expert researchers

### Access and Usage

**Primary Access Point:**
- URL: https://courses.cit.cornell.edu/quipu/contents.htm
- Format: HTML pages with embedded data and images
- Access: Publicly available for research purposes

**Recommended Workflow:**
1. Browse the online catalog
2. Download relevant quipu data
3. Convert to QUIPU-DECODE format
4. Run analysis with framework
5. Validate against existing interpretations

### Citation Requirements

When using Cornell data:

```bibtex
@misc{cornell_quipu_database,
  title={Quipu Database},
  author={Cornell University},
  url={https://courses.cit.cornell.edu/quipu/},
  note={Accessed: [Date]}
}
```

### Integration Example

```python
from quipu_decode.core import QuipuAnalyzer
from quipu_decode.database import ReferenceDatabase

# Load Cornell data (converted to JSON)
analyzer = QuipuAnalyzer()
results = analyzer.analyze_from_json('data/cornell_quipu_001.json')

# Add to reference database for comparative analysis
ref_db = ReferenceDatabase()
# ... add Cornell quipu to reference collection

# Compare with other quipus
comparison = ref_db.perform_comparative_analysis(
    patterns=results.patterns_identified,
    cognitive_proxies=results.cognitive_proxies,
    statistical_tests=results.statistical_tests
)
```

## Other Datasets

### Museum Collections

The framework is designed to work with data from major museum collections:

1. **British Museum** (London)
2. **Larco Museum** (Lima)
3. **Brooklyn Museum** (New York)
4. **Museum of Fine Arts** (Boston)
5. **Peabody Museum** (Harvard)

### Archaeological Excavations

Integration with excavation data from:

1. **Pachacamac Archaeological Project**
2. **Cuzco Valley Archaeological Project**
3. **Machu Picchu Excavations**
4. **Inca Road System Surveys**

### Digital Archives

Compatible with digital archives providing:

1. **3D Scans**: For structural analysis
2. **High-Resolution Images**: For color and material analysis
3. **Metadata Standards**: Dublin Core, MODS, etc.

## Data Standards

### Quipu Data Format

The framework expects standardized quipu data:

```json
{
  "quipu_id": "string",
  "primary_cord": {...},
  "pendant_cords": [...],
  "materials": ["string"],
  "colors": ["string"],
  "knot_types": ["string"],
  "hierarchy_levels": "integer",
  "total_knots": "integer",
  "archaeological_context": {...}
}
```

### Quality Metrics

Data quality is assessed based on:

- **Completeness**: Percentage of required fields present
- **Consistency**: Internal consistency of measurements
- **Accuracy**: Agreement with visual documentation
- **Contextual Richness**: Amount of archaeological context

### Validation Procedures

The framework includes validation for:

- **Format Validation**: JSON schema compliance
- **Data Completeness**: Required field verification
- **Measurement Consistency**: Logical consistency checks
- **Contextual Plausibility**: Archaeological context validation

## Contributing Data

### Submission Guidelines

To contribute quipu data to the framework:

1. **Standardize Format**: Convert to QUIPU-DECODE JSON format
2. **Validate Data**: Run framework validation procedures
3. **Document Source**: Include provenance and citation information
4. **Test Integration**: Verify compatibility with analysis pipeline

### Data Sharing

The framework supports:

- **Export Functions**: Export results in multiple formats
- **Reference Database**: Share reference collections
- **Comparative Analysis**: Cross-collection studies
- **Validation Studies**: Methodology validation across datasets

## Future Developments

### Planned Dataset Integrations

1. **3D Scanning Integration**: Support for STL/OBJ files
2. **Image Analysis Pipeline**: Automated feature extraction from photos
3. **Metadata Harvesting**: Automated extraction from museum databases
4. **Linked Open Data**: Integration with LOD standards

### Machine Learning Datasets

Future development of:

1. **Training Datasets**: Labeled data for pattern recognition
2. **Validation Sets**: Ground truth for algorithm testing
3. **Benchmark Collections**: Standard evaluation datasets

## Support and Resources

### Documentation
- **Framework Guide**: Complete usage documentation
- **API Reference**: Detailed function documentation
- **Examples**: Sample code and tutorials

### Community
- **Research Network**: Collaboration with quipu researchers
- **User Forum**: Community support and discussion
- **Development Team**: Technical support and feature requests

### Technical Resources
- **Data Conversion Tools**: Scripts for format conversion
- **Validation Scripts**: Automated data quality assessment
- **Analysis Templates**: Standardized analysis workflows
