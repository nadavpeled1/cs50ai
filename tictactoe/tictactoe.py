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
    # we will check if there are more X then O on board,
    # more X = its O turns, else X turn
    # Count the number of X and O on the board
    count_x = sum(row.count("X") for row in board)
    count_o = sum(row.count("O") for row in board)

    # Check if the game has ended (someone won or the board is full)
    if winner(board) or (count_o + count_x == 9):
        return None  # Game has ended, return None

    # Determine the next player's turn
    if count_x > count_o:
        return "O"
    else:
        return "X"

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # 1 - use player(board) to check who׳s turn it is
    # 2 - use a nested loop to find every empty cell
    #     if empty cell is found, add the t
    # 3 - return the set
    actions = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 'EMPTY':
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_After = copy.deepcopy(board)
    i, j = action
    board_After[i][j] = player(board)
    return board_After

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # rows&cols check:
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:#row check
            return board[i][0]
        elif board[0][i] == board[1][i] == board[2][i]:#col check
            return board[0][i]

    # diagonal checks
    if (board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0]):
        return board[1][1]

    return None # no winner found

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    #if there are no more actions to do, game over
    return not actions(board)

    # if any(cell == EMPTY for row in board for cell in row):
    #   return False #theres a place for another action
    # return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
