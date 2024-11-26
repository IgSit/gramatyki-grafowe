import networkx as nx
from networkx.algorithms import isomorphism

from productions.production import Production
from productions.p1 import P1
from graph.hypergraph import HyperGraph


class P9(P1):
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

    # TODO: verify if P9 production is really so similar to P1 and can inherit from its class

    # def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
    #     neighbours = tuple(graph.get_neighbours(hyper_node))
    #     subgraph_edges = tuple(nx.subgraph(graph.nx_graph, neighbours).edges)
    #     new_nodes_pos = [(edge, graph.calculate_mean_node_position(edge)) for edge in subgraph_edges]
    #     middle_node_pos = graph.calculate_mean_node_position(neighbours)
    #     new_nodes_ids = list(map(lambda x: f'a{x[1]}', new_nodes_pos))
    #     middle_node_id = 'a' + str(middle_node_pos)
    #     helper_dict = {n:{n, middle_node_id} for n in neighbours}
    #     for i, (edge, _) in enumerate(new_nodes_pos):
    #         for v in edge:
    #             helper_dict[v].add(new_nodes_ids[i])
    #     inner_edges = [({new_node, middle_node_id}, {'label': 'E', 'B': False}) for new_node in new_nodes_ids]
    #     outer_edges = [({v, new_nodes_ids[i]}, {'label': 'E', 'B': graph.nx_graph.edges[*edge]['B']}) for i, edge in enumerate(subgraph_edges) for v in edge]
    #     hyper_edges = list(map(lambda x: (x, {'label': 'Q', 'R': False}), helper_dict.values()))
    #     new_nodes = list(zip(new_nodes_ids, map(lambda x: {'pos':x[1], 'h':graph.nx_graph.edges[*x[0]]['B']}, new_nodes_pos))) + [(middle_node_id, {'pos':middle_node_pos, 'h':False})]
        
    #     graph.shrink(nodes=[], edges=[
    #         set(neighbours), # remove hyperedge
    #         *(set(edge) for edge in subgraph_edges) # remove other edges
    #     ])
    #     graph.extend(
    #         nodes=new_nodes,
    #         edges=inner_edges + outer_edges + hyper_edges
    #     )
    #     return graph

    # def _predicate(self, graph: HyperGraph, hyper_node: str, neighbours: list[str]):
    #     return graph.is_breakable(hyper_node) and all(not graph.is_hanging_node(neighbour) for neighbour in neighbours)

    def _is_hexagon(self, graph: HyperGraph, hyper_node: str, neighbours: list[str]) -> bool:
        subgraph = nx.subgraph(graph.nx_graph, (*neighbours, hyper_node))
        return isomorphism.GraphMatcher(subgraph, self.left_side_graph.nx_graph).is_isomorphic()
