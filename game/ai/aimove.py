from game.pieces.piece import Piece
from game.game_utils import Move, Spot, print_board, is_spot_free, update_turn
from game.board import Board
import random
from operator import itemgetter
from game.ai.scoring import Scoring, Spots


class Ai:
    @staticmethod
    def get_moves(board: [[Piece]], turn: str):
        moves = []
        for row in range(8):
            for colum in range(8):
                moves += [Move(Spot(row, colum), option) for option in
                          Board.get_move_options(board, Spot(row, colum), turn)]
        return moves

    @staticmethod
    def get_move(board: [[Piece]], turn: str):
        return Ai.minimax(board, turn)[0]

    # @staticmethod
    # def best_move(board: [[Piece]], moves: [Move], turn: str):
    #     scores = []
    #     for move in moves:
    #         piece = board[move.move_to.row][move.move_to.colum]
    #         Board.move(board, move.move_from, move.move_to)
    #         scores.append((move, Ai.calculate_board_score(board)))
    #         Board.revert_move(board, piece, move.move_to, move.move_from)
    #     return max(scores, key=itemgetter(1))

    @staticmethod
    def minimax(board: [[Piece]], turn: str, max_color="b", depth=2):
        if depth == 0:
            return Ai.calculate_board_score(board)
        else:
            scores = []
            for move in Ai.get_moves(board, turn):
                piece = board[move.move_to.row][move.move_to.colum]
                board = Board.move(board, move.move_from, move.move_to)
                scores.append((move, Ai.minimax(board, update_turn(turn), depth=depth - 1)))
                board = Board.revert_move(board, piece, move.move_to, move.move_from)

            if turn == max_color:
                if len(scores) == 0:
                    print("Hi")
                return max(scores, key=itemgetter(1))
            else:
                if len(scores) == 0:
                    print("Hi")
                return min(scores, key=itemgetter(1))

    @staticmethod
    def calculate_board_score(board: [[Piece]]):
        score = []
        for row in range(8):
            for colum in range(8):
                if not is_spot_free(board, row, colum):
                    piece = board[row][colum]
                    score.append(
                        Scoring[piece.color][piece.piece_let] + Spots[piece.color][piece.piece_let][row, colum])
        return sum(score)

    @staticmethod
    def get_move_score(board: [[Piece]], move):
        piece = board[move.move_to.row][move.move_to.colum]
        Board.move(board, move.move_from, move.move_to)
        score = (move, Ai.calculate_board_score(board))
        Board.revert_move(board, piece, move.move_to, move.move_from)
        return score
