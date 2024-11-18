import networkx as nx
import matplotlib.pyplot as plt


class HyperGraph:
    """
        Class overlay for nx graph. \n
        **nodes** - list of all nodes in the graph with params
        single node is a tuple:
            - node_id - str/int
            - dict of attributes: attr_name (str) -> attr_value (str/int)
        edges - list of all edges in the graph with params
        single edge is a tuple:
            - (node_id, node_id) - from/to nodes - potentially more node ids are supported (for hyper-vertices)
            - dict of attributes: attr_name (str) -> attr_value (str/int)

        **Convention:** Q* node ids are reserved for hyper-nodes, do not use them.
    """

    def __init__(self,
                 nodes: list[tuple[str | int, dict[str:tuple[float, float] | str]]],
                 edges: list[tuple[set[str | int]], dict[str: str | int]]):
        self.nodes = nodes
        self.edges = edges
        self._hyper_node_cnt = 0

        assert self._check_data(self.nodes, self.edges), "Inconsistent hyper-graph parameters"
        self._construct_nx_graph()

    def extend(self,
               nodes: list[tuple[str | int, dict[str:tuple[float, float] | str]]],
               edges: list[tuple[set[str | int]], dict[str: str | int]]) -> nx.Graph:
        self.nodes.extend(nodes)
        self.edges.extend(edges)
        assert self._check_data(self.nodes, self.edges), "Inconsistent hyper-graph parameters"
        self.nx_graph.add_nodes_from(nodes)
        self._construct_edges(edges)
        return self.nx_graph

    def visualize(self) -> None:
        nx.draw(
            self.nx_graph,
            nx.get_node_attributes(self.nx_graph, 'pos'),
            with_labels=True
        )
        plt.show()

    @classmethod
    def _check_data(cls, nodes, edges) -> bool:
        """
            Graph creation validation - checks that all edges have nodes defined.
        """
        node_ids = set(map(lambda x: x[0], nodes))
        for edge, _ in edges:
            for v in edge:
                if v not in node_ids:
                    print(f"Edge from unknown node {v} not present in nodes")
                    return False
        return True

    def _construct_nx_graph(self) -> None:
        """
            Creates nodes, edges and hyper-edges from provided lists.
        """
        self.nx_graph = nx.Graph()
        self.nx_graph.add_nodes_from(self.nodes)
        self._construct_edges(self.edges)

    def _construct_edges(self, edges) -> None:
        normal_edges = list(map(lambda x: (*x[0], x[1]), filter(lambda x: len(x[0]) == 2, edges)))
        self.nx_graph.add_edges_from(normal_edges)
        hyper_edges = list(filter(lambda x: len(x[0]) > 2, edges))
        self._add_hyper_edges(hyper_edges)

    def _add_hyper_edges(self,
                         hyper_edges: list[tuple[set[str | int], dict[str:str]]]) -> None:
        """
        Hyper-edges should be created within one hyper-vertex (automatically added). If you need to create multiple
        hyper-edges with different hyper-vertices, you should call this method several times.

        single edge is a tuple:
            - (node_id, node_id) - from/to nodes - potentially more node ids are supported (for hyper-vertices)
            - dict of attributes: attr_name (str) -> attr_value (str/int)
        """
        for hyper_edge, attributes in hyper_edges:
            positions = [self.nx_graph.nodes[v]['pos'] for v in hyper_edge]
            pos_x = (max(map(lambda x: x[0], positions)) - min(map(lambda x: x[0], positions))) / 2
            pos_y = (max(map(lambda x: x[1], positions)) - min(map(lambda x: x[1], positions))) / 2
            self._hyper_node_cnt += 1
            hyper_vertex_id = f"Q{self._hyper_node_cnt}"
            self.nx_graph.add_node(hyper_vertex_id, pos=(pos_x, pos_y))
            self.nx_graph.add_edges_from([(hyper_vertex_id, v, attributes) for v in hyper_edge])
