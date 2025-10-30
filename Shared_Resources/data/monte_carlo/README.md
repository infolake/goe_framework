# MONTE_CARLO Data Directory

## Description
Simulações Monte Carlo (sensitivity scans, error propagation)

## Contents
8 files, 4.96 MB total

### Files

| Filename | Size (MB) | Pattern Matched |
|----------|-----------|------------------|
| `goe_complete_mc_results.npy` | 0.76 | `*mc_results*` |
| `mape_monte_carlo_100K.npy` | 0.76 | `*monte_carlo*.npy` |
| `mape_monte_carlo_100K.pt` | 0.76 | `*monte_carlo*.pt` |
| `mape_monte_carlo_100K_clean.npy` | 0.76 | `*monte_carlo*.npy` |
| `mape_monte_carlo_100K_clean.pt` | 0.76 | `*monte_carlo*.pt` |
| `mape_monte_carlo_100K_gpu.pt` | 0.76 | `*monte_carlo*.pt` |
| `mape_monte_carlo_100k_analysis.png` | 0.39 | `mape_monte_carlo_*` |
| `test_goe_mc_results.npy` | 0.01 | `*mc_results*` |


## File Formats


### Monte Carlo Format
- **`.npy` files**: Simulation results arrays
- **Number of samples**: 100,000 - 1,000,000
- **Purpose**: Sensitivity analysis, error propagation
- **Parameters varied**: α, R_Θ, φ within experimental uncertainties


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
