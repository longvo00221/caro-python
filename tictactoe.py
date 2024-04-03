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
    # first make a count number X and O start at 0
    numX = 0
    numO = 0
    # then make 2 for loop the first for is a row of board and the second for is a col depend on Row if row 3 then col is 3
    
    for row in range(len(board)):
        for col in range(len(board[row])):
            # in the for loop make a logic that check if a cell has an X then count the X + 1 , the same with O
            if board[row][col] == X:
                numX += 1
            elif board[row][col] == O:
                numO += 1
    # if the number of X is greater than O so it mean next turn is O
    if numX > numO:
        return O
    # also with X if O is greater than X so next turn is X
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # make an action as a object to check if the cell is empty mean that action is avaible
    actions = set()
    # make a for loop with row and col to check empty
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                # then tell the computer know that cell is empty so update actions
                actions.update({(row, col)})
        # after that return an actions
    return actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """ 
    # check an action if there is no action avaible then exit with exception that is invalid action
    if action not in actions(board):
        raise Exception("Invalid action")
    # the action will start with row and col
    row, col = action
    # make an coppy board to do the action if dont make a coppy it will replace
    board_coppy = copy.deepcopy(board)
    board_coppy[row][col] = player(board)
    return board_coppy
# the function to check row column with 3 same player
def RowCheck(board,player):
    for row in range(len(board)):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    return False
# function check col with 3
def ColCheck(board,player):
    for col in range(len(board)):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    return False
# function check diagonal
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
# winner to check the winner function
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
    # check terminal
    if terminal(board):
        return None
    # check player as X
    elif player(board) == X:
        # make a play as an array to store action
        play = []
        # check action in action is valid or not
        for action in actions(board):
            # then append a valid action in to play ,X is a minvalue
            play.append((min_value(result(board, action)), action))
            # sorted
        return sorted(play,key=lambda x:x[0], reverse=True)[0][1]
    elif player(board) == O:
        # make a play as an array to store action
        play = []
        # check action in action is valid or not
        for action in actions(board):
            # then append a valid action in to play ,O is a maxvalue
            play.append((max_value(result(board, action)), action))
        # sorted
        return sorted(play,key=lambda x:x[0], reverse=False)[0][1]
