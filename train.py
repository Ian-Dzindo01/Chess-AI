import os
import chess
import chess.pgn
from state import State
import h5py
import numpy as np


def get_dataset(num_samples=None):
    X, Y = [], []
    gn = 0
    values = {'1/2-1/2': 0, '0-1': -1, '1-0': 1}
    for fn in os.listdir("C:/Users/USER/Desktop/Kingbase Chess Games"):
        pgn = open(os.path.join("C:/Users/USER/Desktop/Kingbase Chess Games", fn))
        while 1:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            res = game.headers['Result']
            if res not in values:
                continue
            value = values[res]
            board = game.board()
            for i, move in enumerate(game.main_line()):
                board.push(move)
                ser = State(board).serialize()
                X.append(ser)                   # each move is represented in pair with the final result of the game, so the computer can find out which moves were good and which ones weren't.
                Y.append(value)
            print(f"Parsing game: {gn}, got {len(X)} examples")
            if num_samples is not None and len(X) > num_samples:
                return X, Y
            gn += 1
    X = np.array(X)
    Y = np.array(Y)
    return X, Y


if __name__ == "__main__":
    X, Y = get_dataset(3000000)
    np.savez("D:/Projects/AI/Chess AI/processed/dataset_3M.npz", X, Y)
