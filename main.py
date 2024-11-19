from graph.hypergraph import HyperGraph
from productions.p1 import P1

if __name__ == "__main__":
    hyper_graph = HyperGraph(
        nodes=[
            ('v1', {'pos': (0, 0), 'h': False}),
            ('v2', {'pos': (4, 0), 'h': False}),
            ('v3', {'pos': (4, 4), 'h': False}),
            ('v4', {'pos': (0, 4), 'h': False}),
            ('v5', {'pos': (4, 2), 'h': True})
        ],
        edges=[
            ({'v1', 'v2'}, {'label': 'E', 'B': True}),
            ({'v2', 'v5'}, {'label': 'E', 'B': True}),
            ({'v5', 'v3'}, {'label': 'E', 'B': True}),
            ({'v3', 'v4'}, {'label': 'E', 'B': True}),
            ({'v4', 'v1'}, {'label': 'E', 'B': True}),
            ({'v1', 'v2', 'v3', 'v4'}, {'label': 'Q', 'R': 1})
        ]
    )
    hyper_graph.visualize()

    productions = [P1()]

    for level in range(1, 4):
        for production in productions:
            node = production.check(hyper_graph, level)  # TODO change to while loop - returns first found, not all
            # TODO or change so it returns all found
            if node:
                hyper_graph = production.apply(hyper_graph)
                hyper_graph.visualize()
                break

    print(hyper_graph.is_hanging_node('v1'))
