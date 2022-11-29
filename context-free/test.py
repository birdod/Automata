from unittest import TestCase, main
from Theorem import *
from Accepter import *


class GreibachAccepterTest(TestCase):
    def test_npda(self):
        accepter = GreibachAccepter(
            {
                ('a','S'): [['A']],
                ('a','A'): [['C', 'B','A'],['lambda']],
                ('b','A'): [['B']],
                ('b','B'): [['lambda']],
                ('c','C'): [['lambda']]
            }
        )
        self.assertEqual(accepter("aaabc"), True)


if __name__ == "__main__":
    main()