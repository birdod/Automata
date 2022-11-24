from typing import Dict, Set
from Utills import AccepterUtill


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

        self.current = None
        self.lambdacnt = AccepterUtill.lambda_cnt(trans)
    def transadd(
        self, 
        node1: str or Set, 
        node2: str or Set,
        edge: str
    ):
        if edge == "lambda":
            self.lambdacnt += 1
        if isinstance(node1, set):
            node1 = next(iter(node1))
        if isinstance(node2, set):
            if node1 not in self.trans.keys():
                self.trans[node1] = {edge: node2}
            elif edge not in self.trans[node1].keys():
                self.trans[node1][edge] = node2
            else:
                self.trans[node1][edge] = self.trans[node1][edge].union(node2)
        else:
            if node1 not in self.trans.keys():
                self.trans[node1] = {edge: set([node2])}
            elif edge not in self.trans[node1].keys():
                self.trans[node1][edge] = set([node2])
            else:
                self.trans[node1][edge].add(node2)


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

    

