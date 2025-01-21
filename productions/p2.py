import networkx as nx
from networkx.algorithms import isomorphism

from productions.production import Production
from graph.hypergraph import HyperGraph


class P2(Production):
    def __init__(self):
        super().__init__()
        self.hanging_node = None

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        neighbours = list(graph.get_neighbours(hyper_node))
        return self._is_square_with_hanging_node(graph, hyper_node, neighbours) and self._predicate(graph, hyper_node, neighbours)

    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        neighbours = tuple(graph.get_neighbours(hyper_node))
        subgraph_edges = tuple(nx.subgraph(graph.nx_graph, neighbours).edges)
        new_nodes_pos = [(edge, graph.calculate_mean_node_position(edge)) for edge in subgraph_edges]
        middle_node_pos = graph.calculate_mean_node_position(neighbours)
        new_nodes_ids = list(map(lambda x: f'a{x[1]}', new_nodes_pos))
        middle_node_id = 'a' + str(middle_node_pos)
        helper_dict = {n:{n, middle_node_id} for n in neighbours}
        for i, (edge, _) in enumerate(new_nodes_pos):
            for v in edge:
                helper_dict[v].add(new_nodes_ids[i])
        for h in tuple(helper_dict.values()):
            if len(h) == 3:
                h.add(self.hanging_node)
        inner_edges = [({new_node, middle_node_id}, {'label': 'E', 'B': False}) for new_node in new_nodes_ids] + [({self.hanging_node, middle_node_id}, {'label': 'E', 'B': False})]
        outer_edges = [({v, new_nodes_ids[i]}, {'label': 'E', 'B': graph.nx_graph.edges[*edge]['B']}) for i, edge in enumerate(subgraph_edges) for v in edge]
        hyper_edges = list(map(lambda x: (x, {'label': 'Q', 'R': False}), helper_dict.values()))
        new_nodes = list(zip(new_nodes_ids, map(lambda x: {'pos':x[1], 'h': not graph.nx_graph.edges[*x[0]]['B']}, new_nodes_pos))) + [(middle_node_id, {'pos':middle_node_pos, 'h':False})]
        
        graph.shrink(nodes=[], edges=[
            set(neighbours), # remove hyperedge
            *(set(edge) for edge in subgraph_edges) # remove other edges
        ])
        graph.extend(
            nodes=new_nodes,
            edges=inner_edges + outer_edges + hyper_edges
        )
        graph.nx_graph.nodes[self.hanging_node]['h'] = False
        hanging_node, attr = tuple(filter(lambda x: x[0] == self.hanging_node, graph.nodes))[0]
        attr['h'] = False
        return graph

    def _predicate(self, graph: HyperGraph, hyper_node: str, neighbours: list[str]):
        return graph.is_breakable(hyper_node) and all(not graph.is_hanging_node(neighbour) for neighbour in neighbours)

    def _is_square_with_hanging_node(self, graph: HyperGraph, hyper_node: str, neighbours: list[str]) -> bool:
        subgraph = nx.subgraph(graph.nx_graph, neighbours)
        if (len(tuple(subgraph.edges)) != 3):
            return False
        end_nodes = tuple(filter(lambda node: len(tuple(subgraph.neighbors(node))) == 1, subgraph.nodes))
        if len(end_nodes) != 2:
            return False
        u, v = end_nodes
        candidates_u = set(filter(lambda x: x != hyper_node and x not in neighbours and graph.is_hanging_node(x), graph.nx_graph.neighbors(u)))
        candidates_v = set(filter(lambda x: x != hyper_node and x not in neighbours and graph.is_hanging_node(x), graph.nx_graph.neighbors(v)))
        for c_u in candidates_u:
            if c_u in candidates_v:
                self.hanging_node = c_u
                return True
        return False