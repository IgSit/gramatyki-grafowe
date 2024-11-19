from graph.hypergraph import HyperGraph
from productions.p1 import P1

if __name__ == "__main__":
    hyper_graph = HyperGraph(
        nodes=[
            ('v1', {'pos': (0, 0), 'h': 0}),
            ('v2', {'pos': (4, 0), 'h': 0}),
            ('v3', {'pos': (4, 4), 'h': 0}),
            ('v4', {'pos': (0, 4), 'h': 0}),
            ('v5', {'pos': (4, 2), 'h': 1})
        ],
        edges=[
            ({'v1', 'v2'}, {'label': 'E', 'B': 'B1'}),
            ({'v2', 'v5'}, {'label': 'E', 'B': 'B2'}),
            ({'v5', 'v3'}, {'label': 'E', 'B': 'B2'}),
            ({'v3', 'v4'}, {'label': 'E', 'B': 'B3'}),
            ({'v4', 'v1'}, {'label': 'E', 'B': 'B4'}),
            ({'v1', 'v2', 'v3', 'v4'}, {'label': 'Q', 'B': 0, 'R': 1})
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
