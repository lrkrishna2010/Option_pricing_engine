# src/visualization.py
import os
import matplotlib
matplotlib.use("Agg")  # headless backend (no webview needed)

import matplotlib.pyplot as plt
import seaborn as sns

def plot_distribution(simulated_returns, VaR_dict, title="Monte Carlo VaR",
                      save_path="results/var_plot.png", show=False):
    plt.figure(figsize=(10,6))
    sns.histplot(simulated_returns, bins=50, kde=True, alpha=0.7, label="Simulated Returns")

    for cl, value in VaR_dict.items():
        plt.axvline(value, linestyle="--", label=f"VaR {int(cl*100)}%: {value:.4f}")

    plt.title(title)
    plt.xlabel("Simulated Portfolio Return")
    plt.ylabel("Frequency")
    plt.legend()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    plt.close()

    print(f"[OK] Plot saved → {save_path}")
