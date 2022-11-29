from Theorem import *
from Utills import *

    
if __name__ == "__main__":

    diff = regex_to_nfa()("a*b")
    diff2 = regex_to_nfa()("c*c")

    print(diff.intersection(diff2.complement()).is_empty())