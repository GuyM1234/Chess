import pygame
import sys
color1 = (205,89,22)
color2 = (250,255,204)

BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
SQUARESIZE = 100

# פעולה המסירה את הנקודות של האפשרויות על המסך
class graphics_methods(object):
    
    def __init__(self,screen,big_font,small_font):
        self.screen = screen
        self.small_font = small_font
        self.big_font = big_font

    # פעולה המסירה את כל אפשרויות התזוזה
    def remove_option(self, option_list, color, board):
        for option in option_list:
            xpos = option[1] * 100 + 70
            ypos = option[0] * 100 + 65
            self.clearSquare(xpos - 20,ypos - 15)
            piece_on_option = board.board[option[0]][option[1]]
            if piece_on_option.color != "e":
                self.draw(piece_on_option)
        pygame.display.update()

    # פעולה המנקה את הקובייה
    def clearSquare(self,xpos, ypos):
        color = self.screen.get_at((xpos,ypos))
        pygame.draw.rect(self.screen, color, (xpos, ypos, 100, 100))

    # פעולה המציירת את הלוח
    def draw_board(self,board):
        count = 1
        count1 = 1
        for r in range(8):
            for c in range(8):
                if (count1 % 2 == 0):               
                    if count == 1:
                        pygame.draw.rect(self.screen, color1, (c*SQUARESIZE + 50, r*SQUARESIZE + 50, SQUARESIZE, SQUARESIZE))
                        count = 2
                    else:
                        pygame.draw.rect(self.screen, color2, (c*SQUARESIZE + 50, r*SQUARESIZE + 50, SQUARESIZE, SQUARESIZE))
                        count = 1
                else:
                    if count == 1:
                        pygame.draw.rect(self.screen, color2, (c*SQUARESIZE + 50, r*SQUARESIZE + 50, SQUARESIZE, SQUARESIZE))
                        count = 2
                    else:
                        pygame.draw.rect(self.screen, color1, (c*SQUARESIZE + 50, r*SQUARESIZE + 50, SQUARESIZE, SQUARESIZE))
                        count = 1
            count1 +=1
        for i in range(8):
            self.draw(board[0][i])
            self.draw(board[1][i])
            self.draw(board[6][i])
            self.draw(board[7][i])
        
        self.draw_timer(900,10,10)
        self.draw_timer(900,10,860)
    
    # פעולה המחזירה את מיקום הלחיצה
    def get_mouse_pos(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    chosen_xpos = event.pos[0]
                    chosen_ypos = event.pos[1]
                    column_pos = (chosen_xpos - 50) // 100
                    row_pos = (chosen_ypos - 50) // 100
                    if row_pos > - 1 and column_pos < 8 and column_pos > - 1 and column_pos < 8:
                        chosen_spot = ((row_pos,column_pos))
                        return chosen_spot
                    
    # הודעה בפונט גדול
    def big_message(self, msg, color, xpos, ypos):
        message = self.big_font.render(msg, True, color)
        self.screen.blit(message, [xpos, ypos])
        pygame.display.update()

    # הודעה בפונט קטן
    def small_message(self, msg, color, xpos, ypos):
        message = self.small_font.render(msg, True, color)
        self.screen.blit(message, [xpos, ypos])
        pygame.display.update()

    # פעולה המציירת את אפשרויות החלק
    def draw_options(self,option_list):
        for i in option_list:
            pygame.draw.circle(self.screen, BLUE, ((i[1] + 1) * SQUARESIZE, (i[0] + 1) * SQUARESIZE), 8)
            pygame.display.update()
    
        # פעולה לצייר על המסך את הכלי
    
    # 
    def draw_timer(self, t,posx, posy):
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs)
        pygame.draw.rect(self.screen, BLACK, (posx,posy, 100, 40))
        self.small_message(timer,WHITE,posx,posy)

    # פעולה המציירת את הלךק
    def draw(self,piece):
        self.screen.blit(piece.piece_pic, ((piece.spot[1]) * 100 + 70 + piece.offset_x, (piece.spot[0]) * 100 + 65 + piece.offset_y))
        pygame.display.update()