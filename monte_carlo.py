import numpy as np
import matplotlib.pyplot as plt

def simulate_paths(S, T, r, sigma, steps=100, n_paths=50, seed=42):
    np.random.seed(seed)
    dt = T / steps
    Z = np.random.standard_normal((steps, n_paths))
    ST = np.zeros((steps + 1, n_paths))
    ST[0] = S
    for t in range(1, steps + 1):
        ST[t] = ST[t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[t-1])
    return ST

def plot_paths(ST, T):
    steps = ST.shape[0] - 1
    time_grid = np.linspace(0, T, steps + 1)
    for i in range(min(50, ST.shape[1])):
        plt.plot(time_grid, ST[:, i], lw=0.7)
    plt.title("Simulated GBM Price Paths")
    plt.xlabel("Time (Years)")
    plt.ylabel("Price")
    plt.grid(True)
    plt.show()

def monte_carlo_price(S, K, T, r, sigma, num_simulations=100000, option_type='call', 
                      use_antithetic=False, use_control_variate=False, seed=42):
    np.random.seed(seed)
    Z = np.random.standard_normal(num_simulations)

    # Antithetic Variates
    if use_antithetic:
        Z = np.concatenate([Z, -Z])
    
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    if option_type == 'call':
        payoffs = np.maximum(ST - K, 0)
        bs_price = S - K * np.exp(-r * T)  # intrinsic approx for control variate
    elif option_type == 'put':
        payoffs = np.maximum(K - ST, 0)
        bs_price = K * np.exp(-r * T) - S
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # Control Variate
    if use_control_variate:
        control = ST
        control_mean = np.mean(control)
        b = np.cov(payoffs, control)[0, 1] / np.var(control)
        payoffs = payoffs - b * (control - S * np.exp(r * T))

    return np.exp(-r * T) * np.mean(payoffs)
def monte_carlo_greeks(S, K, T, r, sigma, num_simulations=100000, option_type='call', seed=42):
    np.random.seed(seed)
    Z = np.random.standard_normal(num_simulations)
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    if option_type == 'call':
        payoff = np.maximum(ST - K, 0)
        delta = np.mean((ST > K) * ST / S)
    else:
        payoff = np.maximum(K - ST, 0)
        delta = -np.mean((ST < K) * ST / S)

    price = np.exp(-r * T) * np.mean(payoff)

    # Estimate Vega (score function)
    vega = np.mean(payoff * Z * np.sqrt(T)) * np.exp(-r * T)

    # Estimate Rho (∂/∂r via ∂/∂e^(-rT))
    rho = T * price

    return {
        'price': price,
        'delta': delta,
        'vega': vega,
        'rho': rho
    }
