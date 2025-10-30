# PHI_SAMPLES Data Directory

## Description
Amostras de sensibilidade ao parâmetro phi (golden ratio)

## Contents
5 files, 3.80 MB total

### Files

| Filename | Size (MB) | Pattern Matched |
|----------|-----------|------------------|
| `phi_samples_100K.npy` | 0.76 | `phi_samples_*.npy` |
| `phi_samples_100K.pt` | 0.76 | `phi_samples_*.pt` |
| `phi_samples_100K_clean.npy` | 0.76 | `phi_samples_*.npy` |
| `phi_samples_100K_clean.pt` | 0.76 | `phi_samples_*.pt` |
| `phi_samples_100K_gpu.pt` | 0.76 | `phi_samples_*.pt` |


## File Formats


### Phi Sensitivity Format
- **`.npy` files**: Samples varying φ parameter
- **Number of samples**: 100,000
- **Range**: φ ± 3σ around golden ratio (1.618033...)
- **Purpose**: Test robustness to φ deviations


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
