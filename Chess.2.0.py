
import pygame
import sys
import copy
from piece import pawn, king, queen, rook, bishop, knight, empty
from game_board import game_board, copy_game_board


color1 = (205,89,22)
color2 = (250,255,204)
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
SQUARESIZE = 100
WhiteQueen = pygame.image.load(r'Chesspieces\WhiteQueen.png')
BlackQueen = pygame.image.load(r'Chesspieces\BlackQueen.png')

def update_turn(turn):
    if turn == "w":
        return "b"
    else:
        return "w"

def draw_board(screen):
    count = 1
    count1 = 1
    for r in range(8):
        for c in range(8):
            if (count1 % 2 == 0):               
                if count == 1:
                    pygame.draw.rect(screen, color1, (c*SQUARESIZE + 50, r*SQUARESIZE + 50, SQUARESIZE, SQUARESIZE))
                    count = 2
                else:
                    pygame.draw.rect(screen, color2, (c*SQUARESIZE + 50, r*SQUARESIZE + 50, SQUARESIZE, SQUARESIZE))
                    count = 1
            else:
                if count == 1:
                    pygame.draw.rect(screen, color2, (c*SQUARESIZE + 50, r*SQUARESIZE + 50, SQUARESIZE, SQUARESIZE))
                    count = 2
                else:
                    pygame.draw.rect(screen, color1, (c*SQUARESIZE + 50, r*SQUARESIZE + 50, SQUARESIZE, SQUARESIZE))
                    count = 1
        count1 +=1

def get_mouse_pos():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                chosen_xpos = event.pos[0]
                chosen_ypos = event.pos[1]
                column_pos = (chosen_xpos - 50) // 100
                row_pos = (chosen_ypos - 50) // 100
                chosen_spot = ((row_pos,column_pos))
                return chosen_spot
                
def message_to_screen(msg, color,font, screen, xpos, ypos):
    message = font.render(msg, True, color)
    screen.blit(message, [xpos, ypos])
    pygame.display.update()

def draw_options(option_list, screen):
    for i in option_list:
        pygame.draw.circle(screen, BLUE, ((i[1] + 1) * SQUARESIZE, (i[0] + 1) * SQUARESIZE), 8)
        pygame.display.update()

def run_play(piece,board,screen,turn):
    if turn == piece.color:
        piece_options = piece.get_move_options(board.board)
        option_list = board.get_avalibale_moves(piece,piece_options)
        if len(option_list) > 0:
            draw_options(option_list,screen)
            chosen_spot = get_mouse_pos()
            if chosen_spot in option_list:
                turn = update_turn(turn)
                piece.move(chosen_spot, option_list, board)

                board.remove_option(screen, option_list,piece.color,board)
                row = piece.spot[0]
                column = piece.spot[1]
                board.board[row][column].draw(screen)
            else:
                board.remove_option(screen, option_list,piece.color,board)
    return turn

def draw_castels(screen, font):
    pygame.draw.rect(screen,WHITE,(50, 5, 135, 40))
    pygame.draw.rect(screen,BLACK,(55, 10, 125, 30))     
    message_to_screen("CASTLE",WHITE, font, screen, 60, 10)
    
    pygame.draw.rect(screen, WHITE, (715, 5, 135, 40))
    pygame.draw.rect(screen, BLACK, (720, 10, 125, 30))     
    message_to_screen("CASTLE", WHITE, font, screen, 725, 10)

    pygame.draw.rect(screen, WHITE, (715, 855, 135, 40))
    pygame.draw.rect(screen, BLACK, (720, 860, 125, 30))     
    message_to_screen("CASTLE", WHITE, font, screen, 725, 860)

    pygame.draw.rect(screen,WHITE,(50, 855, 135, 40))
    pygame.draw.rect(screen,BLACK,(55, 860, 125, 30))     
    message_to_screen("CASTLE",WHITE, font, screen, 60, 860)

def main():
    pygame.init()
    font = pygame.font.SysFont(None ,40)
    width = 9 * SQUARESIZE
    height = 9 * SQUARESIZE
    size = (width,height)
    screen = pygame.display.set_mode(size)
    draw_board(screen)
    draw_castels(screen,font)
    board = game_board(screen)
    pygame.display.update()
    checkmate = False    
    turn = "w"
    while not checkmate:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                chosen_xpos = event.pos[0]
                chosen_ypos = event.pos[1]
                column_pos = (chosen_xpos - 50) // 100
                row_pos = (chosen_ypos - 50) // 100
                if row_pos > - 1 and row_pos < 8 and column_pos > - 1 and column_pos < 8:
                    piece = board.board[row_pos][column_pos]
                    turn = run_play(piece,board,screen,turn)              
                
                if board.is_check(turn):
                    if board.is_checkmate(turn):
                        message_to_screen("CHECKMATE",WHITE,font,screen,400,10)
                        pygame.time.wait(10000)
                        checkmate = True
                    else:
                        message_to_screen("CHECK",WHITE,font,screen,400,10)
                elif board.is_pat(turn):
                    message_to_screen("PAT",WHITE,font,screen,400,10)
                    pygame.time.wait(10000)
                    checkmate = True
                pygame.display.update()

main()