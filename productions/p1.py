from productions.production import Production
from graph.hypergraph import HyperGraph


class P1(Production):
    def check(self, graph: HyperGraph):
        candidates = self._get_candidates(graph)
        return len(candidates) > 0
    
    def apply(self, graph: HyperGraph):
        return 
    
    def _get_candidates(self, graph: HyperGraph):
        return list(filter(lambda candidate: self._check_candidate(candidate, graph), graph.edges))
    
    def _check_candidate(self, candidate: tuple[set, dict], graph: HyperGraph):
        nodes, attr = candidate
        return attr['label'] == 'Q' and attr['R'] == 1 and len(nodes) == 4 and all(map(lambda x: graph.get_node_attributes(x)['h'] == 0, nodes)) # TODO: check structural condition and refactor