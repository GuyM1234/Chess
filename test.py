import pygame.event

from game.board import Board
from graphics import GraphicsMethods
from game.game_utils import update_turn, Spot
from game.ai.aimove import Ai


def move(board: [[]], move_from: Spot, move_to: Spot, graphics: GraphicsMethods):
    board = Board.move(board, move_from, move_to)
    graphics.move(board, move_from, move_to)
    board = Board.move_side_effect(board, move_to)
    return board


def main():
    board = Board.create_board()
    turn = "b"
    graphics = GraphicsMethods(75)
    graphics.draw_board(board, turn)

    while True:
        pygame.event.get()
        # move_from = graphics.get_mouse_pos()
        # move_options = Board.get_move_options(board, move_from, turn)
        # if len(move_options) > 0:
        #     graphics.draw_options(move_options)
        #     move_to = graphics.get_mouse_pos()
        #     graphics.remove_options(move_options, board)
        #     if move_to in move_options:
        #         board = move(board, move_from, move_to, graphics)
        #         turn = update_turn(turn)
        #         graphics.print_status(Board.status(board, turn))
        #         ai_move = Ai.get_move(board, turn)
        #         board = move(board, ai_move.move_from, ai_move.move_to, graphics)
        #         turn = update_turn(turn)
        #         graphics.print_status(Board.status(board, turn))
        ai_move = Ai.get_move(board, turn)
        board = move(board, ai_move.move_from, ai_move.move_to, graphics)
        turn = update_turn(turn)
        graphics.print_status(Board.status(board, turn))


if __name__ == "__main__":
    main()
