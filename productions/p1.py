from itertools import combinations
import networkx as nx
from networkx.algorithms import isomorphism

from productions.production import Production
from graph.hypergraph import HyperGraph


class P1(Production):
    def __init__(self):
        super().__init__()
        self.left_side_graph = HyperGraph(
            nodes=[
                ('a', {'pos': (0, 0)}),
                ('b', {'pos': (0, 0)}),
                ('c', {'pos': (0, 0)}),
                ('d', {'pos': (0, 0)})
            ],
            edges=[
                ({'a', 'b'}, {}),
                ({'b', 'c'}, {}),
                ({'c', 'd'}, {}),
                ({'a', 'd'}, {}),
                ({'a', 'b', 'c', 'd'}, {})
            ]
        )

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        neighbours = graph.get_neighbours(hyper_node)
        return self._is_square(graph, hyper_node, neighbours) and self._predicate(graph, hyper_node, neighbours)

    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        neighbours = tuple(graph.get_neighbours(hyper_node))
        subgraph_edges = tuple(nx.subgraph(graph.nx_graph, neighbours).edges)
        graph.shrink(nodes=[], edges=[
            set(neighbours), # remove hyperedge
            *(set(edge) for edge in subgraph_edges) # remove other edges
        ])
        new_nodes_pos = [graph.calculate_mean_node_position(edge) for edge in subgraph_edges] + [graph.calculate_mean_node_position(neighbours)]
        new_nodes = list(map(lambda x: (f'a{x}', {'pos':x, 'h':False}), new_nodes_pos))
        graph.extend(
            nodes=new_nodes, 
            edges=[] # TODO: create new edges
        )
        return graph

    def _predicate(self, graph: HyperGraph, hyper_node: str, neighbours: list[str]):
        return graph.is_breakable(hyper_node) and all(not graph.is_hanging_node(neighbour) for neighbour in neighbours)

    def _is_square(self, graph: HyperGraph, hyper_node: str, neighbours: list[str]) -> bool:
        subgraph = nx.subgraph(graph.nx_graph, (*neighbours, hyper_node))
        return isomorphism.GraphMatcher(subgraph, self.left_side_graph.nx_graph).is_isomorphic()
