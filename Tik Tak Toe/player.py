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
        best_score = float('-inf')
        best_move = None

        for i in range(9):
           if board[i] == ' ':
               board[i] = self.letter
               score = self.minimax(board, False)
               board[i] = ' '
               if score > best_score:
                   best_score = score
                   best_move = i
        return best_move
    
    def minimax(self, board, is_maximizing):
        max_player = self.letter
        min_player = 'O' if self.letter == 'X' else 'X'

        if self.check_winner(board, max_player):
            return 1
        elif self.check_winner(board, min_player):
            return -1
        elif ' ' not in board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = max_player
                    score = self.minimax(board, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = min_player
                    score = self.minimax(board, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score
        
    def check_winner(self, board, player):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
                return True
        return False

       
