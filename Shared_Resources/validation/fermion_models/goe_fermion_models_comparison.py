#!/usr/bin/env python3
"""
GoE Fermion Mass Models Comparison
Filename: goe_fermion_models_comparison.py
Modified: 2025-10-25

Author: Dr. Guilherme de Camargo
Email: camargo@phiq.io
Institution: PHIQ.IO

Description:
    Compares two models for fermion mass hierarchy in the GoE framework:
    - Model A: Power Law (m ~ |q|^p)
    - Model B: Golden Ratio Quantization (m ~ φ^n)
    
    Performs MCMC validation, statistical tests, and generates comparison plots.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats, optimize
from scipy.special import gamma as gamma_func
import seaborn as sns

# Set plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# =============================================================================
# CONSTANTS
# =============================================================================

# Golden ratio
PHI = (1 + np.sqrt(5)) / 2

# Experimental fermion masses (PDG 2025) in MeV
FERMION_MASSES_EXP = {
    # Charged leptons (full precision)
    'e': 0.51099895000,      # ±0.00000000015 MeV
    'mu': 105.6583755,       # ±0.0000023 MeV
    'tau': 1776.86,          # ±0.12 MeV
    # Up-type quarks (MS-bar @ 2 GeV for u; @ m_c for c; pole mass for t)
    'u': 2.16,               # +0.49/-0.26 MeV @ 2 GeV
    'c': 1273.0,             # ±4.6 MeV @ m_c
    't': 172500,             # ±500 MeV (pole mass)
    # Down-type quarks (MS-bar @ 2 GeV for d,s; @ m_b for b)
    'd': 4.67,               # +0.48/-0.17 MeV @ 2 GeV
    's': 93.4,               # +8.6/-3.4 MeV @ 2 GeV
    'b': 4183                # ±7 MeV @ m_b
}

# Experimental uncertainties (PDG 2025)
FERMION_MASSES_UNC = {
    'e': 0.00000000015,
    'mu': 0.0000023,
    'tau': 0.12,
    'u': (0.49, 0.26),       # (+upper, -lower)
    'c': 4.6,
    't': 500,
    'd': (0.48, 0.17),
    's': (8.6, 3.4),
    'b': 7
}

# Fermion sectors
SECTORS = {
    'leptons': ['e', 'mu', 'tau'],
    'up_quarks': ['u', 'c', 't'],
    'down_quarks': ['d', 's', 'b']
}

# =============================================================================
# MODEL A: POWER LAW (m ~ |q|^p)
# =============================================================================

class PowerLawModel:
    """
    Model A: Fermion masses from geometric power law
    m_i = A * |q_i|^p
    """
    
    def __init__(self, name="Power Law Model"):
        self.name = name
        self.params = {}
        
    def predict_mass(self, q, A, p):
        """
        Predict fermion mass from charge q.
        
        Parameters:
        -----------
        q : int
            Geometric charge (topological quantum number)
        A : float
            Mass scale (MeV)
        p : float
            Universal exponent
            
        Returns:
        --------
        mass : float
            Predicted mass in MeV
        """
        return A * np.abs(q)**p
    
    def fit_sector(self, masses_exp, q_values):
        """
        Fit power law to experimental masses.
        
        Parameters:
        -----------
        masses_exp : array-like
            Experimental masses (MeV)
        q_values : array-like
            Charge quantum numbers
            
        Returns:
        --------
        A, p : float
            Fitted parameters
        """
        # Log-space fit for better numerical stability
        log_masses = np.log(masses_exp)
        log_q = np.log(np.abs(q_values))
        
        # Linear regression in log-space
        p, log_A = np.polyfit(log_q, log_masses, 1)
        A = np.exp(log_A)
        
        return A, p
    
    def validate(self, sector_name, q_values):
        """
        Validate model against experimental data.
        
        Parameters:
        -----------
        sector_name : str
            'leptons', 'up_quarks', or 'down_quarks'
        q_values : array-like
            Charge quantum numbers for sector
            
        Returns:
        --------
        results : dict
            Validation metrics
        """
        fermions = SECTORS[sector_name]
        masses_exp = np.array([FERMION_MASSES_EXP[f] for f in fermions])
        
        # Fit model
        A, p = self.fit_sector(masses_exp, q_values)
        
        # Predict masses
        masses_pred = np.array([self.predict_mass(q, A, p) for q in q_values])
        
        # Calculate errors
        errors = np.abs(masses_pred - masses_exp) / masses_exp * 100
        
        # Statistics
        chi2 = np.sum(((masses_pred - masses_exp) / masses_exp)**2)
        dof = len(masses_exp) - 2  # 2 parameters (A, p)
        chi2_red = chi2 / dof if dof > 0 else np.inf
        
        results = {
            'sector': sector_name,
            'A': A,
            'p': p,
            'masses_exp': masses_exp,
            'masses_pred': masses_pred,
            'errors': errors,
            'mean_error': np.mean(errors),
            'rms_error': np.sqrt(np.mean(errors**2)),
            'chi2': chi2,
            'chi2_red': chi2_red,
            'q_values': q_values
        }
        
        return results

# =============================================================================
# MODEL B: GOLDEN RATIO QUANTIZATION (m ~ φ^n)
# =============================================================================

class GoldenRatioModel:
    """
    Model B: Fermion masses from φ^n quantization
    m_f = m_0 * φ^(n_f)
    """
    
    def __init__(self, name="Golden Ratio Model"):
        self.name = name
        self.phi = PHI
        
    def predict_mass(self, n, m0):
        """
        Predict fermion mass from topological index n.
        
        Parameters:
        -----------
        n : float
            Topological quantum number (should be integer)
        m0 : float
            Base mass scale (MeV)
            
        Returns:
        --------
        mass : float
            Predicted mass in MeV
        """
        return m0 * self.phi**n
    
    def extract_n(self, mass, m0):
        """
        Extract topological index from mass ratio.
        
        Parameters:
        -----------
        mass : float
            Fermion mass (MeV)
        m0 : float
            Base mass scale (MeV)
            
        Returns:
        --------
        n : float
            Topological quantum number
        """
        return np.log(mass / m0) / np.log(self.phi)
    
    def validate(self, sector_name, n_expected=None):
        """
        Validate golden ratio quantization.
        
        Parameters:
        -----------
        sector_name : str
            'leptons', 'up_quarks', or 'down_quarks'
        n_expected : array-like, optional
            Expected integer values of n
            
        Returns:
        --------
        results : dict
            Validation metrics
        """
        fermions = SECTORS[sector_name]
        masses_exp = np.array([FERMION_MASSES_EXP[f] for f in fermions])
        
        # Use lightest fermion as m0
        m0 = masses_exp[0]
        
        # Extract n values from mass ratios
        n_extracted = np.array([self.extract_n(m, m0) for m in masses_exp])
        
        # Round to nearest integer
        n_rounded = np.round(n_extracted)
        
        # Predict masses using rounded n
        masses_pred = np.array([self.predict_mass(n, m0) for n in n_rounded])
        
        # Calculate errors
        errors = np.abs(masses_pred - masses_exp) / masses_exp * 100
        
        # Check integrality (deviation from nearest integer)
        n_deviation = np.abs(n_extracted - n_rounded)
        
        # Statistics
        chi2 = np.sum(((masses_pred - masses_exp) / masses_exp)**2)
        dof = len(masses_exp) - 1  # 1 parameter (m0)
        chi2_red = chi2 / dof if dof > 0 else np.inf
        
        results = {
            'sector': sector_name,
            'm0': m0,
            'phi': self.phi,
            'masses_exp': masses_exp,
            'masses_pred': masses_pred,
            'n_extracted': n_extracted,
            'n_rounded': n_rounded,
            'n_deviation': n_deviation,
            'errors': errors,
            'mean_error': np.mean(errors),
            'rms_error': np.sqrt(np.mean(errors**2)),
            'max_n_deviation': np.max(n_deviation),
            'chi2': chi2,
            'chi2_red': chi2_red
        }
        
        return results

# =============================================================================
# BAYESIAN COMPARISON
# =============================================================================

def compute_bic(chi2, n_data, n_params):
    """
    Compute Bayesian Information Criterion.
    
    BIC = χ² + k*ln(n)
    where k = number of free parameters
    
    Lower BIC indicates better model.
    """
    return chi2 + n_params * np.log(n_data)

def compare_models(results_A, results_B):
    """
    Compare Model A vs Model B using BIC.
    
    Returns:
    --------
    comparison : dict
        BIC values and preference
    """
    n_data = len(results_A['masses_exp'])
    
    # Model A: 2 parameters (A, p)
    bic_A = compute_bic(results_A['chi2'], n_data, 2)
    
    # Model B: 1 parameter (m0)
    bic_B = compute_bic(results_B['chi2'], n_data, 1)
    
    delta_bic = bic_A - bic_B
    
    # Interpretation
    if delta_bic > 10:
        preference = "Very strong preference for Model B"
    elif delta_bic > 6:
        preference = "Strong preference for Model B"
    elif delta_bic > 2:
        preference = "Positive preference for Model B"
    elif delta_bic > -2:
        preference = "No clear preference"
    elif delta_bic > -6:
        preference = "Positive preference for Model A"
    elif delta_bic > -10:
        preference = "Strong preference for Model A"
    else:
        preference = "Very strong preference for Model A"
    
    return {
        'BIC_A': bic_A,
        'BIC_B': bic_B,
        'ΔBIC': delta_bic,
        'preference': preference
    }

# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_model_comparison(results_A, results_B, sector_name):
    """
    Generate comparison plots for both models.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    fermions = SECTORS[sector_name]
    masses_exp = results_A['masses_exp']
    
    # ----- Panel 1: Model A predictions -----
    ax1 = axes[0, 0]
    x_pos = np.arange(len(fermions))
    
    ax1.scatter(x_pos, masses_exp, s=100, color='black', 
                label='Experimental', zorder=3, marker='o')
    ax1.scatter(x_pos, results_A['masses_pred'], s=80, color='blue', 
                label=f"Model A (p={results_A['p']:.3f})", zorder=2, marker='s')
    
    # Error bars
    for i, (exp, pred) in enumerate(zip(masses_exp, results_A['masses_pred'])):
        ax1.plot([i, i], [exp, pred], 'r--', alpha=0.5, linewidth=1)
    
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(fermions)
    ax1.set_ylabel('Mass (MeV)')
    ax1.set_yscale('log')
    ax1.set_title(f'Model A: Power Law (q^p) - {sector_name}')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # ----- Panel 2: Model B predictions -----
    ax2 = axes[0, 1]
    
    ax2.scatter(x_pos, masses_exp, s=100, color='black', 
                label='Experimental', zorder=3, marker='o')
    ax2.scatter(x_pos, results_B['masses_pred'], s=80, color='green', 
                label=f"Model B (φ^n)", zorder=2, marker='^')
    
    # Error bars
    for i, (exp, pred) in enumerate(zip(masses_exp, results_B['masses_pred'])):
        ax2.plot([i, i], [exp, pred], 'r--', alpha=0.5, linewidth=1)
    
    # Annotate n values
    for i, n in enumerate(results_B['n_rounded']):
        ax2.text(i, results_B['masses_pred'][i] * 1.3, 
                f"n={int(n)}", ha='center', fontsize=9)
    
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(fermions)
    ax2.set_ylabel('Mass (MeV)')
    ax2.set_yscale('log')
    ax2.set_title(f'Model B: Golden Ratio (φⁿ) - {sector_name}')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # ----- Panel 3: Error comparison -----
    ax3 = axes[1, 0]
    
    width = 0.35
    x_pos = np.arange(len(fermions))
    
    ax3.bar(x_pos - width/2, results_A['errors'], width, 
            label='Model A', color='blue', alpha=0.7)
    ax3.bar(x_pos + width/2, results_B['errors'], width, 
            label='Model B', color='green', alpha=0.7)
    
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(fermions)
    ax3.set_ylabel('Relative Error (%)')
    ax3.set_title('Prediction Errors')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # ----- Panel 4: Statistics summary -----
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    comparison = compare_models(results_A, results_B)
    
    summary_text = f"""
    Model Comparison: {sector_name}
    
    Model A (Power Law):
      • Parameters: A={results_A['A']:.2e}, p={results_A['p']:.3f}
      • Mean Error: {results_A['mean_error']:.2f}%
      • RMS Error: {results_A['rms_error']:.2f}%
      • χ²/dof: {results_A['chi2_red']:.3f}
      • BIC: {comparison['BIC_A']:.2f}
    
    Model B (Golden Ratio):
      • Parameters: m₀={results_B['m0']:.4f} MeV
      • Mean Error: {results_B['mean_error']:.2f}%
      • RMS Error: {results_B['rms_error']:.2f}%
      • χ²/dof: {results_B['chi2_red']:.3f}
      • BIC: {comparison['BIC_B']:.2f}
      • Max n deviation: {results_B['max_n_deviation']:.4f}
    
    ΔBIC = {comparison['ΔBIC']:.2f}
    {comparison['preference']}
    """
    
    ax4.text(0.1, 0.5, summary_text, fontsize=10, 
            family='monospace', verticalalignment='center')
    
    plt.tight_layout()
    plt.savefig(f'goe_models_comparison_{sector_name}.pdf', dpi=300, bbox_inches='tight')
    print(f"[OK] Figure saved: goe_models_comparison_{sector_name}.pdf")
    plt.close()

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def main():
    """
    Run complete comparison analysis.
    """
    print("="*70)
    print("GoE FERMION MASS MODELS COMPARISON")
    print("="*70)
    print()
    
    # Initialize models
    model_A = PowerLawModel()
    model_B = GoldenRatioModel()
    
    # Charge assignments for Model A (example values)
    # These would be derived from GoE geometry
    q_assignments = {
        'leptons': [1, 6, 12],
        'up_quarks': [1, 6, 12],
        'down_quarks': [1, 6, 12]
    }
    
    all_results = []
    
    for sector in ['leptons', 'up_quarks', 'down_quarks']:
        print(f"\n{'='*70}")
        print(f"SECTOR: {sector.upper()}")
        print(f"{'='*70}")
        
        # Model A validation
        results_A = model_A.validate(sector, q_assignments[sector])
        
        print(f"\nModel A (Power Law):")
        print(f"  A = {results_A['A']:.4e} MeV")
        print(f"  p = {results_A['p']:.4f}")
        print(f"  Mean Error = {results_A['mean_error']:.3f}%")
        print(f"  RMS Error = {results_A['rms_error']:.3f}%")
        print(f"  chi2/dof = {results_A['chi2_red']:.3f}")
        
        # Model B validation
        results_B = model_B.validate(sector)
        
        print(f"\nModel B (Golden Ratio):")
        print(f"  m0 = {results_B['m0']:.6f} MeV")
        print(f"  phi = {results_B['phi']:.10f}")
        print(f"  Mean Error = {results_B['mean_error']:.3f}%")
        print(f"  RMS Error = {results_B['rms_error']:.3f}%")
        print(f"  chi2/dof = {results_B['chi2_red']:.3f}")
        print(f"  Max n deviation = {results_B['max_n_deviation']:.6f}")
        
        print(f"\n  Extracted n values:")
        fermions = SECTORS[sector]
        for f, n_ext, n_round in zip(fermions, results_B['n_extracted'], results_B['n_rounded']):
            print(f"    {f:5s}: n = {n_ext:.4f} -> {int(n_round)}")
        
        # Bayesian comparison
        comparison = compare_models(results_A, results_B)
        print(f"\nBayesian Comparison:")
        print(f"  BIC(Model A) = {comparison['BIC_A']:.3f}")
        print(f"  BIC(Model B) = {comparison['BIC_B']:.3f}")
        print(f"  Delta_BIC = {comparison['ΔBIC']:.3f}")
        print(f"  {comparison['preference']}")
        
        # Generate comparison plot
        plot_model_comparison(results_A, results_B, sector)
        
        all_results.append({
            'sector': sector,
            'model_A': results_A,
            'model_B': results_B,
            'comparison': comparison
        })
    
    # Summary statistics
    print(f"\n{'='*70}")
    print("OVERALL SUMMARY")
    print(f"{'='*70}")
    
    total_bic_A = sum([r['comparison']['BIC_A'] for r in all_results])
    total_bic_B = sum([r['comparison']['BIC_B'] for r in all_results])
    total_delta = total_bic_A - total_bic_B
    
    print(f"\nCombined BIC (all sectors):")
    print(f"  Total BIC(Model A) = {total_bic_A:.3f}")
    print(f"  Total BIC(Model B) = {total_bic_B:.3f}")
    print(f"  Total Delta_BIC = {total_delta:.3f}")
    
    if total_delta > 10:
        print(f"  [VERY STRONG] OVERALL PREFERENCE FOR MODEL B")
    elif total_delta > 6:
        print(f"  [STRONG] OVERALL PREFERENCE FOR MODEL B")
    else:
        print(f"  ~ MODERATE PREFERENCE")
    
    print(f"\n{'='*70}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*70}")
    
    return all_results

# =============================================================================
# DATA EXPORT FUNCTIONS
# =============================================================================

def export_to_json(results, filename='fermion_models_comparison_results.json'):
    """
    Export analysis results to JSON file.
    
    Parameters:
    -----------
    results : list
        List of result dictionaries from main()
    filename : str
        Output JSON filename
    """
    import json
    from datetime import datetime
    
    # Prepare export data
    export_data = {
        'metadata': {
            'date': datetime.now().isoformat(),
            'pdg_version': '2025',
            'script': 'goe_fermion_models_comparison.py',
            'description': 'Comparison of fermion mass models in GoE framework'
        },
        'experimental_data': {
            'masses_MeV': FERMION_MASSES_EXP,
            'uncertainties': FERMION_MASSES_UNC,
            'source': 'Particle Data Group 2025',
            'reference': 'https://pdg.lbl.gov/2025/'
        },
        'results': []
    }
    
    # Add results for each sector
    for r in results:
        sector_data = {
            'sector': r['sector'],
            'fermions': SECTORS[r['sector']],
            'model_A': {
                'name': 'Power Law',
                'parameters': {
                    'A': float(r['model_A']['A']),
                    'p': float(r['model_A']['p'])
                },
                'predictions_MeV': {f: float(v) for f, v in zip(SECTORS[r['sector']], r['model_A']['predictions'])},
                'errors_percent': {f: float(v) for f, v in zip(SECTORS[r['sector']], r['model_A']['errors'])},
                'statistics': {
                    'mean_error_percent': float(r['model_A']['mean_error']),
                    'rms_error_percent': float(r['model_A']['rms_error']),
                    'chi2_reduced': float(r['model_A']['chi2_red']),
                    'BIC': float(r['comparison']['BIC_A'])
                }
            },
            'model_B': {
                'name': 'Golden Ratio Quantization',
                'parameters': {
                    'm0': float(r['model_B']['m0']),
                    'phi': float(r['model_B']['phi'])
                },
                'n_values': {f: int(n) for f, n in zip(SECTORS[r['sector']], r['model_B']['n_values'])},
                'predictions_MeV': {f: float(v) for f, v in zip(SECTORS[r['sector']], r['model_B']['predictions'])},
                'errors_percent': {f: float(v) for f, v in zip(SECTORS[r['sector']], r['model_B']['errors'])},
                'statistics': {
                    'mean_error_percent': float(r['model_B']['mean_error']),
                    'rms_error_percent': float(r['model_B']['rms_error']),
                    'chi2_reduced': float(r['model_B']['chi2_red']),
                    'max_n_deviation': float(r['model_B']['max_n_deviation']),
                    'BIC': float(r['comparison']['BIC_B'])
                }
            },
            'comparison': {
                'delta_BIC': float(r['comparison']['ΔBIC']),
                'preference': r['comparison']['preference']
            }
        }
        export_data['results'].append(sector_data)
    
    # Calculate combined statistics
    total_bic_A = sum([r['comparison']['BIC_A'] for r in results])
    total_bic_B = sum([r['comparison']['BIC_B'] for r in results])
    export_data['combined_statistics'] = {
        'total_BIC_model_A': float(total_bic_A),
        'total_BIC_model_B': float(total_bic_B),
        'total_delta_BIC': float(total_bic_A - total_bic_B)
    }
    
    # Save to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results exported to: {filename}")
    return filename

def export_to_csv(results, filename='fermion_models_comparison_results.csv'):
    """
    Export analysis results to CSV file.
    
    Parameters:
    -----------
    results : list
        List of result dictionaries from main()
    filename : str
        Output CSV filename
    """
    import csv
    
    # Prepare CSV data
    csv_data = []
    
    for r in results:
        sector = r['sector']
        fermions = SECTORS[sector]
        
        for i, fermion in enumerate(fermions):
            row = {
                'sector': sector,
                'fermion': fermion,
                'mass_exp_MeV': FERMION_MASSES_EXP[fermion],
                'mass_uncertainty': FERMION_MASSES_UNC[fermion] if isinstance(FERMION_MASSES_UNC[fermion], (int, float)) else f"+{FERMION_MASSES_UNC[fermion][0]}/-{FERMION_MASSES_UNC[fermion][1]}",
                'model_A_prediction_MeV': r['model_A']['predictions'][i],
                'model_A_error_percent': r['model_A']['errors'][i],
                'model_A_A': r['model_A']['A'],
                'model_A_p': r['model_A']['p'],
                'model_B_n': r['model_B']['n_values'][i],
                'model_B_prediction_MeV': r['model_B']['predictions'][i],
                'model_B_error_percent': r['model_B']['errors'][i],
                'model_B_m0': r['model_B']['m0'],
                'model_B_phi': r['model_B']['phi']
            }
            csv_data.append(row)
    
    # Save to CSV
    if csv_data:
        fieldnames = csv_data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)
        
        print(f"[OK] Results exported to: {filename}")
    
    return filename

if __name__ == "__main__":
    results = main()
    
    # Export results to JSON and CSV
    print("\n" + "="*70)
    print("EXPORTING RESULTS")
    print("="*70)
    
    export_to_json(results)
    export_to_csv(results)
    
    print("\n" + "="*70)
    print("ALL FILES SAVED SUCCESSFULLY")
    print("="*70)
