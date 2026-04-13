import sys
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout
from localLib.EasyPySide import BaseWindow

#from localLib.EasyPySide.Widgets import UniversalMediaContainer

class Window(BaseWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitleText("Главное окно")
        self.setWindowIconImage(r"resources\terminalWhite.ico")

        content = QVBoxLayout(self.contentArea)
        content.setContentsMargins(10, 10, 10, 10)
        content.addWidget(QLabel("Контент окна"))
        content.addWidget(QPushButton("Кнопка"))

def Main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    Main()