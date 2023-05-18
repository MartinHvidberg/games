
import bp_board

# All coordinates x,y are Math-style (vertical x, horizontal y and 0,0 is Lower Left corner!)
# Values: 1: Ship, 0: Unknown, -1: No-ship

COL, ROW = 9, 9
BINDS = [[0,8,1],[0,7,-1],[1,8,-1],[1,2,1],[7,2,1],[7,1,-1]]  # Given by the puzzle
COUNT = [[1,4,2,3,2,4,1,4,1],[1,4,4,1,1,5,1,1,4]]  # Defines target counts by Col and Row

brd = bp_board.Board(COL, ROW, BINDS, COUNT)

print(f"Initial Board:\n{brd.board_astext()}")

for i in range(brd._cols):
    for j in range(brd._rows):
        # for v in brd.options(i, j):
        #     if brd.full():
        #         if brd.satisfied():
        #             print(f"\Solution:\n{brd.board_astext()}")
        pass

pass