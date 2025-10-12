import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D plots
from black_scholes import black_scholes_price
from binomial_model import binomial_option_price
from monte_carlo import monte_carlo_price

def plot_payoff(S_range, K, option_type='call'):
    """
    Plot payoff diagram for call or put option.
    """
    if option_type == 'call':
        payoff = np.maximum(S_range - K, 0)
    elif option_type == 'put':
        payoff = np.maximum(K - S_range, 0)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    plt.figure()
    plt.plot(S_range, payoff, label=f'{option_type.capitalize()} Payoff')
    plt.axvline(K, color='red', linestyle='--', label='Strike Price')
    plt.title(f'{option_type.capitalize()} Option Payoff')
    plt.xlabel('Stock Price at Expiry')
    plt.ylabel('Payoff')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_vol_surface(pricing_func, model_name, S, T, r, sigma_range, K_range, option_type='call'):
    """
    Generate and plot a 3D volatility surface.
    """
    Sigma, K = np.meshgrid(sigma_range, K_range)
    Z = np.zeros_like(Sigma)

    for i in range(Sigma.shape[0]):
        for j in range(Sigma.shape[1]):
            Z[i, j] = pricing_func(S, K[i, j], T, r, Sigma[i, j], option_type=option_type)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(Sigma, K, Z, cmap='viridis')
    ax.set_title(f'{model_name} Volatility Surface ({option_type.capitalize()})')
    ax.set_xlabel('Volatility (σ)')
    ax.set_ylabel('Strike Price (K)')
    ax.set_zlabel('Option Price')
    plt.tight_layout()
    plt.show()


def plot_all_vol_surfaces(S=100, T=1, r=0.05, option_type='call'):
    sigma_range = np.linspace(0.05, 0.6, 20)
    K_range = np.linspace(80, 120, 20)

    print("Plotting Black-Scholes Volatility Surface...")
    plot_vol_surface(black_scholes_price, "Black-Scholes", S, T, r, sigma_range, K_range, option_type)

    print("Plotting Binomial Volatility Surface...")
    binomial_wrapper = lambda S, K, T, r, sigma, option_type='call': binomial_option_price(
        S, K, T, r, sigma, N=100, option_type=option_type, american=False)
    plot_vol_surface(binomial_wrapper, "Binomial", S, T, r, sigma_range, K_range, option_type)

    print("Plotting Monte Carlo Volatility Surface...")
    monte_carlo_wrapper = lambda S, K, T, r, sigma, option_type='call': monte_carlo_price(
        S, K, T, r, sigma, num_simulations=10000, option_type=option_type)
    plot_vol_surface(monte_carlo_wrapper, "Monte Carlo", S, T, r, sigma_range, K_range, option_type)
