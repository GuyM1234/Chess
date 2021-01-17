import pygame
import copy
from piece import pawn, king, queen, rook, bishop, knight, empty


class game_board(object):
    def __init__(self,color):
        if color =='w':
            self.white_king = king("w", (7, 4) , "K")
            self.black_king = king("b", (0, 4), "K")
            self.board = self.create_white_board()
        else:
            self.white_king = king("w", (0, 4) , "K")
            self.black_king = king("b", (7, 4), "K")
            self.board = self.create_black_board()     
    
    # בונה את הלוח עם כל החלקים
    def create_white_board(self):
        board = [[empty() for x in range(8)] for i in range(8)]
        board[7][4] = self.white_king
        board[7][3] = queen("w",(7,3), "Q")
        board[7][0] = rook("w", (7, 0), "R")
        board[7][7] = rook("w", (7, 7), "R")
        board[7][2] = bishop("w", (7, 2), "B")
        board[7][5] = bishop("w", (7, 5), "B")
        board[7][1] = knight("w" ,(7,1), "k")
        board[7][6] = knight("w", (7,6), "k")
        for i in range(8):
            board[6][i] = pawn("w",(6,i), "P")
            board[1][i] = pawn("b",(1,i), "P")
        board[0][4] = self.black_king
        board[0][3] = queen("b",(0,3), "Q")
        board[0][0] = rook("b", (0, 0), "R")
        board[0][7] = rook("b", (0, 7), "R")
        board[0][2] = bishop("b", (0, 2), "B") 
        board[0][5] = bishop("b", (0, 5), "B")
        board[0][1] = knight("b",(0,1), "k")
        board[0][6] = knight("b",(0,6), "k")
        return board
    
    # 
    def create_black_board(self):
        board = [[empty() for x in range(8)] for i in range(8)]
        board[0][4] = self.white_king
        board[0][3] = queen("w",(0,3), "Q")
        board[0][0] = rook("w", (0, 0), "R")
        board[0][7] = rook("w", (0, 7), "R")
        board[0][2] = bishop("w", (0, 2), "B")
        board[0][5] = bishop("w", (0, 5), "B")
        board[0][1] = knight("w" ,(0,1), "k")
        board[0][6] = knight("w", (0,6), "k")
        for i in range(8):
            board[1][i] = pawn("w",(1,i), "P")
            board[6][i] = pawn("b",(6,i), "P")
        board[7][4] = self.black_king
        board[7][3] = queen("b",(7,3), "Q")
        board[7][0] = rook("b", (7, 0), "R")
        board[7][7] = rook("b", (7, 7), "R")
        board[7][2] = bishop("b", (7, 2), "B") 
        board[7][5] = bishop("b", (7, 5), "B")
        board[7][1] = knight("b",(7,1), "k")
        board[7][6] = knight("b",(7,6), "k")
        return board
        
    # פעולת עזר להדפסת הלוח
    def print_board(self):
        board_printed = ""
        for i in range(8):
            board_printed = board_printed + "["
            for j in range(8):
                if j==7:
                    board_printed = board_printed + self.board[i][j].piece_let
                else:
                    board_printed = board_printed + self.board[i][j].piece_let +", "
            board_printed = board_printed + "]\n"
        print(board_printed)
   
    # פעולה מעדכנת את הלוח
    def update(self,chosen_spot,piece):
        self.board[chosen_spot[0]][chosen_spot[1]] = piece
        self.board[piece.spot[0]][piece.spot[1]] = empty()
   
    # בודק האם המלך שלך בשח
    def is_check(self, turn):
        for row in self.board:
            for piece in row:              
                option_list = piece.get_move_options(self)
                if "w" == turn:
                    if self.white_king.spot in option_list:
                        return True
                else:
                    if self.black_king.spot in option_list:
                        return True
        return False

    # עולה המחזירה את אפשרויות התזוזה אם לא יצרו שח
    def get_avalibale_moves(self, piece, option_list):
        i = 0
        while i < len(option_list):
            option = option_list[i]
            copy_board = copy_game_board(self)
            piece_moving = copy_board.board[piece.spot[0]][piece.spot[1]]
            piece_moving.move(option, [], copy_board) #מעדכן את הלוח המועתק בשביל לבדוק האם יש שח אחרי מהלך
            if copy_board.is_check(piece.color):
                option_list.remove(option)
                i =-1
            i+=1
        return option_list
    
    # פעולה המחזירה האם שחמט
    def is_checkmate(self,turn):
        for row in self.board:
            for piece in row:
                if piece.color == turn:
                    option_list = self.get_avalibale_moves(piece, piece.get_move_options(self))
                    if len(option_list) > 0:
                        return False
        return True
    
    # האם פט
    def is_pat(self,turn):
        return self.is_checkmate(turn) 

    # 
    def get_oppisite_color(self, color):
        if color == 'w':
            return 'b'
        else:
            return 'w'

class copy_game_board(game_board):
    def __init__(self,board):
        self.board = self.create_board(board)
        self.white_king = self.board[board.white_king.spot[0]][board.white_king.spot[1]]
        self.black_king = self.board[board.black_king.spot[0]][board.black_king.spot[1]]

    def create_board(self,board):
        copy_board = []
        for i in range(8):
            row = []
            for j in range(8):
                piece = board.board[i][j].create_copy()
                row.append(piece)
            copy_board.append(row)
        return copy_board