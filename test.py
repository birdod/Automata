from unittest import TestCase, main
from Theorem import *
from Accepter import *


class AccepterTest(TestCase):
    def test_nfa(self):
        accpeter_3anb = Accepter(
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

class TheoremTest(TestCase):
    def test_nfatodfa(self):
        nfa = Accepter(
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