from graph.hypergraph import HyperGraph
from productions.p9 import P9

from copy import deepcopy
from unittest import TestCase
from networkx.algorithms import isomorphism


class TestP9(TestCase):
    def setUp(self):
        self.production = P9()
        self.proper_graph = HyperGraph(
            nodes=[
                ("v1", {"pos": (-4, 0), "h": False}),
                ("v2", {"pos": (-2, 3), "h": False}),
                ("v3", {"pos": (2, 3), "h": False}),
                ("v4", {"pos": (4, 0), "h": False}),
                ("v5", {"pos": (2, -3), "h": False}),
                ("v6", {"pos": (-2, -3), "h": False}),
            ],
            edges=[
                ({"v1", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v3"}, {"label": "E", "B": True}),
                ({"v3", "v4"}, {"label": "E", "B": True}),
                ({"v4", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v6"}, {"label": "E", "B": True}),
                ({"v6", "v1"}, {"label": "E", "B": True}),
                ({"v1", "v2", "v3", "v4", "v5", "v6"}, {"label": "Q", "R": True}),
            ],
        )

        self.excepted_center_edge_nodes_positions = [
            (3, 1.5),
            (3, -1.5),
            (-3, 1.5),
            (-3, -1.5),
            (0, 3),
            (0, -3),
        ]

    def test_proper_graph_check(self):
        proper_graph_hypernode = self.proper_graph.hyper_nodes[0]
        self.assertTrue(
            self.production.check(self.proper_graph, proper_graph_hypernode)
        )

    def test_missing_edge_check(self):
        missing_edge_graph = deepcopy(self.proper_graph)
        missing_edge_graph._remove_edges(missing_edge_graph.edges[0])
        missing_edge_hypernode = missing_edge_graph.hyper_nodes[0]
        self.assertFalse(
            self.production.check(missing_edge_graph, missing_edge_hypernode)
        )

    def test_hanging_node_check(self):
        hanging_node_graph = deepcopy(self.proper_graph)
        hanging_node_graph._remove_edges(({"v5", "v6"}, {"label": "E", "B": True}))
        hanging_node_graph.extend(
            nodes=[("v7", {"pos": (0, -3), "h": True})],
            edges=[
                ({"v5", "v7"}, {"label": "E", "B": False}),
                ({"v7", "v6"}, {"label": "E", "B": False}),
            ],
        )
        hanging_node_hypernode = hanging_node_graph.hyper_nodes[0]
        self.assertFalse(
            self.production.check(hanging_node_graph, hanging_node_hypernode)
        )

    def test_proper_graph_apply(self):
        hyper_graph = deepcopy(self.proper_graph)
        hyper_node = hyper_graph.hyper_nodes[0]

        if self.production.check(hyper_graph, hyper_node):
            starting_graph_nodes_positions = [
                params["pos"] for _, params in hyper_graph.nodes
            ]
            hyper_graph = self.production.apply(hyper_graph, hyper_node)
            modified_graph_nodes_positions = [
                params["pos"] for _, params in hyper_graph.nodes
            ]

            # checking if none of nodes is missing
            # and centers of previously added nodes are now nodes
            new_center_edge_nodes_positions = (
                self.excepted_center_edge_nodes_positions + [(0, 0)]
            )

            self.assertSetEqual(
                set(new_center_edge_nodes_positions + starting_graph_nodes_positions),
                set(modified_graph_nodes_positions),
            )

    def test_in_bigger_graph(self):
        bigger_graph = HyperGraph(
            nodes=[
                ("a", {"pos": (-4, 0), "h": False}),
                ("b", {"pos": (-2, 3), "h": False}),
                ("c", {"pos": (2, 3), "h": False}),
                ("d", {"pos": (4, 0), "h": False}),
                ("e", {"pos": (2, -3), "h": False}),
                ("f", {"pos": (-2, -3), "h": False}),
                ("g", {"pos": (-2, 7), "h": False}),
                ("h", {"pos": (2, 7), "h": False}),
                ("i", {"pos": (-8, 3), "h": False}),
                ("j", {"pos": (-8, 7), "h": False}),
                ("k", {"pos": (-4, 10), "h": False}),
                ("l", {"pos": (-2, -7), "h": False}),
                ("m", {"pos": (2, -7), "h": False}),
                ("n", {"pos": (-8, -2), "h": False}),
                ("o", {"pos": (-6, -6), "h": False}),
                ("p", {"pos": (8, -6), "h": False}),
                ("q", {"pos": (10, -2), "h": False}),
                ("r", {"pos": (8, 4), "h": False}),
                ("s", {"pos": (-8, 0), "h": True}),
                ("t", {"pos": (9, -4), "h": True}),
                ("u", {"pos": (-8, 5), "h": True}),
            ],
            edges=[
                ({"a", "b"}, {"label": "E", "B": False}),
                ({"b", "c"}, {"label": "E", "B": False}),
                ({"c", "d"}, {"label": "E", "B": False}),
                ({"d", "e"}, {"label": "E", "B": False}),
                ({"e", "f"}, {"label": "E", "B": False}),
                ({"f", "a"}, {"label": "E", "B": False}),
                ({"a", "b", "c", "d", "e", "f"}, {"label": "Q1", "R": True}),
                ({"a", "i"}, {"label": "E", "B": False}),
                ({"i", "u"}, {"label": "E", "B": False}),
                ({"u", "j"}, {"label": "E", "B": False}),
                ({"j", "k"}, {"label": "E", "B": True}),
                ({"k", "g"}, {"label": "E", "B": True}),
                ({"g", "b"}, {"label": "E", "B": True}),
                ({"a", "i", "j", "k", "g", "b"}, {"label": "Q2", "R": True}),
                ({"b", "g"}, {"label": "E", "B": False}),
                ({"c", "h"}, {"label": "E", "B": False}),
                ({"g", "h"}, {"label": "E", "B": True}),
                ({"b", "c", "g", "h"}, {"label": "Q3", "R": True}),
                ({"d", "r"}, {"label": "E", "B": False}),
                ({"h", "r"}, {"label": "E", "B": True}),
                ({"c", "d", "h", "r"}, {"label": "Q4", "R": True}),
                ({"e", "m"}, {"label": "E", "B": False}),
                ({"m", "p"}, {"label": "E", "B": True}),
                ({"p", "t"}, {"label": "E", "B": False}),
                ({"t", "q"}, {"label": "E", "B": False}),
                ({"r", "q"}, {"label": "E", "B": True}),
                ({"d", "e", "m", "p", "q", "r"}, {"label": "Q5", "R": True}),
                ({"f", "l"}, {"label": "E", "B": False}),
                ({"l", "m"}, {"label": "E", "B": True}),
                ({"e", "f", "l", "m"}, {"label": "Q6", "R": True}),
                ({"i", "s"}, {"label": "E", "B": False}),
                ({"n", "s"}, {"label": "E", "B": False}),
                ({"n", "o"}, {"label": "E", "B": True}),
                ({"l", "o"}, {"label": "E", "B": True}),
                ({"a", "f", "l", "o", "n", "i"}, {"label": "Q7", "R": True}),
            ],
        )

        expected_new_nodes = [
            (f"z{i}", {"pos": pos, "h": True})
            for i, pos in enumerate(self.excepted_center_edge_nodes_positions)
        ]
        expected_new_edges = [
            ({"z", "a", "z2", "z3"}, {"label": "Q8", "R": True}),
            ({"z", "b", "z2", "z4"}, {"label": "Q9", "R": True}),
            ({"z", "c", "z4", "z0"}, {"label": "Q10", "R": True}),
            ({"z", "d", "z0", "z1"}, {"label": "Q11", "R": True}),
            ({"z", "e", "z1", "z5"}, {"label": "Q12", "R": True}),
            ({"z", "f", "z5", "z3"}, {"label": "Q13", "R": True}),
        ]

        expected_graph = deepcopy(bigger_graph)
        expected_graph._remove_edges(
            [
                {"a", "b", "c", "d", "e", "f"},
                {"a", "b"},
                {"b", "c"},
                {"c", "d"},
                {"d", "e"},
                {"e", "f"},
                {"f", "a"},
            ]
        )

        expected_edges_with_hnodes = []
        for edge, h_node in zip(
            [{"a", "b"}, {"b", "c"}, {"c", "d"}, {"d", "e"}, {"e", "f"}, {"f", "a"}],
            ["z2", "z4", "z0", "z1", "z5", "z3"],
        ):
            first_node = edge.pop()
            second_node = edge.pop()
            expected_edges_with_hnodes.append(
                (
                    {first_node, h_node},
                    {"label": f"g{len(expected_edges_with_hnodes)}", "R": True},
                ),
            )
            expected_edges_with_hnodes.append(
                (
                    {second_node, h_node},
                    {"label": f"g{len(expected_edges_with_hnodes)}", "R": True},
                ),
            )

        expected_graph.extend(
            nodes=expected_new_nodes + [("z", {"pos": (0, 0), "h": False})],
            edges=[({f"z{i}", "z"}, {"label": "E", "B": False}) for i in range(6)]
            + expected_new_edges
            + expected_edges_with_hnodes,
        )

        # bigger_graph.visualize()
        for node in bigger_graph.hyper_nodes:
            if self.production.check(bigger_graph, node):
                hyper_node = node
                self.production.apply(bigger_graph, hyper_node)

        # bigger_graph.visualize()
        self.assertTrue(
            isomorphism.GraphMatcher(
                bigger_graph.nx_graph, expected_graph.nx_graph
            ).is_isomorphic()
        )

    def test_with_boundary(self):
        hyper_graph = HyperGraph(
            nodes=self.proper_graph.nodes,
            edges=[
                ({"v1", "v2"}, {"label": "E", "B": False}),
                ({"v2", "v3"}, {"label": "E", "B": False}),
                ({"v3", "v4"}, {"label": "E", "B": False}),
                ({"v4", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v6"}, {"label": "E", "B": True}),
                ({"v6", "v1"}, {"label": "E", "B": True}),
                ({"v1", "v2", "v3", "v4", "v5", "v6"}, {"label": "Q", "R": True}),
            ],
        )

        hyper_node = hyper_graph.hyper_nodes[0]

        if self.production.check(hyper_graph, hyper_node):
            starting_graph_nodes_positions = [
                params["pos"] for _, params in hyper_graph.nodes
            ]
            hyper_graph = self.production.apply(hyper_graph, hyper_node)
            modified_graph_nodes_positions = [
                params["pos"] for _, params in hyper_graph.nodes
            ]
            self.assertSetEqual(
                set(
                    self.excepted_center_edge_nodes_positions
                    + starting_graph_nodes_positions
                    + [(0, 0)]
                ),
                set(modified_graph_nodes_positions),
            )

            excepted_hanging_nodes_positions = {(-3, 1.5), (3, 1.5), (0, 3)}
            hanging_nodes = [node for node in hyper_graph.nodes if node[1]["h"]]
            self.assertTrue(len(hanging_nodes) == 3)
            created_h_nodes_set = set([h_node[1]["pos"] for h_node in hanging_nodes])
            self.assertSetEqual(created_h_nodes_set, excepted_hanging_nodes_positions)
