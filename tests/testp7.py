from graph.hypergraph import HyperGraph
from productions.p7 import P7

class TestP7():
    def __init__(self):
        pass
    
    def run(self):
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

        production = P7()
        for hyper_node in hyper_graph1.hyper_nodes:
            if production.check(hyper_graph1, hyper_node):
                hyper_graph1.visualize()
                hyper_graph1 = production.apply(hyper_graph1, hyper_node)
                hyper_graph1.visualize()
