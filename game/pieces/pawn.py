from game.game_utils import is_spot_free, is_spot_eatable, Spot
from game.pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "P")
    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples
    def get_move_options(self, board: [], row: int, colum: int):
        options = []
        mult = 1 if self.color == "w" else -1
        if is_spot_free(board, row - (1 * mult), colum):
            options.append(Spot(row - (1 * mult), colum))
            if not self.moved and is_spot_free(board, row - (2 * mult), colum):
                options.append(Spot(row - (2 * mult), colum))

        if is_spot_eatable(board, self, row - (1 * mult), colum - (1 * mult)):
            options.append(Spot(row - (1 * mult), colum - (1 * mult)))

        if is_spot_eatable(board, self, row - (1 * mult), colum + (1 * mult)):
            options.append(Spot(row - (1 * mult), colum + (1 * mult)))

        return options
