# PDO Charts Gallery

**PHIQ Design Optimization (PDO) - Professional Chart Templates**

Esta pasta contém exemplos de gráficos no estilo PDO (clean, borderless, sober) gerados com Matplotlib.

---

## 📊 Gráficos Gerados

### 1. **pdo_bmssp_chart04_cpu_time_rmat_scales.png**
- **Tipo**: Line chart
- **Descrição**: SSSP CPU Time Across RMAT Scales (32T)
- **Séries**: BMSSP CPU P, BMSSP CPU A, BMSSP GPU CUDA, Galois SSSP, Gunrock
- **Script**: `00-pdo_chart_template.py`
- **Características**:
  - Linhas com marcadores circulares (sem bordas)
  - Legenda horizontal (5 colunas, 9pt)
  - Título 20pt, labels 12pt
  - Cores: dourado (#ffde4b, #ffc400), cyan (#00c9c9), grays (#6b7380, #8b919c)
  - Grid limpo (#e5ecf6)
  - 800x500 px

---

### 2. **pdo_bmssp_chart04_bars.png**
- **Tipo**: Grouped bar chart
- **Descrição**: SSSP CPU Time Across RMAT Scales (32T) - versão em barras
- **Séries**: BMSSP CPU P, BMSSP CPU A, BMSSP GPU CUDA, Galois SSSP, Gunrock
- **Script**: `01-pdo_chart_bars.py`
- **Características**:
  - Barras agrupadas sem bordas (`edgecolor='none'`)
  - Grid horizontal apenas
  - Bordas superiores e direita removidas (estilo moderno)
  - Mesma paleta de cores do line chart
  - 800x500 px

---

### 3. **pdo_mcmc_trace_distribution.png**
- **Tipo**: MCMC diagnostic (2 subplots)
- **Descrição**: Trace plot + Posterior distribution
- **Script**: `02-pdo_mcmc_trace.py`
- **Características**:
  - **Painel 1**: Trace plot com região de burn-in destacada
  - **Painel 2**: Histograma sem bordas + KDE + intervalo de credibilidade 95%
  - Cores: dourado (#ffc400), cyan (#00c9c9), vermelho (#ff6b6b)
  - Grid sóbrio
  - 800x500 px

---

### 4. **pdo_black_hole_stability.png**
- **Tipo**: Black hole thermodynamic analysis (2 subplots)
- **Descrição**: GR vs GoE stability comparison
- **Dados**: `proxy_pi3_results.csv` (primeiros 10 buracos negros)
- **Script**: `03-pdo_black_hole_stability.py`
- **Características**:
  - **Painel 1**: Barras comparativas de estabilidade termodinâmica
  - **Painel 2**: Heat capacity vs Mass (escala log)
  - Cores: azul petróleo (#1e5f74) GoE, vermelho (#ff6b6b) GR
  - Barras sem bordas
  - offsetText desativado para layout limpo
  - 800x500 px

---

## 🎨 Estilo PDO (Phosforescent Design Optimization)

### Paleta de Cores Padrão

#### BMSSP Family (Gold Spectrum)
- **Performance**: `#ffde4b` (Vibrant Yellow)
- **Analysis**: `#ffc400` (Dark Gold)
- **GPU Production**: `#00c9c9` (Light Cyan)

#### Competitors (Gray Spectrum)
- **Galois**: `#6b7380` (Dark Gray)
- **Gunrock**: `#8b919c` (Light Gray)

#### Black Hole Physics
- **GoE**: `#1e5f74` (Petrol Blue - stable)
- **GR**: `#ff6b6b` (Red/Pink - unstable)

#### UI Theme
- **Background**: `#ffffff` (Pure White)
- **Grid**: `#e5ecf6` (Light Blue-Gray)
- **Title**: `#586172` (Dark Blue-Gray, 20pt Arial)
- **Legend**: `#5a6470` (Mid Blue-Gray, 9pt Arial)
- **Ticks**: `#4a5568` (Dark Gray, not pure black)

---

### Características Visuais

✓ **Sem bordas** (`edgecolor='none'` em barras e histogramas)  
✓ **Bordas superiores e direita removidas** (estilo moderno)  
✓ **Grid limpo e sóbrio** (#e5ecf6)  
✓ **Fontes profissionais** (Arial, hierarquia clara)  
✓ **Marcadores sem borda** (`markeredgewidth=0`)  
✓ **Transparências controladas** (framealpha=0.8 em legendas)  
✓ **Resolução fixa** (800x500 px, DPI 100)  

---

## 📁 Arquivos da Galeria

```
PDO_CHARTS_GALLERY/
├── 00-pdo_chart_template.py              # Template principal (line chart)
├── 01-pdo_chart_bars.py                  # Variante em barras agrupadas
├── 02-pdo_mcmc_trace.py                  # MCMC trace + distribuição
├── 03-pdo_black_hole_stability.py        # Análise de buracos negros
├── pdo_bmssp_chart04_cpu_time_rmat_scales.png
├── pdo_bmssp_chart04_bars.png
├── pdo_mcmc_trace_distribution.png
├── pdo_black_hole_stability.png
├── proxy_pi3_results.csv                 # Dados de buracos negros
└── README.md                             # Este arquivo
```

---

## 🚀 Como Usar

### Executar um script:
```powershell
python 00-pdo_chart_template.py
python 01-pdo_chart_bars.py
python 02-pdo_mcmc_trace.py
python 03-pdo_black_hole_stability.py
```

### Adaptar para seus dados:
1. Copie o script de exemplo mais próximo do seu caso de uso
2. Ajuste os dados (arrays, DataFrames, CSV)
3. Personalize cores e labels conforme necessário
4. Execute e gere seu PNG 800x500px

---

## 📝 Notas Técnicas

- **Pillow redimensionamento**: Scripts incluem fallback para garantir exatamente 800x500 px
- **Margens explícitas**: Uso de `fig.subplots_adjust()` em vez de `tight_layout()` para controle preciso
- **offsetText desativado**: Em gráficos com escala científica, `ax.xaxis.offsetText.set_visible(False)` evita sobreposições
- **Compatibilidade Windows**: Caminhos absolutos, símbolos Unicode evitados quando possível

---

**Autor**: PHIQ PDO Team  
**Data**: 22 October 2025  
**Versão**: 1.0.0
