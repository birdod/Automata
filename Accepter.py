from typing import Dict, Set
from Utills import AccepterUtill
import Theorem

class Accepter():
    inter = 0
    def __init__(
        self,
        states: Set[str],
        start: Set[str],
        final: Set[str],
        charset: Set[str],
        trans: Dict[str, Dict[str, Set[str]]],
    ):
        self.states = states
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
        self.states.add(node1)
        if isinstance(node2, set):
            self.states = self.states.union(node2)
            if node1 not in self.trans.keys():
                self.trans[node1] = {edge: node2}
            elif edge not in self.trans[node1].keys():
                self.trans[node1][edge] = node2
            else:
                self.trans[node1][edge] = self.trans[node1][edge].union(node2)
        else:
            self.states.add(node2)
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

    def __add__(self, M2):
        M1 = self
        inter_start = f"inter{Accepter.inter*2}"
        inter_final = f"inter{Accepter.inter*2 +1}"
        ret = Accepter(
            self.states.union(M2.states),
            set([inter_start]),
            set([inter_final]),
            M1.charset.union(M2.charset),
            dict(M1.trans, **M2.trans)
        )
        ret.transadd(inter_start, M1.start.union(M2.start), "lambda")
        if len(M1.final)>1:
            for state in M1.final:
                ret.transadd(state, inter_final, "lambda")
        else:
            ret.transadd(M1.final, inter_final, "lambda")
        if len(M2.final)>1:
            for state in M2.final:
                ret.transadd(state, inter_final, "lambda")
        else:
            ret.transadd(M2.final, inter_final, "lambda")

        Accepter.inter += 1
        return ret

    def __mul__(self, M2):
        M1 = self
        inter_start = f"inter{Accepter.inter*2}"
        inter_final = f"inter{Accepter.inter*2 +1}"
        ret = Accepter(
            self.states.union(M2.states),
            set([inter_start]),
            set([inter_final]),
            M1.charset.union(M2.charset),
            dict(M1.trans, **M2.trans)
        )
        ret.transadd(inter_start, M1.start, "lambda")
        if len(M1.final)>1:
            for state in M1.final:
                ret.transadd(state, M2.start, "lambda")
        else:
            ret.transadd(M1.final, M2.start, "lambda")
        if len(M2.final)>1:
            for state in M2.final:
                ret.transadd(state, inter_final, "lambda")
        else:
            ret.transadd(M2.final, inter_final, "lambda")

        Accepter.inter += 1
        return ret

    def aster(self):
        M = self
        inter_start = f"inter{Accepter.inter*2}"
        inter_final = f"inter{Accepter.inter*2 +1}"
        ret = Accepter(
            self.states,
            set([inter_start]),
            set([inter_final]),
            M.charset,
            M.trans
        )

        ret.transadd(inter_start, inter_final, "lambda")
        ret.transadd(inter_final, inter_start, "lambda")
        ret.transadd(inter_start, M.start, "lambda")
        if len(M.final)>1:
            for state in M.final:
                ret.transadd(state, inter_final, "lambda")
        else:
            ret.transadd(M.final, inter_final, "lambda")

        Accepter.inter += 1
        return ret
    
    def complement(self):
        ret = Accepter(
            self.states,
            self.start,
            self.final,
            self.charset,
            self.trans
        )
        if ret.is_nfa():
            ret = Theorem.nfa_to_dfa(ret)
        ret.final = ret.states.difference(ret.final)
        return ret

    def is_nfa(self):
        flag = False
        for start in self.trans.keys():
            for edge in self.trans[start].keys():
                if len(self.trans[start][edge]) > 1:
                    flag = True
        
        return (flag or self.lambdacnt>0)

