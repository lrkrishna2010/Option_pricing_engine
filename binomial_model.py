import numpy as np

def binomial_option_price(S, K, T, r, sigma, N=100, option_type='call', american=False):
    """
    Binomial model for option pricing.
    Parameters:
        S: Initial stock price
        K: Strike price
        T: Time to maturity (in years)
        r: Risk-free interest rate
        sigma: Volatility
        N: Number of time steps
        option_type: 'call' or 'put'
        american: True for American option, False for European
    Returns:
        Option price
    """
    dt = T / N  # time per step
    u = np.exp(sigma * np.sqrt(dt))      # up factor
    d = 1 / u                             # down factor
    p = (np.exp(r * dt) - d) / (u - d)    # risk-neutral probability
    disc = np.exp(-r * dt)               # discount per step

    # Step 1: Stock prices at maturity
    ST = np.array([S * (u ** j) * (d ** (N - j)) for j in range(N + 1)])

    # Step 2: Option values at maturity
    if option_type == 'call':
        option_values = np.maximum(0, ST - K)
    elif option_type == 'put':
        option_values = np.maximum(0, K - ST)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # Step 3: Backward induction
    for i in range(N - 1, -1, -1):
        option_values = disc * (p * option_values[1:] + (1 - p) * option_values[:-1])

        if american:
            ST = np.array([S * (u ** j) * (d ** (i - j)) for j in range(i + 1)])
            if option_type == 'call':
                option_values = np.maximum(option_values, ST - K)
            else:
                option_values = np.maximum(option_values, K - ST)

    return option_values[0]
