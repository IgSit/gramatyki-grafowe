from graph.hypergraph import HyperGraph

if __name__ == "__main__":
    # nx test
    # graph = nx.Graph()
    # graph.add_nodes_from([('v1', {'pos':(0, 0)}),('v2', {'pos':(4, 0)}),('v3', {'pos':(4, 4)}),('v4', {'pos':(0, 4)}),('q', {'pos':(2, 2)})])
    # graph.add_edges_from([('v1','v2'),('v2','v3'),('v3', 'v4'), ('v4','v1')])
    # graph.add_edges_from([('v1','q'),('v2','q'),('v3', 'q'), ('v4', 'q')])
    # nx.draw(graph, nx.get_node_attributes(graph, 'pos'), with_labels=True)
    # plt.show()
    hyper_graph = HyperGraph(
        nodes=[
            ('v0', {'pos':(0, 0)}),
            ('v1', {'pos':(4, 0)}),
            ('v2', {'pos':(4, 4)}),
            ('v3', {'pos':(0, 4)})
        ],
        edges=[
            ({'v0','v1'}, {}),
            ({'v1','v2'}, {}),
            ({'v2', 'v3'}, {}),
            ({'v3','v0'}, {}),
            ({'v0','v1','v2','v3'}, {})
        ]
    )
    hyper_graph.visualize()
