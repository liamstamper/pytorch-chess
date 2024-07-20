import chess
import random

class Engine:
    def generate_move(self, board):
        """
        Generate a random legal move based on the current state of the chess board.
        :param board: An instance of a chess.Board containing the current game state.
        :return: A move in UCI format (e.g., 'e2e4') chosen randomly from the legal moves.
        """
        moves = list(board.legal_moves) 
        if moves:  
            return random.choice(moves).uci()  
        else:
            return None  
