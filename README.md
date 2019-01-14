# ChessAI

An implementation of a neural network chess.

<img width=600px src="https://github.com/Ian-Dzindo01/Chess-AI/blob/master/screenshot.png" />

Usage
-----

```
 pip3 install python-chess torch torchvision numpy flask
 # then...
 ./play.py   # runs webserver on localhost:5000
```

TODOs
-----
1. Implement a score function which evaluates how well the computer is playing.
2. Look into minimax.

Advanced:

3. Add RL self play learning support.
4. Roll out search beyond 1-ply.

Implementation
-----

The trained net is in nets/value.pth. It takes in a serialized board and outputs a range from -1 to 1. -1 means black is win, 1 means white is win.

Serialization
-----

We serialize the board into a 8x8x5 bitvector. See state.py for how.

Training Set
-----

The value function was trained on 100K board positions for now. More trained functions expected in the near future. Data is from http://www.kingbase-chess.net/

Credits:
------

Credits to https://github.com/geohot and his livestream: https://www.youtube.com/watch?v=RFaFmkCEGEs&t=9590s for teaching me how to do this properly.
