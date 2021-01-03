import pygame
import copy
BLACK = (0,0,0)
WHITE = (255,255,255)
SQUARESIZE = 100
from piece import pawn, king, queen, rook, bishop, knight, empty

BlackPawn = pygame.image.load(r'Chesspieces\BlackPawn.png')
WhitePawn = pygame.image.load(r'Chesspieces\WhitePawn.png')
WhiteRook = pygame.image.load(r'Chesspieces\WhiteRook.png')
BlackRook = pygame.image.load(r'Chesspieces\BlackRook.png')
WhiteBishop = pygame.image.load(r'Chesspieces\WhiteBishop.png')
BlackBishop = pygame.image.load(r'Chesspieces\BlackBishop.png')
WhiteKnight = pygame.image.load(r'Chesspieces\WhiteKnight.png')
BlackKnight = pygame.image.load(r'Chesspieces\BlackKnight.png')
WhiteQueen = pygame.image.load(r'Chesspieces\WhiteQueen.png')
BlackQueen = pygame.image.load(r'Chesspieces\BlackQueen.png')
WhiteKing = pygame.image.load(r'Chesspieces\WhiteKing.png')
BlackKing = pygame.image.load(r'Chesspieces\BlackKing.png')

class game_board(object):
    def __init__(self,screen):
        self.white_king_spot = (7, 4)
        self.black_king_spot = (0, 4)
        self.board = self.create_board(screen)
    
    # בונה את הלוח עם כל החלקים
    def create_board(self,screen):
        board = [[empty() for x in range(8)] for i in range(8)]
        board[7][4] = king("w", (7, 4) , WhiteKing, "K")
        board[7][3] = queen("w",(7,3)  , WhiteQueen, "Q")
        board[7][0] = rook("w", (7, 0), WhiteRook, "R")
        board[7][7] = rook("w", (7, 7), WhiteRook, "R")
        board[7][2] = bishop("w", (7, 2), WhiteBishop, "B")
        board[7][5] = bishop("w", (7, 5), WhiteBishop, "B")
        board[7][1] = knight("w" ,(7,1), WhiteKnight, "k")
        board[7][6] = knight("w", (7,6), WhiteKnight, "k")
        for i in range(8):
            board[6][i] = pawn("w",(6,i), WhitePawn, "P")
            board[1][i] = pawn("b",(1,i), BlackPawn, "P")
        board[0][4] = king("b", (0, 4), BlackKing, "K")
        board[0][3] = queen("b",(0,3), BlackQueen, "Q")
        board[0][0] = rook("b", (0, 0), BlackRook, "R")
        board[0][7] = rook("b", (0, 7), BlackRook, "R")
        board[0][2] = bishop("b", (0, 2), BlackBishop, "B") 
        board[0][5] = bishop("b", (0, 5), BlackBishop, "B")
        board[0][1] = knight("b",(0,1), BlackKnight, "k")
        board[0][6] = knight("b",(0,6), BlackKnight, "k")

        for i in range(8):
            board[0][i].draw(screen)
            board[1][i].draw(screen)
            board[6][i].draw(screen)
            board[7][i].draw(screen)
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
   
    # פעולה המסירה את הנקודות של האפשרויות על המסך
    def remove_option(self, screen, option_list, color, board):
        for option in option_list:
            xpos = option[1] * SQUARESIZE + 70
            ypos = option[0] * SQUARESIZE + 65
            self.clearSquare(xpos - 20,ypos - 15,screen)
            piece_on_option = self.board[option[0]][option[1]]
            if piece_on_option.color != "e" and color != piece_on_option.color:
                piece_on_option.draw(screen)
        pygame.display.update()
    
    # פעולה המנקה את הקובייה
    def clearSquare(self, xpos, ypos, screen):
        color = screen.get_at((xpos,ypos))
        pygame.draw.rect(screen, color, (xpos, ypos, 100, 100))

    # בודק האם המלך שלך בשח
    def is_check(self, color):
        for row in self.board:
            for piece in row:              
                option_list = piece.get_move_options(self.board)
                if "w" == color:
                    if self.white_king_spot in option_list:
                        return True
                else:
                    if self.black_king_spot in option_list:
                        return True
        return False

    # עולה המחזירה את אפשרויות התזוזה אם לא יצרו שח
    def get_avalibale_moves(self, piece, option_list):
        i = 0
        while i < len(option_list):
            option = option_list[i]
            copy_board = copy_game_board(self)
            empty = []
            copy_board.board[piece.spot[0]][piece.spot[1]].move(option, empty, copy_board)
            if copy_board.is_check(piece.color):
                option_list.remove(option)
                i =-1
            i+=1
        return option_list
    
    # פעולה המחזירה האם המלך שלך בשח
    def is_checkmate(self,turn):
        for row in self.board:
            for piece in row:
                if piece.color == turn:
                    option_list = self.get_avalibale_moves(piece, piece.get_move_options(self.board))
                    if len(option_list) > 0:
                        return False
        return True

    def turn_pawn(self,piece):
        if str(type(piece)) == "pawn":
            if piece.spot[1] == 0 or piece.spot[1] == 7:
                self.board[piece.spot[0]][piece.spot] == queen(piece.color,piece.spot,BlackQueen,"Q")
            
class copy_game_board(game_board):
    def __init__(self,board):
        self.white_king_spot = board.white_king_spot
        self.black_king_spot = board.black_king_spot
        self.board = self.create_board(board)

    def create_board(self,board):
        copy_board = []
        for i in range(8):
            row = []
            for j in range(8):
                piece = board.board[i][j].create_copy()
                row.append(piece)
            copy_board.append(row)
        return copy_board
