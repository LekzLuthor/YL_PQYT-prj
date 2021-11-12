import sys
from Parcing import update
from DopWindows import ConvertWindow
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)

        self.currencies = ['Рубль', 'Евро', 'Доллар США', 'Японская иена',
                           'Фунт стерлингов', 'Швейцарский франк', 'Украинская гривна']
        self.headlines = ['Валюта', 'Предложение', 'Пред. закрытие',
                          '%', 'Абсол. значение', 'Время']

        self.CONV_WIN = ConvertWindow()
        self.to_convert_btn.clicked.connect(self.to_convert_window)
        self.update_curr.clicked.connect(self.load_curr_table_data)

        self.headlines[0] = self.currencies[0]
        self.RUB_table.setColumnCount(len(self.headlines))
        self.RUB_table.setHorizontalHeaderLabels(self.headlines)
        self.RUB_table.setRowCount(6)

        self.headlines[0] = self.currencies[1]
        self.EUR_table.setColumnCount(len(self.headlines))
        self.EUR_table.setHorizontalHeaderLabels(self.headlines)
        self.EUR_table.setRowCount(4)

        self.headlines[0] = self.currencies[2]
        self.USD_table.setColumnCount(len(self.headlines))
        self.USD_table.setHorizontalHeaderLabels(self.headlines)
        self.USD_table.setRowCount(4)

        update()
        self.load_curr_table_data()

    def to_convert_window(self):
        self.CONV_WIN.show()

    def load_curr_table_data(self):
        alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        dop_row_counter = 0
        with open('url_data_values.txt', 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file.readlines()):
                if line_num < 7:
                    if alphabet.isdisjoint(line.lower()):
                        fp, sp = line.split('%')
                        line = ''.join([fp, sp])
                        for elem_num, elem in enumerate(line.split()):
                            self.RUB_table.setItem(line_num - 1, elem_num, QTableWidgetItem(str(elem)))
                if 7 < line_num < 12:
                    if alphabet.isdisjoint(line.lower()):
                        fp, sp = line.split('%')
                        line = ''.join([fp, sp])
                        for elem_num, elem in enumerate(line.split()):
                            self.EUR_table.setItem(dop_row_counter, elem_num, QTableWidgetItem(str(elem)))
                        dop_row_counter += 1
                if 12 < line_num < 17:
                    if alphabet.isdisjoint(line.lower()):
                        fp, sp = line.split('%')
                        line = ''.join([fp, sp])
                        for elem_num, elem in enumerate(line.split()):
                            self.USD_table.setItem(dop_row_counter, elem_num, QTableWidgetItem(str(elem)))
                        dop_row_counter += 1
                if dop_row_counter >= 4:
                    dop_row_counter = 0

        self.RUB_table.resizeColumnsToContents()
        self.EUR_table.resizeColumnsToContents()
        self.USD_table.resizeColumnsToContents()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


sys.excepthook = excepthook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
