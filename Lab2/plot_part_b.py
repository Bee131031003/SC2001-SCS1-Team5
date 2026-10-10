
import csv
import numpy as np
import matplotlib.pyplot as plt


def read_results(filename):
    """
    Read CSV containing:
    V, E, density, theoretical_complexity, cpu_time_sec
    """

    v_list = []
    e_list = []
    cpu_times = []

    with open(filename, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            v_list.append(int(row["V"]))
            e_list.append(float(row["E"]))
            cpu_times.append(float(row["cpu_time_sec"]))

    return (
        np.array(v_list),
        np.array(e_list),
        np.array(cpu_times)
    )


def theoretical_model(v, e):
    """
    O((V + E) log V)
    """

    return (v + e) * np.log2(v)


def fit_scaling_constant(actual, theoretical):
    """
    Least-squares scaling:
    k = sum(actual * theoretical)
        / sum(theoretical^2)
    """

    return np.dot(actual, theoretical) / np.dot(
        theoretical, theoretical
    )


def plot_varying_v():
    """
    Plot CPU time vs |V| at fixed density.
    """

    v, e, cpu_times = read_results(
        "part_b_varying_v.csv"
    )

    theory = theoretical_model(v, e)

    # Scale theoretical complexity to measured CPU time
    k = fit_scaling_constant(cpu_times, theory)

    scaled_theory = k * theory

    plt.figure(figsize=(9, 6))

    plt.plot(
        v,
        cpu_times,
        "o-",
        color="#9467bd",
        linewidth=2,
        label="Empirical CPU Time"
    )

    plt.plot(
        v,
        scaled_theory,
        "s--",
        color="#d62728",
        linewidth=2,
        label=r"Scaled Theoretical $O((V+E)\log V)$"
    )

    plt.xlabel("Number of Vertices |V|")
    plt.ylabel("CPU Time (seconds)")

    plt.title(
        "Part (b): Runtime vs  \n"
        "(Fixed Density = 0.2)"
    )

    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()

    plt.savefig(
        "part_b_varying_v.png",
        dpi=300
    )

    plt.show()


def plot_varying_e():
    """
    Plot CPU time vs |E| at fixed |V| = 800.
    """

    v, e, cpu_times = read_results(
        "part_b_varying_density.csv"
    )

    theory = theoretical_model(v, e)

    k = fit_scaling_constant(cpu_times, theory)

    scaled_theory = k * theory

    plt.figure(figsize=(9, 6))

    plt.plot(
        e,
        cpu_times,
        "o-",
        color="#2ca02c",
        linewidth=2,
        label="Empirical CPU Time"
    )

    plt.plot(
        e,
        scaled_theory,
        "s--",
        color="#d62728",
        linewidth=2,
        label=r"Scaled Theoretical $O((V+E)\log V)$"
    )

    plt.xlabel("Number of Edges |E|")
    plt.ylabel("CPU Time (seconds)")

    plt.title(
        "Part (b): Runtime vs Number of Edges\n"
        "(Fixed |V| = 800)"
    )

    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()

    plt.savefig(
        "part_b_varying_e.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":

    plot_varying_v()
    plot_varying_e()

    print("All Part (b) plots generated!")
