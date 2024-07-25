import os
import copy
import chess
import torch
from torch import nn 

class Engine:
    def generate_move(self, board):
        """
        Generate the best move for the current player using the minimax function that connects to the evaluation function.
        Utilizes a board copy to prevent changes to the actual game state.
        :param board: An instance of a chess.Board containing the current game state.
        :return: A move in UCI format (e.g., 'e2e4') that represents the best move calculated.
        """
        board_copy = copy.deepcopy(board)
        best_move = None
        best_value = float('-inf') if board_copy.turn == chess.WHITE else float('inf')
        
        for move in board_copy.legal_moves:
            board_copy.push(move)
            value = self.minimax(board_copy, 3, float('-inf'), float('inf'), board_copy.turn)
            board_copy.pop()

            if board_copy.turn == chess.WHITE and value > best_value:
                best_value = value
                best_move = move
            elif board_copy.turn == chess.BLACK and value < best_value:
                best_value = value
                best_move = move
        return best_move.uci() if best_move else None


    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with Alpha-Beta pruning to find the optimal move value.
        :param board: A copy of the chess board for recursive move evaluation.
        :param depth: The maximum depth of the search tree.
        :param alpha: The best already explored option along the path to the root for maximizer.
        :param beta: The best already explored option along the path to the root for minimizer.
        :param maximizing_player: Boolean indicating if the current move is for the maximizing player.
        :return: The value of the board.
        """
        if depth == 0 or board.is_game_over():
            eval = self.evaluate(board)
            return eval

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                current_eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, current_eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                current_eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, current_eval)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate(self, board):
        """
        Simple evaluation function that counts the material advantage.
        :param board: The chess board to evaluate.
        :return: A numerical score where positive values are better for White, negative for Black.
        """
        device = (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )
        print(f"Using {device} device")


        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                score += value if piece.color == chess.WHITE else -value
        return score