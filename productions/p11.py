import networkx as nx

from graph.hypergraph import HyperGraph
from productions.production import Production


class P11(Production):
    def __init__(self):
        super().__init__()

    def check(self, graph: HyperGraph, hyper_node: str) -> bool:
        #is hypernode marked for breaking
        cond1 = graph.is_breakable(hyper_node)

        #is hypernode linked to 6 vertices
        hypernode_neigh_vertices = tuple(graph.get_neighbours(hyper_node))
        cond2 = len(hypernode_neigh_vertices) == 6

        incomplete_vertices, missing_vertice = self.__get_incomplete_vertices(graph, hyper_node)

        #before we move on - check counts - we should have one missing, two incomplete due to hanging node being "neighbours"
        ignored_vertices = [*incomplete_vertices, missing_vertice]
        if len(incomplete_vertices) != 2 or missing_vertice is None:
            return False

        for v in hypernode_neigh_vertices:
            if v not in ignored_vertices:
                if graph.nx_graph.nodes.get(v).get('h'):
                    return False

        # edges we don't have are - incomplete[0] - 'something1' - missing, missing - 'something2' - incomplete[1], order should not matter
        # print(tuple(graph.get_neighbours(incomplete_vertices[0])))
        # print(tuple(graph.get_neighbours(incomplete_vertices[1])))
        # print(tuple(graph.get_neighbours(missing_vertice)))

        #check whether two vertices marked as 'something1', 'something2' above exist
        ignored_vertices = [*incomplete_vertices, missing_vertice]
        checked_vertices = [*list(graph.get_neighbours(incomplete_vertices[0])),
                            *list(graph.get_neighbours(incomplete_vertices[1])),
                            *list(graph.get_neighbours(missing_vertice))]

        #those not connected to graph (and not the missing one)
        unconnected_vertices = []

        for v in checked_vertices:
            if (v not in ignored_vertices
                    and v not in hypernode_neigh_vertices
                    # we want only real vertices, not hyper-vertices if it's connected to any
                    and v[0]=='v'
                    and v not in unconnected_vertices):
                unconnected_vertices.append(v)


        # #now we need to check if we have two matching 'something1', 'something2' in those unconnected
        # #we will do that by checking if the node there is in correct position, and is linked to correct vertices
        something1, something2, _ = self.__get_missing_vertices(graph, incomplete_vertices, missing_vertice, unconnected_vertices)

        cond3 = something1 is not None and something2 is not None

        # print(cond1, cond2, cond3)

        # should probably just fail earlier?
        return cond1 and cond2 and cond3

    def apply(self, graph: HyperGraph, hyper_node: str) -> HyperGraph:
        hypernode_neigh_vertices = tuple(graph.get_neighbours(hyper_node))
        incomplete_vertices, missing_vertice = self.__get_incomplete_vertices(graph, hyper_node)
        unconnected_vertices = self.get_unconnected_vertices(graph, hypernode_neigh_vertices, incomplete_vertices, missing_vertice)
        something1, something2, edges_to_ignore = self.__get_missing_vertices(graph, incomplete_vertices, missing_vertice, unconnected_vertices)

        #something is a WIP name - will stay until someone finds a better one
        print(something1, something2, edges_to_ignore)

        #add new vertices between "non-special" vertices
        subgraph_edges = set(nx.subgraph(graph.nx_graph, hypernode_neigh_vertices).edges)
        set_subgraph_edges = (set(edge) for edge in subgraph_edges)
        print(subgraph_edges)
        print(set_subgraph_edges)
        #remove hyperedges, "regular" edges
        graph.shrink(nodes=[], edges=[set(hypernode_neigh_vertices), *set_subgraph_edges])

        vertices_to_add = []
        edges_to_add = []

        #create nodes between those removed
        for v1, v2 in subgraph_edges:
            print(v1, v2)
            new_vertice_pos = graph.calculate_mean_node_position([v1, v2])
            new_vertice_name = 'v' + str(new_vertice_pos)
            vertices_to_add.append((new_vertice_name, {"h": False, "pos": new_vertice_pos}))

            edges_to_add.append(({v1, new_vertice_name}, {'label': 'E', 'B': False}))
            edges_to_add.append(({new_vertice_name, v2}, {'label': 'E', 'B': False}))

        print(vertices_to_add)
        print(edges_to_add)

        graph.extend(nodes=[*vertices_to_add], edges=[])
        graph.extend(nodes=[], edges=[*edges_to_add])

        return graph


    def __get_incomplete_vertices(self, graph, hyper_node):
        hypernode_neigh_vertices = tuple(graph.get_neighbours(hyper_node))
        subgraph_edges = tuple(nx.subgraph(graph.nx_graph, hypernode_neigh_vertices).edges)


        # correct result for dict - one vertice missing, two have only one occurrence
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

    def get_unconnected_vertices(self, graph, hypernode_neigh_vertices, incomplete_vertices, missing_vertice):
        # check whether two vertices marked as 'something1', 'something2' above exist
        ignored_vertices = [*incomplete_vertices, missing_vertice]
        checked_vertices = [*list(graph.get_neighbours(incomplete_vertices[0])),
                            *list(graph.get_neighbours(incomplete_vertices[1])),
                            *list(graph.get_neighbours(missing_vertice))]

        # those not connected to graph (and not the missing one)
        unconnected_vertices = []

        for v in checked_vertices:
            if (v not in ignored_vertices
                    and v not in hypernode_neigh_vertices
                    # we want only real vertices, not hyper-vertices if it's connected to any
                    and v[0] != 'X'
                    and v not in unconnected_vertices):
                unconnected_vertices.append(v)

        return unconnected_vertices


    def __get_missing_vertices(self, graph, incomplete_vertices, missing_vertice, unconnected_vertices):
        # now we need to check if we have two matching 'something1', 'something2' in those unconnected
        # we will do that by checking if the node there is in correct position, and is linked to correct vertices
        expected_first_pos = graph.calculate_mean_node_position([incomplete_vertices[0], missing_vertice])
        expected_second_pos = graph.calculate_mean_node_position([incomplete_vertices[1], missing_vertice])

        something1 = None
        something2 = None

        for v in unconnected_vertices:
            v_attributes = graph.nx_graph.nodes.get(v)

            pos = v_attributes.get("pos")
            pos_float = (pos[0] / 1.0, pos[1] / 1.0)
            hanging = v_attributes.get("h")
            # print(v_attributes)
            # print(pos_float, hanging)

            if pos_float == expected_first_pos:
                if hanging:
                    if all(e in list(graph.get_neighbours(v)) for e in [incomplete_vertices[0], missing_vertice]):
                        something1 = v
            if pos_float == expected_second_pos:
                if hanging:
                    if all(e in list(graph.get_neighbours(v)) for e in [incomplete_vertices[1], missing_vertice]):
                        something2 = v

        edges_to_ignore = [{incomplete_vertices[0], something1}, {something1, missing_vertice}, {missing_vertice, something2}, {something2, incomplete_vertices[1]}]

        return something1, something2, edges_to_ignore