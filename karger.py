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
                parts = line.split()
                u, v = map(int, parts[:2])
                w = int(parts[2]) if len(parts) == 3 else 1
                edges.append((u, v, w))
                nodes.update([u, v])
    return list(nodes), edges


def choose_edge_weighted(edges):
    total_weight = sum(w for _, _, w in edges)
    r = random.uniform(0, total_weight)
    upto = 0
    for u, v, w in edges:
        if upto + w >= r:
            return u, v
        upto += w
    return edges[-1][0], edges[-1][1]


def contract_weighted(nodes, edges, target_count):
    vertices = {v: [v] for v in nodes}
    edges_current = edges.copy()

    while len(vertices) > target_count:
        u, v = choose_edge_weighted(edges_current)
        if v not in vertices or u not in vertices or u == v:
            continue

        vertices[u].extend(vertices[v])
        del vertices[v]

        new_edges = []
        for x, y, w in edges_current:
            if x == v: x = u
            if y == v: y = u
            if x != y:
                new_edges.append((x, y, w))
        edges_current = new_edges

    new_nodes = list(vertices.keys())
    return new_nodes, edges_current


def karger_stein_weighted(nodes, edges):
    n = len(nodes)
    if n <= 6:
        return karger_min_cut_weighted(nodes, edges)

    t = math.ceil(n / math.sqrt(2))

    nodes1, edges1 = contract_weighted(nodes, edges, t)
    nodes2, edges2 = contract_weighted(nodes, edges, t)

    cut1 = karger_stein_weighted(nodes1, edges1)
    cut2 = karger_stein_weighted(nodes2, edges2)

    return min(cut1, cut2)


def karger_min_cut_weighted(nodes, edges):
    vertices = {v: [v] for v in nodes}
    edges_current = edges.copy()

    while len(vertices) > 2:
        u, v = choose_edge_weighted(edges_current)
        if v not in vertices or u not in vertices or u == v:
            continue

        vertices[u].extend(vertices[v])
        del vertices[v]

        new_edges = []
        for x, y, w in edges_current:
            if x == v: x = u
            if y == v: y = u
            if x != y:
                new_edges.append((x, y, w))
        edges_current = new_edges

    return sum(w for _, _, w in edges_current)


def run_single_weighted(nodes, edges, seed=None):
    if seed is not None:
        random.seed(seed)
    return karger_stein_weighted(nodes, edges)


def estimate_min_cut_parallel(nodes, edges, iterations=100):
    with Pool(processes=cpu_count()) as pool:
        seeds = [random.randint(0, 1_000_000) for _ in range(iterations)]
        func = partial(run_single_weighted, nodes, edges)
        results = pool.map(func, seeds)

    best_cut = min(results)
    indices = [i+1 for i, cut in enumerate(results) if cut == best_cut]
    avg_iter = sum(indices) / len(indices)

    return best_cut, avg_iter


def optimal_min_cut_networkx(nodes, edges):
    G = nx.Graph()
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    cut_value, _ = nx.algorithms.connectivity.stoer_wagner(G, weight='weight')
    return cut_value


import csv
import os
import multiprocessing


def process_graph_worker(filename, result_queue):
    try:
        name = os.path.basename(filename)
        nodes, edges = read_graph(filename)
        n = len(nodes)
        m = len(edges)

        opt = optimal_min_cut_networkx(nodes, edges)

        iterations = 100
        est_cut, avg_iter = estimate_min_cut_parallel(nodes, edges, iterations)
        print(f"{name} ({n}, {m}) {opt} {avg_iter:.2f}")
        result_queue.put([name, n, m, opt, est_cut, round(avg_iter, 2)])
    except Exception as e:
        result_queue.put([filename, "ERROR", "ERROR", "ERROR", "ERROR", str(e)])


def process_graph_with_timeout(filename, timeout_seconds=1800):
    result_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=process_graph_worker, args=(filename, result_queue))
    p.start()
    p.join(timeout_seconds)

    if p.is_alive():
        p.terminate()
        p.join()
        print(f"{filename} timed out after {timeout_seconds} seconds.")
        return [filename, "TIMEOUT", "TIMEOUT", "TIMEOUT", "TIMEOUT", "TIMEOUT"]

    if result_queue.empty():
        return [filename, "ERROR", "ERROR", "ERROR", "ERROR", "NO_RESULT"]

    return result_queue.get()


def main():
    filenames = [f"g{str(i).zfill(2)}.graph" for i in range(1, 14)]
    output_file = "results.csv"

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "n", "m", "opt", "est_cut", "avg_iter"])

        for fname in filenames:
            if not os.path.exists(fname):
                print(f"File not found: {fname}")
                writer.writerow([fname, "MISSING", "MISSING", "MISSING", "MISSING", "MISSING"])
                continue

            result = process_graph_with_timeout(fname, timeout_seconds=1800)
            writer.writerow(result)
            print("Processed:", result[0])


if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    main()
