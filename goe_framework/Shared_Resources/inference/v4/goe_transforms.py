# File: goe_transforms.py
# Last Modified: 2025-10-30
#
# Reparameterization functions with Jacobian computation
# Transforms unconstrained parameters to constrained physical space

import numpy as np

EPS = 1e-12

def softplus(x):
    # Numerically stable softplus
    return np.log1p(np.exp(-np.abs(x))) + np.maximum(x, 0.0)

def log_sigmoid(x):
    # Stable log(sigmoid(x)) = -softplus(-x)
    return -softplus(-x)

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def to_constrained(theta_u):
    """
    Maps theta_u (unconstrained) -> physical parameters (constrained)
    and returns also log|Jacobian| to be added to logp.
    
    Expected order: [theta_sigma, theta_rho, theta_a, theta_M, theta_f]
    
    Returns:
        params: dict with H_sigma, rho_crit_NET, a_min, M_seed, f_NET
        log_det_jac: scalar
    """
    θσ, θρ, θa, θM, θf = theta_u
    
    # H_sigma in (0, 1) via sigmoid
    H_sigma = sigmoid(θσ)
    # dH/dθ = sigmoid(θσ) * (1 - sigmoid(θσ))
    dH = sigmoid(θσ) * (1.0 - sigmoid(θσ))
    logJ_H = np.log(np.clip(dH, EPS, None))
    
    # rho_crit_NET in (1e-6, 1e-2) via logit-scaled transform
    rho_lo, rho_hi = 1e-6, 1e-2
    log_rho_lo = np.log(rho_lo)
    log_rho_hi = np.log(rho_hi)
    # Map unconstrained to log-space, then to physical
    log_rho = log_rho_lo + (log_rho_hi - log_rho_lo) * sigmoid(θρ)
    rho_crit_NET = np.exp(log_rho)
    # Jacobian: d/dθ exp(log_rho_lo + ...) = rho * (log_rho_hi - log_rho_lo) * dsigmoid/dθ
    ds = sigmoid(θρ) * (1.0 - sigmoid(θρ))
    logJ_rho = log_rho + np.log(log_rho_hi - log_rho_lo) + np.log(np.clip(ds, EPS, None))
    
    # a_min in (1e-33, 1e-27) via logit-scaled transform in log10 space
    a_lo, a_hi = 1e-33, 1e-27
    log10_a_lo = np.log10(a_lo)
    log10_a_hi = np.log10(a_hi)
    # Map unconstrained to log10-space, then to physical
    log10_a = log10_a_lo + (log10_a_hi - log10_a_lo) * sigmoid(θa)
    a_min = 10.0 ** log10_a
    # Jacobian
    ds = sigmoid(θa) * (1.0 - sigmoid(θa))
    logJ_a = log10_a * np.log(10.0) + np.log(log10_a_hi - log10_a_lo) + np.log(np.clip(ds, EPS, None))
    
    # M_seed in (1e3, 1e7) via logit-scaled transform in log10 space
    M_lo, M_hi = 1e3, 1e7
    log10_M_lo = np.log10(M_lo)
    log10_M_hi = np.log10(M_hi)
    log10_M = log10_M_lo + (log10_M_hi - log10_M_lo) * sigmoid(θM)
    M_seed = 10.0 ** log10_M
    # Jacobian
    ds = sigmoid(θM) * (1.0 - sigmoid(θM))
    logJ_M = log10_M * np.log(10.0) + np.log(log10_M_hi - log10_M_lo) + np.log(np.clip(ds, EPS, None))
    
    # f_NET in (1e-4, 0.1) via logit-scaled transform
    f_lo, f_hi = 1e-4, 0.1
    sf = sigmoid(θf)
    f_NET = f_lo + (f_hi - f_lo) * sf
    df_dθ = (f_hi - f_lo) * sf * (1.0 - sf)
    logJ_f = np.log(np.clip(df_dθ, EPS, None))
    
    log_det_jac = logJ_H + logJ_rho + logJ_a + logJ_M + logJ_f
    
    params = dict(
        H_sigma=H_sigma,
        rho_crit_NET=rho_crit_NET,
        a_min=a_min,
        M_seed=M_seed,
        f_NET=f_NET,
    )
    return params, float(log_det_jac)

