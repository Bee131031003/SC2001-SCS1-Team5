# inf denotes nodes are not connected
INFINITY = float('inf')


def dijkstra_matrix_array(graph_matrix, source):
    """
    :param graph_matrix: 2D adjacent matrix, size |V| x |V|
    :param source: starting node = 0
    :return: list dist of shortest route from starting node to each node
    """
    # |V|
    num_vertices = len(graph_matrix)

    if any(weight < 0 for row in graph_matrix for weight in row):
        raise ValueError("Dijkstra does not allow negative edge weights")

    # 1. dist btw SN and SN = 0，set SN to all other node = inf
    dist = []
    for i in range(num_vertices):
        dist.append(INFINITY)
    dist[source] = 0

    # 2. ：all not visited at first
    visited = []
    for i in range(num_vertices):
        visited.append(False)

    # 3. check for shortest dist btw every node,loop |V| time
    for count in range(num_vertices):

        min_distance = INFINITY
        u = -1

        for v in range(num_vertices):
            if not visited[v] and dist[v] < min_distance:
                min_distance = dist[v]
                u = v

        # cant find any  reachable node, meaning all remaining node not connected
        if u == -1:
            break

        # shortest dist for node u is cfmed
        visited[u] = True

        # relaxation
        for v in range(num_vertices):
            weight = graph_matrix[u][v]
            #condition for relaxation
            if v != u and not visited[v] and weight != INFINITY:
                new_dist = dist[u] + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist

    return dist
