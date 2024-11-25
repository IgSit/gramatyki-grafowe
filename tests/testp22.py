from graph.hypergraph import HyperGraph
from productions.p22 import P22

class TestP22():
    def __init__(self):
        pass
    
    def run(self):
        hyper_graph1 = HyperGraph(
            nodes=[
                ('v1', {'pos': (0, 0), 'h': False}),
                ('v2', {'pos': (4, 0), 'h': False}),
                ('v3', {'pos': (4, 4), 'h': False}),
                ('v4', {'pos': (0, 4), 'h': False}),
                ('v5', {'pos': (4, 2), 'h': True}),
                ('v6', {'pos': (8, 2), 'h': False}),
                ('v7', {'pos': (8, 4), 'h': False}),
                ('v8', {'pos': (2, 0), 'h': False}),
                ('v9', {'pos': (0, 2), 'h': False})
            ],
            edges=[
                ({'v3', 'v5'}, {'label': 'E', 'B': False}),
                ({'v5', 'v2'}, {'label': 'E', 'B': False}),
                ({'v3', 'v5', 'v6', 'v7'}, {'label': 'Q1', 'R': True}),
                ({'v1', 'v2', 'v3', 'v4', 'v8', 'v9'}, {'label': 'Q2', 'R': False})
            ]
        )
        #hyper_graph1.visualize()
        productions = [P22()]

        for production in productions:
            for hyper_node in hyper_graph1.hyper_nodes:
                #print(f"Check {hyper_node}")
                if production.check(hyper_graph1, hyper_node):
                    hyper_graph1.visualize()
                    hyper_graph1 = production.apply(hyper_graph1, hyper_node)
                    hyper_graph1.visualize()
                    break