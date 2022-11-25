from Accepter import Accepter
from queue import Queue
from Utills import states_is_final, states_to_string


'''
    Regular Languages (nfa <=> dfa) <=>
    Regular Expression              
'''
def nfa_to_dfa(nfa):

    dfa = Accepter(
            states = set(),
            start = nfa.start,
            final = set(),
            charset = nfa.charset,
            trans = {}
        )
    Q = Queue()

    if states_is_final(dfa.start, nfa.final):
        dfa.final.add(states_to_string(dfa.start))
    Q.put(dfa.start)

    while(not Q.empty()):
        nowstates = Q.get()
        nownode = states_to_string(nowstates)
        for char in nfa.charset:
            nextstates = nfa.delta(nowstates, char)
            nextnode = states_to_string(nextstates)
            if nextnode not in dfa.trans.keys():
                Q.put(nextstates)
                if states_is_final(nextstates, nfa.final):
                    dfa.final.add(nextnode)
            dfa.transadd(nownode, nextnode,char)
    return dfa


class regex_to_nfa():
    state = 0
    def __init__(self):
        self.inter = 0
        self.reglist = None
    
    def Minit(self, x: str):
        local_start = f"q{regex_to_nfa.state*2}"
        local_final = f"q{regex_to_nfa.state*2 + 1}"
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
            set([local_start,local_final]),
            set([local_start]),
            set([local_final]),
            charset,
            trans
        )
        regex_to_nfa.state += 1
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
                    cur = cur+2
                if (cur<end) and self.reglist[cur]=='^':
                    Mlist.append(Mlist.pop(-1).aster())
                    cur += 1
                second = Mlist.pop(-1)
                Mlist.append(Mlist.pop(-1) * second)
            elif self.reglist[cur] == '^':
                Mlist.append(Mlist.pop(-1).aster())
                cur += 1
            else:
                Mlist.append(self.Minit(self.reglist[cur]))
                cur += 1
        if Mlist:
            ret = Mlist.pop(0)
            for M in Mlist:
                ret = ret + M
            return ret

                
    def __call__(self, regex):
        self.init = 0
        self.inter = 0
        self.reglist = self.preproc(regex)
        return self.eval(0, len(self.reglist))
    
        
