"""Plot the three paired Part (a) benchmark scenarios."""

import csv

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_results(filename):
    with open(filename, newline="") as file:
        return list(csv.DictReader(file))


def plot_scenario(filename, output, x_column, title):
    rows = read_results(filename)
    x = [float(row[x_column]) for row in rows]
    measured = [float(row["cpu_time_sec"]) for row in rows]
    theoretical = [float(row["V_squared"]) for row in rows]
    # Match Part (b)'s least-squares scaling for visual shape comparison.
    scale = sum(t * y for t, y in zip(theoretical, measured)) / sum(
        t * t for t in theoretical
    )
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(x, measured, "o-", label="Measured CPU time")
    ax.plot(x, [scale * t for t in theoretical], "s--",
            label="Scaled V² reference")
    ax.set(xlabel="Vertices (V)" if x_column == "V" else "Actual edges (E)",
           ylabel="CPU seconds per execution", title=title)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(output, dpi=300)
    plt.close(fig)


def plot_results():
    plot_scenario("part_a_varying_v.csv", "part_a_varying_v.png", "V",
                  "Part (a): fixed density = 0.2")
    plot_scenario("part_a_varying_density.csv", "part_a_varying_e.png", "E",
                  "Part (a): fixed V = 800; varying density")
    plot_scenario("part_a_sparse_v.csv", "part_a_sparse_v.png", "V",
                  "Part (a): sparse scaling, E = 10V")


if __name__ == "__main__":
    plot_results()
