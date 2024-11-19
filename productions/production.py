from abc import ABC

from graph.hypergraph import HyperGraph


class Production(ABC):
    def __init__(self):
        pass

    def check(self, graph: HyperGraph, level: int):
        pass

    def apply(self, graph: HyperGraph) -> HyperGraph:
        pass
