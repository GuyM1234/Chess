from network import Network
import pygame
import sys
import time

from graphics import graphics_methods
pygame.init()
font1 = pygame.font.SysFont(None ,40)
font2 = pygame.font.SysFont(None ,200)
width = 9 * 100
height = 9 * 100
size = (width,height)
screen = pygame.display.set_mode(size)
from game import game_data, Game
n = Network()

data = game_data()

data.get_game = True
g = n.send(data)
data.get_game = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            data.status = "clicked"
            data.turnMade = ((0,5),(7,8))
            g = n.send(data)
            time.sleep(0.1)
            print(g.status)
            print(g.piece_spot)
            print(g.chosen_spot)
