

""" Thoughts:
    Object landscape: Game, Player, Board, Piece

    a Game have x Players and 1 Board
    a Board holds the Pieces
    the Game runs the Players
    the Players run the Board, in turn
    the Board runs the Pieces.

    After each move, the Board self-evaluated on 'done' and 'winner'
    therefore the Player have to ID himself to the Board when running it.

    The 'done' and 'winner' info should progress back through the Player, to the Game.

    Needed functionality:

    Game: init, next_player, give_turn, play, done
    Player: analyse..., draw, done
    Board: init, get, set, series, series_stat, done
    Piece: empty, c, s, h

    """

import random

import board_and_pieces as B
import players as P

class HGame:
    """ The Game """
    def __init__(self, lst_plrs):
        """ Initialise the Game, incl. the Board, Pieces and Players
        :lst_plrs: list of tuples of str_name and str_type. eg. [("A", "KB"), ("B", "Rolf")] """
        self._board = B.Hboard()
        self._players = [P.player(tup_pl) for tup_pl in lst_plrs]  # Make players from the nemes and types
        self._current_player = 0
        self.random_next_player()  # Shuffle who starts...
        self.winner = None
        self.done = False

    def random_next_player(self):
        """ Randomly sets value for next player, to be used for choosing a player to start """
        self._current_player = random.randint(0, len(self._players) - 1)

    def next_player(self):
        """ Select the next player, before giving him his turn """
        self._current_player += 1
        if not self._current_player < len(self._players):
            self._current_player = 0

    def give_turn(self):
        plr_a = self._players[self._current_player]
        self._board = plr_a.draw(self._board)
        if self._board.done():  # trigger the Boards self check for Done
            self.winner = plr_a.name
        self.next_player()

    def play(self):
        print(f"Game begin: {self._players[self._current_player].name} starts")
        while not self.done:
            self.give_turn()
        print(f"Game over. Winner is: {self.winner}")


if __name__ == "__main__":

    gam_a = HGame([("A", "Rolf"), ("B", "KB")])  # Initialise the game with player names and types
    gam_a.play()
