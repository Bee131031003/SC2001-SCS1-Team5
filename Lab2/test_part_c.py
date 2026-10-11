import csv

import pytest

from plot_part_c import load_paired_results


FIELDS = ["V", "E", "density", "average_degree", "graphs",
          "trials_per_graph", "cpu_time_sec"]


def write_pair(directory, a_row, b_row):
    for part, row in (("a", a_row), ("b", b_row)):
        with (directory / f"part_{part}_sparse_v.csv").open("w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerow(row)


def test_load_paired_results_computes_speedup(tmp_path):
    a = dict(V="100", E="1000", density="", average_degree="10",
             graphs="3", trials_per_graph="3", cpu_time_sec="0.2")
    b = {**a, "cpu_time_sec": "0.05"}
    write_pair(tmp_path, a, b)

    result = load_paired_results("sparse_v", tmp_path)

    assert result == [{"V": 100, "E": 1000.0, "density": None,
                       "average_degree": 10, "a_sec": 0.2,
                       "b_sec": 0.05, "speedup": 4.0}]


def test_load_paired_results_rejects_mismatched_graphs(tmp_path):
    a = dict(V="100", E="1000", density="", average_degree="10",
             graphs="3", trials_per_graph="3", cpu_time_sec="0.2")
    b = {**a, "E": "1001", "cpu_time_sec": "0.05"}
    write_pair(tmp_path, a, b)

    with pytest.raises(ValueError, match="paired"):
        load_paired_results("sparse_v", tmp_path)
