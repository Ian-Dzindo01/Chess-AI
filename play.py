from state import State
import torch
from train import Net
import chess
import chess.svg


class Valuator(object):
    def __init__(self):
        vals = torch.load("nets/value.pth", map_location=lambda storage, loc: storage)    # these lines make sure that the CPU is used instead of the GPU.
        self.model = Net()
        self.model.load_state_dict(vals)

    def __call__(self, s):                        # this return a value representing how good a move actually is.
        brd = s.serialize()[None]                 # QUESTION: Why is this [None]?
        output = model(torch.tensor(brd).float())
        return float(output.data[0][0])

    def explore_leaves(s, v):               # this function iterates over all the available moves and stores the move and it's likelihood to win.
        ret = []
        for e in s.edges():                 # s.edges might be the available moves
            s.board.push(e)
            ret.append((v(s), e))
            s.board.pop()
        return ret


v = Valuator()
s = State()

app = Flask(__name__)


def computer_move():
    move = sorted(explore_leaves(s, v), key=lambda x: x[0], reverse=s.board.turn)[0]


computer_move()


@app.route("/")
def hello():
    return '<html><body><img src="board.svg" />'


@app.route("/board.svg")
def hello():
    chess.svg.board(board=s.board)


# if __name__ == '__main__':

#     # self play
#     while not s.board.is_game_over():
#         l = sorted(explore_leaves(s, v), key=lambda x: x[0], reverse=s.board.turn)    # this orders the moves by their likelihoods of winning
#         move = l[0]
#         print(move)
#         s.board.push(move[1])                                                         # and performs the best possible move
#     print(s.board.result())
