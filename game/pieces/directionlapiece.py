from abc import ABC

from game.game_utils import is_in_board, is_spot_free, is_spot_eatable, Spot
from game.pieces.piece import Piece


class DirectionalPiece(Piece, ABC):
    def __init__(self, color: str, piece_let: str, directions: [()]):
        super().__init__(color, piece_let)
        self.directions = directions

    def get_move_option_for_dir(self, board: [[]], row: int, colum: int, row_offset: int, colum_offset: int):
        options = []
        row += row_offset
        colum += colum_offset
        blocked = False
        while is_in_board(row, colum) and not blocked:
            if is_spot_free(board, row, colum) or is_spot_eatable(board, self, row, colum):
                options.append(Spot(row, colum))
            blocked = not is_spot_free(board, row, colum)
            row += row_offset
            colum += colum_offset
        return options

    def get_move_options(self, board: [[]], row: int, colum: int):
        return sum([self.get_move_option_for_dir(board, row, colum, direction[0], direction[1]) for direction in self.directions], [])
