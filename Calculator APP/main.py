from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton, QLineEdit)
import sys
import math
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.initUI()

    def initUI(self):
        self.layout  = QGridLayout()
        self.display = QLineEdit(self)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(40)
        self.display.setAlignment(Qt.AlignRight)

        # self.layout.addWidget(widget, row, column, rowSpan, columnSpan)
        self.layout.addWidget(self.display, 0, 0, 1, 6) 

        buttons = [
            ['7', '8', '9', '/', 'C', 'AC'],
            ['4', '5', '6', '*', 'mod', 'M'],      
            ['1', '2', '3', '-', 'sqrt', 'abs'],     
            ['0', '.', '=', '+', 'log', 'ln'],       
             ['(', ')', '^', 'sin', 'cos', 'deg'],    
            ['tan', 'exp', 'pi', 'e', '!', 'floor']  
        ]

        for i, row in enumerate(buttons):
            for j, button in enumerate(row):
                btn = QPushButton(button, self)

                if button == '=':
                    btn.setObjectName('equal')
                elif button in ['C', 'AC']:
                    btn.setObjectName('clear')

                btn.clicked.connect(self.on_button_click)
                self.layout.addWidget(btn, i + 1, j)

        self.setLayout(self.layout)
        
        with open('style.css', 'r') as f:
            self.setStyleSheet(f.read())

    def on_button_click(self):
        button_text = self.sender().text()
        current_text = self.display.text()

        if button_text == 'C':
            self.display.setText(current_text[:-1]) # clear last character
        elif button_text == 'AC':
            self.display.clear()
        elif button_text == '=':
            try:
                expression =  ( current_text.replace('^', '**') 
                                        .replace('mod', '%') 
                                        .replace('pi', str(math.pi)) 
                                        .replace('e', str(math.e)) 
                                        .replace('sqrt', 'math.sqrt') 
                                        .replace('log', 'math.log10') 
                                        .replace('ln', 'math.log') 
                                        .replace('sin', 'math.sin') 
                                        .replace('cos', 'math.cos') 
                                        .replace('tan', 'math.tan') 
                                        .replace('exp', 'math.exp') 
                                        .replace('abs', 'abs') 
                                        .replace('floor', 'math.floor')
                )

                if '!' in expression:
                    expr = expression.replace('!', '')
                    result = math.factorial(int(eval(expr)))
                else:
                    result = eval(expression)

                self.display.setText(str(result))
                self.last_result = result 
            except:
                self.display.setText("Error")
        elif button_text == 'M':
            self.display.setText(current_text + str(getattr(self, 'last_result', '')))
        else:
            self.display.setText(current_text + button_text)



if __name__ == "__main__":
    app = QApplication([])
    window = Calculator()
    window.show()
    sys.exit(app.exec_())