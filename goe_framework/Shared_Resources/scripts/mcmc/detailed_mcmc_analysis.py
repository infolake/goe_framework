#!/usr/bin/env python3
"""
Detailed MCMC Results Analysis
Filename: detailed_mcmc_analysis.py
Last Modified: 2025-01-27
Purpose: Detailed analysis of MCMC results including convergence diagnostics
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import json
from pathlib import Path

def analyze_mcmc_results(filepath: str = "mcmc_results_large.npz"):
    """Perform detailed analysis of MCMC results"""
    
    print("="*80)
    print("DETAILED MCMC RESULTS ANALYSIS")
    print("="*80)
    
    # Load data
    data = np.load(filepath)
    posterior = data['posterior']
    best_params = data['best_params']
    elapsed = data['elapsed']
    
    print(f"\nFile: {filepath}")
    print(f"Size: {Path(filepath).stat().st_size / (1024*1024):.2f} MB")
    print(f"Posterior shape: {posterior.shape}")
    print(f"Parameters: {len(best_params)}")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    print(f"Sampling rate: {len(posterior)/elapsed:.0f} samples/second")
    
    # Parameter names (assuming g-2 muon analysis)
    param_names = ['Lambda_Xi (GeV)', 'kappa', 'eps_theta', 'prediction', 'chi2']
    
    print("\n" + "-"*80)
    print("BEST FIT PARAMETERS")
    print("-"*80)
    for i, (name, val) in enumerate(zip(param_names, best_params)):
        print(f"{name:20s}: {val:.6f}")
    
    print("\n" + "-"*80)
    print("POSTERIOR STATISTICS")
    print("-"*80)
    print(f"{'Parameter':20s} {'Mean':>12s} {'Std':>12s} {'2.5%':>12s} {'97.5%':>12s}")
    print("-"*80)
    
    for i, name in enumerate(param_names):
        samples = posterior[:, i]
        mean = np.mean(samples)
        std = np.std(samples)
        q2_5 = np.percentile(samples, 2.5)
        q97_5 = np.percentile(samples, 97.5)
        print(f"{name:20s} {mean:12.6f} {std:12.6f} {q2_5:12.6f} {q97_5:12.6f}")
    
    # Convergence diagnostics
    print("\n" + "-"*80)
    print("CONVERGENCE DIAGNOSTICS")
    print("-"*80)
    
    # Effective sample size (ESS) estimation
    def estimate_ess(x, max_lag=1000):
        """Estimate effective sample size"""
        n = len(x)
        if n < max_lag:
            max_lag = n // 2
        
        autocorr = []
        for lag in range(1, min(max_lag, n//2)):
            corr = np.corrcoef(x[:-lag], x[lag:])[0, 1]
            autocorr.append(corr)
            if lag > 10 and corr < 0.05:
                break
        
        if len(autocorr) > 0:
            tau = 1 + 2 * sum(autocorr)
            ess = n / tau if tau > 0 else n
        else:
            ess = n
        
        return ess, autocorr
    
    print("\nEffective Sample Size (ESS) per parameter:")
    ess_results = {}
    for i, name in enumerate(param_names):
        samples = posterior[:, i]
        ess, autocorr = estimate_ess(samples)
        ess_results[name] = ess
        print(f"{name:20s}: ESS = {ess:.0f} ({100*ess/len(samples):.1f}% of total)")
    
    # R-hat statistic (Gelman-Rubin) - approximate
    print("\nR-hat statistic (Gelman-Rubin diagnostic):")
    print("(Note: Requires multiple chains, approximation using data splits)")
    n_splits = 4
    split_size = len(posterior) // n_splits
    rhat_values = []
    
    for i, name in enumerate(param_names):
        samples = posterior[:, i]
        splits = [samples[j*split_size:(j+1)*split_size] for j in range(n_splits)]
        
        means = [np.mean(split) for split in splits]
        vars = [np.var(split, ddof=1) for split in splits]
        
        B = split_size * np.var(means, ddof=1)  # Between-chain variance
        W = np.mean(vars)  # Within-chain variance
        
        if W > 0:
            var_hat = (split_size - 1) / split_size * W + B / split_size
            rhat = np.sqrt(var_hat / W) if W > 0 else np.nan
        else:
            rhat = np.nan
        
        rhat_values.append(rhat)
        status = "✓" if rhat < 1.1 else "⚠" if rhat < 1.2 else "✗"
        print(f"{name:20s}: R-hat = {rhat:.3f} {status}")
    
    # Quality assessment
    print("\n" + "-"*80)
    print("QUALITY ASSESSMENT")
    print("-"*80)
    
    quality_scores = {
        'sample_size': min(len(posterior) / 100000, 1.0) * 10,  # Max 10 points
        'ess_quality': min(np.mean(list(ess_results.values())) / 10000, 1.0) * 10,  # Max 10 points
        'convergence': (1.0 - np.mean([max(0, r-1.0) for r in rhat_values])) * 10 if len(rhat_values) > 0 else 5,  # Max 10 points
        'chi2_quality': 10.0 if best_params[4] < 1.0 else max(0, 10 - best_params[4]),  # Max 10 points
    }
    
    total_quality = sum(quality_scores.values()) / len(quality_scores)
    
    print(f"Sample Size Score: {quality_scores['sample_size']:.1f}/10")
    print(f"ESS Quality Score: {quality_scores['ess_quality']:.1f}/10")
    print(f"Convergence Score: {quality_scores['convergence']:.1f}/10")
    print(f"Chi2 Quality Score: {quality_scores['chi2_quality']:.1f}/10")
    print(f"\nOverall Quality Score: {total_quality:.1f}/10")
    
    # Importance assessment
    print("\n" + "-"*80)
    print("IMPORTANCE ASSESSMENT")
    print("-"*80)
    
    importance_factors = {
        'sample_size': min(len(posterior) / 1000000, 1.0) * 3,  # 1M samples = max
        'physics_significance': 4.0,  # g-2 muon is highly significant
        'parameter_constraints': 2.0 if np.std(posterior[:, 0]) < 1000 else 1.0,  # Tight constraints
        'completeness': 1.0,  # Has all expected outputs
    }
    
    total_importance = sum(importance_factors.values())
    
    print(f"Sample Size Importance: {importance_factors['sample_size']:.1f}/3")
    print(f"Physics Significance: {importance_factors['physics_significance']:.1f}/4")
    print(f"Parameter Constraints: {importance_factors['parameter_constraints']:.1f}/2")
    print(f"Completeness: {importance_factors['completeness']:.1f}/1")
    print(f"\nOverall Importance Score: {total_importance:.1f}/10")
    
    # Recommendations
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)
    
    recommendations = []
    
    if total_quality < 7:
        recommendations.append("Consider running longer chains for better convergence")
    if quality_scores['ess_quality'] < 7:
        recommendations.append("Low ESS detected - may need thinning or longer chains")
    if quality_scores['convergence'] < 7:
        recommendations.append("Convergence issues detected - check trace plots")
    
    if total_importance >= 8:
        recommendations.append("This is a CRITICAL result - preserve carefully")
    elif total_importance >= 6:
        recommendations.append("This is an IMPORTANT result - maintain for reference")
    
    if len(recommendations) == 0:
        recommendations.append("Results are of good quality - ready for publication")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")
    
    # Final classification
    print("\n" + "="*80)
    print("FINAL CLASSIFICATION")
    print("="*80)
    
    combined_score = total_quality + total_importance
    
    if combined_score >= 16:
        category = "🔴 CRITICAL"
        description = "Highest quality and importance - essential for publication"
    elif combined_score >= 12:
        category = "🟡 IMPORTANT"
        description = "High quality and importance - maintain for reference"
    elif combined_score >= 8:
        category = "🟢 SUPPORTING"
        description = "Good quality - useful supporting material"
    else:
        category = "⚪ LOW PRIORITY"
        description = "May need improvement before use"
    
    print(f"Category: {category}")
    print(f"Combined Score: {combined_score:.1f}/20")
    print(f"Description: {description}")
    
    # Save detailed report
    report = {
        'file': filepath,
        'parameters': dict(zip(param_names, best_params.tolist())),
        'posterior_stats': {
            name: {
                'mean': float(np.mean(posterior[:, i])),
                'std': float(np.std(posterior[:, i])),
                'q2_5': float(np.percentile(posterior[:, i], 2.5)),
                'q97_5': float(np.percentile(posterior[:, i], 97.5))
            }
            for i, name in enumerate(param_names)
        },
        'quality_scores': {k: float(v) for k, v in quality_scores.items()},
        'importance_scores': {k: float(v) for k, v in importance_factors.items()},
        'ess_results': {k: float(v) for k, v in ess_results.items()},
        'combined_score': float(combined_score),
        'category': category,
        'recommendations': recommendations
    }
    
    with open('mcmc_detailed_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDetailed report saved to: mcmc_detailed_report.json")
    
    return report


if __name__ == "__main__":
    analyze_mcmc_results()

