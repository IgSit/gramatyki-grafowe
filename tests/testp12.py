from graph.hypergraph import HyperGraph
from productions.p11 import P11
from productions.p12 import P12


class TestP12():
    def __init__(self):
        pass

    def run(self):
        #change later - irrelevant square graph

        hyper_graph1 = HyperGraph(
            nodes=[
                ('v1', {'pos': (2, -2), 'h': False}),
                ('v2', {'pos': (4, -2), 'h': False}),
                ('v3', {'pos': (4, 2), 'h': False}),
                ('v4', {'pos': (2, 2), 'h': False}),
                ('v5', {'pos': (6, 0), 'h': False}),
                ('v6', {'pos': (0, 0), 'h': False}),
                ('v7', {'pos': (3, -2), 'h': True}),
                ('v8', {'pos': (1, 1), 'h': True}),
            ],
            edges=[
                ({'v1', 'v7'}, {'label': 'E', 'B': False}),
                ({'v7', 'v2'}, {'label': 'E', 'B': False}),
                ({'v2', 'v5'}, {'label': 'E', 'B': False}),
                ({'v5', 'v3'}, {'label': 'E', 'B': False}),
                ({'v3', 'v4'}, {'label': 'E', 'B': False}),
                ({'v6', 'v1'}, {'label': 'E', 'B': False}),
                ({'v4', 'v8'}, {'label': 'E', 'B': False}),
                ({'v8', 'v6'}, {'label': 'E', 'B': False}),
                ({'v1', 'v2', 'v5', 'v3', 'v4', 'v6'}, {'label': 'S', 'R': True})
            ]
        )

        productions = [P12()]

        hyper_graph1.visualize()

        for production in productions:
            for hyper_node in hyper_graph1.hyper_nodes:
                if production.check(hyper_graph1, hyper_node):
                    hyper_graph1.visualize()
                    hyper_graph1 = production.apply(hyper_graph1, hyper_node)
                    hyper_graph1.visualize()
                    break

        hyper_graph2 = HyperGraph(
            nodes=[
                ('v1', {'pos': (2, -2), 'h': False}),
                ('v2', {'pos': (4, -2), 'h': False}),
                ('v3', {'pos': (4, 2), 'h': False}),
                ('v4', {'pos': (2, 2), 'h': False}),
                ('v5', {'pos': (6, 0), 'h': False}),
                ('v6', {'pos': (0, 0), 'h': False}),
                ('v7', {'pos': (3, -2), 'h': True}),
                ('v9', {"pos": (0,-6), 'h': False}),
                # ('v10', {"pos": (0, 6), 'h': False}),
                # ('v11', {"pos": (6, -6), 'h': False}),
                # ('v12', {"pos": (6, 6), 'h': False}),
                ('v8', {'pos': (1, 1), 'h': True}),
            ],
            edges=[
                ({'v1', 'v7'}, {'label': 'E', 'B': False}),
                ({'v7', 'v2'}, {'label': 'E', 'B': False}),
                ({'v2', 'v5'}, {'label': 'E', 'B': False}),
                ({'v5', 'v3'}, {'label': 'E', 'B': False}),
                ({'v3', 'v4'}, {'label': 'E', 'B': False}),
                ({'v6', 'v1'}, {'label': 'E', 'B': False}),
                ({'v4', 'v8'}, {'label': 'E', 'B': False}),
                ({'v8', 'v6'}, {'label': 'E', 'B': False}),
                # ({'v6', 'v10'}, {'label': 'E', 'B': False}),
                ({'v6', 'v9'}, {'label': 'E', 'B': False}),
                ({'v9', 'v1'}, {'label': 'E', 'B': False}),
                # ({'v2', 'v11'}, {'label': 'E', 'B': False}),
                # ({'v11', 'v5'}, {'label': 'E', 'B': False}),
                # ({'v5', 'v12'}, {'label': 'E', 'B': False}),
                # ({'v3', 'v12'}, {'label': 'E', 'B': False}),
                # ({'v10', 'v4'}, {'label': 'E', 'B': False}),
                ({'v1', 'v2', 'v5', 'v3', 'v4', 'v6'}, {'label': 'S', 'R': True})
            ]
        )

        # productions = [P12()]

        hyper_graph2.visualize()

        for production in productions:
            for hyper_node in hyper_graph2.hyper_nodes:
                if production.check(hyper_graph2, hyper_node):
                    hyper_graph2.visualize()
                    hyper_graph2 = production.apply(hyper_graph2, hyper_node)
                    hyper_graph2.visualize()
                    break

        hyper_graph3 = HyperGraph(
            nodes=[
                ('v1', {'pos': (2, -2), 'h': False}),
                ('v2', {'pos': (4, -2), 'h': False}),
                ('v3', {'pos': (4, 2), 'h': False}),
                ('v4', {'pos': (2, 2), 'h': False}),
                ('v5', {'pos': (6, 0), 'h': False}),
                ('v6', {'pos': (0, 0), 'h': False}),
                ('v7', {'pos': (3, -2), 'h': True}),
                ('v9', {"pos": (0, -6), 'h': False}),
                ('v10', {"pos": (0, 6), 'h': False}),
                ('v11', {"pos": (6, -6), 'h': False}),
                ('v12', {"pos": (6, 6), 'h': False}),
                ('v8', {'pos': (1, 1), 'h': True}),
            ],
            edges=[
                ({'v1', 'v7'}, {'label': 'E', 'B': False}),
                ({'v7', 'v2'}, {'label': 'E', 'B': False}),
                ({'v2', 'v5'}, {'label': 'E', 'B': False}),
                ({'v5', 'v3'}, {'label': 'E', 'B': False}),
                ({'v3', 'v4'}, {'label': 'E', 'B': False}),
                ({'v6', 'v1'}, {'label': 'E', 'B': False}),
                ({'v4', 'v8'}, {'label': 'E', 'B': False}),
                ({'v8', 'v6'}, {'label': 'E', 'B': False}),
                ({'v6', 'v10'}, {'label': 'E', 'B': False}),
                ({'v6', 'v9'}, {'label': 'E', 'B': False}),
                ({'v9', 'v1'}, {'label': 'E', 'B': False}),
                ({'v2', 'v11'}, {'label': 'E', 'B': False}),
                ({'v11', 'v5'}, {'label': 'E', 'B': False}),
                ({'v5', 'v12'}, {'label': 'E', 'B': False}),
                ({'v3', 'v12'}, {'label': 'E', 'B': False}),
                ({'v10', 'v4'}, {'label': 'E', 'B': False}),
                ({'v1', 'v2', 'v5', 'v3', 'v4', 'v6'}, {'label': 'S', 'R': True})
            ]
        )

        # productions = [P12()]

        hyper_graph3.visualize()

        for production in productions:
            for hyper_node in hyper_graph3.hyper_nodes:
                if production.check(hyper_graph3, hyper_node):
                    hyper_graph3.visualize()
                    hyper_graph3 = production.apply(hyper_graph3, hyper_node)
                    hyper_graph3.visualize()
                    break

        hyper_graph_big = HyperGraph(
            nodes=[
                ('v1', {'pos': (2, -2), 'h': False}),
                ('v2', {'pos': (4, -2), 'h': False}),
                ('v3', {'pos': (4, 2), 'h': False}),
                ('v4', {'pos': (2, 2), 'h': False}),
                ('v5', {'pos': (5, 0), 'h': False}),
                ('v6', {'pos': (1, 0), 'h': False}),
                ('v7', {'pos': (3, -2), 'h': True}),
                ('v8', {'pos': (1.5, 1), 'h': True}),
                ('v9', {'pos': (0, 3), 'h': False}),
                # ('v9', {'pos': (0, 3), 'h': True}),
                ('v10', {'pos': (6, 3), 'h': False}),
                ('v1011', {'pos': (6, 0), 'h': False}),
                ('v11', {'pos': (6, -3), 'h': False}),
                ('v12', {'pos': (0, -3), 'h': False}),
                ('v1112', {'pos': (3, -3), 'h': False}),
                ('v912', {'pos': (0, 0), 'h': False}),
                ('v9912', {'pos': (0, 1.5), 'h': False}),
                # ('v12912', {'pos': (0, -1.5), 'h': False}),
            ],
            edges=[
                ({'v1', 'v7'}, {'label': 'E', 'B': False}),
                ({'v1', 'v6'}, {'label': 'E', 'B': False}),
                ({'v7', 'v2'}, {'label': 'E', 'B': False}),
                ({'v2', 'v5'}, {'label': 'E', 'B': False}),
                ({'v5', 'v3'}, {'label': 'E', 'B': False}),
                ({'v3', 'v4'}, {'label': 'E', 'B': False}),
                ({'v4', 'v8'}, {'label': 'E', 'B': False}),
                ({'v8', 'v6'}, {'label': 'E', 'B': False}),
                # ({'v4', 'v6'}, {'label': 'E', 'B': False}),
                # ({'v6', 'v8'}, {'label': 'E', 'B': False}),
                # ({'v8', 'v1'}, {'label': 'E', 'B': False}),
                # ({'v8', 'v12912'}, {'label': 'E', 'B': False}),
                ({'v7', 'v1112'}, {'label': 'E', 'B': False}),
                ({'v9', 'v10'}, {'label': 'E', 'B': True}),
                # ({'v11', 'v12'}, {'label': 'E', 'B': True}),
                # ({'v12', 'v12912'}, {'label': 'E', 'B': True}),
                # ({'v912', 'v12912'}, {'label': 'E', 'B': True}),
                ({'v10', 'v1011'}, {'label': 'E', 'B': True}),
                ({'v11', 'v1011'}, {'label': 'E', 'B': True}),
                ({'v11', 'v1112'}, {'label': 'E', 'B': True}),
                ({'v12', 'v1112'}, {'label': 'E', 'B': True}),
                ({'v12', 'v912'}, {'label': 'E', 'B': True}),
                ({'v8', 'v9912'}, {'label': 'E', 'B': False}),
                # ({'v9', 'v912'}, {'label': 'E', 'B': True}),
                ({'v9', 'v9912'}, {'label': 'E', 'B': True}),
                ({'v9912', 'v912'}, {'label': 'E', 'B': True}),
                ({'v4', 'v9'}, {'label': 'E', 'B': False}),
                ({'v3', 'v10'}, {'label': 'E', 'B': False}),
                ({'v2', 'v11'}, {'label': 'E', 'B': False}),
                ({'v1', 'v12'}, {'label': 'E', 'B': False}),
                ({'v5', 'v1011'}, {'label': 'E', 'B': False}),
                ({'v6', 'v912'}, {'label': 'E', 'B': False}),
                ({'v6', 'v912'}, {'label': 'E', 'B': False}),
                ({'v1', 'v2', 'v5', 'v3', 'v4', 'v6'}, {'label': 'S', 'R': True}),
                # ({'v1', 'v12', 'v12912', 'v8'}, {'label': 'Q', 'R': False}),
                # ({'v6', 'v912', 'v12912', 'v8'}, {'label': 'Q', 'R': False}),
                ({'v3', 'v4', 'v9', 'v10'}, {'label': 'Q', 'R': False}),
                ({'v3', 'v5', 'v1011', 'v10'}, {'label': 'Q', 'R': False}),
                ({'v2', 'v5', 'v1011', 'v11'}, {'label': 'Q', 'R': False}),
                ({'v1', 'v12', 'v1112', 'v7'}, {'label': 'Q', 'R': False}),
                ({'v1', 'v12', 'v912', 'v6'}, {'label': 'Q', 'R': False}),
                ({'v2', 'v11', 'v1112', 'v7'}, {'label': 'Q', 'R': False}),
                ({'v8', 'v4', 'v9', 'v9912'}, {'label': 'Q', 'R': False}),
                ({'v6', 'v8', 'v9912', 'v912'}, {'label': 'Q', 'R': False}),
            ]
        )

        hyper_graph_big.visualize()

        for production in productions:
            for hyper_node in hyper_graph_big.hyper_nodes:
                if production.check(hyper_graph_big, hyper_node):
                    hyper_graph_big.visualize()
                    hyper_graph_big = production.apply(hyper_graph_big, hyper_node)
                    hyper_graph_big.visualize()
                    break