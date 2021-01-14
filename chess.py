
import pygame
import sys
import copy
import time
from piece import pawn, king, queen, rook, bishop, knight, empty
from game_board import game_board, copy_game_board
from network import Network
from game import Game
from graphics import graphics_methods
import threading

BLACK = (0,0,0)
WHITE = (255,255,255)
pygame.init()
font1 = pygame.font.SysFont(None ,40)
font2 = pygame.font.SysFont(None ,200)
width = 9 * 100
height = 9 * 100
size = (width,height)
screen = pygame.display.set_mode(size)
graphics = graphics_methods(screen,font2,font1)

def make_play(piece, chosen_spot,board,option_list):
    if piece.piece_let == "K":
        if chosen_spot[1] - piece.spot[1] == 2:
            rook = board.board[piece.spot[0]][7]
            make_play(rook,(piece.spot[0],5),board,[rook.spot])
        elif  piece.spot[1] - chosen_spot[1] == 2:
            rook = board.board[piece.spot[0]][0]
            make_play(rook,(piece.spot[0],3),board,[rook.spot])

    piece.move(chosen_spot, option_list, board)
    graphics.remove_option(option_list, piece.color, board)
    graphics.draw(board.board[piece.spot[0]][piece.spot[1]])

def run_play(piece,board,screen,player,n):
    if player == piece.color:
        piece_options = piece.get_move_options(board)
        option_list = board.get_avalibale_moves(piece,piece_options)
        if len(option_list) > 0:
            graphics.draw_options(option_list)
            chosen_spot = graphics.get_mouse_pos()
            if chosen_spot in option_list:
                turnMade = str(piece.spot) + "," + str(chosen_spot)
                make_play(piece,chosen_spot,board,option_list)
                return turnMade 
            else:
                graphics.remove_option(option_list,piece.color,board)
    return None

def return_status(turn,board):
    if board.is_check(turn):
        if board.is_checkmate(turn):
            return "CHECKMATE"
        else:
            return "CHECK"
    elif board.is_pat(turn):
        return "PAT"
    else:
        return " "

def oppounent_turn(game, board):
    pygame.draw.rect(screen, BLACK, (400, 10, 200, 40)) 
    piece = board.board[game.piece_spot[0]][game.piece_spot[1]]
    make_play(piece,game.chosen_spot,board, [game.chosen_spot])
    graphics.small_message(game.status, WHITE, 400, 10)

def countdown(t,n, posx,posy, stop_cloak):
    while True: 
        graphics.draw_timer(t,posx,posy)
        time.sleep(1)
        t -= 1
        n.send(str(t))
        if stop_cloak():
            break

def get_time(game):
    if game.turn == 'w':
        return game.white_time
    return game.black_time

def main():
    n = Network()
    player = n.getP()
    board = game_board(player)
    graphics.draw_board(board.board)
    graphics.small_message("Player " + player, WHITE, 390, 860)
    
    pygame.display.update()
    game_over = False
    connected = True
    while connected:
        pygame.event.get()
        game = n.get("get")
        if game.ready:
            while not game_over:
                graphics.draw_timer(get_time(game),10,10)
                pygame.event.get()
                game = n.get("get")
                if game.turn == player:
                    if game.piece_spot[0] != None:
                        oppounent_turn(game,board)
                        stop_cloak = False
                        pygame.draw.rect(screen, BLACK, (400, 10, 100, 40))
                        graphics.small_message(game.status,WHITE,400,10)
                        timer = threading.Thread(target=countdown, args=[get_time(game),n,10,860, lambda : stop_cloak,])
                        timer.start()
                        
                    if game.status != "CHECKMATE" and game.status != "PAT":
                        turnMade = None
                        while turnMade == None:
                            chosen_spot = graphics.get_mouse_pos()
                            piece = board.board[chosen_spot[0]][chosen_spot[1]]
                            turnMade = run_play(piece,board,screen,player,n)
                        
                        if game.piece_spot[0] != None:
                            stop_cloak = True
                            timer.join()

                        pygame.draw.rect(screen, BLACK, (400, 10, 100, 40))
                        status = return_status(board.get_oppisite_color(game.turn),board)
                        graphics.small_message(status,WHITE,400,10)
                        n.send(status)
                        n.send(turnMade)
                    else:
                        stop_cloak = True
                        game_over = True
                        connected = False
                    

if __name__ == "__main__":
    main()