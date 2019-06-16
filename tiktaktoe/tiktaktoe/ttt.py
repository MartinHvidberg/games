import secrets

class Suite(object):

    def __init__(self, colour=2):
        if not colour in [1,2]:
            print("err")
            colour = 2
        self.colour = colour

    def next(self):
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


class Player(object):

    def __init__(self, board, who):
        return

    # def whos_next(self, who):
    #     who.next()
    #     return who

class Odin_player(Player):
    """ One
    Only looks at the present board, no long term strategy.
    Avoids the most obvious traps, and know s strategy ..."""

    def __init__(self):
        return

    def draw_ttt(self, board, who):
        # Look for immediate Win
        for sli in board.slices:
            if can_win()
        # Look for immediate Lose

        # Look for other options ...
        who.next()
        return board, who

class Rolf_player(Player):
    """ Rolf (Random Of Legal Fields)
    This player will pick a random, though legal, move.
    No strategy involved - pure random play. """
    def __init__(self):
        return

    def draw_ttt(self, board, who):
        if isinstance(board, TTTboard):
            if not board.full(who):
                while True:
                    guess = secrets.randbelow(9)
                    if board.vacant(guess):
                        board.set(guess, who)
                        break
            else:
                while True:
                    guess1 = secrets.randbelow(9)
                    if board.get(guess1) == who.colour:
                        board.set(guess1, 0)
                        while True:
                            guess2 = secrets.randbelow(9)
                            if guess2 != guess1:
                                if board.get(guess2) == 0:
                                    board.set(guess2, who.colour)
                                    break
                        break
        who.next()
        return board, who


if __name__ == '__main__':

    def play_rolf_x2():
        brd_p = TTTboard()
        rolf = Rolf_player()
        who = Suite(secrets.choice([1,2]))
        while not brd_p.done():
            rolf.draw_ttt(brd_p, who)
        return brd_p.winner()

    dic_win = {1: 0, 2: 0}
    for n in range(10000):
        dic_win[play_rolf_x2()] += 1
    print(dic_win)
