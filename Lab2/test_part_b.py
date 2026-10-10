
from dijkstra_matrix import dijkstra_matrix_array

from dijkstra_heap import (
    dijkstra_list_heap,
    matrix_to_adj_list
)

from graph_generator import generate_random_matrix


INFINITY = float("inf")


def test_small_graph():
    """
    Test a small directed graph with known answers.
    """

    matrix = [
        [0,        4,        2, INFINITY],
        [INFINITY, 0,        1,        3],
        [INFINITY, 1,        0,        5],
        [INFINITY, INFINITY, INFINITY, 0]
    ]

    adj_list = matrix_to_adj_list(matrix)

    result_a = dijkstra_matrix_array(matrix, 0)
    result_b = dijkstra_list_heap(adj_list, 0)

    expected = [0, 3, 2, 6]

    print("Part (a):", result_a)
    print("Part (b):", result_b)

    assert result_a == expected
    assert result_b == expected

    print("Small graph test passed!\n")


def test_disconnected_graph():
    """
    Check that unreachable vertices remain infinity.
    """

    graph = [
        [(1, 5)],
        [],
        [(3, 2)],
        []
    ]

    result = dijkstra_list_heap(graph, 0)

    assert result == [
        0, 5, INFINITY, INFINITY
    ]

    print("Disconnected graph test passed!\n")


def test_single_vertex():
    """
    Check a graph containing only one vertex.
    """

    graph = [[]]

    result = dijkstra_list_heap(graph, 0)

    assert result == [0]

    print("Single vertex test passed!\n")


def test_random_graphs():
    """
    Compare Part (a) and Part (b) on random graphs.
    """

    v_sizes = [10, 50, 100]
    densities = [0.1, 0.5, 1.0]

    for v in v_sizes:
        for density in densities:

            matrix = generate_random_matrix(
                num_vertices=v,
                density=density
            )

            adj_list = matrix_to_adj_list(matrix)

            result_a = dijkstra_matrix_array(matrix, 0)
            result_b = dijkstra_list_heap(adj_list, 0)

            assert result_a == result_b, (
                f"Mismatch at V={v}, density={density}"
            )

            print(
                f"Passed: V={v}, density={density}"
            )

    print("\nAll random graph tests passed!")


if __name__ == "__main__":

    test_small_graph()
    test_disconnected_graph()
    test_single_vertex()
    test_random_graphs()

    print("\nALL TESTS PASSED!")
