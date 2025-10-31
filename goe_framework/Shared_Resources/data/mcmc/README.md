# MCMC Data Directory

## Description
Resultados de amostragem MCMC Bayesiana (chains, posteriors)

## Contents
3 files, 37.15 MB total

### Files

| Filename | Size (MB) | Pattern Matched |
|----------|-----------|------------------|
| `mcmc_analysis_report.json` | 0.0 | `*mcmc*.json` |
| `mcmc_detailed_report.json` | 0.0 | `*mcmc*.json` |
| `mcmc_results_large.npz` | 37.15 | `*mcmc*.npz` |


## File Formats


### MCMC Chain Format
- **`.npz` files**: Compressed NumPy arrays containing:
  - `samples`: MCMC chain samples (shape: [n_iterations, n_parameters])
  - `log_prob`: Log-probability values
  - `acceptance`: Acceptance rates
- **Seeds**: SHA256("GoE")[:8] for reproducibility
- **Sampler**: emcee 3.1 (Goodman-Weare affine-invariant)
- **Diagnostics**: Gelman-Rubin R̂ < 1.01, ESS > 400


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
