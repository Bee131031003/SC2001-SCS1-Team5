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
        raw_data = generate_random_array(current_n)
        test_data = raw_data.copy()

        cmp_count = hybrid_merge_sort(test_data, fixed_s)

        recorded_rows.append([current_n, fixed_s, cmp_count])
        print(f"current_n = {current_n}, cmp_count = {cmp_count}")

    # will auto create fixed_s_varying_n.csv
    save_data_to_csv("fixed_s_varying_n.csv", ["n", "S", "comparisons"], recorded_rows)
    print("experiment 1 result saved to fixed_s_varying_n.csv\n")


# experiment 2: fix n = 100,000, vary S
def experiment_fixed_n_varying_s():
    fixed_n = 100_000
    s_candidates = range(1,129)
    recorded_rows = []

    print("=== experiment 2: fix n = 100,000, vary S ===")
    base_data = generate_random_array(fixed_n)

    for current_s in s_candidates:
        test_data = base_data.copy()

        start_time = time.process_time()
        cmp_count = hybrid_merge_sort(test_data, current_s)
        end_time = time.process_time()

        cpu_time_seconds = end_time - start_time

        recorded_rows.append([fixed_n, current_s, cmp_count, cpu_time_seconds])
        print(f"S = {current_s} -> cmp_count: {cmp_count}, cpu_time_seconds: {cpu_time_seconds:.4f} s")


    save_data_to_csv("fixed_n_varying_s.csv", ["n", "S", "comparisons", "cpu_time_seconds"], recorded_rows)
    print("experiment 2 result saved to fixed_n_varying_s.csv\n")



import statistics
import time


def measure_median_cpu_time(
    sort_function,
    test_array,
    repeat_count,
    s_value=None,
    batch_size=1
):
    average_times = []
    comparisons = None

    for _ in range(repeat_count):

        # Prepare copies BEFORE timing so array copying is not measured.
        array_copies = [
            test_array.copy()
            for _ in range(batch_size)
        ]

        start_time = time.process_time()

        for array_copy in array_copies:

            if s_value is None:
                current_comparisons = sort_function(array_copy)
            else:
                current_comparisons = sort_function(
                    array_copy,
                    s_value
                )

            if comparisons is None:
                comparisons = current_comparisons

        end_time = time.process_time()

        # Average CPU time for ONE sort
        average_time = (
            end_time - start_time
        ) / batch_size

        average_times.append(average_time)

    median_time = statistics.median(average_times)

    return median_time, comparisons


def get_timing_parameters(n):

    if n <= 1_000:
        return 5, 100

    elif n <= 10_000:
        return 5, 30

    elif n <= 100_000:
        return 5, 5

    else:
        return 3, 1


def test_s_candidates(current_n, base_data, s_candidates, stage):

    results = []

    repeat_count, batch_size = get_timing_parameters(
        current_n
    )

    best_s = None
    best_time = float("inf")

    for current_s in s_candidates:

        median_cpu_time, comparisons = (
            measure_median_cpu_time(
                sort_function=hybrid_merge_sort,
                test_array=base_data,
                repeat_count=repeat_count,
                s_value=current_s,
                batch_size=batch_size
            )
        )

        results.append([
            current_n,
            current_s,
            comparisons,
            median_cpu_time,
            stage
        ])

        if median_cpu_time < best_time:
            best_time = median_cpu_time
            best_s = current_s

        print(
            f"n={current_n:,}, "
            f"S={current_s}, "
            f"time={median_cpu_time:.6f}s"
        )

    return results, best_s, best_time


def generate_refined_s_candidates(coarse_best_s):

    lower = max(1, coarse_best_s // 2)
    upper = min(128, coarse_best_s * 2)

    # For smaller values test every integer.
    if upper <= 32:
        return list(range(lower, upper + 1))

    # For a large range, use step 2 to keep
    # the 10-million experiment manageable.
    return list(range(lower, upper + 1, 2))


# experiment 3: ciii) testing for optimal S
def experiment_optimal_s():

    n_values = [
        1_000,
        10_000,
        100_000,
        1_000_000,
        10_000_000
    ]

    coarse_s_candidates = [1, 2, 4, 8, 16, 32, 64, 128]

    recorded_rows = []
    best_s_by_n = {}

    print("=== experiment3: finding optimal S ===")

    for current_n in n_values:

        print(f"\n--- Testing n = {current_n:,} ---")

        # Same dataset used for all S values
        # for this n.
        base_data = generate_random_array(current_n)

        # Stage 1: coarse search

        coarse_results, coarse_best_s, _ = (
            test_s_candidates(current_n=current_n, base_data=base_data, s_candidates=coarse_s_candidates, stage="coarse")
        )

        recorded_rows.extend(coarse_results)

        print(f"Coarse best S = {coarse_best_s}")

        # Stage 2: refinement

        # reduce the generating time lol
        if current_n == 10_000_000:
            refined_candidates = list(
                range(
                max(1,coarse_best_s - 8), 
                min(128, coarse_best_s + 8)+1,
                2
                )
            )
        else:
            refined_candidates = (generate_refined_s_candidates(coarse_best_s))

        # Don't re-run values already tested
        # during coarse search.
        refined_candidates = [s for s in refined_candidates if s not in coarse_s_candidates]

        refined_results, refined_best_s, refined_best_time = (
            test_s_candidates(current_n=current_n, base_data=base_data, s_candidates=refined_candidates, stage="refined")
        )

        recorded_rows.extend(refined_results)

        # Find overall best S

        all_results_for_n = (coarse_results + refined_results)

        best_row = min(all_results_for_n, key=lambda row: row[3])

        best_s = best_row[1]
        best_cpu_time = best_row[3]

        best_s_by_n[current_n] = best_s

        print(
            f"FINAL for n={current_n:,}: "
            f"best S={best_s}, "
            f"median CPU time="
            f"{best_cpu_time:.6f}s"
        )

    save_data_to_csv("optimal_s.csv", ["n", "S", "comparisons", "median_cpu_time_sec", "stage"], recorded_rows)

    return best_s_by_n

# experiment 4: task d, n = 10000000
def experiment_task_d_10_million(best_s):
    n_ten_million = 10000000
    repeats = 3
    recorded_rows = []

    print(f"=== experiment 3: task d, n = 10000000 ===")
    print("generating data...")
    large_dataset = generate_random_array(n_ten_million)


    print("runing original merge sort...")
    merge_time, cmp_original = measure_median_cpu_time(merge_sort, large_dataset, repeats)

    recorded_rows.append(["Original Merge Sort", n_ten_million, "-", cmp_original, merge_time])


    print(f"runing hybrid merge sort (S={best_s})...")
    hybrid_time, cmp_hybrid = measure_median_cpu_time( hybrid_merge_sort, large_dataset, repeats, best_s)

    recorded_rows.append([f"Hybrid Sort (S={best_s})",n_ten_million, best_s, cmp_hybrid, hybrid_time])


    save_data_to_csv(
                      "task_d_10_million.csv",
                      ["Algorithm", "n", "S", "comparisons", "median_cpu_time_sec"],
                      recorded_rows,
                      )

    print(
        f"Original Merge Sort median CPU time: "
        f"{merge_time:.4f}s"
    )

    print(
        f"Hybrid Merge Sort median CPU time: "
        f"{hybrid_time:.4f}s"
    )
    
    print("experiment 4 result saved to task_d_10_million.csv\n")


if __name__ == "__main__":
    experiment_fixed_s_varying_n()
    experiment_fixed_n_varying_s()

    best_s_by_n = experiment_optimal_s()

    # Use the optimal S found for n = 10 million
    best_s = best_s_by_n[10_000_000]

    experiment_task_d_10_million(best_s)
