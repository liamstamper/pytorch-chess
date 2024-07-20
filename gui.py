import tkinter as tk
from PIL import Image, ImageTk
import chess
from board import ChessBoard

class Gui:
    def __init__(self, root, controller):
        self.root = root
        self.root.title("Pytorch Chess Engine - Liam Stamper")
        self.controller = controller
        self.canvas = tk.Canvas(root, width=640, height=640)
        self.canvas.pack(side="left", padx=10)
        self.images = self.load_images()
        self.setup_board()
        self.selected_piece = None
        self.selected_position = None
        self.canvas.bind("<Button-1>", self.calculate_clicks) 



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
        Submit the move clicked by the user, update the game state, and refresh the GUI.
        """
        move_str = (str(self.selected_piece) + str(self.selected_position))
        if self.controller.validate_move(move_str):
            self.controller.make_move(move_str)
            self.controller.update_gui_board()
        else:
            print("Invalid move attempted.")
            self.selected_piece = None
            self.selected_position = None

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

    def highlight_square(self, position):
        """
        Highlight given square
        :param postion: col, row
        """
        col, row = position
        self.canvas.create_rectangle(col*80, row*80, col*80+80, row*80+80, outline='yellow', width=2)

    def unhighlight_squares(self):
        """
        Unhiglights given square by redrawing board
        """
        self.setup_board()


    def calculate_clicks(self, event):
        """
        Convert pixel coordinates to board coordinates and manage the selection and movement of pieces.
        :param event: The mouse event containing the x and y coordinates of the click.
        """
        col = event.x // 80  
        row = event.y // 80  
        pixel_position = (col, row)  
        uci_position = chr(col + ord('a')) + str(8 - row)  

        if not self.selected_piece:
            self.highlight_square(pixel_position)  
            self.selected_piece = uci_position
        else:
            self.selected_position = uci_position
            self.unhighlight_squares()
            self.submit_move()
            self.selected_piece = None  
            self.selected_position = None

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
