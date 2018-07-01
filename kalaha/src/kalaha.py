

class Kalaha(object):

    variable = "blah"

    def __init__(self, m=6, n=6):  # m: number of houses, n: number of stones in each house
        self.m = m
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

    def move(self, house, player='S'):
        """ Make a single move, i.e. one player grabs all stones in a house, and redistribute them """
        print(" move: {} {}".format(player, house))
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
        self.show()
        if house == 0 or house == 7: # Last drop was in home. You may play again
            return True
        if self.b[house] > 1: # We didn't drop last stone in an empty house
            return self.move(house, player)  # Recursively go again
        else: # last drop was in an empty house
            if (player == 'S' and house > 0 and house < 7) or (player == 'N' and house > 7 and house < 14): # but it was our own house
                return self.move(house, player) # Recursively go again
            else: # and it was opponents's house
                return False # hand over the game to opponene

ka = Kalaha()
ka.show()
strategy = [1,5,4,1,6,5,6,5]
again = True
for stra in strategy:
    print("stra: {}".format(stra))
    if again:
        again = ka.move(stra, 'S')
ka.show()
print(again)