from graph.hypergraph import HyperGraph
from productions.p22 import P22

class TestP22():
    def __init__(self):
        pass
    
    def run(self):
        self.test1()
        #self.test2()
        #self.test3()
        #self.test4()
        #self.test5()

        

    def test1(self):
        hyper_graph = HyperGraph(
            nodes=[
                ('v1', {'pos': (0, 0), 'h': False}),
                ('v2', {'pos': (4, 0), 'h': False}),
                ('v3', {'pos': (4, 4), 'h': False}),
                ('v4', {'pos': (0, 4), 'h': False}),
                ('v5', {'pos': (4, 2), 'h': True}),
                ('v6', {'pos': (8, 2), 'h': False}),
                ('v7', {'pos': (8, 4), 'h': False}),
                ('v8', {'pos': (2, 0), 'h': False}),
                ('v9', {'pos': (0, 2), 'h': False})
            ],
            edges=[
                ({'v3', 'v5'}, {'label': 'E', 'B': False}),
                ({'v5', 'v2'}, {'label': 'E', 'B': False}),
                ({'v3', 'v5', 'v6', 'v7'}, {'label': 'Q1', 'R': True}),
                ({'v1', 'v2', 'v3', 'v4', 'v8', 'v9'}, {'label': 'Q2', 'R': False})
            ]
        )
        hyper_graph.visualize()
        productions = [P22()]

        for production in productions:
            for hyper_node in hyper_graph.hyper_nodes:
                #print(f"Check {hyper_node}")
                if production.check(hyper_graph, hyper_node):
                    hyper_graph = production.apply(hyper_graph, hyper_node)
                    hyper_graph.visualize()
                    break

    def test2(self):
        hyper_graph = HyperGraph(
            nodes=[
                ('v1', {'pos': (0, 0), 'h': False}),
                ('v2', {'pos': (4, 0), 'h': False}),
                ('v3', {'pos': (4, 4), 'h': False}),
                ('v4', {'pos': (0, 4), 'h': False}),
                ('v5', {'pos': (4, 2), 'h': True}),
                ('v6', {'pos': (8, 2), 'h': False}),
                ('v7', {'pos': (8, 4), 'h': False})
            ],
            edges=[
                ({'v1', 'v2'}, {'label': 'E', 'B': True}),
                ({'v2', 'v5'}, {'label': 'E', 'B': False}),
                ({'v5', 'v3'}, {'label': 'E', 'B': False}),
                ({'v3', 'v4'}, {'label': 'E', 'B': True}),
                ({'v4', 'v1'}, {'label': 'E', 'B': True}),
                ({'v3', 'v7'}, {'label': 'E', 'B': True}),
                ({'v7', 'v6'}, {'label': 'E', 'B': True}),
                ({'v6', 'v5'}, {'label': 'E', 'B': False}),
                ({'v3', 'v5', 'v6', 'v7'}, {'label': 'Q1', 'R': True}),
                ({'v1', 'v2', 'v3', 'v4'}, {'label': 'Q2', 'R': False})
            ]
        )

        productions = [P22()]
        hyper_graph.visualize()
        for production in productions:
            for hyper_node in hyper_graph.hyper_nodes:
                #print(f"Check {hyper_node}")
                if production.check(hyper_graph, hyper_node):
                    hyper_graph = production.apply(hyper_graph, hyper_node)
                    hyper_graph.visualize()
                    break
    def test3(self):
        hyper_graph = HyperGraph(
            nodes=[
                ('v1', {'pos': (0, 0), 'h': False}),
                ('v2', {'pos': (4, 0), 'h': False}),
                ('v3', {'pos': (4, 4), 'h': False}),
                ('v4', {'pos': (0, 4), 'h': False}),
                ('v5', {'pos': (4, 2), 'h': True}),
                ('v6', {'pos': (8, 2), 'h': False}),
                ('v7', {'pos': (8, 4), 'h': False}),
                ('v8', {'pos': (-4, 4), 'h': False}), 
                ('v9', {'pos': (-4, 0), 'h': False})
            ],
            edges=[
                ({'v1', 'v2'}, {'label': 'E', 'B': True}),
                ({'v2', 'v5'}, {'label': 'E', 'B': False}),
                ({'v5', 'v3'}, {'label': 'E', 'B': False}),
                ({'v3', 'v4'}, {'label': 'E', 'B': True}),
                ({'v4', 'v1'}, {'label': 'E', 'B': False}),
                ({'v3', 'v7'}, {'label': 'E', 'B': True}),
                ({'v7', 'v6'}, {'label': 'E', 'B': True}),
                ({'v6', 'v5'}, {'label': 'E', 'B': False}),
                ({'v8', 'v4'}, {'label': 'E', 'B': True}), 
                ({'v8', 'v9'}, {'label': 'E', 'B': True}),
                ({'v9', 'v1'}, {'label': 'E', 'B': True}),
                ({'v3', 'v5', 'v6', 'v7'}, {'label': 'Q1', 'R': True}),
                ({'v1', 'v2', 'v3', 'v4'}, {'label': 'Q2', 'R': False}),
                ({'v1', 'v4', 'v8', 'v9'}, {'label': 'Q3', 'R': False})
            ]
        )

        productions = [P22(), P22()]
        hyper_graph.visualize()
        for production in productions:
            for hyper_node in hyper_graph.hyper_nodes:
                #print(f"Check {hyper_node}")
                if production.check(hyper_graph, hyper_node):
                    hyper_graph = production.apply(hyper_graph, hyper_node)
                    hyper_graph.visualize()
                    break

    def test4(self):
        hyper_graph = HyperGraph(
            nodes=[
                ('v1', {'pos': (0, 0), 'h': False}),
                ('v2', {'pos': (4, 0), 'h': False}),
                ('v3', {'pos': (4, 4), 'h': False}),
                ('v4', {'pos': (0, 4), 'h': False}),
                ('v5', {'pos': (4, 2), 'h': True}),
                ('v6', {'pos': (8, 2), 'h': False}),
                ('v7', {'pos': (8, 4), 'h': False}),
                ('v8', {'pos': (-4, 4), 'h': False}), 
                ('v9', {'pos': (-4, 0), 'h': False}),
                ('v10', {'pos': (0, 2), 'h': True}),
            ],
            edges=[
                ({'v1', 'v2'}, {'label': 'E', 'B': True}),
                ({'v2', 'v5'}, {'label': 'E', 'B': False}),
                ({'v5', 'v3'}, {'label': 'E', 'B': False}),
                ({'v3', 'v4'}, {'label': 'E', 'B': True}),
                ({'v3', 'v7'}, {'label': 'E', 'B': True}),
                ({'v7', 'v6'}, {'label': 'E', 'B': True}),
                ({'v6', 'v5'}, {'label': 'E', 'B': False}),
                ({'v8', 'v4'}, {'label': 'E', 'B': True}), 
                ({'v8', 'v9'}, {'label': 'E', 'B': True}),
                ({'v9', 'v1'}, {'label': 'E', 'B': True}),
                ({'v10', 'v4'}, {'label': 'E', 'B': False}),
                ({'v10', 'v1'}, {'label': 'E', 'B': False}),
                ({'v3', 'v5', 'v6', 'v7'}, {'label': 'Q1', 'R': True}),
                ({'v1', 'v2', 'v3', 'v4'}, {'label': 'Q2', 'R': False}),
                ({'v1', 'v4', 'v8', 'v9'}, {'label': 'Q3', 'R': False})
            ]
        )

        productions = [P22(), P22()]
        hyper_graph.visualize()
        for production in productions:
            for hyper_node in hyper_graph.hyper_nodes:
                #print(f"Check {hyper_node}")
                if production.check(hyper_graph, hyper_node):
                    hyper_graph = production.apply(hyper_graph, hyper_node)
                    hyper_graph.visualize()
                    break

                
    def test5(self):
        hyper_graph = HyperGraph(
            nodes=[
                ('v1', {'pos': (0, -4), 'h': False}),
                ('v2', {'pos': (4, 0), 'h': False}),
                ('v3', {'pos': (4, 4), 'h': False}),
                ('v4', {'pos': (0, 4), 'h': False}),
                ('v5', {'pos': (4, 2), 'h': True}),
                ('v6', {'pos': (8, 2), 'h': False}),
                ('v7', {'pos': (8, 4), 'h': False}),
                ('v8', {'pos': (-4, 4), 'h': False}), 
                ('v9', {'pos': (-4, -4), 'h': False}),
                ('v10', {'pos': (0, 0), 'h': True}),
            ],
            edges=[
                ({'v10', 'v2'}, {'label': 'E', 'B': False}),
                ({'v2', 'v5'}, {'label': 'E', 'B': False}),
                ({'v5', 'v3'}, {'label': 'E', 'B': False}),
                ({'v3', 'v4'}, {'label': 'E', 'B': True}),
                ({'v3', 'v7'}, {'label': 'E', 'B': True}),
                ({'v7', 'v6'}, {'label': 'E', 'B': True}),
                ({'v6', 'v5'}, {'label': 'E', 'B': False}),
                ({'v8', 'v4'}, {'label': 'E', 'B': True}), 
                ({'v8', 'v9'}, {'label': 'E', 'B': True}),
                ({'v9', 'v1'}, {'label': 'E', 'B': True}),
                ({'v10', 'v4'}, {'label': 'E', 'B': False}),
                ({'v10', 'v1'}, {'label': 'E', 'B': False}),
                ({'v3', 'v5', 'v6', 'v7'}, {'label': 'Q1', 'R': True}),
                ({'v10', 'v2', 'v3', 'v4'}, {'label': 'Q2', 'R': False}),
                ({'v1', 'v4', 'v8', 'v9'}, {'label': 'Q3', 'R': False})
            ]
        )

        productions = [P22(), P22()]
        hyper_graph.visualize()
        for production in productions:
            for hyper_node in hyper_graph.hyper_nodes:
                #print(f"Check {hyper_node}")
                if production.check(hyper_graph, hyper_node):
                    hyper_graph = production.apply(hyper_graph, hyper_node)
                    hyper_graph.visualize()
                    break