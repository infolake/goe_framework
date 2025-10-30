# PERMUTATION Data Directory

## Description
Testes de permutação (null hypothesis, p-values)

## Contents
8 files, 4.55 MB total

### Files

| Filename | Size (MB) | Pattern Matched |
|----------|-----------|------------------|
| `goe_complete_perm_results.npy` | 0.38 | `*perm_results*` |
| `mape_permutation_100K.npy` | 0.76 | `*permutation*.npy` |
| `mape_permutation_100K.pt` | 0.76 | `*permutation*.pt` |
| `mape_permutation_100K_clean.npy` | 0.76 | `*permutation*.npy` |
| `mape_permutation_100K_clean.pt` | 0.76 | `*permutation*.pt` |
| `mape_permutation_100K_gpu.pt` | 0.76 | `*permutation*.pt` |
| `mape_permutation_100k_analysis.png` | 0.37 | `mape_permutation_*` |
| `test_goe_perm_results.npy` | 0.0 | `*perm_results*` |


## File Formats


### Permutation Test Format
- **`.npy` files**: Arrays with permuted MAPE values
- **Number of permutations**: 10,000 - 500,000
- **Seed**: 2025 for reproducibility
- **Null hypothesis**: Random φⁿ assignments produce same fit quality
- **p-value calculation**: Empirical (# permutations < observed MAPE) / total


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
