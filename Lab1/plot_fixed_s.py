import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read data from csv
df = pd.read_csv("fixed_s_varying_n.csv")

# Extract columns
n = df["n"]
S = df["S"]
actual = df["comparisons"]

# Asymptotic growth model:
# T(n, S) = n log2(n/S) + nS
theoretical = n * np.log2(n / S) + n * S

# Find a scaling constant k using least squares so the asymptotic model
# can be displayed on the same vertical scale as the empirical counts.
k = np.sum(actual * theoretical) / np.sum(theoretical ** 2)

scaled_theoretical = k * theoretical

print("Scaling constant k =", k)



# Plot

plt.figure(figsize=(10, 6))

plt.plot(
    n,
    actual,
    marker="o",
    label="Actual key comparisons"
)

plt.plot(
    n,
    scaled_theoretical,
    marker="s",
    linestyle="--",
    label=r"Scaled Asymptotic Model $k[n\log_2(n/S)+nS]$"
)

plt.xlabel("Input size n")
plt.ylabel("Number of key comparisons")
plt.title("Empirical Key Comparisons vs Scaled Asymptotic Model")
plt.legend()
plt.grid(True)

plt.show()
