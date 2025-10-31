# GoE Inference V4 - User Guide

**Version:** 4.0  
**Date:** October 30, 2025  
**Status:** Production Ready

## Quick Start

### 1. Validate Installation

```bash
python3 test_v4_quick.py
```

Expected: Chains moving (std > 0.1)

### 2. Run Production Inference

```bash
python3 run_production_inference.py
```

Expected runtime: 45-60 minutes

### 3. Check Results

```bash
python3 -c "import numpy as np; chains = np.load('results/v4_production_chains.npy'); print(f'Chains: {chains.shape}')"
```

## File Overview

| File | Purpose | Status |
|------|---------|--------|
| `goe_transforms.py` | Parameter reparameterizations | Core |
| `goe_logp.py` | Log-posterior computation | Core |
| `goe_nuts_v4.py` | NUTS sampler | Core |
| `run_production_inference.py` | Production script | Ready |
| `run_teste_medio.py` | Validation test | Validated |
| `test_v4_quick.py` | Quick test | Validated |

## Documentation

- `V4_COMPLETE_DOCUMENTATION.md` - Technical details
- `V4_FINAL_REPORT.md` - Validation results and setup
- `README_V4.md` - This file

## Results

Test results stored in:
- `results/teste_medio_*.npy` - Medium test validation
- `results/v4_production_*.npy` - Production run (after execution)

## Support

For issues or questions, refer to:
1. `V4_COMPLETE_DOCUMENTATION.md` for technical details
2. `V4_FINAL_REPORT.md` for validation results
3. Code comments in individual files

