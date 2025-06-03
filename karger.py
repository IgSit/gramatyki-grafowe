import random
import math
import networkx as nx
from multiprocessing import Pool, cpu_count
from functools import partial


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


def contract(nodes, edges, target_count):
    vertices = {v: [v] for v in nodes}
    edges_current = edges.copy()

    while len(vertices) > target_count:
        u, v = random.choice(edges_current)
        if v not in vertices or u not in vertices:
            continue
        vertices[u].extend(vertices[v])
        del vertices[v]

        new_edges = []
        for x, y in edges_current:
            if x == v: x = u
            if y == v: y = u
            if x != y:
                new_edges.append((x, y))
        edges_current = new_edges

    new_nodes = list(vertices.keys())
    return new_nodes, edges_current


def karger_stein(nodes, edges):
    n = len(nodes)
    if n <= 6:
        return karger_min_cut(nodes, edges)

    t = math.ceil(n / math.sqrt(2))

    nodes1, edges1 = contract(nodes, edges, t)
    nodes2, edges2 = contract(nodes, edges, t)

    cut1 = karger_stein(nodes1, edges1)
    cut2 = karger_stein(nodes2, edges2)

    return min(cut1, cut2)


def karger_min_cut(nodes, edges):
    vertices = {v: [v] for v in nodes}
    edges_current = edges.copy()

    while len(vertices) > 2:
        u, v = random.choice(edges_current)
        if v not in vertices or u not in vertices:
            continue
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


def run_single_karger_stein(nodes, edges, seed=None):
    if seed is not None:
        random.seed(seed)
    return karger_stein(nodes, edges)


def estimate_min_cut_parallel(nodes, edges, iterations=100):
    with Pool(processes=cpu_count()) as pool:
        seeds = [random.randint(0, 1_000_000) for _ in range(iterations)]
        func = partial(run_single_karger_stein, nodes, edges)
        results = pool.map(func, seeds)

    best_cut = min(results)
    indices = [i+1 for i, cut in enumerate(results) if cut == best_cut]
    avg_iter = sum(indices) / len(indices)

    return best_cut, avg_iter


def optimal_min_cut_networkx(nodes, edges):
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    cut_value, _ = nx.algorithms.connectivity.stoer_wagner(graph)
    return cut_value


def main():
    filename = 'g01.graph'
    name = filename.split('/')[-1]
    nodes, edges = read_graph(filename)
    n = len(nodes)
    m = len(edges)

    opt = optimal_min_cut_networkx(nodes, edges)

    iterations = 100
    est_cut, avg_iter = estimate_min_cut_parallel(nodes, edges, iterations)

    print(f"{name} ({n}, {m}) {opt} {avg_iter:.2f}")


if __name__ == "__main__":
    main()
