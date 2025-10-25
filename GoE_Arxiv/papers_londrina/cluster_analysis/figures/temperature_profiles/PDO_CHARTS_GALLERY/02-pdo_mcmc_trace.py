#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PHIQ DESIGN OPTIMIZATION (PDO)                            ║
║                    MCMC Trace Plot & Distribution                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

MCMC Diagnostic Plot: Trace plot + Posterior Distribution
Clean, borderless, professional style for Bayesian analysis visualization

Author: PHIQ PDO Team
Date: 22 October 2025
Version: 1.0.0 - MCMC Template
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# ============================================================================
# SIMULAR DADOS MCMC (exemplo: posterior de um parâmetro)
# ============================================================================
np.random.seed(42)

# Simular cadeia MCMC convergida para distribuição normal
n_samples = 5000
burnin = 500

# Trace: mix de exploração inicial + convergência
trace = []
current = 0
for i in range(n_samples):
    # Random walk Metropolis-Hastings simulado
    proposal = current + np.random.normal(0, 0.5)
    if i < burnin:
        # Fase de burn-in: mais exploração
        current = proposal
    else:
        # Fase pós-burn-in: convergido para N(2, 1)
        current = np.random.normal(2.0, 1.0)
    trace.append(current)

trace = np.array(trace)

# ============================================================================
# PDO PHIQ DESIGN OPTIMIZATION - COLOR PALETTE
# ============================================================================
COLOR_PRIMARY = '#ffc400'      # Dark Gold - linha principal
COLOR_BURNIN = '#ff6b6b'       # Red - região de burn-in
COLOR_CONVERGED = '#00c9c9'    # Cyan - região convergida
COLOR_HIST = '#6b7380'         # Gray - histograma

# UI Theme Colors
UI_BACKGROUND = '#ffffff'      # Pure white background
UI_GRID = '#e5ecf6'            # Light blue-gray grid
UI_TITLE = '#586172'           # Dark blue-gray title
UI_LEGEND = '#5a6470'          # Mid blue-gray legend text
UI_TICKS = '#6b7380'           # Light blue-gray axis labels

# ============================================================================
# CONFIGURAÇÃO DA FIGURA (800x500px) - 2 subplots
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5), dpi=100)

# ============================================================================
# SUBPLOT 1: TRACE PLOT
# ============================================================================

# Região de burn-in em vermelho claro
ax1.axvspan(0, burnin, alpha=0.15, color=COLOR_BURNIN, zorder=1)
ax1.text(burnin/2, trace.max() * 0.95, 'Burn-in', 
         fontsize=9, color=COLOR_BURNIN, ha='center', va='top',
         fontfamily='Arial')

# Trace line
ax1.plot(trace, 
         color=COLOR_PRIMARY, 
         linewidth=0.8, 
         alpha=0.7,
         zorder=3)

# Média pós-burn-in (linha horizontal)
post_burnin_mean = trace[burnin:].mean()
ax1.axhline(post_burnin_mean, 
            color=COLOR_CONVERGED, 
            linestyle='--', 
            linewidth=1.5, 
            alpha=0.8,
            label=f'Mean = {post_burnin_mean:.2f}',
            zorder=2)

ax1.set_title('MCMC Trace Plot', 
              fontsize=14, 
              fontweight='normal', 
              color=UI_TITLE, 
              pad=10,
              fontfamily='Arial')

ax1.set_xlabel('Iteration', 
               fontsize=10, 
               color=UI_TITLE, 
               fontfamily='Arial',
               labelpad=8)

ax1.set_ylabel('Parameter Value', 
               fontsize=10, 
               color=UI_TITLE, 
               fontfamily='Arial',
               labelpad=8)

# Grid e background
ax1.set_facecolor(UI_BACKGROUND)
ax1.grid(True, linestyle='-', linewidth=0.8, color=UI_GRID, alpha=1.0, zorder=0)
ax1.set_axisbelow(True)

# Bordas limpas
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color(UI_GRID)
ax1.spines['left'].set_linewidth(1)
ax1.spines['bottom'].set_color(UI_GRID)
ax1.spines['bottom'].set_linewidth(1)

# Ticks
ax1.tick_params(axis='both', labelsize=9, colors=UI_TICKS, length=5, width=1)

# Legenda
leg1 = ax1.legend(loc='upper right', fontsize=8, frameon=True, 
                  fancybox=False, framealpha=0.8, edgecolor=UI_GRID)
leg1.get_frame().set_facecolor(UI_BACKGROUND)
for text in leg1.get_texts():
    text.set_color(UI_LEGEND)

# ============================================================================
# SUBPLOT 2: POSTERIOR DISTRIBUTION (HISTOGRAM + KDE)
# ============================================================================

post_burnin_samples = trace[burnin:]

# Histograma (sem borda)
n, bins, patches = ax2.hist(post_burnin_samples, 
                             bins=40, 
                             density=True,
                             color=COLOR_HIST, 
                             alpha=0.6,
                             edgecolor='none',
                             zorder=2)

# KDE (Kernel Density Estimation)
kde = stats.gaussian_kde(post_burnin_samples)
x_range = np.linspace(post_burnin_samples.min(), post_burnin_samples.max(), 200)
ax2.plot(x_range, kde(x_range), 
         color=COLOR_PRIMARY, 
         linewidth=2.5, 
         label='KDE',
         zorder=3)

# Média e intervalos de credibilidade
mean_val = post_burnin_samples.mean()
ci_lower = np.percentile(post_burnin_samples, 2.5)
ci_upper = np.percentile(post_burnin_samples, 97.5)

ax2.axvline(mean_val, color=COLOR_CONVERGED, linestyle='--', linewidth=1.5, 
            label=f'Mean = {mean_val:.2f}', zorder=3)
ax2.axvline(ci_lower, color=UI_TICKS, linestyle=':', linewidth=1, alpha=0.7, zorder=2)
ax2.axvline(ci_upper, color=UI_TICKS, linestyle=':', linewidth=1, alpha=0.7, zorder=2)

# Texto de intervalo de credibilidade
ax2.text(mean_val, kde(x_range).max() * 0.95, 
         f'95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]',
         fontsize=8, color=UI_TICKS, ha='center', va='top',
         fontfamily='Arial')

ax2.set_title('Posterior Distribution', 
              fontsize=14, 
              fontweight='normal', 
              color=UI_TITLE, 
              pad=10,
              fontfamily='Arial')

ax2.set_xlabel('Parameter Value', 
               fontsize=10, 
               color=UI_TITLE, 
               fontfamily='Arial',
               labelpad=8)

ax2.set_ylabel('Density', 
               fontsize=10, 
               color=UI_TITLE, 
               fontfamily='Arial',
               labelpad=8)

# Grid e background
ax2.set_facecolor(UI_BACKGROUND)
ax2.grid(True, axis='y', linestyle='-', linewidth=0.8, color=UI_GRID, alpha=1.0, zorder=0)
ax2.set_axisbelow(True)

# Bordas limpas
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color(UI_GRID)
ax2.spines['left'].set_linewidth(1)
ax2.spines['bottom'].set_color(UI_GRID)
ax2.spines['bottom'].set_linewidth(1)

# Ticks
ax2.tick_params(axis='both', labelsize=9, colors=UI_TICKS, length=5, width=1)

# Legenda
leg2 = ax2.legend(loc='upper left', fontsize=8, frameon=True, 
                  fancybox=False, framealpha=0.8, edgecolor=UI_GRID)
leg2.get_frame().set_facecolor(UI_BACKGROUND)
for text in leg2.get_texts():
    text.set_color(UI_LEGEND)

# ============================================================================
# AJUSTAR MARGENS E EXPORTAR
# ============================================================================

fig.patch.set_facecolor(UI_BACKGROUND)
fig.subplots_adjust(left=0.08, right=0.98, top=0.92, bottom=0.12, wspace=0.25)
fig.set_size_inches(8, 5)
output_filename = 'pdo_mcmc_trace_distribution.png'

plt.savefig(output_filename,
            dpi=100,
            facecolor=UI_BACKGROUND,
            edgecolor='none',
            pad_inches=0.2)

# Garantir 800x500 pixels
try:
    from PIL import Image
    img = Image.open(output_filename)
    desired_size = (800, 500)
    if img.size != desired_size:
        img = img.resize(desired_size, Image.LANCZOS)
        img.save(output_filename)
    img.close()
except Exception:
    pass

print(output_filename)
