from typing import List, Dict, Set
import networkx as nx
import matplotlib.pyplot as plt


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
        
        for keyf in accepter.trans.keys():
            for edge in accepter.trans[keyf].keys():
                for keyt in accepter.trans[keyf][edge]:
                    graph.add_edge(keyf,keyt, edge)
        color_map = []
        for node in graph:
            if node in accepter.final:
                color_map.append('red')
            else: 
                color_map.append('blue')     
        ax = plt.plot()
        nx.draw(graph, node_color = color_map,with_labels = True)
        plt.show()
        return

class Accepter():
    def __init__(
        self,
        start: str,
        final: Set[str],
        trans: Dict[str, Dict[str, Set[str]]]
    ):
        self.start = set([start])
        self.current = set([start])
        self.final = final
        self.trans = trans
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
    
    def __call__(self, string):
        self.current = self.start
        for char in string:
            for _ in range(self.lambdacnt):
                self.forward("lambda")
            self.forward(char)
        
        for _ in range(self.lambdacnt):
            self.forward("lambda")
        
        return self.is_accepted()

    

    
if __name__ == "__main__":
    accepter = Accepter("q0", 
        set(["q2","q3"]), 
        {   "q0":{"lambda":set(["q2"]), "b":set(["q1"])}, 
            "q2":{"a":set(["q2"])},
            "q1":{"a":set(["q3"]), "b":set(["q1"])},
        })
    # print(accepter("aaaaaa"))
    # print(accepter(""))
    # print(accepter("bbba"))
    
    # print(accepter("bbb"))
    # print(accepter("bab"))

    AccepterUtill.draw_graph(accepter)