from black_scholes import black_scholes_price
from binomial_model import binomial_option_price

def compute_greeks(model_func, S, K, T, r, sigma, option_type='call', american=False, h=1e-4):
    """
    Computes Delta, Gamma, Theta, Vega, and Rho using finite differences.
    """
    # Detect if model is Black-Scholes (no `american` flag)
    if model_func.__name__ == 'black_scholes_price':
        kwargs = {'option_type': option_type}
    else:
        kwargs = {'option_type': option_type, 'american': american}

    # --- Base Price ---
    base_price = model_func(S, K, T, r, sigma, **kwargs)

    # --- Delta ---
    price_up = model_func(S + h, K, T, r, sigma, **kwargs)
    price_down = model_func(S - h, K, T, r, sigma, **kwargs)
    delta = (price_up - price_down) / (2 * h)

    # --- Gamma ---
    gamma = (price_up - 2 * base_price + price_down) / (h ** 2)

    # --- Theta ---
    price_shorter_T = model_func(S, K, T - h, r, sigma, **kwargs)
    theta = (price_shorter_T - base_price) / h

    # --- Vega ---
    price_up_sigma = model_func(S, K, T, r, sigma + h, **kwargs)
    price_down_sigma = model_func(S, K, T, r, sigma - h, **kwargs)
    vega = (price_up_sigma - price_down_sigma) / (2 * h)

    # --- Rho ---
    price_up_r = model_func(S, K, T, r + h, sigma, **kwargs)
    price_down_r = model_func(S, K, T, r - h, sigma, **kwargs)
    rho = (price_up_r - price_down_r) / (2 * h)

    return {
        'price': base_price,
        'delta': delta,
        'gamma': gamma,
        'theta': theta,
        'vega': vega,
        'rho': rho
    }
