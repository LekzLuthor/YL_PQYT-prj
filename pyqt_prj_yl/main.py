import sys
from Parcing import update
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.CONV_WIN = ConvertWindow()
        self.to_convert_btn.clicked.connect(self.to_convert_window)

    def to_convert_window(self):
        self.CONV_WIN.show()


class ConvertWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('convertor_window.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
