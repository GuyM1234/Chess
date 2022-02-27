from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, color: str, piece_let: str):
        self.color = color
        self.piece_let = piece_let
        self.moved = False

    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples 
    @abstractmethod
    def get_move_options(self, board: [[]], row: int, colum: int):
        pass

    def first_move(self):
        self.moved = True

    # פעולה המחזירה העתק בעל יחוס אחר לאובייקט
    def create_copy(self):
        return type(self)(self.color, self.piece_let)
