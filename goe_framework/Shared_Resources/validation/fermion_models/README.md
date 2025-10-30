# Fermion Mass Models Comparison

**Location:** `Shared_Resources/validation/fermion_models/`  
**Date:** 2025-10-25  
**Status:** Validation complete, figures ready for publication

---

## Overview

Statistical comparison of two fermion mass hierarchy models in the GoE framework:

- **Model A:** Power law (m ∝ |q|^p, charge-based)
- **Model B:** Golden ratio quantization (m = m₀ φⁿ, topology-based)

**Result:** Model B (φⁿ quantization) shows superior statistical performance across all fermion sectors.

---

## Files

### Source Scripts

| File | Description | Generates |
|------|-------------|-----------|
| `goe_fermion_models_comparison.py` | Main comparison analysis | 3 PDFs (leptons, up, down) |
| `goe_strong_force_analysis.py` | Strong force contribution | 1 PDF (strong force) |

### Generated Figures (PDF)

| Figure | Sector | Comparison |
|--------|--------|------------|
| `goe_models_comparison_leptons.pdf` | e, μ, τ | Model A vs B + MCMC |
| `goe_models_comparison_up_quarks.pdf` | u, c, t | Model A vs B + MCMC |
| `goe_models_comparison_down_quarks.pdf` | d, s, b | Model A vs B + MCMC |
| `goe_strong_force_analysis.pdf` | All quarks | Strong force contribution |

---

## Reproduction Instructions

### Prerequisites
```bash
pip install numpy scipy matplotlib pandas seaborn
```

### Generate All Comparison Plots
```bash
cd Shared_Resources/validation/fermion_models
python goe_fermion_models_comparison.py
```

**Output:**
- `goe_models_comparison_leptons.pdf`
- `goe_models_comparison_up_quarks.pdf`
- `goe_models_comparison_down_quarks.pdf`

### Generate Strong Force Analysis
```bash
python goe_strong_force_analysis.py
```

**Output:**
- `goe_strong_force_analysis.pdf`

---

## Key Results

### Model B (φⁿ Quantization) Performance

| Sector | MAPE | R² | χ²/dof |
|--------|------|-----|--------|
| **Leptons** | 2.15% | 0.9997 | 0.089 |
| **Up quarks** | 7.95% | 0.9992 | 0.412 |
| **Down quarks** | 8.02% | 0.9991 | 0.389 |
| **Combined** | 7.28% | 0.9994 | 0.298 |

### Statistical Significance

- **ΔBIC (Model B vs A):** -13.5 (decisive evidence for Model B)
- **Permutation p-value:** 0.004476 (rejects null hypothesis)
- **MCMC convergence:** Gelman-Rubin R̂ ≈ 1.000

---

## Data Sources

- **Fermion masses:** PDG 2024 (Particle Data Group)
- **φ (golden ratio):** (1 + √5)/2 = 1.618034... (exact)
- **Topological charges n:** Derived from C₅ dihedral symmetry

---

## Citation

If using these analyses in publications:

```
Camargo, G. (2025). Geometrodynamics of Entropy: Fermion Mass Quantization 
from Extended Wheeler-DeWitt Framework. GitHub: github.com/infolake/goe_framework
```

---

**Last updated:** 2025-10-30  
**Author:** Dr. Guilherme de Camargo (camargo@phiq.io)

