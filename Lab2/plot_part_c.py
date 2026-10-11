"""Compare measured CPU time for the paired Part (a) and (b) experiments."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SCENARIOS = (
    ("varying_v", "V", "Fixed density = 0.2"),
    ("varying_density", "E", "Fixed V = 800; varying density"),
    ("sparse_v", "V", "Sparse scaling: E = 10V"),
)
PAIR_FIELDS = ("V", "E", "density", "average_degree", "graphs",
               "trials_per_graph")


def load_paired_results(scenario, directory=None):
    """Read matching CSV rows and calculate Part (a) / Part (b) speedup."""
    directory = Path(directory) if directory is not None else Path(__file__).resolve().parent
    data = {}
    for part in ("a", "b"):
        with (directory / f"part_{part}_{scenario}.csv").open(newline="") as file:
            data[part] = list(csv.DictReader(file))

    if not data["a"] or len(data["a"]) != len(data["b"]):
        raise ValueError(f"Missing or unpaired rows in {scenario}")

    results = []
    for a, b in zip(data["a"], data["b"]):
        if any(a[field] != b[field] for field in PAIR_FIELDS):
            raise ValueError(f"Mismatched paired graph settings in {scenario}")
        a_sec, b_sec = float(a["cpu_time_sec"]), float(b["cpu_time_sec"])
        if a_sec <= 0 or b_sec <= 0:
            raise ValueError(f"Nonpositive CPU time in {scenario}")
        results.append({
            "V": int(a["V"]),
            "E": float(a["E"]),
            "density": float(a["density"]) if a["density"] else None,
            "average_degree": int(a["average_degree"])
            if a["average_degree"] else None,
            "a_sec": a_sec,
            "b_sec": b_sec,
            "speedup": a_sec / b_sec,
        })
    return results


def plot_results(directory=None):
    """Write direct runtime and speedup comparisons for all three scenarios."""
    directory = Path(directory) if directory is not None else Path(__file__).resolve().parent
    fig_time, time_axes = plt.subplots(1, 3, figsize=(18, 5.5))
    fig_ratio, ratio_axes = plt.subplots(1, 3, figsize=(18, 5.5))

    for (scenario, x_field, title), time_ax, ratio_ax in zip(
        SCENARIOS, time_axes, ratio_axes
    ):
        rows = load_paired_results(scenario, directory)
        x = [row[x_field] for row in rows]
        time_ax.plot(x, [row["a_sec"] for row in rows], "o-",
                     label="Part (a): matrix + array")
        time_ax.plot(x, [row["b_sec"] for row in rows], "s-",
                     label="Part (b): list + heap")
        time_ax.set(xlabel="Vertices (V)" if x_field == "V" else "Actual edges (E)",
                    ylabel="CPU seconds per execution", title=title)
        time_ax.grid(alpha=0.3)
        time_ax.legend()

        ratio_ax.plot(x, [row["speedup"] for row in rows], "o-", color="#6f42a1")
        ratio_ax.axhline(1, color="gray", linestyle="--", label="Equal CPU time")
        ratio_ax.set(xlabel="Vertices (V)" if x_field == "V" else "Actual edges (E)",
                     ylabel="Part (a) time / Part (b) time", title=title)
        ratio_ax.grid(alpha=0.3)
        ratio_ax.legend()

    fig_time.suptitle("Dijkstra implementations: measured CPU time")
    fig_ratio.suptitle("Part (b) speedup over Part (a); above 1 favors Part (b)")
    for figure, filename in (
        (fig_time, "part_c_runtime_comparison.png"),
        (fig_ratio, "part_c_speedup.png"),
    ):
        figure.tight_layout()
        figure.savefig(directory / filename, dpi=300)
        plt.close(figure)


if __name__ == "__main__":
    plot_results()
