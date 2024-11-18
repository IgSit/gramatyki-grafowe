import networkx as nx
import matplotlib.pyplot as plt
from functools import reduce

class HyperGraph:
    def __init__(self, nodes: list[tuple[str|int, dict[str:tuple[float, float]|str]]], edges: list[tuple[set[str|int]], dict[str: str]]):
        self.nodes = nodes
        self.edges = edges
        assert self._check_data(), "Inconsistent hypergraph parametrs"
        self.nx_graph = self._construct_nx_graph()
        
    def _check_data(self) -> bool:
        node_ids = set(map(lambda x: x[0], self.nodes))
        for edge, _ in self.edges:
            for v in edge:
                if v not in node_ids:
                    print(f"Edge from unknown node {v} not present in nodes")
                    return False
        return True

    def _construct_nx_graph(self) -> nx.Graph:
        graph = nx.Graph()
        graph.add_nodes_from(self.nodes)

        edges = list(map(lambda x: (*x[0], x[1]), filter(lambda x: len(x[0]) == 2, self.edges)))

        graph.add_edges_from(edges)

        hyperedges = list(filter(lambda x: len(x[0]) > 2, self.edges))
        self._add_hyperedges(graph, hyperedges)
        return graph

    def _add_hyperedges(self, graph: nx.Graph, hyperedges: list[tuple[set[str|int], dict[str:str]]]):
        assert len(hyperedges) == 1,"WIP: 'Q' must be unique per hyperedge" # FIXME
        for hyperedge, attributes in hyperedges:
            positions = [graph.nodes[v]['pos'] for v in hyperedge]
            pos_x = (max(map(lambda x: x[0], positions)) - min(map(lambda x: x[0], positions))) / 2
            pos_y = (max(map(lambda x: x[1], positions)) - min(map(lambda x: x[1], positions))) / 2
            graph.add_node('Q', pos=(pos_x, pos_y))
            graph.add_edges_from([('Q', v, attributes) for v in hyperedge])

    def visualize(self):
        nx.draw(self.nx_graph, nx.get_node_attributes(self.nx_graph, 'pos'), with_labels=True)
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
    # graph = nx.Graph()
    # graph.add_nodes_from([('v1', {'pos':(0, 0)}),('v2', {'pos':(4, 0)}),('v3', {'pos':(4, 4)}),('v4', {'pos':(0, 4)}),('q', {'pos':(2, 2)})])
    # graph.add_edges_from([('v1','v2'),('v2','v3'),('v3', 'v4'), ('v4','v1')])
    # graph.add_edges_from([('v1','q'),('v2','q'),('v3', 'q'), ('v4', 'q')])
    # nx.draw(graph, nx.get_node_attributes(graph, 'pos'), with_labels=True)
    # plt.show()
    hypergraph = HyperGraph(
        nodes=[('v1', {'pos':(0, 0)}),('v2', {'pos':(4, 0)}),('v3', {'pos':(4, 4)}),('v4', {'pos':(0, 4)})],
        edges=[({'v1','v2'}, dict()),({'v2','v3'}, dict()),({'v3', 'v4'}, dict()), ({'v4','v1'}, dict()), ({'v1','v2','v3','v4'}, dict())])
    hypergraph.visualize()