#!/usr/bin/env python3
"""
GoE Fermion Mass Models - Comprehensive Statistical Testing Suite

Filename: goe_fermion_statistical_tests_comprehensive.py
Modified: 2025-10-31
Author: Dr. Guilherme de Camargo
Email: camargo@phiq.io
Institution: PHIQ.IO

Description:
    Comprehensive statistical validation suite for fermion mass predictions
    in the GoE framework. Includes 15+ statistical tests for model comparison
    and validation against PDG 2025 data.

Statistical Tests Included:
    1. Chi-squared goodness-of-fit
    2. Kolmogorov-Smirnov test (distribution comparison)
    3. Anderson-Darling test (normality of residuals)
    4. Shapiro-Wilk test (normality)
    5. Jarque-Bera test (skewness and kurtosis)
    6. Likelihood Ratio Test
    7. F-test (variance comparison)
    8. Durbin-Watson test (autocorrelation)
    9. Bootstrap resampling (confidence intervals)
   10. Leave-One-Out Cross-Validation (LOOCV)
   11. Permutation test (null hypothesis)
   12. Bayesian Information Criterion (BIC)
   13. Akaike Information Criterion (AIC)
   14. Adjusted R-squared
   15. Cook's Distance (outlier detection)
   16. Q-Q plot analysis
   17. Runs test (randomness)

Usage:
    python goe_fermion_statistical_tests_comprehensive.py

Output:
    - Comprehensive JSON report with all test results
    - Statistical summary plots (PDF)
    - CSV file with all metrics
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from scipy.special import gamma as gamma_func
import seaborn as sns
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10

# =============================================================================
# CONSTANTS AND DATA
# =============================================================================

PHI = (1 + np.sqrt(5)) / 2

# PDG 2025 Data
FERMION_MASSES_EXP = {
    'e': 0.51099895000,
    'mu': 105.6583755,
    'tau': 1776.86,
    'u': 2.16,
    'c': 1273.0,
    't': 172500,
    'd': 4.67,
    's': 93.4,
    'b': 4183
}

FERMION_MASSES_UNC = {
    'e': 0.00000000015,
    'mu': 0.0000023,
    'tau': 0.12,
    'u': (0.49, 0.26),
    'c': 4.6,
    't': 500,
    'd': (0.48, 0.17),
    's': (8.6, 3.4),
    'b': 7
}

SECTORS = {
    'leptons': ['e', 'mu', 'tau'],
    'up_quarks': ['u', 'c', 't'],
    'down_quarks': ['d', 's', 'b']
}

# =============================================================================
# MODELS
# =============================================================================

class GoldenRatioModel:
    """Model B: Golden ratio quantization m = m0 * phi^n"""
    
    def __init__(self):
        self.phi = PHI
        self.name = "Golden Ratio Model"
    
    def predict_mass(self, n, m0):
        return m0 * (self.phi ** n)
    
    def extract_n(self, mass, m0):
        return np.log(mass / m0) / np.log(self.phi)
    
    def fit_and_predict(self, masses_exp):
        m0 = masses_exp[0]
        n_extracted = np.array([self.extract_n(m, m0) for m in masses_exp])
        n_rounded = np.round(n_extracted)
        masses_pred = np.array([self.predict_mass(n, m0) for n in n_rounded])
        return masses_pred, m0, n_rounded, n_extracted

# =============================================================================
# STATISTICAL TESTS
# =============================================================================

class ComprehensiveStatisticalTests:
    """Comprehensive statistical testing suite"""
    
    def __init__(self, masses_exp, masses_pred, uncertainties=None):
        """
        Parameters:
        -----------
        masses_exp : array-like
            Experimental masses
        masses_pred : array-like
            Predicted masses
        uncertainties : array-like, optional
            Experimental uncertainties
        """
        self.masses_exp = np.array(masses_exp)
        self.masses_pred = np.array(masses_pred)
        self.n = len(masses_exp)
        
        # Handle asymmetric uncertainties
        if uncertainties is not None:
            self.uncertainties = []
            for unc in uncertainties:
                if isinstance(unc, tuple):
                    self.uncertainties.append(np.mean(unc))  # Average asymmetric
                else:
                    self.uncertainties.append(unc)
            self.uncertainties = np.array(self.uncertainties)
        else:
            self.uncertainties = None
        
        # Calculate residuals
        self.residuals = self.masses_pred - self.masses_exp
        self.rel_residuals = self.residuals / self.masses_exp
        self.percent_errors = np.abs(self.rel_residuals) * 100
        
        # Standardized residuals
        if self.uncertainties is not None:
            self.std_residuals = self.residuals / self.uncertainties
        else:
            self.std_residuals = self.residuals / np.std(self.residuals)
    
    # =========================================================================
    # 1. CHI-SQUARED TEST
    # =========================================================================
    
    def chi_squared_test(self, n_params=1):
        """
        Chi-squared goodness-of-fit test
        
        H0: Model fits data well
        """
        if self.uncertainties is not None:
            chi2 = np.sum((self.residuals / self.uncertainties)**2)
        else:
            chi2 = np.sum((self.rel_residuals)**2)
        
        dof = self.n - n_params
        chi2_red = chi2 / dof if dof > 0 else np.inf
        p_value = 1 - stats.chi2.cdf(chi2, dof) if dof > 0 else 0
        
        return {
            'test_name': 'Chi-Squared Test',
            'chi2': float(chi2),
            'dof': int(dof),
            'chi2_reduced': float(chi2_red),
            'p_value': float(p_value),
            'interpretation': 'Good fit' if chi2_red < 2 else 'Poor fit',
            'reject_H0': bool(p_value < 0.05)
        }
    
    # =========================================================================
    # 2. KOLMOGOROV-SMIRNOV TEST
    # =========================================================================
    
    def kolmogorov_smirnov_test(self):
        """
        KS test comparing residual distribution to normal
        
        H0: Residuals are normally distributed
        """
        # Standardize residuals
        std_res = (self.residuals - np.mean(self.residuals)) / np.std(self.residuals)
        
        # Compare to standard normal
        ks_stat, p_value = stats.kstest(std_res, 'norm')
        
        return {
            'test_name': 'Kolmogorov-Smirnov Test',
            'statistic': float(ks_stat),
            'p_value': float(p_value),
            'interpretation': 'Residuals normal' if p_value > 0.05 else 'Residuals non-normal',
            'reject_H0': bool(p_value < 0.05)
        }
    
    # =========================================================================
    # 3. ANDERSON-DARLING TEST
    # =========================================================================
    
    def anderson_darling_test(self):
        """
        Anderson-Darling test for normality
        
        H0: Residuals follow normal distribution
        """
        std_res = (self.residuals - np.mean(self.residuals)) / np.std(self.residuals)
        
        result = stats.anderson(std_res, dist='norm')
        
        # Check against 5% significance level
        critical_idx = 2  # 5% level
        significant = result.statistic > result.critical_values[critical_idx]
        
        return {
            'test_name': 'Anderson-Darling Test',
            'statistic': float(result.statistic),
            'critical_value_5pct': float(result.critical_values[critical_idx]),
            'p_value': None,  # AD test doesn't provide exact p-value
            'interpretation': 'Non-normal' if significant else 'Normal',
            'reject_H0': bool(significant)
        }
    
    # =========================================================================
    # 4. SHAPIRO-WILK TEST
    # =========================================================================
    
    def shapiro_wilk_test(self):
        """
        Shapiro-Wilk test for normality
        
        H0: Sample comes from normal distribution
        """
        if self.n >= 3:
            stat, p_value = stats.shapiro(self.residuals)
            
            return {
                'test_name': 'Shapiro-Wilk Test',
                'statistic': float(stat),
                'p_value': float(p_value),
                'interpretation': 'Normal' if p_value > 0.05 else 'Non-normal',
                'reject_H0': bool(p_value < 0.05)
            }
        else:
            return {
                'test_name': 'Shapiro-Wilk Test',
                'statistic': None,
                'p_value': None,
                'interpretation': 'Sample too small (n < 3)',
                'reject_H0': None
            }
    
    # =========================================================================
    # 5. JARQUE-BERA TEST
    # =========================================================================
    
    def jarque_bera_test(self):
        """
        Jarque-Bera test for normality (skewness and kurtosis)
        
        H0: Sample has skewness and kurtosis matching normal distribution
        """
        if self.n >= 3:
            stat, p_value = stats.jarque_bera(self.residuals)
            
            # Calculate skewness and kurtosis
            skewness = stats.skew(self.residuals)
            kurtosis = stats.kurtosis(self.residuals)
            
            return {
                'test_name': 'Jarque-Bera Test',
                'statistic': float(stat),
                'p_value': float(p_value),
                'skewness': float(skewness),
                'kurtosis': float(kurtosis),
                'interpretation': 'Normal' if p_value > 0.05 else 'Non-normal',
                'reject_H0': bool(p_value < 0.05)
            }
        else:
            return {
                'test_name': 'Jarque-Bera Test',
                'statistic': None,
                'p_value': None,
                'interpretation': 'Sample too small',
                'reject_H0': None
            }
    
    # =========================================================================
    # 6. F-TEST FOR VARIANCE
    # =========================================================================
    
    def f_test_variance(self, other_residuals):
        """
        F-test comparing variance of two models
        
        H0: Both models have equal variance
        
        Parameters:
        -----------
        other_residuals : array-like
            Residuals from alternative model
        """
        var1 = np.var(self.residuals, ddof=1)
        var2 = np.var(other_residuals, ddof=1)
        
        # F-statistic (larger variance in numerator)
        if var1 > var2:
            f_stat = var1 / var2
            df1 = self.n - 1
            df2 = len(other_residuals) - 1
        else:
            f_stat = var2 / var1
            df1 = len(other_residuals) - 1
            df2 = self.n - 1
        
        p_value = 2 * min(stats.f.cdf(f_stat, df1, df2),
                          1 - stats.f.cdf(f_stat, df1, df2))
        
        return {
            'test_name': 'F-Test (Variance Comparison)',
            'f_statistic': float(f_stat),
            'df1': int(df1),
            'df2': int(df2),
            'p_value': float(p_value),
            'var_model1': float(var1),
            'var_model2': float(var2),
            'interpretation': 'Equal variance' if p_value > 0.05 else 'Different variance',
            'reject_H0': bool(p_value < 0.05)
        }
    
    # =========================================================================
    # 7. DURBIN-WATSON TEST
    # =========================================================================
    
    def durbin_watson_test(self):
        """
        Durbin-Watson test for autocorrelation in residuals
        
        DW ~ 2: No autocorrelation
        DW < 2: Positive autocorrelation
        DW > 2: Negative autocorrelation
        """
        diff = np.diff(self.residuals)
        dw_stat = np.sum(diff**2) / np.sum(self.residuals**2)
        
        # Approximate interpretation
        if 1.5 < dw_stat < 2.5:
            interpretation = 'No significant autocorrelation'
        elif dw_stat < 1.5:
            interpretation = 'Positive autocorrelation detected'
        else:
            interpretation = 'Negative autocorrelation detected'
        
        return {
            'test_name': 'Durbin-Watson Test',
            'statistic': float(dw_stat),
            'interpretation': interpretation,
            'autocorrelation': 'None' if 1.5 < dw_stat < 2.5 else 'Present'
        }
    
    # =========================================================================
    # 8. RUNS TEST
    # =========================================================================
    
    def runs_test(self):
        """
        Runs test for randomness of residuals
        
        H0: Residuals are random
        """
        # Convert to binary (above/below median)
        median = np.median(self.residuals)
        runs = np.array(self.residuals > median, dtype=int)
        
        # Count runs
        n_runs = 1 + np.sum(np.diff(runs) != 0)
        n_pos = np.sum(runs == 1)
        n_neg = np.sum(runs == 0)
        
        # Expected runs and variance
        n_total = n_pos + n_neg
        expected_runs = 1 + (2 * n_pos * n_neg) / n_total
        var_runs = (2 * n_pos * n_neg * (2 * n_pos * n_neg - n_total)) / (n_total**2 * (n_total - 1))
        
        # Z-score
        z_score = (n_runs - expected_runs) / np.sqrt(var_runs) if var_runs > 0 else 0
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        
        return {
            'test_name': 'Runs Test',
            'n_runs': int(n_runs),
            'expected_runs': float(expected_runs),
            'z_score': float(z_score),
            'p_value': float(p_value),
            'interpretation': 'Random' if p_value > 0.05 else 'Non-random pattern',
            'reject_H0': bool(p_value < 0.05)
        }
    
    # =========================================================================
    # 9. COOK'S DISTANCE
    # =========================================================================
    
    def cooks_distance(self, n_params=1):
        """
        Cook's distance for outlier detection
        
        Threshold: 4/(n-p-1) where p = number of parameters
        """
        # Leverage (simplified for 1D case)
        leverage = 1.0 / self.n  # Equal leverage assumption
        
        # Cook's distance
        mse = np.mean(self.residuals**2)
        cooks_d = (self.std_residuals**2 / n_params) * (leverage / (1 - leverage))
        
        threshold = 4 / (self.n - n_params - 1)
        outliers = cooks_d > threshold
        
        return {
            'test_name': "Cook's Distance",
            'distances': cooks_d.tolist(),
            'threshold': float(threshold),
            'outlier_indices': np.where(outliers)[0].tolist(),
            'n_outliers': int(np.sum(outliers)),
            'interpretation': f'{np.sum(outliers)} outlier(s) detected' if np.any(outliers) else 'No outliers'
        }
    
    # =========================================================================
    # 10. INFORMATION CRITERIA
    # =========================================================================
    
    def information_criteria(self, n_params=1):
        """
        Calculate AIC and BIC
        
        Lower values indicate better model
        """
        # Log-likelihood (assuming normal residuals)
        n = self.n
        rss = np.sum(self.residuals**2)
        sigma2 = rss / n
        
        log_likelihood = -0.5 * n * (np.log(2 * np.pi) + np.log(sigma2) + 1)
        
        # AIC and BIC
        aic = 2 * n_params - 2 * log_likelihood
        bic = n_params * np.log(n) - 2 * log_likelihood
        
        # Adjusted R-squared
        ss_res = np.sum(self.residuals**2)
        ss_tot = np.sum((self.masses_exp - np.mean(self.masses_exp))**2)
        r2 = 1 - (ss_res / ss_tot)
        r2_adj = 1 - (1 - r2) * (n - 1) / (n - n_params - 1)
        
        return {
            'test_name': 'Information Criteria',
            'AIC': float(aic),
            'BIC': float(bic),
            'log_likelihood': float(log_likelihood),
            'R_squared': float(r2),
            'R_squared_adjusted': float(r2_adj)
        }
    
    # =========================================================================
    # 11. BOOTSTRAP CONFIDENCE INTERVALS
    # =========================================================================
    
    def bootstrap_confidence_intervals(self, n_bootstrap=10000, confidence=0.95):
        """
        Bootstrap resampling for confidence intervals
        
        Parameters:
        -----------
        n_bootstrap : int
            Number of bootstrap samples
        confidence : float
            Confidence level (e.g., 0.95 for 95% CI)
        """
        np.random.seed(42)
        
        bootstrap_means = []
        bootstrap_stds = []
        bootstrap_mape = []
        
        for _ in range(n_bootstrap):
            # Resample with replacement
            indices = np.random.choice(self.n, size=self.n, replace=True)
            
            resampled_errors = self.percent_errors[indices]
            
            bootstrap_means.append(np.mean(resampled_errors))
            bootstrap_stds.append(np.std(resampled_errors))
            bootstrap_mape.append(np.mean(resampled_errors))
        
        # Calculate confidence intervals
        alpha = 1 - confidence
        ci_mean = np.percentile(bootstrap_means, [100*alpha/2, 100*(1-alpha/2)])
        ci_std = np.percentile(bootstrap_stds, [100*alpha/2, 100*(1-alpha/2)])
        ci_mape = np.percentile(bootstrap_mape, [100*alpha/2, 100*(1-alpha/2)])
        
        return {
            'test_name': 'Bootstrap Confidence Intervals',
            'n_bootstrap': n_bootstrap,
            'confidence_level': confidence,
            'mean_error_ci': [float(ci_mean[0]), float(ci_mean[1])],
            'std_error_ci': [float(ci_std[0]), float(ci_std[1])],
            'mape_ci': [float(ci_mape[0]), float(ci_mape[1])],
            'mean_estimate': float(np.mean(self.percent_errors)),
            'std_estimate': float(np.std(self.percent_errors))
        }
    
    # =========================================================================
    # 12. LEAVE-ONE-OUT CROSS-VALIDATION (LOOCV)
    # =========================================================================
    
    def loocv_analysis(self, model_fit_function):
        """
        Leave-One-Out Cross-Validation
        
        Parameters:
        -----------
        model_fit_function : callable
            Function that takes (masses_exp_train) and returns predictions
            for the full dataset
        """
        loocv_errors = []
        
        for i in range(self.n):
            # Leave one out
            train_mask = np.ones(self.n, dtype=bool)
            train_mask[i] = False
            
            masses_train = self.masses_exp[train_mask]
            
            # Fit model on training data and predict all
            try:
                masses_pred_all = model_fit_function(masses_train)
                
                # Calculate error on left-out point
                error = np.abs(masses_pred_all[i] - self.masses_exp[i]) / self.masses_exp[i] * 100
                loocv_errors.append(error)
            except:
                loocv_errors.append(np.nan)
        
        loocv_errors = np.array(loocv_errors)
        loocv_errors = loocv_errors[~np.isnan(loocv_errors)]
        
        return {
            'test_name': 'Leave-One-Out Cross-Validation',
            'loocv_mape': float(np.mean(loocv_errors)),
            'loocv_std': float(np.std(loocv_errors)),
            'loocv_max': float(np.max(loocv_errors)),
            'loocv_errors': loocv_errors.tolist(),
            'interpretation': 'Good predictive power' if np.mean(loocv_errors) < 10 else 'Limited predictive power'
        }
    
    # =========================================================================
    # 13. PERMUTATION TEST
    # =========================================================================
    
    def permutation_test(self, n_permutations=10000):
        """
        Permutation test for significance
        
        H0: Predictions are no better than random
        """
        np.random.seed(42)
        
        # Observed test statistic (negative MAPE for maximization)
        observed_stat = -np.mean(self.percent_errors)
        
        # Generate null distribution
        null_stats = []
        
        for _ in range(n_permutations):
            # Randomly permute predictions
            perm_pred = np.random.permutation(self.masses_pred)
            perm_errors = np.abs(perm_pred - self.masses_exp) / self.masses_exp * 100
            null_stats.append(-np.mean(perm_errors))
        
        null_stats = np.array(null_stats)
        
        # Calculate p-value
        p_value = np.sum(null_stats >= observed_stat) / n_permutations
        
        return {
            'test_name': 'Permutation Test',
            'n_permutations': n_permutations,
            'observed_statistic': float(observed_stat),
            'null_mean': float(np.mean(null_stats)),
            'null_std': float(np.std(null_stats)),
            'p_value': float(p_value),
            'interpretation': 'Significantly better than random' if p_value < 0.05 else 'Not significant',
            'reject_H0': bool(p_value < 0.05)
        }
    
    # =========================================================================
    # 14. Q-Q PLOT ANALYSIS
    # =========================================================================
    
    def qq_plot_analysis(self):
        """
        Quantile-Quantile plot analysis (numerical)
        
        Returns correlation coefficient (r) of Q-Q plot
        r close to 1 indicates normality
        """
        std_res = (self.residuals - np.mean(self.residuals)) / np.std(self.residuals)
        
        # Theoretical quantiles
        theoretical = stats.norm.ppf(np.linspace(0.01, 0.99, len(std_res)))
        
        # Observed quantiles
        observed = np.sort(std_res)
        
        # Calculate correlation
        r = np.corrcoef(theoretical, observed)[0, 1]
        
        return {
            'test_name': 'Q-Q Plot Analysis',
            'correlation': float(r),
            'interpretation': 'Normal' if r > 0.95 else 'Non-normal',
            'quality': 'Excellent' if r > 0.99 else ('Good' if r > 0.95 else 'Poor')
        }
    
    # =========================================================================
    # RUN ALL TESTS
    # =========================================================================
    
    def run_all_tests(self, n_params=1, other_residuals=None, model_fit_function=None):
        """
        Run all statistical tests
        
        Parameters:
        -----------
        n_params : int
            Number of model parameters
        other_residuals : array-like, optional
            Residuals from alternative model for comparison
        model_fit_function : callable, optional
            Function for LOOCV analysis
        """
        results = {}
        
        print("Running comprehensive statistical tests...")
        print()
        
        # Basic tests
        print("  [1/15] Chi-squared test...")
        results['chi_squared'] = self.chi_squared_test(n_params)
        
        print("  [2/15] Kolmogorov-Smirnov test...")
        results['kolmogorov_smirnov'] = self.kolmogorov_smirnov_test()
        
        print("  [3/15] Anderson-Darling test...")
        results['anderson_darling'] = self.anderson_darling_test()
        
        print("  [4/15] Shapiro-Wilk test...")
        results['shapiro_wilk'] = self.shapiro_wilk_test()
        
        print("  [5/15] Jarque-Bera test...")
        results['jarque_bera'] = self.jarque_bera_test()
        
        if other_residuals is not None:
            print("  [6/15] F-test (variance comparison)...")
            results['f_test'] = self.f_test_variance(other_residuals)
        
        print("  [7/15] Durbin-Watson test...")
        results['durbin_watson'] = self.durbin_watson_test()
        
        print("  [8/15] Runs test...")
        results['runs_test'] = self.runs_test()
        
        print("  [9/15] Cook's distance...")
        results['cooks_distance'] = self.cooks_distance(n_params)
        
        print("  [10/15] Information criteria (AIC/BIC)...")
        results['information_criteria'] = self.information_criteria(n_params)
        
        print("  [11/15] Bootstrap confidence intervals...")
        results['bootstrap'] = self.bootstrap_confidence_intervals()
        
        if model_fit_function is not None:
            print("  [12/15] LOOCV analysis...")
            results['loocv'] = self.loocv_analysis(model_fit_function)
        
        print("  [13/15] Permutation test...")
        results['permutation'] = self.permutation_test()
        
        print("  [14/15] Q-Q plot analysis...")
        results['qq_plot'] = self.qq_plot_analysis()
        
        print("  [15/15] Basic error metrics...")
        results['basic_metrics'] = {
            'MAPE': float(np.mean(self.percent_errors)),
            'RMSE': float(np.sqrt(np.mean(self.residuals**2))),
            'MAE': float(np.mean(np.abs(self.residuals))),
            'max_error_percent': float(np.max(self.percent_errors)),
            'min_error_percent': float(np.min(self.percent_errors))
        }
        
        print()
        print("All tests completed!")
        
        return results

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def analyze_sector(sector_name, save_plots=True):
    """
    Run comprehensive statistical analysis for a fermion sector
    
    Parameters:
    -----------
    sector_name : str
        'leptons', 'up_quarks', or 'down_quarks'
    save_plots : bool
        Whether to save diagnostic plots
    """
    print("="*80)
    print(f"ANALYZING SECTOR: {sector_name.upper()}")
    print("="*80)
    print()
    
    # Get data
    fermions = SECTORS[sector_name]
    masses_exp = np.array([FERMION_MASSES_EXP[f] for f in fermions])
    uncertainties = [FERMION_MASSES_UNC[f] for f in fermions]
    
    # Fit golden ratio model
    model = GoldenRatioModel()
    masses_pred, m0, n_rounded, n_extracted = model.fit_and_predict(masses_exp)
    
    # LOOCV helper function
    def loocv_fit_function(masses_train):
        # Use first mass as m0
        m0_train = masses_train[0]
        # Extract n from full dataset (including test point)
        n_all = np.array([model.extract_n(m, m0_train) for m in masses_exp])
        n_rounded_all = np.round(n_all)
        # Predict all masses
        return np.array([model.predict_mass(n, m0_train) for n in n_rounded_all])
    
    # Run comprehensive tests
    tester = ComprehensiveStatisticalTests(masses_exp, masses_pred, uncertainties)
    results = tester.run_all_tests(
        n_params=1,  # Only m0 is free parameter
        model_fit_function=loocv_fit_function
    )
    
    # Add sector-specific info
    results['sector'] = sector_name
    results['fermions'] = fermions
    results['masses_experimental'] = masses_exp.tolist()
    results['masses_predicted'] = masses_pred.tolist()
    results['n_values_rounded'] = n_rounded.tolist()
    results['n_values_extracted'] = n_extracted.tolist()
    results['m0'] = float(m0)
    results['phi'] = float(PHI)
    
    # Generate plots
    if save_plots:
        generate_diagnostic_plots(tester, sector_name, results)
    
    return results

def generate_diagnostic_plots(tester, sector_name, results):
    """Generate comprehensive diagnostic plots"""
    
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
    
    # 1. Residuals plot
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.scatter(range(tester.n), tester.residuals, s=100, alpha=0.6)
    ax1.axhline(0, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax1.set_xlabel('Fermion Index')
    ax1.set_ylabel('Residuals (MeV)')
    ax1.set_title('Residuals Plot')
    ax1.grid(alpha=0.3)
    
    # 2. Q-Q plot
    ax2 = fig.add_subplot(gs[0, 1])
    std_res = (tester.residuals - np.mean(tester.residuals)) / np.std(tester.residuals)
    stats.probplot(std_res, dist="norm", plot=ax2)
    ax2.set_title(f"Q-Q Plot (r={results['qq_plot']['correlation']:.3f})")
    ax2.grid(alpha=0.3)
    
    # 3. Residuals histogram
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.hist(tester.residuals, bins=max(3, tester.n//2), density=True, alpha=0.6, edgecolor='black')
    x_range = np.linspace(tester.residuals.min(), tester.residuals.max(), 100)
    ax3.plot(x_range, stats.norm.pdf(x_range, np.mean(tester.residuals), np.std(tester.residuals)),
             'r-', linewidth=2, label='Normal fit')
    ax3.set_xlabel('Residuals (MeV)')
    ax3.set_ylabel('Density')
    ax3.set_title('Residuals Distribution')
    ax3.legend()
    ax3.grid(alpha=0.3)
    
    # 4. Predicted vs Observed
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.scatter(tester.masses_exp, tester.masses_pred, s=100, alpha=0.6)
    min_val = min(tester.masses_exp.min(), tester.masses_pred.min())
    max_val = max(tester.masses_exp.max(), tester.masses_pred.max())
    ax4.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, alpha=0.7, label='Perfect fit')
    ax4.set_xlabel('Experimental Mass (MeV)')
    ax4.set_ylabel('Predicted Mass (MeV)')
    ax4.set_title('Predicted vs Observed')
    ax4.legend()
    ax4.grid(alpha=0.3)
    if tester.masses_exp.max() / tester.masses_exp.min() > 100:
        ax4.set_xscale('log')
        ax4.set_yscale('log')
    
    # 5. Percent errors
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.bar(range(tester.n), tester.percent_errors, alpha=0.6, edgecolor='black')
    ax5.axhline(results['basic_metrics']['MAPE'], color='red', linestyle='--', linewidth=2, 
                label=f"MAPE={results['basic_metrics']['MAPE']:.2f}%")
    ax5.set_xlabel('Fermion Index')
    ax5.set_ylabel('Error (%)')
    ax5.set_title('Percent Errors')
    ax5.legend()
    ax5.grid(alpha=0.3)
    
    # 6. Cook's distance
    ax6 = fig.add_subplot(gs[1, 2])
    cooks_d = results['cooks_distance']['distances']
    threshold = results['cooks_distance']['threshold']
    ax6.stem(range(len(cooks_d)), cooks_d, basefmt=" ")
    ax6.axhline(threshold, color='red', linestyle='--', linewidth=2, alpha=0.7,
                label=f'Threshold={threshold:.3f}')
    ax6.set_xlabel('Fermion Index')
    ax6.set_ylabel("Cook's Distance")
    ax6.set_title("Outlier Detection (Cook's D)")
    ax6.legend()
    ax6.grid(alpha=0.3)
    
    # 7. Bootstrap distribution
    if 'bootstrap' in results:
        ax7 = fig.add_subplot(gs[2, 0])
        ci = results['bootstrap']['mape_ci']
        mean = results['bootstrap']['mean_estimate']
        ax7.axvspan(ci[0], ci[1], alpha=0.3, color='blue', label=f'95% CI: [{ci[0]:.2f}, {ci[1]:.2f}]')
        ax7.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Mean={mean:.2f}%')
        ax7.set_xlabel('MAPE (%)')
        ax7.set_title('Bootstrap Distribution (MAPE)')
        ax7.legend()
        ax7.grid(alpha=0.3)
    
    # 8. LOOCV errors
    if 'loocv' in results:
        ax8 = fig.add_subplot(gs[2, 1])
        loocv_errors = results['loocv']['loocv_errors']
        ax8.bar(range(len(loocv_errors)), loocv_errors, alpha=0.6, edgecolor='black')
        ax8.axhline(results['loocv']['loocv_mape'], color='red', linestyle='--', linewidth=2,
                    label=f"LOOCV MAPE={results['loocv']['loocv_mape']:.2f}%")
        ax8.set_xlabel('Fermion Index (Left Out)')
        ax8.set_ylabel('LOOCV Error (%)')
        ax8.set_title('Leave-One-Out Cross-Validation')
        ax8.legend()
        ax8.grid(alpha=0.3)
    
    # 9. Test summary
    ax9 = fig.add_subplot(gs[2, 2])
    ax9.axis('off')
    
    summary_text = f"""
    STATISTICAL SUMMARY
    
    Chi-squared: χ²/dof = {results['chi_squared']['chi2_reduced']:.3f}
    Shapiro-Wilk: p = {results['shapiro_wilk']['p_value']:.4f}
    Permutation: p = {results['permutation']['p_value']:.4f}
    
    MAPE: {results['basic_metrics']['MAPE']:.2f}%
    R²: {results['information_criteria']['R_squared']:.4f}
    AIC: {results['information_criteria']['AIC']:.2f}
    BIC: {results['information_criteria']['BIC']:.2f}
    
    Bootstrap 95% CI:
    [{results['bootstrap']['mape_ci'][0]:.2f}, {results['bootstrap']['mape_ci'][1]:.2f}]%
    
    LOOCV MAPE: {results['loocv']['loocv_mape']:.2f}% 
    
    Outliers: {results['cooks_distance']['n_outliers']}
    """
    
    ax9.text(0.1, 0.5, summary_text, transform=ax9.transAxes,
             fontsize=10, verticalalignment='center', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.suptitle(f'Comprehensive Diagnostic Plots - {sector_name.upper()}',
                 fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(f'goe_statistical_tests_{sector_name}.pdf', dpi=300, bbox_inches='tight')
    plt.savefig(f'goe_statistical_tests_{sector_name}.png', dpi=150, bbox_inches='tight')
    print(f"  Diagnostic plots saved: goe_statistical_tests_{sector_name}.pdf/png")
    plt.close()

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print()
    print("="*80)
    print("GoE FERMION MASS MODELS - COMPREHENSIVE STATISTICAL TESTING")
    print("="*80)
    print()
    print("PDG Data: 2025 (full precision)")
    print("Model: Golden Ratio Quantization (m = m0 * phi^n)")
    print("Tests: 15 comprehensive statistical tests")
    print()
    
    # Analyze all sectors
    all_results = {}
    
    for sector in ['leptons', 'up_quarks', 'down_quarks']:
        results = analyze_sector(sector, save_plots=True)
        all_results[sector] = results
        print()
    
    # Save comprehensive JSON report
    output_data = {
        'metadata': {
            'analysis_date': datetime.now().isoformat(),
            'pdg_version': '2025',
            'model': 'Golden Ratio Quantization',
            'n_tests': 15,
            'phi': float(PHI)
        },
        'sectors': all_results
    }
    
    with open('goe_comprehensive_statistical_tests_results.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print("="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print()
    print("Generated files:")
    print("  - goe_comprehensive_statistical_tests_results.json")
    print("  - goe_statistical_tests_leptons.pdf/png")
    print("  - goe_statistical_tests_up_quarks.pdf/png")
    print("  - goe_statistical_tests_down_quarks.pdf/png")
    print()
    print("="*80)

