import unittest
from graph.hypergraph import HyperGraph
from productions.p6 import P6
from io import BytesIO
import os
from test_utils import (
    get_current_file_directory,
    create_test_directory,
    apply_production,
    compare_with_baseline,
)

class TestP6(unittest.TestCase):

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
                ("v6", {"pos": (2, 0), "h": True}),
                ("v7", {"pos": (0, 2), "h": True}),
                ("v8", {"pos": (2, 4), "h": True}),
            ],
            edges=[
                ({"v1", "v6"}, {"label": "E", "B": True}),
                ({"v6", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v3"}, {"label": "E", "B": True}),
                ({"v3", "v8"}, {"label": "E", "B": True}),
                ({"v8", "v4"}, {"label": "E", "B": True}),
                ({"v4", "v7"}, {"label": "E", "B": True}),
                ({"v7", "v1"}, {"label": "E", "B": True}),
                ({"v1", "v2", "v3", "v4"}, {"label": "Q", "R": True}),
            ]
        )

        initial_buffer = BytesIO()
        graph.save_figure_to_buffer(initial_buffer)

        graph = apply_production(graph, P6())

        final_buffer = BytesIO()
        graph.save_figure_to_buffer(final_buffer)

        self.assertTrue(compare_with_baseline(initial_buffer, os.path.join(test_dir, "before.png")))
        self.assertTrue(compare_with_baseline(final_buffer, os.path.join(test_dir, "after.png")))


    def test_missing_vertice(self):
        test_dir = create_test_directory(self.test_base_dir, f"{self.__class__.__name__}/missing_vertice")

        graph = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0), "h": False}),
                ("v2", {"pos": (4, 0), "h": False}),
                ("v3", {"pos": (4, 4), "h": False}),
                ("v4", {"pos": (0, 4), "h": False}),
                ("v5", {"pos": (4, 2), "h": True}),
                ("v6", {"pos": (2, 0), "h": True}),
                ("v8", {"pos": (2, 4), "h": True}),
            ],
            edges=[
                ({"v1", "v6"}, {"label": "E", "B": True}),
                ({"v6", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v3"}, {"label": "E", "B": True}),
                ({"v3", "v8"}, {"label": "E", "B": True}),
                ({"v8", "v4"}, {"label": "E", "B": True}),
                ({"v4", "v1"}, {"label": "E", "B": True}),
                ({"v1", "v2", "v3", "v4"}, {"label": "Q", "R": True}),
            ]
        )


        initial_buffer = BytesIO()
        graph.save_figure_to_buffer(initial_buffer)

        graph = apply_production(graph, P6())

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
                ("v6", {"pos": (2, 0), "h": True}),
                ("v7", {"pos": (0, 2), "h": True}),
                ("v8", {"pos": (2, 4), "h": True}),
            ],
            edges=[
                ({"v1", "v6"}, {"label": "E", "B": True}),
                ({"v6", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v3"}, {"label": "E", "B": True}),
                ({"v8", "v4"}, {"label": "E", "B": True}),
                ({"v4", "v7"}, {"label": "E", "B": True}),
                ({"v7", "v1"}, {"label": "E", "B": True}),
                ({"v1", "v2", "v3", "v4"}, {"label": "Q", "R": True}),
            ]
        )

        initial_buffer = BytesIO()
        graph.save_figure_to_buffer(initial_buffer)

        graph = apply_production(graph, P6())

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
                ("v6", {"pos": (2, 0), "h": True}),
                ("v7", {"pos": (0, 2), "h": True}),
                ("v8", {"pos": (2, 4), "h": True}),
            ],
            edges=[
                ({"v1", "v6"}, {"label": "E", "B": True}),
                ({"v6", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v3"}, {"label": "E", "B": True}),
                ({"v3", "v8"}, {"label": "E", "B": True}),
                ({"v8", "v4"}, {"label": "E", "B": True}),
                ({"v4", "v7"}, {"label": "E", "B": True}),
                ({"v7", "v1"}, {"label": "E", "B": True}),
                ({"v1", "v2", "v3", "v4"}, {"label": "Q", "R": False}),
            ]
        )

        initial_buffer = BytesIO()
        graph.save_figure_to_buffer(initial_buffer)

        graph = apply_production(graph, P6())

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
                ("v6", {"pos": (2, 0), "h": True}),
                ("v7", {"pos": (0, 2), "h": True}),
                ("v8", {"pos": (8, 0), "h": False}),
                ("v9", {"pos": (8, 4), "h": False}),
                ("v10", {"pos": (8, 8), "h": False}),
                ("v11", {"pos": (4, 8), "h": False}),
                ("v12", {"pos": (4, 6), "h": True}),
                ("v13", {"pos": (6, 8), "h": True}),
                ("v14", {"pos": (8, 6), "h": True}),
                ("v15", {"pos": (0, 8), "h": False}),
                ("v16", {"pos": (2, 4), "h": True}),
                ("v17", {"pos": (6, 4), "h": True})
            ],
            edges=[
                ({"v1", "v6"}, {"label": "E", "B": True}),
                ({"v6", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v5"}, {"label": "E", "B": False}),
                ({"v5", "v3"}, {"label": "E", "B": False}),
                ({"v3", "v16"}, {"label": "E", "B": False}),
                ({"v16", "v4"}, {"label": "E", "B": False}),
                ({"v4", "v7"}, {"label": "E", "B": True}),
                ({"v7", "v1"}, {"label": "E", "B": True}),
                ({"v2", "v8"}, {"label": "E", "B": True}),
                ({"v8", "v9"}, {"label": "E", "B": True}),
                ({"v9", "v14"}, {"label": "E", "B": True}),
                ({"v14", "v10"}, {"label": "E", "B": True}),
                ({"v10", "v13"}, {"label": "E", "B": True}),
                ({"v13", "v11"}, {"label": "E", "B": True}),
                ({"v11", "v15"}, {"label": "E", "B": True}),
                ({"v15", "v4"}, {"label": "E", "B": True}),
                ({"v3", "v17"}, {"label": "E", "B": False}),
                ({"v17", "v9"}, {"label": "E", "B": False}),
                ({"v3", "v12"}, {"label": "E", "B": False}),
                ({"v12", "v11"}, {"label": "E", "B": False}),
                ({"v1", "v2", "v3", "v4"}, {"label": "Q", "R": True}),
                ({"v3", "v9", "v10", "v11"}, {"label": "Q", "R": True})
            ]
        )

        initial_buffer = BytesIO()
        graph.save_figure_to_buffer(initial_buffer)

        graph = apply_production(graph, P6())

        final_buffer = BytesIO()
        graph.save_figure_to_buffer(final_buffer)

        self.assertTrue(compare_with_baseline(initial_buffer, os.path.join(test_dir, "before.png")))
        self.assertTrue(compare_with_baseline(final_buffer, os.path.join(test_dir, "after.png")))

    def test_production_in_subgraph2(self):
        test_dir = create_test_directory(self.test_base_dir, f"{self.__class__.__name__}/production_in_subgraph2")

        graph = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0), "h": False}),
                ("v2", {"pos": (2, 0), "h": False}),
                ("v3", {"pos": (6, 0), "h": False}),
                ("v4", {"pos": (8, 0), "h": False}),
                ("v5", {"pos": (8, 2), "h": False}),
                ("v6", {"pos": (8, 4), "h": False}),
                ("v7", {"pos": (8, 8), "h": False}),
                ("v8", {"pos": (6, 8), "h": False}),
                ("v9", {"pos": (4, 8), "h": False}),
                ("v10", {"pos": (2, 8), "h": False}),
                ("v11", {"pos": (0, 8), "h": False}),
                ("v12", {"pos": (0, 4), "h": False}),
                ("v13", {"pos": (0, 2), "h": False}),
                ("v14", {"pos": (2, 2), "h": True}),
                ("v15", {"pos": (6, 2), "h": True}),
                ("v16", {"pos": (6, 4), "h": False}),
                ("v17", {"pos": (6, 6), "h": True}),
                ("v18", {"pos": (4, 4), "h": True}),
                ("v19", {"pos": (2, 6), "h": True}),
                ("v20", {"pos": (2, 4), "h": False}),
                ("v21", {"pos": (4, 6), "h": False}),
                ("v22", {"pos": (0, -4), "h": False}),
                ("v23", {"pos": (2, -4), "h": False}),
                ("v24", {"pos": (4, -4), "h": False}),
                ("v25", {"pos": (6, -4), "h": False}),
                ("v26", {"pos": (8, -4), "h": False}),
                ("v27", {"pos": (2, -2), "h": True}),
                ("v28", {"pos": (4, -2), "h": False}),
                ("v29", {"pos": (6, -2), "h": True}),
                ("v30", {"pos": (4, 0), "h": True}),
            ],
            edges=[
                ({"v1", "v2"}, {"label": "E", "B": False}),
                ({"v2", "v30"}, {"label": "E", "B": False}),
                ({"v30", "v3"}, {"label": "E", "B": False}),
                ({"v3", "v4"}, {"label": "E", "B": False}),
                ({"v4", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v6"}, {"label": "E", "B": True}),
                ({"v6", "v7"}, {"label": "E", "B": True}),
                ({"v7", "v8"}, {"label": "E", "B": True}),
                ({"v8", "v9"}, {"label": "E", "B": True}),
                ({"v9", "v10"}, {"label": "E", "B": True}),
                ({"v10", "v11"}, {"label": "E", "B": True}),
                ({"v11", "v12"}, {"label": "E", "B": True}),
                ({"v12", "v13"}, {"label": "E", "B": True}),
                ({"v13", "v1"}, {"label": "E", "B": True}),
                ({"v1", "v22"}, {"label": "E", "B": True}),
                ({"v22", "v23"}, {"label": "E", "B": True}),
                ({"v23", "v24"}, {"label": "E", "B": True}),
                ({"v24", "v25"}, {"label": "E", "B": True}),
                ({"v25", "v26"}, {"label": "E", "B": True}),
                ({"v26", "v4"}, {"label": "E", "B": True}),

                ({"v13", "v14"}, {"label": "E", "B": False}),
                ({"v2", "v14"}, {"label": "E", "B": False}),
                ({"v14", "v20"}, {"label": "E", "B": False}),
                ({"v12", "v20"}, {"label": "E", "B": False}),
                ({"v20", "v19"}, {"label": "E", "B": False}),
                ({"v19", "v10"}, {"label": "E", "B": False}),
                ({"v19", "v21"}, {"label": "E", "B": False}),
                ({"v9", "v21"}, {"label": "E", "B": False}),
                ({"v17", "v21"}, {"label": "E", "B": False}),
                ({"v18", "v21"}, {"label": "E", "B": False}),
                ({"v8", "v17"}, {"label": "E", "B": False}),
                ({"v17", "v16"}, {"label": "E", "B": False}),
                ({"v20", "v18"}, {"label": "E", "B": False}),
                ({"v18", "v16"}, {"label": "E", "B": False}),
                ({"v16", "v15"}, {"label": "E", "B": False}),
                ({"v15", "v3"}, {"label": "E", "B": False}),
                ({"v16", "v6"}, {"label": "E", "B": False}),
                ({"v15", "v5"}, {"label": "E", "B": False}),
                ({"v2", "v27"}, {"label": "E", "B": False}),
                ({"v27", "v23"}, {"label": "E", "B": False}),
                ({"v27", "v28"}, {"label": "E", "B": False}),
                ({"v30", "v28"}, {"label": "E", "B": False}),
                ({"v28", "v24"}, {"label": "E", "B": False}),
                ({"v28", "v29"}, {"label": "E", "B": False}),
                ({"v3", "v29"}, {"label": "E", "B": False}),
                ({"v29", "v25"}, {"label": "E", "B": False}),

                ({"v1", "v2", "v13", "v14"}, {"label": "Q", "R": False}),
                ({"v13", "v14", "v12", "v20"}, {"label": "Q", "R": False}),
                ({"v12", "v20", "v10", "v11"}, {"label": "Q", "R": False}),
                ({"v10", "v9", "v19", "v21"}, {"label": "Q", "R": False}),
                ({"v9", "v8", "v21", "v17"}, {"label": "Q", "R": False}),
                ({"v19", "v21", "v20", "v18"}, {"label": "Q", "R": False}),
                ({"v21", "v17", "v18", "v16"}, {"label": "Q", "R": False}),
                ({"v8", "v7", "v16", "v6"}, {"label": "Q", "R": False}),
                ({"v2", "v3", "v20", "v16"}, {"label": "Q", "R": True}),
                ({"v3", "v4", "v15", "v5"}, {"label": "Q", "R": False}),
                ({"v15", "v5", "v16", "v6"}, {"label": "Q", "R": False}),
                
                ({"v1", "v2", "v22", "v23"}, {"label": "Q", "R": False}),
                ({"v2", "v30", "v28", "v27"}, {"label": "Q", "R": False}),
                ({"v27", "v28", "v24", "v23"}, {"label": "Q", "R": False}),
                ({"v3", "v30", "v28", "v29"}, {"label": "Q", "R": False}),
                ({"v28", "v29", "v24", "v25"}, {"label": "Q", "R": False}),
                ({"v3", "v4", "v25", "v26"}, {"label": "Q", "R": False}),
            ]
        )

        initial_buffer = BytesIO()
        graph.save_figure_to_buffer(initial_buffer)

        graph = apply_production(graph, P6())

        final_buffer = BytesIO()
        graph.save_figure_to_buffer(final_buffer)

        self.assertTrue(compare_with_baseline(initial_buffer, os.path.join(test_dir, "before.png")))
        self.assertTrue(compare_with_baseline(final_buffer, os.path.join(test_dir, "after.png")))
