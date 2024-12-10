import copy
import itertools

from productions.production import Production
from graph.hypergraph import HyperGraph

class P10(Production):
    def __init__(self):
        super().__init__()

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        if not graph.is_breakable(hyper_node):
            return False

        hyper_edge = set(graph.get_neighbours(hyper_node))
        for edge, labels in graph.edges:
            if edge == hyper_edge:
                if labels["label"] != "S":
                    return False
                break

        node2labels = {node:labels for node, labels in graph.nodes}
        for node in hyper_edge:
            labels = node2labels[node]
            if labels['h']:
                return False

        additional_node, _ = self._find_additional_node_in_chain(hyper_edge, graph)
        if additional_node is None or not node2labels[additional_node]['h']:
            return False
        return True

    @staticmethod
    def _find_additional_node_in_chain(chain_parts, graph: HyperGraph):

        def get_neighbours(n):
            for neighbour in graph.get_neighbours(n):
                if neighbour.startswith('X'):
                    continue
                yield neighbour

        chain_parts = copy.deepcopy(chain_parts)
        chain = [chain_parts.pop()]
        additional_node = None

        while len(chain_parts) > 0:
            chain_head = chain[-1]
            for node in get_neighbours(chain_head):
                if node in chain_parts:
                    chain.append(node)
                    chain_parts.remove(node)
                    break
            else:
                if additional_node is not None:
                    return None, None  # At least 2 additional nodes
                for node in get_neighbours(chain_head):
                    for nodeNode in get_neighbours(node):
                        if nodeNode in chain_parts:
                            additional_node = node
                            chain.append(node)
                            chain.append(nodeNode)
                            chain_parts.remove(nodeNode)
                        break
                    if additional_node is not None:
                        break

        if additional_node is None:
            for node in get_neighbours(chain[-1]):
                if node == chain[0]:
                    return None, None
                for nodeNode in get_neighbours(node):
                    if nodeNode == chain[0]:
                        chain.append(node)
                        return node, chain
        else:
            for node in get_neighbours(chain[-1]):
                if node == chain[0]:
                    return additional_node, chain
        return None, None

    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        hyper_edge = set(graph.get_neighbours(hyper_node))
        edges_to_remove = [hyper_edge]
        edges_to_add = []
        nodes_to_add = []

        node2labels = {node:labels for node, labels in graph.nodes}
        edge2labels = {frozenset(edge):labels for edge, labels in graph.edges}

        center_node = self._create_center_node(hyper_edge, node2labels)
        nodes_to_add.append(center_node)

        additional_node, chain = self._find_additional_node_in_chain(hyper_edge, graph)

        extended_chain = []

        for node1, node2 in itertools.pairwise(chain + chain[:1]):
            extended_chain.append(node1)
            if node1 == additional_node or node2 == additional_node:
                continue

            is_boundary_edge = edge2labels[frozenset([node1, node2])]["B"]

            new_node_x = (node2labels[node1]["pos"][0] + node2labels[node2]["pos"][0]) / 2
            new_node_y = (node2labels[node1]["pos"][1] + node2labels[node2]["pos"][1]) / 2
            new_node = f"v{new_node_x:.3f}x{new_node_y:.3f}y"
            extended_chain.append(new_node)
            nodes_to_add.append((new_node, {"pos": (new_node_x, new_node_y), "h": not is_boundary_edge}))

            edges_to_remove.append({node1, node2})
            edges_to_add.append(({node1, new_node}, {"label": "E", "B": is_boundary_edge}))
            edges_to_add.append(({node2, new_node}, {"label": "E", "B": is_boundary_edge}))

        for i in range(6):
            node1 = extended_chain[(1 + 2*i) % len(extended_chain)]
            node2 = extended_chain[(2 + 2*i) % len(extended_chain)]
            node3 = extended_chain[(3 + 2*i) % len(extended_chain)]

            edges_to_add.append(({node1, center_node[0]}, {"label": "E", "B": False}))
            edges_to_add.append(({node1, node2, node3, center_node[0]}, {"label": "Q", "R": False}))

        graph.shrink(nodes=[], edges=edges_to_remove)
        graph.extend(nodes_to_add, edges_to_add)
        graph.change_label(additional_node, {"h": False})

        return graph

    @staticmethod
    def _create_center_node(hyper_edge, node2labels):
        center_node_x = [node2labels[n]["pos"][0] for n in hyper_edge]
        center_node_x = sum(center_node_x) / len(center_node_x)
        center_node_y = [node2labels[n]["pos"][1] for n in hyper_edge]
        center_node_y = sum(center_node_y) / len(center_node_y)

        return f"v{center_node_x:.3f}x{center_node_y:.3f}y", {"pos": (center_node_x, center_node_y), "h": False}

