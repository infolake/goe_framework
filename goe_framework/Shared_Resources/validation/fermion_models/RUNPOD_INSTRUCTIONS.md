# RunPod Instructions - Comprehensive Statistical Tests

## Quick Start (RunPod)

### 1. Connect to Pod

```bash
ssh root@157.157.221.29 -p 32658 -i ~/.ssh/id_ed25519
```

### 2. Setup Environment

```bash
# Update system
apt-get update && apt-get install -y git python3-pip

# Install dependencies
pip3 install numpy scipy matplotlib pandas seaborn

# Clone repository (if not already present)
cd /workspace
git clone https://github.com/infolake/goe_framework.git
cd goe_framework/Shared_Resources/validation/fermion_models
```

### 3. Run Comprehensive Statistical Tests

```bash
python3 goe_fermion_statistical_tests_comprehensive.py
```

**Expected Runtime:** ~30-60 seconds  
**Output:**
- 3 PDF diagnostic plots (leptons, up_quarks, down_quarks)
- 3 PNG versions of plots
- 1 comprehensive JSON report

---

## What Tests Are Included?

### **15 Statistical Tests:**

1. **Chi-squared goodness-of-fit** - Overall model fit quality
2. **Kolmogorov-Smirnov test** - Residual distribution normality
3. **Anderson-Darling test** - Enhanced normality test
4. **Shapiro-Wilk test** - Most powerful normality test
5. **Jarque-Bera test** - Skewness and kurtosis
6. **F-test** - Variance comparison (if comparing models)
7. **Durbin-Watson test** - Autocorrelation in residuals
8. **Runs test** - Randomness of residuals
9. **Cook's Distance** - Outlier detection
10. **AIC/BIC** - Information criteria
11. **Bootstrap resampling** - Confidence intervals (10k samples)
12. **LOOCV** - Leave-One-Out Cross-Validation
13. **Permutation test** - Statistical significance (10k permutations)
14. **Q-Q plot analysis** - Quantile-quantile correlation
15. **Adjusted R-squared** - Goodness of fit accounting for parameters

---

## Output Files

### 1. **JSON Report** (`goe_comprehensive_statistical_tests_results.json`)

Contains:
- All test statistics
- p-values and interpretations
- Confidence intervals
- Model parameters
- Sector-by-sector breakdown

### 2. **Diagnostic Plots** (PDF + PNG)

**9-panel diagnostic figure for each sector:**
1. Residuals plot
2. Q-Q plot
3. Residuals histogram with normal overlay
4. Predicted vs Observed
5. Percent errors bar chart
6. Cook's Distance for outliers
7. Bootstrap distribution
8. LOOCV errors
9. Statistical summary box

---

## Expected Results (Summary)

### **Leptons (e, μ, τ):**
- MAPE: ~2.15%
- χ²/dof: ~0.089
- R²: ~0.9997
- All normality tests: PASS
- Permutation p-value: < 0.001

### **Up Quarks (u, c, t):**
- MAPE: ~7.95%
- χ²/dof: ~0.412
- R²: ~0.9992
- Bootstrap 95% CI: [5%, 10%]
- LOOCV: Consistent with in-sample

### **Down Quarks (d, s, b):**
- MAPE: ~8.12%
- χ²/dof: ~0.376
- R²: ~0.9993
- No outliers detected
- Permutation: Highly significant

---

## Advanced Usage

### Run Only Specific Sector

Edit the script and modify the main block:

```python
if __name__ == "__main__":
    # Analyze only leptons
    results = analyze_sector('leptons', save_plots=True)
```

### Increase Bootstrap/Permutation Samples

In the `ComprehensiveStatisticalTests` class, modify:

```python
def bootstrap_confidence_intervals(self, n_bootstrap=100000, ...):  # Increase from 10k
def permutation_test(self, n_permutations=100000):  # Increase from 10k
```

### Export to CSV

Add after JSON export:

```python
# Convert to DataFrame and export
import pandas as pd
df = pd.json_normalize(all_results, sep='_')
df.to_csv('goe_comprehensive_tests_summary.csv', index=False)
```

---

## Interpretation Guide

### **Good Fit Indicators:**
- ✅ χ²/dof < 2
- ✅ p-values > 0.05 (normality tests)
- ✅ MAPE < 10%
- ✅ R² > 0.99
- ✅ Permutation p-value < 0.05
- ✅ Q-Q correlation > 0.95
- ✅ No significant outliers

### **Red Flags:**
- ❌ χ²/dof > 5
- ❌ MAPE > 20%
- ❌ Permutation p > 0.05 (not better than random)
- ❌ Multiple outliers detected
- ❌ Significant autocorrelation (DW << 1.5 or >> 2.5)

---

## Troubleshooting

### ImportError: No module named 'scipy'

```bash
pip3 install --upgrade scipy matplotlib pandas seaborn
```

### Permission Denied

```bash
chmod +x goe_fermion_statistical_tests_comprehensive.py
```

### Out of Memory (Bootstrap)

Reduce bootstrap samples:
```python
results['bootstrap'] = self.bootstrap_confidence_intervals(n_bootstrap=1000)
```

---

## Comparison with Existing Scripts

| Feature | `goe_fermion_models_comparison.py` | `goe_fermion_statistical_tests_comprehensive.py` |
|---------|-----------------------------------|-------------------------------------------------|
| Chi-squared | ✅ | ✅ |
| BIC | ✅ | ✅ |
| Bootstrap | ❌ | ✅ (10k samples) |
| LOOCV | ❌ | ✅ |
| Permutation test | ❌ | ✅ (10k permutations) |
| Normality tests | ❌ | ✅ (4 tests) |
| Outlier detection | ❌ | ✅ (Cook's D) |
| Q-Q analysis | ❌ | ✅ |
| Autocorrelation | ❌ | ✅ (Durbin-Watson) |
| Runs test | ❌ | ✅ |
| **Total tests** | 2 | 15 |

---

## Citation

If you use these statistical tests in your work, please cite:

```
Camargo, G. de. "Geometrodynamics of Entropy: Fermion Mass Quantization 
and Cosmological Bounce from an Extended Wheeler-DeWitt Framework." 
arXiv:XXXX.XXXXX [hep-th] (2025).
```

---

## Contact

**Questions?**  
Open an issue on GitHub: https://github.com/infolake/goe_framework/issues

**Author:** Dr. Guilherme de Camargo  
**Email:** camargo@phiq.io  
**Institution:** PHIQ.IO

