import subprocess
import sys
import pip

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    print("[GAME] Trying to import pygame")
    import pygame
except:
    print("[EXCEPTION] Pygame not installed")

    try:
        print("[GAME] Trying to install pygame via pip")
        import pip
        install("pygame")
        print("[GAME] Pygame has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[GAME] Trying to install pip")
        get_pip.main()
        print("[GAME] Pip has been installed")
        try:
            print("[GAME] Trying to install pygame")
            import pip
            install("pygame")
            print("[GAME] Pygame has been installed")
        except:
            print("[ERROR 1] Pygame could not be installed")

import time
from piece import pawn, king, queen, rook, bishop, knight, empty
from game_board import game_board, copy_game_board
from network import Network
from game import Game, game_data
from graphics import graphics_methods
import threading

squaresize = int(input("Enter Square Size "))

BLACK = (0,0,0)
WHITE = (255,255,255)
pygame.init()
font1 = pygame.font.SysFont(None ,squaresize//2 - 10)
font2 = pygame.font.SysFont(None ,200)
width = 9 * squaresize
height = 9 * squaresize
size = (width,height)
screen = pygame.display.set_mode(size)
graphics = graphics_methods(screen,font2,font1,squaresize)

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
                turnMade = (piece.spot,chosen_spot)
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
    graphics.cover_text(graphics.squaresize * 4, 0, graphics.squaresize * 3, graphics.border)
    graphics.small_message(game.status, WHITE, graphics.squaresize * 4, graphics.squaresize * 0.1)
    piece = board.board[game.piece_spot[0]][game.piece_spot[1]]
    make_play(piece,game.chosen_spot,board, [game.chosen_spot])

def countdown(game):
    while True:
        graphics.draw_timer(game.time[player] ,graphics.timer_pos[0], graphics.timer_pos[1])  
        graphics.draw_timer(game.time[get_oppisite_color(player)] ,graphics.oppounent_timer_pos[0], graphics.oppounent_timer_pos[1])
        game = n.get(get)
        if game.game_over() or game.out_of_time():
            break

def get_time(game):
    if game.turn == 'w':
        return game.white_time
    return game.black_time

def get_oppisite_color(color):
    if color == 'w':
        return 'b'
    else:
        return 'w'                                                                                                                        

def main():
    global n, player, send, get, game
    n = Network()
    player = n.getP()
    send = game_data("update")
    get = game_data("get_game")

    board = game_board(player)
    
    graphics.draw_board(board.board,player)
    graphics.small_message("Player " + player, WHITE, graphics.squaresize * 4 - graphics.squaresize * 0.1, graphics.squaresize * 8 + graphics.border * 1.1)
    
    pygame.display.update()
    game_over = False
    connected = True
    while connected:
        pygame.event.get()
        game = n.get(get)
        if game.ready:
            draw_timers = threading.Thread(target=countdown, args=[game])
            draw_timers.start()
            while not game_over:
                pygame.event.get()
                game = n.get(get)
                if game.turn == player:
                    if game.piece_spot[0] != None:
                        oppounent_turn(game,board)
                        draw_timers = threading.Thread(target=countdown, args=[game])
                        draw_timers.start()
                    if not game.game_over():
                        turnMade = None
                        while not game.out_of_time() and turnMade == None:
                            chosen_spot = graphics.get_mouse_pos()
                            piece = board.board[chosen_spot[0]][chosen_spot[1]]
                            turnMade = run_play(piece,board,screen,player,n)
                        
                        if turnMade != None:
                            send.status = return_status(board.get_oppisite_color(game.turn),board)
                            send.turnMade = turnMade
                        else:
                            send.status = player + "OUT OF TIME"
                            piece_spot = game.reverse_spot(turnMade[0])
                            chosen_spot = game.reverse_spot(turnMade[1])
                            send.turnMade = (piece_spot,chosen_spot)
                            
                        
                        graphics.cover_text(graphics.squaresize * 4, 0, graphics.squaresize * 3, graphics.border)
                        graphics.small_message(send.status, WHITE, graphics.squaresize * 4, graphics.border * 0.2)
                        game = n.get(send)

                    else:
                        graphics.cover_text(graphics.squaresize * 4, 0, graphics.squaresize * 3, graphics.border)
                        graphics.small_message(game.status, WHITE, graphics.squaresize * 4, graphics.border * 0.2)
                        game_over = True
                        connected = False
                    
if __name__ == "__main__":
    main()