from graph.hypergraph import HyperGraph
from productions.production import Production

class P21(Production):
    def __init__(self):
        super().__init__()

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        return not graph.is_breakable(hyper_node) and len(list(graph.get_neighbours(hyper_node))) == 6

    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        neighbours = set(graph.get_neighbours(hyper_node))
        graph.shrink(nodes=[], edges=[neighbours])
        graph.extend(nodes=[], edges=[(neighbours, {"label": "S", "R": True})])

        return graph