import sys
sys.path.append('..')

from graph.hypergraph import HyperGraph
from productions.p4 import P4
from productions.p7 import P7
import networkx as nx

graph = HyperGraph(
    nodes=[
        ('v1', {'pos': (1, 1), 'h': False}),
        ('v2', {'pos': (6, 1), 'h': False}),
        ('v3', {'pos': (6, 3), 'h': False}),
        ('v4', {'pos': (6, 5), 'h': False}),
        ('v5', {'pos': (1, 5), 'h': False}),
        ('v6', {'pos': (1, 3), 'h': False}),

        ('v7', {'pos': (3, 2), 'h': False}),
        ('v8', {'pos': (4, 2), 'h': False}),
        ('v9', {'pos': (5, 3), 'h': False}),
        ('v10', {'pos': (4, 4), 'h': False}),
        ('v11', {'pos': (3, 4), 'h': False}),
        ('v12', {'pos': (2, 3), 'h': False}),

    ],
    edges=[
        ({'v1', 'v2'}, {'label': 'E', 'B': True}),
        ({'v2', 'v3'}, {'label': 'E', 'B': True}),
        ({'v3', 'v4'}, {'label': 'E', 'B': True}),
        ({'v4', 'v5'}, {'label': 'E', 'B': True}),
        ({'v5', 'v6'}, {'label': 'E', 'B': True}),
        ({'v6', 'v1'}, {'label': 'E', 'B': True}),

        ({'v7', 'v8'}, {'label': 'E', 'B': True}),
        ({'v8', 'v9'}, {'label': 'E', 'B': True}),
        ({'v9', 'v10'}, {'label': 'E', 'B': True}),
        ({'v10', 'v11'}, {'label': 'E', 'B': True}),
        ({'v11', 'v12'}, {'label': 'E', 'B': True}),
        ({'v12', 'v7'}, {'label': 'E', 'B': True}),

        ({'v1', 'v7'}, {'label': 'E', 'B': True}),
        ({'v2', 'v8'}, {'label': 'E', 'B': True}),
        ({'v3', 'v9'}, {'label': 'E', 'B': True}),
        ({'v4', 'v10'}, {'label': 'E', 'B': True}),
        ({'v5', 'v11'}, {'label': 'E', 'B': True}),
        ({'v6', 'v12'}, {'label': 'E', 'B': True}),

        ({'v1', 'v2', 'v8', 'v7'}, {'label': 'Q', 'R': False}),
        ({'v2', 'v3', 'v9', 'v8'}, {'label': 'Q', 'R': False}),
        ({'v3', 'v4', 'v10', 'v9'}, {'label': 'Q', 'R': False}),
        ({'v4', 'v5', 'v11', 'v10'}, {'label': 'Q', 'R': False}),
        ({'v5', 'v6', 'v12', 'v11'}, {'label': 'Q', 'R': False}),
        ({'v6', 'v1', 'v7', 'v12'}, {'label': 'Q', 'R': False}),

        ({'v7', 'v8', 'v9', 'v10', 'v11', 'v12'}, {'label': 'S', 'R': False})
    ]
)
graph.visualize()

p7 = P7()
for hyper_node in graph.hyper_nodes:
    if p7.check(graph, hyper_node):
        graph = p7.apply(graph, hyper_node)

graph.visualize()
