import random

INFINITY = float("inf")


def generate_random_matrix(num_vertices, density=0.2, max_weight=100,
                           rng=None, min_weight=1):
    """
    :param num_vertices: no. of nodes |V|
    :param density: probability of route existance bte each node (0.0 - 1.0)
    :param max_weight: max weight
    :return: 2D adjacent matrix
    """
    if not 0 <= density <= 1 or not 0 <= min_weight <= max_weight:
        raise ValueError("density and weight range must be valid and nonnegative")
    rng = rng if rng is not None else random
    matrix = []

    for i in range(num_vertices):
        row = []
        for j in range(num_vertices):
            if i == j:
                row.append(0)
            else:
                if rng.random() < density:
                    weight = rng.randint(min_weight, max_weight)
                    row.append(weight)
                else:
                    row.append(INFINITY)
        matrix.append(row)

    return matrix


def generate_sparse_matrix(num_vertices, average_degree=10, max_weight=100,
                           rng=None, min_weight=1):
    """Generate a directed matrix with exactly average_degree edges per vertex.

    The default weight range stays 1..100, matching the density generator.
    Set min_weight=0 when a test needs zero-weight edges.
    """
    if not 0 <= average_degree < num_vertices or not 0 <= min_weight <= max_weight:
        raise ValueError("degree and weight range must be valid and nonnegative")
    rng = rng if rng is not None else random
    matrix = [[INFINITY] * num_vertices for _ in range(num_vertices)]
    for u in range(num_vertices):
        matrix[u][u] = 0
        neighbours = rng.sample([v for v in range(num_vertices) if v != u],
                                average_degree)
        for v in neighbours:
            matrix[u][v] = rng.randint(min_weight, max_weight)
    return matrix
