# board.py
import chess

class ChessBoard:
    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move):
        move = chess.Move.from_uci(move)
        if move in self.board.legal_moves:
            self.board.push(move)
        
    def current_board_state(self):
        return self.board.fen()

    def legal_moves(self):
        return [move.uci() for move in self.board.legal_moves]
