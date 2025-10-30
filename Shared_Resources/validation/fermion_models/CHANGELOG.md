# CHANGELOG: Fermion Models Validation Scripts

## [2.0.0] - 2025-10-30

### 🔄 MAJOR UPDATES

#### 1. PDG Data Updated: 2023 → 2025
All experimental fermion mass values updated to **Particle Data Group 2025** with full precision:

**Leptons (full precision):**
- Electron: `0.51099895000 ± 0.00000000015 MeV` (11 decimal places)
- Muon: `105.6583755 ± 0.0000023 MeV` (7 decimal places)
- Tau: `1776.86 ± 0.12 MeV`

**Up-type Quarks:**
- Up: `2.16 (+0.49/-0.26) MeV` @ MS-bar 2 GeV
- Charm: `1273.0 ± 4.6 MeV` @ m_c (**updated** from 1275)
- Top: `172500 ± 500 MeV` (pole mass)

**Down-type Quarks:**
- Down: `4.67 (+0.48/-0.17) MeV` @ MS-bar 2 GeV
- Strange: `93.4 (+8.6/-3.4) MeV` @ MS-bar 2 GeV
- Bottom: `4183 ± 7 MeV` @ m_b (**updated** from 4180)

**Source:** https://pdg.lbl.gov/2025/  
**References:**
- Leptons: https://pdg.lbl.gov/2025/tables/rpp2025-sum-leptons.pdf
- Quarks: https://pdg.lbl.gov/2025/tables/rpp2025-sum-quarks.pdf

---

#### 2. Data Export Features Added

**Both scripts now export results to disk:**

**Script 1: `goe_fermion_models_comparison.py`**

New outputs:
- ✅ `fermion_models_comparison_results.json` (comprehensive structured data)
- ✅ `fermion_models_comparison_results.csv` (tabular data for analysis)

JSON includes:
- Metadata (date, PDG version, script name)
- Experimental data with uncertainties
- Model A & B parameters, predictions, errors
- Statistical metrics (BIC, χ², MAPE, RMS)
- Combined statistics

CSV includes:
- Sector, fermion, experimental mass, uncertainty
- Model A predictions and errors
- Model B n-values, predictions and errors
- All model parameters

**Script 2: `goe_strong_force_analysis.py`**

New outputs:
- ✅ `goe_strong_force_analysis_results.json` (comprehensive structured data)
- ✅ `goe_strong_force_analysis_results.csv` (hadron masses)
- ✅ `goe_strong_force_analysis_results_coupling.csv` (α_s(Q²) data)

JSON includes:
- Metadata (date, PDG version, script name)
- Fundamental constants (φ, α_em, Λ_QCD, R_N, L_N)
- Strong coupling α_s at various Q scales
- Quark potential V(r) components
- Hadron mass predictions and errors

CSV includes:
- Hadron type (meson/baryon), particle name, n-value
- Predicted mass, experimental mass, error %
- Separate file for coupling constant evolution

---

#### 3. Uncertainty Data Added

New dictionary `FERMION_MASSES_UNC` with experimental uncertainties:
```python
FERMION_MASSES_UNC = {
    'e': 0.00000000015,
    'mu': 0.0000023,
    'tau': 0.12,
    'u': (0.49, 0.26),    # asymmetric: (+upper, -lower)
    'c': 4.6,
    't': 500,
    'd': (0.48, 0.17),
    's': (8.6, 3.4),
    'b': 7
}
```

---

### 📊 Output Files Summary

| Script | PDFs | JSON | CSV | Total |
|--------|------|------|-----|-------|
| **Fermion Comparison** | 3 | 1 | 1 | 5 files |
| **Strong Force** | 1 | 1 | 2 | 4 files |
| **TOTAL** | 4 | 2 | 3 | **9 files** |

---

### 🔍 What Changed in Code

**`goe_fermion_models_comparison.py`:**
- Lines 37-64: Updated experimental masses (PDG 2025, full precision)
- Lines 570-659: New `export_to_json()` function
- Lines 661-709: New `export_to_csv()` function
- Lines 711-724: Updated `if __name__ == "__main__"` to call export functions

**`goe_strong_force_analysis.py`:**
- Lines 438-494: New `export_to_json()` function
- Lines 496-556: New `export_to_csv()` function
- Lines 558-571: Updated `if __name__ == "__main__"` to call export functions

---

### ✅ Validation

All updates validated using:
- **Perplexity MCP** for PDG 2025 data lookup
- Cross-reference with official PDG 2025 tables
- Full precision maintained (up to 11 decimal places for electron)
- Asymmetric uncertainties preserved for quarks

---

### 📚 References

1. **Particle Data Group 2025 Review**  
   https://pdg.lbl.gov/2025/

2. **Charged Lepton Summary**  
   https://pdg.lbl.gov/2025/tables/rpp2025-sum-leptons.pdf

3. **Quark Summary**  
   https://pdg.lbl.gov/2025/tables/rpp2025-sum-quarks.pdf

4. **Charm Quark Listing**  
   https://pdg.lbl.gov/2025/listings/rpp2025-list-c-quark.pdf

5. **Bottom Quark Listing**  
   https://pdg.lbl.gov/2025/listings/rpp2025-list-b-quark.pdf

---

### 🔜 Future Improvements

- [ ] Add automatic comparison between PDG versions
- [ ] Implement error propagation for derived quantities
- [ ] Add visualization of uncertainty bands
- [ ] Export to HDF5 for large datasets
- [ ] Add automated unit tests

---

### 👥 Contributors

- **Data Update:** Perplexity AI (MCP integration)
- **Code Implementation:** Dr. Guilherme de Camargo
- **Validation:** Cross-checked with PDG 2025 official tables

---

### 📝 Notes

- **Breaking change:** Output file count increased from 4 to 9
- **Backward compatible:** Original PDF outputs unchanged
- **Data provenance:** Full traceability to PDG 2025
- **Precision:** Maximum available precision maintained
- **Encoding:** UTF-8 for all text files
- **Format:** JSON with 2-space indentation, CSV with headers

---

**Status:** ✅ Complete and tested  
**Version:** 2.0.0  
**Date:** 2025-10-30  
**PDG Version:** 2025

