from graph.hypergraph import HyperGraph
from productions.p1 import P1

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
            ('v1', {'pos':(0, 0), 'h':0}),
            ('v2', {'pos':(4, 0), 'h':0}),
            ('v3', {'pos':(4, 4), 'h':0}),
            ('v4', {'pos':(0, 4), 'h':0}),
            ('v5', {'pos':(4, 2), 'h':1})
        ],
        edges=[
            ({'v1','v2'}, {'label':'E', 'B':'B1'}),
            ({'v2','v5'}, {'label':'E', 'B':'B2'}),
            ({'v5','v3'}, {'label':'E', 'B':'B2'}),
            ({'v3', 'v4'}, {'label':'E', 'B':'B3'}),
            ({'v4','v1'}, {'label':'E', 'B':'B4'}),
            ({'v1','v2','v3','v4'}, {'label':'Q', 'B':0, 'R':1})
        ]
    )
    # hyper_graph.visualize()

