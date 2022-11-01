from .board import Board


class ChessBoard(Board):
    def __init__(self):
        super().__init__(8)

    def reset(self):
        self.turn = 'white'
        self.running = True

        # self.passant['white'] = None
        # self.passant['black'] = None
