import random

INFINITY = float("inf")


def generate_random_matrix(num_vertices, density=0.2, max_weight=100):
    """
    :param num_vertices: no. of nodes |V|
    :param density: probability of route existance bte each node (0.0 - 1.0)
    :param max_weight: max weight
    :return: 2D adjacent matrix
    """
    matrix = []

    for i in range(num_vertices):
        row = []
        for j in range(num_vertices):
            if i == j:
                row.append(0)
            else:
                if random.random() < density:
                    weight = random.randint(1, max_weight)
                    row.append(weight)
                else:
                    row.append(INFINITY)
        matrix.append(row)

    return matrix