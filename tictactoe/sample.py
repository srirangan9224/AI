import tictactoe


X = "X"
O = "O"
EMPTY = None

board_1 = [[X, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
print(tictactoe.max_value(board_1))