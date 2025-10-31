# GPU-Accelerated Statistical Tests - Quick Start

## For RTX 4090 / RunPod

**One-liner setup and execution:**

```bash
ssh root@157.157.221.29 -p 32658 -i ~/.ssh/id_ed25519
```

Then paste this:

```bash
cd /workspace && \
curl -sSL https://raw.githubusercontent.com/infolake/goe_framework/main/Shared_Resources/validation/fermion_models/setup_and_run_gpu.sh | bash
```

**OR manual setup:**

```bash
# In RunPod terminal
cd /workspace
apt-get update && apt-get install -y git python3-pip
pip3 install numpy scipy matplotlib pandas seaborn torch torchvision --index-url https://download.pytorch.org/whl/cu121

git clone https://github.com/infolake/goe_framework.git
cd goe_framework/Shared_Resources/validation/fermion_models

python3 goe_fermion_statistical_tests_gpu.py
```

---

## Performance (RTX 4090)

| Operation | Samples | Expected Time | Throughput |
|-----------|---------|---------------|------------|
| Bootstrap | 100,000 | ~5-10s | ~10-20k/s |
| Permutation | 100,000 | ~5-10s | ~10-20k/s |
| **Total (3 sectors)** | **600,000** | **~30-60s** | **~10-20k/s** |

---

## Output Files

1. **`goe_gpu_statistical_tests_results.json`** - Complete results
2. **`goe_gpu_tests_leptons.pdf/png`** - Diagnostic plots
3. **`goe_gpu_tests_up_quarks.pdf/png`** - Diagnostic plots
4. **`goe_gpu_tests_down_quarks.pdf/png`** - Diagnostic plots

---

## GPU vs CPU Comparison

| Feature | CPU Version | **GPU Version (RTX 4090)** |
|---------|-------------|---------------------------|
| Bootstrap | 10,000 | **100,000** |
| Permutation | 10,000 | **100,000** |
| Runtime (all sectors) | ~2-3 min | **~30-60 sec** |
| Throughput | ~100/s | **~10-20k/s** |
| **Speedup** | 1x | **~100-200x** |

---

## What the GPU Accelerates

### ✅ GPU-Accelerated (PyTorch):
- Bootstrap resampling (100k samples)
- Permutation test (100k permutations)
- Basic metrics (MAPE, RMSE, MAE)
- Tensor operations

### 📊 CPU (SciPy - required):
- Chi-squared test
- Shapiro-Wilk test
- Kolmogorov-Smirnov test
- AIC/BIC calculation

---

## Expected Results

### Leptons (e, μ, τ)
```json
{
  "MAPE": 2.15,
  "Chi2/dof": 0.089,
  "R_squared": 0.9997,
  "bootstrap_gpu": {
    "samples": 100000,
    "time_seconds": 5.2,
    "samples_per_second": 19230,
    "mean_error_ci": [1.89, 2.41]
  },
  "permutation_gpu": {
    "tests": 100000,
    "time_seconds": 6.8,
    "permutations_per_second": 14706,
    "p_value": 0.00001
  }
}
```

### Up Quarks (u, c, t)
```json
{
  "MAPE": 7.95,
  "R_squared": 0.9992,
  "bootstrap_gpu": {
    "mean_error_ci": [6.2, 9.7]
  }
}
```

### Down Quarks (d, s, b)
```json
{
  "MAPE": 8.12,
  "R_squared": 0.9993,
  "permutation_gpu": {
    "p_value": 0.00002
  }
}
```

---

## Troubleshooting

### CUDA Out of Memory

Reduce batch size in `goe_fermion_statistical_tests_gpu.py`:

```python
# Line ~180
batch_size = 5000  # Reduce from 10000
```

### Torch not found

```bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### GPU not detected

```bash
nvidia-smi  # Check if GPU is visible
python3 -c "import torch; print(torch.cuda.is_available())"
```

---

## Customization

### Increase samples (if VRAM allows):

```python
# In main block
results = analyze_sector_gpu(
    sector,
    n_bootstrap=500000,      # 5x more
    n_permutations=500000,   # 5x more
    save_plots=True
)
```

### Run only one sector:

```python
if __name__ == "__main__":
    results = analyze_sector_gpu('leptons', n_bootstrap=100000, n_permutations=100000)
```

---

## Citation

```bibtex
@article{camargo2025goe,
  title={Geometrodynamics of Entropy: Fermion Mass Quantization and Cosmological Bounce},
  author={Camargo, Guilherme de},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2025}
}
```

---

## Contact

**Author:** Dr. Guilherme de Camargo  
**Email:** camargo@phiq.io  
**GitHub:** https://github.com/infolake/goe_framework

