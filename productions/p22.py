import networkx as nx

from graph.hypergraph import HyperGraph
from productions.production import Production


# Config
edge_logs = True
condition_logs = False

class P22(Production):
    def __init__(self):
        super().__init__()

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        # Production only for hyper_node elements marked to be broken
        if not graph.is_hyper_node(hyper_node) or not graph.is_breakable(hyper_node):
            return False
        
        # Taking neighbours for hyper_node
        neighbours = self._get_hyper_node_neighbours(graph, hyper_node)

        # Checking every hyper_node in graph 
        for h_node in graph.hyper_nodes:
            if hyper_node == h_node:
                continue
            #print(f"H_node: {hyper_node}-{h_node}")
            neighbours2 = self._get_hyper_node_neighbours(graph, h_node)
            # if it is adjacent to our hyper_node
            common_nodes = [node for node in neighbours if node in neighbours2]
            cond1 = len(common_nodes) == 1
            # Find hanging node in subgraph
            hanging_nodes = self._get_hanging_nodes(graph, neighbours2)
            #print(hanging_node)
            cond2 = hanging_nodes and not graph.is_breakable(h_node)
            # and if this hanging node is in our hyper_node neighbourhood
            cond3 = [node for node in hanging_nodes if node in neighbours]
            if(condition_logs):
                print(f"cond1: {cond1}")
                print(f"cond2: {cond2}")
                print(f"cond3: {cond3}")
            if cond1 and cond2 and cond3:
                print(f"Accept for: {hyper_node}")
                return True
        return False
    
    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        # Production only for hyper_node elements marked to be broken
        if not graph.is_hyper_node(hyper_node) or not graph.is_breakable(hyper_node):
            return graph
        if(edge_logs):
            print("Before:")
            for edge in graph.edges:
                print(edge)

        neighbours = self._get_hyper_node_neighbours(graph, hyper_node)

        # Checking every hyper_node in graph 
        for h_node in graph.hyper_nodes:
            neighbours2 = self._get_hyper_node_neighbours(graph, h_node)
            # if it is adjacent to our hyper_node
            common_nodes = [node for node in neighbours if node in neighbours2]
            cond1 = len(common_nodes) == 1
            # Find hanging node in subgraph
            hanging_nodes = self._get_hanging_nodes(graph, neighbours2)
            cond2 = hanging_nodes and not graph.is_breakable(h_node)
            # and if this hanging node is in our hyper_node neighbourhood
            cond3 = [node for node in hanging_nodes if node in neighbours]
            if cond1 and cond2 and cond3:
                node_to_change = self._find_node(graph, h_node)
                # Code inconsistency - if you change in nodes you don't change on graph and vice versa
                # Lack of function graph.update()
                graph.nx_graph.nodes[h_node]['R'] = True
                node_to_change[1]['R'] = True
        if(edge_logs):
            print("After:")
            for edge in graph.edges:
                print(edge)
        return graph

    def _get_hanging_nodes(self, graph: HyperGraph, neighbours: list[str]) -> bool:
        # 'node' - 'hanging node' - 'node'
        hangings = []
        for node in neighbours:
            neigh = list(graph.get_neighbours(node))
            if len(neigh) < 2:
                continue
            for x in neigh:
                if graph.is_hanging_node(x):
                    hangings.append(x)
        return list(set(hangings))
    
    def _get_hyper_node_neighbours(self, graph: HyperGraph, hyper_node: str) -> list:
        if len(hyper_node) < 2:
            return []
        changed_name = 'Q' + hyper_node[1:]
        for edge in graph.edges:
            if edge[1]['label'] == changed_name:
                return list(edge[0])
        return []
    
    def _find_node(self, graph: HyperGraph, node: str) -> tuple:
        changed_name = 'Q' + node[1:]
        for x in graph.edges:
            if x[1]['label'] == changed_name:
                return x
        return None 

                    






