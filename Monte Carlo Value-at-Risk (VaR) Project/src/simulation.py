import numpy as np
import pandas as pd

def simulate_portfolio_returns(returns, weights, num_simulations=10000, method="bootstrap"):
    """
    Simulate portfolio returns using historical bootstrap or normal distribution.
    """
    portfolio_returns = returns.dot(weights)

    if method == "bootstrap":
        simulated = np.random.choice(portfolio_returns, size=num_simulations)
    elif method == "normal":
        mu, sigma = np.mean(portfolio_returns), np.std(portfolio_returns)
        simulated = np.random.normal(mu, sigma, num_simulations)
    else:
        raise ValueError("method must be 'bootstrap' or 'normal'")

    return simulated


def compute_var(simulated_returns, confidence_levels=[0.95, 0.99]):
    """
    Compute Value-at-Risk (VaR) at given confidence levels.
    """
    VaR = {}
    for cl in confidence_levels:
        alpha = 1 - cl
        VaR[cl] = np.percentile(simulated_returns, 100 * alpha)
    return VaR


def compute_cvar(simulated_returns, confidence_levels=[0.95, 0.99]):
    """
    Compute Conditional VaR (Expected Shortfall).
    """
    CVaR = {}
    for cl in confidence_levels:
        alpha = 1 - cl
        cutoff = np.percentile(simulated_returns, 100 * alpha)
        CVaR[cl] = simulated_returns[simulated_returns <= cutoff].mean()
    return CVaR
