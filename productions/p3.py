import networkx as nx
from networkx.algorithms import isomorphism
import itertools

from productions.production import Production
from graph.hypergraph import HyperGraph


class P3(Production):
    def __init__(self):
        super().__init__()
        self.left_side_graph = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0)}),
                ("v2", {"pos": (0, 0)}),
                ("v3", {"pos": (0, 0)}),
                ("v4", {"pos": (0, 0)}),
                ("v5", {"pos": (0, 0)}),
                ("v6", {"pos": (0, 0)})
            ],
            edges=[
                ({"v1", "v6"}, {}),
                ({"v6", "v2"}, {}),
                ({"v2", "v5"}, {}),
                ({"v5", "v3"}, {}),
                ({"v3", "v4"}, {}),
                ({"v4", "v1"}, {}),
                ({"v1", "v2", "v3", "v4"}, {})
            ]
        )

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        neighbours = list(graph.get_neighbours(hyper_node))

        neighbours2 = []
        for n1, n2 in itertools.combinations(neighbours, 2):
            for v in nx.common_neighbors(graph.nx_graph, n1, n2):
                if graph.is_hyper_node(v):
                    continue
                if v in neighbours:
                    continue
                neighbours2.append(v)

        if len(neighbours2) != 2:
            return False

        if not (graph.is_breakable(hyper_node) and \
            all(not graph.is_hanging_node(n) for n in neighbours) and \
            all(graph.is_hanging_node(n) for n in neighbours2)):
            return False

        subgraph = nx.subgraph(graph.nx_graph, (*neighbours, *neighbours2, hyper_node))
        return isomorphism.GraphMatcher(subgraph, self.left_side_graph.nx_graph).is_isomorphic()

    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        neighbours = list(graph.get_neighbours(hyper_node))

        neighbours2 = []
        for n1, n2 in itertools.combinations(neighbours, 2):
            for v in nx.common_neighbors(graph.nx_graph, n1, n2):
                if graph.is_hyper_node(v):
                    continue
                if v in neighbours:
                    continue
                neighbours2.append(v)

        neighbours2.sort()
        v5, v6 = neighbours2[0], neighbours2[1]
        v2 = list(nx.common_neighbors(graph.nx_graph, v5, v6))[0]

        v1 = [n for n in nx.common_neighbors(graph.nx_graph, v6, hyper_node) if n != v2][0]
        v3 = [n for n in nx.common_neighbors(graph.nx_graph, v5, hyper_node) if n != v2][0]
        v4 = [n for n in nx.common_neighbors(graph.nx_graph, v1, v3) if n != hyper_node][0]

        pos = graph.calculate_mean_node_position((v1, v4))
        v14 = (f"v{pos}", {"pos": pos})
        pos = graph.calculate_mean_node_position((v3, v4))
        v34 = (f"v{pos}", {"pos": pos})
        pos = graph.calculate_mean_node_position((v1, v2, v3, v4))
        v1234 = (f"v{pos}", {"pos": pos})

        e_v1_v14 = ({v1, v14[0]}, {"B": graph.is_on_border((v1, v4))})
        e_v14_v4 = ({v14[0], v4}, {"B": graph.is_on_border((v1, v4))})
        e_v4_v34 = ({v4, v34[0]}, {"B": graph.is_on_border((v3, v4))})
        e_v34_v3 = ({v34[0], v3}, {"B": graph.is_on_border((v3, v4))})

        e_v11_v1234 = ({v14[0], v1234[0]}, {})
        e_v34_v1234 = ({v34[0], v1234[0]}, {})
        e_v5_v1234 = ({v5, v1234[0]}, {})
        e_v6_v1234 = ({v6, v1234[0]}, {})

        graph.set_node_attrs(v5, {"h": False})
        graph.set_node_attrs(v6, {"h": False})

        graph.shrink(
            nodes=[],
            edges=[
                {v1, v4},
                {v4, v3},
                neighbours  # remove hyperedge
            ]
        )

        graph.extend(
            nodes=[v14, v34, v1234],
            edges=[
                e_v1_v14,
                e_v14_v4,
                e_v4_v34,
                e_v34_v3,

                e_v11_v1234,
                e_v34_v1234,
                e_v5_v1234,
                e_v6_v1234,

                # hiper edges
                ({v1, v6, v1234[0], v14[0]}, {"R": False}),
                ({v14[0], v1234[0], v34[0], v4}, {"R": False}),
                ({v1234[0], v5, v3, v34[0]}, {"R": False}),
                ({v6, v2, v5, v1234[0]}, {"R": False})
            ]
        )

        return graph
