import unittest
import tictactoe
import math

X = "X"
O = "O"
EMPTY = None
initial_board = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
board_1 = [[X, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

actions_1 = {(0, 1), (1, 2), (2, 1), (0, 0), (1, 1), (2, 0), (0, 2), (2, 2), (1, 0)}

class TestFunctions(unittest.TestCase):
    
    def test_initialState(self):
        self.assertTrue(tictactoe.initial_state() == initial_board )
    
    def test_player(self):
        self.assertTrue(tictactoe.player(tictactoe.initial_state()) == X)
        self.assertTrue(tictactoe.player(board_1) == O)
        
    def test_actions(self):
        self.assertTrue(tictactoe.actions(board_1) == actions_1)

if __name__ == "___main__":
    unittest.main()