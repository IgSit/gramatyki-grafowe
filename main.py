from graph.hypergraph import HyperGraph
from productions.p1 import P1
import networkx as nx

if __name__ == "__main__":
    hyper_graph1 = HyperGraph(
        nodes=[
            ('v1', {'pos': (0, 0), 'h': False}),
            ('v2', {'pos': (4, 0), 'h': False}),
            ('v3', {'pos': (4, 4), 'h': False}),
            ('v4', {'pos': (0, 4), 'h': False}),
            ('v5', {'pos': (4, 2), 'h': True})
        ],
        edges=[
            ({'v1', 'v2'}, {'label': 'E', 'B': True}),
            ({'v2', 'v5'}, {'label': 'E', 'B': True}),
            ({'v5', 'v3'}, {'label': 'E', 'B': True}),
            ({'v3', 'v4'}, {'label': 'E', 'B': True}),
            ({'v4', 'v1'}, {'label': 'E', 'B': True}),
            ({'v1', 'v2', 'v3', 'v4'}, {'label': 'Q', 'R': True})
        ]
    )
    hyper_graph2 = HyperGraph(
        nodes=[
            ('v11', {'pos': (0, 0), 'h': False}),
            ('v12', {'pos': (4, 0), 'h': False}),
            ('v13', {'pos': (4, 4), 'h': False}),
            ('v14', {'pos': (0, 4), 'h': False})
        ],
        edges=[
            ({'v11', 'v12'}, {'label': 'E', 'B': True}),
            ({'v12', 'v13'}, {'label': 'E', 'B': True}),
            ({'v13', 'v14'}, {'label': 'E', 'B': True}),
            ({'v14', 'v11'}, {'label': 'E', 'B': True}),
            ({'v11', 'v12', 'v13', 'v14'}, {'label': 'Q', 'R': True})
        ]
    )

    productions = [P1()]

    for production in productions:
        for hyper_node in hyper_graph2.hyper_nodes:
            if production.check(hyper_graph2, hyper_node):
                hyper_graph2.visualize()
                hyper_graph2 = production.apply(hyper_graph2, hyper_node)
                hyper_graph2.visualize()
                break