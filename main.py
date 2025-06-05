import sys
from PySide6.QtWidgets import QApplication
from typing_game_gui import TypingGameWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingGameWindow()
    window.show()
    sys.exit(app.exec())
