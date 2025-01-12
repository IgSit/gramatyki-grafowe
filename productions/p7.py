import networkx as nx
from networkx.algorithms import isomorphism
import itertools

from productions.production import Production
from graph.hypergraph import HyperGraph


class P7(Production):
    def __init__(self):
        super().__init__()

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        if graph.is_breakable(hyper_node):
            return False
        neighbours = list(graph.get_neighbours(hyper_node))
        return len(neighbours) == 4

    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        graph.set_node_attrs(hyper_node, {"label": "Q", "R": True})
        return graph
