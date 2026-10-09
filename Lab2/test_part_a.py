
from dijkstra_matrix import INFINITY, dijkstra_matrix_array


def test_simple_graph():
    # 0 --(10)--> 1 --(1)--> 2
    # 0 --------(3)--------> 2
    # 1 --(2)--> 3
    # 2 --(8)--> 3 --(7)--> 4
    # 2 --(2)--> 4
    num_nodes = 5
    matrix = []

    # 5*5 matrix
    for i in range(num_nodes):
        row = []
        for j in range(num_nodes):
            if i == j:
                row.append(0)  # dist btw self
            else:
                row.append(INFINITY)
        matrix.append(row)

    # weight
    matrix[0][1] = 10
    matrix[0][2] = 3
    matrix[1][2] = 1
    matrix[1][3] = 2
    matrix[2][3] = 8
    matrix[2][4] = 2
    matrix[3][4] = 7


    distances = dijkstra_matrix_array(matrix, 0)

    print("Shortest distance from source node 0：")
    for node_id in range(num_nodes):
        print(f"Shortest dist to node {node_id} : {distances[node_id]}")


if __name__ == "__main__":
    test_simple_graph()