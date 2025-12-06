# EEF Options Pricing Engine

A Python-based quantitative finance project implementing foundational and advanced methods for pricing financial derivatives. The engine includes closed-form solutions, numerical methods, risk sensitivities (Greeks), simulations, and research-oriented tools used in modern quantitative finance.

Developed as part of the Essex Equity Fund — Quant Research Division (2025).

------------------------------------------------------------

## What This Project Is

This project is a comprehensive, educational, and research-focused library designed to mirror the core tools used by quantitative analysts, financial engineers, and derivatives researchers.

Purpose of the project:

1. Educational resource for Essex Equity Fund members  
2. A real quantitative finance coding framework  
3. A research tool demonstrating theory-to-code translation  

The project models how actual quant libraries are structured, ensuring readability, mathematical clarity, and extendability.

------------------------------------------------------------

## Features

### Closed-Form Pricing
- Black–Scholes European call and put
- Greeks: Delta, Gamma, Vega, Theta, Rho
- Implied volatility solvers

### Numerical Methods
- Binomial Tree (Cox–Ross–Rubinstein)
  - European and American options
  - Early exercise handling
  - Convergence to Black–Scholes
- Monte Carlo Simulation
  - GBM path simulation
  - European option pricing
  - Variance reduction techniques
  - Confidence intervals

### Structure
src/
    black_scholes.py
    binomial_tree.py
    monte_carlo.py
    greeks.py
notebooks/
    demo_black_scholes.ipynb
    demo_monte_carlo.ipynb
    demo_binomial_tree.ipynb

------------------------------------------------------------

## Research-Style Mathematical Derivation

This section explains the mathematics behind each model, similar to research papers or master’s-level financial engineering notes.

------------------------------------------------------------
### 1. Stochastic Process Assumptions

The underlying asset price S_t is assumed to follow a Geometric Brownian Motion (GBM):

dS_t = mu S_t dt + sigma S_t dW_t

where:  
mu = drift  
sigma = volatility  
W_t = standard Brownian motion  

Under risk-neutral measure Q:

mu is replaced with r (risk-free rate), giving:

dS_t = r S_t dt + sigma S_t dW_t^(Q)

Solution of GBM:

S_T = S_0 * exp((r - 0.5 sigma^2) T + sigma sqrt(T) Z)

where Z ~ N(0,1).

------------------------------------------------------------
### 2. Risk-Neutral Pricing Principle

The fair price of a derivative with payoff X at maturity T is:

Price = E_Q[ exp(-rT) * X ]

All pricing models in this engine implement this principle either analytically, numerically, or via simulation.

------------------------------------------------------------
### 3. Black–Scholes Derivation (Summary)

Assume a European call with payoff:

C_T = max(S_T - K, 0)

Under no-arbitrage, the Black–Scholes PDE applies:

dC/dt + 0.5 sigma^2 S^2 d^2C/dS^2 + r S dC/dS - rC = 0

Solving this PDE with terminal condition C_T produces:

C = S_0 N(d1) - K exp(-rT) N(d2)

where:

d1 = [ ln(S_0 / K) + (r + 0.5 sigma^2) T ] / (sigma sqrt(T))
d2 = d1 - sigma sqrt(T)

Put prices follow from put-call parity.

------------------------------------------------------------
### 4. Greeks Derivation

The Greeks measure sensitivity of option prices to inputs.

Delta = dC/dS  
Gamma = d^2C/dS^2  
Vega  = dC/dsigma  
Theta = dC/dt  
Rho   = dC/dr  

For example:

Delta_call = N(d1)  
Delta_put  = N(d1) - 1  

Gamma = N'(d1) / (S_0 sigma sqrt(T))  

These values are implemented analytically for speed and accuracy.

------------------------------------------------------------
### 5. Binomial Tree Derivation

The CRR discrete-time approximation builds a recombining tree.

Time step: Delta t = T / N  
Up and down factors:
u = exp(sigma sqrt(Delta t))  
d = 1/u  

Risk-neutral probability:
p = (exp(r Delta t) - d) / (u - d)

Option values are computed by backward induction:

Value = exp(-r Delta t) * ( p * V_up + (1 - p) * V_down )

American options include early exercise:
Value = max( exercise_value, continuation_value )

------------------------------------------------------------
### 6. Monte Carlo Derivation

Using the GBM solution:

S_T = S_0 * exp((r - 0.5 sigma^2) T + sigma sqrt(T) Z)

Simulate many Z ~ N(0,1) and compute:

C_MC = exp(-rT) * mean( max(S_T - K, 0) )

Variance reduction (optional):
- Antithetic variates: simulate both Z and -Z
- Reduces estimator variance without increasing cost

Confidence interval of estimate:
CI = mean ± z * (std / sqrt(n_paths))

Monte Carlo is model-flexible and handles payoff types where no closed form exists.

------------------------------------------------------------

## Why This Project Matters

This project demonstrates key quantitative finance concepts:
1. Risk-neutral pricing and no-arbitrage
2. Continuous-time modelling using stochastic calculus
3. Numerical approximation of PDE-driven pricing models
4. Simulation-based derivative valuation
5. Sensitivity and risk measurement (Greeks)
6. Research extensibility for more advanced derivative models

It provides a foundation for:
- American options via LSM  
- Heston and SABR stochastic volatility models  
- Volatility surface calibration  
- Monte Carlo Greeks (pathwise and likelihood ratio methods)  
- Finite-difference PDE solvers  

------------------------------------------------------------

## Installation

git clone https://github.com/essex-equity-fund/eef-option-pricing-engine  
cd eef-option-pricing-engine  
pip install -r requirements.txt

------------------------------------------------------------

## Quick Start

from src.black_scholes import black_scholes_call  
price = black_scholes_call(S=100, K=100, r=0.05, sigma=0.2, T=1)

from src.monte_carlo import mc_european_call  
price = mc_european_call(S0=100, K=100, r=0.05, sigma=0.2, T=1, n_paths=100000)

from src.binomial_tree import binomial_call  
price = binomial_call(S=100, K=100, r=0.05, sigma=0.2, T=1, steps=200)




------------------------------------------------------------

## Credits

Project Lead: Radhesh Krishna Lalam  
Head of Quantitative Research — Essex Equity Fund
