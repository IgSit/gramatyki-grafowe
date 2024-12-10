import unittest
from productions.p10 import P10
from graph.hypergraph import HyperGraph
import math
from copy import deepcopy

class TestP10Check(unittest.TestCase):

    def setUp(self):
        self.prod = P10()
        self.nodes = [
            ('v1', {'pos': (0, 0), 'h': False}),
            ('v2', {'pos': (1, 0), 'h': False}),
            ('v3', {'pos': (1.5, math.sqrt(3) / 2), 'h': False}),
            ('v4', {'pos': (1, math.sqrt(3)), 'h': False}),
            ('v5', {'pos': (0, math.sqrt(3)), 'h': False}),
            ('v6', {'pos': (-0.5, math.sqrt(3) / 2), 'h': False}),
            ('v7', {'pos': (0.5, 0), 'h': True}),
        ]
        self.edges = [
            ({'v1', 'v7'}, {'label': 'E', 'B': True}),
            ({'v7', 'v2'}, {'label': 'E', 'B': True}),
            ({'v2', 'v3'}, {'label': 'E', 'B': True}),
            ({'v3', 'v4'}, {'label': 'E', 'B': True}),
            ({'v4', 'v5'}, {'label': 'E', 'B': True}),
            ({'v5', 'v6'}, {'label': 'E', 'B': True}),
            ({'v6', 'v1'}, {'label': 'E', 'B': True}),
            ({'v1', 'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'S', 'R': True})
        ]

    def test_checkShouldReturnTrue(self):
        graph = HyperGraph(self.nodes, self.edges)
        graph.visualize()
        self.assertTrue(self.prod.check(graph, graph.hyper_nodes[0]))



