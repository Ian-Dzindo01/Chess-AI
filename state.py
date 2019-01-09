import chess
import numpy as np
from nnet import Net


class State(object):
    def __init__(self, board=None):
        if board is None:
            self.board = chess.Board()
        else:
            self.board = board

    # this function essentially serializes the state of the board and stores it in a 3 dimensional array, which gets returned.
    def serialize(self):
        assert self.board.is_valid()

        bstate = np.zeros(64, np.uint8)      # bstate tells which figure is on which position on the board

        for i in range(64):
            pp = self.board.piece_at(i)

            if pp is not None:
                bstate[i] = {"P": 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6,
                             "p": 9, "n": 10, "b": 11, "r": 12, "q": 13, "k": 14}[pp.symbol()]

        # QUESTION: Why are we setting these to blank here?
        if self.board.has_queenside_castling_rights(chess.WHITE):
            assert bstate[0] == 4                                # going to assert if rook is not in it's place
            bstate[0] = 7                                        # this is going to be blank now. It removes the rook from it's place?

        if self.board.has_kingside_castling_rights(chess.WHITE):
            assert bstate[7] == 4
            bstate[7] = 7

        if self.board.has_queenside_castling_rights(chess.BLACK):
            assert bstate[56] == 12
            bstate[56] = 8 + 7

        if self.board.has_kingside_castling_rights(chess.BLACK):
            assert bstate[63] == 12                               # again, check whether the rook is in it's place
            bstate[63] = 8 + 7                                    # set to blank

        if self.board.ep_square is not None:
            assert bstate[self.board.ep_square] == 0
            bstate[self.board.ep_square] = 8                      # set to blank

        bstate = bstate.reshape(8, 8)

        # binary state
        state = np.zeros((5, 8, 8), np.uint8)

        # 0-3 columns to binary
        state[0] = (bstate >> 3) & 1                        # QUESTION: Why are we even doing this here?
        state[1] = (bstate >> 2) & 1                        # Returns bstate with the bits shifted to the right by 2 places. This is the same as dividing bstate by 2**2.
        state[2] = (bstate >> 1) & 1
        state[3] = (bstate >> 0) & 1

        # 4th column is who's turn it is
        state[4] = (self.board.turn * 1.0)

        return state

    def edges(self):
        return list(self.board.legal_moves)


if __name__ == "__main__":
    s = State()
