from RLgames.Games.Game import Move, Board, gameState
from package.Point import Point
from package.Grid import Grid
from package.GridPointsStruct import GridPoints

class nokinlineMove(Move):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.coords = tuple(map(int, name[1:-1].split(",")))
        self.point = Point(*self.coords)

class nokinlineBoard(Board):
    def __init__(self, board_size: tuple, k: int) -> None:
        board_dims = (board_size[0],) * board_size[1]
        super().__init__(board_dims, ['O'])
        self.gp = GridPoints(n=board_size[0], d=board_size[1], k_in_line=k)
        self.legal_moves = self.gp.valid
        
    def create_move(self, input: str) -> Move:
        i = input[1:-1].split(',')
        if len(i) == len(self.board.shape):
            return nokinlineMove(input)
        return None
        
    def make_move(self, move: nokinlineMove):
        self.history.append(move)
        self.gp.add(p=move.point)
    
    def unmake_move(self, move: nokinlineMove = None):
        if move is None:
            move = self.history.pop()
        self.gp.remove(p=move.point)
    
    def update_state(self, move: Move):
        if len(self.gp.valid):
            self.state = gameState.ENDED
        self.winner = 'O'
        
        
        
        
        
        
        