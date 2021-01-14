import pygame
WhiteQueen = pygame.image.load(r'Chesspieces\WhiteQueen.png')
BlackQueen = pygame.image.load(r'Chesspieces\BlackQueen.png')

class piece(object):
    offset_x = 0
    offset_y = 0
    def __init__(self, color, spot, piece_pic, piece_let):
        self.spot = spot
        self.color = color
        self.piece_pic = piece_pic
        self.piece_let = piece_let
        self.moved = False
    
    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples 
    def get_move_options(self, board):
        option_list = []
        return option_list

    # פעולה המזיזה את החייל על הלוח ואת עצמו (התכונת מקום שלו)
    def move(self, chosen_spot, option_list, board):
        option_list.append((self.spot))
        board.update(chosen_spot,self)   
        self.spot = chosen_spot
        if not self.moved:
            self.moved = True
    
    # פעולה המחזירה העתק בעל יחוס אחר לאובייקט
    def create_copy(self):
        return type(self)(self.color, self.spot,self.piece_pic,self.piece_let)
    
class pawn(piece):
    offset_x = 5
    offset_y = 0
    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples 
    def get_move_options(self, game_board):
        board = game_board.board
        rowpos = self.spot[0]
        columnpos = self.spot[1]
        option_list = []
        if rowpos > 0:
            if board[rowpos - 1][columnpos].color == "e":
                option_list.append((rowpos - 1, columnpos))
                if rowpos == 6 and board[rowpos - 2][columnpos].color == "e":
                    option_list.append((rowpos - 2, columnpos))

            if columnpos != 0:
                if board[rowpos - 1][columnpos - 1].color != self.color and board[rowpos - 1][columnpos - 1].color != 'e':
                    option_list.append((rowpos - 1, columnpos - 1))

            if columnpos != 7:
                if board[rowpos - 1][columnpos + 1].color != self.color and board[rowpos - 1][columnpos + 1].color != 'e':
                    option_list.append((rowpos - 1, columnpos + 1))
        return option_list

    def move(self, chosen_spot, option_list, board):
        super().move(chosen_spot, option_list, board)
        if self.spot[0] == 0 or self.spot[0] == 7:
            if self.color == "w":
                board.board[self.spot[0]][self.spot[1]] = queen(self.color, self.spot, WhiteQueen, "Q")
            else:
                board.board[self.spot[0]][self.spot[1]] = queen(self.color, self.spot, BlackQueen, "Q")

class rook(piece):
    offset_x = 0
    offset_y = 0
    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples  
    def get_move_options(self, game_board):
        board = game_board.board
        option_list = []
        blocked = False
        rowpos = self.spot[0]
        columnpos = self.spot[1]
        while not blocked and rowpos < 7:
            if board[rowpos + 1][columnpos].color != "e":
                if board[rowpos + 1][columnpos].color != self.color:
                    option_list.append((rowpos + 1, columnpos))
                    blocked = True
                else:
                    blocked = True
            else:
                option_list.append((rowpos + 1, columnpos))
            rowpos += 1

        blocked = False
        rowpos = self.spot[0]
        while not blocked and columnpos < 7:
            if board[rowpos][columnpos + 1].color != "e":
                if board[rowpos][columnpos + 1].color != self.color:
                    option_list.append((rowpos, columnpos + 1))
                    blocked = True
                else:
                    blocked = True
            else:
                option_list.append((rowpos, columnpos + 1))
            columnpos += 1
            
        blocked = False
        columnpos = self.spot[1]
        while not blocked and rowpos > 0:
            if board[rowpos - 1][columnpos].color != "e":
                if board[rowpos  - 1][columnpos].color != self.color:
                    option_list.append((rowpos  - 1, columnpos))
                    blocked = True
                else:
                    blocked = True
            else:
                option_list.append((rowpos - 1, columnpos))
            rowpos = rowpos - 1

        blocked = False
        rowpos = self.spot[0]
        while not blocked and columnpos > 0:
            if board[rowpos][columnpos - 1].color != "e":
                if board[rowpos][columnpos - 1].color != self.color:
                    option_list.append((rowpos, columnpos - 1))
                    blocked = True
                else:
                    blocked = True
            else:
                option_list.append((rowpos, columnpos - 1))
            columnpos = columnpos - 1
        return option_list
 
class bishop(piece):
    offset_x = 0
    offset_y = 0
    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples 
    def get_move_options(self, game_board):
        board = game_board.board
        rowpos = self.spot[0]
        columnpos = self.spot[1]
        option_list = []
        blocked = False
        while not blocked and rowpos < 7 and columnpos < 7:
            if board[rowpos + 1][columnpos + 1].color != "e":
                if board[rowpos + 1][columnpos + 1].color != self.color:
                    option_list.append((rowpos + 1, columnpos + 1))
                    blocked = True
                else:
                    blocked = True
            else:
                option_list.append((rowpos + 1, columnpos + 1))
            columnpos += 1
            rowpos += 1

        blocked = False
        rowpos = self.spot[0]
        columnpos = self.spot[1]
        while not blocked and columnpos < 7 and rowpos > 0:
            if board[rowpos - 1][columnpos + 1].color != "e":
                if board[rowpos - 1][columnpos + 1].color != self.color:
                    option_list.append((rowpos - 1, columnpos + 1))
                    blocked = True
                else:
                    blocked = True
            else:
                option_list.append((rowpos - 1, columnpos + 1))
            columnpos += 1
            rowpos = rowpos - 1

        blocked = False
        rowpos = self.spot[0]
        columnpos = self.spot[1]
        while not blocked and rowpos > 0 and columnpos > 0:
            if board[rowpos - 1][columnpos - 1].color != "e":
                if board[rowpos  - 1][columnpos - 1].color != self.color:
                    option_list.append((rowpos  - 1, columnpos - 1))
                    blocked = True
                else:
                    blocked = True
            else:
                option_list.append((rowpos - 1, columnpos - 1))
            rowpos = rowpos - 1
            columnpos = columnpos - 1

        blocked = False
        rowpos = self.spot[0]
        columnpos = self.spot[1]
        while not blocked and columnpos > 0 and rowpos < 7:
            if board[rowpos + 1][columnpos - 1].color != "e":
                if board[rowpos + 1][columnpos - 1].color != self.color:
                    option_list.append((rowpos + 1, columnpos - 1))
                    blocked = True
                else:
                    blocked = True
            else:
                option_list.append((rowpos + 1, columnpos - 1))
            columnpos = columnpos - 1
            rowpos += 1
        return option_list

class queen(bishop,rook):
    offset_x = - 2
    offset_y = + 3
    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples 
    def get_move_options(self, game_board):
        option_list = bishop.get_move_options(self,game_board)
        option_list.extend(rook.get_move_options(self,game_board))
        return option_list

class king(piece):
    offset_x = - 2
    offset_y = + 3
        
    # פעולה מחזירה את כל אפשרויות ההזה של כלי ברשימה של tuples 
    def get_move_options(self, game_board):
        board = game_board.board
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
        
        if self.castle(game_board,[(self.spot[0],3),(self.spot[0],2),(self.spot[0],1)], game_board.board[self.spot[0]][0]):
            option_list.append((self.spot[0],2))
        
        if self.castle(game_board,[(self.spot[0],5),(self.spot[0],6)], game_board.board[self.spot[0]][7]):
            option_list.append((self.spot[0],6))

        return option_list


    def castle(self,board,squares_checkinng, rook):
        prevlength = len(squares_checkinng)
        if not self.moved and not rook.moved:
            for square in squares_checkinng:
                if board.board[square[0]][square[1]].color != "e":
                    return False
        else:
            return False
        squares_checkinng = board.get_avalibale_moves(self,squares_checkinng)
        if len(squares_checkinng) == prevlength:
            return True
        return False

class knight(piece):
    offset_x = 0
    offset_y = 0
    # פעולה מחזירה את כל אפשרויות הזזה של כלי ברשימה של tuples 
    def get_move_options(self, game_board):
        board = game_board.board
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
class empty(piece):
    def __init__(self):
        self.color = "e"
        self.piece_let = "0"
        self.moved = True

    def create_copy(self):
        return empty()

