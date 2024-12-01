import unittest
import networkx as nx
from graph.hypergraph import HyperGraph
from productions.p3 import P3

class TestP3(unittest.TestCase):
    def test(self):
        # given
        hyper_graph1 = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0), "h": False}),
                ("v2", {"pos": (4, 0), "h": False}),
                ("v3", {"pos": (4, 4), "h": False}),
                ("v4", {"pos": (0, 4), "h": False}),
                ("v5", {"pos": (4, 2), "h": True}),
                ("v6", {"pos": (2, 0), "h": True}),
            ],
            edges=[
                ({"v1", "v6"}, {"label": "E", "B": False}),
                ({"v6", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v3"}, {"label": "E", "B": True}),
                ({"v3", "v4"}, {"label": "E", "B": True}),
                ({"v4", "v1"}, {"label": "E", "B": True}),
                ({"v1", "v2", "v3", "v4"}, {"label": "Q", "R": True})
            ]
        )

        # when
        production = P3()
        for hyper_node in hyper_graph1.hyper_nodes:
            if production.check(hyper_graph1, hyper_node):
                hyper_graph1 = production.apply(hyper_graph1, hyper_node)

        # then
        expected_graph = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0), "h": False}),
                ("v2", {"pos": (4, 0), "h": False}),
                ("v3", {"pos": (4, 4), "h": False}),
                ("v4", {"pos": (0, 4), "h": False}),
                ("v5", {"pos": (4, 2), "h": False}),
                ("v6", {"pos": (2, 0), "h": False}),
                ("v7", {"pos": (2, 4), "h": False}),
                ("v8", {"pos": (0, 2), "h": False}),
                ("v9", {"pos": (2, 2), "h": False}),
            ],
            edges=[
                ({"v1", "v6"}, {"label": "E", "B": True}),
                ({"v6", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v3"}, {"label": "E", "B": True}),
                ({"v3", "v7"}, {"label": "E", "B": True}),
                ({"v7", "v4"}, {"label": "E", "B": True}),
                ({"v4", "v8"}, {"label": "E", "B": True}),
                ({"v8", "v1"}, {"label": "E", "B": True}),
                ({"v6", "v9"}, {"label": "E", "B": True}),
                ({"v5", "v9"}, {"label": "E", "B": True}),
                ({"v7", "v9"}, {"label": "E", "B": True}),
                ({"v8", "v9"}, {"label": "E", "B": True}),
                ({"v1", "v6", "v9", "v8"}, {"label": "Q", "B": True}),
                ({"v6", "v2", "v5", "v9"}, {"label": "Q", "B": True}),
                ({"v9", "v5", "v3", "v7"}, {"label": "Q", "B": True}),
                ({"v8", "v9", "v7", "v4"}, {"label": "Q", "B": True}),
            ]
        )

        self.assertTrue(
             nx.is_isomorphic(hyper_graph1.nx_graph, expected_graph.nx_graph)
        )

    def test2(self):
        # given
        
        hyper_graph = HyperGraph(
            nodes=[
                ("v1", {"pos": (1, 1), "h": False}),
                ("v2", {"pos": (2, 1), "h": False}),
                ("v3", {"pos": (3, 1), "h": False}),
                ("v4", {"pos": (4, 1), "h": False}),
                ("v5", {"pos": (5, 1), "h": False}),
                ("v6", {"pos": (5, 2), "h": False}),
                ("v7", {"pos": (5, 3), "h": False}),
                ("v8", {"pos": (5, 4), "h": False}),
                ("v9", {"pos": (5, 5), "h": False}),
                ("v10", {"pos": (4, 5), "h": False}),
                ("v11", {"pos": (3, 5), "h": False}),
                ("v12", {"pos": (1, 5), "h": False}),
                ("v13", {"pos": (1, 3), "h": False}),
                ("v14", {"pos": (3, 2), "h": False}),
                ("v15", {"pos": (4, 2), "h": False}),
                ("v16", {"pos": (4, 3), "h": False}),
                ("v17", {"pos": (4, 4), "h": False}),
                ("v18", {"pos": (3, 4), "h": True}),
                ("v19", {"pos": (2, 3), "h": True}),
                ("v20", {"pos": (3, 3), "h": False}),
            ],
            edges=[ # TODO breakable or not
                ({"v1", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v3"}, {"label": "E", "B": True}),
                ({"v3", "v4"}, {"label": "E", "B": True}),
                ({"v4", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v6"}, {"label": "E", "B": True}),
                ({"v6", "v7"}, {"label": "E", "B": True}),
                ({"v7", "v8"}, {"label": "E", "B": True}),
                ({"v8", "v9"}, {"label": "E", "B": True}),
                ({"v9", "v10"}, {"label": "E", "B": True}),
                ({"v10", "v11"}, {"label": "E", "B": True}),
                ({"v11", "v12"}, {"label": "E", "B": True}),
                ({"v12", "v13"}, {"label": "E", "B": True}),
                ({"v13", "v1"}, {"label": "E", "B": True}),
                ({"v14", "v15"}, {"label": "E", "B": False}),
                ({"v15", "v16"}, {"label": "E", "B": False}),
                ({"v16", "v17"}, {"label": "E", "B": False}),
                ({"v17", "v18"}, {"label": "E", "B": False}),
                ({"v19", "v20"}, {"label": "E", "B": False}),
                ({"v18", "v20"}, {"label": "E", "B": False}),
                ({"v19", "v2"}, {"label": "E", "B": False}),
                ({"v14", "v3"}, {"label": "E", "B": False}),
                ({"v15", "v4"}, {"label": "E", "B": False}),
                ({"v20", "v14"}, {"label": "E", "B": False}),
                ({"v13", "v19"}, {"label": "E", "B": False}),
                ({"v11", "v18"}, {"label": "E", "B": False}),
                ({"v10", "v17"}, {"label": "E", "B": False}),
                ({"v20", "v16"}, {"label": "E", "B": False}),
                ({"v15", "v6"}, {"label": "E", "B": False}),
                ({"v16", "v7"}, {"label": "E", "B": False}),
                ({"v17", "v8"}, {"label": "E", "B": False}),
                ({"v13", "v20", "v11", "v12"}, {"label": "Q", "R": True})
            ],
        )

        hyper_graph.visualize()

        production = P3()
        for hyper_node in hyper_graph.hyper_nodes:
            if production.check(hyper_graph, hyper_node):
                hyper_graph = production.apply(hyper_graph, hyper_node)

        hyper_graph.visualize()
        
