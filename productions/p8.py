import networkx as nx
from networkx.algorithms import isomorphism
import itertools

from productions.production import Production
from graph.hypergraph import HyperGraph


class P8(Production):
    def __init__(self):
        super().__init__()
        self.small_hyper_node = None
        self.big_hyper_node = None

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        def process_hyper_node(check_func, graph, node, opposite_check):
            check_func(graph, node)
            if opposite_check(graph, hyper_node):
                self._reset_hyper_nodes()
                return True
            self._reset_hyper_nodes()
            return False
    
        hyper_nodes = [node for node in graph.hyper_nodes if node != hyper_node]
    
        if graph.is_breakable(hyper_node):
            for hn in hyper_nodes:
                if process_hyper_node(self._check_big_hyper_node, graph, hn, self._check_small_hyper_node):
                    return True
        else:
            for hn in hyper_nodes:
                if process_hyper_node(self._check_small_hyper_node, graph, hn, self._check_big_hyper_node):
                    return True
    
        self._reset_hyper_nodes()
        return False



    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        hyper_nodes = [node for node in graph.hyper_nodes if node != hyper_node]

        if graph.is_breakable(hyper_node):
            for hn in hyper_nodes:
                self._check_big_hyper_node(graph, hn)

                if self.big_hyper_node is not None:
                    if self._check_small_hyper_node(graph, hyper_node):
                        break
                    else:
                        self.big_hyper_node = None
                        self.small_hyper_node = None
        else:
            for hn in hyper_nodes:
                self._check_small_hyper_node(graph, hn)

                if self.small_hyper_node is not None:
                    if self._check_big_hyper_node(graph, hyper_node):
                        break
                    else:
                        self.small_hyper_node = None
                        self.big_hyper_node = None

        if self.small_hyper_node is None or self.big_hyper_node is None:
            return graph

        neighbours = list(graph.get_neighbours(self.big_hyper_node))

        new_hyper_node = (neighbours, {"label": "Q", "R": True})

        graph.shrink(
            nodes=[],
            edges=[
                neighbours
            ]
        )

        graph.extend(
            nodes=[],
            edges=[
                new_hyper_node
            ]
        )

        self._reset_hyper_nodes()
        return graph
    
    def _check_small_hyper_node(self, graph: HyperGraph, hyper_node: str) -> bool:
        neighbours = list(graph.get_neighbours(hyper_node))

        if len(neighbours) != 4:
            return False
    
        if self.big_hyper_node is None:
            contains_edge_with_hanging_v = False

            for n1, n2 in itertools.combinations(neighbours, 2):
                if graph.nx_graph.has_edge(n1, n2) and (graph.is_hanging_node(n1) or graph.is_hanging_node(n2)):
                    contains_edge_with_hanging_v = True
                    break

            if contains_edge_with_hanging_v:
                self.small_hyper_node = hyper_node
            
            return False
        else:
            big_neighbours = list(graph.get_neighbours(self.big_hyper_node))

            for n1, n2 in itertools.combinations(big_neighbours, 2):
                for v in nx.common_neighbors(graph.nx_graph, n1, n2):
                    if graph.is_hyper_node(v) or v in big_neighbours:
                        continue
                    if graph.calculate_mean_node_position((n1, n2)) != graph.nx_graph.nodes[v]["pos"]:
                        continue
                    if v in neighbours and graph.is_hanging_node(v):
                        self.small_hyper_node = hyper_node
                        return True
                    
            return False
            
    def _check_big_hyper_node(self, graph: HyperGraph, hyper_node: str) -> bool:
        neighbours = list(graph.get_neighbours(hyper_node))

        if len(neighbours) != 4:
            return False
    
        if self.small_hyper_node is None:
            contains_edge_with_hanging_v = False

            for n1, n2 in itertools.combinations(neighbours, 2):
                for v in nx.common_neighbors(graph.nx_graph, n1, n2):
                    if graph.is_hyper_node(v) or v in neighbours:
                        continue
                    if graph.calculate_mean_node_position((n1, n2)) != graph.nx_graph.nodes[v]["pos"]:
                        continue
                    if graph.is_hanging_node(v):
                        contains_edge_with_hanging_v = True
                        break

            if contains_edge_with_hanging_v:
                self.big_hyper_node = hyper_node

            return False
        else:
            small_neighbours = list(graph.get_neighbours(self.small_hyper_node))

            for n1, n2 in itertools.combinations(neighbours, 2):
                for v in nx.common_neighbors(graph.nx_graph, n1, n2):
                    if graph.is_hyper_node(v) or v in neighbours:
                        continue
                    if graph.calculate_mean_node_position((n1, n2)) != graph.nx_graph.nodes[v]["pos"]:
                        continue
                    if v in small_neighbours and graph.is_hanging_node(v):
                        self.big_hyper_node = hyper_node
                        return True
            
            return False
        
    def _reset_hyper_nodes(self):
        self.small_hyper_node = None
        self.big_hyper_node = None
    