from abc import ABC

from graph.hypergraph import HyperGraph


class Production(ABC):
    def __init__(self):
        pass

    def check(self, left_side_graph: HyperGraph) -> bool:
        pass

    def apply(self) -> HyperGraph:
        pass
