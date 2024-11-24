import networkx as nx

from graph.hypergraph import HyperGraph
from productions.production import Production


class P12(Production):
    def __init__(self):
        super().__init__()

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        #is hypernode marked for breaking
        cond1 = graph.is_breakable(hyper_node)

        #is hypernode linked to 6 vertices
        hypernode_neigh_vertices = tuple(graph.get_neighbours(hyper_node))
        cond2 = len(hypernode_neigh_vertices) == 6

        incomplete_vertices, missing_vertice = self.__get_incomplete_vertices(graph, hyper_node)

        #before we move on - check counts - we should have none missing, four incomplete due to hanging node not being neighbours

        if len(incomplete_vertices) != 4 or missing_vertice is not None:
            return False

        ignored_vertices = [*incomplete_vertices]

        for v in hypernode_neigh_vertices:
            if v not in ignored_vertices:
                if graph.nx_graph.nodes.get(v).get('h'):
                    return False

        # edges we don't have are - incomplete[0] - 'something1' - incomplete[1], incomplete[2] - 'something2' - incomplete[3]
        # we don't know which ones though - we need to find common neighbour that is not connected to hyperedge between them
        # probably - check if we have a node that is:
        # 1. neighbor
        # 2. located between the two

        ignored_vertices = [*incomplete_vertices]
        checked_vertices = [*list(graph.get_neighbours(incomplete_vertices[0])),
                            *list(graph.get_neighbours(incomplete_vertices[1])),
                            *list(graph.get_neighbours(incomplete_vertices[2])),
                            *list(graph.get_neighbours(incomplete_vertices[3]))]

        #those not connected to graph (and not the missing one)
        unconnected_vertices = []

        for v in checked_vertices:
            if (v not in ignored_vertices
                    and v not in hypernode_neigh_vertices
                    # we want only real vertices, not hyper-vertices if it's connected to any
                    and v[0]=='v'
                    and v not in unconnected_vertices):
                unconnected_vertices.append(v)


        # #now we need to check if we have any matching "somethings"
        # #we will do that by checking if the node there is in correct position, and is linked to correct vertices
        somethings = self.__get_missing_vertices(graph, incomplete_vertices, unconnected_vertices)

        cond3 = len(somethings) == 2

        return cond1 and cond2 and cond3

    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        hypernode_neigh_vertices = tuple(graph.get_neighbours(hyper_node))
        incomplete_vertices, _ = self.__get_incomplete_vertices(graph, hyper_node)
        print(incomplete_vertices)
        unconnected_vertices = self.get_unconnected_vertices(graph, hypernode_neigh_vertices, incomplete_vertices)
        something1, something2 = self.__get_missing_vertices(graph, incomplete_vertices, unconnected_vertices)

        #something is a WIP name - will stay until someone finds a better one
        print(something1, something2)


        #set h to false when needed
        idx_to_set_h = []

        for idx, node in enumerate(graph.nodes):
            if node[0] == something1 or node[0] == something2:
                idx_to_set_h.append(idx)

        for idx in idx_to_set_h:
            print(graph.nodes[idx])
            vertice = graph.nodes[idx][0]
            attrs = graph.nodes[idx][1]
            attrs['h'] = False
            graph.nodes[idx] = (vertice, attrs)

        print(graph.nodes)

        #add new vertices between "non-special" vertices
        subgraph_edges = set(nx.subgraph(graph.nx_graph, hypernode_neigh_vertices).edges)
        set_subgraph_edges = (set(edge) for edge in subgraph_edges)

        print(graph.edges)

        #remove hyperedges, "regular" edges
        vertices_to_add = []
        edges_to_add = []

        #create nodes between those removed
        for v1, v2 in subgraph_edges:
            print(v1, v2)
            new_vertice_pos = graph.calculate_mean_node_position([v1, v2])
            new_vertice_name = 'v' + str(new_vertice_pos)
            old_edge, old_edge_attr = self.__get_edge(graph, v1, v2)
            vertices_to_add.append((new_vertice_name, {"h": False, "pos": new_vertice_pos}))
            edges_to_add.append(({v1, new_vertice_name}, {'label': 'E', 'B': old_edge_attr["B"]}))
            edges_to_add.append(({new_vertice_name, v2}, {'label': 'E', 'B': old_edge_attr["B"]}))

        center_vertice_pos = graph.calculate_mean_node_position(list(graph.get_neighbours(hyper_node)))
        center_vertice_name = 'v' + str(center_vertice_pos)
        vertices_to_add.append((center_vertice_name, {"pos": center_vertice_pos, "h": 0}))

        print(vertices_to_add)
        print(edges_to_add)

        graph.shrink(nodes=[], edges=[set(hypernode_neigh_vertices), *set_subgraph_edges])
        graph.extend(nodes=[*vertices_to_add], edges=[])
        graph.extend(nodes=[], edges=[*edges_to_add])

        #replace

        # now - all neighbors of "preexisting" nodes have to be connected to the center v
        # and we need to create hypergraphs for each

        later_edges_to_add = []

        for v in hypernode_neigh_vertices:
            neigh_vertices = graph.get_neighbours(v)
            # there will be 2 - each should be connected to new center here
            nv_list = list(neigh_vertices)
            for nv in nv_list:
                later_edges_to_add.append(({nv, center_vertice_name}, {'label': 'E', 'B': True}))
                print(nv)
            later_edges_to_add.append(({v, nv_list[0], center_vertice_name, nv_list[1]}, {'label': 'Q', 'R': False}))

        graph.extend(nodes=[], edges=[*later_edges_to_add])

        return graph


    def __get_incomplete_vertices(self, graph, hyper_node):
        hypernode_neigh_vertices = tuple(graph.get_neighbours(hyper_node))
        subgraph_edges = tuple(nx.subgraph(graph.nx_graph, hypernode_neigh_vertices).edges)

        # correct result for dict - no vertices missing, two have only two occurrences
        # (connected to a breaking node instead of a hn-connected)
        # we can assume that because we have a neighboring hanging node situation

        occurrences = {}
        for edge in subgraph_edges:
            if occurrences.get(edge[0]):
                occurrences[edge[0]] += 1
            else:
                occurrences[edge[0]] = 1
            if occurrences.get(edge[1]):
                occurrences[edge[1]] += 1
            else:
                occurrences[edge[1]] = 1

        incomplete_vertices = []
        missing_vertice = None

        # check which nodes are not connected between them (fully or partially)
        for vertice in hypernode_neigh_vertices:
            if occurrences.get(vertice) == 1:
                incomplete_vertices.append(vertice)
            if occurrences.get(vertice) == None:
                missing_vertice = vertice

        return incomplete_vertices, missing_vertice

    def get_unconnected_vertices(self, graph, hypernode_neigh_vertices, incomplete_vertices):
        ignored_vertices = [*incomplete_vertices]
        checked_vertices = [*list(graph.get_neighbours(incomplete_vertices[0])),
                            *list(graph.get_neighbours(incomplete_vertices[1])),
                            *list(graph.get_neighbours(incomplete_vertices[2])),
                            *list(graph.get_neighbours(incomplete_vertices[3]))]

        # those not connected to graph (and not the missing one)
        unconnected_vertices = []

        for v in checked_vertices:
            if (v not in ignored_vertices
                    and v not in hypernode_neigh_vertices
                    # we want only real vertices, not hyper-vertices if it's connected to any
                    and v[0] == 'v'
                    and v not in unconnected_vertices):
                unconnected_vertices.append(v)

        return unconnected_vertices


    def __get_missing_vertices(self, graph, incomplete_vertices, unconnected_vertices):
        # now we need to check if we have two matching 'something1', 'something2' in those unconnected
        # we will do that by checking if the node there is in correct position, and is linked to correct vertices

        somethings = []
        print(incomplete_vertices)
        print(unconnected_vertices)

        #if it's stupid but it works...
        for i in range(0,4):
            for j in range(1,4):
                checked_pos = graph.calculate_mean_node_position([incomplete_vertices[i], incomplete_vertices[j]])
                for v in unconnected_vertices:
                    if graph.calculate_mean_node_position([v]) == checked_pos:
                        if (v in graph.get_neighbours(incomplete_vertices[i])
                                and v in graph.get_neighbours(incomplete_vertices[j])
                                and v not in somethings):
                            somethings.append(v)

        print(somethings)


        # edges_to_ignore = [{incomplete_vertices[0], something1}, {something1, missing_vertice}, {missing_vertice, something2}, {something2, incomplete_vertices[1]}]

        return somethings

    def __get_edge(self, graph, v1, v2):
        for edge in graph.edges:
            if len(edge[0]) == 2 and v1 in edge[0] and v2 in edge[0]:
                return edge[0], edge[1]