from game.game_utils import is_spot_free, Spot, is_pick_allowed
from game.pieces.bishop import Bishop
from game.pieces.king import King
from game.pieces.knight import Knight
from game.pieces.pawn import Pawn
from game.pieces.queen import Queen
from game.pieces.rook import Rook
from game.pieces.piece import Piece
import copy
import numpy as np


class Board:
    @staticmethod
    def create_board(white_row=7, black_row=0):
        board = np.empty((8, 8), dtype=Piece)
        board[white_row][4] = King("w")
        board[white_row][3] = Queen("w")
        board[white_row][0] = Rook("w")
        board[white_row][7] = Rook("w")
        board[white_row][2] = Bishop("w")
        board[white_row][5] = Bishop("w")
        board[white_row][1] = Knight("w")
        board[white_row][6] = Knight("w")
        for i in range(8):
            board[6][i] = Pawn("w")
            board[1][i] = Pawn("b")
        board[black_row][4] = King("b")
        board[black_row][3] = Queen("b")
        board[black_row][0] = Rook("b")
        board[black_row][7] = Rook("b")
        board[black_row][2] = Bishop("b")
        board[black_row][5] = Bishop("b")
        board[black_row][1] = Knight("b")
        board[black_row][6] = Knight("b")
        return board

    @staticmethod
    def move(board: [[Piece]], move_from: Spot, move_to: Spot):
        board[move_to.row][move_to.colum] = copy.deepcopy(board[move_from.row][move_from.colum])
        board[move_from.row][move_from.colum] = None
        return board

    @staticmethod
    def move_side_effect(board: [[Piece]], move: Spot):
        board[move.row][move.colum].moved = True
        board = Board.turn_to_queen(board, move.row, move.colum)
        return board

    @staticmethod
    def revert_move(board: [[Piece]], piece: Piece, move_from: Spot, move_to: Spot):
        board[move_to.row][move_to.colum] = board[move_from.row][move_from.colum]
        board[move_from.row][move_from.colum] = piece
        return board

    @staticmethod
    def get_move_options(board: [[Piece]], move_from: Spot, turn: str):
        piece = board[move_from.row][move_from.colum]
        return Board.get_available_moves(board, move_from, piece.get_move_options(board, move_from.row, move_from.colum), turn) \
            if is_pick_allowed(board, move_from.row, move_from.colum, turn) else []

    @staticmethod
    def get_available_moves(board: [[Piece]], move_from: Spot, options: [Spot], turn):
        new_options = []
        for option in options:
            piece_on_option = board[option.row][option.colum]
            board = Board.move(board, move_from, option)
            if not Board.is_check(board, turn):
                new_options.append(option)
            Board.revert_move(board, piece_on_option, option, move_from)
        return new_options

    @staticmethod
    def turn_to_queen(board: [[Piece]], row: int, colum: int):
        if isinstance(board[row][colum], Pawn) and not (0 < row < 7):
            board[row][colum] = Queen(board[row][colum].color)
        return board

    @staticmethod
    def is_check(board: [[Piece]], turn):
        for row in range(8):
            for colum in range(8):
                if not is_spot_free(board, row, colum):
                    for option in board[row][colum].get_move_options(board, row, colum):
                        if Board.is_spot_king(board, option, turn):
                            return True
        return False

    @staticmethod
    def is_checkmate(board: [[Piece]], turn: str):
        for row in range(8):
            for colum in range(8):
                if len(Board.get_move_options(board, Spot(row, colum), turn)) > 0:
                    return False
        return True

    @staticmethod
    def is_pat(board: [[Piece]], turn: str):
        return Board.is_checkmate(board, turn)

    @staticmethod
    def status(board: [[Piece]], turn: str):
        if Board.is_check(board, turn):
            return "Checkmate" if Board.is_checkmate(board, turn) else "Check"
        else:
            return "Pat" if Board.is_pat(board, turn) else ""

    @staticmethod
    def is_spot_king(board: [[Piece]], spot: Spot, turn):
        return isinstance(board[spot.row][spot.colum], King) and board[spot.row][
            spot.colum].color == turn
