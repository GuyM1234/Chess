import pygame
import sys
from game.game_utils import is_spot_free, is_in_board, Spot

color1 = (205, 89, 22)
color2 = (250, 255, 204)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DEFAULT_SQUARESIZE = 100
pygame.init()


class GraphicsMethods(object):
    def __init__(self, squaresize: int):
        self.screen = pygame.display.set_mode((9 * squaresize, 9 * squaresize))
        self.squaresize = squaresize
        self.ratio = squaresize / DEFAULT_SQUARESIZE
        self.small_font = pygame.font.SysFont(None, 200)
        self.big_font = pygame.font.SysFont(None, squaresize // 2 - 10)
        self.pic_dict = self.build_pic_dict()
        self.border = self.squaresize // 2
        # self.timer_pos = (self.border * 0.2, self.squaresize * 8.5 + self.border * 0.2)
        # self.oppounent_timer_pos = (self.border * 0.2, self.border * 0.2)

    def build_pic_dict(self):
        pic_dict = {'w': {'P': Picture(pygame.image.load(r'Chesspieces\WhitePawn.png'), 61, 80),
                          'R': Picture(pygame.image.load(r'Chesspieces\WhiteRook.png'), 70, 80),
                          'B': Picture(pygame.image.load(r'Chesspieces\WhiteBishop.png'), 77, 80),
                          'k': Picture(pygame.image.load(r'Chesspieces\WhiteKnight.png'), 81, 80),
                          'Q': Picture(pygame.image.load(r'Chesspieces\WhiteQueen.png'), 85, 80),
                          'K': Picture(pygame.image.load(r'Chesspieces\WhiteKing.png'), 81, 80)},
                    'b': {'P': Picture(pygame.image.load(r'Chesspieces\BlackPawn.png'), 61, 80),
                          'R': Picture(pygame.image.load(r'Chesspieces\BlackRook.png'), 70, 80),
                          'B': Picture(pygame.image.load(r'Chesspieces\BlackBishop.png'), 77, 80),
                          'k': Picture(pygame.image.load(r'Chesspieces\BlackKnight.png'), 81, 80),
                          'Q': Picture(pygame.image.load(r'Chesspieces\BlackQueen.png'), 85, 80),
                          'K': Picture(pygame.image.load(r'Chesspieces\BlackKing.png'), 81, 80)}
                    }

        for color in pic_dict.values():
            for pic in color.values():
                self.update_pic_to_ratio(pic)

        return pic_dict

    def update_pic_to_ratio(self, pic):
        pic.width = round(pic.width * self.ratio)
        pic.height = round(pic.height * self.ratio)
        pic.pic = pygame.transform.scale(pic.pic, (pic.width, pic.height))

    def move(self, board, move_from, move_to):
        xpos = move_from.colum * self.squaresize + 0.5 * self.squaresize
        ypos = move_from.row * self.squaresize + 0.5 * self.squaresize
        self.clearSquare(xpos, ypos)
        xpos = move_to.colum * self.squaresize + 0.5 * self.squaresize
        ypos = move_to.row * self.squaresize + 0.5 * self.squaresize
        self.clearSquare(xpos, ypos)
        self.draw(board, move_to.row, move_to.colum)

    # פעולה המציירת את אפשרויות החלק
    def draw_options(self, options):
        for option in options:
            pygame.draw.circle(self.screen, BLUE,
                               ((option.colum + 1) * self.squaresize, (option.row + 1) * self.squaresize), 8)
            pygame.display.update()

    # פעולה המסירה את כל אפשרויות התזוזה
    def remove_options(self, options, board):
        for option in options:
            xpos = option.colum * self.squaresize + 0.5 * self.squaresize
            ypos = option.row * self.squaresize + 0.5 * self.squaresize
            self.clearSquare(xpos, ypos)
            if not is_spot_free(board, option.row, option.colum):
                self.draw(board, option.row, option.colum)

    # פעולה המנקה את הקובייה
    def clearSquare(self, xpos, ypos):
        color = self.screen.get_at((round(xpos), round(ypos)))
        pygame.draw.rect(self.screen, color, (xpos, ypos, self.squaresize, self.squaresize))
        pygame.display.update()

    # פעולה המציירת את הלוח
    def draw_board(self, board, color):
        i = 0
        if color == 'b':
            i += 1
        colors = (color1, color2)
        for r in range(8):
            for c in range(8):
                i += 1
                pygame.draw.rect(self.screen, colors[i % 2], (
                    c * self.squaresize + self.border, r * self.squaresize + self.border, self.squaresize,
                    self.squaresize))
            i += 1

        for i in range(8):
            self.draw(board, 0, i)
            self.draw(board, 1, i)
            self.draw(board, 6, i)
            self.draw(board, 7, i)

        # self.draw_timer(900, self.timer_pos[0], self.timer_pos[1])
        # self.draw_timer(900, self.oppounent_timer_pos[0], self.oppounent_timer_pos[1])

    # פעולה המחזירה את מיקום הלחיצה
    def get_mouse_pos(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    chosen_xpos = event.pos[0]
                    chosen_ypos = event.pos[1]
                    column = (chosen_xpos - self.border) // self.squaresize
                    row = (chosen_ypos - self.border) // self.squaresize
                    if is_in_board(row, column):
                        return Spot(row, column)

    # הודעה בפונט גדול
    def big_message(self, msg, color, xpos, ypos):
        message = self.big_font.render(msg, True, color)
        self.screen.blit(message, [xpos, ypos])
        pygame.display.update()

    def print_status(self, status: str):
        self.cover_text(self.squaresize * 4, 0, self.squaresize * 4, self.squaresize // 2)
        self.big_message(status, WHITE, self.squaresize * 4, self.squaresize // 10)

    # הודעה בפונט קטן
    def small_message(self, msg, color, xpos, ypos):
        message = self.small_font.render(msg, True, color)
        self.screen.blit(message, [xpos, ypos])
        pygame.display.update()

    # def draw_timer(self, t, posx, posy):
    #     mins, secs = divmod(t, 60)
    #     timer = '{:02d}:{:02d}'.format(mins, secs)
    #     self.cover_text(posx, posy, self.squaresize, self.border * 0.7)
    #     self.small_message(timer, WHITE, posx, posy)

    # פעולה המציירת את החלק
    def draw(self, board, row, colum):
        piece = board[row][colum]
        if piece is not None:
            piece_pic = self.pic_dict[piece.color][piece.piece_let]
            ypos_offset = round(0.5 * self.squaresize + (self.squaresize - piece_pic.height) / 2)
            xpos_offset = round(0.5 * self.squaresize + (self.squaresize - piece_pic.width) / 2)
            self.screen.blit(piece_pic.pic, (
                colum * self.squaresize + xpos_offset, row * self.squaresize + ypos_offset))
            pygame.display.update()

    def cover_text(self, xpos, ypos, width, height):
        pygame.draw.rect(self.screen, BLACK, (round(xpos), round(ypos), round(width), round(height)))


class Picture(object):
    def __init__(self, pic, width, height):
        self.pic = pic
        self.width = width
        self.height = height
