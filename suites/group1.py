from graph.hypergraph import HyperGraph
from productions.p1 import P1
from productions.p2 import P2
from productions.p21 import P21
from productions.p3 import P3
from productions.p7 import P7
from productions.p8 import P8
from productions.p9 import P9

if __name__ == '__main__':
    hyper_graph = HyperGraph(
        nodes=[
            ("v1", {"pos": (-4, 0), "h": False}),
            ("v2", {"pos": (-2, 3), "h": False}),
            ("v3", {"pos": (2, 3), "h": False}),
            ("v4", {"pos": (4, 0), "h": False}),
            ("v5", {"pos": (2, -3), "h": False}),
            ("v6", {"pos": (-2, -3), "h": False}),

            ("v7", {"pos": (-7, -7), "h": False}),
            ("v8", {"pos": (7, -7), "h": False}),
            ("v9", {"pos": (7, 7), "h": False}),
            ("v10", {"pos": (-7, 7), "h": False}),
            ("v11", {"pos": (-7, 0), "h": False}),
            ("v12", {"pos": (7, 0), "h": False}),
        ],
        edges=[
            ({"v1", "v2"}, {"label": "E", "B": False}),
            ({"v2", "v3"}, {"label": "E", "B": False}),
            ({"v3", "v4"}, {"label": "E", "B": False}),
            ({"v4", "v5"}, {"label": "E", "B": False}),
            ({"v5", "v6"}, {"label": "E", "B": False}),
            ({"v6", "v1"}, {"label": "E", "B": False}),
            ({"v1", "v2", "v3", "v4", "v5", "v6"}, {"label": "S", "R": False}),

            ({"v10", "v11"}, {"label": "E", "B": True}),
            ({"v11", "v7"}, {"label": "E", "B": True}),
            ({"v7", "v8"}, {"label": "E", "B": True}),
            ({"v8", "v12"}, {"label": "E", "B": True}),
            ({"v12", "v9"}, {"label": "E", "B": True}),
            ({"v9", "v10"}, {"label": "E", "B": True}),

            ({"v2", "v10"}, {"label": "E", "B": False}),
            ({"v1", "v11"}, {"label": "E", "B": False}),
            ({"v6", "v7"}, {"label": "E", "B": False}),
            ({"v5", "v8"}, {"label": "E", "B": False}),
            ({"v4", "v12"}, {"label": "E", "B": False}),
            ({"v3", "v9"}, {"label": "E", "B": False}),

            ({"v1", "v2", "v10", "v11"}, {"label": "Q", "R": False}),
            ({"v1", "v6", "v7", "v11"}, {"label": "Q", "R": False}),
            ({"v5", "v8", "v7", "v6"}, {"label": "Q", "R": False}),
            ({"v12", "v4", "v5", "v8"}, {"label": "Q", "R": False}),
            ({"v4", "v3", "v9", "v12"}, {"label": "Q", "R": False}),
            ({"v2", "v3", "v9", "v10"}, {"label": "Q", "R": False}),
            ],
    )

    hyper_graph.visualize()

    productions = [(P21(), False, None),
                   (P9(), True, None),
                   (P7(), False, (2.5, 0.0)),
                   (P8(), True, None),
                   (P2(), True, None),
                   (P3(), True, None),
                   (P1(), True, None),
                   (P7(), False, (3.375, 0.0)),
                   (P8(), True, None),
                   (P2(), True, None),
                   (P3(), True, None),
                   (P1(), True, None)
                   ]

    for production, rerun, preferred_node_pos in productions:
        initial = True
        while initial or rerun:
            initial = False
            changed = False
            print(f"(Re)running check for {production.__class__.__name__}")
            hyper_nodes = hyper_graph.hyper_nodes
            if preferred_node_pos:
                idx = hyper_graph.hyper_positions.index(preferred_node_pos)
                preferred_node = hyper_graph.hyper_nodes[idx]
                if production.check(hyper_graph, preferred_node):
                    print(f"Production {production.__class__.__name__} applied.")
                    hyper_graph = production.apply(hyper_graph, preferred_node)
                    hyper_graph.visualize()
                    changed = True
                    break
            for hyper_node in hyper_nodes:
                if production.check(hyper_graph, hyper_node):
                    print(f"Production {production.__class__.__name__} applied.")
                    hyper_graph = production.apply(hyper_graph, hyper_node)
                    hyper_graph.visualize()
                    changed = True
                    break
            if not changed:
                break

    print(hyper_graph.hyper_positions)
