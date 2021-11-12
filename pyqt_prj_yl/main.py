import sys
from Parcing import update
from DopWindows import ConvertWindow
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        update()
        self.CONV_WIN = ConvertWindow()
        self.to_convert_btn.clicked.connect(self.to_convert_window)
        self.update_curr.clicked.connect(self.load_curr_table_data)
        self.load_curr_table_data()

    def to_convert_window(self):
        self.CONV_WIN.show()

    def load_curr_table_data(self):
        alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        currencies = ['Рубль', 'Евро', 'Доллар США', 'Японская иена',
                      'Фунт стерлингов', 'Швейцарский франк', 'Украинская гривна']
        headlines = ['Предложение', 'Пред. закрытие',
                     '%', 'Абсол. значение', 'Время']
        self.curr_table1.setColumnCount(len(headlines))
        self.curr_table1.setHorizontalHeaderLabels(headlines)
        self.curr_table1.setRowCount(6)

        self.curr_table2.setColumnCount(len(headlines))
        self.curr_table2.setHorizontalHeaderLabels(headlines)
        self.curr_table2.setRowCount(4)

        self.curr_table3.setColumnCount(len(headlines))
        self.curr_table3.setHorizontalHeaderLabels(headlines)
        self.curr_table3.setRowCount(4)

        with open('url_data_values.txt', 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file):
                if line_num < 7:
                    if alphabet.isdisjoint(line.lower()):
                        for elem_num, elem in enumerate(line):
                            self.curr_table1.setItem(line_num, elem_num, elem)


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


sys.excepthook = excepthook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
