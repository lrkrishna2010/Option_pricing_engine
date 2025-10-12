# main.py

import numpy as np
import pandas as pd
from src.data_loader import get_price_data, get_returns
from src.simulation import simulate_portfolio_returns, compute_var, compute_cvar
from src.visualisation import plot_distribution


# Step 1: Fetch data
tickers = ["AAPL", "MSFT", "GOOG", "AMZN"]
data = get_price_data(tickers, start="2022-01-01")
returns = get_returns(data)

# Step 2: Portfolio weights
weights = np.array([0.25, 0.25, 0.25, 0.25])

# Step 3: Simulation
simulated = simulate_portfolio_returns(returns, weights, num_simulations=10000, method="bootstrap")

# Step 4: Risk metrics
VaR = compute_var(simulated)
CVaR = compute_cvar(simulated)

# Step 5: Plot
plot_distribution(simulated, VaR, title="Monte Carlo Portfolio VaR",
                  save_path="results/var_plot.png", show=False)


# Step 6: Summary
summary = pd.DataFrame({"VaR": VaR, "CVaR": CVaR})
print(summary)
summary.to_csv("results/summary_table.csv")
