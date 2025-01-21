from graph.hypergraph import HyperGraph
from productions import *
import networkx as nx
from matplotlib import pyplot as plt

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

def try_apply_prods(prods, hyper_node):
    for prod in prods:
        if prod.check(hyper_graph, hyper_node):
            fig, [ax_before, ax_after] = plt.subplots(1, 2, figsize=(32, 16), dpi=100)
            ax_before.set_title("Before")
            ax_after.set_title("After")
            fig.suptitle(f"{prod.__class__.__name__} on {hyper_node}")
            hyper_graph.visualize(ax_before)
            print(f"Applying production {prod.__class__.__name__} on hyper node {hyper_node}")
            prod.apply(hyper_graph, hyper_node)
            hyper_graph.visualize(ax_after)
            plt.tight_layout()
            plt.show()
            return True
    return False

break_prods = [P1(), P2(), P3(), P4(), P5(), P6(), P9(), P10(), P11(), P12()]
set_break_prods = [P7(), P21()]
propagate_prods = [P8(), P22()]

hyper_graph.visualize()

while True:
    to_break = input("Hyper node: ")
    try_apply_prods(set_break_prods, to_break)

    while any(try_apply_prods(prods, h) \
              for prods in [propagate_prods, break_prods] \
              for h in hyper_graph.hyper_nodes):
        pass

