#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PHIQ DESIGN OPTIMIZATION (PDO)                            ║
║                         Chart Template System                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

Family: BMSSP (Bellman-Ford Multi-Source Shortest Path)
Product Line: Tiers (3 produtos principais)

Chart 04: SSSP CPU Time Across RMAT Scales (32 Threads)
Comparison: BMSSP CPU Performance vs Analysis vs Galois SSSP

PDO Color Theme:
┌────────────────────────────────────────────────────────────────────────────┐
│ BMSSP Products (Gold Spectrum)                                             │
│  • CPU Performance: #ffde4bff (Vibrant Yellow) - O mais rápido na CPU       │
│  • CPU Analysis:    #ffc400ff (Dark Gold) - O mais completo para análise    │
│  • GPU Production:  #00c9c9ff (Light Cyan) - GPU production-ready           │
│                                                                             │
│ Competitors (Gray Spectrum)                                                │
│  • Galois:          #9da8bb (Dark Gray)                                    │
│  • Gunrock:         #70a3ac (Light Gray)                                   │
│                                                                             │
│ UI Elements                                                                 │
│  • Background:      #ffffff (Pure White)                                   │
│  • Grid:            #e5ecf6 (Light Blue-Gray)                              │
│  • Title:           #586172 (Dark Blue-Gray) - 20pt Arial                 │
│  • Legend Text:     #5a6470 (Mid Blue-Gray) - 10pt Arial                  │
│  • Axis Ticks:      #6b7380 (Light Blue-Gray) - 10pt Arial                │
└────────────────────────────────────────────────────────────────────────────┘

Author: PHIQ PDO Team
Date: 19 October 2025
Version: 1.0.0 - Canonical Template
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# DADOS DO GRÁFICO - BMSSP Triunvirato vs Galois
# ============================================================================
scales = ['S18', 'S19', 'S20']
bmssp_cpu_performance = [67, 142, 359]    # CPU Performance (mais rápido - 100% coverage)
bmssp_cpu_analysis = [108, 215, 446]      # CPU Analysis (mais completo - 100% coverage)
bmssp_gpu_cuda = [30, 60, 120]            # GPU CUDA (production-ready)
galois_sssp = [180, 254, 265]             # Galois SSSP (competitor reference)
gunrock = [200, 280, 300]                 # Gunrock (competitor)

# ============================================================================
# PDO PHIQ DESIGN OPTIMIZATION - COLOR PALETTE
# ============================================================================
# BMSSP Family Colors (Gold Spectrum)
COLOR_PERFORMANCE = '#ffde4bff'  # Vibrant Yellow - Performance Product (mais rápido)
COLOR_ANALYSIS = '#ffc400ff'     # Dark Gold - Analysis Product (mais completo)
COLOR_GPU_PROD = '#00c9c9ff'     # Light Cyan - GPU Production

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
# CONFIGURAÇÃO DA FIGURA (800x500px para validação rápida)
# ============================================================================
fig, ax = plt.subplots(figsize=(8, 5), dpi=100)

# ============================================================================
# PLOTAR LINHAS - BMSSP Triunvirato (3 produtos) + Competitors
# ============================================================================

# Produto 1: BMSSP CPU Performance (O Mais Rápido)
ax.plot(scales, bmssp_cpu_performance, 
        color=COLOR_PERFORMANCE,           # Cor: Vibrant Yellow (#ffde4bff)
        linewidth=2,                       # Espessura da linha: 2px
        marker='o',                        # Marcador: círculo
        markersize=6,                      # Tamanho do marcador: 6px
        markerfacecolor=COLOR_PERFORMANCE, # Cor de preenchimento do marcador
        markeredgewidth=0,                 # Sem borda no marcador
        label='BMSSP CPU P',               # Nome na legenda
        zorder=3)                          # Camada 3 (acima do grid)

# Produto 2: BMSSP CPU Analysis (O Mais Completo)
ax.plot(scales, bmssp_cpu_analysis, 
        color=COLOR_ANALYSIS,              # Cor: Dark Gold (#ffc400ff)
        linewidth=2,                       # Espessura da linha: 2px
        marker='o',                        # Marcador: círculo
        markersize=6,                      # Tamanho do marcador: 6px
        markerfacecolor=COLOR_ANALYSIS,    # Cor de preenchimento do marcador
        markeredgewidth=0,                 # Sem borda no marcador
        label='BMSSP CPU A',               # Nome na legenda
        zorder=3)                          # Camada 3 (acima do grid)

# Produto 3: BMSSP GPU CUDA (Production-Ready)
ax.plot(scales, bmssp_gpu_cuda, 
        color=COLOR_GPU_PROD,              # Cor: Light Cyan (#00c9c9ff)
        linewidth=2,                       # Espessura da linha: 2px
        marker='o',                        # Marcador: círculo
        markersize=6,                      # Tamanho do marcador: 6px
        markerfacecolor=COLOR_GPU_PROD,    # Cor de preenchimento do marcador
        markeredgewidth=0,                 # Sem borda no marcador
        label='BMSSP GPU CUDA',           # Nome na legenda
        zorder=3)                          # Camada 3 (acima do grid)

# Competitor: Galois SSSP
ax.plot(scales, galois_sssp, 
        color=COLOR_GALOIS,                # Cor: Dark Gray (#6b7380)
        linewidth=2,                       # Espessura da linha: 2px
        marker='o',                        # Marcador: círculo
        markersize=6,                      # Tamanho do marcador: 6px
        markerfacecolor=COLOR_GALOIS,      # Cor de preenchimento do marcador
        markeredgewidth=0,                 # Sem borda no marcador
        label='Galois SSSP',               # Nome na legenda
        zorder=3)                          # Camada 3 (acima do grid)

# Competitor: Gunrock
ax.plot(scales, gunrock, 
        color=COLOR_GUNROCK,               # Cor: Light Gray (#8b919c)
        linewidth=2,                       # Espessura da linha: 2px
        marker='o',                        # Marcador: círculo
        markersize=6,                      # Tamanho do marcador: 6px
        markerfacecolor=COLOR_GUNROCK,     # Cor de preenchimento do marcador
        markeredgewidth=0,                 # Sem borda no marcador
        label='Gunrock',                   # Nome na legenda
        zorder=3)                          # Camada 3 (acima do grid)

# ============================================================================
# CONFIGURAÇÃO DE BACKGROUND E GRID
# ============================================================================

# Background branco limpo
fig.patch.set_facecolor(UI_BACKGROUND)  # Cor de fundo da figura
ax.set_facecolor(UI_BACKGROUND)         # Cor de fundo da área do gráfico

# Grid com cor e estilo do tema profissional PDO
ax.grid(True,                        # Ativar grid
        linestyle='-',               # Estilo da linha: sólida
        linewidth=1,                 # Espessura das linhas do grid
        color=UI_GRID,               # Cor do grid: azul-cinza claro (#e5ecf6)
        alpha=1.0,                   # Opacidade: 100% (totalmente visível)
        zorder=0)                    # Ordem de empilhamento (0 = atrás de tudo)
ax.set_axisbelow(True)               # Colocar grid atrás dos dados

# ============================================================================
# TÍTULO E LABELS (Hierarquia de cores: Title > Legend > Ticks)
# ============================================================================

# Título principal (20pt, cor mais escura #586172)
ax.set_title('SSSP CPU Time Across RMAT Scales (32T)', 
             fontsize=20,                # Tamanho da fonte: 20pt
             fontweight='normal',        # Peso da fonte: normal (não negrito)
             color=UI_TITLE,             # Cor: Dark Blue-Gray (#586172 - darkest)
             pad=40,                     # Espaçamento superior: 40px (ajustado -10px)
             fontfamily='Arial')         # Fonte: Arial

# Label do eixo X (12pt, mesma cor do título)
ax.set_xlabel('Graph Scale', 
              fontsize=12,               # Tamanho da fonte: 12pt
              color=UI_TITLE,            # Cor: Dark Blue-Gray (#586172)
              fontfamily='Arial',        # Fonte: Arial
              labelpad=10)               # Espaçamento do eixo: 10px

# Label do eixo Y (12pt, mesma cor do título)
ax.set_ylabel('Time (ms)', 
              fontsize=12,               # Tamanho da fonte: 12pt
              color=UI_TITLE,            # Cor: Dark Blue-Gray (#586172)
              fontfamily='Arial',        # Fonte: Arial
              labelpad=10)               # Espaçamento do eixo: 10px

# ============================================================================
# CONFIGURAÇÃO DOS EIXOS
# ============================================================================

# Configurar limites do eixo Y
ax.set_ylim(0, 500)  # Limite Y: 0 a 500ms

# Configurar ticks do eixo Y com divisões de 50 em 50
ax.set_yticks(np.arange(0, 501, 50))  # Ticks: 0, 50, 100, ..., 500

# Configurar ticks com cor do tema (10pt, cor mais clara #6b7380)
ax.tick_params(axis='both',           # Aplica para ambos os eixos (X e Y)
               which='major',         # Aplica apenas para ticks principais
               labelsize=10,          # Tamanho da fonte: 10pt
               colors=UI_TICKS,       # Cor: Light Blue-Gray (#6b7380 - lightest)
               length=6,              # Comprimento das linhas de marcação: 6px
               width=1,               # Espessura das linhas de marcação: 1px
               direction='out')       # Direção: para fora do gráfico

# ============================================================================
# LEGENDA HORIZONTAL (Cor intermediária #5a6470)
# ============================================================================

legend = ax.legend(
    loc='upper center',              # Posição: centralizada no topo
    bbox_to_anchor=(0.5, 1.15),      # Âncora: 50% horizontal, 112% vertical (subir legenda)
    frameon=True,                    # Ativar quadro ao redor da legenda
    fancybox=False,                  # Desativar estilo arredondado
    shadow=False,                    # Desativar sombra
    fontsize=9,                      # Tamanho da fonte: 9pt
    ncol=5,                          # Número de colunas: 5 (layout horizontal)
    framealpha=0.8,                  # Transparência do quadro: 80% opaco
    edgecolor=UI_GRID,               # Cor da borda: Light Blue-Gray (#e5ecf6)
    borderpad=0.8,                   # Espaçamento interno: 0.8
    handlelength=2.5,                # Comprimento das linhas/marcadores: 2.5
    handletextpad=0.5,               # Espaçamento entre marcador e texto: 0.5
    columnspacing=1.5)               # Espaçamento entre colunas: 1.5

# Configurar background da legenda
legend.get_frame().set_facecolor(UI_BACKGROUND)  # Fundo branco
legend.get_frame().set_linewidth(1)              # Espessura da borda: 1px

# Ajustar cor do texto da legenda (tom intermediário #5a6470)
for text in legend.get_texts():
    text.set_color(UI_LEGEND)  # Cor: Mid Blue-Gray (#5a6470 - mid)

# ============================================================================
# BORDAS DO GRÁFICO
# ============================================================================

# Ativar todas as bordas
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)

# Estilizar bordas
for spine in ax.spines.values():
    spine.set_color(UI_GRID)         # Cor da borda: Light Blue-Gray (#e5ecf6)
    spine.set_linewidth(1)            # Espessura: 1px

# ============================================================================
# AJUSTAR MARGENS E EXPORTAR
# ============================================================================

# Ajustar margens com valores explícitos para evitar 'achatamento' horizontal e cortes
# (tight_layout e bbox_inches='tight' podem reduzir a área de plot em algumas configurações)
# Aumentamos margens para acomodar título, legenda, labels e dados sem cortes
fig.subplots_adjust(left=0.10, right=0.96, top=0.82, bottom=0.12)

# Forçar tamanho da figura em polegadas e DPI para tentar garantir 800x500 px
fig.set_size_inches(8, 5)
output_filename = 'pdo_bmssp_chart04_cpu_time_rmat_scales.png'

# Salvar somente PNG (sem exibir) e garantir recorte de margens
plt.savefig(output_filename,
            dpi=100,
            facecolor=UI_BACKGROUND,
            edgecolor='none',
            pad_inches=0.2)

# Alguns backends e configurações de sistema podem alterar levemente os pixels finais.
# Para garantir exatamente 800x500 pixels, reabrimos a imagem com Pillow e redimensionamos
try:
        from PIL import Image
        img = Image.open(output_filename)
        # Se já estiver nas dimensões desejadas, mantemos; caso contrário, forçamos redimensionamento
        desired_size = (800, 500)
        if img.size != desired_size:
                img = img.resize(desired_size, Image.LANCZOS)
                img.save(output_filename)
        img.close()
except Exception:
        # Se Pillow não estiver disponível, continuamos com o arquivo salvo pelo matplotlib
        pass

# ============================================================================
# RELATÓRIO DE SAÍDA (minimizado para saída apenas PNG)
# ============================================================================
print(output_filename)
