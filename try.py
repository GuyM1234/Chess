from network import Network
import pygame
import sys
import time
import threading

from graphics import graphics_methods
pygame.init()
font1 = pygame.font.SysFont(None ,40)
font2 = pygame.font.SysFont(None ,40)
width = 9 * 100
height = 9 * 100
size = (width,height)
screen = pygame.display.set_mode(size)
from game import game_data, Game
from graphics import graphics_methods

n = Network()
player = n.getP()
graphics = graphics_methods(screen, font1,font2,75)
game = Game()
send = game_data()
get = game_data()
get.message = "get_game"

def countdown(game, n):
    while True:
        if game.turn == player:
            graphics.draw_timer(game.time[player] ,graphics.timer_pos[0], graphics.timer_pos[1])
        else:
            graphics.draw_timer(game.time[game.turn] ,graphics.oppounent_timer_pos[0], graphics.oppounent_timer_pos[1])
        game = n.get(get)



send.turnMade = ((7,5),(2,5))

timer = threading.Thread(target=countdown, args=[game, n])
timer.start()

while True:
    pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:      
            game = n.get(send)
            
            

            
            
            
