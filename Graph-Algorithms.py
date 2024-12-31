import sys

class GraphAlgorithms:
    # Floyd-Warshall Algorithm
    @staticmethod
    def floyd_warshall(graph):
        """
        Computes shortest paths between all pairs of nodes.
        :param graph: 2D list (adjacency matrix) representing the graph. graph[i][j] is the weight of edge i->j.
        :return: 2D list with shortest path distances between nodes or sys.maxsize for no path.
        """
        # Validate input
        if not graph or len(graph) != len(graph[0]):
            raise ValueError("Input graph must be a non-empty square matrix.")

        n = len(graph)
        dist = [
            [graph[i][j] if graph[i][j] != 0 or i == j else sys.maxsize for j in range(n)]
            for i in range(n)
        ]

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] != sys.maxsize and dist[k][j] != sys.maxsize:
                        dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

        return dist

    # Bellman-Ford Algorithm
    @staticmethod
    def bellman_ford(graph, source):
        """
        Computes shortest paths from the source node to all other nodes.
        :param graph: List of tuples (u, v, w) where u -> v is an edge with weight w.
        :param source: The source vertex.
        :return: List of shortest distances from source to each vertex or a message if a negative-weight cycle exists.
        """
        # Validate input
        if not graph or not all(len(edge) == 3 for edge in graph):
            raise ValueError("Graph must be a list of edges (u, v, w).")

        num_vertices = len(set([edge[0] for edge in graph] + [edge[1] for edge in graph]))
        if source < 0 or source >= num_vertices:
            raise ValueError("Source node is out of bounds.")

        dist = [sys.maxsize] * num_vertices
        dist[source] = 0

        # Relax edges |V|-1 times
        for _ in range(num_vertices - 1):
            for u, v, w in graph:
                if dist[u] != sys.maxsize and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w

        # Check for negative-weight cycles
        for u, v, w in graph:
            if dist[u] != sys.maxsize and dist[u] + w < dist[v]:
                raise Exception("Graph contains a negative-weight cycle.")

        return dist

# Example Usage
if __name__ == "__main__":
    # Example graph for Floyd-Warshall (Adjacency Matrix)
    fw_graph = [
        [0, 3, sys.maxsize, sys.maxsize],
        [sys.maxsize, 0, 1, sys.maxsize],
        [sys.maxsize, sys.maxsize, 0, 7],
        [sys.maxsize, sys.maxsize, sys.maxsize, 0]
    ]

    # Example graph for Bellman-Ford (Edge List)
    bf_graph = [
        (0, 1, 3),  # Edge from 0 to 1 with weight 3
        (1, 2, 1),  # Edge from 1 to 2 with weight 1
        (2, 3, 7),  # Edge from 2 to 3 with weight 7
        (0, 3, 5)   # Edge from 0 to 3 with weight 5
    ]

    print("Floyd-Warshall Algorithm Result:")
    result = GraphAlgorithms.floyd_warshall(fw_graph)
    for row in result:
        print(['\u221e' if x == sys.maxsize else x for x in row])

    print("\nBellman-Ford Algorithm Result:")
    try:
        print(GraphAlgorithms.bellman_ford(bf_graph, 0))
    except Exception as e:
        print(f"Error: {e}")
