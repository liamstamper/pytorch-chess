# controller.py
from board import ChessBoard
from engine import Engine  
from gui import Gui
import tkinter as tk
import chess

class ChessController:
    def __init__(self, root):
        self.root = root
        self.board = ChessBoard()
        self.engine = Engine()  # Initialize the engine
        self.gui = Gui(root, self)
        self.update_gui_board()  # Initial update to render the chess pieces

    def update_gui_board(self):
        """
        # Updates the GUI to reflect the current state of the chess board.
        This involves clearing the existing pieces from the canvas and
        redrawing them according to the board state.
        """
        self.gui.clear_pieces()
        for square in chess.SQUARES:
            piece = self.board.board.piece_at(square)
            if piece:
                piece_type = piece.piece_type
                piece_color = 'w' if piece.color else 'b'
                piece_name = {
                    chess.PAWN: 'pawn',
                    chess.KNIGHT: 'knight',
                    chess.BISHOP: 'bishop',
                    chess.ROOK: 'rook',
                    chess.QUEEN: 'queen',
                    chess.KING: 'king'
                }[piece_type]
                image_key = f"{piece_color}_{piece_name}"
                image = self.gui.images.get(image_key)
                if image:
                    x, y = self.gui.calculate_position(square)
                    self.gui.canvas.create_image(x, y, image=image, tags="piece")
                else:
                    print(f"No image found for key: {image_key}")

    def make_move(self, move_str):
        """
        Attempt to make a player's move followed by generating and making an AI move.
        Update the GUI and display messages according to the move's success or failure.
        """
        try:
            self.board.make_move(move_str)
            self.update_gui_board()  # Update GUI after the player's move
            ai_move = self.engine.generate_move(self.board.board)
            self.board.make_move(ai_move)
            self.update_gui_board()  # Update GUI after the AI's move
            self.gui.message_label.config(text=f"AI moved {ai_move}")
        except ValueError as e:
            self.gui.message_label.config(text=str(e))
            # Optionally, re-raise the exception if further handling is needed elsewhere
            raise ValueError(e)

    def on_square_selected(self, square):
        """
        Handle selections of squares on the GUI to process and make moves.
        """
        if self.gui.selected_position is None:
            self.gui.selected_position = square
        else:
            try:
                move_uci = f"{chess.square_name(self.gui.selected_position)}{chess.square_name(square)}"
                self.make_move(move_uci)
            except ValueError as e:
                print(e)  # Optionally, handle this more gracefully in the GUI
            finally:
                self.gui.selected_position = None
