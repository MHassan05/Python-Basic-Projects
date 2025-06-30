from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from game import TikTakToe 
from player import HumanPlayer, ComputerPlayer, AIPlayer 

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎮 Tic Tac Toe - Main Menu")
        self.setFixedSize(400, 500)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(25)
        self.layout.setContentsMargins(40, 40, 40, 40)
        
        self.create_ui()
        self.apply_styles()

    def create_ui(self):
        # Title
        self.title = QLabel("🎯 TIC TAC TOE")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 28, QFont.Bold))
        
        # Subtitle
        self.subtitle = QLabel("Choose Your Game Mode")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setFont(QFont("Arial", 14))
        
        # Game mode buttons
        self.human_vs_human = QPushButton("👥 Human vs Human")
        self.human_vs_human.setFixedHeight(70)
        self.human_vs_human.clicked.connect(self.start_game)

        self.human_vs_computer = QPushButton("🤖 Human vs Computer")
        self.human_vs_computer.setFixedHeight(70)
        self.human_vs_computer.clicked.connect(self.start_game)

        self.human_vs_ai = QPushButton("🧠 Human vs AI")
        self.human_vs_ai.setFixedHeight(70)
        self.human_vs_ai.clicked.connect(self.start_game)
        
        # Footer
        self.footer = QLabel("Select a game mode to start playing!")
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setFont(QFont("Arial", 10))
        
        # Add widgets to layout
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.human_vs_human)
        self.layout.addWidget(self.human_vs_computer)
        self.layout.addWidget(self.human_vs_ai)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.footer)

    def apply_styles(self):
       self.setStyleSheet("""
                    QLabel {
                        color: #333;
                        background: transparent;
                        padding: 5px;
                    }

                    QPushButton {
                        border: 3px solid rgba(51, 51, 51, 0.3); /* matches #333 with transparency */
                        border-radius: 20px;
                        font-size: 18px;
                        font-weight: bold;
                        color: #333;
                        padding: 15px;
                        margin: 5px;
                    }

                    QPushButton:hover {
                        border: 3px solid #333;
                    }

                    QPushButton:pressed {
                        border: 3px solid rgba(51, 51, 51, 0.6); /* matches #333 with transparency */
                    }
                """)


    def start_game(self):
        sender_text = self.sender().text()
        if "Human vs Human" in sender_text:
            self.game = TikTakToe(HumanPlayer, HumanPlayer)
        elif "Human vs Computer" in sender_text:
            self.game = TikTakToe(HumanPlayer, ComputerPlayer)
        elif "Human vs AI" in sender_text:
            self.game = TikTakToe(HumanPlayer, AIPlayer)
        self.game.show()
        self.close()

if __name__ == "__main__":
    import sys
    app = QApplication([])
    menu = Menu()
    menu.show()
    sys.exit(app.exec_())