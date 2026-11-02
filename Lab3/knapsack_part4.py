"""
SC2001 Project 3 - Part (4): Unbounded Knapsack, bottom-up dynamic programming
==============================================================================

Problem
    Knapsack capacity C (positive integer), n object types, unlimited copies of
    each. Object i has weight w[i] > 0 and profit p[i] > 0. Find P(C), the
    maximum total profit of any set of objects whose total weight is <= C.
    Notation (same as Part 3): big C = overall capacity, small c = current capacity.

Recursive definition (Part 1)
    P(C) = 0                                                         if C = 0
    P(C) = max( {0} U { p_i + P(C - w_i) | 0 <= i < n, w_i <= C } )  if C > 0
    The {0} covers the case where no object fits.

Bottom-up algorithm (Part 3)  ->  function knapsack(C, n, w, p) below
    profit[0..C], profit[0] = 0; fill c = 1..C in increasing order, so every
    profit[c - w[i]] that profit[c] needs is already final. Only a 1-D array is
    needed because objects can be reused: profit[c] depends only on capacity.

Complexity
    Time  : Theta(n * C)  - C capacities x n object types, O(1) work each
    Space : Theta(C)      - array profit[0..C] (+ array choice[0..C] for traceback)
    Pseudo-polynomial: polynomial in the VALUE of C, exponential in its bit-length.

What this file does
    4(a)  P(16) with w = [4, 5, 8], p = [7, 6, 9]
    4(b)  P(12) with w = [5, 6, 7], p = [7, 6, 9]
    For each case it prints the step-by-step DP table, the final answer, one
    optimal selection (traceback), and cross-checks the answer against two
    independent methods (top-down memoisation and brute-force enumeration).

Run:  python knapsack_part4.py            (both cases)
      python knapsack_part4.py --bench    (also a small running-time experiment)
"""

import sys
import time
import random


# ---------------------------------------------------------------------------
# 1. Main algorithm: line-by-line translation of the Part 3 pseudocode
# ---------------------------------------------------------------------------
def knapsack(C, n, w, p):
    """Knapsack(C, n, w, p) from Part 3.

    Returns (profit, choice):
      profit[c] = maximum profit for capacity c, for c = 0..C  (answer: profit[C])
      choice[c] = object put in LAST to reach profit[c], -1 if nothing fits
                  (choice[] is an addition to the pseudocode, used only to
                   recover WHICH objects are taken; it does not change profit[])
    """
    validate(C, n, w, p)
    profit = [0] * (C + 1)                  # create array profit[0..C]
    choice = [-1] * (C + 1)
    profit[0] = 0                           # base case: capacity 0 -> profit 0

    for c in range(1, C + 1):               # for c = 1 to C  (small c first)
        profit[c] = 0                       # the {0} option: nothing fits
        for i in range(n):                  # for i = 0 to n-1
            if w[i] <= c:                   # object i fits in capacity c
                if profit[c] < p[i] + profit[c - w[i]]:
                    profit[c] = p[i] + profit[c - w[i]]
                    choice[c] = i
    return profit, choice


def traceback(C, w, choice):
    """Follow choice[] back from C to count how many of each object were used."""
    counts = [0] * len(w)
    c = C
    while c > 0 and choice[c] != -1:
        i = choice[c]
        counts[i] = counts[i] + 1
        c = c - w[i]
    return counts


# ---------------------------------------------------------------------------
# 2. Independent checks (used only to verify the DP answer is correct)
# ---------------------------------------------------------------------------
def knapsack_top_down(C, n, w, p):
    """Same recursive definition (Part 1), solved top-down with a memo table."""
    memo = {}                               # memo[c] = P(c) once computed

    def P(c):
        if c in memo:
            return memo[c]
        best = 0
        for i in range(n):
            if w[i] <= c:
                best = max(best, p[i] + P(c - w[i]))
        memo[c] = best
        return best

    return P(C)


def all_selections(C, n, w):
    """Every count vector (k_0, ..., k_{n-1}) with total weight <= C. Exponential."""
    if n == 0:
        return [[]]
    result = []
    for k in range(C // w[0] + 1):          # k copies of the first object
        for rest in all_selections(C - k * w[0], n - 1, w[1:]):
            result.append([k] + rest)
    return result


def knapsack_brute_force(C, n, w, p):
    """Try every possible selection and keep the best total profit."""
    best = 0
    for counts in all_selections(C, n, w):
        total = sum(counts[i] * p[i] for i in range(n))
        best = max(best, total)
    return best


def all_optimal_selections(C, n, w, p, target):
    """List every selection that reaches the optimal profit (small C only)."""
    return [counts for counts in all_selections(C, n, w)
            if sum(counts[i] * p[i] for i in range(n)) == target]


def validate(C, n, w, p):
    if n != len(w) or n != len(p) or n == 0:
        raise ValueError("w and p must both have n > 0 entries")
    if not isinstance(C, int) or C < 0:
        raise ValueError("C must be a non-negative integer")
    if any(x <= 0 or not isinstance(x, int) for x in list(w) + list(p)):
        raise ValueError("all weights and profits must be positive integers")


# ---------------------------------------------------------------------------
# 3. Pretty printing
# ---------------------------------------------------------------------------
def print_trace_table(C, w, p, profit, choice):
    """One row per capacity c: the candidate p[i] + profit[c - w[i]] for every i,
    then the max that becomes profit[c]. Shows exactly how each cell is filled."""
    n = len(w)
    head = f"{'c':>3} | " + " | ".join(f"{'i=' + str(i) + ' (w=' + str(w[i]) + ')':^18}" for i in range(n))
    head += f" | {'P(c)':>4} | last item"
    print(head)
    print("-" * len(head))
    for c in range(C + 1):
        cells = []
        for i in range(n):
            if c == 0:
                cells.append(f"{'base case':^18}" if i == 0 else " " * 18)
            elif w[i] <= c:
                expr = f"{p[i]}+P({c - w[i]})={p[i] + profit[c - w[i]]}"
                mark = "*" if choice[c] == i else " "
                cells.append(f"{expr + mark:^18}")
            else:
                cells.append(f"{'-':^18}")
        last = "-" if choice[c] == -1 else f"object {choice[c]}"
        print(f"{c:>3} | " + " | ".join(cells) + f" | {profit[c]:>4} | {last}")
    print("  ('-' = object does not fit;  '*' = candidate chosen as the max)")


def run_case(title, C, w, p):
    print("=" * 78)
    print(f"{title}:  compute P({C})")
    print("=" * 78)
    print(f"{'i':>5} " + "".join(f"{i:>5}" for i in range(len(w))))
    print(f"{'w_i':>5} " + "".join(f"{x:>5}" for x in w))
    print(f"{'p_i':>5} " + "".join(f"{x:>5}" for x in p))
    print()

    n = len(w)
    profit, choice = knapsack(C, n, w, p)

    print("Step-by-step bottom-up table (P(c) = profit[c]):")
    print_trace_table(C, w, p, profit, choice)
    print()
    print("Final 1-D DP array profit[0..C]:")
    print("   c   : " + " ".join(f"{c:>3}" for c in range(C + 1)))
    print("  P(c) : " + " ".join(f"{v:>3}" for v in profit))
    print()

    counts = traceback(C, w, choice)
    print("Optimal selection (traceback through choice[]):")
    for i, k in enumerate(counts):
        if k:
            print(f"  {k} x object {i}  (w={w[i]}, p={p[i]})  -> weight {k * w[i]}, profit {k * p[i]}")
    tw = sum(k * x for k, x in zip(counts, w))
    tp = sum(k * x for k, x in zip(counts, p))
    print(f"  total weight = {tw} <= {C},  total profit = {tp},  unused capacity = {C - tw}")

    others = all_optimal_selections(C, n, w, p, profit[C])
    if len(others) > 1:
        print(f"  ({len(others)} optimal selections exist; counts per type: {others})")
    else:
        print("  (this optimal selection is unique)")
    print()

    td = knapsack_top_down(C, n, w, p)
    bf = knapsack_brute_force(C, n, w, p)
    ok = profit[C] == td == bf
    print(f"Verification: bottom-up = {profit[C]}, top-down memo = {td}, brute force = {bf}"
          f"  -> {'PASS' if ok else 'FAIL'}")
    print()
    print(f">>> Maximum profit P({C}) = {profit[C]}")
    print()
    return profit[C]


# ---------------------------------------------------------------------------
# 4. Self-tests and optional running-time experiment
# ---------------------------------------------------------------------------
def self_test(trials=300):
    """Random small instances: bottom-up must equal brute force every time."""
    rng = random.Random(2001)
    for _ in range(trials):
        n = rng.randint(1, 4)
        w = [rng.randint(1, 10) for _ in range(n)]
        p = [rng.randint(1, 15) for _ in range(n)]
        C = rng.randint(0, 25)
        profit, _ = knapsack(C, n, w, p)
        assert profit[C] == knapsack_brute_force(C, n, w, p), (C, w, p)
    # edge cases
    assert knapsack(0, 1, [3], [5])[0][0] == 0          # empty knapsack
    assert knapsack(2, 2, [3, 4], [5, 6])[0][2] == 0    # nothing fits
    assert knapsack(9, 1, [3], [5])[0][9] == 15         # reuse one type 3x
    print(f"Self-test: {trials} random instances + edge cases all match brute force -> PASS")
    print()


def benchmark():
    """Empirical check of Theta(n*C): time should grow linearly in C and in n."""
    rng = random.Random(1)

    def timed(C, n, reps=3):
        w = [rng.randint(1, 100) for _ in range(n)]
        p = [rng.randint(1, 100) for _ in range(n)]
        knapsack(C, n, w, p)                 # warm-up run, not timed
        best = float("inf")
        for _ in range(reps):
            t0 = time.perf_counter()
            knapsack(C, n, w, p)
            best = min(best, time.perf_counter() - t0)
        return best

    print("Running-time experiment (best of 3 runs)")
    print("  Fix n = 10, vary C:")
    print(f"  {'C':>8} {'time (ms)':>11} {'ns per cell':>17}")
    for C in [10_000, 20_000, 40_000, 80_000]:
        t = timed(C, 10)
        print(f"  {C:>8} {t * 1000:>11.2f} {t * 1e9 / (10 * C):>17.2f}")
    print("  Fix C = 20000, vary n:")
    print(f"  {'n':>8} {'time (ms)':>11} {'ns per cell':>17}")
    for n in [5, 10, 20, 40]:
        t = timed(20_000, n)
        print(f"  {n:>8} {t * 1000:>11.2f} {t * 1e9 / (n * 20_000):>17.2f}")
    print("  Roughly constant ns per cell -> running time grows as n*C.")
    print()


if __name__ == "__main__":
    self_test()

    # Question 4(a): weights and profits from Part (2), capacity 16
    run_case("Question 4(a)", 16, [4, 5, 8], [7, 6, 9])

    # Question 4(b): new weights and profits, capacity 12
    run_case("Question 4(b)", 12, [5, 6, 7], [7, 6, 9])

    if "--bench" in sys.argv:
        benchmark()
