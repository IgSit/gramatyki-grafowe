import networkx as nx
from networkx.algorithms import isomorphism

from productions.p1 import P1
from graph.hypergraph import HyperGraph


class P9(P1):
    """
    As it turns out P9 is in fact really similar to P1.
    """
    def __init__(self):
        super().__init__()
        self.left_side_graph = HyperGraph(
            nodes=[
                ('a', {'pos': (0, 0)}),
                ('b', {'pos': (0, 0)}),
                ('c', {'pos': (0, 0)}),
                ('d', {'pos': (0, 0)}),
                ('e', {'pos': (0, 0)}),
                ('f', {'pos': (0, 0)}),
            ],
            edges=[
                ({'a', 'b'}, {}),
                ({'b', 'c'}, {}),
                ({'c', 'd'}, {}),
                ({'d', 'e'}, {}),
                ({'e', 'f'}, {}),
                ({'f', 'a'}, {}),
                ({'a', 'b', 'c', 'd', 'e', 'f'}, {}),
            ]
        )

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        neighbours = graph.get_neighbours(hyper_node)
        return self._is_hexagon(graph, hyper_node, neighbours) and self._predicate(graph, hyper_node, neighbours)

    def _is_hexagon(self, graph: HyperGraph, hyper_node: str, neighbours: list[str]) -> bool:
        subgraph = nx.subgraph(graph.nx_graph, (*neighbours, hyper_node))
        return isomorphism.GraphMatcher(subgraph, self.left_side_graph.nx_graph).is_isomorphic()
