from game.pieces.directionlapiece import DirectionalPiece


class Bishop(DirectionalPiece):
    def __init__(self, color: str):
        super().__init__(color, "B", [(1, 1), (1, -1), (-1, 1), (-1, -1)])
