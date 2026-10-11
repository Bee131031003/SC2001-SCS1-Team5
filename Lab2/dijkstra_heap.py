import heapq

INFINITY = float("inf")


def matrix_to_adj_list(graph_matrix):
    """
    Convert an adjacency matrix into an adjacency list.

    Adjacency list format:
        adj_list[u] = [(v, weight), ...]

    An edge exists if its weight is nonnegative and finite.
    """

    num_vertices = len(graph_matrix)

    # Create an empty neighbour list for each vertex
    adj_list = [[] for _ in range(num_vertices)]

    for u in range(num_vertices):
        for v in range(num_vertices):

            weight = graph_matrix[u][v]

            if weight < 0:
                raise ValueError("Dijkstra does not allow negative edge weights")
            # Diagonal zeros represent distance to self, not edges.
            if u != v and weight != INFINITY:
                adj_list[u].append((v, weight))

    return adj_list


def dijkstra_list_heap(graph, source):
    """
    Dijkstra's Algorithm using:
      1. Adjacency list
      2. Min-heap priority queue

    Parameters:
        graph: adjacency list
        source: starting vertex

    Returns:
        dist: shortest distance from source to each vertex
    """

    num_vertices = len(graph)

    if any(weight < 0 for neighbours in graph for _, weight in neighbours):
        raise ValueError("Dijkstra does not allow negative edge weights")

    # Step 1: Initialize distances
    dist = [INFINITY] * num_vertices
    dist[source] = 0

    # Step 2: Initialize min-heap
    # Each entry is (distance, vertex)
    min_heap = [(0, source)]

    # Step 3: Process heap until empty
    while min_heap:

        # Extract vertex with smallest tentative distance
        current_dist, u = heapq.heappop(min_heap)

        # Ignore outdated heap entries
        if current_dist > dist[u]:
            continue

        # Step 4: Examine all neighbours of vertex u
        for v, weight in graph[u]:

            # Calculate distance through vertex u
            new_dist = current_dist + weight

            # Step 5: Relax edge if a shorter path is found
            if new_dist < dist[v]:

                # Update shortest distance
                dist[v] = new_dist

                # Insert updated distance into min-heap
                heapq.heappush(min_heap, (new_dist, v))

    return dist


if __name__ == "__main__":

    # Example directed graph
    graph = [
        [(1, 4), (2, 2)],
        [(2, 1), (3, 3)],
        [(1, 1), (3, 5)],
        []
    ]

    result = dijkstra_list_heap(graph, source=0)

    print("Shortest distances from vertex 0:")
    print(result)
