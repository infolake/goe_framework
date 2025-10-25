#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PHIQ DESIGN OPTIMIZATION (PDO)                            ║
║                         Chart Template System - Bars                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

Family: BMSSP (Bellman-Ford Multi-Source Shortest Path)
Product Line: Tiers (3 produtos principais)

Chart 04 Bars: SSSP CPU Time Across RMAT Scales (32 Threads) - Bar Chart Version
Comparison: BMSSP CPU Performance vs Analysis vs Galois SSSP

PDO Color Theme: Clean bars without borders, sober professional style

Author: PHIQ PDO Team
Date: 22 October 2025
Version: 1.0.0 - Bar Chart Template
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# DADOS DO GRÁFICO - BMSSP Triunvirato vs Galois
# ============================================================================
scales = ['S18', 'S19', 'S20']
bmssp_cpu_performance = [67, 142, 359]    # CPU Performance (mais rápido)
bmssp_cpu_analysis = [108, 215, 446]      # CPU Analysis (mais completo)
bmssp_gpu_cuda = [30, 60, 120]            # GPU CUDA (production-ready)
galois_sssp = [180, 254, 265]             # Galois SSSP (competitor reference)
gunrock = [200, 280, 300]                 # Gunrock (competitor)

# ============================================================================
# PDO PHIQ DESIGN OPTIMIZATION - COLOR PALETTE
# ============================================================================
# BMSSP Family Colors (Gold Spectrum)
COLOR_PERFORMANCE = '#ffde4b'  # Vibrant Yellow - Performance Product
COLOR_ANALYSIS = '#ffc400'     # Dark Gold - Analysis Product
COLOR_GPU_PROD = '#00c9c9'     # Light Cyan - GPU Production

# Competitor Colors (Gray Spectrum)
COLOR_GALOIS = '#6b7380'       # Dark Gray - Galois SSSP
COLOR_GUNROCK = '#8b919c'      # Light Gray - Gunrock

# UI Theme Colors
UI_BACKGROUND = '#ffffff'      # Pure white background
UI_GRID = '#e5ecf6'            # Light blue-gray grid
UI_TITLE = '#586172'           # Dark blue-gray title (darkest)
UI_LEGEND = '#5a6470'          # Mid blue-gray legend text (mid)
UI_TICKS = '#6b7380'           # Light blue-gray axis labels (lightest)

# ============================================================================
# CONFIGURAÇÃO DA FIGURA (800x500px)
# ============================================================================
fig, ax = plt.subplots(figsize=(8, 5), dpi=100)

# ============================================================================
# PLOTAR BARRAS AGRUPADAS - BMSSP Triunvirato + Competitors
# ============================================================================

x = np.arange(len(scales))  # Posições das barras
width = 0.15  # Largura de cada barra

# Barras sem borda (edgecolor='none', linewidth=0)
bars1 = ax.bar(x - 2*width, bmssp_cpu_performance, width, 
               label='BMSSP CPU P', 
               color=COLOR_PERFORMANCE, 
               edgecolor='none',
               zorder=3)

bars2 = ax.bar(x - width, bmssp_cpu_analysis, width, 
               label='BMSSP CPU A', 
               color=COLOR_ANALYSIS, 
               edgecolor='none',
               zorder=3)

bars3 = ax.bar(x, bmssp_gpu_cuda, width, 
               label='BMSSP GPU CUDA', 
               color=COLOR_GPU_PROD, 
               edgecolor='none',
               zorder=3)

bars4 = ax.bar(x + width, galois_sssp, width, 
               label='Galois SSSP', 
               color=COLOR_GALOIS, 
               edgecolor='none',
               zorder=3)

bars5 = ax.bar(x + 2*width, gunrock, width, 
               label='Gunrock', 
               color=COLOR_GUNROCK, 
               edgecolor='none',
               zorder=3)

# ============================================================================
# CONFIGURAÇÃO DE BACKGROUND E GRID
# ============================================================================

# Background branco limpo
fig.patch.set_facecolor(UI_BACKGROUND)
ax.set_facecolor(UI_BACKGROUND)

# Grid horizontal apenas (mais limpo para barras)
ax.grid(True, 
        axis='y',                    # Apenas grid horizontal
        linestyle='-', 
        linewidth=1, 
        color=UI_GRID, 
        alpha=1.0, 
        zorder=0)
ax.set_axisbelow(True)

# ============================================================================
# TÍTULO E LABELS
# ============================================================================

ax.set_title('SSSP CPU Time Across RMAT Scales (32T)', 
             fontsize=20, 
             fontweight='normal', 
             color=UI_TITLE, 
             pad=40,
             fontfamily='Arial')

ax.set_xlabel('Graph Scale', 
              fontsize=12, 
              color=UI_TITLE, 
              fontfamily='Arial', 
              labelpad=10)

ax.set_ylabel('Time (ms)', 
              fontsize=12, 
              color=UI_TITLE, 
              fontfamily='Arial', 
              labelpad=10)

# ============================================================================
# CONFIGURAÇÃO DOS EIXOS
# ============================================================================

# Configurar eixo X
ax.set_xticks(x)
ax.set_xticklabels(scales)

# Configurar limites e ticks do eixo Y
ax.set_ylim(0, 500)
ax.set_yticks(np.arange(0, 501, 50))

# Configurar ticks com cor do tema
ax.tick_params(axis='both', 
               which='major', 
               labelsize=10, 
               colors=UI_TICKS, 
               length=6, 
               width=1, 
               direction='out')

# ============================================================================
# LEGENDA HORIZONTAL
# ============================================================================

legend = ax.legend(
    loc='upper center', 
    bbox_to_anchor=(0.5, 1.15), 
    frameon=True, 
    fancybox=False, 
    shadow=False, 
    fontsize=9, 
    ncol=5, 
    framealpha=0.8, 
    edgecolor=UI_GRID, 
    borderpad=0.8, 
    handlelength=2.5, 
    handletextpad=0.5, 
    columnspacing=1.5)

legend.get_frame().set_facecolor(UI_BACKGROUND)
legend.get_frame().set_linewidth(1)

for text in legend.get_texts():
    text.set_color(UI_LEGEND)

# ============================================================================
# BORDAS DO GRÁFICO
# ============================================================================

# Bordas limpas (sem spines no topo e direita para estilo moderno)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(UI_GRID)
ax.spines['left'].set_linewidth(1)
ax.spines['bottom'].set_color(UI_GRID)
ax.spines['bottom'].set_linewidth(1)

# ============================================================================
# AJUSTAR MARGENS E EXPORTAR
# ============================================================================

fig.subplots_adjust(left=0.10, right=0.96, top=0.82, bottom=0.12)
fig.set_size_inches(8, 5)
output_filename = 'pdo_bmssp_chart04_bars.png'

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
