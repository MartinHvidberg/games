
class Hpiece(object):
    """ Define a piece/token/brik """

    def __init__(self, c=0, s=0, h=0):
        self._colour = c  # [0: unset, 1: red, 2: black]
        self._shape = s  # [0: unset, 1: round, 2: heart]
        self._hollow = h  # [0: unset, 1: hollow, 2: solid]

    def __str__(self):
        return f"<{self._colour}{self._shape}{self._hollow}>"


class Hboard(object):
    """ Defines the 4x4 square game board
    and the set of pieces that goes with it """

    def __init__(self):
        self.board = [None] * 16  # None=Empty
        self.x_pcs = self.create_piece_set()
        self._current = 0  # some internal counter for iterator __next__
        self._done = False  # Initially False, but become True if game is done
        self._winner = 0  # Initially 0, later holds the id of the winner
        self._cnt_draws = 0  # Number of draws in the game so far
        self._latest_draw_id = 0  # Id of the latest player to draw

    def __iter__(self):
        return self

    def __next__(self):
        if self._current > 8:
            raise StopIteration
        else:
            self._current += 1
            return self.board[self._current - 1]

    def __str__(self):
        b = [str(itm) if isinstance(itm, str) else '<--->' for itm in self.board]
        x = [str(tok) for tok in self.x_pcs]
        str_b = ",".join(b[0:4]) + "\n" + ",".join(b[4:8]) + "\n" + ",".join(b[8:12]) + "\n" + ",".join(b[12:16])
        str_x = "[" + " ".join(x) + "]"
        return str_b + "\n" + str_x

    def create_piece_set(self):
        """ Creates a set of 8 pieces that suites this game """
        lst_ret = list()
        for c in range(1, 3):  # Colour
            for s in range(1, 3):  # Shape
                for h in range(1, 3):  # Hollow
                    lst_ret.append(Hpiece(c, s, h))
        return (lst_ret)

    def set(self, pos, pce):
        if isinstance(pce, Hpiece):
            self.board[pos] = pce
            self._latest_draw_colour = player_id
            self._cnt_draws += 1
            self._check_done()

    def get(self, pos):
        """ Returns a type Hpiece, or None """
        return self.board[pos]

    def slices(self):
        """ 0 1 2 3
            4 5 6 7
            8 9 0 1
            2 3 4 5 """
        lst_slices = [
            [0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],
            [0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15],
            [0,5,10,15],[3,6,9,12]
        ]
        return [[self.board[n] for n in sli] for sli in lst_slices]

    def vacant(self, pos):
        return self.board[pos] is None

    def count(self, suite):
        """ Relic from TTT, might not make sense here """
        cnt = 0
        for pos in self.board:
            if pos == suite.colour:
                cnt += 1
        return cnt

    def full(self, suite):
        if self.count(suite) > 2:
            return True
        else:
            return False

    def _check_done(self):
        if not self._done:
            if any([any(uniform_att(lst_pcs) for lst_pcs in self.get_all_series())]):
                self._done = True
            if self._done:
                self._winner = self._latest_draw_colour

    def done(self):
        self._check_done()
        return self._done

    def winner(self):
        if self.done():
            return self._winner
        else:
            return None


if __name__ == "__main__":

    brd_b = Hboard()
    print(f"board: \n{brd_b}")
