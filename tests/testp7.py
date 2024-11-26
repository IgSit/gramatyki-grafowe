import unittest
from graph.hypergraph import HyperGraph
from productions.p7 import P7

class TestP7(unittest.TestCase):
    def test(self):
        # given
        hyper_graph1 = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0), "h": False}),
                ("v2", {"pos": (4, 0), "h": False}),
                ("v3", {"pos": (4, 4), "h": False}),
                ("v4", {"pos": (0, 4), "h": False})
            ],
            edges=[
                ({"v1", "v2", "v3", "v4"}, {"label": "Q", "R": False})
            ]
        )

        # when
        production = P7()
        for hyper_node in hyper_graph1.hyper_nodes:
            if production.check(hyper_graph1, hyper_node):
                hyper_graph1 = production.apply(hyper_graph1, hyper_node)

        # then
        for hyper_node in hyper_graph1.hyper_nodes:
            self.assertTrue(hyper_graph1.is_breakable(hyper_node))
        
