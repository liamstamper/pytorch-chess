import tkinter as tk
from PIL import Image, ImageTk
import chess

class Gui:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.canvas = tk.Canvas(root, width=640, height=640)
        self.images = self.load_images()
        self.setup_board()
        self.selected_position = None

        self.side_frame = tk.Frame(root, width=200, height=640)
        self.side_frame.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.move_entry = tk.Entry(self.side_frame, width=15)
        self.move_entry.pack(pady=20)

        self.submit_button = tk.Button(self.side_frame, text="Make Move", command=self.submit_move)
        self.submit_button.pack(pady=10)

        self.message_label = tk.Label(self.side_frame, text="Enter your moves (e.g., e2e4)")
        self.message_label.pack(pady=10)

    def load_images(self):
        """
        Load all chess piece images and store them in a dictionary.
        :return: Dictionary of ImageTk.PhotoImage objects keyed by piece type and color.
        """
        pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        colors = ['b', 'w']
        images = {}
        for color in colors:
            for piece in pieces:
                filename = f'{color}_{piece}.png'
                try:
                    image = Image.open(f'imgs/{filename}')
                    key = f"{color}_{piece}"  # Using the full piece name for the key
                    images[key] = ImageTk.PhotoImage(image)
                except FileNotFoundError:
                    print(f"Error: Image file not found: imgs/{filename}")
                except Exception as e:
                    print(f"Error loading image {filename}: {e}")
        return images

    def submit_move(self):
        """
        Submit the move entered by the user, update the game state, and refresh the GUI.
        """
        move_str = self.move_entry.get()
        try:
            self.controller.make_move(move_str)
            self.move_entry.delete(0, tk.END)
        except ValueError as e:
            self.move_entry.delete(0, tk.END)
        self.controller.update_gui_board()

    def setup_board(self):
        """
        Setup the chessboard visualization
        """
        color1, color2 = "white", "gray"
        for row in range(8):
            color = color1 if row % 2 == 0 else color2
            for col in range(8):
                x1, y1 = col * 80, row * 80
                x2, y2 = x1 + 80, y1 + 80
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                color = color1 if color == color2 else color2
        self.canvas.pack()

    def calculate_position(self, square):
        """
        Calculate the canvas coordinates for a chess square.
        :param square: Chess square index.
        :return: Tuple (x, y) representing pixel coordinates on the canvas.
        """
        col = chess.square_file(square)
        row = 7 - chess.square_rank(square)
        x = col * 80 + 40  # Center of square horizontally
        y = row * 80 + 40  # Center of square vertically
        return x, y

    def clear_pieces(self):
        """
        Clear all piece images from the canvas.
        """
        self.canvas.delete("piece")
