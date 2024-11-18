import networkx as nx
import matplotlib.pyplot as plt

class HyperGraph:
    def __init__(self, nodes: list[tuple[str|int, dict[str:tuple[float, float]|str]]], edges: list[set[str|int]]):
        self.nodes = nodes
        self.edges = edges
        assert self._check_data(), "Inconsistent hypergraph parametrs"
        self.nx_graph = self._construct_nx_graph()
        
    def _check_data(self) -> bool:
        node_ids = set(map(lambda x: x[0], self.nodes))
        for edge in self.edges:
            for v in edge:
                if v not in node_ids:
                    print(f"Edge from unknown node {v} not present in nodes")
                    return False
        return True

    def _construct_nx_graph(self) -> nx.Graph:
        pass

    def visualize(self):
        nx.draw(self.nx_graph)
        plt.show()

class Production:
    def __init__(self, left_side_hypergraph: HyperGraph):
        self.left_side_hypergraph = left_side_hypergraph

    def check() -> bool:
        pass
    
    def apply() -> HyperGraph:
        pass

if __name__ == "__main__":
    # nx test
    graph = nx.Graph()
    graph.add_nodes_from([('v1', {'pos':(0, 0)}),('v2', {'pos':(4, 0)}),('v3', {'pos':(4, 4)}),('v4', {'pos':(0, 4)}),('q', {'pos':(2, 2)})])
    graph.add_edges_from([('v1','v2'),('v2','v3'),('v3', 'v4'), ('v4','v1')])
    graph.add_edges_from([('v1','q'),('v2','q'),('v3', 'q'), ('v4', 'q')])
    nx.draw(graph, nx.get_node_attributes(graph, 'pos'), with_labels=True)
    plt.show()