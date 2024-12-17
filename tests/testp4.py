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

    def test2(self):
        # given
        hyper_graph1 = HyperGraph(
            nodes = [
                ("v1", {"pos": (0, 0), "h": False}),
                ("v2", {"pos": (1, 0), "h": False}),
                ("v3", {"pos": (2, 0), "h": False}),
                ("v4", {"pos": (4, 0), "h": False}),
                ("v5", {"pos": (5, 0), "h": False}),
                ("v6", {"pos": (6, 0), "h": False}),

                ("v7", {"pos": (6, 1), "h": False}),
                ("v8", {"pos": (5, 1), "h": False}),

                ("v9", {"pos": (4, 1), "h": True}),
                ("v10", {"pos": (2, 1), "h": True}),

                ("v11", {"pos": (1, 1), "h": False}),
                ("v12", {"pos": (0, 1), "h": False}),

                ("v13", {"pos": (0, 2), "h": False}),
                ("v14", {"pos": (1, 2), "h": False}),
                ("v15", {"pos": (2, 2), "h": False}),
                ("v16", {"pos": (4, 2), "h": False}),
                ("v17", {"pos": (5, 2), "h": False}),
                ("v18", {"pos": (6, 2), "h": False}),
            ],
            edges = [
                ({"v1", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v3"}, {"label": "E", "B": True}),
                ({"v3", "v4"}, {"label": "E", "B": True}),
                ({"v4", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v6"}, {"label": "E", "B": True}),

                ({"v7", "v8"}, {"label": "E", "B": False}),
                ({"v8", "v9"}, {"label": "E", "B": False}),
                ({"v10", "v11"}, {"label": "E", "B": False}),
                ({"v11", "v12"}, {"label": "E", "B": False}),

                ({"v13", "v14"}, {"label": "E", "B": True}),
                ({"v14", "v15"}, {"label": "E", "B": True}),
                ({"v15", "v16"}, {"label": "E", "B": True}),
                ({"v16", "v17"}, {"label": "E", "B": True}),
                ({"v17", "v18"}, {"label": "E", "B": True}),

                ({"v1", "v12"}, {"label": "E", "B": True}),
                ({"v2", "v11"}, {"label": "E", "B": False}),
                ({"v3", "v10"}, {"label": "E", "B": False}),
                ({"v4", "v9"}, {"label": "E", "B": False}),
                ({"v5", "v8"}, {"label": "E", "B": False}),
                ({"v6", "v7"}, {"label": "E", "B": True}),


                ({"v7", "v18"}, {"label": "E", "B": True}),
                ({"v8", "v17"}, {"label": "E", "B": False}),
                ({"v9", "v16"}, {"label": "E", "B": False}),
                ({"v10", "v15"}, {"label": "E", "B": False}),
                ({"v11", "v14"}, {"label": "E", "B": False}),
                ({"v12", "v13"}, {"label": "E", "B": True}),

                ({"v3", "v4", "v15", "v16"}, {"label": "Q", "R": True}),

                ({"v1", "v2", "v11", "v12"}, {"label": "Q", "R": True}),
                ({"v2", "v3", "v10", "v11"}, {"label": "Q", "R": True}),
                ({"v4", "v5", "v8", "v9"}, {"label": "Q", "R": True}),
                ({"v5", "v6", "v7", "v8"}, {"label": "Q", "R": True}),
                ({"v12", "v11", "v14", "v13"}, {"label": "Q", "R": True}),
                ({"v11", "v10", "v15", "v14"}, {"label": "Q", "R": True}),
                ({"v9", "v8", "v17", "v16"}, {"label": "Q", "R": True}),
                ({"v8", "v7", "v18", "v17"}, {"label": "Q", "R": True}),
            ],
        )

        hyper_graph1.visualize()
        self.assertTrue(True)

        # when
        production = P4()
        for hyper_node in hyper_graph1.hyper_nodes:
            if production.check(hyper_graph1, hyper_node):
                hyper_graph1 = production.apply(hyper_graph1, hyper_node)


        hyper_graph1.visualize()

        # then
        expected_graph = HyperGraph(
            nodes = [
                ("v1", {"pos": (0, 0), "h": False}),
                ("v2", {"pos": (1, 0), "h": False}),
                ("v3", {"pos": (2, 0), "h": False}),
                ("v4", {"pos": (4, 0), "h": False}),
                ("v5", {"pos": (5, 0), "h": False}),
                ("v6", {"pos": (6, 0), "h": False}),

                ("v7", {"pos": (6, 1), "h": False}),
                ("v8", {"pos": (5, 1), "h": False}),

                ("v9", {"pos": (4, 1), "h": True}),
                ("v10", {"pos": (2, 1), "h": True}),

                ("v11", {"pos": (1, 1), "h": False}),
                ("v12", {"pos": (0, 1), "h": False}),

                ("v13", {"pos": (0, 2), "h": False}),
                ("v14", {"pos": (1, 2), "h": False}),
                ("v15", {"pos": (2, 2), "h": False}),
                ("v16", {"pos": (4, 2), "h": False}),
                ("v17", {"pos": (5, 2), "h": False}),
                ("v18", {"pos": (6, 2), "h": False}),
                

                ("v19", {"pos": (3, 0), "h": False}),
                ("v20", {"pos": (3, 1), "h": False}),
                ("v21", {"pos": (3, 2), "h": False}),
            ],
            edges = [
                ({"v1", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v3"}, {"label": "E", "B": True}),
                ({"v4", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v6"}, {"label": "E", "B": True}),

                ({"v7", "v8"}, {"label": "E", "B": False}),
                ({"v8", "v9"}, {"label": "E", "B": False}),
                ({"v10", "v11"}, {"label": "E", "B": False}),
                ({"v11", "v12"}, {"label": "E", "B": False}),

                ({"v13", "v14"}, {"label": "E", "B": True}),
                ({"v14", "v15"}, {"label": "E", "B": True}),
                ({"v16", "v17"}, {"label": "E", "B": True}),
                ({"v17", "v18"}, {"label": "E", "B": True}),

                ({"v1", "v12"}, {"label": "E", "B": True}),
                ({"v2", "v11"}, {"label": "E", "B": False}),
                ({"v3", "v10"}, {"label": "E", "B": False}),
                ({"v4", "v9"}, {"label": "E", "B": False}),
                ({"v5", "v8"}, {"label": "E", "B": False}),
                ({"v6", "v7"}, {"label": "E", "B": True}),

                ({"v7", "v18"}, {"label": "E", "B": True}),
                ({"v8", "v17"}, {"label": "E", "B": False}),
                ({"v9", "v16"}, {"label": "E", "B": False}),
                ({"v10", "v15"}, {"label": "E", "B": False}),
                ({"v11", "v14"}, {"label": "E", "B": False}),
                ({"v12", "v13"}, {"label": "E", "B": True}),

                ({"v3", "v19"}, {"label": "E", "B": True}),
                ({"v19", "v4"}, {"label": "E", "B": True}),
                ({"v9", "v20"}, {"label": "E", "B": False}),
                ({"v20", "v10"}, {"label": "E", "B": False}),
                ({"v15", "v21"}, {"label": "E", "B": True}),
                ({"v21", "v16"}, {"label": "E", "B": True}),

                ({"v19", "v20"}, {"label": "E", "B": False}),
                ({"v20", "v21"}, {"label": "E", "B": False}),

                ({"v1", "v2", "v11", "v12"}, {"label": "Q", "R": True}),
                ({"v2", "v3", "v10", "v11"}, {"label": "Q", "R": True}),
                ({"v4", "v5", "v8", "v9"}, {"label": "Q", "R": True}),
                ({"v5", "v6", "v7", "v8"}, {"label": "Q", "R": True}),
                ({"v12", "v11", "v14", "v13"}, {"label": "Q", "R": True}),
                ({"v11", "v10", "v15", "v14"}, {"label": "Q", "R": True}),
                ({"v9", "v8", "v17", "v16"}, {"label": "Q", "R": True}),
                ({"v8", "v7", "v18", "v17"}, {"label": "Q", "R": True}),

                ({"v15", "v21", "v10", "v20"}, {"label": "Q", "R": False}),
                ({"v3", "v19", "v10", "v20"}, {"label": "Q", "R": False}),
                ({"v19", "v4", "v9", "v20"}, {"label": "Q", "R": False}),
                ({"v20", "v9", "v16", "v21"}, {"label": "Q", "R": False}),
            ],
        )

        # expected_graph.visualize()
        self.assertTrue(
             nx.is_isomorphic(hyper_graph1.nx_graph, expected_graph.nx_graph)
        )
