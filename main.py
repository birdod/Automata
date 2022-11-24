from Accepter import *
from Theorem import *

    
if __name__ == "__main__":
    accepter = Accepter(
        set(["q0"]), 
        set(["q1"]),
        set(["0","1"]),
        {   "q0":{"0":set(["q0","q1"]), "1":set(["q1"])}, 
            "q2":{"1":set(["q2"])},
            "q1":{"0":set(["q2"]), "1":set(["q2"])},
        }
    )


    AccepterUtill.draw_graph(nfa_to_dfa(accepter))