# GPU_TENSORS Data Directory

## Description
Tensores em formato PyTorch (GPU-accelerated computations)

## Contents
4 files, 30.52 MB total

### Files

| Filename | Size (MB) | Pattern Matched |
|----------|-----------|------------------|
| `mape_bootstrap_1M_clean.pt` | 7.63 | `*_clean.pt` |
| `mape_bootstrap_1M_gpu.pt` | 7.63 | `*_gpu.pt` |
| `rmse_bootstrap_1M_clean.pt` | 7.63 | `*_clean.pt` |
| `rmse_bootstrap_1M_gpu.pt` | 7.63 | `*_gpu.pt` |


## File Formats


### PyTorch Tensor Format
- **`.pt` files**: PyTorch tensors (load with `torch.load()`)
- **`_gpu.pt`**: Optimized for GPU computation
- **`_clean.pt`**: Post-processed, outlier-filtered versions
- **Compatibility**: PyTorch 2.0+, CUDA 11.8+


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
