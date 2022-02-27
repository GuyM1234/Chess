from game.game_utils import is_spot_free, is_spot_eatable, Spot
from game.pieces.piece import Piece
# from game.board import Board


class King(Piece):
    def __init__(self, color):
        super().__init__(color, "K")

    # פעולה מחזירה את כל אפשרויות ההזה של כלי ברשימה של tuples
    def get_move_options(self, board: [[]], row: int, colum: int):
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        options = [Spot(row + offset[0], colum + offset[1]) for offset in offsets if
                   is_spot_free(board, row + offset[0], colum + offset[1]) or is_spot_eatable(board, self,
                                                                                              row + offset[0],
                                                                                              colum + offset[1])]
        # if self.can_castle(board, [Spot(row, 5), Spot(row, 6)], Spot(row, 7)):
        #     options.append(Spot(row, 6))
        #
        # if self.can_castle(board, [Spot(row, 3), Spot(row, 2)], Spot(row, 0)):
        #     options.append(Spot(row, 2))

        return options

    def can_castle(self, board, squares_checking, rook_spot):
        if self.moved and board[rook_spot.row][rook_spot.colum].moved:
            return False
        for square in squares_checking:
            if is_spot_free(board, square.row, square.colum):
                return False
        if get_avalibale_moves != len(squares_checking):
            return False
        return True
