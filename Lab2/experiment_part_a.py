import csv
import time

from dijkstra_matrix import dijkstra_matrix_array
from graph_generator import generate_random_matrix


def save_to_csv(filename, headers, rows):
    file = open(filename, "w", newline="")
    writer = csv.writer(file)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    file.close()


def run_experiment_varying_v():
    """
    test diff |V| affect proccessing time (fix density=0.2)
    test theoretical time complexity of O(|V|^2)
    """

    v_sizes = [100, 200, 400, 600, 800, 1000, 1200, 1500]
    recorded_rows = []

    print("=== fix density=0.2, vary |V| ===")

    for v in v_sizes:
        matrix = generate_random_matrix(num_vertices=v, density=0.2)

        # 2. CPU time from source node 0
        start_time = time.process_time()
        dijkstra_matrix_array(matrix, source=0)
        end_time = time.process_time()

        cpu_time = end_time - start_time

        # 3. record result
        v_squared = v * v
        recorded_rows.append([v, v_squared, cpu_time])

        print(f"|V| = {v:4d} | |V|^2 = {v_squared:10d} | CPU Time = {cpu_time:.6f}s")

    # 4. save as csv
    save_to_csv(
        "part_a_varying_v.csv", ["V", "V_squared", "cpu_time_sec"], recorded_rows
    )
    print("Saved result to part_a_varying_v.csv！\n")


def run_experiment_varying_density():
    """fix |V|，vary density (test if CPU time affected by |E| )"""
    fixed_v = 800
    densities = [0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0]
    recorded_rows = []

    print(f"=== fixed |V|={fixed_v}, vary density ===")

    for d in densities:
        matrix = generate_random_matrix(num_vertices=fixed_v, density=d)

        start_time = time.process_time()
        dijkstra_matrix_array(matrix, source=0)
        end_time = time.process_time()

        cpu_time = end_time - start_time

        recorded_rows.append([fixed_v, d, cpu_time])
        print(f"|V| = {fixed_v} | Density = {d:4.2f} | CPU Time = {cpu_time:.6f}s")

    save_to_csv(
        "part_a_varying_density.csv", ["V", "density", "cpu_time_sec"], recorded_rows
    )
    print("Saved result to part_a_varying_density.csv！\n")


if __name__ == "__main__":
    run_experiment_varying_v()
    run_experiment_varying_density()