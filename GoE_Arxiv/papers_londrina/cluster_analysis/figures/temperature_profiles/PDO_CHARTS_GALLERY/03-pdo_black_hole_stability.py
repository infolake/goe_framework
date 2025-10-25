#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PHIQ DESIGN OPTIMIZATION (PDO)                            ║
║              Proxy Pi3: Black Hole Thermodynamic Stability                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Black Hole Analysis: GR vs GoE Thermodynamic Stability
Data: First 10 Black Holes from proxy_pi3_results.csv

Author: PHIQ PDO Team
Date: 22 October 2025
Version: 1.0.0 - Black Hole Physics Template
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import LogFormatterSciNotation

# ============================================================================
# CARREGAR DADOS DO CSV
# ============================================================================
csv_path = 'd:/INFOLAKE/0-phosforescent/elastic-kv-cache/cores-protected/PHIQ_IO_GOE_NUCLEUS/phiq-io-elastic-kv-cache/src/evolution_engine_english/black_hole_validation/proxy_pi3_results.csv'

df = pd.read_csv(csv_path)

# Selecionar primeiros 10 buracos negros
df_10 = df.head(10).copy()

# Preparar labels (abreviar nomes longos)
labels = []
for name in df_10['BH']:
    if len(name) > 20:
        labels.append(name[:17] + '...')
    else:
        labels.append(name)

# Extrair dados
mass_kg = df_10['Mass_kg'].values
stable_gr = df_10['Stable_GR'].astype(int).values  # False=0, True=1
stable_goe = df_10['Stable_GoE'].astype(int).values
heat_cap_gr = df_10['C_std'].values
heat_cap_goe = df_10['C_GoE'].values

# ============================================================================
# PDO PHIQ DESIGN OPTIMIZATION - COLOR PALETTE
# ============================================================================
COLOR_GR = '#ff6b6b'           # Red/Pink - GR (unstable)
COLOR_GOE = '#1e5f74'          # Petrol Blue - GoE (stable)
COLOR_MASS = '#6b7380'         # Gray - Mass reference

# UI Theme Colors
UI_BACKGROUND = '#ffffff'      # Pure white background
UI_GRID = '#e5ecf6'            # Light blue-gray grid
UI_TITLE = '#586172'           # Dark blue-gray title
UI_LEGEND = '#5a6470'          # Mid blue-gray legend text
UI_TICKS = '#4a5568'           # Dark gray axis labels (not pure black)

# ============================================================================
# CONFIGURAÇÃO DA FIGURA (800x500px) - 2 subplots
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5), dpi=100)

# ============================================================================
# SUBPLOT 1: THERMODYNAMIC STABILITY
# ============================================================================

x = np.arange(len(labels))
width = 0.35

# Barras sem borda
bars1 = ax1.bar(x - width/2, stable_gr, width, 
                label='GR', 
                color=COLOR_GR, 
                edgecolor='none',
                zorder=3)

bars2 = ax1.bar(x + width/2, stable_goe, width, 
                label='GoE', 
                color=COLOR_GOE, 
                edgecolor='none',
                zorder=3)

ax1.set_title('Thermodynamic Stability (First 10 BHs)', 
              fontsize=13, 
              fontweight='normal', 
              color=UI_TITLE, 
              pad=10,
              fontfamily='Arial')

ax1.set_xlabel('Black Hole', 
               fontsize=9, 
               color=UI_TITLE, 
               fontfamily='Arial',
               labelpad=8)

ax1.set_ylabel('Stable? (1=Yes, 0=No)', 
               fontsize=9, 
               color=UI_TITLE, 
               fontfamily='Arial',
               labelpad=8)

ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=45, ha='right', fontsize=7)
ax1.set_ylim(0, 1.2)
ax1.set_yticks([0, 1])
ax1.set_yticklabels(['Unstable', 'Stable'])

# Grid e background
ax1.set_facecolor(UI_BACKGROUND)
ax1.grid(True, axis='y', linestyle='-', linewidth=0.8, color=UI_GRID, alpha=1.0, zorder=0)
ax1.set_axisbelow(True)

# Bordas limpas
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color(UI_GRID)
ax1.spines['left'].set_linewidth(1)
ax1.spines['bottom'].set_color(UI_GRID)
ax1.spines['bottom'].set_linewidth(1)

# Ticks
ax1.tick_params(axis='both', labelsize=8, colors=UI_TICKS, length=5, width=1)

# Legenda
leg1 = ax1.legend(loc='upper right', fontsize=8, frameon=True, 
                  fancybox=False, framealpha=0.8, edgecolor=UI_GRID)
leg1.get_frame().set_facecolor(UI_BACKGROUND)
for text in leg1.get_texts():
    text.set_color(UI_LEGEND)

# ============================================================================
# SUBPLOT 2: HEAT CAPACITY VS MASS
# ============================================================================

# Plotar linhas com marcadores
ax2.plot(mass_kg, heat_cap_gr, 
         color=COLOR_GR, 
         linewidth=2, 
         marker='s',
         markersize=5,
         markerfacecolor=COLOR_GR,
         markeredgewidth=0,
         label='GR',
         zorder=3)

ax2.plot(mass_kg, heat_cap_goe, 
         color=COLOR_GOE, 
         linewidth=2, 
         marker='o',
         markersize=5,
         markerfacecolor=COLOR_GOE,
         markeredgewidth=0,
         label='GoE',
         zorder=3)

# Linha de referência em zero
ax2.axhline(0, color=UI_TICKS, linestyle='--', linewidth=1, alpha=0.5, zorder=2)

ax2.set_title('Heat Capacity vs Mass', 
              fontsize=13, 
              fontweight='normal', 
              color=UI_TITLE, 
              pad=10,
              fontfamily='Arial')

ax2.set_xlabel('Mass (Msun)', 
               fontsize=9, 
               color=UI_TITLE, 
               fontfamily='Arial',
               labelpad=8)

ax2.set_ylabel('Heat Capacity', 
               fontsize=9, 
               color=UI_TITLE, 
               fontfamily='Arial',
               labelpad=8)

# Escala logarítmica no eixo X para melhor visualização
ax2.set_xscale('log')

# Grid e background
ax2.set_facecolor(UI_BACKGROUND)
ax2.grid(True, linestyle='-', linewidth=0.8, color=UI_GRID, alpha=1.0, zorder=0)
ax2.set_axisbelow(True)

# Bordas limpas
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color(UI_GRID)
ax2.spines['left'].set_linewidth(1)
ax2.spines['bottom'].set_color(UI_GRID)
ax2.spines['bottom'].set_linewidth(1)

# Ticks
ax2.tick_params(axis='both', labelsize=8, colors=UI_TICKS, length=5, width=1)
ax2.tick_params(axis='x', labelsize=7)  # Reduzir ainda mais fonte do eixo X para evitar sobreposição

# Desativar o offsetText automático que aparece no topo (2×10⁴¹, etc)
ax2.xaxis.offsetText.set_visible(False)

# Legenda
leg2 = ax2.legend(loc='lower right', fontsize=8, frameon=True, 
                  fancybox=False, framealpha=0.8, edgecolor=UI_GRID)
leg2.get_frame().set_facecolor(UI_BACKGROUND)
for text in leg2.get_texts():
    text.set_color(UI_LEGEND)

# ============================================================================
# AJUSTAR MARGENS E EXPORTAR
# ============================================================================

fig.patch.set_facecolor(UI_BACKGROUND)
fig.subplots_adjust(left=0.08, right=0.98, top=0.92, bottom=0.22, wspace=0.30)
fig.set_size_inches(8, 5)
output_filename = 'pdo_black_hole_stability.png'

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
