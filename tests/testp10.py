import copy
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
        self.assertTrue(self.prod.check(graph, graph.hyper_nodes[0]))

    def test_checkShouldReturnFalseWhenHangingNodeIsMissing(self):
        graph = HyperGraph(
            [node for node in self.nodes if node[0] != "v7"],
            [edge for edge in self.edges if "v7" not in edge[0]] + [
                ({'v1', 'v2'}, {'label': 'E', 'B': True}),
            ])
        self.assertFalse(self.prod.check(graph, graph.hyper_nodes[0]))

    def test_checkShouldReturnFalseWhenEdgeLabelIsWrong(self):
        graph = HyperGraph(
            self.nodes,
            [edge for edge in self.edges if len(edge[0]) < 3] + [
                ({'v1', 'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'SS', 'R': True}),
            ])
        self.assertFalse(self.prod.check(graph, graph.hyper_nodes[0]))

    def test_checkShouldReturnFalseWhenBreakableIsFalse(self):
        graph = HyperGraph(
            self.nodes,
            [edge for edge in self.edges if len(edge[0]) < 3] + [
                ({'v1', 'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'S', 'R': False}),
            ])
        self.assertFalse(self.prod.check(graph, graph.hyper_nodes[0]))

    def test_checkShouldReturnFalseWhenMultipleHangingNodesArePresent(self):
        graph = HyperGraph(
        nodes = [
            ('v1', {'pos': (0, 0), 'h': False}),
            ('v2', {'pos': (1, 0), 'h': False}),
            ('v3', {'pos': (1.5, math.sqrt(3) / 2), 'h': False}),
            ('v4', {'pos': (1, math.sqrt(3)), 'h': False}),
            ('v5', {'pos': (0, math.sqrt(3)), 'h': False}),
            ('v6', {'pos': (-0.5, math.sqrt(3) / 2), 'h': False}),
            ('v7', {'pos': (0.5, 0), 'h': True}),
            ('v8', {'pos': (0.5, math.sqrt(3)), 'h': True}),
        ],
        edges = [
            ({'v1', 'v7'}, {'label': 'E', 'B': True}),
            ({'v7', 'v2'}, {'label': 'E', 'B': True}),
            ({'v2', 'v3'}, {'label': 'E', 'B': True}),
            ({'v3', 'v4'}, {'label': 'E', 'B': True}),
            ({'v4', 'v8'}, {'label': 'E', 'B': True}),
            ({'v8', 'v5'}, {'label': 'E', 'B': True}),
            ({'v5', 'v6'}, {'label': 'E', 'B': True}),
            ({'v6', 'v1'}, {'label': 'E', 'B': True}),
            ({'v1', 'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'S', 'R': True})
        ]
        )
        self.assertFalse(self.prod.check(graph, graph.hyper_nodes[0]))

class TestP10Apply(unittest.TestCase):
    def setUp(self):
        self.prod = P10()

    def test_apply(self):
        nodes = [
            ('v1', {'pos': (0, 0), 'h': False}),
            ('v2', {'pos': (1, 0), 'h': False}),
            ('v3', {'pos': (1.5, math.sqrt(3) / 2), 'h': False}),
            ('v4', {'pos': (1, math.sqrt(3)), 'h': False}),
            ('v5', {'pos': (0, math.sqrt(3)), 'h': False}),
            ('v6', {'pos': (-0.5, math.sqrt(3) / 2), 'h': False}),
            ('v7', {'pos': (0.5, 0), 'h': True}),
        ]
        edges = [
            ({'v1', 'v7'}, {'label': 'E', 'B': True}),
            ({'v7', 'v2'}, {'label': 'E', 'B': True}),
            ({'v2', 'v3'}, {'label': 'E', 'B': True}),
            ({'v3', 'v4'}, {'label': 'E', 'B': True}),
            ({'v4', 'v5'}, {'label': 'E', 'B': True}),
            ({'v5', 'v6'}, {'label': 'E', 'B': True}),
            ({'v6', 'v1'}, {'label': 'E', 'B': True}),
            ({'v1', 'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'S', 'R': True})
        ]
        graph = HyperGraph(copy.deepcopy(nodes), copy.deepcopy(edges))
        self.prod.apply(graph, graph.hyper_nodes[0])
        self.assertEqual(len(graph.nodes), len(nodes) + 6)
        for node in nodes:
            if node[1]['h']:
                new_node = deepcopy(node)
                new_node[1]['h'] = False
                self.assertTrue(new_node in graph.nodes)
            else:
                self.assertTrue(node in graph.nodes)
        self.assertEqual(len(graph.edges), len(edges) + 16)

        self.assertEqual(len([e for e in graph.edges if e[1]["label"] == "E"]), 18)
        self.assertEqual(len([e for e in graph.edges if e[1]["label"] == "E" and e[1]["B"]]), 12)
        self.assertEqual(len([e for e in graph.edges if e[1]["label"] == "Q"]), 6)
        self.assertEqual(len([e for e in graph.edges if e[1]["label"] == "S"]), 0)

    def test_apply_with_different_boundary(self):
        nodes = [
            ('v1', {'pos': (0, 0), 'h': False}),
            ('v2', {'pos': (1, 0), 'h': False}),
            ('v3', {'pos': (1.5, math.sqrt(3) / 2), 'h': False}),
            ('v4', {'pos': (1, math.sqrt(3)), 'h': False}),
            ('v5', {'pos': (0, math.sqrt(3)), 'h': False}),
            ('v6', {'pos': (-0.5, math.sqrt(3) / 2), 'h': False}),
            ('v7', {'pos': (0.5, 0), 'h': True}),
        ]
        edges = [
            ({'v1', 'v7'}, {'label': 'E', 'B': False}),
            ({'v7', 'v2'}, {'label': 'E', 'B': False}),
            ({'v2', 'v3'}, {'label': 'E', 'B': True}),
            ({'v3', 'v4'}, {'label': 'E', 'B': True}),
            ({'v4', 'v5'}, {'label': 'E', 'B': True}),
            ({'v5', 'v6'}, {'label': 'E', 'B': True}),
            ({'v6', 'v1'}, {'label': 'E', 'B': True}),
            ({'v1', 'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'S', 'R': True})
        ]
        graph = HyperGraph(deepcopy(nodes), deepcopy(edges))
        self.prod.apply(graph, graph.hyper_nodes[0])
        self.assertEqual(len(graph.nodes), len(nodes) + 6)
        for node in nodes:
            if node[1]['h']:
                new_node = deepcopy(node)
                new_node[1]['h'] = False
                self.assertTrue(new_node in graph.nodes)
            else:
                self.assertTrue(node in graph.nodes)
        self.assertEqual(len(graph.edges), len(edges) + 16)

        self.assertEqual(len([e for e in graph.edges if e[1]["label"] == "E"]), 18)
        self.assertEqual(len([e for e in graph.edges if e[1]["label"] == "E" and e[1]["B"]]), 10)
        self.assertEqual(len([e for e in graph.edges if e[1]["label"] == "Q"]), 6)
        self.assertEqual(len([e for e in graph.edges if e[1]["label"] == "S"]), 0)


class TestP10(unittest.TestCase):
    def setUp(self):
        self.prod = P10()

    def test_multistep(self):
        sr3 = math.sqrt(3)
        hyper_graph = HyperGraph(
            nodes=[
                ('v1', {'pos': (0, 0), 'h': False}),
                ('v2', {'pos': (1, 0), 'h': False}),
                ('vh', {'pos': (0.5, 0), 'h': True}),
                ('v3', {'pos': (1.5, sr3 / 2), 'h': False}),
                ('v4', {'pos': (1, sr3), 'h': False}),
                ('v5', {'pos': (0, sr3), 'h': False}),
                ('v6', {'pos': (-0.5, sr3 / 2), 'h': False}),

                ('v7', {'pos': (-0.5, -sr3 / 2), 'h': False}),
                ('v8', {'pos': (0.5, -sr3/2), 'h': False}),
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
                ({'v1', 'vh'}, {'label': 'E', 'B': False}),
                ({'vh', 'v2'}, {'label': 'E', 'B': False}),
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
                ({'v8', 'v10'}, {'label': 'E', 'B': True}),
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
                ({"v8", "vh"}, {'label': 'E', 'B': False}),
                ({"v1", "vh", "v8", "v7"}, {'label': 'Q', 'R': False}),
                ({"v2", "vh", "v10", "v8"}, {'label': 'Q', 'R': False}),
                ({'v1', 'v2', 'v3', 'v4', 'v5', 'v6'}, {'label': 'S', 'R': True}),
                ({'v10', 'v2', 'v3', 'v11', 'v12', 'v13'}, {'label': 'S', 'R': False}),
                ({'v13', 'v14', 'v3', 'v4', 'v15', 'v16'}, {'label': 'S', 'R': False}),
                ({'v16', 'v17', 'v18', 'v4', 'v5', 'v19'}, {'label': 'S', 'R': False}),
                ({'v19', 'v20', 'v21', 'v22', 'v5', 'v6'}, {'label': 'S', 'R': True}),
                ({'v22', 'v23', 'v24', 'v1', 'v7', 'v6'}, {'label': 'S', 'R': False}),
            ]
        )
        nodes, edges = deepcopy(hyper_graph.nodes), deepcopy(hyper_graph.edges)
        hyper_graph.visualize()
        applicable_nodes = [v for v in hyper_graph.hyper_nodes if self.prod.check(hyper_graph, v)]
        self.assertEqual(len(applicable_nodes), 1)
        self.assertEqual(len([n for n in hyper_graph.nodes if n[1]['h']]), 1)
        self.prod.apply(hyper_graph, applicable_nodes[0])
        hyper_graph.visualize()
        for node in nodes:
            if node[1]['h']:
                new_node = deepcopy(node)
                new_node[1]['h'] = False
                self.assertTrue(new_node in hyper_graph.nodes)
            else:
                self.assertTrue(node in hyper_graph.nodes)

        self.assertEqual(len([n for n in hyper_graph.nodes if n[1]['h']]), 5)
        self.assertEqual(len(hyper_graph.edges), len(edges) + 16)

        self.assertEqual(len([e for e in hyper_graph.edges if e[1]["label"] == "E"]), 42)
        self.assertEqual(len([e for e in hyper_graph.edges if e[1]["label"] == "E" and e[1]["B"]]), 17)
        self.assertEqual(len([e for e in hyper_graph.edges if e[1]["label"] == "Q"]), 8)
        self.assertEqual(len([e for e in hyper_graph.edges if e[1]["label"] == "S"]), 5)


        applicable_nodes = [v for v in hyper_graph.hyper_nodes if self.prod.check(hyper_graph, v)]
        self.assertEqual(len(applicable_nodes), 1)
        self.prod.apply(hyper_graph, applicable_nodes[0])
        hyper_graph.visualize()
        self.assertEqual(len([n for n in hyper_graph.nodes if n[1]['h']]), 6)

        self.assertEqual(len(hyper_graph.edges), len(edges) + 32)

        self.assertEqual(len([e for e in hyper_graph.edges if e[1]["label"] == "E"]), 53)
        self.assertEqual(len([e for e in hyper_graph.edges if e[1]["label"] == "E" and e[1]["B"]]), 20)
        self.assertEqual(len([e for e in hyper_graph.edges if e[1]["label"] == "Q"]), 14)
        self.assertEqual(len([e for e in hyper_graph.edges if e[1]["label"] == "S"]), 4)



