# main.py
import tkinter as tk
from controller import ChessController

def main():
    root = tk.Tk()
    app = ChessController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
