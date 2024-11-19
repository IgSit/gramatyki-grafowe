from itertools import combinations

from productions.production import Production
from graph.hypergraph import HyperGraph


class P1(Production):
    def check(self, graph: HyperGraph, level: int):
        for node in graph.hyper_nodes:
            if node['level'] == level and self._is_square(graph, node):  # TODO check if nodes.h are correct etc
                return node
        return None

    def apply(self, graph: HyperGraph):
        return 

    # TODO move to hypergraph.py
    @classmethod
    def _is_square(cls, graph, node):
        neighbours = graph.get_neighbours(node)
        if len(neighbours) != 4:
            return False  # Not enough nodes to form a square

            # Check if all nodes are connected to exactly two others in the given set
        for node in neighbours:
            neighbors = set(graph.nx_graph.neighbors(node))
            shared_neighbors = neighbors.intersection(neighbours)
            if len(shared_neighbors) != 2:
                return False  # A node doesn't have exactly two connections in this set

            # Check for a cycle: Ensure that there are exactly 4 edges between these 4 nodes
        edges = list(combinations(neighbours, 2))
        edge_count = sum(1 for u, v in edges if graph.nx_graph.has_edge(u, v))
        return edge_count == 4
