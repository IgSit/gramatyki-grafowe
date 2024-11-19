from abc import ABC

from graph.hypergraph import HyperGraph


class Production(ABC):
    def __init__(self):
        pass

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        pass

    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        pass
