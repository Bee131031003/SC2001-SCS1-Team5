import csv
import math
import random
import statistics
import time

from graph_generator import generate_random_matrix

from dijkstra_heap import (
    dijkstra_list_heap,
    matrix_to_adj_list
)


# Experimental settings
NUM_GRAPHS = 3
REPEATS = 3
MAX_WEIGHT = 100


def save_to_csv(filename, headers, rows):
    """
    Save experiment results into a CSV file.
    """

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


def count_edges(adj_list):
    """
    Count the total number of directed edges.
    """

    return sum(len(neighbours) for neighbours in adj_list)


def theoretical_complexity(v, e):
    """
    Standard asymptotic model for Dijkstra
    with adjacency list and binary min-heap.
    """

    return (v + e) * math.log2(v)


def measure_dijkstra(adj_list, source=0):
    """
    Measure CPU time for Dijkstra only.

    Run the same graph multiple times to reduce
    measurement noise.
    """

    times = []

    for _ in range(REPEATS):

        start_time = time.process_time()

        dijkstra_list_heap(adj_list, source)

        end_time = time.process_time()

        times.append(end_time - start_time)

    return statistics.mean(times)


def run_configuration(v, density):
    """
    Generate several graphs with the same
    V and density.

    Measure Dijkstra on each graph.
    Return average edge count and CPU time.
    """

    edge_counts = []
    cpu_times = []

    for _ in range(NUM_GRAPHS):

        # Generate weighted directed graph
        matrix = generate_random_matrix(
            num_vertices=v,
            density=density,
            max_weight=MAX_WEIGHT
        )

        # Convert into adjacency list
        # Conversion is outside the timed section
        adj_list = matrix_to_adj_list(matrix)

        # Count actual number of edges
        e = count_edges(adj_list)

        # Measure algorithm execution time
        cpu_time = measure_dijkstra(adj_list)

        edge_counts.append(e)
        cpu_times.append(cpu_time)

    avg_e = statistics.mean(edge_counts)
    avg_time = statistics.mean(cpu_times)

    return avg_e, avg_time


def run_experiment_varying_v():
    """
    Experiment 1:
    Fix density = 0.2 and vary |V|.
    """

    v_sizes = [
        100, 200, 400, 600,
        800, 1000, 1200, 1500
    ]

    density = 0.2
    recorded_rows = []

    print("=== Experiment 1: Vary |V| ===")

    for v in v_sizes:

        avg_e, avg_time = run_configuration(
            v, density
        )

        theory = theoretical_complexity(v, avg_e)

        recorded_rows.append([
            v,
            avg_e,
            density,
            theory,
            avg_time
        ])

        print(
            f"V={v:4d} | "
            f"E={avg_e:10.1f} | "
            f"CPU Time={avg_time:.6f}s"
        )

    save_to_csv(
        "part_b_varying_v.csv",
        [
            "V",
            "E",
            "density",
            "theoretical_complexity",
            "cpu_time_sec"
        ],
        recorded_rows
    )

    print("Saved part_b_varying_v.csv\n")


def run_experiment_varying_density():
    """
    Experiment 2:
    Fix |V| = 800 and vary edge density.
    """

    fixed_v = 800

    densities = [
        0.05, 0.1, 0.2, 0.4,
        0.6, 0.8, 1.0
    ]

    recorded_rows = []

    print("=== Experiment 2: Vary |E| ===")

    for density in densities:

        avg_e, avg_time = run_configuration(
            fixed_v, density
        )

        theory = theoretical_complexity(
            fixed_v, avg_e
        )

        recorded_rows.append([
            fixed_v,
            avg_e,
            density,
            theory,
            avg_time
        ])

        print(
            f"V={fixed_v} | "
            f"Density={density:.2f} | "
            f"E={avg_e:10.1f} | "
            f"CPU Time={avg_time:.6f}s"
        )

    save_to_csv(
        "part_b_varying_density.csv",
        [
            "V",
            "E",
            "density",
            "theoretical_complexity",
            "cpu_time_sec"
        ],
        recorded_rows
    )

    print("Saved part_b_varying_density.csv\n")


if __name__ == "__main__":

    # Make random graph generation reproducible
    random.seed(42)

    run_experiment_varying_v()
    run_experiment_varying_density()

    print("All Part (b) experiments completed!")
