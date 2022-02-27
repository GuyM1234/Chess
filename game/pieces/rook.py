from game.pieces.directionlapiece import DirectionalPiece


class Rook(DirectionalPiece):
    def __init__(self, color: str):
        super().__init__(color, "R", [(1, 0), (-1, 0), (0, 1), (0, -1)])
