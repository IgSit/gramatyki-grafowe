import networkx as nx
import matplotlib.pyplot as plt


class HyperGraph:
    """
        Class overlay for nx graph. \n
        **nodes** - list of all nodes in the graph with params
        single node is a tuple:
            - node_id - str
            - dict of attributes: attr_name (str) -> attr_value (any)
        edges - list of all edges in the graph with params
        single edge is a tuple:
            - (node_id, node_id) - from/to nodes - potentially more node ids are supported (for hyper-vertices)
            - dict of attributes: attr_name (str) -> attr_value (any)

        **Convention:** Q* node ids are reserved for hyper-nodes, do not use them.
    """

    def __init__(self,
                 nodes: list[tuple[str, dict]],
                 edges: list[tuple[set[str], dict]]):
        self.nodes = nodes
        self.edges = edges
        self._hyper_node_cnt = 0
        self._node_cnt = len(nodes)

        assert self._check_data(self.nodes, self.edges), "Inconsistent hyper-graph parameters"
        self._construct_nx_graph()

    @classmethod
    def is_hyper_node(cls, node):
        return str(node).startswith('Q')

    def is_hanging_node(self, node) -> bool:
        pass

    def is_breakable(self, node) -> bool:
        pass

    def get_neighbours(self, node):
        return self.nx_graph.neighbors(node)

    def get_next(self, how_many: int) -> list[str]:
        """
            Get names (ids) for x new nodes to be created.
        """
        cnt = self._node_cnt
        names = [f"v{i}" for i in range(cnt, cnt + how_many)]
        self._node_cnt += how_many
        return names
    
    def get_node_attributes(self, node_id: str): # TODO: change self.nodes to dict
        return tuple(filter(lambda x: x[0] == node_id, self.nodes))[0][1]

    def extend(self,
               nodes: list[tuple[str, dict]],
               edges: list[tuple[set[str], dict]]) -> nx.Graph:
        self._node_cnt += len(nodes)
        self.nodes.extend(nodes)
        self.edges.extend(edges)
        assert self._check_data(self.nodes, self.edges), "Inconsistent hyper-graph parameters"
        self.nx_graph.add_nodes_from(nodes)
        self._construct_edges(edges)
        return self.nx_graph

    def visualize(self) -> None:
        node_colors = ['#f88fff' if self.is_hyper_node(node) else '#8fdfff' for node in self.nx_graph.nodes]
        edge_colors = ['#f88fff' if any(self.is_hyper_node(node) for node in edge) else '#8fdfff'
                       for edge in self.nx_graph.edges]
        nx.draw(
            self.nx_graph,
            nx.get_node_attributes(self.nx_graph, 'pos'),
            node_color=node_colors,
            edge_color=edge_colors,
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

    def _add_hyper_edges(self, hyper_edges) -> None:
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
