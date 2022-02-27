from game.game_utils import is_spot_free, is_spot_eatable, Spot
from game.pieces.piece import Piece


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "k")
    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples

    def get_move_options(self, board: [[]], row: int, colum: int):
        offsets = [(2, 1), (2, -1), (1, 2), (1, -2), (-2, 1), (-2, -1), (-1, 2), (-1, -2)]
        return [Spot(row + offset[0], colum + offset[1]) for offset in offsets if
                is_spot_free(board, row + offset[0], colum + offset[1]) or is_spot_eatable(board, self, row + offset[0], colum + offset[1])]
