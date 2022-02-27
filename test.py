from game.board import Board
from graphics import GraphicsMethods
from game.game_utils import update_turn


def main():
    board = Board.create_board()
    turn = "w"
    graphics = GraphicsMethods(75)
    graphics.draw_board(board, turn)
    while True:
        move_from = graphics.get_mouse_pos()
        move_options = Board.get_move_options(board, move_from, turn)
        if len(move_options) > 0:
            graphics.draw_options(move_options)
            move_to = graphics.get_mouse_pos()
            graphics.remove_options(move_options, board)
            if move_to in move_options:
                board = Board.move(board, move_from, move_to)
                graphics.move(board, move_from, move_to)
                turn = update_turn(turn)
                board = Board.move_side_effect(board, move_to)
                graphics.print_status(Board.status(board, turn))


if __name__ == "__main__":
    main()
