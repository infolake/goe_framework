#!/usr/bin/env python3
"""
GoE Fermion Mass Models - GPU-Accelerated Statistical Testing

Filename: goe_fermion_statistical_tests_gpu.py
Modified: 2025-10-31
Author: Dr. Guilherme de Camargo
Email: camargo@phiq.io

Description:
    GPU-accelerated version for RTX 4090 using PyTorch
    Runs 100k bootstrap + 100k permutation samples in <1 minute
    
Hardware Requirements:
    - NVIDIA GPU with CUDA support (tested on RTX 4090)
    - 8+ GB VRAM recommended
    - PyTorch with CUDA

Usage:
    python3 goe_fermion_statistical_tests_gpu.py
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import seaborn as sns
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# PyTorch for GPU acceleration
import torch
import torch.nn.functional as F

# Check GPU availability
if torch.cuda.is_available():
    device = torch.device('cuda')
    print(f"GPU Detected: {torch.cuda.get_device_name(0)}")
    print(f"CUDA Version: {torch.version.cuda}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
else:
    device = torch.device('cpu')
    print("WARNING: GPU not available, using CPU")

print(f"Using device: {device}")
print()

# Set random seeds for reproducibility
np.random.seed(42)
torch.manual_seed(42)
if torch.cuda.is_available():
    torch.cuda.manual_seed(42)

# Plotting style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10

# =============================================================================
# CONSTANTS
# =============================================================================

PHI = (1 + np.sqrt(5)) / 2

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
# GPU-ACCELERATED STATISTICAL TESTS
# =============================================================================

class GPUAcceleratedTests:
    """GPU-accelerated statistical tests using PyTorch"""
    
    def __init__(self, masses_exp, masses_pred, uncertainties=None):
        self.n = len(masses_exp)
        
        # Convert to PyTorch tensors on GPU
        self.masses_exp_torch = torch.tensor(masses_exp, dtype=torch.float32, device=device)
        self.masses_pred_torch = torch.tensor(masses_pred, dtype=torch.float32, device=device)
        
        # CPU versions for scipy compatibility
        self.masses_exp = np.array(masses_exp)
        self.masses_pred = np.array(masses_pred)
        
        # Handle uncertainties
        if uncertainties is not None:
            unc_list = []
            for unc in uncertainties:
                if isinstance(unc, tuple):
                    unc_list.append(np.mean(unc))
                else:
                    unc_list.append(unc)
            self.uncertainties = np.array(unc_list)
            self.uncertainties_torch = torch.tensor(self.uncertainties, dtype=torch.float32, device=device)
        else:
            self.uncertainties = None
            self.uncertainties_torch = None
        
        # Calculate residuals
        self.residuals_torch = self.masses_pred_torch - self.masses_exp_torch
        self.residuals = self.residuals_torch.cpu().numpy()
        
        self.rel_residuals_torch = self.residuals_torch / self.masses_exp_torch
        self.rel_residuals = self.rel_residuals_torch.cpu().numpy()
        
        self.percent_errors_torch = torch.abs(self.rel_residuals_torch) * 100
        self.percent_errors = self.percent_errors_torch.cpu().numpy()
    
    # =========================================================================
    # GPU-ACCELERATED BOOTSTRAP (100k samples)
    # =========================================================================
    
    def bootstrap_gpu(self, n_bootstrap=100000, confidence=0.95):
        """
        GPU-accelerated bootstrap with 100k samples
        
        RTX 4090: ~5-10 seconds for 100k samples
        """
        print(f"  Running GPU Bootstrap with {n_bootstrap:,} samples...")
        
        start_time = torch.cuda.Event(enable_timing=True)
        end_time = torch.cuda.Event(enable_timing=True)
        
        start_time.record()
        
        # Generate all bootstrap indices at once on GPU
        indices = torch.randint(0, self.n, (n_bootstrap, self.n), device=device)
        
        # Gather samples
        bootstrap_errors = self.percent_errors_torch[indices]
        
        # Calculate statistics along sample dimension
        bootstrap_means = torch.mean(bootstrap_errors, dim=1)
        bootstrap_stds = torch.std(bootstrap_errors, dim=1)
        
        end_time.record()
        torch.cuda.synchronize()
        elapsed_time = start_time.elapsed_time(end_time) / 1000  # Convert to seconds
        
        # Calculate confidence intervals
        alpha = 1 - confidence
        ci_mean = torch.quantile(bootstrap_means, torch.tensor([alpha/2, 1-alpha/2], device=device))
        ci_std = torch.quantile(bootstrap_stds, torch.tensor([alpha/2, 1-alpha/2], device=device))
        
        print(f"    Completed in {elapsed_time:.2f} seconds")
        print(f"    Throughput: {n_bootstrap/elapsed_time:.0f} samples/sec")
        
        return {
            'test_name': 'GPU Bootstrap',
            'n_bootstrap': n_bootstrap,
            'confidence_level': confidence,
            'mean_error_ci': [float(ci_mean[0].cpu()), float(ci_mean[1].cpu())],
            'std_error_ci': [float(ci_std[0].cpu()), float(ci_std[1].cpu())],
            'mean_estimate': float(torch.mean(self.percent_errors_torch).cpu()),
            'std_estimate': float(torch.std(self.percent_errors_torch).cpu()),
            'gpu_time_seconds': elapsed_time,
            'samples_per_second': int(n_bootstrap/elapsed_time)
        }
    
    # =========================================================================
    # GPU-ACCELERATED PERMUTATION TEST (100k permutations)
    # =========================================================================
    
    def permutation_test_gpu(self, n_permutations=100000, n_values=None, m0=None, phi=PHI):
        """
        GPU-accelerated permutation test with CORRECT method (as in paper)
        
        Permutes N-VALUES (not predictions) to test if n-value assignments are accidental
        
        Parameters:
        -----------
        n_values : array-like
            Integer topological charges for this sector
        m0 : float
            Base mass for this sector
        phi : float
            Golden ratio constant
        
        RTX 4090: ~5-10 seconds for 100k permutations
        """
        print(f"  Running GPU Permutation Test (n-values) with {n_permutations:,} permutations...")
        
        if n_values is None or m0 is None:
            # Fallback to old method (for compatibility)
            return self._permutation_test_predictions_legacy(n_permutations)
        
        start_time = torch.cuda.Event(enable_timing=True)
        end_time = torch.cuda.Event(enable_timing=True)
        
        start_time.record()
        
        # Observed statistic (negative MAPE for maximization)
        observed_stat = -torch.mean(self.percent_errors_torch)
        
        # Convert to GPU tensors
        n_values_torch = torch.tensor(n_values, dtype=torch.float32, device=device)
        m0_torch = torch.tensor(m0, dtype=torch.float32, device=device)
        phi_torch = torch.tensor(phi, dtype=torch.float32, device=device)
        masses_exp_torch = self.masses_exp_torch
        
        # Generate null distribution by permuting n-values
        null_stats = torch.zeros(n_permutations, device=device)
        
        # Process in batches to avoid OOM
        batch_size = 10000
        n_batches = (n_permutations + batch_size - 1) // batch_size
        
        for i in range(n_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, n_permutations)
            current_batch_size = end_idx - start_idx
            
            # Random permutations of n-values (shuffle within this sector)
            batch_mape = torch.zeros(current_batch_size, device=device)
            
            for j in range(current_batch_size):
                # Shuffle n-values
                perm_indices = torch.randperm(self.n, device=device)
                n_perm = n_values_torch[perm_indices]
                
                # Recalculate predictions with permuted n-values
                masses_pred_perm = m0_torch * (phi_torch ** n_perm)
                
                # Calculate percent errors
                perm_errors = torch.abs(masses_pred_perm - masses_exp_torch) / masses_exp_torch * 100
                
                # MAPE (negative for maximization)
                batch_mape[j] = -torch.mean(perm_errors)
            
            null_stats[start_idx:end_idx] = batch_mape
        
        # Calculate p-value (how many permuted MAPEs are as good or better than observed)
        p_value = torch.sum(null_stats >= observed_stat).float() / n_permutations
        
        end_time.record()
        torch.cuda.synchronize()
        elapsed_time = start_time.elapsed_time(end_time) / 1000
        
        # Calculate statistics
        permuted_mape_median = -torch.median(null_stats).cpu()
        permuted_mape_mean = -torch.mean(null_stats).cpu()
        separation_ratio = permuted_mape_mean / torch.mean(self.percent_errors_torch).cpu()
        
        print(f"    Completed in {elapsed_time:.2f} seconds")
        print(f"    Throughput: {n_permutations/elapsed_time:.0f} permutations/sec")
        print(f"    Original MAPE: {torch.mean(self.percent_errors_torch).item():.2f}%")
        print(f"    Permuted MAPE (median): {permuted_mape_median:.2f}%")
        print(f"    Separation ratio: {separation_ratio:.2e}")
        
        return {
            'test_name': 'GPU Permutation Test (n-values)',
            'n_permutations': n_permutations,
            'observed_statistic': float(observed_stat.cpu()),
            'observed_mape': float(torch.mean(self.percent_errors_torch).cpu()),
            'permuted_mape_median': float(permuted_mape_median),
            'permuted_mape_mean': float(permuted_mape_mean),
            'separation_ratio': float(separation_ratio),
            'null_mean': float(torch.mean(null_stats).cpu()),
            'null_std': float(torch.std(null_stats).cpu()),
            'p_value': float(p_value.cpu()),
            'interpretation': 'HIGHLY SIGNIFICANT - n-values are NOT arbitrary' if p_value < 0.01 else ('Significantly better than random' if p_value < 0.05 else 'Not significant'),
            'reject_H0': bool(p_value < 0.05),
            'gpu_time_seconds': elapsed_time,
            'permutations_per_second': int(n_permutations/elapsed_time)
        }
    
    def _permutation_test_predictions_legacy(self, n_permutations=100000):
        """Legacy method - permutes predictions (not recommended, kept for compatibility)"""
        print(f"  Running GPU Permutation Test (LEGACY - predictions) with {n_permutations:,} permutations...")
        
        start_time = torch.cuda.Event(enable_timing=True)
        end_time = torch.cuda.Event(enable_timing=True)
        
        start_time.record()
        
        observed_stat = -torch.mean(self.percent_errors_torch)
        null_stats = torch.zeros(n_permutations, device=device)
        
        batch_size = 10000
        n_batches = (n_permutations + batch_size - 1) // batch_size
        
        for i in range(n_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, n_permutations)
            current_batch_size = end_idx - start_idx
            
            perm_indices = torch.argsort(torch.rand(current_batch_size, self.n, device=device), dim=1)
            perm_pred = self.masses_pred_torch[perm_indices]
            perm_errors = torch.abs(perm_pred - self.masses_exp_torch.unsqueeze(0)) / self.masses_exp_torch.unsqueeze(0) * 100
            null_stats[start_idx:end_idx] = -torch.mean(perm_errors, dim=1)
        
        p_value = torch.sum(null_stats >= observed_stat).float() / n_permutations
        
        end_time.record()
        torch.cuda.synchronize()
        elapsed_time = start_time.elapsed_time(end_time) / 1000
        
        return {
            'test_name': 'GPU Permutation Test (LEGACY - predictions)',
            'n_permutations': n_permutations,
            'observed_statistic': float(observed_stat.cpu()),
            'p_value': float(p_value.cpu()),
            'interpretation': 'NOTE: This tests predictions, not n-values. Use n-value permutation for geometric structure.',
            'reject_H0': bool(p_value < 0.05),
            'gpu_time_seconds': elapsed_time
        }
    
    # =========================================================================
    # CPU TESTS (scipy-based, kept for compatibility)
    # =========================================================================
    
    def chi_squared_test(self, n_params=1):
        """Chi-squared test (CPU)"""
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
    
    def shapiro_wilk_test(self):
        """Shapiro-Wilk test (CPU)"""
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
                'interpretation': 'Sample too small',
                'reject_H0': None
            }
    
    def kolmogorov_smirnov_test(self):
        """KS test (CPU)"""
        std_res = (self.residuals - np.mean(self.residuals)) / np.std(self.residuals)
        ks_stat, p_value = stats.kstest(std_res, 'norm')
        
        return {
            'test_name': 'Kolmogorov-Smirnov Test',
            'statistic': float(ks_stat),
            'p_value': float(p_value),
            'interpretation': 'Residuals normal' if p_value > 0.05 else 'Residuals non-normal',
            'reject_H0': bool(p_value < 0.05)
        }
    
    def information_criteria(self, n_params=1):
        """AIC/BIC (CPU)"""
        n = self.n
        rss = np.sum(self.residuals**2)
        sigma2 = rss / n
        
        log_likelihood = -0.5 * n * (np.log(2 * np.pi) + np.log(sigma2) + 1)
        
        aic = 2 * n_params - 2 * log_likelihood
        bic = n_params * np.log(n) - 2 * log_likelihood
        
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
    
    def basic_metrics(self):
        """Basic error metrics (GPU)"""
        mape = torch.mean(self.percent_errors_torch)
        rmse = torch.sqrt(torch.mean(self.residuals_torch**2))
        mae = torch.mean(torch.abs(self.residuals_torch))
        max_err = torch.max(self.percent_errors_torch)
        min_err = torch.min(self.percent_errors_torch)
        
        return {
            'test_name': 'Basic Metrics',
            'MAPE': float(mape.cpu()),
            'RMSE': float(rmse.cpu()),
            'MAE': float(mae.cpu()),
            'max_error_percent': float(max_err.cpu()),
            'min_error_percent': float(min_err.cpu())
        }
    
    def run_all_gpu_tests(self, n_params=1, n_bootstrap=100000, n_permutations=100000, n_values=None, m0=None, phi=PHI):
        """Run all GPU-accelerated tests"""
        results = {}
        
        print("  [1/7] Basic metrics (GPU)...")
        results['basic_metrics'] = self.basic_metrics()
        
        print("  [2/7] Chi-squared test...")
        results['chi_squared'] = self.chi_squared_test(n_params)
        
        print("  [3/7] Shapiro-Wilk test...")
        results['shapiro_wilk'] = self.shapiro_wilk_test()
        
        print("  [4/7] Kolmogorov-Smirnov test...")
        results['kolmogorov_smirnov'] = self.kolmogorov_smirnov_test()
        
        print("  [5/7] Information criteria...")
        results['information_criteria'] = self.information_criteria(n_params)
        
        print(f"  [6/7] GPU Bootstrap ({n_bootstrap:,} samples)...")
        results['bootstrap_gpu'] = self.bootstrap_gpu(n_bootstrap, confidence=0.95)
        
        print(f"  [7/7] GPU Permutation test ({n_permutations:,})...")
        results['permutation_gpu'] = self.permutation_test_gpu(n_permutations, n_values=n_values, m0=m0, phi=phi)
        
        return results

# =============================================================================
# GOLDEN RATIO MODEL
# =============================================================================

class GoldenRatioModel:
    """Model: m = m0 * phi^n"""
    
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
# ANALYSIS AND PLOTTING
# =============================================================================

def analyze_sector_gpu(sector_name, n_bootstrap=100000, n_permutations=100000, save_plots=True):
    """GPU-accelerated analysis for a sector"""
    print("="*80)
    print(f"ANALYZING SECTOR: {sector_name.upper()} (GPU-ACCELERATED)")
    print("="*80)
    print()
    
    # Get data
    fermions = SECTORS[sector_name]
    masses_exp = np.array([FERMION_MASSES_EXP[f] for f in fermions])
    uncertainties = [FERMION_MASSES_UNC[f] for f in fermions]
    
    # Fit model
    model = GoldenRatioModel()
    masses_pred, m0, n_rounded, n_extracted = model.fit_and_predict(masses_exp)
    
    # Run GPU tests
    tester = GPUAcceleratedTests(masses_exp, masses_pred, uncertainties)
    results = tester.run_all_gpu_tests(
        n_params=1,
        n_bootstrap=n_bootstrap,
        n_permutations=n_permutations,
        n_values=n_rounded,  # Pass n-values for correct permutation test
        m0=m0,                # Pass m0 for recalculation
        phi=PHI              # Pass phi constant
    )
    
    # Add sector info
    results['sector'] = sector_name
    results['fermions'] = fermions
    results['masses_experimental'] = masses_exp.tolist()
    results['masses_predicted'] = masses_pred.tolist()
    results['n_values_rounded'] = n_rounded.tolist()
    results['n_values_extracted'] = n_extracted.tolist()
    results['m0'] = float(m0)
    results['phi'] = float(PHI)
    
    # Generate simplified plot
    if save_plots:
        generate_gpu_diagnostic_plot(tester, sector_name, results)
    
    print()
    return results

def generate_gpu_diagnostic_plot(tester, sector_name, results):
    """Generate diagnostic plot"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    # 1. Residuals
    ax = axes[0]
    ax.scatter(range(tester.n), tester.residuals, s=100, alpha=0.6)
    ax.axhline(0, color='red', linestyle='--', linewidth=2)
    ax.set_xlabel('Fermion Index')
    ax.set_ylabel('Residuals (MeV)')
    ax.set_title('Residuals Plot')
    ax.grid(alpha=0.3)
    
    # 2. Q-Q plot
    ax = axes[1]
    std_res = (tester.residuals - np.mean(tester.residuals)) / np.std(tester.residuals)
    stats.probplot(std_res, dist="norm", plot=ax)
    ax.set_title('Q-Q Plot')
    ax.grid(alpha=0.3)
    
    # 3. Percent errors
    ax = axes[2]
    ax.bar(range(tester.n), tester.percent_errors, alpha=0.6, edgecolor='black')
    ax.axhline(results['basic_metrics']['MAPE'], color='red', linestyle='--', linewidth=2,
               label=f"MAPE={results['basic_metrics']['MAPE']:.2f}%")
    ax.set_xlabel('Fermion Index')
    ax.set_ylabel('Error (%)')
    ax.set_title('Percent Errors')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # 4. Pred vs Obs
    ax = axes[3]
    ax.scatter(tester.masses_exp, tester.masses_pred, s=100, alpha=0.6)
    min_val = min(tester.masses_exp.min(), tester.masses_pred.min())
    max_val = max(tester.masses_exp.max(), tester.masses_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect fit')
    ax.set_xlabel('Experimental (MeV)')
    ax.set_ylabel('Predicted (MeV)')
    ax.set_title('Predicted vs Observed')
    ax.legend()
    ax.grid(alpha=0.3)
    if tester.masses_exp.max() / tester.masses_exp.min() > 100:
        ax.set_xscale('log')
        ax.set_yscale('log')
    
    # 5. Bootstrap CI
    ax = axes[4]
    if 'bootstrap_gpu' in results:
        ci = results['bootstrap_gpu']['mean_error_ci']
        mean = results['bootstrap_gpu']['mean_estimate']
        n_boot = results['bootstrap_gpu']['n_bootstrap']
        time_boot = results['bootstrap_gpu']['gpu_time_seconds']
        
        ax.axvspan(ci[0], ci[1], alpha=0.3, color='blue', 
                   label=f'95% CI: [{ci[0]:.2f}, {ci[1]:.2f}]')
        ax.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Mean={mean:.2f}%')
        ax.set_xlabel('MAPE (%)')
        ax.set_title(f'Bootstrap ({n_boot:,} samples, {time_boot:.1f}s)')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
    
    # 6. Summary
    ax = axes[5]
    ax.axis('off')
    
    summary_text = f"""
GPU-ACCELERATED RESULTS

MAPE: {results['basic_metrics']['MAPE']:.2f}%
Chi2/dof: {results['chi_squared']['chi2_reduced']:.3f}
R2: {results['information_criteria']['R_squared']:.4f}

Shapiro-Wilk p: {results['shapiro_wilk']['p_value']:.4f}

Bootstrap (GPU):
  Samples: {results['bootstrap_gpu']['n_bootstrap']:,}
  Time: {results['bootstrap_gpu']['gpu_time_seconds']:.2f}s
  Speed: {results['bootstrap_gpu']['samples_per_second']:,}/s
  CI: [{results['bootstrap_gpu']['mean_error_ci'][0]:.2f}, {results['bootstrap_gpu']['mean_error_ci'][1]:.2f}]%

Permutation (GPU):
  Tests: {results['permutation_gpu']['n_permutations']:,}
  Time: {results['permutation_gpu']['gpu_time_seconds']:.2f}s
  Speed: {results['permutation_gpu']['permutations_per_second']:,}/s
  p-value: {results['permutation_gpu']['p_value']:.6f}
    """
    
    ax.text(0.1, 0.5, summary_text, transform=ax.transAxes,
            fontsize=9, verticalalignment='center', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    plt.suptitle(f'GPU-Accelerated Diagnostic Plots - {sector_name.upper()}',
                 fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'goe_gpu_tests_{sector_name}.pdf', dpi=300, bbox_inches='tight')
    plt.savefig(f'goe_gpu_tests_{sector_name}.png', dpi=150, bbox_inches='tight')
    print(f"  Plots saved: goe_gpu_tests_{sector_name}.pdf/png")
    plt.close()

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print()
    print("="*80)
    print("GoE FERMION MASS MODELS - GPU-ACCELERATED STATISTICAL TESTING")
    print("="*80)
    print()
    print(f"Device: {device}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    print()
    print("PDG Data: 2025")
    print("Model: Golden Ratio Quantization")
    print("Bootstrap samples: 100,000 (GPU)")
    print("Permutation tests: 100,000 (GPU)")
    print()
    
    # Analyze all sectors
    all_results = {}
    total_start = datetime.now()
    
    for sector in ['leptons', 'up_quarks', 'down_quarks']:
        results = analyze_sector_gpu(
            sector,
            n_bootstrap=100000,
            n_permutations=100000,
            save_plots=True
        )
        all_results[sector] = results
    
    total_time = (datetime.now() - total_start).total_seconds()
    
    # Save results
    output_data = {
        'metadata': {
            'analysis_date': datetime.now().isoformat(),
            'pdg_version': '2025',
            'model': 'Golden Ratio Quantization',
            'gpu_device': str(device),
            'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU',
            'bootstrap_samples': 100000,
            'permutation_tests': 100000,
            'total_time_seconds': total_time,
            'phi': float(PHI)
        },
        'sectors': all_results
    }
    
    with open('goe_gpu_statistical_tests_results.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print()
    print("="*80)
    print("GPU-ACCELERATED ANALYSIS COMPLETE")
    print("="*80)
    print()
    print(f"Total runtime: {total_time:.2f} seconds")
    print()
    print("Generated files:")
    print("  - goe_gpu_statistical_tests_results.json")
    print("  - goe_gpu_tests_leptons.pdf/png")
    print("  - goe_gpu_tests_up_quarks.pdf/png")
    print("  - goe_gpu_tests_down_quarks.pdf/png")
    print()
    
    # Print summary
    print("="*80)
    print("PERFORMANCE SUMMARY")
    print("="*80)
    for sector, res in all_results.items():
        print(f"\n{sector.upper()}:")
        print(f"  MAPE: {res['basic_metrics']['MAPE']:.2f}%")
        print(f"  Bootstrap: {res['bootstrap_gpu']['samples_per_second']:,} samples/s")
        print(f"  Permutation: {res['permutation_gpu']['permutations_per_second']:,} perms/s")
        print(f"  p-value: {res['permutation_gpu']['p_value']:.6f}")
    
    print()
    print("="*80)

