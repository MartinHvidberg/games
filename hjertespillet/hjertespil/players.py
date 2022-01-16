

class Hplayer:
    """ A player - This is a basic class, that may be ancestor to players with more advanced strategies """
    def __init__(self):
        self.name = "Abu"  # Absolutely Basic Understanding. This one can't really play...
        self.done = False

    def draw(self, brd):
        # ToDo: Make a move ...

        return brd

class Rolf(Hplayer):
    """ Player type 'Rolf' - Random Of Legal Field """
    def __init__(self, tup_p):
        super().__init__()
        self.name = tup_p[0]

    def draw(self, brd):
        # ToDo: Make a move ...

        return brd

class Keyb(Hplayer):
    """ Player type 'KB' - Keyboard, i.e. Human interface """
    def __init__(self, tup_p):
        super().__init__()
        self.name = tup_p[0]

    def draw(self, brd):
        # Make a move ...
        bol_okay = False
        while not bol_okay:
            print(f"Keyboard move:\n{brd}")
            mv = input('Choose a move, e.g. A b2 or a3 b2.\n')
            print(f"Keyb: {mv}")
            bol_okay, str_mv = brd.move_validator(mv)
            if not bol_okay:
                print(str_mv)  # move was invalid, printing why.
        print(f"making move: {str_mv}")
        return brd

def player(tup_p):
    """ Call this to generate a player of predefined type
    :parapm tuple tup_p: tuple of 'name' and 'type' of player to re generated
    :return: Hplayer descendent class, of the right type, or simple Hplayer if type unknown
    """
    if tup_p[1] == "Rolf":
        return Rolf(tup_p)
    elif tup_p[1] == "KB":
        return Keyb(tup_p)
    else:
        print(f"::players.py: players(): Warning: Unknown player type: {tup_p[1]}, returns base type Hplayer()")
        return Hplayer(tup_p)