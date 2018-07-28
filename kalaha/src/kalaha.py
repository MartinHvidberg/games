
import copy

class Kalaha(object):

    variable = "blah"

    def __init__(self, m=6, n=6):  # m: number of houses, n: number of stones in each house
        self.m = m
        self.n = n
        self.b = [] # Board: South houses from west, south home, north houses from east, north home
        self.initboard(m,n)

    def initboard(self, m, n):
        """ Initialize the board.
        Houses numbered as follow
        v 13 12 11 10 9  8  <
        0                   7
        > 1  2  3  4  5  6  ^
        """
        for p in range(m*2+2):
            self.b.append(n)  # m stones in all houses
        self.b[0] = 0  # empty south house
        self.b[m+1] = 0  # empty north house

    def __str__(self):
        return str(self.b)

    def show(self):
        print("  {:2} {:2} {:2} {:2} {:2} {:2} ".format(self.b[13],self.b[12],self.b[11],self.b[10],self.b[9],self.b[8]))
        print("{:2}                 {:2}".format(self.b[0],self.b[7]))
        print("  {:2} {:2} {:2} {:2} {:2} {:2} ".format(self.b[1],self.b[2],self.b[3],self.b[4],self.b[5],self.b[6]))

    def get_board(self):
        return self.b

    def set_board(self, board=None):
        if board:
            if isinstance(board, list):
                if len(board) == (self.m+1)*2:
                    self.b = board
        return None

    def get_my_houses(self, player="S"):
        if player not in ['N', 'S']:
            raise ValueError("Player must be 'N' or 'S'")
        if player == "S":
            return range(1, self.m)
        elif player == "N":
            return range(1+(self.m+1), 1+(2*self.m))

    def score(self, player='S'):
        if player not in ['N', 'S']:
            raise ValueError("Player must be 'N' or 'S'")
        if player == 'S':
            return self.b[7]
        else:
            return self.b[0]

    def move(self, house, player='S'):
        """ Make a single move, i.e. one player grabs all stones in a house,
        and redistribute them. An keep grabbing, as long the last stone drops in
        a house with stones.
        :param house int: The house to grab
        :param player str: "S" or "N"
        :return: True if it's still your turn, i.e. you dropped last stone
         in your own home, otherwise it returns False
        """
        ##print(" move: {} {}".format(player, house))
        if player not in ['N', 'S']:
            raise ValueError("Player must be 'N' or 'S'")
        if player=='N':
            house += 7
        hand = self.b[house]
        self.b[house] = 0
        while hand > 0:
            house += 1
            if house == 14:  # We shot 1 over the top, loop to start
                house = 0
            if player == 'N':
                if house == 6:
                    house = 7  # N don't drop in S's home
            else:
                if house == 0:
                    house = 1  # S don't drop in N's home
            # Drop
            self.b[house] += 1
            hand -= 1
        ##self.show()
        if house == 0 or house == 7: # Last drop was in home. You may play again
            return True
        if self.b[house] > 1: # We didn't drop last stone in an empty house
            return self.move(house, player)  # Recursively go again
        else: # last drop was in an empty house
            if (player == 'S' and house > 0 and house < 7) or (player == 'N' and house > 7 and house < 14): # but it was our own house
                #print("regel x")
                return self.move(house, player) # Recursively go again
            else: # and it was opponents's house
                return False # hand over the game to opponent


def playall(board=None, player="S", strategy = []):
    """
    Plays the given board to end, exploring all possible strategies recursively
    :param board: List of int. The present situation of the board
    :param player: 'N' or 'S'
    :param strategy: List of int. The moves this player have made, up till now
    :return: TBD, likely nothing
    """
    if not board:
        board = [0, 6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6]
    if not isinstance(board, list):
        print("Board is not list")
        return None
    if len(board) != 14:
        print("Board not length 14")
        return None
    if len(strategy) > 9:
        #print("We are in too deep: {}".format(strategy))
        return None
    for h in [1,2,3,4,5,6]:
        if board[h] > 0:  # there exist stones to grab
            ka = Kalaha()
            ka.set_board(copy.deepcopy(board))
            if ka.move(h, player):  # True if we didn't die
                board_nxt = copy.deepcopy(ka.get_board())
                strat_nxt = copy.deepcopy(strategy)
                strat_nxt.append(h)
                playall(board_nxt, player, strat_nxt)
                del ka, board_nxt, strat_nxt
            else:  # it was a valid move, but we lost the initiative
                strat_nxt = copy.deepcopy(strategy)
                strat_nxt.append(h)
                #if ka.score(player) > 36 and len(strat_nxt) <= 4:
                if ka.score(player) > 56:
                    print("End of initiative: {} with points {}".format(strat_nxt, ka.score(player)))
                del ka, strat_nxt


##  # Some test cases
if False:
    ka = Kalaha()
    print(ka.get_my_houses('N'))


### Check the strategy of the boys
# https://politiken.dk/viden/Viden/art6610055/S%C3%A5dan-vinder-du-kalaha-hver-gang
ka = Kalaha()
strategy = [1,5,4,1,6,5,6,5]  # strategy as described in paper
again = True  # We are allowed to start
for stra in strategy:
    if again:
        again = ka.move(stra, 'S')
ka.show()  # show the board
print(again)  # make sure we have no right to continue
print(ka.score())  # Print the score (assomed 39)
del ka, again,stra, strategy


### Check some strategy... 3,2 = 7
ka = Kalaha()
strategy = [3,2]  # strategy as described in paper
again = True  # We are allowed to start
for stra in strategy:
    if again:
        again = ka.move(stra, 'S')
ka.show()  # show the board
print(again)  # make sure we have no right to continue
print(ka.score())  # Print the score (assomed 39)
del ka, again,stra, strategy


### Find optimal strategy
print("\nPLAY:")
#playall(None, 'S')

