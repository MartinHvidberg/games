

class Hboard:
    """ Defines the 4x4 square game board
    and the set of pieces that goes with it """

    def __init__(self):
        self.board = [Hpiece()] * 16  # 4x4 Empty pieces
        self.x_pcs = self.create_piece_set()  # the xtra (reserve) pieces, outside the board
        self._current = 0  # some internal counter for iterator __next__
        self._done = False  # Initially False, but become True if game is done
        self._winner = ''  # Initially '', later holds the id of the winner
        self._cnt_draws = 0  # Number of draws in the game so far
        #self._latest_draw_id = 0  # Id of the latest player to draw

    def __iter__(self):
        return self

    def __next__(self):
        if self._current > 8:
            raise StopIteration
        else:
            self._current += 1
            return self.board[self._current - 1]

    def __str__(self):
        b = [str(itm) if isinstance(itm, Hpiece) else '<--->' for itm in self.board]
        x = [str(tok) for tok in self.x_pcs]
        r = [chr(n+65) for n in range(len(x))]
        lst_rest = [str(itm).replace("'", "").replace("(", "").replace(")", "").replace(", ", ":") for itm in list(zip(r,x))]  # ToDo: Find a prettier way
        str_a = "    a     b     c     d"
        str_b = "1 " + ",".join(b[0:4]) + "\n2 " + ",".join(b[4:8]) + "\n3 " + ",".join(b[8:12]) + "\n4 " + ",".join(b[12:16])
        str_x =  ", ".join(lst_rest)
        return str_a + "\n" + str_b + "\n\n reserve: " + str_x

    @staticmethod
    def tile_valid(str_pos):
        """ Check if the given tile (board position) is valid.
        :param str_pos: string of row,col position"""
        if not (isinstance(str_pos, str) and len(str_pos) == 2):
            return False  # str_pos must be string of length 2
        if not all([any([itm.lower() in ['a', 'b', 'c', 'd'] for itm in str_pos]),
                    any([itm in ['1', '2', '3', '4'] for itm in str_pos])]):
            print(f"board position must be a row/col combination from [abcd, 1234]: {str_pos}")
            #return False
            raise ValueError(f"board position must be a row/col combination from [abcd, 1234]: {str_pos}")
        return True  # No problems detected ...

    @staticmethod
    def _pos2n(pos):
        """ translate from pos to n
        e.g. a1 = 0, a4 = 3, b1 = 4, ... d4 = 15 """
        if Hboard.tile_valid(pos):
            cols, rows = "abcd", "1234"
            num_c = max(cols.find(pos[0]), cols.find(pos[1]))
            num_r = max(rows.find(pos[0]), rows.find(pos[1]))
            return num_c * 4 + num_r
        else:
            raise ValueError(f"_pos2n() can't handle input, since it's not tile_valid(): {pos}")

    @staticmethod
    def _n2pos(n):
        """ reverse of _pos2n() """
        if isinstance(n, int) and 0 <= n < 16:
            cols, rows = "abcd", "1234"
            # print(f"x {n} > {n//4}, {n%4} >> {cols[n//4]}{rows[n%4]}")
            return f"{cols[n//4]}{rows[n%4]}"
        else:
            raise ValueError

    @staticmethod
    def create_piece_set():
        """ Creates a set of 8 pieces that suites this game """
        lst_ret = list()
        for c in range(1, 3):  # Colour
            for s in range(1, 3):  # Shape
                for h in range(1, 3):  # Hollow
                    lst_ret.append(Hpiece(c, s, h))
        return (lst_ret)

    def get(self, pos):
        """ Tell what is on that position, without picking it up
        Returns a type Hpiece """
        return self.board[Hboard._pos2n(pos)]

    def pic(self, pos):
        """ Pick up the piece in this position
        pos of type b4 is in the board, while single letter (max H) is the reserve
        :param pos: a string length 1 or 2 """
        if len(pos) == 1:
            num_pos = 'ABCDEFGH'.find(pos.upper())
            if num_pos < len(self.x_pcs):
                return self.x_pcs.pop(num_pos)
        if len(pos) == 2:
            pce_ret = self.get(pos)
            self.set(Hpiece(), pos)
            return pce_ret
        else:
            raise ValueError(f"pic() can't handle inout: {pos}")

    def set(self, pce, pos):
        """ Set the piece on that position """
        num_pos = Hboard._pos2n(pos)
        print(f" bb: {pce}, {pos}/{num_pos},\n{self}")
        self.board[num_pos] = pce  xxx why is set not holding...
        print(f" ba: {pce}, {pos}/{num_pos},\n{self}")

    def move_validator(self, mve_a):
        """ Tests a move, to access if it's valid.
        :param tuple mve: tuple of 2 items, each string describing board position, or single letter for reserve pieces.
            e.g. a3 b2 or A b2. Any non letter or digit is a seperator
            Board locations are pairs of row, col. Rows a, b, c and d, while Cols are 1, 2, 3 and 4
            Spare pieces (not yet put on the board) are A through H.
        :return tuple of boolean and str: False if violation is found, otherwise True. String describes violation """

        lst_mve = "".join([tok if tok.lower() in 'abcdefgh1234' else ' ' for tok in mve_a]).split(' ')  # make all separators ' '
        lst_mve = list(filter(lambda a: a != '', lst_mve))  # remove all empty entries
        if len(lst_mve) != 2:
            return False, f"Invalid move: more than two locations specified: {lst_mve}"
        # Check the From item
        itm_f = lst_mve[0]
        num_reserve_slot = 'ABCDEFGH'.find(itm_f.upper())
        bol_valid_reserve = (num_reserve_slot > -1) and (num_reserve_slot < len(self.x_pcs))
        bol_valid_bordpce = (Hboard.tile_valid(itm_f)) and (not self.vacant(itm_f))
        if not any([bol_valid_bordpce, bol_valid_reserve]):
            return False, f"Invalid move: From part do not specify a valid piece: {lst_mve}"
        # Check the To item
        itm_t = lst_mve[1]
        print(f"move_validator(): lst_mve: {lst_mve}")
        return True, ", ".join(lst_mve)

    def move(self, str_m):
        """ Make the actual move
        Don't assume it have been validated """
        bol_go, str_mv = self.move_validator(str_m)
        if bol_go:
            f, t = [tok.strip(',') for tok in str_mv.split()]  # str in form 'A, b2' or 'a1, b2'
            if len(f) in [1, 2]:
                pce_a = self.pic(f)
                print(f" --- got piece: {pce_a}")
                self.set(pce_a, t)
                print(f" --- sot it at: {t}")
            else:
                raise ValueError(f"move(): Very strange. From sems to be neither length 1 nor 2? {str_mv}")
        else:
            raise ValueError(f"move(): Can't handle input, since it didn't pass move_validator(): {str_mv}")

    def slices(self):
        """
        For each 4-on-a-row field combinations, returns the Pieces.
        :return: list of 10 lists of each 4 Hpiece-objects
        """
        lst_slices = [
            [0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],
            [0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15],
            [0,5,10,15],[3,6,9,12]
        ]
        return [[self.board[n] for n in sli] for sli in lst_slices]

    def vacant(self, pos):
        return self.get(pos).is_empty()

    def uniform_att(self, slice_of_pieces):
        """ For the slice_of_pieces check if there are any uniform attributes
        :param list slice_of_pieces: list of 4 Hpiece
        :return: List of True/False for uniformity found in any of the attributes, e.g. colour, shape, hollow, etc.
        """
        return [True, False, False]

    def _check_done(self):
        self._done = any([any(self.uniform_att(lst_pcs)) for lst_pcs in self.slices()])

    def done(self):
        self._check_done()
        return self._done

    def winner(self):
        if self.done():
            return self._winner
        else:
            return None

class Hpiece:
    """ Define a piece/token/brik """

    def __init__(self, c=0, s=0, h=0):
        self._colour = c  # [0: unset, 1: red, 2: black]
        self._shape = s  # [0: unset, 1: round, 2: heart]
        self._hollow = h  # [0: unset, 1: hollow, 2: solid]

    def __str__(self):
        return f"<{self._colour}{self._shape}{self._hollow}>"

    def valid(self):
        if not all([itm in [0, 1, 2] for itm in [self._colour, self._shape, self._hollow]]):
            return False
        else:
            if (all([itm == 0 for itm in [self._colour, self._shape, self._hollow]]) or
                all([itm in [1, 2] for itm in [self._colour, self._shape, self._hollow]])):
                return True
            else:
                return False

    def is_empty(self):
        if all([itm == 0 for itm in [self._colour, self._shape, self._hollow]]):
            return True
        else:
            return False


