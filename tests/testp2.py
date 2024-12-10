import networkx as nx
from unittest import TestCase
from graph.hypergraph import HyperGraph
from productions.p2 import P2
from tests.test_utils import prepare_edges


class TestP2(TestCase):

    def test(self):
        hyper_graph = HyperGraph(
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

        productions = [P2()]

        for production in productions:
            for hyper_node in hyper_graph.hyper_nodes:
                if production.check(hyper_graph, hyper_node):
                    hyper_graph = production.apply(hyper_graph, hyper_node)

        expected_graph = HyperGraph(
            nodes=[
                ('v1', {'pos': (0, 0), 'h': False}),
                ('v2', {'pos': (4, 0), 'h': False}),
                ('v3', {'pos': (4, 4), 'h': False}),
                ('v4', {'pos': (0, 4), 'h': False}),
                ('v5', {'pos': (4, 2), 'h': False}),
                ('a(0.0, 2.0)', {'pos': (0, 2), 'h': False}),
                ('a(2.0, 2.0)', {'pos': (2, 2), 'h': False}),
                ('a(2.0, 4.0)', {'pos': (2, 4), 'h': False}),
                ('a(2.0, 0.0)', {'pos': (2, 0), 'h': False}),
            ],
            edges=[
                ({'v1', 'a(2.0, 0.0)'}, {'label': 'E', 'B': True}),
                ({'a(2.0, 0.0)', 'v2'}, {'label': 'E', 'B': True}),
                ({'v2', 'v5'}, {'label': 'E', 'B': True}),
                ({'v5', 'v3'}, {'label': 'E', 'B': True}),
                ({'v3', 'a(2.0, 4.0)'}, {'label': 'E', 'B': True}),
                ({'a(2.0, 4.0)', 'v4'}, {'label': 'E', 'B': True}),
                ({'v4', 'a(0.0, 2.0)'}, {'label': 'E', 'B': True}),
                ({'a(0.0, 2.0)', 'v1'}, {'label': 'E', 'B': True}),
                ({'a(0.0, 2.0)', 'a(2.0, 2.0)'}, {'label': 'E', 'B': False}),
                ({'a(2.0, 0.0)', 'a(2.0, 2.0)'}, {'label': 'E', 'B': False}),
                ({'v5', 'a(2.0, 2.0)'}, {'label': 'E', 'B': False}),
                ({'a(2.0, 4.0)', 'a(2.0, 2.0)'}, {'label': 'E', 'B': False}),
                ({'a(0.0, 2.0)', 'v1', 'a(2.0, 0.0)', 'a(2.0, 2.0)'}, {'label': 'Q', 'R': False}),
                ({'a(2.0, 0.0)', 'v2', 'v5', 'a(2.0, 2.0)'}, {'label': 'Q', 'R': False}),
                ({'a(0.0, 2.0)', 'a(2.0, 2.0)', 'a(2.0, 4.0)', 'v4'}, {'label': 'Q', 'R': False}),
                ({'a(2.0, 2.0)', 'v5', 'v3', 'a(2.0, 4.0)'}, {'label': 'Q', 'R': False}),
            ]
        )

        self.assertTrue(
            nx.is_isomorphic(hyper_graph.nx_graph, expected_graph.nx_graph)
        )

        self.assertDictEqual(
            nx.get_node_attributes(hyper_graph.nx_graph, 'h'),
            nx.get_node_attributes(expected_graph.nx_graph, 'h')
        )

        self.assertDictEqual(
            prepare_edges(nx.get_edge_attributes(hyper_graph.nx_graph, 'label')),
            prepare_edges(nx.get_edge_attributes(expected_graph.nx_graph, 'label'))
        )

        self.assertDictEqual(
            prepare_edges(nx.get_edge_attributes(hyper_graph.nx_graph, 'B')),
            prepare_edges(nx.get_edge_attributes(expected_graph.nx_graph, 'B'))
        )

        self.assertDictEqual(
            prepare_edges(nx.get_edge_attributes(hyper_graph.nx_graph, 'R')),
            prepare_edges(nx.get_edge_attributes(expected_graph.nx_graph, 'R'))
        )
