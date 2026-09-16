import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read data from csv
df = pd.read_csv("fixed_s_varying_n.csv")

# Extract columns
n = df["n"]
S = df["S"]
actual = df["comparisons"]

# Theoretical complexity:
# T(n, S) = n log2(n/S) + nS
theoretical = n * np.log2(n / S) + n * S

# Find a scaling constant k using least squares
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
    label=r"Scaled theoretical $k[n\log_2(n/S)+nS]$"
)

plt.xlabel("Input size n")
plt.ylabel("Number of key comparisons")
plt.title("Actual vs Theoretical Key Comparisons")
plt.legend()
plt.grid(True)

plt.show()
