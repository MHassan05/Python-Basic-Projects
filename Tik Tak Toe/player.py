import random 

class Player: 
    def __init__(self, letter):
        self.letter = letter
    
    def make_move(self, board):
        pass 

class HumanPlayer(Player):

    def __init__(self, letter):
        super().__init__(letter)
    
    # No need to override make_move for human player, as it will be handled by the UI

class ComputerPlayer(Player):
    
    def __init__(self, letter):
        super().__init__(letter)
    
    def make_move(self, board):
        return random.choice([i for i, cell in enumerate(board) if cell == ' '])
        
class AIPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def make_move(self, board):
        # TODO: Implement Minimax algorithm,
        # but for now, just return a random move 
        return random.choice([i for i, cell in enumerate(board) if cell == ' '])