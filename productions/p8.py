import networkx as nx
from networkx.algorithms import isomorphism
import itertools

from productions.production import Production
from graph.hypergraph import HyperGraph


class P8(Production):
    def __init__(self):
        super().__init__()

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        hyper_edge = set(graph.get_neighbours(hyper_node))
        if graph.is_breakable(hyper_node) or len(hyper_edge) != 4:
            return False

        edges = {frozenset(k): v for k, v in graph.edges}

        hanging_to_check = []
        for v1, v2 in itertools.combinations(hyper_edge, 2):
            if frozenset({v1, v2}) in edges:
                continue
            for v3 in graph.get_neighbours(v1):
                if not v3 in hyper_edge and not graph.is_hyper_node(v3) and  graph.is_hanging_node(v3) and frozenset({v2, v3}) in edges:
                    hanging_to_check.append((v1, v2, v3))
        if len(hanging_to_check) == 0:
            return False

        for hn in graph.hyper_nodes:
            he = set(graph.get_neighbours(hn))
            if hyper_edge == he or len(he) != 4 or not graph.is_breakable(hn):
                continue
            for v1, v2, vh in hanging_to_check:
                if {v1, vh}.issubset(he) or {v2, vh}.issubset(he):
                    return True
        return False


    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        graph.change_label(hyper_node, {"R": True})
        return graph
    