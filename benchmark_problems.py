from random import sample


def random_regular_graph(n, d):
    """Generate a random d-regular graph according to Algorithm 1 from https://doi.org/10.1017/S0963548399003867.

    Parameters
    ----------
    n: int
        Number of vertices.
    d: int
        Graph degree.

    Returns
    -------
    list
        A list of lists, where list $i$ is a list containing the neighbours of vertex $i$.
    """

    while True:
        U = set(range(n * d))
        graph = {}

        while len(U):
            j, k = sample(U, 2)

            U.remove(j)
            U.remove(k)

            if int(j / d) == int(k / d):
                break
            if not int(j / d) in graph:
                graph[int(j / d)] = []
            if not int(k / d) in graph:
                graph[int(k / d)] = []

            graph[int(j / d)].append(int(k / d))
            graph[int(k / d)].append(int(j / d))

        if len(graph) == n and all([len(set(graph[v])) == d and v not in graph[v] for v in graph]):
            return graph