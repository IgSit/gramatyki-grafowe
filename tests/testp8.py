import unittest
from graph.hypergraph import HyperGraph
from productions.p8 import P8
from io import BytesIO
import os
from test_utils import (
    get_current_file_directory,
    create_test_directory,
    apply_production,
    compare_with_baseline,
)

class TestP8(unittest.TestCase):

    def setUp(self):
        self.test_base_dir = get_current_file_directory()

    def test_production_executing_correctly(self):
        test_dir = create_test_directory(self.test_base_dir, f"{self.__class__.__name__}/production_executing_correctly")

        graph = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0), "h": False}),
                ("v2", {"pos": (4, 0), "h": False}),
                ("v3", {"pos": (4, 4), "h": False}),
                ("v4", {"pos": (0, 4), "h": False}),
                ("v5", {"pos": (4, 2), "h": True}),
                ("v6", {"pos": (8, 2), "h": False}),
                ("v7", {"pos": (8, 4), "h": False}),
            ],
            edges=[
                ({"v2", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v3"}, {"label": "E", "B": True}),
                ({"v1", "v2", "v3", "v4"}, {"label": "Q", "R": False}),
                ({"v3", "v5", "v6", "v7"}, {"label": "Q", "R": True})
            ]
        )

        initial_buffer = BytesIO()
        graph.save_figure_to_buffer(initial_buffer)

        graph = apply_production(graph, P8())

        final_buffer = BytesIO()
        graph.save_figure_to_buffer(final_buffer)

        self.assertTrue(compare_with_baseline(initial_buffer, os.path.join(test_dir, "before.png")))
        self.assertTrue(compare_with_baseline(final_buffer, os.path.join(test_dir, "after.png")))


    def test_missing_vertice(self):
        test_dir = create_test_directory(self.test_base_dir, f"{self.__class__.__name__}/missing_vertice")

        graph = HyperGraph(
            nodes=[
                ("v2", {"pos": (4, 0), "h": False}),
                ("v3", {"pos": (4, 4), "h": False}),
                ("v4", {"pos": (0, 4), "h": False}),
                ("v5", {"pos": (4, 2), "h": True}),
                ("v6", {"pos": (8, 2), "h": False}),
                ("v7", {"pos": (8, 4), "h": False}),
            ],
            edges=[
                ({"v2", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v3"}, {"label": "E", "B": True}),
                ({"v2", "v3", "v4"}, {"label": "Q", "R": False}),
                ({"v3", "v5", "v6", "v7"}, {"label": "Q", "R": True})
            ]
        )

        initial_buffer = BytesIO()
        graph.save_figure_to_buffer(initial_buffer)

        graph = apply_production(graph, P8())

        final_buffer = BytesIO()
        graph.save_figure_to_buffer(final_buffer)

        self.assertTrue(compare_with_baseline(initial_buffer, os.path.join(test_dir, "before.png")))
        self.assertTrue(compare_with_baseline(final_buffer, os.path.join(test_dir, "after.png")))
        
    def test_missing_edge(self):
        test_dir = create_test_directory(self.test_base_dir, f"{self.__class__.__name__}/missing_edge")

        graph = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0), "h": False}),
                ("v2", {"pos": (4, 0), "h": False}),
                ("v3", {"pos": (4, 4), "h": False}),
                ("v4", {"pos": (0, 4), "h": False}),
                ("v5", {"pos": (4, 2), "h": True}),
                ("v6", {"pos": (8, 2), "h": False}),
                ("v7", {"pos": (8, 4), "h": False}),
            ],
            edges=[
                ({"v5", "v3"}, {"label": "E", "B": True}),
                ({"v1", "v2", "v3", "v4"}, {"label": "Q", "R": False}),
                ({"v3", "v5", "v6", "v7"}, {"label": "Q", "R": True})
            ]
        )

        initial_buffer = BytesIO()
        graph.save_figure_to_buffer(initial_buffer)

        graph = apply_production(graph, P8())

        final_buffer = BytesIO()
        graph.save_figure_to_buffer(final_buffer)

        self.assertTrue(compare_with_baseline(initial_buffer, os.path.join(test_dir, "before.png")))
        self.assertTrue(compare_with_baseline(final_buffer, os.path.join(test_dir, "after.png")))

    def test_wrong_label_value(self):
        test_dir = create_test_directory(self.test_base_dir, f"{self.__class__.__name__}/wrong_label_value")

        graph = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0), "h": False}),
                ("v2", {"pos": (4, 0), "h": False}),
                ("v3", {"pos": (4, 4), "h": False}),
                ("v4", {"pos": (0, 4), "h": False}),
                ("v5", {"pos": (4, 2), "h": True}),
                ("v6", {"pos": (8, 2), "h": False}),
                ("v7", {"pos": (8, 4), "h": False}),
            ],
            edges=[
                ({"v2", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v3"}, {"label": "E", "B": True}),
                ({"v1", "v2", "v3", "v4"}, {"label": "Q", "R": False}),
                ({"v3", "v5", "v6", "v7"}, {"label": "Q", "R": False})
            ]
        )

        initial_buffer = BytesIO()
        graph.save_figure_to_buffer(initial_buffer)

        graph = apply_production(graph, P8())

        final_buffer = BytesIO()
        graph.save_figure_to_buffer(final_buffer)

        self.assertTrue(compare_with_baseline(initial_buffer, os.path.join(test_dir, "before.png")))
        self.assertTrue(compare_with_baseline(final_buffer, os.path.join(test_dir, "after.png")))

    def test_production_in_subgraph(self):
        test_dir = create_test_directory(self.test_base_dir, f"{self.__class__.__name__}/production_in_subgraph")

        graph = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0), "h": False}),
                ("v2", {"pos": (4, 0), "h": False}),
                ("v3", {"pos": (4, 4), "h": False}),
                ("v4", {"pos": (0, 4), "h": False}),
                ("v5", {"pos": (4, 2), "h": True}),
                ("v6", {"pos": (8, 2), "h": True}),
                ("v7", {"pos": (8, 4), "h": False}),
                ("v8", {"pos": (8, 0), "h": False}),
                ("v9", {"pos": (12, 0), "h": False}),
                ("v10", {"pos": (12, 4), "h": False}),
            ],
            edges=[
                ({"v2", "v5"}, {"label": "E", "B": False}),
                ({"v5", "v3"}, {"label": "E", "B": False}),
                ({"v1", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v8"}, {"label": "E", "B": True}),
                ({"v8", "v9"}, {"label": "E", "B": True}),
                ({"v9", "v10"}, {"label": "E", "B": True}),
                ({"v10", "v7"}, {"label": "E", "B": True}),
                ({"v7", "v3"}, {"label": "E", "B": True}),
                ({"v3", "v4"}, {"label": "E", "B": True}),
                ({"v4", "v1"}, {"label": "E", "B": True}),
                ({"v5", "v6"}, {"label": "E", "B": False}),
                ({"v6", "v8"}, {"label": "E", "B": False}),
                ({"v6", "v7"}, {"label": "E", "B": False}),
                ({"v1", "v2", "v3", "v4"}, {"label": "Q", "R": False}),
                ({"v3", "v5", "v6", "v7"}, {"label": "Q", "R": True}),
                ({"v7", "v8", "v9", "v10"}, {"label": "Q", "R": False}),
                ({"v2", "v5", "v6", "v8"}, {"label": "Q", "R": True})
            ]
        )

        initial_buffer = BytesIO()
        graph.save_figure_to_buffer(initial_buffer)

        graph = apply_production(graph, P8())

        final_buffer = BytesIO()
        graph.save_figure_to_buffer(final_buffer)

        self.assertTrue(compare_with_baseline(initial_buffer, os.path.join(test_dir, "before.png")))
        self.assertTrue(compare_with_baseline(final_buffer, os.path.join(test_dir, "after.png")))
