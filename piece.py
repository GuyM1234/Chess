import pygame
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
SQUARESIZE = 100
last_piece_eaten = []

class piece(object):
    offset_x = 0
    offset_y = 0
    def __init__(self, color, spot, piece_pic, piece_let):
        self.spot = spot
        self.color = color
        self.piece_pic = piece_pic
        self.piece_let = piece_let
    
    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples 
    def get_move_options(self, board):
        pass
    # פעולה המזיזה את החייל על הלוח ואת עצמו (התכונת מקום שלו)
    def move(self, chosen_spot, option_list, board):
        option_list.append((self.spot)) 
        board.update_board(chosen_spot,self)   
        self.spot = chosen_spot
    
    #  פעולה המחזירה העתק בעל יחוס אחר לאובייקט
    def create_copy(self):
        return type(self)(self.color, self.spot,self.piece_pic,self.piece_let)
    
    # פעולה לצייר על המסך את הכלי
    def draw(self,screen):
        screen.blit(self.piece_pic, ((self.spot[1])* SQUARESIZE + 70 + self.offset_x, (self.spot[0]) * SQUARESIZE + 65 + self.offset_y))
        pygame.display.update()

class pawn(piece):
    offset_x = 5
    offset_y = 0
    def get_move_options(self, board):
        rowpos = self.spot[0]
        columnpos = self.spot[1]
        option_list = []
        if self.color == "b" and rowpos < 7:
            if board[rowpos + 1][columnpos].color == "e":
                option_list.append((rowpos + 1, columnpos))
                if rowpos == 1 and board[rowpos + 2][columnpos].color == "e":
                    option_list.append((rowpos + 2, columnpos))

            if columnpos != 7:
                if board[rowpos + 1][columnpos + 1].color == "w":
                    option_list.append((rowpos + 1, columnpos + 1))

            if columnpos != 0:
                if board[rowpos + 1][columnpos - 1].color == "w":
                    option_list.append((rowpos + 1, columnpos - 1))
        elif rowpos > 0:
            if board[rowpos - 1][columnpos].color == "e":
                option_list.append((rowpos - 1, columnpos))
                if rowpos == 6 and board[rowpos - 2][columnpos].color == "e":
                    option_list.append((rowpos - 2, columnpos))

            if columnpos != 0:
                if board[rowpos - 1][columnpos - 1].color == "b":
                    option_list.append((rowpos - 1, columnpos - 1))

            if columnpos != 7:
                if board[rowpos - 1][columnpos + 1] != 0:
                    if board[rowpos - 1][columnpos + 1].color == "b":
                        option_list.append((rowpos - 1, columnpos + 1))
        return option_list

class rook(piece):
    offset_x = 0
    offset_y = 0
    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples  
    def get_move_options(self, board):
        option_list = get_horizontal_options(self.spot, self.color, board)
        return option_list
 
class bishop(piece):
    offset_x = 0
    offset_y = 0
    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples 
    def get_move_options(self, board):
        option_list = get_diaganol_options(self.spot, self.color, board)
        return option_list

class queen(piece):
    offset_x = - 2
    offset_y = + 3
    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples 
    def get_move_options(self, board):
        option_list = get_diaganol_options(self.spot, self.color, board)
        option_list.extend(get_horizontal_options(self.spot, self.color, board))
        return option_list

class king(piece):
    offset_x = - 2
    offset_y = + 3
    # פעולה מחזירה את כל אפשרויות ההזה של כלי ברשימה של tuples 
    def get_move_options(self, board):
        rowpos = self.spot[0]
        columnpos = self.spot[1]
        option_list = []
        if rowpos < 7:
            if board[rowpos + 1][columnpos].color != self.color:
                option_list.append((rowpos + 1, columnpos))
        
        if rowpos > 0:
            if board[rowpos  - 1][columnpos].color != self.color:
                option_list.append((rowpos - 1, columnpos))

        if columnpos < 7:
            if board[rowpos][columnpos + 1].color != self.color:
                option_list.append((rowpos, columnpos + 1))

        if columnpos > 0:
            if board[rowpos][columnpos - 1].color != self.color:
                option_list.append((rowpos, columnpos - 1))

        if rowpos < 7 and columnpos < 7:
            if board[rowpos + 1][columnpos + 1].color != self.color:
                option_list.append((rowpos + 1, columnpos + 1))

        if rowpos < 7 and columnpos > 0:
            if board[rowpos + 1][columnpos - 1].color != self.color:
                option_list.append((rowpos + 1, columnpos - 1))

        if rowpos > 0 and columnpos > 0:
            if board[rowpos - 1][columnpos - 1].color != self.color:
                option_list.append((rowpos - 1, columnpos - 1))

        if rowpos > 0 and columnpos < 7:
            if board[rowpos - 1][columnpos + 1].color != self.color:
                option_list.append((rowpos - 1, columnpos + 1))
        
        return option_list

class knight(piece):
    offset_x = 0
    offset_y = 0
    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples 
    def get_move_options(self, board):
        rowpos = self.spot[0]
        columnpos = self.spot[1]
        option_list = []
        if rowpos < 6 and columnpos < 7:
            if board[rowpos + 2][columnpos + 1].color != self.color:
                option_list.append((rowpos + 2, columnpos + 1))
                

        if rowpos < 6 and columnpos > 0:
            if board[rowpos + 2][columnpos - 1].color != self.color:
                option_list.append((rowpos + 2, columnpos - 1))
        
        if rowpos < 7 and columnpos < 6:
            if board[rowpos + 1][columnpos + 2].color != self.color:
                option_list.append((rowpos + 1, columnpos + 2))
        
        if rowpos < 7 and columnpos > 1:
            if board[rowpos + 1][columnpos - 2].color != self.color:
                option_list.append((rowpos + 1, columnpos - 2))
            
        if rowpos > 1 and columnpos < 7:
            if board[rowpos - 2][columnpos + 1].color != self.color:
                option_list.append((rowpos - 2, columnpos + 1))

        if rowpos > 1 and columnpos > 0:
            if board[rowpos - 2][columnpos - 1].color != self.color:
                option_list.append((rowpos - 2, columnpos - 1))

        if rowpos > 0 and columnpos > 1:
            if board[rowpos - 1][columnpos - 2].color != self.color:
                option_list.append((rowpos - 1, columnpos - 2))
        
        if rowpos > 0 and columnpos < 6:
            if board[rowpos - 1][columnpos + 2].color != self.color:
                option_list.append((rowpos - 1, columnpos + 2))
        return option_list

# אובייקט ריק שיופיע במקומות בלוח שבהן אין כלי בשביל לחסוך בדיקות האם המקום ריק
class empty():
    def __init__(self):
        self.color = "e"
        self.piece_let = "0"

    def create_copy(self):
        return empty()

# פעולה מחזירה את כל אפשרויות הזזה של נקודה באלכסון ברשימה של tuples 
def get_diaganol_options(spot, color, board):
    rowpos = spot[0]
    columnpos = spot[1]
    option_list = []
    blocked = False
    while not blocked and rowpos < 7 and columnpos < 7:
        if board[rowpos + 1][columnpos + 1].color != "e":
            if board[rowpos + 1][columnpos + 1].color != color:
                option_list.append((rowpos + 1, columnpos + 1))
                blocked = True
            else:
                blocked = True
        else:
            option_list.append((rowpos + 1, columnpos + 1))
        columnpos += 1
        rowpos += 1

    blocked = False
    rowpos = spot[0]
    columnpos = spot[1]
    while not blocked and columnpos < 7 and rowpos > 0:
        if board[rowpos - 1][columnpos + 1].color != "e":
            if board[rowpos - 1][columnpos + 1].color != color:
                option_list.append((rowpos - 1, columnpos + 1))
                blocked = True
            else:
                blocked = True
        else:
            option_list.append((rowpos - 1, columnpos + 1))
        columnpos += 1
        rowpos = rowpos - 1

    blocked = False
    rowpos = spot[0]
    columnpos = spot[1]
    while not blocked and rowpos > 0 and columnpos > 0:
        if board[rowpos - 1][columnpos - 1].color != "e":
            if board[rowpos  - 1][columnpos - 1].color != color:
                option_list.append((rowpos  - 1, columnpos - 1))
                blocked = True
            else:
                blocked = True
        else:
            option_list.append((rowpos - 1, columnpos - 1))
        rowpos = rowpos - 1
        columnpos = columnpos - 1

    blocked = False
    rowpos = spot[0]
    columnpos = spot[1]
    while not blocked and columnpos > 0 and rowpos < 7:
        if board[rowpos + 1][columnpos - 1].color != "e":
            if board[rowpos + 1][columnpos - 1].color != color:
                option_list.append((rowpos + 1, columnpos - 1))
                blocked = True
            else:
                blocked = True
        else:
            option_list.append((rowpos + 1, columnpos - 1))
        columnpos = columnpos - 1
        rowpos += 1
    return option_list

# פעולה מחזירה את כל אפשרויות הזזה של נקודה בישר ברשימה של tuples 
def get_horizontal_options(spot, color, board):
    option_list = []
    blocked = False
    rowpos = spot[0]
    columnpos = spot[1]
    while not blocked and rowpos < 7:
        if board[rowpos + 1][columnpos].color != "e":
            if board[rowpos + 1][columnpos].color != color:
                option_list.append((rowpos + 1, columnpos))
                blocked = True
            else:
                blocked = True
        else:
            option_list.append((rowpos + 1, columnpos))
        rowpos += 1

    blocked = False
    rowpos = spot[0]
    while not blocked and columnpos < 7:
        if board[rowpos][columnpos + 1].color != "e":
            if board[rowpos][columnpos + 1].color != color:
                option_list.append((rowpos, columnpos + 1))
                blocked = True
            else:
                blocked = True
        else:
            option_list.append((rowpos, columnpos + 1))
        columnpos += 1
        
    blocked = False
    columnpos = spot[1]
    while not blocked and rowpos > 0:
        if board[rowpos - 1][columnpos].color != "e":
            if board[rowpos  - 1][columnpos].color != color:
                option_list.append((rowpos  - 1, columnpos))
                blocked = True
            else:
                blocked = True
        else:
            option_list.append((rowpos - 1, columnpos))
        rowpos = rowpos - 1

    blocked = False
    rowpos = spot[0]
    while not blocked and columnpos > 0:
        if board[rowpos][columnpos - 1].color != "e":
            if board[rowpos][columnpos - 1].color != color:
                option_list.append((rowpos, columnpos - 1))
                blocked = True
            else:
                blocked = True
        else:
            option_list.append((rowpos, columnpos - 1))
        columnpos = columnpos - 1
    return option_list