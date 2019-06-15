import random

class Suite(object):

    def __init__(self, colour=1):
        if not colour in [1,2]:
            colour = 1
        self.colour = colour

    def flip(self):
        if self.colour == 1:
            self.colour = 2
        elif self.colour == 2:
            self.colour = 1


class TTTboard(object):

    def __init__(self):
        self.board = [0,0,0,0,0,0,0,0,0]  # 0=Empty, 1=x and 2=o
        self._current = 0
        self._done = False
        self._winner = 0
        self._cnt_draws = 0
        self._latest_draw_colour = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current > 8:
            raise StopIteration
        else:
            self._current += 1
            return self.board[self._current - 1]

    def __str__(self):
        b = [str(itm) for itm in self.board]
        return " ".join(b[0:3]) + "\n" + " ".join(b[3:6]) + "\n" + " ".join(b[6:9])

    def set(self, pos, suite):
        if isinstance(suite, Suite):
            colour = suite.colour
            self._cnt_draws += 1
        elif isinstance(suite, int):
            colour = suite
        self.board[pos] = colour
        self._latest_draw_colour = colour
        self._cnt_draws += 1
        self._check_done()

    def get(self, pos):
        return self.board[pos]

    def slices(self):
        lst_slices = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        return [[self.board[n] for n in sli] for sli in lst_slices]

    def vacant(self, pos):
        if self.board[pos] == 0:
            return True
        else:
            return False

    def count(self, suite):
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
            for slice in self.slices():
                if all([tok == 1 for tok in slice]):
                    self._done = True
                elif all([tok == 2 for tok in slice]):
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

class Rolf_player(object):

    def __init__(self):
        return

    def draw_ttt(self, board, suite):
        if isinstance(board, TTTboard):
            if not board.full(suite):
                while True:
                    guess = random.randrange(9)
                    if board.vacant(guess):
                        board.set(guess, suite)
                        break
            else:
                while True:
                    guess1 = random.randrange(9)
                    if board.get(guess1) == suite.colour:
                        board.set(guess1, 0)
                        while True:
                            guess2 = random.randrange(9)
                            if guess2 != guess1:
                                if board.get(guess2) == 0:
                                    board.set(guess2, suite.colour)
                                    break
                        break
        suite.flip()
        return board, suite


if __name__ == '__main__':

    def play_rolf_x2():
        brd_p = TTTboard()
        rolf = Rolf_player()
        suite = Suite(random.randrange(2)-1)
        while not brd_p.done():
            rolf.draw_ttt(brd_p, suite)
        return brd_p.winner()

    brd_tst = TTTboard()
    rolf = Rolf_player()
    suite = Suite()
    while not brd_tst.done():
        rolf.draw_ttt(brd_tst, suite)
    print(brd_tst)
    print("Winner is {}, in {} draws".format(brd_tst.winner(), brd_tst._cnt_draws))

    dic_win = {1: 0, 2: 0}
    for n in range(100000):
        dic_win[play_rolf_x2()] += 1
    print(dic_win)