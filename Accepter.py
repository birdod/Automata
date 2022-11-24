from typing import Dict, Set
import networkx as nx
import matplotlib.pyplot as plt

#@TODO graph mutiedge collapse, self edge label missing
class AccepterUtill():
    def lambda_cnt(trans):
        cnt = 0
        for key in trans.keys():
            for target in trans[key].keys():
                if target == "lambda":
                    cnt += 1
        return cnt
    
    def draw_graph(accepter):
        graph = nx.MultiDiGraph()
        for state in accepter.trans.keys():
            graph.add_node(state)
        edge_labels = {}
        for keyf in accepter.trans.keys():
            for edge in accepter.trans[keyf].keys():
                for keyt in accepter.trans[keyf][edge]:
                    graph.add_edge(keyf,keyt, label = edge)
                    if (keyf, keyt) in edge_labels.keys():
                        edge_labels[(keyf, keyt)] += f',{edge}'
                    else:
                        edge_labels[(keyf, keyt)] = edge
        color_map = []
        for node in graph:
            if node in accepter.final:
                color_map.append('red')
            else: 
                color_map.append('blue')     
        ax = plt.plot()
        pos = nx.shell_layout(graph)
        nx.draw_shell(graph, node_color = color_map,with_labels = True)
        nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=edge_labels)
        plt.show()
        return


class Accepter():
    def __init__(
        self,
        start: Set[str],
        final: Set[str],
        charset: Set[str],
        trans: Dict[str, Dict[str, Set[str]]],
    ):
        self.start = start
        self.final = final
        self.charset = charset
        self.trans = trans

        self.current = start
        self.lambdacnt = AccepterUtill.lambda_cnt(trans)
    
    def forward(self, x):
        next = set([])
        if x=="lambda":
            next = self.current

        for state in self.current:
            if state not in self.trans.keys():
                continue
            if x in self.trans[state].keys():
                next = next.union(self.trans[state][x])
        self.current = next
        return
    
    def is_accepted(self):
        for state in self.current:
            if state in self.final:
                return True
        return False

    def delta(self, start, string):
        self.current = start
        for char in string:
            for _ in range(self.lambdacnt):
                self.forward("lambda")
            self.forward(char)
        for _ in range(self.lambdacnt):
            self.forward("lambda")
        return self.current

    def __call__(self, string):
        self.current = self.start
        for char in string:
            for _ in range(self.lambdacnt):
                self.forward("lambda")
            self.forward(char)
        
        for _ in range(self.lambdacnt):
            self.forward("lambda")
        
        return self.is_accepted()

    

