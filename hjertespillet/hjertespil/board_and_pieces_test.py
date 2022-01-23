import unittest

import board_and_pieces as bap

class BoardTestCase(unittest.TestCase):

    def test_board_primitive_functions(self):
        print("<<< Test _pos2n() and _n2pos() >>>")

        brd = bap.Hboard
        for pair in [('a1', 0), ('a2', 1), ('a3', 2), ('a4', 3),
                     ('b1', 4), ('b2', 5), ('b3', 6), ('b4', 7),
                     ('c1', 8), ('c2', 9), ('c3', 10), ('c4', 11),
                     ('d1', 12), ('d2', 13), ('d3', 14), ('d4', 15)]:
            # # print(f"{pair[0]}: {brd._pos2n(self, pair[0])}")
            self.assertEqual(pair[1], brd._pos2n(pair[0]))
            # # print(f"{pair[1]}: {brd._n2pos(self, pair[1])}")
            self.assertEqual(pair[0], brd._n2pos(pair[1]))
        # Alternatives
        self.assertEqual(0, brd._pos2n('A1'))
        self.assertEqual(4, brd._pos2n('B1'))
        self.assertEqual(8, brd._pos2n('C1'))
        self.assertEqual(12, brd._pos2n('D1'))
        self.assertEqual(13, brd._pos2n('D2'))
        self.assertEqual(14, brd._pos2n('D3'))
        self.assertEqual(15, brd._pos2n('D4'))
        # Illegal input
        # self.assertEqual(0, brd._pos2n('X1')) will raise: ValueError: board position must be a row/col combination from [abcd, 1234]: x1


    def test_board_set_get_pic(self):
        print("<<< Test _set(), get() and _pic() >>>")

        brd = bap.Hboard()
        pce_emp = bap.Hpiece()
        pce_111 = bap.Hpiece(1,1,1)
        pce_222 = bap.Hpiece(2,2,2)
        brd._set(pce_111, 'a1')
        self.assertEqual('<111>', str(brd.get('a1')))
        brd._set(pce_222, 'b2')
        self.assertEqual('<222>', str(brd.get('b2')))
        brd._set(pce_emp, 'a1')
        self.assertEqual('<000>', str(brd.get('a1')))
        self.assertEqual('<222>', str(brd._pic('b2')))
        # Board should now be back in empty position
        self.assertEqual(str(bap.Hboard()), str(brd))

    def test_board_makemove(self):
        print("<<< Test make_move() >>>")

        brd = bap.Hboard()
        brd.make_move('A, b2')
        brd.make_move('a, A1')
        self.assertEqual("|<112>,<000>,<000>,<000>,<000>,<111>,<000>,<000>,<000>,<000>,<000>,<000>,<000>,<000>,<000>,<000>/<121>,<122>,<211>,<212>,<221>,<222>|", brd.as_text_line())
        brd.make_move('A, d4')
        brd.make_move('E, c3')
        self.assertEqual("|<112>,<000>,<000>,<000>,<000>,<111>,<000>,<000>,<000>,<000>,<222>,<000>,<000>,<000>,<000>,<121>/<122>,<211>,<212>,<221>|", brd.as_text_line())
        brd.make_move('c, A4')
        self.assertEqual("|<112>,<000>,<000>,<212>,<000>,<111>,<000>,<000>,<000>,<000>,<222>,<000>,<000>,<000>,<000>,<121>/<122>,<211>,<221>|", brd.as_text_line())
        brd.make_move('b, b3')
        brd.make_move('a, D1')
        brd.make_move('a, C2')
        ##print(brd)  # We now have a X of pieces
        self.assertEqual("|<112>,<000>,<000>,<212>,<000>,<111>,<211>,<000>,<000>,<221>,<222>,<000>,<122>,<000>,<000>,<121>/|", brd.as_text_line())
        # flip a, b up/down and c, d left right
        brd.make_move('a1, b1')  # all mix of upper- and lower-case
        brd.make_move('a4, B4')
        brd.make_move('B2, a2')
        brd.make_move('B3, A3')
        brd.make_move('2c, 1c')  # reverse number-letter
        brd.make_move('3C, 4c')
        brd.make_move('1d, 2D')
        brd.make_move('4D, 3D')
        ##print(brd)  # We now have a X of empty
        self.assertEqual("|<000>,<111>,<211>,<000>,<112>,<000>,<000>,<212>,<221>,<000>,<000>,<222>,<000>,<122>,<121>,<000>/|", brd.as_text_line())


if __name__ == '__main__':
    unittest.main()
