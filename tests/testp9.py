from graph.hypergraph import HyperGraph
from productions.p9 import P9

class TestP9():
    def __init__(self):
        pass
    
    def run(self):
        hyper_graph = HyperGraph(
            nodes=[
                ('v1', {'pos': (-4, 0), 'h': False}),
                ('v2', {'pos': (-2, 3), 'h': False}),
                ('v3', {'pos': (2, 3), 'h': False}),
                ('v4', {'pos': (4, 0), 'h': False}),
                ('v5', {'pos': (2, -3), 'h': False}),
                ('v6', {'pos': (-2, -3), 'h': False}),
            ],
            edges=[
                ({'v1', 'v2'}, {'label': 'E', 'B': True}),
                ({'v2', 'v3'}, {'label': 'E', 'B': True}),
                ({'v3', 'v4'}, {'label': 'E', 'B': True}),
                ({'v4', 'v5'}, {'label': 'E', 'B': True}),
                ({'v5', 'v6'}, {'label': 'E', 'B': True}),
                ({'v6', 'v1'}, {'label': 'E', 'B': True}),
                ({'v1', 'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'Q', 'R': True})
            ]
        )

        productions = [P9()]

        for production in productions:
            for hyper_node in hyper_graph.hyper_nodes:
                if production.check(hyper_graph, hyper_node):
                    hyper_graph.visualize()
                    hyper_graph = production.apply(hyper_graph, hyper_node)
                    hyper_graph.visualize()
                    break
        