# File: goe_logp.py
# Last Modified: 2025-10-30
#
# Log-posterior wrapper with transformation and Jacobian
# Integrates physical model likelihood with reparameterization

import numpy as np
from goe_transforms import to_constrained

def log_prior_physical(params):
    """Uniform prior within physical bounds"""
    # Check bounds
    if not (0.0 <= params["H_sigma"] <= 1.0):
        return float(-np.inf)
    if not (1e-6 <= params["rho_crit_NET"] <= 1e-2):
        return float(-np.inf)
    if not (1e-33 <= params["a_min"] <= 1e-27):
        return float(-np.inf)
    if not (1e3 <= params["M_seed"] <= 1e7):
        return float(-np.inf)
    if not (1e-4 <= params["f_NET"] <= 0.1):
        return float(-np.inf)
    return 0.0

def cmb_likelihood(cmb_axis, axis_ref, H_sigma):
    """CMB anomaly: alignment of low-multipole axis with NET direction"""
    cosang = np.sum(cmb_axis * axis_ref)
    return -((1.0 - cosang * H_sigma)**2)

def pta_likelihood(pta_dirs, pta_helicity, axis_ref, H_sigma):
    """PTA gravitational wave helicity"""
    proj = np.dot(pta_dirs, axis_ref)
    pred = H_sigma * np.sign(proj)
    sigma2 = 0.05**2
    chi2 = np.sum((pta_helicity - pred)**2) / sigma2
    return -0.5 * chi2

def bh_likelihood(bh_mass, bh_z, M_seed, f_NET):
    """High-z SMBH formation from massive seeds"""
    log10_obs = np.log10(bh_mass)
    target = np.log10(M_seed) + np.log10(f_NET)
    sigma2 = 0.3**2
    chi2 = np.sum((log10_obs - target)**2) / sigma2
    highz_bonus = np.mean((bh_z > 9.0).astype(float))
    bonus = 2.0 * highz_bonus * max(0.0, np.log10(M_seed / 1e5))
    return -0.5 * chi2 + bonus

def filament_likelihood(fil_dirs, axis_ref, H_sigma):
    """Cosmic filament alignment with NET axis"""
    proj = np.abs(np.dot(fil_dirs, axis_ref))
    mean_proj = np.mean(proj)
    penalty = max(0.0, 0.5 - mean_proj)
    val = -penalty * (1.0 - H_sigma) * 50.0
    val = val + 20.0 * max(0.0, mean_proj - 0.7)
    return val

def model_logp_constrained(params, data):
    """
    Returns log p(data, params_constrained) (prior + likelihood),
    already in physical space, without Jacobian.
    """
    # Prior
    lp = log_prior_physical(params)
    if not np.isfinite(lp):
        return float(-np.inf)
    
    # Physical penalties on bounce parameters
    log10_amin = np.log10(params["a_min"])
    penalty_a = -0.5 * ((log10_amin - np.log10(1e-30)) / 0.5)**2
    
    log10_rho = np.log10(params["rho_crit_NET"])
    penalty_rho = -0.5 * ((log10_rho - np.log10(1e-4)) / 0.5)**2
    
    # Observational constraints
    if "cmb_axis" in data and "axis_ref" in data:
        L_cmb = cmb_likelihood(data["cmb_axis"], data["axis_ref"], params["H_sigma"])
    else:
        L_cmb = 0.0
    
    if "pta_dirs" in data and "pta_helicity" in data and "axis_ref" in data:
        L_pta = pta_likelihood(data["pta_dirs"], data["pta_helicity"], data["axis_ref"], params["H_sigma"])
    else:
        L_pta = 0.0
    
    if "bh_mass" in data and "bh_z" in data:
        L_bh = bh_likelihood(data["bh_mass"], data["bh_z"], params["M_seed"], params["f_NET"])
    else:
        L_bh = 0.0
    
    if "fil_dirs" in data and "axis_ref" in data:
        L_fil = filament_likelihood(data["fil_dirs"], data["axis_ref"], params["H_sigma"])
    else:
        L_fil = 0.0
    
    total = lp + L_cmb + L_pta + L_bh + L_fil + penalty_a + penalty_rho
    
    return float(total) if np.isfinite(total) else float(-np.inf)

def logp_unconstrained(theta_u, data):
    """
    Correct wrapper: applies transformations + adds log|Jacobian|.
    This is the logp that NUTS should see.
    """
    params, logJ = to_constrained(theta_u)
    lp = model_logp_constrained(params, data)
    
    # Check for finiteness
    if not np.isfinite(lp) or not np.isfinite(logJ):
        return float(-np.inf)
    
    return lp + logJ

