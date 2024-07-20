# controller.py
from board import ChessBoard
from engine import Engine  
from gui import Gui
import tkinter as tk
import chess
import threading

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
        Attempt to make a player's move and then initiate an AI move.
        Update the GUI immediately after the player's move, and then again after the AI's move.
        """
        self.board.make_move(move_str)
        self.update_gui_board()  

        # Runs AI move generation in a separate thread to avoid freezing the GUI
        ai_thread = threading.Thread(target=self.handle_ai_move)
        ai_thread.start()


    def handle_ai_move(self):
        """
        Handles the generation and making of the AI move.
        """
        ai_move = self.engine.generate_move(self.board.board)
        if ai_move:
            self.board.make_move(ai_move)
            self.root.after(0, self.update_gui_board)  # Ensure GUI update happens on the main thread
            self.root.after(0, lambda: self.gui.message_label.config(text=f"AI moved {ai_move}"))
        else:
            self.root.after(0, lambda: self.gui.message_label.config(text="No valid AI moves available."))

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
