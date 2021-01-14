import concurrent.futures
import threading
import time
import pygame
import sys

from graphics import graphics_methods
pygame.init()
font1 = pygame.font.SysFont(None ,40)
font2 = pygame.font.SysFont(None ,200)
width = 9 * 100
height = 9 * 100
size = (width,height)
screen = pygame.display.set_mode(size)
graphics = graphics_methods(screen,font2,font1)
stop_cloak = False

def countdown(t, stop_cloak):
    while True: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs)
        pygame.draw.rect(screen, (0,0,0), (100, 100, 400, 400))
        graphics.small_message(timer,(255,255,255),100,100)
        time.sleep(1)
        t -= 1
        if stop_cloak():
            break

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     f1 = executor.submit(countdown, 900)

t = threading.Thread(target=countdown, args=[900, lambda : stop_cloak,])

t.start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            stop_cloak = True
