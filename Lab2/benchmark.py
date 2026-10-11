"""Paired CPU benchmarks for Project 2 Parts (a) and (b).

Run this script once to regenerate all six CSV files on the same machine.
Each graph is generated once, then used by both implementations. Graph
generation, matrix-to-list conversion, and file output occur outside the
timed batches. Each algorithm's negative-weight guard remains in its timing.
"""

import csv
import math
import random
import statistics
import time

from dijkstra_heap import dijkstra_list_heap, matrix_to_adj_list
from dijkstra_matrix import dijkstra_matrix_array
from graph_generator import generate_random_matrix, generate_sparse_matrix

SEED = 42
NUM_GRAPHS = 3
TRIALS_PER_GRAPH = 3
MIN_BATCH_CPU_SEC = 0.05
VERTEX_COUNTS = (100, 200, 400, 600, 800, 1000, 1200, 1500)
DENSITIES = (0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0)
AVERAGE_DEGREE = 10


def measure_batched(algorithm, graph, trials, min_batch_cpu_sec):
    """Return mean CPU seconds per call across independent timed batches.

    Doubling the batch size within each trial makes even fast executions
    measurable with a coarse CPU clock. The same graph is reused throughout.
    """
    times = []
    for _ in range(trials):
        batch_size = 1
        while True:
            start = time.process_time()
            for _ in range(batch_size):
                algorithm(graph, 0)
            elapsed = time.process_time() - start
            if elapsed >= min_batch_cpu_sec:
                times.append(elapsed / batch_size)
                break
            batch_size *= 2
            if batch_size > 1_048_576:
                raise RuntimeError("CPU clock did not advance during benchmark")
    return statistics.mean(times)


def benchmark_graph(matrix, trials=TRIALS_PER_GRAPH,
                    min_batch_cpu_sec=MIN_BATCH_CPU_SEC, heap_first=False):
    """Compare both representations of exactly one generated graph."""
    adj_list = matrix_to_adj_list(matrix)
    # Correctness and conversion are checked before either clock starts.
    if dijkstra_matrix_array(matrix, 0) != dijkstra_list_heap(adj_list, 0):
        raise AssertionError("Dijkstra implementations disagree on a paired graph")
    matrix_times, heap_times = [], []
    for trial in range(trials):
        runs = (
            ("matrix", dijkstra_matrix_array, matrix),
            ("heap", dijkstra_list_heap, adj_list),
        )
        if heap_first != (trial % 2 == 1):
            runs = reversed(runs)
        for name, algorithm, graph in runs:
            elapsed = measure_batched(algorithm, graph, 1, min_batch_cpu_sec)
            (matrix_times if name == "matrix" else heap_times).append(elapsed)
    return {
        "E": sum(map(len, adj_list)),
        "matrix_time": statistics.mean(matrix_times),
        "heap_time": statistics.mean(heap_times),
    }


def run_configuration(v, density=None, average_degree=None, rng=None,
                      num_graphs=NUM_GRAPHS, trials=TRIALS_PER_GRAPH,
                      min_batch_cpu_sec=MIN_BATCH_CPU_SEC):
    """Average paired timings over independently generated graphs."""
    if (density is None) == (average_degree is None):
        raise ValueError("specify exactly one of density or average_degree")
    rng = rng if rng is not None else random.Random(SEED)
    samples = []
    for graph_index in range(num_graphs):
        if density is not None:
            matrix = generate_random_matrix(v, density=density, rng=rng)
        else:
            matrix = generate_sparse_matrix(v, average_degree=average_degree,
                                            rng=rng)
        samples.append(benchmark_graph(matrix, trials, min_batch_cpu_sec,
                                       heap_first=graph_index % 2 == 1))
    return {
        "E": statistics.mean(sample["E"] for sample in samples),
        "matrix_time": statistics.mean(sample["matrix_time"] for sample in samples),
        "heap_time": statistics.mean(sample["heap_time"] for sample in samples),
        "graphs": num_graphs,
        "trials_per_graph": trials,
    }


def write_scenario(name, configurations, rng):
    """Write matching Part (a)/(b) CSVs from one sequence of paired runs."""
    rows_a, rows_b = [], []
    for v, density, degree in configurations:
        result = run_configuration(v, density=density, average_degree=degree,
                                   rng=rng)
        e = result["E"]
        common = [v, e, density if density is not None else "",
                  degree if degree is not None else "", NUM_GRAPHS,
                  TRIALS_PER_GRAPH]
        rows_a.append(common + [v * v, result["matrix_time"]])
        rows_b.append(common + [(v + e) * math.log2(v), result["heap_time"]])
        print(f"{name}: V={v:4d}, E={e:10.1f}, "
              f"matrix={result['matrix_time']:.8f}s, "
              f"heap={result['heap_time']:.8f}s", flush=True)

    for part, headers, rows in (
        ("a", ["V", "E", "density", "average_degree", "graphs",
                "trials_per_graph", "V_squared", "cpu_time_sec"], rows_a),
        ("b", ["V", "E", "density", "average_degree", "graphs",
                "trials_per_graph", "theoretical_complexity", "cpu_time_sec"], rows_b),
    ):
        with open(f"part_{part}_{name}.csv", "w", newline="") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerow(headers)
            writer.writerows(rows)


def run_all():
    rng = random.Random(SEED)
    write_scenario("varying_v", ((v, 0.2, None) for v in VERTEX_COUNTS), rng)
    write_scenario("varying_density", ((800, d, None) for d in DENSITIES), rng)
    write_scenario("sparse_v", ((v, None, AVERAGE_DEGREE)
                                for v in VERTEX_COUNTS), rng)


if __name__ == "__main__":
    run_all()
