import copy

from productions.production import Production
from graph.hypergraph import HyperGraph

class P10(Production):
    def __init__(self):
        super().__init__()

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        if not graph.is_breakable(hyper_node):
            return False

        hyper_edge = set(graph.get_neighbours(hyper_node))
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

    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        ...