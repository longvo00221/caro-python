"""
Tic Tac Toe Player
"""

import copy
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

    numX = 0
    numO = 0

    for row in range(len(board)):
        for col in range(len(board[row])):

            if board[row][col] == X:
                numX += 1
            elif board[row][col] == O:
                numO += 1

    if numX > numO:
        return O

    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = set()

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:

                actions.update({(row, col)})

    return actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """ 

    if action not in actions(board):
        raise Exception("Invalid action")

    row, col = action

    board_coppy = copy.deepcopy(board)
    board_coppy[row][col] = player(board)
    return board_coppy

def RowCheck(board,player):
    for row in range(len(board)):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    return False
def ColCheck(board,player):
    for col in range(len(board)):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    return False
def CheckFirstDiagonal(board,player):
    calculator = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if row == col and board[row][col] == player:
                calculator += 1
    if calculator == 3:
        return True
    else:
        return False
def checkSecondDiagonal(board,player):
    calculator = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if (len(board) - row - 1) == col and board[row][col] == player:
                calculator += 1
    if calculator == 3:
        return True
    else:
        return False
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if RowCheck(board , X) or ColCheck(board,X) or CheckFirstDiagonal(board,X) or checkSecondDiagonal(board,X):
        return X
    elif RowCheck(board , O) or ColCheck(board,O) or CheckFirstDiagonal(board,O) or checkSecondDiagonal(board,O):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X:
        return True
    elif winner(board) == O:
        return True
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
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
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v
def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    elif player(board) == X:
        play = []
        for action in actions(board):
            play.append((min_value(result(board, action)), action))
        return sorted(play,key=lambda x:x[0], reverse=True)[0][1]
    elif player(board) == O:
        play = []
        for action in actions(board):
            play.append((max_value(result(board, action)), action))
        return sorted(play,key=lambda x:x[0], reverse=False)[0][1]
