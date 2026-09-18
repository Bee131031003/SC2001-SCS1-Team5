import pandas as pd
import matplotlib.pyplot as plt


# Read results from c(iii)
df = pd.read_csv("optimal_s.csv")


# Graph 1: Best S for each input size n

# Find the row with minimum median CPU time for each n
best_indices = (
    df.groupby("n")["median_cpu_time_sec"]
    .idxmin()
)

best_results = (
    df.loc[
        best_indices,
        ["n", "S", "median_cpu_time_sec"]
    ]
    .sort_values("n")
)


print("\nOptimal S for each input size:")
print(best_results.to_string(index=False))


plt.figure(figsize=(9, 6))

plt.plot(
    best_results["n"],
    best_results["S"],
    marker="o"
)

# n varies from 1,000 to 10,000,000,
# so log scale makes the graph easier to read
plt.xscale("log")

plt.xlabel("Input Size n (log scale)")
plt.ylabel("Best Threshold S")

plt.title(
    "Empirically Best S Across Different Input Sizes"
)

plt.grid(True)

plt.tight_layout()
plt.show()


# Graph 2: Relative CPU time for different S values

# For each n:
# relative time = CPU time / minimum CPU time for that n

# Therefore:
# 1.00 = fastest tested S
# 1.05 = 5% slower than the fastest tested S
df["relative_time"] = (
    df["median_cpu_time_sec"]
    /
    df.groupby("n")["median_cpu_time_sec"]
    .transform("min")
)


plt.figure(figsize=(10, 6))

for current_n in sorted(df["n"].unique()):

    subset = df[df["n"] == current_n]

    # Sort by S so that the line is drawn correctly
    subset = subset.sort_values("S")

    plt.plot(
        subset["S"],
        subset["relative_time"],
        marker="o",
        label=f"n={current_n:,}"
    )


plt.xlabel("Threshold S")
plt.ylabel("Relative CPU Time")

plt.title(
    "Relative CPU Time Across Different Threshold S Values"
)

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()