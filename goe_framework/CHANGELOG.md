# Changelog - GoE Framework

All notable changes to the GoE Framework will be documented in this file.

## [v2.0] - 2025-10-29

### 🎯 Major Release - arXiv Submission Ready

#### Added
- **MCMC Analysis Package** (39 MB - complete audit trail)
  - mcmc_results_large.npz (37 MB, 1M samples, score 20/20)
  - 4 analysis scripts: comprehensive, detailed, g-2, GPU-accelerated
  - 2 JSON reports: analysis + detailed statistics
  - Diagnostic plot: trace + posterior + convergence (1.8 MB)
  - Organized: Shared_Resources/data/mcmc/, scripts/mcmc/, figures/mcmc/

- **Complete statistical validation suite**
  - 1M Monte Carlo samples validation
  - 500k permutation tests (p=0.004476)
  - 100k bootstrap replicates
  - LOOCV with MAPE=7.28%
  
- **arXiv submission package** (1.3 MB)
  - Final corrected main.tex (1764 lines)
  - 14 PDF figures (vectorial)
  - Complete bibliography
  - Submission guide (SUBMIT_TO_ARXIV.md)
  
- **Statistical documentation**
  - docs/statistical_validation_report.md (technical)
  - docs/statistical_validation_summary.md (paper integration)
  - docs/statistical_results_organization.md
  
- **Automated scripts**
  - prepare_arxiv_package.py
  - integrate_statistical_validation.py
  - cleanup_repository.py

#### Fixed
- **Critical parameter correction**: 4 → 2 calibrated parameters
  - Only m₀(ℓ) and α are calibrated
  - m₀(u) and m₀(d) are DERIVED from geometry
  - Represents ~90% reduction vs Standard Model (19+ → 2)
  
- **Numerical consistency** across entire paper
  - MAPE unified to 7.28% (12 locations)
  - z_b unified to 3.68×10⁴ (12 locations)
  - ∆BIC unified to 13.5 (3 locations)
  
- **Mathematical derivation** of η
  - Corrected algebraic steps
  - η = 0.927 from holographic projection
  - Added cross-reference to Sec. 3.2.1 for φ derivation

#### Changed
- **Repository cleanup**
  - Removed ~50 temporary files (aux, log, backups)
  - Removed PNG files (kept 14 PDFs)
  - Moved 15 internal reports to Goe_Toolkit_Arquivo
  - Professional structure maintained
  
- **PDF renamed**: main.pdf (was long descriptive name)
- **All figures**: PDF format only (arXiv standard)

#### Repository Structure
```
goe_framework/
├── docs/                      (3 statistical MDs)
├── Shared_Resources/          (notebooks + data)
│   ├── notebooks/             (3 Jupyter notebooks)
│   └── data/                  (bounce CSVs)
├── papers/arxiv_submission/   (clean, production-ready)
│   ├── main.tex               (1764 lines, corrected)
│   ├── figures/               (14 PDFs)
│   ├── arxiv_package/         (working version)
│   └── arxiv_submission_final_corrected.zip (FINAL)
├── README.md
├── requirements.txt
└── LICENSE
```

### 📊 Paper Statistics
- **Pages**: 45
- **Figures**: 14 (PDF)
- **Tables**: ~10
- **Equations**: ~150
- **References**: 40+
- **Calibrated parameters**: 2 (electron mass + bounce stiffness)
- **Reduction vs SM**: ~90%

### 🔬 Validation Results
- **LOOCV MAPE**: 7.28% (leptons: 2.15%, quarks: 7.95%)
- **Monte Carlo**: 1M samples, R̂ ≈ 1.000
- **Permutation**: p = 0.004476 (rejects chance)
- **Bootstrap**: IC95 [7.266%, 7.285%]
- **Effect Size**: Cohen's d = -1.014, KS = 0.995524

### 🚀 Ready for Submission
- ✅ All corrections applied
- ✅ Numerical consistency verified
- ✅ Mathematical derivations correct
- ✅ Repository clean and professional
- ✅ arXiv package ready (1.3 MB)

---

## [v1.0] - 2025-10-28

### Initial Public Release
- Core GoE framework
- Basic documentation
- Jupyter notebooks
- Initial paper draft

---

## DOI References
- **v2.0**: [Awaiting Zenodo DOI]
- **v1.0**: 10.5281/zenodo.17471368

