import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import os

PLOT_DIR = "plots"
os.makedirs(PLOT_DIR, exist_ok=True)

sns.set(style="whitegrid", font_scale=1.1)

data = pd.read_csv("results.csv").to_csv(index=False)

df = pd.read_csv(StringIO(data))

# Replace "timeout" with NaN so they don't break the plots
df = df.replace("timeout", np.nan)

# Convert numeric columns
for col in ["search", "search2", "search3", "search4"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---- Heatmap ----
plt.figure(figsize=(12, 8))
sns.heatmap(df.set_index("File"), cmap="viridis", annot=True, fmt=".2f")
plt.title("Runtime Heatmap (seconds)")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "HeatMap.png"), dpi=150)
plt.show()
plt.close()

# ---- Log-scale median comparison ----
plt.figure(figsize=(10, 6))
melted = df.melt(id_vars="File", var_name="Algorithm", value_name="Time")
sns.barplot(data=melted, x="Algorithm", y="Time", estimator=np.median)
plt.yscale("log")
plt.title("Median Runtime (log scale)")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "MedianRuntime.png"), dpi=150)
plt.show()
plt.close()

# ---- Speed comparison relative to search4 ----
speed = df.copy()
for col in ["search", "search2", "search3"]:
    speed[col] = speed[col] / speed["search4"]

speed_melt = speed.melt(id_vars="File", var_name="Algorithm", value_name="Speed")
plt.figure(figsize=(10, 6))
sns.barplot(data=speed_melt[speed_melt["Algorithm"] != "search4"],
            x="Algorithm", y="Speed")
plt.yscale("log")
plt.title("Relative Slowdown vs search4 (higher = slower)")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "SpeedComparison.png"), dpi=150)
plt.show()
plt.close()

# ---- Average rank ----
rankings = df[["search", "search2", "search3", "search4"]].rank(axis=1)
avg_rank = rankings.mean().sort_values()

plt.figure(figsize=(8, 5))
sns.barplot(x=avg_rank.index, y=avg_rank.values)
plt.title("Average Performance Rank (lower is better)")
plt.ylabel("Avg Rank")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "AvgRank.png"), dpi=150)
plt.show()
plt.close()

print("Average rank:\n", avg_rank)
