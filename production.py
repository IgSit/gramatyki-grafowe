from abc import ABC

from hypergraph import HyperGraph


class Production(ABC):
    def __init__(self, left_side_graph: HyperGraph):
        self.left_side_graph = left_side_graph

    def check(self) -> bool:
        pass

    def apply(self) -> HyperGraph:
        pass
