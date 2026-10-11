import math
import random

import pytest

from dijkstra_heap import dijkstra_list_heap, matrix_to_adj_list
from dijkstra_matrix import dijkstra_matrix_array
from graph_generator import generate_random_matrix, generate_sparse_matrix


@pytest.mark.parametrize(
    ("matrix", "source", "expected"),
    [
        (
            [
                [0, 10, 3, math.inf, math.inf],
                [math.inf, 0, 1, 2, math.inf],
                [math.inf, math.inf, 0, 8, 2],
                [math.inf, math.inf, math.inf, 0, 7],
                [math.inf, math.inf, math.inf, math.inf, 0],
            ],
            0,
            [0, 10, 3, 11, 5],
        ),
        (
            [[0, 0, 9], [math.inf, 0, 2], [math.inf, math.inf, 0]],
            0,
            [0, 0, 2],
        ),
        (
            [[0, 5, math.inf], [math.inf, 0, math.inf], [math.inf, math.inf, 0]],
            0,
            [0, 5, math.inf],
        ),
        ([[0]], 0, [0]),
    ],
)
def test_known_shortest_paths_match_both_representations(matrix, source, expected):
    assert dijkstra_matrix_array(matrix, source) == expected
    assert dijkstra_list_heap(matrix_to_adj_list(matrix), source) == expected


def test_zero_weight_edge_is_preserved_by_conversion():
    matrix = [[0, 0, math.inf], [math.inf, 0, 2], [math.inf, math.inf, 0]]
    assert matrix_to_adj_list(matrix) == [[(1, 0)], [(2, 2)], []]


def test_negative_weight_edges_are_rejected():
    matrix = [[0, -1], [math.inf, 0]]
    with pytest.raises(ValueError, match="negative"):
        dijkstra_matrix_array(matrix, 0)
    with pytest.raises(ValueError, match="negative"):
        matrix_to_adj_list(matrix)
    with pytest.raises(ValueError, match="negative"):
        dijkstra_list_heap([[(1, -1)], []], 0)


def test_random_graphs_match_on_identical_matrices():
    rng = random.Random(2026)
    for vertices in (10, 50, 100):
        for density in (0.1, 0.5, 1.0):
            matrix = generate_random_matrix(vertices, density, rng=rng)
            assert dijkstra_matrix_array(matrix, 0) == dijkstra_list_heap(
                matrix_to_adj_list(matrix), 0
            )


def test_sparse_generator_has_ten_outgoing_edges_per_vertex():
    for vertices in (100, 200):
        matrix = generate_sparse_matrix(vertices, average_degree=10, rng=random.Random(42))
        assert len(matrix) == vertices
        assert all(row[u] == 0 for u, row in enumerate(matrix))
        assert all(sum(weight != math.inf for v, weight in enumerate(row) if v != u) == 10
                   for u, row in enumerate(matrix))
        assert all(weight >= 0 for row in matrix for weight in row)


def test_seeded_generation_is_reproducible():
    assert generate_random_matrix(20, 0.2, rng=random.Random(42)) == \
        generate_random_matrix(20, 0.2, rng=random.Random(42))


def test_generator_can_create_zero_weight_edges_when_requested():
    matrix = generate_random_matrix(3, density=1, max_weight=0,
                                    min_weight=0, rng=random.Random(42))
    assert matrix_to_adj_list(matrix) == [
        [(1, 0), (2, 0)], [(0, 0), (2, 0)], [(0, 0), (1, 0)]
    ]
