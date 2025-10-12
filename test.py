import pytest
from black_scholes import black_scholes_price
from binomial_model import binomial_option_price
from monte_carlo import monte_carlo_price
from greeks import compute_greeks
from utils import validate_inputs
from plots import plot_payoff

# === 1. PRICE TESTS ===

def test_black_scholes_price():
    price = black_scholes_price(100, 100, 1, 0.05, 0.2, option_type='call')
    assert abs(price - 10.45) < 0.5

def test_binomial_price():
    price = binomial_option_price(100, 100, 1, 0.05, 0.2, option_type='call')
    assert abs(price - 10.45) < 0.5

def test_monte_carlo_price():
    price = monte_carlo_price(100, 100, 1, 0.05, 0.2, option_type='call', num_simulations=10000)
    assert abs(price - 10.45) < 1.0

# === 2. GREEKS TESTS ===

def test_black_scholes_delta_positive():
    greeks = compute_greeks(black_scholes_price, 100, 100, 1, 0.05, 0.2, option_type='call')
    assert greeks['delta'] > 0.5

def test_black_scholes_theta_negative():
    greeks = compute_greeks(black_scholes_price, 100, 100, 1, 0.05, 0.2, option_type='call')
    assert greeks['theta'] < 0

# === 3. ERROR HANDLING ===

def test_invalid_inputs():
    with pytest.raises(ValueError):
        validate_inputs(S=-100, K=100, T=1, r=0.05, sigma=0.2)

    with pytest.raises(ValueError):
        validate_inputs(S=100, K=0, T=1, r=0.05, sigma=0.2)

# === 4. PLOT SMOKE TEST ===

def test_plot_payoff_runs():
    import matplotlib
    import numpy as np
    matplotlib.use("Agg")  # Use non-interactive backend
    plot_payoff(np.arange(50, 150), 100, option_type='call')

