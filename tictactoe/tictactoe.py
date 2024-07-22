"""
Tic Tac Toe Player
"""
from copy import deepcopy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0
    for row in board:
        for value in row:
            if value == X:
                count_x += 1
            elif value == O:
                count_o += 1
    if count_o >= count_x:
        return X
    elif count_o < count_x:
        return O
    else:
        return X
        
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                actions.add((i,j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i,j = action 
    result = deepcopy(board)
    
    if board[i][j] != EMPTY:
        raise ValueError("slot is already filled")
     
    result[i][j] = player(board)
    return result

def vertical(board,i):
    return [row[i] for row in board]

def diagonal(board):
    l1 = [board[i][i] for i in range(len(board))]
    l2 = [board[i][len(board)-1-i] for i in range(len(board))]
    return l1,l2
    
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count(X) == 3:
            return X
        
        elif row.count(O) == 3:
            return O
        
    for i in range(len(board)):
        if vertical(board,i).count(X) == 3:
            return X
        
        elif vertical(board,i).count(O) == 3:
            return O
        
    l1,l2 = diagonal(board)
    
    if l1.count(X) == 3 or l2.count(X) == 3:
        return X
    
    if l1.count(O) == 3 or l2.count(O) == 3:
        return O
        
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    
def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    else:
        for action in actions(board):
            v = max(v,min_value(result(board,action)))
        return v
    
def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    else:
        for action in actions(board):
            v = min(v,max_value(result(board,action)))
        return v  

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if player is x then minimise utility
    if player(board) == X:
        possible = []
        for action in actions(board):
            possible.append((min_value(result(board, action)), action))
        return sorted(possible, reverse=True)[0][1]
    # if player is O then maximise utility
    elif player(board) == O:
        # min player
        possible = []
        for action in actions(board):
            possible.append((max_value(result(board, action)), action))
        return sorted(possible)[0][1]
        