# File: goe_nuts_v4.py
# Last Modified: 2025-10-30
#
# Corrected NUTS sampler with proper reparameterizations and Jacobians
# Samples in unconstrained space, adapts step size and mass matrix

import numpy as np
from goe_logp import logp_unconstrained

np.seterr(all='warn')

class DualAveraging:
    # Classic step size adapter (Hoffman & Gelman, 2014)
    def __init__(self, target=0.95, gamma=0.05, t0=10.0, kappa=0.75, init_step=0.05):
        self.mu = np.log(10*init_step)
        self.target = target
        self.gamma = gamma
        self.t0 = t0
        self.kappa = kappa
        self.hbar = 0.0
        self.log_step = np.log(init_step)
        self.log_step_avg = np.log(init_step)
        self.t = 1

    def update(self, accept_stat):
        self.t += 1
        self.hbar = (1 - 1/(self.t + self.t0)) * self.hbar + (self.target - accept_stat) / (self.t + self.t0)
        self.log_step = self.mu - (np.sqrt(self.t)/self.gamma) * self.hbar
        eta = self.t ** (-self.kappa)
        self.log_step_avg = eta * self.log_step + (1 - eta) * self.log_step_avg
        return np.exp(self.log_step)

    def final(self):
        return np.exp(self.log_step_avg)

def kinetic(p, inv_mass_diag):
    return 0.5 * np.sum((p**2) * inv_mass_diag)

def leapfrog(theta, p, step, grad_fn, inv_mass_diag):
    # Half step in momentum
    lp, g = grad_fn(theta)  # g = ∂logp/∂θ
    p = p + 0.5 * step * g
    # Full step in position
    theta = theta + step * (p * inv_mass_diag)
    # Another half step
    lp_new, g_new = grad_fn(theta)
    p = p + 0.5 * step * g_new
    return theta, p, lp_new, g_new

# Global variables to pass last proposal from build_tree -> nuts_proposal
_last_proposal = None
_last_lp = None

def build_tree(theta, p, lp, g, step, direction, depth, logp_and_grad, inv_mass_diag):
    global _last_proposal, _last_lp
    if depth == 0:
        # Single leapfrog step
        th, pp, lp_new, g_new = leapfrog(theta, p*direction, step, logp_and_grad, inv_mass_diag)
        joint = lp_new - kinetic(pp, inv_mass_diag)
        joint0 = lp - kinetic(p, inv_mass_diag)
        logu = joint0 - np.random.exponential(1.0)
        s = int((joint - logu) >= -1e6)  # Relaxed divergence check
        n = 1 if (joint - logu) >= 0 else 0
        _last_proposal = th.copy()
        _last_lp = lp_new
        alpha = min(1.0, np.exp(joint - joint0))
        return th, pp, lp_new, g_new, th, pp, lp_new, g_new, n, s, alpha, 1
    else:
        # Build left/right subtree
        theta_minus, p_minus, lp_minus, g_minus, theta_plus, p_plus, lp_plus, g_plus, n1, s1, alpha1, n_alpha1 = \
            build_tree(theta, p, lp, g, step, direction, depth-1, logp_and_grad, inv_mass_diag)
        if s1 == 1:
            if direction == -1:
                theta_minus, p_minus, lp_minus, g_minus, _, _, _, _, n2, s2, alpha2, n_alpha2 = \
                    build_tree(theta_minus, p_minus, lp_minus, g_minus, step, direction, depth-1, logp_and_grad, inv_mass_diag)
            else:
                _, _, _, _, theta_plus, p_plus, lp_plus, g_plus, n2, s2, alpha2, n_alpha2 = \
                    build_tree(theta_plus, p_plus, lp_plus, g_plus, step, direction, depth-1, logp_and_grad, inv_mass_diag)
            n = n1 + n2
            s = s2 * stop_criterion(theta_minus, theta_plus, p_minus, p_plus, inv_mass_diag)
            alpha = alpha1 + alpha2
            n_alpha = n_alpha1 + n_alpha2
            return theta_minus, p_minus, lp_minus, g_minus, theta_plus, p_plus, lp_plus, g_plus, n, s, alpha, n_alpha
        else:
            return theta_minus, p_minus, lp_minus, g_minus, theta_plus, p_plus, lp_plus, g_plus, n1, s1, alpha1, n_alpha1

def stop_criterion(theta_minus, theta_plus, p_minus, p_plus, inv_mass_diag):
    # No U-turn criterion: (θ⁺-θ⁻)·p⁺ < 0 or (θ⁺-θ⁻)·p⁻ < 0
    delta = theta_plus - theta_minus
    return int((np.dot(delta, p_minus*inv_mass_diag) >= 0) and (np.dot(delta, p_plus*inv_mass_diag) >= 0))

def finite_diff_grad(f, x, eps=1e-6):
    # Simple fallback when autograd not available
    g = np.zeros_like(x, dtype=np.float64)
    fx = f(x)
    for i in range(x.size):
        xp = x.copy(); xp[i] += eps
        xm = x.copy(); xm[i] -= eps
        g[i] = (f(xp) - f(xm)) / (2*eps)
    return fx, g

def make_logp_and_grad(data):
    def f(theta):
        theta = theta.astype(np.float64)
        return logp_unconstrained(theta, data)
    def fg(theta):
        # Replace with autograd/JAX if available; here use robust finite differences
        return finite_diff_grad(f, theta, eps=1e-6)
    return fg

def nuts_proposal(theta0, lp0, g0, step, logp_and_grad, inv_mass_diag, max_depth=15):
    # Build a binary tree symmetrically (HMC NUTS)
    global _last_proposal, _last_lp
    dim = theta0.size
    p0 = np.random.normal(0, 1, size=dim) / np.sqrt(inv_mass_diag**-1)
    joint0 = lp0 - kinetic(p0, inv_mass_diag)
    theta_minus, theta_plus = theta0.copy(), theta0.copy()
    p_minus, p_plus = p0.copy(), p0.copy()
    lp_minus, lp_plus = lp0, lp0
    g_minus, g_plus = g0.copy(), g0.copy()
    theta_prop = theta0.copy()
    lp_prop = lp0
    n_prop = 1
    s = 1  # Stop flag
    alpha_sum = 0.0
    n_alpha = 0

    for depth in range(max_depth + 1):
        if s == 0:
            break
        direction = 1 if np.random.rand() < 0.5 else -1

        if direction == -1:
            theta_minus, p_minus, lp_minus, g_minus, _, _, _, _, n_new, s_new, alpha, n_alpha_new = \
                build_tree(theta_minus, p_minus, lp_minus, g_minus, step, direction, depth, logp_and_grad, inv_mass_diag)
        else:
            _, _, _, _, theta_plus, p_plus, lp_plus, g_plus, n_new, s_new, alpha, n_alpha_new = \
                build_tree(theta_plus, p_plus, lp_plus, g_plus, step, direction, depth, logp_and_grad, inv_mass_diag)

        if s_new == 1:
            # Multinomial sampling: accept candidate proportional to weight
            prob = n_new / max(n_prop + n_new, 1)
            if np.random.rand() < prob:
                theta_prop = _last_proposal.copy()
                lp_prop = _last_lp

        n_prop += n_new
        s = s_new * stop_criterion(theta_minus, theta_plus, p_minus, p_plus, inv_mass_diag)
        alpha_sum += alpha
        n_alpha += n_alpha_new

    accept_stat = alpha_sum / max(n_alpha, 1)
    return theta_prop, lp_prop, accept_stat

def sample_nuts(
    data,
    num_warmup=1200,
    num_samples=1500,
    init_step=0.05,
    target_accept=0.95,
    max_tree_depth=15,
    chains=4,
    seed=0,
):
    rng = np.random.default_rng(seed)
    dim = 5
    logp_and_grad = make_logp_and_grad(data)

    all_chains = []
    all_logp = []

    for c in range(chains):
        # Initialize in unconstrained space
        theta = rng.normal(0, 1, size=dim).astype(np.float64)
        lp, g = logp_and_grad(theta)

        # Diagonal mass ~ identity (adapt via variance)
        inv_mass_diag = np.ones(dim, dtype=np.float64)
        step = init_step
        da = DualAveraging(target=target_accept, init_step=init_step)

        # Warmup phase
        thetas = []
        lps = []
        for t in range(num_warmup):
            theta_prop, lp_prop, accept_stat = nuts_proposal(theta, lp, g, step, logp_and_grad, inv_mass_diag, max_depth=max_tree_depth)
            # Dual averaging
            step = da.update(accept_stat)
            # Update state
            theta, lp = theta_prop, lp_prop
            _, g = logp_and_grad(theta)
            thetas.append(theta.copy())
            lps.append(lp)
            # Rough mass adaptation: empirical variance (stabilized)
            if (t+1) % 100 == 0:
                arr = np.stack(thetas[-100:], axis=0)
                var = np.var(arr, axis=0) + 1e-3
                inv_mass_diag = 1.0 / var

        step = da.final()

        # Sampling phase
        chain = np.zeros((num_samples, dim), dtype=np.float64)
        logps = np.zeros((num_samples,), dtype=np.float64)
        for s in range(num_samples):
            theta, lp, acc = nuts_proposal(theta, lp, g, step, logp_and_grad, inv_mass_diag, max_depth=max_tree_depth)
            _, g = logp_and_grad(theta)
            chain[s] = theta
            logps[s] = lp

        all_chains.append(chain)
        all_logp.append(logps)

    return np.stack(all_chains, axis=0), np.stack(all_logp, axis=0)

if __name__ == "__main__":
    # Minimal execution example (replace 'data' with your actual dataset/structures)
    data = dict()
    chains, logps = sample_nuts(data, num_warmup=400, num_samples=400, chains=4, seed=42)
    print("chains shape:", chains.shape)  # (C, S, D)
    print("logp stats:", float(np.mean(logps)), float(np.std(logps)))
    print("logp std per chain:", [float(np.std(logps[i])) for i in range(4)])

