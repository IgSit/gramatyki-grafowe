import unittest
import networkx as nx
from productions.p3 import P3
from graph.hypergraph import HyperGraph

class TestP3(unittest.TestCase):
    def test(self, visualize=False):
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

    def test2(self, visualize=False):
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
                ("v21", {"pos": (1, 2), "h": False}),
                ("v22", {"pos": (2, 2), "h": False}),
            ],
            edges=[
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
                ({"v13", "v21"}, {"label": "E", "B": True}),
                ({"v21", "v1"}, {"label": "E", "B": True}),
                ({"v21", "v22"}, {"label": "E", "B": False}),
                ({"v22", "v14"}, {"label": "E", "B": False}),
                ({"v13", "v20", "v11", "v12"}, {"label": "Q", "R": True}),
                ({"v1", "v2", "v22", "v21"}, {"label": "Q", "R": False}),
                ({"v2", "v3", "v14", "v22"}, {"label": "Q", "R": False}),
                ({"v22", "v14", "v20", "v19"}, {"label": "Q", "R": False}),
                ({"v21", "v22", "v19", "v13"}, {"label": "Q", "R": False}),
                ({"v3", "v4", "v15", "v14"}, {"label": "Q", "R": False}),
                ({"v4", "v5", "v6", "v15"}, {"label": "Q", "R": False}),
                ({"v15", "v6", "v7", "v16"}, {"label": "Q", "R": False}),
                ({"v14", "v15", "v16", "v20"}, {"label": "Q", "R": False}),
                ({"v20", "v16", "v17", "v18"}, {"label": "Q", "R": False}),
                ({"v16", "v7", "v8", "v17"}, {"label": "Q", "R": False}),
                ({"v17", "v8", "v9", "v10"}, {"label": "Q", "R": False}),
                ({"v18", "v17", "v10", "v11"}, {"label": "Q", "R": False}),
            ],
        )

        if visualize:
            hyper_graph.visualize()

        # when
        production = P3()
        for hyper_node in hyper_graph.hyper_nodes:
            if production.check(hyper_graph, hyper_node):
                hyper_graph = production.apply(hyper_graph, hyper_node)

        if visualize:
            hyper_graph.visualize()

        # then
        expected_graph = HyperGraph(
            nodes=[
                ('v1', {'pos': (1, 1), 'h': False}),
                ('v2', {'pos': (2, 1), 'h': False}),
                ('v3', {'pos': (3, 1), 'h': False}),
                ('v4', {'pos': (4, 1), 'h': False}),
                ('v5', {'pos': (5, 1), 'h': False}),
                ('v6', {'pos': (5, 2), 'h': False}),
                ('v7', {'pos': (5, 3), 'h': False}),
                ('v8', {'pos': (5, 4), 'h': False}),
                ('v9', {'pos': (5, 5), 'h': False}),
                ('v10', {'pos': (4, 5), 'h': False}),
                ('v11', {'pos': (3, 5), 'h': False}),
                ('v12', {'pos': (1, 5), 'h': False}),
                ('v13', {'pos': (1, 3), 'h': False}),
                ('v14', {'pos': (3, 2), 'h': False}),
                ('v15', {'pos': (4, 2), 'h': False}),
                ('v16', {'pos': (4, 3), 'h': False}),
                ('v17', {'pos': (4, 4), 'h': False}),
                ('v20', {'pos': (3, 3), 'h': False}),
                ('v21', {'pos': (1, 2), 'h': False}),
                ('v22', {'pos': (2, 2), 'h': False}),
                ('v18', {'h': False, 'pos': (3, 4)}),
                ('v19', {'h': False, 'pos': (2, 3)}),
                ('v23', {'pos': (1.0, 4.0)}),
                ('v24', {'pos': (2.0, 5.0)}),
                ('v25', {'pos': (2.0, 4.0)})
            ],
            edges=[
                ({'v2', 'v1'}, {'label': 'E', 'B': True}),
                ({'v2', 'v3'}, {'label': 'E', 'B': True}),
                ({'v4', 'v3'}, {'label': 'E', 'B': True}),
                ({'v4', 'v5'}, {'label': 'E', 'B': True}),
                ({'v5', 'v6'}, {'label': 'E', 'B': True}),
                ({'v6', 'v7'}, {'label': 'E', 'B': True}),
                ({'v8', 'v7'}, {'label': 'E', 'B': True}),
                ({'v8', 'v9'}, {'label': 'E', 'B': True}),
                ({'v10', 'v9'}, {'label': 'E', 'B': True}),
                ({'v10', 'v11'}, {'label': 'E', 'B': True}),
                ({'v14', 'v15'}, {'label': 'E', 'B': False}),
                ({'v15', 'v16'}, {'label': 'E', 'B': False}),
                ({'v17', 'v16'}, {'label': 'E', 'B': False}),
                ({'v18', 'v17'}, {'label': 'E', 'B': False}),
                ({'v19', 'v20'}, {'label': 'E', 'B': False}),
                ({'v18', 'v20'}, {'label': 'E', 'B': False}),
                ({'v2', 'v19'}, {'label': 'E', 'B': False}),
                ({'v14', 'v3'}, {'label': 'E', 'B': False}),
                ({'v4', 'v15'}, {'label': 'E', 'B': False}),
                ({'v14', 'v20'}, {'label': 'E', 'B': False}),
                ({'v13', 'v19'}, {'label': 'E', 'B': False}),
                ({'v18', 'v11'}, {'label': 'E', 'B': False}),
                ({'v17', 'v10'}, {'label': 'E', 'B': False}),
                ({'v20', 'v16'}, {'label': 'E', 'B': False}),
                ({'v6', 'v15'}, {'label': 'E', 'B': False}),
                ({'v7', 'v16'}, {'label': 'E', 'B': False}),
                ({'v8', 'v17'}, {'label': 'E', 'B': False}),
                ({'v13', 'v21'}, {'label': 'E', 'B': True}),
                ({'v21', 'v1'}, {'label': 'E', 'B': True}),
                ({'v22', 'v21'}, {'label': 'E', 'B': False}),
                ({'v22', 'v14'}, {'label': 'E', 'B': False}),
                ({'v22', 'v21', 'v2', 'v1'}, {'label': 'Q', 'R': False}),
                ({'v22', 'v14', 'v2', 'v3'}, {'label': 'Q', 'R': False}),
                ({'v22', 'v14', 'v19', 'v20'}, {'label': 'Q', 'R': False}),
                ({'v22', 'v13', 'v21', 'v19'}, {'label': 'Q', 'R': False}),
                ({'v4', 'v14', 'v15', 'v3'}, {'label': 'Q', 'R': False}),
                ({'v4', 'v6', 'v15', 'v5'}, {'label': 'Q', 'R': False}),
                ({'v6', 'v7', 'v15', 'v16'}, {'label': 'Q', 'R': False}),
                ({'v14', 'v15', 'v20', 'v16'}, {'label': 'Q', 'R': False}),
                ({'v17', 'v18', 'v20', 'v16'}, {'label': 'Q', 'R': False}),
                ({'v8', 'v17', 'v7', 'v16'}, {'label': 'Q', 'R': False}),
                ({'v17', 'v8', 'v10', 'v9'}, {'label': 'Q', 'R': False}),
                ({'v17', 'v18', 'v10', 'v11'}, {'label': 'Q', 'R': False}),
                ({'v13', 'v23'}, {'B': True}),
                ({'v12', 'v23'}, {'B': True}),
                ({'v12', 'v24'}, {'B': True}),
                ({'v24', 'v11'}, {'B': True}),
                ({'v25', 'v23'}, {'B': False}),
                ({'v25', 'v24'}, {'B': False}),
                ({'v25', 'v18'}, {'B': False}),
                ({'v25', 'v19'}, {'B': False}),
                ({'v25', 'v13', 'v19', 'v23'}, {'R': False}),
                ({'v25', 'v12', 'v24', 'v23'}, {'R': False}),
                ({'v25', 'v18', 'v24', 'v11'}, {'R': False}),
                ({'v25', 'v18', 'v19', 'v20'}, {'R': False})
            ]
        )

        self.assertTrue(
             nx.is_isomorphic(hyper_graph.nx_graph, expected_graph.nx_graph)
        )
        

if __name__ == "__main__":
    test = TestP3()
    test.test(visualize=True)
    test.test2(visualize=True)

