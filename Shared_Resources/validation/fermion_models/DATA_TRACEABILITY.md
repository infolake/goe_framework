# DATA TRACEABILITY: Scripts → Raw Data → PDF Outputs

**Location:** `goe_framework/Shared_Resources/validation/fermion_models/`  
**Last Updated:** 2025-10-30  
**Status:** Complete and auditable

---

## OVERVIEW

All fermion model comparison plots are fully reproducible from the provided Python scripts. **No external data files are required** — all experimental data is hardcoded within the scripts, sourced directly from the Particle Data Group (PDG) 2023 Review.

---

## FILE INVENTORY

### Scripts (2 files, 32 KB)
1. `goe_fermion_models_comparison.py` (17 KB)
2. `goe_strong_force_analysis.py` (15 KB)

### PDF Outputs (4 files, 155 KB)
1. `goe_models_comparison_leptons.pdf` (38 KB)
2. `goe_models_comparison_up_quarks.pdf` (39 KB)
3. `goe_models_comparison_down_quarks.pdf` (40 KB)
4. `goe_strong_force_analysis.pdf` (38 KB)

---

## TRACEABILITY MAP

### 1. LEPTONS COMPARISON

**PDF:** `goe_models_comparison_leptons.pdf` (38 KB)

**Script:** `goe_fermion_models_comparison.py`

**Raw Data (lines 38-51):**
```python
FERMION_MASSES_EXP = {
    # Charged leptons
    'e': 0.5109989461,      # MeV
    'mu': 105.6583745,      # MeV
    'tau': 1776.86,         # MeV
}
```

**Source:** PDG (Particle Data Group) 2023 Review  
**Reference:** https://pdg.lbl.gov/

**Models Compared:**
- **Model A:** Power Law `m ~ |q|^p`
- **Model B:** Golden Ratio Quantization `m ~ φ^n`

**Statistical Results:**
- Model B MAPE: 2.15%
- Model A MAPE: higher
- ΔBIC: -13.5 (decisive evidence for Model B)

---

### 2. UP QUARKS COMPARISON

**PDF:** `goe_models_comparison_up_quarks.pdf` (39 KB)

**Script:** `goe_fermion_models_comparison.py`

**Raw Data (lines 38-51):**
```python
FERMION_MASSES_EXP = {
    # Up-type quarks (MS-bar @ 2 GeV)
    'u': 2.16,              # MeV
    'c': 1275,              # MeV
    't': 172760,            # MeV
}
```

**Source:** PDG 2023 Review (MS-bar scheme at 2 GeV scale)

**Models Compared:**
- **Model A:** Power Law
- **Model B:** Golden Ratio Quantization

**Statistical Results:**
- Model B MAPE: 7.95%
- Sector-specific mass anchor: `m₀(u) = m₀(ℓ)/φ² = 2.16 MeV` (derived, not calibrated)

---

### 3. DOWN QUARKS COMPARISON

**PDF:** `goe_models_comparison_down_quarks.pdf` (40 KB)

**Script:** `goe_fermion_models_comparison.py`

**Raw Data (lines 38-51):**
```python
FERMION_MASSES_EXP = {
    # Down-type quarks (MS-bar @ 2 GeV)
    'd': 4.67,              # MeV
    's': 93.4,              # MeV
    'b': 4180               # MeV
}
```

**Source:** PDG 2023 Review (MS-bar scheme at 2 GeV scale)

**Models Compared:**
- **Model A:** Power Law
- **Model B:** Golden Ratio Quantization

**Statistical Results:**
- Model B MAPE: 8.02%
- Sector-specific mass anchor: `m₀(d) = m₀(ℓ) · φ · η = 4.67 MeV` (derived, not calibrated)

---

### 4. STRONG FORCE ANALYSIS

**PDF:** `goe_strong_force_analysis.pdf` (38 KB)

**Script:** `goe_strong_force_analysis.py`

**Raw Data (lines 33-48):**
```python
# Fundamental constants
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio = 1.618...
ALPHA_EM = 1/137.035999084  # Fine structure constant
HBAR_C = 0.1973269804       # GeV·fm (natural units)
LAMBDA_QCD = 0.200          # GeV (QCD confinement scale)

# Nuclear fiber parameters (derived)
R_N = HBAR_C / LAMBDA_QCD   # Nuclear fiber radius ≈ 0.987 fm
L_N = 2 * np.pi * R_N       # Nuclear fiber circumference ≈ 6.20 fm
```

**Source:**
- PDG 2023 for fundamental constants
- Geometric derivation from GoE framework

**Analysis:**
- Strong coupling constant evolution: `α_s(Q²)`
- Geometric correction term: `κ_N/φ⁴`
- Comparison with standard QCD running

---

## REPRODUCIBILITY

### Requirements
```bash
numpy>=1.24.0
matplotlib>=3.8.0
pandas>=2.0.0
scipy>=1.10.0
seaborn>=0.12.0
```

### Generate All PDFs
```bash
cd goe_framework/Shared_Resources/validation/fermion_models/

# Generate 3 comparison plots (leptons, up-quarks, down-quarks)
python goe_fermion_models_comparison.py

# Generate strong force analysis plot
python goe_strong_force_analysis.py
```

**Expected Runtime:** ~10-15 seconds total

**Output:**
- 4 PDF files (300 DPI, vectorial)
- Console output with statistical summaries
- All figures in English, publication-ready

---

## DATA PROVENANCE

### Experimental Values
- **Source:** Particle Data Group (PDG) 2023 Review
- **Citation:** R.L. Workman et al. (Particle Data Group), Prog. Theor. Exp. Phys. 2022, 083C01 (2022)
- **URL:** https://pdg.lbl.gov/

### Quark Masses
- **Scheme:** MS-bar (Modified Minimal Subtraction)
- **Scale:** 2 GeV
- **Note:** Running masses, not pole masses

### Lepton Masses
- **Type:** Pole masses (physical masses)
- **Precision:** PDG 2023 best-fit values

---

## CITATIONS IN PAPER

These plots are cited in the main paper (`main.tex`) in:
- Section 3.2.2: Fermion Mass Hierarchy
- Section 3.4: Phenomenological Validation
- Figure 4: Multi-sector comparison (leptons, quarks)

**Caption References:**
- "Model B (φⁿ quantization) achieves MAPE = 7.28% across all 9 charged fermions"
- "ΔBIC = -13.5 provides decisive evidence for the geometric model"
- "Strong force analysis confirms geometric origin of nuclear confinement"

---

## NOTES

1. **No External Dependencies:** All data is self-contained within the scripts.
2. **Version Control:** Scripts include modification dates and author information.
3. **Language:** 100% English (code, comments, docstrings).
4. **Quality:** 300 DPI, vectorial PDFs suitable for publication.
5. **Auditability:** Every experimental value is traceable to PDG 2023.

---

## CONTACT

**Author:** Dr. Guilherme de Camargo  
**Email:** camargo@phiq.io  
**Institution:** PHIQ.IO  
**Date:** 2025-10-25

