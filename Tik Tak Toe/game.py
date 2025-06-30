from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton, QLabel,
                              QMessageBox, QHBoxLayout, QVBoxLayout)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
from player import HumanPlayer, ComputerPlayer, AIPlayer
from functools import partial

class TikTakToe(QWidget):
    def __init__(self, player1=HumanPlayer, player2=ComputerPlayer):
        super().__init__()
        self.setWindowTitle("🎮 Tic Tac Toe")
        self.setFixedSize(450, 550)

        self.player1 = player1('X')
        self.player2 = player2('O')
        self.current_player = self.player1

        self.board = [' ' for _ in range(9)]
        self.buttons = []

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.create_UI()
        self.apply_styles()

    def create_UI(self):
        # Title
        self.title_label = QLabel("🎯 TIC TAC TOE")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        
        # Current player info
        self.player_info = QLabel(f"Current Turn: Player ({self.current_player.letter})")
        self.player_info.setAlignment(Qt.AlignCenter)
        self.player_info.setFont(QFont("Arial", 14))
        
        # Game board
        self.board_widget = QWidget()
        self.grid_layout = QGridLayout(self.board_widget)
        self.grid_layout.setSpacing(5)
        self.create_board()
        
        # Control buttons
        self.controls_layout = QHBoxLayout()
        self.new_game_btn = QPushButton("🔄 New Game")
        self.new_game_btn.clicked.connect(self.reset_game)
        self.back_to_menu_btn = QPushButton("🏠 Main Menu")
        self.back_to_menu_btn.clicked.connect(self.back_to_menu)
        
        self.controls_layout.addWidget(self.new_game_btn)
        self.controls_layout.addWidget(self.back_to_menu_btn)
        
        # Add everything to main layout
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.player_info)
        self.main_layout.addWidget(self.board_widget)
        self.main_layout.addLayout(self.controls_layout)

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = QPushButton(' ')
                button.setFixedSize(100, 100)
                button.clicked.connect(partial(self.make_move, i * 3 + j))
                self.grid_layout.addWidget(button, i, j)
                self.buttons.append(button)

    def apply_styles(self):
        # Apply specific styles to control buttons
        self.new_game_btn.setObjectName("controlBtn")
        self.back_to_menu_btn.setObjectName("controlBtn")
        with open("styles.css", "r") as f:
            style = f.read()
            self.setStyleSheet(style)

    def make_move(self, index):
        if self.board[index] == ' ':
            self.board[index] = self.current_player.letter
            self.buttons[index].setText(self.current_player.letter)
            self.buttons[index].setEnabled(False)
            if self.check_winner():
                QMessageBox.information(self, "Game Over", f"Player {self.current_player.letter} wins!")
                self.reset_game()
            elif ' ' not in self.board:
                QMessageBox.information(self, "Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.switch_player()

    def switch_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2
        self.player_info.setText(f"Current Turn: Player ({self.current_player.letter})") 

        if isinstance(self.current_player, AIPlayer) or isinstance(self.current_player, ComputerPlayer):
            idx = self.current_player.make_move(self.board)
            self.make_move(idx) # recursively call make_move for Computer's turn

    def check_winner(self):
       winnig_combinations = [
           (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
           (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
           (0, 4, 8), (2, 4, 6)              # Diagonals
       ]
       for combo in winnig_combinations:
              if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return True

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        for button in self.buttons:
            button.setText(' ')
            button.setEnabled(True)
        self.current_player = self.player1
        self.player_info.setText(f"Current Turn: Player ({self.current_player.letter})")

    def back_to_menu(self):
        from main import Menu
        self.menu = Menu()
        self.menu.show()
        self.close()

    
if __name__ == "__main__":
    app = QApplication([])
    game = TikTakToe(HumanPlayer, ComputerPlayer)
    game.show()
    sys.exit(app.exec_())