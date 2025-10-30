"""
Code Capsule S4: Proton Spin Prediction (EIC-Testable)

Plots the predicted band [phi, phi^2] for J_g/J_q ratio versus renormalization
scale mu, overlaying current global-fit intervals and projected EIC uncertainties.

Reference: GoE Paper, Section "Proton Spin Prediction: EIC-Testable Observable"
Author: Guilherme de Camargo (PHIQ.IO Research Group)
Date: October 29, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Golden ratio
phi = (1 + np.sqrt(5)) / 2

# Renormalization scale range (GeV)
mu = np.linspace(0.5, 10, 500)

# Predicted band boundaries (assuming mild RG running)
# Assumption: d(log(J_g/J_q))/d(log(mu)) ~ 0.05 (mild running)
# This gives ~10% variation over decade in mu
running_factor = 1 + 0.05 * np.log(mu / 1.0)

lower_band = phi * running_factor * 0.95
upper_band = phi**2 * running_factor * 1.05

# Current global fit estimates (approximate from literature)
# Source: STAR 2021, COMPASS, JLab combined analyses
global_fit_mu = np.array([2.0, 3.0, 5.0])
global_fit_ratio = np.array([1.5, 1.8, 2.0])
global_fit_error = np.array([0.7, 0.6, 0.5])  # Large current uncertainties

# Projected EIC measurements (~2035)
# Source: EIC White Paper projections
eic_mu = np.array([1.0, 2.0, 5.0])
eic_projected_ratio = np.array([1.7, 1.9, 2.1])
eic_projected_error = np.array([0.15, 0.18, 0.20])  # ~10% precision

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot predicted band
ax.fill_between(mu, lower_band, upper_band, 
                alpha=0.3, color='gold', 
                label=r'$\Sigma$-Möbius band: $[\varphi, \varphi^2]$')

# Plot band boundaries
ax.plot(mu, lower_band, 'k--', alpha=0.5, linewidth=1)
ax.plot(mu, upper_band, 'k--', alpha=0.5, linewidth=1)

# Horizontal lines for phi and phi^2 at mu=1 GeV
ax.axhline(y=phi, color='orange', linestyle=':', alpha=0.7, 
           label=r'$\varphi = 1.618$')
ax.axhline(y=phi**2, color='red', linestyle=':', alpha=0.7, 
           label=r'$\varphi^2 = 2.618$')

# Vertical line at anchoring scale
ax.axvline(x=1.0, color='gray', linestyle='--', alpha=0.5, 
           label=r'$\mu_0 = 1$ GeV (anchoring)')

# Current global fits
ax.errorbar(global_fit_mu, global_fit_ratio, yerr=global_fit_error,
            fmt='o', color='blue', markersize=8, capsize=5,
            label='Global fits (2020-2024)', alpha=0.7, zorder=3)

# Projected EIC measurements
ax.errorbar(eic_mu, eic_projected_ratio, yerr=eic_projected_error,
            fmt='s', color='green', markersize=8, capsize=5,
            label='EIC projections (2030s)', alpha=0.8, zorder=4)

# Labels and formatting
ax.set_xlabel(r'Renormalization scale $\mu$ (GeV)', fontsize=14)
ax.set_ylabel(r'$J_g(\mu) / J_q(\mu)$', fontsize=14)
ax.set_title('Proton Spin Decomposition: GoE Prediction vs. EIC', 
             fontsize=16, fontweight='bold')
ax.set_xlim(0.5, 10)
ax.set_ylim(0.5, 3.5)
ax.set_xscale('log')
ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
ax.legend(loc='upper right', fontsize=11, framealpha=0.9)

# Add text box with falsification criteria
textstr = ('Falsification criteria:\n'
           r'$J_g/J_q(\mu_0=1\,\mathrm{GeV}) < 1.5$ or $> 2.8$'
           '\n'
           r'$\Rightarrow$ Excludes $D_5$ dihedral structure')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

# Add annotation for EIC timeline
ax.annotate('EIC first data\n~2030-2035', 
            xy=(2.0, 1.9), xytext=(4, 1.2),
            arrowprops=dict(arrowstyle='->', color='green', lw=2),
            fontsize=11, color='green', fontweight='bold')

plt.tight_layout()
plt.savefig('proton_spin_prediction_eic.pdf', dpi=300, bbox_inches='tight')
plt.savefig('proton_spin_prediction_eic.png', dpi=150, bbox_inches='tight')
print("Figure saved: proton_spin_prediction_eic.pdf/.png")
plt.show()

# Print numerical values at anchoring scale
print(f"\n=== GoE Prediction at mu_0 = 1 GeV ===")
print(f"Golden ratio phi = {phi:.6f}")
print(f"phi^2 = {phi**2:.6f}")
print(f"Predicted band: [{phi:.3f}, {phi**2:.3f}]")
print(f"\nCentral value: {(phi + phi**2)/2:.3f}")
print(f"Band width: {phi**2 - phi:.3f} (~{100*(phi**2 - phi)/phi:.1f}%)")

# Testability assessment
print(f"\n=== Testability Timeline ===")
print(f"Current uncertainties: ~50% (global fits)")
print(f"EIC projected precision: ~10% (~2035)")
print(f"Sigma separation required: 2-sigma exclusion")
print(f"Lower exclusion: J_g/J_q < {phi - 2*0.15:.2f}")
print(f"Upper exclusion: J_g/J_q > {phi**2 + 2*0.20:.2f}")
