import unittest
from graph.hypergraph import HyperGraph
from productions.p21 import P21
import math


class TestsP21Check(unittest.TestCase):

    def setUp(self):
        self.prod = P21()
        self.nodes = [
            ('v1', {'pos': (0, 0), 'h': False}),
            ('v2', {'pos': (1, 0), 'h': False}),
            ('v3', {'pos': (1.5, math.sqrt(3) / 2), 'h': False}),
            ('v4', {'pos': (1, math.sqrt(3)), 'h': False}),
            ('v5', {'pos': (0, math.sqrt(3)), 'h': False}),
            ('v6', {'pos': (-0.5, math.sqrt(3) / 2), 'h': False}),
        ]
        self.edges = [
            ({'v1', 'v2'}, {'label': 'E', 'B': True}),
            ({'v2', 'v3'}, {'label': 'E', 'B': True}),
            ({'v3', 'v4'}, {'label': 'E', 'B': True}),
            ({'v4', 'v5'}, {'label': 'E', 'B': True}),
            ({'v5', 'v6'}, {'label': 'E', 'B': True}),
            ({'v6', 'v1'}, {'label': 'E', 'B': True}),
            ({'v1', 'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'Q', 'R': False})
        ]

    def test_checkShouldReturnTrue(self):
        hyper_graph = HyperGraph(self.nodes, self.edges)
        self.assertTrue(self.prod.check(hyper_graph, hyper_graph.hyper_nodes[0]))

    def test_checkShouldReturnFalseWhenNodeIsMissing(self):
        hyper_graph = HyperGraph(
            nodes=[node for node in self.nodes if node[0] != 'v1'],
            edges=[edge for edge in self.edges if 'v1' not in edge[0]]
                  + [({'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'Q', 'R': False})]

        )
        self.assertFalse(self.prod.check(hyper_graph, hyper_graph.hyper_nodes[0]))

    def test_checkShouldReturnFalseWhenEdgeIsMissing(self):
        hyper_graph = HyperGraph(
            nodes=self.nodes,
            edges=[edge for edge in self.edges if len(edge[0]) < 3]
                  + [({'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'Q', 'R': False})]
        )
        self.assertFalse(self.prod.check(hyper_graph, hyper_graph.hyper_nodes[0]))

    def test_checkShouldReturnFalseWhenLabelIsWrong(self):
        hyper_graph = HyperGraph(
            nodes=self.nodes,
            edges=[edge for edge in self.edges if len(edge[0]) < 3]
                  + [({'v1','v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'Q', 'R': True})]
        )
        self.assertFalse(self.prod.check(hyper_graph, hyper_graph.hyper_nodes[0]))


class TestsP21Apply(unittest.TestCase):
    def setUp(self):
        self.prod = P21()

    def test_applyShouldChangeBreakability1(self):
        hyper_graph = HyperGraph(
            nodes=[
                ('v1', {'pos': (0, 0), 'h': False}),
                ('v2', {'pos': (1, 0), 'h': False}),
                ('v3', {'pos': (1.5, math.sqrt(3) / 2), 'h': False}),
                ('v4', {'pos': (1, math.sqrt(3)), 'h': False}),
                ('v5', {'pos': (0, math.sqrt(3)), 'h': False}),
                ('v6', {'pos': (-0.5, math.sqrt(3) / 2), 'h': False}),
            ],
            edges=[
                ({'v1', 'v2'}, {'label': 'E', 'B': True}),
                ({'v2', 'v3'}, {'label': 'E', 'B': True}),
                ({'v3', 'v4'}, {'label': 'E', 'B': True}),
                ({'v4', 'v5'}, {'label': 'E', 'B': True}),
                ({'v5', 'v6'}, {'label': 'E', 'B': True}),
                ({'v6', 'v1'}, {'label': 'E', 'B': True}),
                ({'v1', 'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'S', 'R': False})
            ]
        )

        node_id = hyper_graph.hyper_nodes[0]
        self.assertFalse(hyper_graph.is_breakable(node_id))

        hyper_graph = self.prod.apply(hyper_graph, node_id)

        self.assertEqual(len(hyper_graph.hyper_nodes), 1, "Number of hiper nodes changed")
        node_id = hyper_graph.hyper_nodes[0]
        self.assertTrue(hyper_graph.is_breakable(node_id))


if __name__ == '__main__':
    unittest.main()
