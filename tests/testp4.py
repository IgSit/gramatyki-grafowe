from graph.hypergraph import HyperGraph
from productions.p4 import P4

class TestP4():
    def __init__(self):
        pass
    
    def run(self):
        hyper_graph1 = HyperGraph(
            nodes=[
                ("v1", {"pos": (0, 0), "h": False}),
                ("v2", {"pos": (4, 0), "h": False}),
                ("v3", {"pos": (4, 4), "h": False}),
                ("v4", {"pos": (0, 4), "h": False}),
                ("v5", {"pos": (4, 2), "h": True}),
                ("v6", {"pos": (0, 2), "h": True}),
            ],
            edges=[
                ({"v1", "v2"}, {"label": "E", "B": True}),
                ({"v2", "v5"}, {"label": "E", "B": True}),
                ({"v5", "v3"}, {"label": "E", "B": True}),
                ({"v3", "v4"}, {"label": "E", "B": True}),
                ({"v4", "v6"}, {"label": "E", "B": True}),
                ({"v6", "v1"}, {"label": "E", "B": True}),
                ({"v1", "v2", "v3", "v4"}, {"label": "Q", "R": True})
            ]
        )

        production = P4()
        for hyper_node in hyper_graph1.hyper_nodes:
            if production.check(hyper_graph1, hyper_node):
                hyper_graph1.visualize()
                hyper_graph1 = production.apply(hyper_graph1, hyper_node)
                hyper_graph1.visualize()
