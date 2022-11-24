from Accepter import Accepter
from queue import Queue
from Utills import states_is_final, states_to_string


'''
    Regular Languages (nfa <=> dfa) <=>
    Regular Expression              <=>
    Regular Grammar                 
'''
def nfa_to_dfa(nfa):

    dfa = Accepter(
            start = nfa.start,
            final = set(),
            trans = {},
            charset = nfa.charset
        )
    Q = Queue()

    dfa.trans[states_to_string(dfa.start)] = {}
    if states_is_final(dfa.start, nfa.final):
        dfa.final.add(states_to_string(dfa.start))
    Q.put(dfa.start)

    while(not Q.empty()):
        nowstates = Q.get()
        nownode = states_to_string(nowstates)
        for char in nfa.charset:
            nextstates = nfa.delta(nowstates, char)
            nextnode = states_to_string(nextstates)
            if nextnode in dfa.trans.keys():
                dfa.trans[nownode][char] = set([nextnode])
            else:
                dfa.trans[nextnode] = {}
                Q.put(nextstates)
                if states_is_final(nextstates, nfa.final):
                    dfa.final.add(nextnode)
                dfa.trans[nownode][char] = set([nextnode])
    return dfa


class regex_to_nfa():
    def __init__(self):
        self.init = 0
        self.inter = 0
        self.reglist = None
    
    def Minit(self, x: str):
        local_start = f"q{self.init*2}"
        local_final = f"q{self.init*2 + 1}"
        if x == "none":
            trans = {}
            charset = set()
        elif x== "lambda":
            trans = {local_start:{"lambda":set([local_final])}}
            charset = set()

        else:
            trans = {local_start:{x:set([local_final])}}
            charset = set([x])

        ret = Accepter(
            set([local_start]),
            set([local_final]),
            charset,
            trans
        )
        self.init += 1
        return ret

    def add(self, M1, M2):
        inter_start = f"inter{self.inter*2}"
        inter_final = f"inter{self.inter*2 +1}"
        ret = Accepter(
            set([inter_start]),
            set([inter_final]),
            M1.charset.union(M2.charset),
            dict(M1.trans, **M2.trans)
        )
        ret.transadd(inter_start, M1.start.union(M2.start), "lambda")
        ret.transadd(M1.final, inter_final, "lambda")
        ret.transadd(M2.final, inter_final, "lambda")
        self.inter += 1
        return ret

    def mult(self, M1, M2):
        inter_start = f"inter{self.inter*2}"
        inter_final = f"inter{self.inter*2 +1}"
        ret = Accepter(
            set([inter_start]),
            set([inter_final]),
            M1.charset.union(M2.charset),
            dict(M1.trans, **M2.trans)
        )
        ret.transadd(inter_start, M1.start, "lambda")
        ret.transadd(M1.final, M2.start, "lambda")
        ret.transadd(M2.final, inter_final, "lambda")

        self.inter += 1
        return ret

    def aster(self, M):
        inter_start = f"inter{self.inter*2}"
        inter_final = f"inter{self.inter*2 +1}"
        ret = Accepter(
            set([inter_start]),
            set([inter_final]),
            M.charset,
            M.trans
        )

        ret.transadd(inter_start, inter_final, "lambda")
        ret.transadd(inter_final, inter_start, "lambda")
        ret.transadd(inter_start, M.start, "lambda")
        ret.transadd(M.final, inter_final, "lambda")
        self.inter += 1
        return ret

    def preproc(self,regex):
        ret = []
        now = 0
        while (now < len(regex)):
            if regex[now] in ['(', ')', '+','*','^']:
                ret.append(regex[now])
                now += 1
            elif regex[now] == ' ':
                now += 1
            else:
                start = now
                while((now < len(regex)) and (regex[now] not in ['(', ')', '+','*','^', ' '])):
                    now += 1
                ret.append(regex[start:now])
        return ret

    def braket(self, cur):
        bcnt = 0
        while (bcnt >= 0):
            cur += 1
            if self.reglist[cur] == '(':
                bcnt += 1
            if self.reglist[cur] == ')':
                bcnt -= 1
        return cur

    def eval(self, cur, end):
        Mlist = []
        while(cur < end):
            if self.reglist[cur] == '(':
                Mlist.append(self.eval(cur + 1, self.braket(cur)))
                cur = self.braket(cur) + 1
            
            elif self.reglist[cur] == '+':
                cur += 1
                continue
        
            elif self.reglist[cur] == '*':
                if self.reglist[cur+1] == '(':
                    Mlist.append(self.eval(cur+2, self.braket(cur+1)))
                    cur = self.braket(cur+1) + 1
                else:
                    Mlist.append(self.eval(cur+1, cur+2))
                    cur = cur+3
                if (cur<end) and self.reglist[cur]=='^':
                    Mlist.append(self.aster(Mlist.pop(-1)))
                    cur += 1
                second = Mlist.pop(-1)
                Mlist.append(self.mult(Mlist.pop(-1),second))
            elif self.reglist[cur] == '^':
                Mlist.append(self.aster(Mlist.pop(-1)))
                cur += 1
            else:
                Mlist.append(self.Minit(self.reglist[cur]))
                cur += 1
        if Mlist:
            ret = Mlist.pop(0)
            for M in Mlist:
                ret = self.add(ret, M)
            return ret

                
    def __call__(self, regex):
        self.init = 0
        self.inter = 0
        self.reglist = self.preproc(regex)
        return self.eval(0, len(self.reglist))
    
        
