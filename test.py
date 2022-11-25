from unittest import TestCase, main
from Theorem import *
from Accepter import *


class AccepterTest(TestCase):
    def test_nfa(self):
        accpeter_3anb = Accepter(
            set(["q0","q1","q2","q3"]),
            set(["q0"]),
            set(["q3"]),
            set(["a","b"]),
            {
                "q0" : {"a": set(["q1"])},
                "q1" : {"a": set(["q2"])},
                "q2" : {"a": set(["q3"])},
                "q3" : {"b": set(["q3"])},
            }
        )
        self.assertEqual(accpeter_3anb("aaabbbb"), True)
        self.assertEqual(accpeter_3anb("aaa"), True)
        self.assertEqual(accpeter_3anb("aa"), False)
        self.assertEqual(accpeter_3anb("aaba"), False)
        
    # this test rely on
    # [test_nfa, test_nfatodfa, test_regextonfa]
    def test_complement(self):
        accepter_an2bcn = regex_to_nfa()("a^*b*b*c^")
        self.assertEqual(accepter_an2bcn("aaaabb"),True)
        self.assertEqual(accepter_an2bcn("aabbccc"),True)
        self.assertEqual(accepter_an2bcn("aaaab"),False)
        self.assertEqual(accepter_an2bcn("aaaccabb"),False)
        an2bcn_comp = accepter_an2bcn.complement()
        self.assertEqual(an2bcn_comp("aaaabb"), False)
        self.assertEqual(an2bcn_comp("aabbccc"), False)
        self.assertEqual(an2bcn_comp("aaaab"), True)
        self.assertEqual(an2bcn_comp("aaaccabb"), True)
        
        return


class TheoremTest(TestCase):
    # this test rely on 
    # [test_nfa]
    def test_nfatodfa(self):
        nfa = Accepter(
            set(["q0","q1","q2","q3"]),
            set(["q0"]),
            set(["q3"]),
            set(["a","b"]),
            {
                "q0" : {"a": set(["q1"])},
                "q1" : {"a": set(["q2"])},
                "q2" : {"a": set(["q3"])},
                "q3" : {"b": set(["q3"])},
            }
        )
        dfa = nfa_to_dfa(nfa)
        self.assertEqual(nfa("aaabbbb"), dfa("aaabbbb"))
        self.assertEqual(nfa("aaa"), dfa("aaa"))
        self.assertEqual(nfa("aa"), dfa("aa"))
        self.assertEqual(nfa("aaba"), dfa("aaba"))
   
    # this test rely on 
    # [test_nfa]
    def test_regextonfa(self):
        accpeter_3anb = regex_to_nfa()("a*a*a*b^")
        self.assertEqual(accpeter_3anb("aaabbbb"), True)
        self.assertEqual(accpeter_3anb("aaa"), True)
        self.assertEqual(accpeter_3anb("aa"), False)
        self.assertEqual(accpeter_3anb("aaba"), False)
        accpeter_case = regex_to_nfa()("(a+c)^*b+d^")
        self.assertEqual(accpeter_case("accacb"), True)
        self.assertEqual(accpeter_case("dddd"), True)
        self.assertEqual(accpeter_case("aa"), False)
        self.assertEqual(accpeter_case("aaba"), False)
if __name__ == "__main__":
    main()