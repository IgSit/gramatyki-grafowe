import unittest
from graph.hypergraph import HyperGraph
from productions.p4 import P4
import networkx as nx

class TestP4(unittest.TestCase):
    def test(self):
        # given
        hyper_graph1 = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0), "h": False}),
                ("v2", {"pos": (4, 0), "h": False}),
                ("v3", {"pos": (4, 4), "h": False}),
                ("v4", {"pos": (0, 4), "h": False}),
                ("v5", {"pos": (4, 2), "h": True}),
                ("v6", {"pos": (0, 2), "h": True}),
            ],
            edges=[
                ({"v1", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v3"}, {"label": "E", "B": True}),
                ({"v3", "v4"}, {"label": "E", "B": True}),
                ({"v4", "v6"}, {"label": "E", "B": True}),
                ({"v6", "v1"}, {"label": "E", "B": True}),
                ({"v1", "v2", "v3", "v4"}, {"label": "Q", "R": True})
            ]
        )

        # when
        production = P4()
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
                ("v6", {"pos": (0, 2), "h": False}),
                ("v7", {"pos": (2, 0), "h": False}),
                ("v8", {"pos": (2, 4), "h": False}),
                ("v9", {"pos": (2, 2), "h": False}),
            ],
            edges=[
                ({"v1", "v7"}, {"label": "E", "B": True}),
                ({"v7", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v3"}, {"label": "E", "B": True}),
                ({"v3", "v8"}, {"label": "E", "B": True}),
                ({"v8", "v4"}, {"label": "E", "B": True}),
                ({"v4", "v6"}, {"label": "E", "B": True}),
                ({"v6", "v1"}, {"label": "E", "B": True}),
                ({"v6", "v9"}, {"label": "E", "B": True}),
                ({"v7", "v9"}, {"label": "E", "B": True}),
                ({"v5", "v9"}, {"label": "E", "B": True}),
                ({"v8", "v9"}, {"label": "E", "B": True}),
                ({"v1", "v7", "v9", "v6"}, {"label": "Q", "B": True}),
                ({"v7", "v2", "v5", "v9"}, {"label": "Q", "B": True}),
                ({"v9", "v5", "v3", "v8"}, {"label": "Q", "B": True}),
                ({"v6", "v9", "v8", "v4"}, {"label": "Q", "B": True}),
            ]
        )

        self.assertTrue(
             nx.is_isomorphic(hyper_graph1.nx_graph, expected_graph.nx_graph)
        )
