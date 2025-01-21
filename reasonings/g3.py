from matplotlib import pyplot as plt

from graph.hypergraph import HyperGraph
from productions import *

if __name__ == "__main__":
    starting_graph = HyperGraph(
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
    starting_graph.visualize()

    brake_prods = [P2(), P11(), P3(), P1()]
    make_breakable_probs = [P7()]
    propagate_probs = [P8(), P22()]


    def prepare_plot(title):
        fig, [ax_before, ax_after] = plt.subplots(1, 2, figsize=(32, 16), dpi=100)
        ax_before.set_title("Before")
        ax_after.set_title("After")
        fig.suptitle(title)
        return ax_before, ax_after


    def try_apply(prod, h_nodes):
        for h_node in h_nodes:
            if prod.check(starting_graph, h_node):
                ax_before, ax_after = prepare_plot(f"{prod.__class__.__name__} on {h_node}")
                starting_graph.visualize(ax_before)
                print(f"Applying production {prod.__class__.__name__} on hyper node {h_node}")
                prod.apply(starting_graph, h_node)
                starting_graph.visualize(ax_after)
                plt.tight_layout()
                plt.show()
                return True
        return False

    def try_apply_list(prods, h_nodes):
        for prod in prods:
            if try_apply(prod, h_nodes):
                return True
        return False


    while True:
        hyper_node_to_break = input("Hyper node: ")

        for h_node in starting_graph.hyper_nodes:
            if h_node == hyper_node_to_break:
                if try_apply_list(make_breakable_probs, [h_node]):
                    break
        else:
            print(f"Couldn't make node '{hyper_node_to_break}' breakable")
            break


        while try_apply_list(propagate_probs, starting_graph.hyper_nodes) or try_apply_list(brake_prods, starting_graph.hyper_nodes) :
            pass