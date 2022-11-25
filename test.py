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
        accepter_anb2cn = regex_to_nfa()("a^*b*b*c^")
        self.assertEqual(accepter_anb2cn("aaaabb"),True)
        self.assertEqual(accepter_anb2cn("aabbccc"),True)
        self.assertEqual(accepter_anb2cn("aaaab"),False)
        self.assertEqual(accepter_anb2cn("aaaccabb"),False)
        anb2cn_comp = accepter_anb2cn.complement()
        self.assertEqual(anb2cn_comp("aaaabb"), False)
        self.assertEqual(anb2cn_comp("aabbccc"), False)
        self.assertEqual(anb2cn_comp("aaaab"), True)
        self.assertEqual(anb2cn_comp("aaaccabb"), True)
        return

    def testintersection(self):
        accepter_anb2cn = regex_to_nfa()("a^*b*b*c^")
        accepter_a2b2cn = regex_to_nfa()("a*a*b*b*c^")
        intersect = accepter_a2b2cn.intersection(accepter_anb2cn)
        self.assertEqual(intersect("aabbccc"),True)
        self.assertEqual(intersect("aabb"),True)
        self.assertEqual(intersect("aaaaabbccc"),False)
        self.assertEqual(intersect("aaaaabbbccc"),False)

    def testisempty(self):
        test1 = regex_to_nfa()("a*a")
        self.assertEqual(test1.is_empty(), False)

    def testeq(self):
        test1 = regex_to_nfa()("(a+b)*(a+b)")
        test2 = regex_to_nfa()("a*a+a*b+b*a+b*b")
        diff = regex_to_nfa()("a*b")


        self.assertEqual(test1==test2, True)

        self.assertEqual(test1==diff, False)
        self.assertEqual(diff==test2, False)

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