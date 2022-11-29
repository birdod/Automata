from typing import Dict, Set, Tuple, List


class GreibachAccepter():
    def __init__(
        self,
        trans: Dict[Tuple[str, str], List[List[str]]],
        stack0 = 'S'
    ):
        self.trans = trans
        self.stack0 = stack0

        self.stack = [stack0]
        self.accept = False

    def stack_control(self, next, append):
        if "lambda" in next:
            return
        if append:
            for next in next:
                self.stack.append(next)
        else:
            self.stack = self.stack[0:-len(next)]

    def forward(self, string):
        if len(self.stack)==0 or len(string)==0:
            if len(self.stack)==0 and len(string)==0:
                self.accept = True
            return 
        char = string[0]
        top = self.stack.pop(-1)

        if (char, top) not in self.trans.keys():
            self.stack.append(top)
            return
        for ntop in self.trans[(char,top)]:
            self.stack_control(ntop, True)
            self.forward(string[1:])
            self.stack_control(ntop, False)
        
        self.stack.append(top)

    def __call__(self, string):
        self.stack = [self.stack0]
        self.accept = False

        self.forward(string)

        return self.accept


        
