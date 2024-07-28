# /network/processing.py
import chess.pgn


class Processing:
    def load_games(pgn_path):
        games = []
        with open(pgn_path, 'r') as pgn_file:
            while True:
                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    break
                games.append(game)
            return games
        
    

