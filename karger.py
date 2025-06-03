import random
import networkx as nx


def read_graph(filename):
    edges = []
    nodes = set()
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                u, v = map(int, line.split())
                edges.append((u, v))
                nodes.update([u, v])
    return list(nodes), edges


def karger_min_cut(nodes, edges):
    vertices = {v: [v] for v in nodes}
    edges_current = edges.copy()

    while len(vertices) > 2:
        u, v = random.choice(edges_current)
        vertices[u].extend(vertices[v])
        del vertices[v]
        new_edges = []
        for x, y in edges_current:
            if x == v: x = u
            if y == v: y = u
            if x != y:
                new_edges.append((x, y))
        edges_current = new_edges

    return len(edges_current)


def estimate_min_cut(nodes, edges, iterations=100):
    best_cut = float('inf')
    cuts_found = 0
    total_iters_to_best = 0

    for i in range(1, iterations + 1):
        cut = karger_min_cut(nodes, edges)
        if cut < best_cut:
            best_cut = cut
            cuts_found = 1
            total_iters_to_best = i
        elif cut == best_cut:
            cuts_found += 1
            total_iters_to_best = (total_iters_to_best * (cuts_found - 1) + i) / cuts_found

    return best_cut, total_iters_to_best


def optimal_min_cut_networkx(nodes, edges):
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    cut_value, partition = nx.algorithms.connectivity.stoer_wagner(graph)
    return cut_value


def main():
    filename = 'g01.graph'
    name = filename.split('/')[-1]
    nodes, edges = read_graph(filename)
    n = len(nodes)
    m = len(edges)

    opt = optimal_min_cut_networkx(nodes, edges)

    iterations = 200
    est_cut, avg_iter = estimate_min_cut(nodes, edges, iterations)

    print(f"{name} ({n}, {m}) {opt} {avg_iter:.2f}")


if __name__ == "__main__":
    main()
