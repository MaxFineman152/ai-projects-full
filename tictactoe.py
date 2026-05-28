"""
Tic Tac Toe Player
"""

import math
import copy

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
    X_count = 0  # X turns taken
    O_count = 0  # O turns taken

    # Count X and O
    for row in board:
        X_count += row.count(X)
        O_count += row.count(O)
    
    # Check if X has more than 0
    if X_count == O_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()

    # If space not taken, append as available choice
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == EMPTY:
                actions_set.add((i, j))

    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Assign row and column
    i = action[0]
    j = action[1]

    # Check action possible
    if board[i][j] != EMPTY:
        raise Exception("Invalid action: space occupied")
    if i not in range(3) or j not in range(3):
        raise Exception("Invalid action: space not on grid")
    
    # Return new board with action taken
    updated_board = copy.deepcopy(board)
    updated_board[i][j] = player(board)

    return updated_board
    
    
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # All possible victories
    victories_list = [{(0, 0), (0, 1), (0, 2)}, 
                      {(1, 0), (1, 1), (1, 2)},
                      {(2, 0), (2, 1), (2, 2)},
                      {(0, 0), (1, 0), (2, 0)},
                      {(0, 1), (1, 1), (2, 1)},
                      {(0, 2), (1, 2), (2, 2)},
                      {(0, 0), (1, 1), (2, 2)},
                      {(0, 2), (1, 1), (2, 0)}]
    
    X_list = []
    # Add X positions
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == X:
                X_list.append((i, j))

    # See if X has met a win condition
    for three in victories_list:
        if three.issubset(X_list):
            return X
        
    O_list = []
    # Add O positions
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == O:
                O_list.append((i, j))

    # See if O has met a win condition
    for three in victories_list:
        if three.issubset(O_list):
            return O

    return None  # If no winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    elif len(actions(board)) == 0:  # No more free moves
        return True
    else:
        return False


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


def max_value(board, alpha, beta):
    """
    Returns the maximum possible utility achievable from a boardstate.
    """
    # Check if game over
    if terminal(board) == True:
        return utility(board)
    
    else:
        v = float("-inf")  # Start with lowest utility and increase
        for action in actions(board):
            score = result(board, action)
            v = max(v, min_value(score, alpha, beta))
            # Alpha-Beta pruning
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v


def min_value(board, alpha, beta):
    """
    Returns the minimum possible utility achievable from a boardstate.
    """
    # Check if game over
    if terminal(board) == True:
        return utility(board)
    
    else:
        v = float("inf")  # Start with highest utility and decrease
        for action in actions(board):
            score = result(board, action)
            v = min(v, max_value(score, alpha, beta))
            # Alpha-Beta pruning
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check if game over
    if terminal(board) == True:
        return None
    
    # Shortcut - known best move
    elif board == initial_state():
        return (0, 0)
    
    else:
        # Set up player, alpha and beta
        current_player = player(board)
        alpha = float("-inf")
        beta = float("+inf")

        # AI plays X
        if current_player == X:
            best_score = float("-inf")  # Worst score
            best_move = None

            # Check all actions
            for action in actions(board):
                score = result(board, action)
                branch = min_value(score, alpha, beta)  # Iterate
                # Update score
                if best_score < branch:
                    best_score = branch
                    best_move = action
                alpha = max(alpha, best_score)
            return best_move
        
        # AI plays O
        if current_player == O:
            best_score = float("inf")  # Worst score
            best_move = None

            # Check all actions
            for action in actions(board):
                score = result(board, action)
                branch = max_value(score, alpha, beta)  # Iterate
                # Update score
                if best_score > branch:
                    best_score = branch
                    best_move = action
                beta = min(beta, best_score)
            return best_move
