import unittest

import bp_board

""" Bismarck puzzle: Unit test for class Board """

class BoardTestCase(unittest.TestCase):

    def build_board_0(self):  # Minimal, yet unrealistic, empty Board
        return bp_board.Board(9, 9, [], [[],[]])

    def build_board_1(self):  # Realistic Board
        COL, ROW = 9, 9
        BINDS = [[0,8,1],[0,7,-1],[1,8,-1],[1,2,1],[7,2,1],[7,1,-1]]  # Given by the puzzle
        COUNT = [[1,4,2,3,2,4,1,4,1],[1,4,4,1,1,5,1,1,4]]  # Defines target counts by Col and Row
        return bp_board.Board(COL, ROW, BINDS, COUNT)

    def build_board_a(self):  # Not a valid board, but convenient for som tests
        COL, ROW = 9, 9
        brd_ret = bp_board.Board(COL, ROW, [], [[],[]])
        for c in range(COL):
            for r in range(ROW):
                brd_ret.set(c, r, chr(33+(c*9)+r))
        return brd_ret

    def test_init(self):
        """ Thes the newly initialised Board object
            brd0: Mainly internal, not-user-exposed parameters are checked
            brd1: A valid filled Board """

        brd0 = self.build_board_0()
        self.assertIsInstance(brd0, bp_board.Board)
        self.assertEqual(9, brd0._cols)
        self.assertEqual(9, brd0._rows)
        self.assertEqual(9, len(brd0._board))
        for col in brd0._board:
            self.assertEqual(9, len(col))
        self.assertIsInstance(brd0._binds, dict)
        self.assertIsInstance(brd0._cntc, list)
        self.assertIsInstance(brd0._cntr, list)

        brd1 = self.build_board_1()
        self.assertEqual(1, brd1._board[0][8])  # Bound ship in 0,8
        self.assertEqual(1, brd1._binds[0][8])
        self.assertEqual(-1, brd1._board[0][7])  # Bound empty in 0,7
        self.assertEqual(-1, brd1._binds[0][7])
        self.assertEqual(0, brd1._board[8][8])  # cell 8,8 is empty
        self.assertFalse(8 in brd1._binds.keys())  # Key not set since all cell in col 8 are empty and unknown
        self.assertFalse(4 in brd1._binds[0].keys())  # Key not set since all cell 0,4 is empty and unknown
        self.assertEqual(brd1._cols, len(brd1._cntc))
        self.assertEqual(brd1._rows, len(brd1._cntr))
        self.assertEqual(2, brd1._cntc[4])  # just sample test a single specific value
        self.assertEqual(1, brd1._cntr[4])

    def test_get_and_set(self):
        """ test get() and set() """
        brd1 = self.build_board_1()
        self.assertEqual(-1, brd1.get(7, 1))  # read from initialised data
        self.assertEqual(0, brd1.get(1, 6))
        self.assertEqual(1, brd1.get(0, 8))
        self.assertEqual(0, brd1.get(4, 6))  # read test cell
        brd1.set(4,6,1)  # change test cell
        self.assertEqual(1, brd1.get(4, 6))  # read test cell, again
        brd1.set(4,6,-1)  # change test cell
        self.assertEqual(-1, brd1.get(4, 6))  # read test cell, again
        brd1.set(4,6,0)  # change test cell
        self.assertEqual(0, brd1.get(4, 6))  # read test cell, again

    def test_getcol_and_getrow(self):
        """ Test get_col() and get_row() """
        brda = self.build_board_a()
        print(f"brdA:\n{brda.board_asrawtxt()}")


    def test_count(self):
        """ test count() """
        brd1 = self.build_board_1()
        print(brd1.board_astext())
        self.assertEqual(1, brd1.count('c', 0))
        self.assertEqual(1, brd1.count('c', 1))
        self.assertEqual(0, brd1.count('c', 2))
        # # self.assertEqual(1, brd1.count('r', 0))
        # # self.assertEqual(0, brd1.count('r', 1))
        # self.assertEqual(2, brd1.count('r', 7))

    # def test_something(self):
    #     self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
