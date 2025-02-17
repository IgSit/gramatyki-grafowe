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

        **Convention:** X* node ids are reserved for hyper-nodes, do not use them.
    """

    def __init__(self,
                 nodes: list[tuple[str, dict]],
                 edges: list[tuple[set[str], dict]]):
        self.nodes = nodes
        self.hyper_nodes = list()
        self.hyper_positions = list()
        self.hyper_dict = dict()
        self.edges = edges
        self._hyper_node_cnt = 0

        assert self._check_data(self.nodes, self.edges), "Inconsistent hyper-graph parameters"
        self._construct_nx_graph()

    @classmethod
    def is_hyper_node(cls, node):
        return str(node).startswith('X')

    def is_hanging_node(self, node_id: str) -> bool:
        h = self.nx_graph.nodes[node_id].get('h')
        return h if h is not None else False

    def is_breakable(self, node_id: str) -> bool:
        r = self.nx_graph.nodes[node_id].get('R')
        return r if r is not None else False
    
    def is_on_border(self, edge: tuple[str, str]):
        b = self.nx_graph.edges[*edge].get('B')
        return b if b is not None else False

    def get_neighbours(self, node):
        return self.nx_graph.neighbors(node)
    
    def set_node_attrs(self, node: str, attrs: dict) -> None:
        if not HyperGraph.is_hyper_node(node):
            n = list(filter(lambda n: n[0] == node, self.nodes))[0]
            attrs["pos"] = n[1]["pos"]
            self.nodes = list(filter(lambda n: n[0] != node, self.nodes))
            self.nodes.append((node, attrs))

        nx.set_node_attributes(self.nx_graph, {node: attrs})

    def extend(self,
               nodes: list[tuple[str, dict]],
               edges: list[tuple[set[str], dict]]):
        self.nodes.extend(nodes)
        self.edges.extend(edges)
        assert self._check_data(self.nodes, self.edges), "Inconsistent hyper-graph extention parameters"
        self.nx_graph.add_nodes_from(nodes)
        self._construct_edges(edges)

    def shrink(self,
               nodes: list[str],
               edges: list[set[str]]):
        for node in nodes:
            self.nodes.remove(tuple(filter(lambda x: x[0] == node, self.nodes))[0])
        for edge in edges:
            self.edges.remove(tuple(filter(lambda x: tuple(sorted(x[0])) == tuple(sorted(edge)), self.edges))[0])
        assert self._check_data(self.nodes, self.edges), "Inconsistent hyper-graph shrinkage parameters"
        self._remove_edges(edges)
        self.nx_graph.remove_nodes_from(nodes)

    def change_label(self, node: str, labels_to_change: dict):
        if self.is_hyper_node(node):
            hyper_edge = set(self.get_neighbours(node))
            for edge, edge_labels in self.edges:
                if edge == hyper_edge:
                    edge_labels.update(labels_to_change)
                    break
            for v in hyper_edge:
                self.nx_graph.edges[node, v].update(labels_to_change)
        else:
            for n, node_labels in self.nodes:
                if n == node:
                    node_labels.update(labels_to_change)
                    break
        self.nx_graph.nodes[node].update(labels_to_change)

    def calculate_mean_node_position(self, nodes) -> tuple[float, float]:
        positions = [self.nx_graph.nodes[n]['pos'] for n in nodes]
        return sum(p[0] for p in positions) / len(nodes), sum(p[1] for p in positions) / len(nodes)

    def visualize(self, ax=None) -> None:
        node_colors = [('#84298a' if self.is_breakable(node) else '#f88fff') if self.is_hyper_node(node) else ('#1278a1' if self.is_hanging_node(node) else '#8fdfff') for node in self.nx_graph.nodes]
        edge_colors = ['#f88fff' if any(self.is_hyper_node(node) for node in edge) else ('#135210' if self.is_on_border(edge) else '#8fdfff')
                       for edge in self.nx_graph.edges]
        nx.draw(
            self.nx_graph,
            nx.get_node_attributes(self.nx_graph, 'pos'),
            node_color=node_colors,
            edge_color=edge_colors,
            with_labels=True,
            ax=ax
        )
        if not ax:
            plt.show()
        
    def save_figure_to_buffer(self, buffer) -> None:
        node_colors = [('#84298a' if self.is_breakable(node) else '#f88fff') if self.is_hyper_node(node) else ('#1278a1' if self.is_hanging_node(node) else '#8fdfff') for node in self.nx_graph.nodes]
        edge_colors = ['#f88fff' if any(self.is_hyper_node(node) for node in edge) else ('#135210' if self.is_on_border(edge) else '#8fdfff')
                       for edge in self.nx_graph.edges]
        nx.draw(
            self.nx_graph,
            nx.get_node_attributes(self.nx_graph, 'pos'),
            node_color=node_colors,
            edge_color=edge_colors,
            with_labels=True
        )
        
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)

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

    def _remove_edges(self, edges) -> None:
        normal_edges = list(map(tuple, filter(lambda x: len(x) == 2, edges)))
        self.nx_graph.remove_edges_from(normal_edges)
        hyper_edges = list(filter(lambda x: len(x) > 2, edges))
        self._remove_hyper_edges(hyper_edges)
        
    def _add_hyper_edges(self, hyper_edges) -> None:
        """
        Hyper-edges should be created within one hyper-vertex (automatically added). If you need to create multiple
        hyper-edges with different hyper-vertices, you should call this method several times.

        single edge is a tuple:
            - (node_id, node_id) - from/to nodes - potentially more node ids are supported (for hyper-vertices)
            - dict of attributes: attr_name (str) -> attr_value (str/int)
        """
        for hyper_edge, attributes in hyper_edges:
            self._hyper_node_cnt += 1
            hyper_vertex_id = f"X{self._hyper_node_cnt}"
            position = self.calculate_mean_node_position(hyper_edge)
            self.nx_graph.add_node(hyper_vertex_id, pos=position, **attributes)
            idx = 0
            while len(self.hyper_nodes) > 0 and self.hyper_positions[idx][0] < position[0] and idx < len(self.hyper_nodes) - 1:
                idx += 1
            self.hyper_dict[hyper_vertex_id] = position
            self.hyper_positions.insert(idx, position)
            self.hyper_nodes.insert(idx, hyper_vertex_id)
            self.nx_graph.add_edges_from([(hyper_vertex_id, v, attributes) for v in hyper_edge])

    def _remove_hyper_edges(self, hyper_edges) -> None:
        for hyper_edge in hyper_edges:
            hyper_vertex_id = self._find_hyper_node(hyper_edge)
            self.nx_graph.remove_node(hyper_vertex_id)
            self.hyper_nodes.remove(hyper_vertex_id)
            position = self.hyper_dict[hyper_vertex_id]
            self.hyper_dict.pop(hyper_vertex_id)
            self.hyper_positions.remove(position)
    
    def _find_hyper_node(self, hyper_edge) -> str:
        for hyper_node in self.hyper_nodes:
            if tuple(sorted(self.nx_graph.neighbors(hyper_node))) == tuple(sorted(hyper_edge)):
                return hyper_node
        return None
