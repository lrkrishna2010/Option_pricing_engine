# main.py
import numpy as np

from black_scholes import black_scholes_price
from binomial_model import binomial_option_price
from monte_carlo import monte_carlo_price, simulate_paths, plot_paths, monte_carlo_greeks
from greeks import compute_greeks
from plots import plot_payoff, plot_all_vol_surfaces
from utils import validate_inputs, convert_days_to_years, print_greeks, format_option_summary

# --- Parameters ---
S = 100        # Initial stock price
K = 100        # Strike price
T = convert_days_to_years(365)  # Maturity in years
r = 0.05       # Risk-free rate
sigma = 0.2    # Volatility
option_type = 'call'

# --- Input Validation ---
validate_inputs(S, K, T, r, sigma)

# --- Black-Scholes ---
bs_price = black_scholes_price(S, K, T, r, sigma, option_type=option_type)
bs_greeks = compute_greeks(black_scholes_price, S, K, T, r, sigma, option_type=option_type)
format_option_summary(bs_price, bs_greeks, option_type, model="Black-Scholes")

# --- Binomial Tree (European) ---
bin_price = binomial_option_price(S, K, T, r, sigma, option_type=option_type, american=False)
bin_greeks = compute_greeks(binomial_option_price, S, K, T, r, sigma, option_type=option_type, american=False)
format_option_summary(bin_price, bin_greeks, option_type, model="Binomial Tree (European)")

# --- Binomial Tree (American) ---
bin_am_price = binomial_option_price(S, K, T, r, sigma, option_type=option_type, american=True)
format_option_summary(bin_am_price, model="Binomial Tree (American)", option_type=option_type)

# --- Monte Carlo ---
mc_price = monte_carlo_price(S, K, T, r, sigma, option_type=option_type, num_simulations=10000)
mc_greeks = monte_carlo_greeks(S, K, T, r, sigma, option_type=option_type, num_simulations=10000)
format_option_summary(mc_price, mc_greeks, option_type, model="Monte Carlo (European)")

# --- Payoff Diagrams ---
plot_payoff(S_range=np.linspace(50, 150, 200), K=K, option_type='call')
plot_payoff(S_range=np.linspace(50, 150, 200), K=K, option_type='put')

# --- Volatility Surfaces ---
plot_all_vol_surfaces(S=S, T=T, r=r, option_type='call')

# --- GBM Path Simulation ---
paths = simulate_paths(S=S, T=T, r=r, sigma=sigma, steps=100, n_paths=50)
plot_paths(paths, T=T)
