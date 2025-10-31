# File: run_production_inference.py
# Last Modified: October 30, 2025
#
# Production-grade inference script for GoE model
# Configuration optimized for publication-quality results

from goe_nuts_v4 import sample_nuts
import numpy as np
import time
import warnings
import os
from datetime import datetime

warnings.filterwarnings("ignore")

# Create results directory
os.makedirs("results", exist_ok=True)

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    'num_warmup': 1200,
    'num_samples': 15000,
    'chains': 4,
    'target_accept': 0.95,
    'max_tree_depth': 15,
    'init_step': 0.05,
    'seed': 2025,
}

# ============================================================================
# DATA PREPARATION
# ============================================================================

print("="*70)
print("GoE Inference V4 - Production Run")
print("="*70)
print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\nConfiguration:")
for key, value in CONFIG.items():
    print(f"  {key}: {value}")

print("\nLoading observational data...")

# Prepare data dictionary
# TODO: Replace with actual data file loading
data = dict(
    axis_ref=np.array([0.3, -0.7, 0.64]),
    cmb_axis=np.array([0.28, -0.73, 0.62]),
    pta_dirs=np.random.randn(24, 3),
    pta_helicity=np.random.randn(24) * 0.05,
    bh_mass=np.array([1.2e8, 8e7, 4e7, 2e8, 9e7, 6e7, 1.5e8, 7e7, 5e7, 1.1e8]),
    bh_z=np.array([8.5, 9.1, 10.2, 8.9, 9.7, 11.0, 10.5, 9.3, 9.8, 10.7]),
    fil_dirs=np.random.randn(12, 3),
)

# Normalize vectors
data["axis_ref"] = data["axis_ref"] / np.linalg.norm(data["axis_ref"])
data["cmb_axis"] = data["cmb_axis"] / np.linalg.norm(data["cmb_axis"])
data["pta_dirs"] = data["pta_dirs"] / np.linalg.norm(data["pta_dirs"], axis=1, keepdims=True)
data["fil_dirs"] = data["fil_dirs"] / np.linalg.norm(data["fil_dirs"], axis=1, keepdims=True)

print("Data prepared. Starting inference...")
print("="*70)

# ============================================================================
# INFERENCE
# ============================================================================

start_time = time.time()

chains, logps = sample_nuts(
    data=data,
    num_warmup=CONFIG['num_warmup'],
    num_samples=CONFIG['num_samples'],
    chains=CONFIG['chains'],
    target_accept=CONFIG['target_accept'],
    max_tree_depth=CONFIG['max_tree_depth'],
    init_step=CONFIG['init_step'],
    seed=CONFIG['seed'],
)

elapsed = time.time() - start_time

# ============================================================================
# RESULTS SUMMARY
# ============================================================================

print("\n" + "="*70)
print("INFERENCE COMPLETE")
print("="*70)
print(f"Total time: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

print(f"\nResults:")
print(f"  Chains shape: {chains.shape}")
print(f"  Logps shape: {logps.shape}")

print(f"\nGlobal statistics:")
print(f"  Logp mean: {np.mean(logps):.2f}")
print(f"  Logp std: {np.std(logps):.2f}")
print(f"  Logp min: {np.min(logps):.2f}")
print(f"  Logp max: {np.max(logps):.2f}")

print(f"\nPer-chain statistics:")
param_names = ['H_sigma', 'rho_crit_NET', 'a_min', 'M_seed', 'f_NET']

for i in range(CONFIG['chains']):
    print(f"\n  Chain {i+1}:")
    print(f"    Logp: mean={np.mean(logps[i]):.2f}, std={np.std(logps[i]):.4f}, "
          f"range=[{np.min(logps[i]):.2f}, {np.max(logps[i]):.2f}]")
    
    if np.std(logps[i]) > 1.0:
        status = "EXCELLENT"
    elif np.std(logps[i]) > 0.1:
        status = "GOOD"
    elif np.std(logps[i]) > 0:
        status = "LOW"
    else:
        status = "STUCK"
    print(f"    Status: {status}")

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("\n" + "="*70)
print("Saving results...")

output_prefix = "results/v4_production"
np.save(f"{output_prefix}_chains.npy", chains)
np.save(f"{output_prefix}_logps.npy", logps)

# Save configuration
import json
with open(f"{output_prefix}_config.json", 'w') as f:
    config_save = CONFIG.copy()
    config_save['elapsed_seconds'] = elapsed
    config_save['timestamp'] = datetime.now().isoformat()
    json.dump(config_save, f, indent=2)

print(f"Results saved:")
print(f"  {output_prefix}_chains.npy")
print(f"  {output_prefix}_logps.npy")
print(f"  {output_prefix}_config.json")

print("\n" + "="*70)
print("Next steps:")
print("  1. Run diagnostics: python goe_diagnostics_v4.py")
print("  2. Generate visualizations: python goe_visualize_v4.py")
print("  3. Extract posterior summaries for paper")
print("="*70)

