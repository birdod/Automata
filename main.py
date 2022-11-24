from Accepter import *
from Theorem import *

    
if __name__ == "__main__":
    transfer = regex_to_nfa()
    accepter = transfer("a*b^")
    for temp in accepter.trans:
        print(temp, accepter.trans[temp])
