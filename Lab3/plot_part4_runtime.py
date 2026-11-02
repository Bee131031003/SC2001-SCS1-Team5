"""
SC2001 Project 3 - Part (4) empirical analysis.
Times knapsack() for growing C (n fixed) and growing n (C fixed),
and saves runtime_analysis.png for the slides.

Run:  python plot_part4_runtime.py      (needs matplotlib)
"""
import json
import random
import time

import matplotlib.pyplot as plt

from knapsack_part4 import knapsack

REPS = 7                 # take the best of REPS runs to reduce noise
rng = random.Random(2001)


def time_once(C, n):
    w = [rng.randint(1, 100) for _ in range(n)]
    p = [rng.randint(1, 100) for _ in range(n)]
    knapsack(C, n, w, p)                              # warm-up, not timed
    best = float("inf")
    for _ in range(REPS):
        t0 = time.perf_counter()
        knapsack(C, n, w, p)
        best = min(best, time.perf_counter() - t0)
    return best * 1000                                # milliseconds


def linear_fit(xs, ys):
    """Least-squares line y = a + b*x and its R^2.
    With C fixed, time = (outer-loop cost per c) * C + (inner cost) * n * C,
    so a straight line with a small intercept is what Theta(nC) predicts."""
    m = len(xs)
    mx, my = sum(xs) / m, sum(ys) / m
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    return a, b, 1 - ss_res / ss_tot


# Experiment 1: n fixed, vary C
N_FIXED = 10
Cs = [10_000 * k for k in range(1, 11)]
t_C = [time_once(C, N_FIXED) for C in Cs]

# Experiment 2: C fixed, vary n
C_FIXED = 20_000
ns = [5 * k for k in range(1, 11)]
t_n = [time_once(C_FIXED, n) for n in ns]

print(f"{'C':>8} {'time (ms)':>10}      {'n':>4} {'time (ms)':>10}")
for C, a, n, b in zip(Cs, t_C, ns, t_n):
    print(f"{C:>8} {a:>10.2f}      {n:>4} {b:>10.2f}")

# save raw numbers (used for the native charts in the slides)
with open("runtime_data.json", "w") as f:
    json.dump({"n_fixed": N_FIXED, "C": Cs, "t_C": t_C, "fit_C": linear_fit(Cs, t_C),
               "C_fixed": C_FIXED, "n": ns, "t_n": t_n, "fit_n": linear_fit(ns, t_n)}, f, indent=1)

# ---- plot ----
BLUE, INK, MUTED, GRID = "#2a78d6", "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"font.size": 12, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED})
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), facecolor="white")

panels = [
    (axes[0], Cs, t_C, "Capacity C", f"Time vs C  (n = {N_FIXED} fixed)", lambda v: f"{v // 1000}k"),
    (axes[1], ns, t_n, "Number of object types n", f"Time vs n  (C = {C_FIXED:,} fixed)", str),
]
for ax, xs, ys, xlabel, title, xfmt in panels:
    a, b, r2 = linear_fit(xs, ys)
    ax.plot([0, xs[-1]], [a, a + b * xs[-1]], color=MUTED, lw=1.5, ls="--",
            label=f"linear fit  (R² = {r2:.3f})")
    ax.plot(xs, ys, color=BLUE, lw=2, marker="o", ms=8,
            markeredgecolor="white", markeredgewidth=2, label="measured")
    ax.set_title(title, loc="left", color=INK, fontsize=13, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Running time (ms)")
    ax.set_xlim(0, xs[-1] * 1.05)
    ax.set_ylim(0, max(ys) * 1.12)
    ax.set_xticks(xs[1::2])
    ax.set_xticklabels([xfmt(x) for x in xs[1::2]])
    ax.grid(axis="y", color=GRID, lw=1)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(frameon=False, loc="upper left", labelcolor=INK)

fig.suptitle("Bottom-up unbounded knapsack: running time grows linearly in C and in n  →  Θ(nC)",
             x=0.01, ha="left", color=INK, fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig("runtime_analysis.png", dpi=200)
print("saved runtime_analysis.png")
