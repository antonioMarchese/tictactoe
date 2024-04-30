"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None
INF = 1000000


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board: list[list]) -> str:
    """
    Returns player who has the next turn on a board.
    """
    X_plays = O_plays = 0
    for row in board:
        X_plays += row.count(X)
        O_plays += row.count(O)
    return X if (X_plays + O_plays) % 2 == 0 else O


def actions(board: list[list]) -> set[tuple] | set:
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                possible_actions.add((row, col))

    return possible_actions


def result(board: list[list], action: tuple[int, int]) -> list[list]:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row, col = action
    if row not in range(3) or col not in range(3):
        raise IndexError("actions must be restricted to [0, 2]")

    if board[row][col] is not EMPTY:
        raise IndexError("this place has alredy a value")

    new_board = copy.deepcopy(board)
    current_player = player(board)
    row, col = action
    new_board[row][col] = current_player
    return new_board


def winner(board: list[list]) -> str | None:
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontally
    for row in board:
        if row.count(X) == 3:
            return X

        if row.count(O) == 3:
            return O

    # Diagonally
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[-1][0] == board[1][1] == board[0][2]:
        return board[-1][0]

    # Vertically
    for i in range(len(board)):
        val = board[0][i]
        score = 1
        for j in range(1, len(board)):
            if val == board[j][i]:
                score += 1
        if score == 3:
            return val

    return None


def terminal(board: list[list]) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    empty_spaces = 0
    for row in board:
        empty_spaces += row.count(EMPTY)

    return empty_spaces == 0


def utility(board: list[list]) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1

    elif game_winner == O:
        return -1

    return 0


def min_value(board: list[list]):
    if terminal(board):
        return utility(board), None

    val = (INF, None)
    for action in actions(board):
        new_val, _ = max_value(result(board, action))
        if new_val < val[0]:
            val = (new_val, action)

    return val


def max_value(board: list[list]):
    if terminal(board):
        return utility(board), None

    val = (-INF, None)
    for action in actions(board):
        new_val, _ = min_value(result(board, action))
        if new_val > val[0]:
            val = (new_val, action)

    return val


def minimax(board: list[list]):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        _, action = max_value(board)
    else:
        _, action = min_value(board)

    return action
