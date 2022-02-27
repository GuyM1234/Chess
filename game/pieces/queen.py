from game.pieces.directionlapiece import DirectionalPiece


class Queen(DirectionalPiece):

    def __init__(self, color: str):
        super().__init__(color, "Q", [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)])
