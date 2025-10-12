import numpy as np
from scipy.stats import norm


def convert_days_to_years(days):
    """
    Converts number of days to fractional years.
    """
    return days / 365.0


def cumulative_normal(x):
    """
    Returns cumulative distribution of the standard normal variable.
    """
    return norm.cdf(x)


def safe_divide(a, b, default=0.0):
    """
    Divides a by b, returns default if division fails.
    """
    try:
        return a / b
    except ZeroDivisionError:
        return default


def round_dict(d, decimals=4):
    """
    Rounds all float values in a dictionary.
    """
    return {k: round(v, decimals) if isinstance(v, (int, float)) else v for k, v in d.items()}


def print_greeks(greeks_dict, title="Option Greeks"):
    """
    Pretty prints Greek values.
    """
    print(f"\n🧠 {title}")
    greeks_dict = round_dict(greeks_dict)
    for k, v in greeks_dict.items():
        print(f"  {k.capitalize():<6}: {v}")


def validate_inputs(S, K, T, r, sigma):
    """
    Validates that all required parameters are positive and logical.
    Raises ValueError if invalid.
    """
    if S <= 0:
        raise ValueError("Stock price S must be > 0")
    if K <= 0:
        raise ValueError("Strike price K must be > 0")
    if T <= 0:
        raise ValueError("Time to maturity T must be > 0")
    if sigma < 0:
        raise ValueError("Volatility σ must be ≥ 0")
    if r < 0:
        raise ValueError("Risk-free rate r must be ≥ 0")


def log_run(message):
    """
    Simple run-time log wrapper.
    """
    print(f"[LOG] {message}")


def format_option_summary(price, greeks=None, option_type="call", model=""):
    """
    Formats a summary for CLI display.
    """
    print(f"\n📈 {model} {option_type.capitalize()} Option Summary")
    print(f"  Price : {round(price, 4)}")
    if greeks:
        greeks = round_dict(greeks)
        for k, v in greeks.items():
            print(f"  {k.capitalize():<6}: {v}")
