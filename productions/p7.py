import networkx as nx
from networkx.algorithms import isomorphism
import itertools

from productions.production import Production
from graph.hypergraph import HyperGraph


class P7(Production):
    def __init__(self):
        super().__init__()
        self.left_side_graph = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0)}),
                ("v2", {"pos": (0, 0)}),
                ("v3", {"pos": (0, 0)}),
                ("v4", {"pos": (0, 0)})
            ],
            edges=[
                ({"v1", "v2", "v3", "v4"}, {})
            ]
        )

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        neighbours = list(graph.get_neighbours(hyper_node))

        if graph.is_breakable(hyper_node):
            return False

        subgraph = nx.subgraph(graph.nx_graph, (*neighbours, hyper_node))
        return isomorphism.GraphMatcher(subgraph, self.left_side_graph.nx_graph).is_isomorphic()

    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        graph.set_node_attrs(hyper_node, {"label": "Q", "R": True})
        return graph
