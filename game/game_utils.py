from typing import NamedTuple


class Spot(NamedTuple):
    row: int
    colum: int


def is_in_board(row, colum):
    return 0 <= row <= 7 and 0 <= colum <= 7


def is_spot_free(board: [[]], row: int, colum: int):
    return is_in_board(row, colum) and board[row][colum] is None


def is_spot_eatable(board: [[]], piece, row: int, colum: int):
    return is_in_board(row, colum) and not is_spot_free(board, row, colum) and board[row][colum].color != piece.color


def is_spot_blocked(board: [[]], piece, row: int, colum: int):
    return is_in_board(row, colum) and not is_spot_free(board, row, colum) and board[row][colum].color == piece.color


def update_turn(turn: str):
    return "b" if turn == "w" else "w"


def is_pick_allowed(board: [[]], row: int, colum: int, turn: str):
    return is_in_board(row, colum) and not is_spot_free(board, row, colum) and board[row][
        colum].color == turn


def print_board(board: [[]]):
    board_printed = ""
    for i in range(8):
        board_printed = board_printed + "["
        for j in range(8):
            if j == 7:
                if not is_spot_free(self.board, i, j):
                    board_printed += board[i][j].piece_let
                else:
                    board_printed += "0"
            else:
                if not is_spot_free(board, i, j):
                    board_printed += board[i][j].piece_let + ", "
                else:
                    board_printed += "0, "
        board_printed = board_printed + "]\n"
    print(board_printed)
