import numpy as np
import time
from multiprocessing import Pool, cpu_count

# Dados experimentais (muon)
a_mu_exp = 11659209.1e-10
a_mu_SM = 11659181.0e-10
delta_a_mu_exp = a_mu_exp - a_mu_SM

phi = (1 + np.sqrt(5)) / 2
m_mu_MeV = 105.6583745

def goe_g2(muon_m, Lambda_Xi_GeV, kappa=1, eps_theta=0.0):
    """Contribuição GoE ao g-2 do múon."""
    mf = muon_m / 1e3
    delta_a = kappa * (mf ** 2) / (Lambda_Xi_GeV ** 2) / (phi ** 2) + eps_theta
    return delta_a

def process_batch(batch_data):
    """Processa um lote de pontos MCMC"""
    Lambda_batch, kappa_batch, eps_batch = batch_data
    results = []
    
    for L, k, e in zip(Lambda_batch, kappa_batch, eps_batch):
        pred = goe_g2(m_mu_MeV, L, k, e)
        chi2 = ((pred - delta_a_mu_exp) / 8e-10) ** 2
        results.append([L, k, e, pred, chi2])
    
    return results

def run_large_mcmc(n_points=1000000, batch_size=10000):
    """Executa MCMC com paralelização para grandes amostras"""
    
    print(f"Iniciando MCMC com {n_points:,} pontos...")
    print(f"Usando {cpu_count()} CPUs")
    
    start_time = time.time()
    np.random.seed(123)
    
    # Gera todos os priors de uma vez
    Lambda_vals = np.random.uniform(100, 2000, n_points)
    kappa_vals = np.random.normal(1.0, 0.3, n_points)
    eps_vals = np.random.normal(0, 1e-10, n_points)
    
    # Divide em lotes para processamento paralelo
    n_batches = n_points // batch_size
    if n_batches == 0:
        n_batches = 1  # Pelo menos 1 lote
        batch_size = n_points
    
    batches = []
    for i in range(n_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, n_points)  # Evita overflow
        batch = (Lambda_vals[start_idx:end_idx], 
                kappa_vals[start_idx:end_idx], 
                eps_vals[start_idx:end_idx])
        batches.append(batch)
    
    print(f"Processando {n_batches} lotes...")
    with Pool(processes=min(cpu_count(), n_batches)) as pool:  # Não usar mais processos que lotes
        results = pool.map(process_batch, batches)
    
    # Junta resultados
    posterior = np.concatenate([np.array(batch_result) for batch_result in results])
    
    # Análise
    best_idx = np.argmin(posterior[:, 4])
    best = posterior[best_idx]
    
    elapsed = time.time() - start_time
    
    print("""
=== RESULTADOS MCMC ===
""")
    print(f"Pontos processados: {len(posterior):,}")
    print(f"Tempo total: {elapsed:.1f} segundos ({elapsed/3600:.2f} horas)")
    print(f"Melhor χ²: {best[4]:.3f}")
    print(f"Λ_Ξ ótimo: {best[0]:.2f} GeV")
    
    # Estatísticas de convergência
    within_1sigma = posterior[posterior[:, 4] < 1]
    within_2sigma = posterior[posterior[:, 4] < 4]
    
    print(f"Pontos 1σ: {len(within_1sigma):,} ({100*len(within_1sigma)/len(posterior):.3f}%)")
    print(f"Pontos 2σ: {len(within_2sigma):,} ({100*len(within_2sigma)/len(posterior):.3f}%)")
    
    if len(within_1sigma) > 0:
        Lambda_1sigma = within_1sigma[:, 0]
        print(f"Λ_Ξ (1σ): [{Lambda_1sigma.min():.1f}, {Lambda_1sigma.max():.1f}] GeV")
    
    # Salva resultados
    np.savez_compressed('mcmc_results_large.npz', 
                       posterior=posterior,
                       best_params=best,
                       elapsed=elapsed)
    
    print("Resultados salvos em: mcmc_results_large.npz")
    
    return posterior, best

if __name__ == "__main__":
    # Para teste pequeno: n_points=10000
    # Para lote médio: n_points=100000
    # Para grande lote: n_points=1000000 (1M pontos)
    # Para produção: n_points=50000000 (50M pontos) - requer máquina potente
    
    posterior, best = run_large_mcmc(n_points=1000000, batch_size=10000)  # Grande lote: 1M pontos
