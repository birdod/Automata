from Accepter import Accepter
from queue import Queue

def states_to_string(states):
    if len(states)==0:
        return "none"
    ret = ""
    for state in sorted(states):
        ret += state
    return ret
def states_is_final(states,final):
    for state in states:
        if state in final:
            return True
    return False


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