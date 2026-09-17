import csv
import time

from data_generator import generate_random_array
from sorting import hybrid_merge_sort, merge_sort


# save result to csv
def save_data_to_csv(filename, header_list, row_data_list):
    file = open(filename, "w", newline="")
    writer = csv.writer(file)

    writer.writerow(header_list)
    for row in row_data_list:
        writer.writerow(row)

    file.close()


# ex1 fix s vary n
def experiment_fixed_s_varying_n():
    fixed_s = 32
    size_list = [1000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 10000000]
    recorded_rows = []

    print("=== experiment 1: fix s vary n ===")
    for current_n in size_list:
        # generate and copy test data
        raw_data = generate_random_array(current_n, current_n)
        test_data = raw_data.copy()

        cmp_count = hybrid_merge_sort(test_data, fixed_s)

        recorded_rows.append([current_n, fixed_s, cmp_count])
        print(f"current_n = {current_n}, cmp_count = {cmp_count}")

    # will auto create fixed_s_varying_n.csv
    save_data_to_csv("fixed_s_varying_n.csv", ["n", "S", "comparisons"], recorded_rows)
    print("experiment 1 result saved to fixed_s_varying_n.csv\n")


# experiment 2：fix n=100,000，fix best S
def experiment_fixed_n_varying_s():
    fixed_n = 100000
    s_candidates = range(1,129)
    recorded_rows = []

    print("=== experiment 2：fix n=100,000，fix best S ===")
    base_data = generate_random_array(fixed_n, fixed_n)

    for current_s in s_candidates:
        test_data = base_data.copy()

        start_time = time.perf_counter()
        cmp_count = hybrid_merge_sort(test_data, current_s)
        end_time = time.perf_counter()
        elapsed_seconds = end_time - start_time

        recorded_rows.append([fixed_n, current_s, cmp_count, elapsed_seconds])
        print(f"S = {current_s} -> cmp_count: {cmp_count}, elapsed_seconds: {elapsed_seconds:.4f} s")


    save_data_to_csv("fixed_n_varying_s.csv", ["n", "S", "comparisons", "time_seconds"], recorded_rows)
    print("experiment 2 result saved to fixed_n_varying_s.csv\n")


# experiment 3: task d, n = 10000000
def experiment_task_d_10_million(best_s=32):
    n_ten_million = 10000000
    recorded_rows = []

    print(f"=== experiment 3: task d, n = 10000000 ===")
    print("generating data...")
    large_dataset = generate_random_array(n_ten_million, n_ten_million)


    print("runing original merge sort...")
    data_for_original = large_dataset.copy()
    start_t1 = time.perf_counter()
    cmp_original = merge_sort(data_for_original)
    end_t1 = time.perf_counter()
    time_original = end_t1 - start_t1
    recorded_rows.append(["Original Merge Sort", n_ten_million, 1, cmp_original, time_original])


    print(f"runing hybrid merge sort (S={best_s})...")
    data_for_hybrid = large_dataset.copy()
    start_t2 = time.perf_counter()
    cmp_hybrid = hybrid_merge_sort(data_for_hybrid, best_s)
    end_t2 = time.perf_counter()
    time_hybrid = end_t2 - start_t2
    recorded_rows.append([f"Hybrid Sort (S={best_s})", n_ten_million, best_s, cmp_hybrid, time_hybrid])


    save_data_to_csv(
                      "task_d_10_million.csv",
                      ["Algorithm", "n", "S", "comparisons", "cpu_time_sec"],
                      recorded_rows,
                      )
    print("experiment 3 result saved to task_d_10_million.csv\n")


if __name__ == "__main__":
    experiment_fixed_s_varying_n()
    experiment_fixed_n_varying_s()
    experiment_task_d_10_million(best_s=32)
