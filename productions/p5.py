import networkx as nx
from networkx.algorithms import isomorphism
import itertools

from productions.production import Production
from graph.hypergraph import HyperGraph


class P5(Production):
    def __init__(self):
        super().__init__()
        self.left_side_graph = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0)}),
                ("v2", {"pos": (0, 0)}),
                ("v3", {"pos": (0, 0)}),
                ("v4", {"pos": (0, 0)}),
                ("v5", {"pos": (0, 0)}),
                ("v6", {"pos": (0, 0)}),
                ("v7", {"pos": (0, 0)}),
            ],
            edges=[
                ({"v1", "v6"}, {}),
                ({"v6", "v2"}, {}),
                ({"v2", "v5"}, {}),
                ({"v5", "v3"}, {}),
                ({"v3", "v4"}, {}),
                ({"v4", "v7"}, {}),
                ({"v7", "v1"}, {}),
                ({"v1", "v2", "v3", "v4"}, {}),
            ]
        )

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        neighbours = list(graph.get_neighbours(hyper_node))

        if len(neighbours) != 4:
            return False

        hanging_nodes = []

        for n1, n2 in itertools.combinations(neighbours, 2):
            for v in nx.common_neighbors(graph.nx_graph, n1, n2):
                if graph.is_hyper_node(v) or v in neighbours:
                    continue
                if (graph.calculate_mean_node_position((n1, n2)) != graph.nx_graph.nodes[v]["pos"]):
                    continue
                hanging_nodes.append(v)

        if len(hanging_nodes) != 3:
            return False
        
        if not (graph.is_breakable(hyper_node)) or \
            any(graph.is_hanging_node(n) for n in neighbours) or \
            any(not graph.is_hanging_node(n) for n in hanging_nodes):
            return False
        
        subgraph = nx.subgraph(graph.nx_graph, (*neighbours, *hanging_nodes, hyper_node))

        return isomorphism.GraphMatcher(subgraph, self.left_side_graph.nx_graph).is_isomorphic()


    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        neighbours = list(graph.get_neighbours(hyper_node))

        hanging_nodes = []

        for n1, n2 in itertools.combinations(neighbours, 2):
            for v in nx.common_neighbors(graph.nx_graph, n1, n2):
                if graph.is_hyper_node(v) or v in neighbours:
                    continue
                if (graph.calculate_mean_node_position((n1, n2)) != graph.nx_graph.nodes[v]["pos"]):
                    continue
                hanging_nodes.append(v)
                
        hanging_nodes.sort()

        for n1, n2 in itertools.combinations(neighbours, 2):
            if not graph.nx_graph.has_edge(n1, n2):
                continue
    
            common_neighbors = list(nx.common_neighbors(graph.nx_graph, n1, n2))
            valid_neighbors = [
                node for node in common_neighbors 
                if node not in hanging_nodes and not graph.is_hyper_node(node)
            ]
            if not valid_neighbors:
                v3, v4 = sorted([n1, n2])
                break

        used_nodes = {v3, v4}
            
        v7 = next(
            n for n in hanging_nodes if n not in used_nodes and graph.nx_graph.has_edge(n, v4)
        )

        used_nodes.add(v7)
    
        v5 = next(
            n for n in hanging_nodes if n not in used_nodes and graph.nx_graph.has_edge(n, v3)
        )

        used_nodes.add(v5)
    
        v1 = next(
            n for n in neighbours if n not in used_nodes and graph.nx_graph.has_edge(n, v7)
        )

        used_nodes.add(v1)
    
        v2 = next(
            n for n in neighbours if n not in used_nodes and graph.nx_graph.has_edge(n, v5)
        )
    
        used_nodes.add(v2)

        v6 = next(
            n for n in hanging_nodes if n not in used_nodes and graph.nx_graph.has_edge(n, v1) and graph.nx_graph.has_edge(n, v2)
        )


        e_v4_v3_b = graph.nx_graph.get_edge_data(v4, v3)["B"]

        # New nodes

        v43_pos = graph.calculate_mean_node_position((v4, v3))
        v43 = (f"v{v43_pos}", {"pos": v43_pos, "h" : not e_v4_v3_b})

        v1234_pos = graph.calculate_mean_node_position((v1, v2, v3, v4))
        v1234 = (f"v{v1234_pos}", {"pos": v1234_pos})

        # New edges

        e_v4_v43 = ({v4, v43[0]}, {"B": e_v4_v3_b})
        e_v43_v3 = ({v43[0], v3}, {"B": e_v4_v3_b})

        e_v7_v1234 = ({v7, v1234[0]}, {"B": False})
        e_v6_v1234 = ({v6, v1234[0]}, {"B": False})
        e_v5_v1234 = ({v5, v1234[0]}, {"B": False})
        e_v43_v1234 = ({v43[0], v1234[0]}, {"B": False})

        # New hyperedges

        e_v1_v6_v7_v1234 = ({v1, v6, v7, v1234[0]}, {"R": False})
        e_v6_v2_v5_v1234 = ({v6, v2, v5, v1234[0]}, {"R": False})
        e_v5_v3_v43_v1234 = ({v5, v3, v43[0], v1234[0]}, {"R": False})
        e_v4_v43_v1234_v7 = ({v4, v43[0], v1234[0], v7}, {"R": False})

        # Update node attributes

        graph.set_node_attrs(v5, {"h": False})
        graph.set_node_attrs(v6, {"h": False})
        graph.set_node_attrs(v7, {"h": False})


        graph.shrink(
            nodes=[],
            edges=[
                (v4, v3),
                neighbours
            ]
        )

        graph.extend(
            nodes=[
                v43,
                v1234
            ],
            edges=[
                e_v4_v43,
                e_v43_v3,
                e_v7_v1234,
                e_v6_v1234,
                e_v5_v1234,
                e_v43_v1234,
                e_v1_v6_v7_v1234,
                e_v6_v2_v5_v1234,
                e_v5_v3_v43_v1234,
                e_v4_v43_v1234_v7
            ]
        )


        return graph