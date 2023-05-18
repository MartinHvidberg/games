

class Board:
    """ Defines the game board """

    def __init__(self, COL, ROW, BINDS, COUNT):
        # self.board = [[0]*COL]*ROW  # problematic echoing...!
        self._cols, self._rows = COL, ROW
        self._board = [[0 for i in range(ROW)] for j in range(COL)]  # The COLxROW large board, all zeroes, i.e. unset
        self._binds = dict()
        for bind in BINDS:
            c, r, v = bind
            if not c in self._binds.keys():
                self._binds[c] = dict()
            if not r in self._binds[c].keys():
                self._binds[c][r] = v
                self._board[c][r] = v  # Also set the board, while we are in the loop...
            else:
                print(f"Conflict in Binding: {bind[0]}, {bind[1]} seems to defined more than once: {BINDS}")
        self._cntc = COUNT[0]
        self._cntr = COUNT[1]

        # Impliment BINDS

    def set(self, c, r, v):
        """ Set bord cell x,y to value v """
        self._board[c][r] = v

    def get(self, c, r):
        """ So banale that it's hardly relevant """
        return self._board[c][r]

    def get_col(self, i):
        return self._board[i]

    def get_row(self, i):
        vrow = [col[i] for col in self._board]
        return vrow

    def count(self, mode, i):
        """ Count number of 'ship' celle, per coll or row
            mode: 'c': coll mode, 'r': row mode
            i: the number of the coll/row to count """
        if mode == 'c':
            return self.get_col(i).count(1)
        elif mode == 'r':
            return self.get_row(i).count(1)
        else:
            raise ValueError(f"Illegal mode: {mode}, should be 'c' or 'r'")

    def full(self):
        """ Is all celles, on the board, filled with a non-zero value """
        return any([[v != 0 for v in inner] for inner in self._board])

    def satisfied(self):
        """ All bindings and counts satisfied """
        if all([[self._board[i][j] == self._binds[i][j] for j in self._binds[i].keys()] for i in self._binds.keys()]):
            if any([self._count('c', i) != self._cntc[i] for i in range(self._cntc)]):
                return False
        else:
            print(f"BIND seems to be violates! {self._binds} in {self.board_astext()}")
            return False

    def board_asrawtxt(self):
        str_ou = str()
        for r in reversed(range(self._rows)):  # Screen print top-down
            for c in range(self._cols):
                str_ou += ' ' + self._board[c][r]
            str_ou += "\n"
        return str_ou


    def board_astext(self):
        str_ou = str()
        for r in reversed(range(self._rows)):  # Screen print top-down
            for c in range(self._cols):
                v = self._board[c][r]
                if v == -1:  # No-ship
                    p = ' O'
                elif v == 0:  # unknown
                    p = ' .'
                elif v == 1:  # Ship
                    p = ' X'
                else:
                    raise ValueError(f"Illigal value in board: {self._board}")
                str_ou += p
            str_ou += "\n"
        return str_ou