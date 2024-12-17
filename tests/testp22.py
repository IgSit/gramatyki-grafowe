from graph.hypergraph import HyperGraph
from productions.p22 import P22

class TestP22():
    def __init__(self):
        pass
    
    def run(self):
        # self.test1()
        # self.test2()
        # self.test3()
        # self.test4()
        # self.test5()
        # self.test6()
        # self.test7()
        self.test8()

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
                ('v7', {'pos': (8, 4), 'h': False}),
                ('v8', {'pos': (-2, 2), 'h': False}),
                ('v9', {'pos': (2,-2), 'h': False}),
            ],
            edges=[
                ({'v1', 'v9'}, {'label': 'E', 'B': True}),
                ({'v2', 'v9'}, {'label': 'E', 'B': True}),
                ({'v2', 'v5'}, {'label': 'E', 'B': True}),
                ({'v5', 'v3'}, {'label': 'E', 'B': False}),
                ({'v3', 'v4'}, {'label': 'E', 'B': True}),
                ({'v4', 'v8'}, {'label': 'E', 'B': True}),
                ({'v1', 'v8'}, {'label': 'E', 'B': True}),
                ({'v3', 'v7'}, {'label': 'E', 'B': True}),
                ({'v7', 'v6'}, {'label': 'E', 'B': True}),
                ({'v6', 'v5'}, {'label': 'E', 'B': False}),
                ({'v3', 'v5', 'v6', 'v7'}, {'label': 'Q1', 'R': True}),
                ({'v1', 'v2', 'v3', 'v4', 'v8', 'v9'}, {'label': 'Q2', 'R': False})
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

    def test6(self):
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
                ('v11', {'pos': (4, -4), 'h': False}),
                ('v12', {'pos': (8, -4), 'h': False}),
                ('v13', {'pos': (8, 0), 'h': False}),
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
                ({'v1', 'v11'}, {'label': 'E', 'B': True}),
                ({'v11', 'v2'}, {'label': 'E', 'B': False}),
                ({'v11', 'v12'}, {'label': 'E', 'B': True}),
                ({'v12', 'v13'}, {'label': 'E', 'B': True}),
                ({'v2', 'v13'}, {'label': 'E', 'B': False}),
                ({'v6', 'v13'}, {'label': 'E', 'B': True}),
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


    def test7(self):
        hyper_graph = HyperGraph(
            nodes=[
                ('v1', {'pos': (0, 0), 'h': False}),
                ('v2', {'pos': (4, 0), 'h': False}),
                ('v3', {'pos': (-2, 2), 'h': False}),
                ('v4', {'pos': (0, 4), 'h': False}),
                ('v5', {'pos': (6, 2), 'h': False}),
                ('v6', {'pos': (4, 4), 'h': False}),
                ('v7', {'pos': (5, 3), 'h': True}),
                ('v8', {'pos': (7, 3.5), 'h': False}),
                ('v9', {'pos': (8, 2.5), 'h': False}),
                ('v10', {'pos': (6, 4.5), 'h': False}),
                ('v11', {'pos': (6, -2), 'h': False}),
                ('v12', {'pos': (9, -1), 'h': False}),
                ('v13', {'pos': (11, 1), 'h': False}),
                ('v14', {'pos': (10, 3), 'h': False}),
            ],
            edges=[
                ({'v1', 'v2'}, {'label': 'E', 'B': True}),
                ({'v2', 'v5'}, {'label': 'E', 'B': True}),
                ({'v5', 'v7'}, {'label': 'E', 'B': False}),
                ({'v7', 'v6'}, {'label': 'E', 'B': True}),
                ({'v6', 'v4'}, {'label': 'E', 'B': True}),
                ({'v4', 'v3'}, {'label': 'E', 'B': True}),
                ({'v3', 'v1'}, {'label': 'E', 'B': True}),
                ({'v5', 'v9'}, {'label': 'E', 'B': True}),
                ({'v9', 'v8'}, {'label': 'E', 'B': True}),
                ({'v8', 'v7'}, {'label': 'E', 'B': False}),
                ({'v10', 'v6'}, {'label': 'E', 'B': True}),
                ({'v10', 'v8'}, {'label': 'E', 'B': True}),
                ({'v9', 'v14'}, {'label': 'E', 'B': True}),
                ({'v14', 'v13'}, {'label': 'E', 'B': True}),
                ({'v13', 'v12'}, {'label': 'E', 'B': True}),
                ({'v12', 'v11'}, {'label': 'E', 'B': True}),
                ({'v11', 'v2'}, {'label': 'E', 'B': True}),
                ({'v1', 'v2', 'v5', 'v6', 'v4', 'v3'}, {'label': 'Q1', 'R': False}),
                ({'v5', 'v7', 'v8', 'v9'}, {'label': 'Q2', 'R': True}),
                ({'v2', 'v5', 'v14', 'v13', 'v12', 'v11'}, {'label': 'Q3', 'R': False})
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

    def test8(self):
        hyper_graph = HyperGraph(
            nodes=[
                ('v1', {'pos': (0, 0), 'h': False}),
                ('v2', {'pos': (4, 0), 'h': False}),
                ('v3', {'pos': (-2, 2), 'h': False}),
                ('v4', {'pos': (0, 4), 'h': False}),
                ('v5', {'pos': (6, 2), 'h': False}),
                ('v6', {'pos': (4, 4), 'h': False}),
                ('v7', {'pos': (5, 3), 'h': True}),
                ('v8', {'pos': (7, 3.5), 'h': False}),
                ('v9', {'pos': (8, 2.5), 'h': True}),
                ('v10', {'pos': (6, 4.5), 'h': False}),
                ('v12', {'pos': (9, -1), 'h': False}),
                ('v14', {'pos': (10, 3), 'h': False}),
                ('v15', {'pos': (8, 5), 'h': False}),
                ('v16', {'pos': (9, 4), 'h': False}),
            ],
            edges=[
                ({'v1', 'v2'}, {'label': 'E', 'B': True}),
                ({'v2', 'v5'}, {'label': 'E', 'B': False}),
                ({'v5', 'v7'}, {'label': 'E', 'B': False}),
                ({'v7', 'v6'}, {'label': 'E', 'B': False}),
                ({'v6', 'v4'}, {'label': 'E', 'B': True}),
                ({'v4', 'v3'}, {'label': 'E', 'B': True}),
                ({'v3', 'v1'}, {'label': 'E', 'B': True}),
                ({'v5', 'v9'}, {'label': 'E', 'B': False}),
                ({'v9', 'v8'}, {'label': 'E', 'B': False}),
                ({'v8', 'v7'}, {'label': 'E', 'B': False}),
                ({'v10', 'v6'}, {'label': 'E', 'B': True}),
                ({'v10', 'v8'}, {'label': 'E', 'B': False}),
                ({'v9', 'v14'}, {'label': 'E', 'B': False}),
                ({'v14', 'v12'}, {'label': 'E', 'B': True}),
                ({'v15', 'v16'}, {'label': 'E', 'B': True}),
                ({'v12', 'v2'}, {'label': 'E', 'B': True}),
                ({'v16', 'v14'}, {'label': 'E', 'B': True}),
                ({'v10', 'v15'}, {'label': 'E', 'B': True}),
                ({'v8', 'v16'}, {'label': 'E', 'B': False}),
                ({'v1', 'v2', 'v5', 'v6', 'v4', 'v3'}, {'label': 'Q1', 'R': False}),
                ({'v5', 'v7', 'v8', 'v9'}, {'label': 'Q2', 'R': True}),
                ({'v2', 'v5', 'v14','v12'}, {'label': 'Q3', 'R': False}),
                ({'v6', 'v7', 'v10','v8'}, {'label': 'Q4', 'R': False}),
                ({'v8', 'v10', 'v15','v16'}, {'label': 'Q5', 'R': False}),
                ({'v8', 'v16', 'v14','v9'}, {'label': 'Q6', 'R': False}),
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