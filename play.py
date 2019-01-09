from state import State
import torch
from nnet import Net
import chess
import chess.svg
import time


class Valuator(object):
    def __init__(self):
        vals = torch.load("nets/value.pth", map_location=lambda storage, loc: storage)    # these lines make sure that the CPU is used instead of the GPU.
        self.model = Net()
        self.model.load_state_dict(vals)

    def __call__(self, s):                        # this returns a value representing how good a move actually is.
        brd = s.serialize()[None]                 # QUESTION: Why is this [None]?
        output = self.model(torch.tensor(brd).float())
        return float(output.data[0][0])


def explore_leaves(s, v):               # this function iterates over all the available moves and stores the move and how good the move is.
    ret = []
    for e in s.edges():                 # s.edges returns the list of legal moves
        s.board.push(e)
        ret.append((v(s), e))
        s.board.pop()
    return ret


# chess board and engine
s = State()
v = Valuator()


from flask import Flask, Response, request
app = Flask(__name__)


@app.route("/")
def hello():
    ret = '<html><head>'
    ret += '<style> input { font-size: 30px; } button { font-size: 30px; }</style>'
    ret += '</head><body>'
    ret += '<img width=600 height=600 src="/board.svg"?%f ></img><br/>' % time.time()
    ret += '<form action="/move"><input name="move" type="text"></input><input type="submit" value="Move"></form><br/>'
    return ret


@app.route("/board.svg")
def board():
    return Response(chess.svg.board(board=s.board), mimetype='image/svg+xml')


def computer_move():
    move = sorted(explore_leaves(s, v), key=lambda x: x[0], reverse=s.board.turn)[0]
    print(move)
    s.board.push(move[1])


@app.route("/move")
def move():
    if not s.board.is_game_over():
        move = request.args.get('move', default="")
        if move is not None and move != "":
            print("Human moves ", move)
            s.board.push_san(move)
            computer_move()
    else:
        print("GAME IS OVER")
    return hello()


if __name__ == "__main__":
    app.run(debug=True)

    # if __name__ == '__main__':

    #     # self play
    #     while not s.board.is_game_over():
    #         l = sorted(explore_leaves(s, v), key=lambda x: x[0], reverse=s.board.turn)    # this orders the moves by their likelihoods of winning
    #         move = l[0]
    #         print(move)
    #         s.board.push(move[1])                                                         # and performs the best possible move
    #     print(s.board.result())
