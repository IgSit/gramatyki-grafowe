import networkx as nx
from unittest import TestCase

from graph.hypergraph import HyperGraph
from productions.p1 import P1

from tests.test_utils import prepare_edges


class TestP1(TestCase):

    def test(self):
        hyper_graph = HyperGraph(
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
            for hyper_node in hyper_graph.hyper_nodes:
                if production.check(hyper_graph, hyper_node):
                    hyper_graph = production.apply(hyper_graph, hyper_node)

        expected_graph = HyperGraph(
            nodes=[
                ('v11', {'pos': (0, 0), 'h': False}),
                ('v12', {'pos': (4, 0), 'h': False}),
                ('v13', {'pos': (4, 4), 'h': False}),
                ('v14', {'pos': (0, 4), 'h': False}),
                ('a(2.0, 2.0)', {'pos': (0, 2), 'h': False}),
                ('a(0.0, 2.0)', {'pos': (0, 2), 'h': True}),
                ('a(4.0, 2.0)', {'pos': (4, 2), 'h': True}),
                ('a(2.0, 4.0)', {'pos': (2, 4), 'h': True}),
                ('a(2.0, 0.0)', {'pos': (2, 0), 'h': True}),
            ],
            edges=[
                ({'v11', 'a(2.0, 0.0)'}, {'label': 'E', 'B': True}),
                ({'a(2.0, 0.0)', 'v12'}, {'label': 'E', 'B': True}),
                ({'v12', 'a(4.0, 2.0)'}, {'label': 'E', 'B': True}),
                ({'a(4.0, 2.0)', 'v13'}, {'label': 'E', 'B': True}),
                ({'v13', 'a(2.0, 4.0)'}, {'label': 'E', 'B': True}),
                ({'a(2.0, 4.0)', 'v14'}, {'label': 'E', 'B': True}),
                ({'v14', 'a(0.0, 2.0)'}, {'label': 'E', 'B': True}),
                ({'a(0.0, 2.0)', 'v11'}, {'label': 'E', 'B': True}),
                ({'a(0.0, 2.0)', 'a(2.0, 2.0)'}, {'label': 'E', 'B': False}),
                ({'a(2.0, 0.0)', 'a(2.0, 2.0)'}, {'label': 'E', 'B': False}),
                ({'a(4.0, 2.0)', 'a(2.0, 2.0)'}, {'label': 'E', 'B': False}),
                ({'a(2.0, 4.0)', 'a(2.0, 2.0)'}, {'label': 'E', 'B': False}),
                ({'a(2.0, 0.0)', 'v12', 'a(4.0, 2.0)', 'a(2.0, 2.0)'}, {'label': 'Q', 'R': False}),
                ({'a(2.0, 2.0)', 'a(4.0, 2.0)', 'v13', 'a(2.0, 4.0)'}, {'label': 'Q', 'R': False}),
                ({'a(0.0, 2.0)', 'v11', 'a(2.0, 0.0)', 'a(2.0, 2.0)'}, {'label': 'Q', 'R': False}),
                ({'a(0.0, 2.0)', 'a(2.0, 2.0)', 'a(2.0, 4.0)', 'v14'}, {'label': 'Q', 'R': False}),
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
