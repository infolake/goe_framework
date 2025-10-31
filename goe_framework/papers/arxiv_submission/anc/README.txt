ANCILLARY FILES FOR ARXIV SUBMISSION
=====================================

Paper: Geometrodynamics of Entropy: Fermion Mass Quantization and 
       Cosmological Bounce from an Extended Wheeler-DeWitt Framework

Authors: Dr. Guilherme de Camargo
Date: October 2025
arXiv Category: hep-th (High Energy Physics - Theory)

=====================================
PURPOSE
=====================================

These ancillary files provide complete computational reproducibility for
all numerical results, statistical validations, and plots presented in
the main paper.

=====================================
FILE ORGANIZATION
=====================================

COMPUTATIONAL NOTEBOOKS:
  01_goe_fermion_hierarchy_pentagonal.ipynb
    - Core fermion mass quantization validation
    - MCMC analysis with 1M samples
    - Statistical tests (LOOCV, permutation, bootstrap)
    - Figures 1-4 in main paper
    
  02_goe_computational_protocol.ipynb
    - Extended computational protocol (CITED in paper)
    - Bayesian model comparison (BIC analysis)
    - Convergence diagnostics
    - Supplementary material figures
    - Referenced in main text (lines 906, 937, 1688)
    
  03_goe_unified_quantum_foundations.ipynb
    - Unified quantum foundations (Preprint Ready)
    - Wheeler-DeWitt + natural bounce from first principles
    - CMB/BBN constraints with comparison table
    - JWST LRD phenomena explained
    - Einstein-Cartan connection (torsion-spin coupling)

VALIDATION SCRIPTS:
  validation_fermion_models_comparison.py
    - Model A (power law) vs Model B (phi^n quantization)
    - PDG 2025 experimental data
    - CSV/JSON output generation
    
  validation_strong_force_analysis.py
    - Nuclear fiber analysis
    - Strong coupling constant calculation
    - Hadron mass predictions

DATA FILES:
  fermion_models_comparison_results.json
    - Complete comparison statistics
    - Model parameters and predictions
    - BIC values (Delta_BIC = 13.545)
    
  fermion_models_comparison_results.csv
    - Tabular format for analysis
    - All 9 charged fermions
    
  strong_force_analysis_results.json
    - Hadron mass calculations
    - Coupling constant evolution
    
  strong_force_analysis_coupling.csv
    - alpha_s(Q) at various energy scales

DOCUMENTATION:
  INSTALL.txt
    - Software requirements
    - Installation instructions
    
  REPRODUCE.txt
    - Step-by-step reproduction guide
    - Expected runtime estimates

=====================================
DATA SOURCES
=====================================

Experimental fermion masses: Particle Data Group 2025
  https://pdg.lbl.gov/2025/

Reference:
  R.L. Workman et al. (Particle Data Group),
  Prog. Theor. Exp. Phys. 2022, 083C01 (2022)
  Updated 2025: https://pdg.lbl.gov/2025/tables/

=====================================
COMPUTATIONAL ENVIRONMENT
=====================================

Minimum requirements:
  - Python 3.10 or higher
  - NumPy 1.24+
  - SciPy 1.10+
  - Matplotlib 3.8+
  - Pandas 2.0+
  - Jupyter (for notebooks)

Recommended for full MCMC:
  - 16 GB RAM
  - GPU with CUDA support (optional, for acceleration)

=====================================
KEY NUMERICAL RESULTS
=====================================

Fermion Mass Quantization (Model B):
  MAPE = 7.28%
  Delta_BIC = 13.545 (decisive evidence)
  p-value = 0.004476 (permutation test)

Statistical Validation:
  LOOCV: Median MAPE = 7.28%, P95 = 15.8%
  Monte Carlo: 1M samples, convergence verified
  Bootstrap: 100k iterations, CI95 = [7.266, 7.285]%
  Effect Size: KS statistic = 0.9955

Cosmological Predictions:
  Bounce redshift: z_b = 3.68e4
  Stiff-matter parameter: alpha ~ 7.3e-14 H_0^2

=====================================
REPRODUCTION TIME ESTIMATES
=====================================

Quick validation (fermion models only):
  Runtime: ~10-15 seconds
  Output: CSV/JSON files, 4 PDF plots

Full notebook execution:
  Runtime: ~5-10 minutes (without MCMC)
  Runtime: ~2-4 hours (with 1M MCMC samples)

=====================================
CITATION
=====================================

If you use these computational materials, please cite:

  G. de Camargo, "Geometrodynamics of Entropy: Fermion Mass 
  Quantization and Cosmological Bounce from an Extended 
  Wheeler-DeWitt Framework," arXiv:XXXX.XXXXX [hep-th] (2025).

=====================================
CONTACT
=====================================

For questions or issues:
  Email: camargo@phiq.io
  GitHub: https://github.com/infolake/goe_framework
  Zenodo DOI: 10.5281/zenodo.17479743

=====================================
LICENSE
=====================================

All code and data are released under MIT License.
See LICENSE file in GitHub repository.

=====================================
VERSION HISTORY
=====================================

v1.0 (October 2025):
  - Initial arXiv submission
  - PDG 2025 data
  - Complete statistical validation suite
  - All plots in English

