import unittest

import board_and_pieces as bap

class BoardTestCase(unittest.TestCase):
    def test_board_primitive_functions(self):
        # test _pos2n() and _n2pos()
        brd = bap.Hboard
        for pair in [('a1', 0), ('a2', 1), ('a3', 2), ('a4', 3),
                     ('b1', 4), ('b2', 5), ('b3', 6), ('b4', 7),
                     ('c1', 8), ('c2', 9), ('c3', 10), ('c4', 11),
                     ('d1', 12), ('d2', 13), ('d3', 14), ('d4', 15)]:
            # # print(f"{pair[0]}: {brd._pos2n(self, pair[0])}")
            self.assertEqual(pair[1], brd._pos2n(pair[0]))
            # # print(f"{pair[1]}: {brd._n2pos(self, pair[1])}")
            self.assertEqual(pair[0], brd._n2pos(pair[1]))


if __name__ == '__main__':
    unittest.main()
