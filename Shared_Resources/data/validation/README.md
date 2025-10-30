# VALIDATION Data Directory

## Description
Resultados compilados de validação (LOOCV, BIC, cross-validation)

## Contents
7 files, 0.08 MB total

### Files

| Filename | Size (MB) | Pattern Matched |
|----------|-----------|------------------|
| `goe_complete_summary.json` | 0.0 | `*goe_*_summary.json` |
| `goe_complete_telemetry.json` | 0.08 | `*goe_*_telemetry.json` |
| `robust_statistical_analysis_results.json` | 0.0 | `robust_statistical_analysis*.json` |
| `tensor_analysis_summary.csv` | 0.0 | `tensor_analysis_summary.*` |
| `tensor_analysis_summary.json` | 0.0 | `tensor_analysis_summary.*` |
| `tensor_summary.json` | 0.0 | `tensor_summary.json` |
| `validation_results.json` | 0.0 | `*validation*.json` |


## File Formats


### Validation Results Format
- **`.json` files**: Structured validation metrics
  - LOOCV: Leave-One-Out Cross-Validation errors
  - BIC: Bayesian Information Criterion
  - MAPE: Mean Absolute Percentage Error
  - RMSE: Root Mean Squared Error
- **Tensor summaries**: Decomposition analysis metadata


## Reproducibility

To reproduce these results:
1. Install dependencies: `pip install -r requirements.txt`
2. Run corresponding script in `scripts/` directory
3. Compare output with files in this directory

## Metadata

- **Generated**: 2025-10-29 16:46:53
- **Framework**: Geometrodynamics of Entropy (GoE)
- **Paper**: arXiv submission (main.tex in papers/arxiv_submission/)
- **Repository**: https://github.com/infolake/goe_framework
- **DOI**: 10.5281/zenodo.14513152

## Questions?

See main repository README.md or contact authors via GitHub Issues.
