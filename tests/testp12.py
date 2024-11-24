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
