import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read data
df = pd.read_csv("fixed_n_varying_s.csv")

S = df["S"]
comparisons = df["comparisons"]

n = df["n"].iloc[0]

# Find S with minimum number of comparisons
min_index = comparisons.idxmin()

best_S = df.loc[min_index, "S"]
min_comparisons = df.loc[min_index, "comparisons"]

print("Minimum comparisons:", min_comparisons)
print("S giving minimum comparisons:", best_S)

theoretical = (
    n * np.log2(n / S)
    + n * S
)

k = (
    np.sum(comparisons * theoretical)
    / np.sum(theoretical ** 2)
)

scaled_theoretical = k * theoretical

# Plot
plt.figure(figsize=(10, 6))

plt.plot(
    S,
    comparisons,
    marker = 'o',
    linewidth=1.8,
    label="Actual key comparisons"
)

plt.plot(
    S,
    scaled_theoretical,
    linestyle="--",
    label="Scaled theoretical growth"
)

plt.xlabel("Threshold S")
plt.ylabel("Number of Key Comparisons")

plt.title(
    f"Number of Key Comparisons vs Threshold S (n = {n:,})"
)

plt.xticks(range(0, 129, 8))

plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()
