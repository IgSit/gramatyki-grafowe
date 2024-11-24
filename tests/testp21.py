import copy
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

    def test_applyShouldNotChangeBiggerGraph(self):
        sr3 = math.sqrt(3)
        hyper_graph = HyperGraph(
            nodes=[
                ('v1', {'pos': (0, 0), 'h': False}),
                ('v2', {'pos': (1, 0), 'h': False}),
                ('v3', {'pos': (1.5, sr3 / 2), 'h': False}),
                ('v4', {'pos': (1, sr3), 'h': False}),
                ('v5', {'pos': (0, sr3), 'h': False}),
                ('v6', {'pos': (-0.5, sr3 / 2), 'h': False}),

                ('v7', {'pos': (-0.5, -sr3 / 2), 'h': False}),
                ('v8', {'pos': (0, -sr3), 'h': False}),
                ('v9', {'pos': (1, -sr3), 'h': False}),
                ('v10', {'pos': (1.5, -sr3/2), 'h': False}),

                ('v11', {'pos': (2.5, -sr3/2), 'h': False}),
                ('v12', {'pos': (3, 0), 'h': False}),
                ('v13', {'pos': (2.5, sr3/2), 'h': False}),

                ('v14', {'pos': (3, sr3), 'h': False}),
                ('v15', {'pos': (2.5, sr3 * 1.5), 'h': False}),
                ('v16', {'pos': (1.5, sr3 * 1.5), 'h': False}),

                ('v17', {'pos': (1, sr3 * 2), 'h': False}),
                ('v18', {'pos': (0, sr3 * 2), 'h': False}),
                ('v19', {'pos': (-0.5, sr3 * 1.5), 'h': False}),

                ('v20', {'pos': (-1.5, sr3 * 1.5), 'h': False}),
                ('v21', {'pos': (-2, sr3 * 1), 'h': False}),
                ('v22', {'pos': (-1.5, sr3 * 0.5), 'h': False}),

                ('v23', {'pos': (-2, sr3 * 0), 'h': False}),
                ('v24', {'pos': (-1.5, sr3 * -0.5), 'h': False}),

            ],
            edges=[
                ({'v1', 'v2'}, {'label': 'E', 'B': False}),
                ({'v2', 'v3'}, {'label': 'E', 'B': False}),
                ({'v3', 'v4'}, {'label': 'E', 'B': False}),
                ({'v4', 'v5'}, {'label': 'E', 'B': False}),
                ({'v5', 'v6'}, {'label': 'E', 'B': False}),
                ({'v6', 'v1'}, {'label': 'E', 'B': False}),

                ({'v6', 'v22'}, {'label': 'E', 'B': False}),
                ({'v5', 'v19'}, {'label': 'E', 'B': False}),
                ({'v4', 'v16'}, {'label': 'E', 'B': False}),
                ({'v3', 'v13'}, {'label': 'E', 'B': False}),
                ({'v2', 'v10'}, {'label': 'E', 'B': False}),
                ({'v1', 'v7'}, {'label': 'E', 'B': False}),

                ({'v7', 'v8'}, {'label': 'E', 'B': True}),
                ({'v8', 'v9'}, {'label': 'E', 'B': True}),
                ({'v9', 'v10'}, {'label': 'E', 'B': True}),
                ({'v10', 'v11'}, {'label': 'E', 'B': True}),
                ({'v11', 'v12'}, {'label': 'E', 'B': True}),
                ({'v12', 'v13'}, {'label': 'E', 'B': True}),
                ({'v13', 'v14'}, {'label': 'E', 'B': True}),
                ({'v14', 'v15'}, {'label': 'E', 'B': True}),
                ({'v15', 'v16'}, {'label': 'E', 'B': True}),
                ({'v16', 'v17'}, {'label': 'E', 'B': True}),
                ({'v17', 'v18'}, {'label': 'E', 'B': True}),
                ({'v18', 'v19'}, {'label': 'E', 'B': True}),
                ({'v19', 'v20'}, {'label': 'E', 'B': True}),
                ({'v20', 'v21'}, {'label': 'E', 'B': True}),
                ({'v21', 'v22'}, {'label': 'E', 'B': True}),
                ({'v22', 'v23'}, {'label': 'E', 'B': True}),
                ({'v23', 'v24'}, {'label': 'E', 'B': True}),
                ({'v24', 'v7'}, {'label': 'E', 'B': True}),


                ({'v1', 'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'S', 'R': False}),
                ({'v1', 'v2', 'v7', 'v8', 'v9', 'v10'}, {'label': 'S', 'R': True}),
                ({'v10', 'v2', 'v3', 'v11', 'v12', 'v13'}, {'label': 'S', 'R': True}),
                ({'v13', 'v14', 'v3', 'v4', 'v15', 'v16'}, {'label': 'S', 'R': True}),
                ({'v16', 'v17', 'v18', 'v4', 'v5', 'v19'}, {'label': 'S', 'R': True}),
                ({'v19', 'v20', 'v21', 'v22', 'v5', 'v6'}, {'label': 'S', 'R': True}),
                ({'v22', 'v23', 'v24', 'v1', 'v7', 'v6'}, {'label': 'S', 'R': True}),
            ]
        )
        nodes = copy.deepcopy(hyper_graph.nodes)
        edges = copy.deepcopy(hyper_graph.edges)
        hyper_nodes = copy.deepcopy(hyper_graph.hyper_nodes)

        target_hyper_node = None
        for n in hyper_nodes:
            if not hyper_graph.is_breakable(n):
                target_hyper_node = n
                break

        hyper_nodes.remove(target_hyper_node)
        edges.remove(({'v1', 'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'S', 'R': False}))

        self.prod.apply(hyper_graph, target_hyper_node)
        self.assertEqual(nodes, hyper_graph.nodes)
        for expected_edge in edges:
            self.assertTrue(expected_edge in hyper_graph.edges)
        for expected_hyper_node in hyper_nodes:
            self.assertTrue(expected_hyper_node in hyper_graph.hyper_nodes)

        self.assertTrue(({'v1', 'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'S', 'R': True}) in hyper_graph.edges)
        self.assertTrue(len(hyper_graph.hyper_nodes) == len(hyper_nodes) + 1)



if __name__ == '__main__':
    unittest.main()
