# plot by ai

import csv
import matplotlib.pyplot as plt
import numpy as np


def plot_results():
  v_list, cpu_time_v = [], []
  with open("part_a_varying_v.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
      v_list.append(int(row[0]))
      cpu_time_v.append(float(row[2]))

  densities, cpu_time_density = [], []
  with open("part_a_varying_density.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
      densities.append(float(row[1]))
      cpu_time_density.append(float(row[2]))

  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

  ax1.plot(
      v_list,
      cpu_time_v,
      "o-",
      color="#1f77b4",
      linewidth=2,
      label="Empirical CPU Time (Measured)",
  )
  v_fit = np.linspace(min(v_list), max(v_list), 100)
  c = cpu_time_v[-1] / (v_list[-1] ** 2)
  ax1.plot(
      v_fit,
      c * (v_fit**2),
      "--",
      color="#d62728",
      linewidth=2,
      label=r"Theoretical Fit $\Theta(|V|^2)$",
  )
  ax1.set_xlabel("Number of Vertices |V|", fontsize=11, fontweight="bold")
  ax1.set_ylabel("CPU Time (seconds)", fontsize=11, fontweight="bold")
  ax1.set_title(
      "Part (a): Runtime vs |V|\n(Fixed Density = 0.2)",
      fontsize=12,
      fontweight="bold",
  )
  ax1.legend()
  ax1.grid(True, linestyle="--", alpha=0.6)

  ax2.plot(
      densities,
      cpu_time_density,
      "s-",
      color="#2ca02c",
      linewidth=2,
      label="Empirical CPU Time (|V|=800)",
  )
  mean_t = sum(cpu_time_density) / len(cpu_time_density)
  ax2.axhline(
      mean_t,
      color="gray",
      linestyle=":",
      linewidth=1.5,
      label=f"Mean Time ({mean_t:.3f}s)",
  )
  ax2.set_xlabel(
      "Edge Density (Proportional to |E|)", fontsize=11, fontweight="bold"
  )
  ax2.set_ylabel("CPU Time (seconds)", fontsize=11, fontweight="bold")
  ax2.set_title(
      "Part (a): Runtime vs Density\n(Fixed |V| = 800)",
      fontsize=12,
      fontweight="bold",
  )
  ax2.set_ylim(0, max(cpu_time_density) * 2)
  ax2.legend()
  ax2.grid(True, linestyle="--", alpha=0.6)

  plt.tight_layout()
  plt.savefig("part_a_empirical_results.png", dpi=300)
  plt.show()


if __name__ == "__main__":
  plot_results()