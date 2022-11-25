from Accepter import *
from Theorem import *

    
if __name__ == "__main__":
    transfer = regex_to_nfa()
    acc1 = transfer("a")
    acc2 = transfer("b")
    print((acc1 + acc2)("a"))
    
