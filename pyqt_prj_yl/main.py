import sys
from Parcing import update
from DopWindows import ConvertWindow
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer, QTime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)

        self.currencies = ['Рубль', 'Евро', 'Доллар США', 'Японская иена',
                           'Фунт стерлингов', 'Швейцарский франк', 'Украинская гривна']
        self.headlines = ['Валюта', 'Предложение', 'Пред. закрытие',
                          '%', 'Абсол. значение', 'Время']
        self.is_jpy_error_checker = True

        self.CONV_WIN = ConvertWindow()
        self.to_convert_btn.clicked.connect(self.to_convert_window)
        self.update_curr.clicked.connect(self.load_curr_table_data)
        self.replace_btn_1.clicked.connect(self.replace_table)
        self.replace_btn_2.clicked.connect(self.replace_table)
        self.replace_btn_3.clicked.connect(self.replace_table)

        self.hide_ft.clicked.connect(self.hide_table)
        self.hide_st.clicked.connect(self.hide_table)
        self.hide_tt.clicked.connect(self.hide_table)
        self.hide_fft.clicked.connect(self.hide_table)
        self.show_ft.clicked.connect(self.show_table)
        self.show_st.clicked.connect(self.show_table)
        self.show_tt.clicked.connect(self.show_table)
        self.show_fft.clicked.connect(self.show_table)

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

        self.headlines[0] = self.currencies[3]
        self.JPY_table.setColumnCount(len(self.headlines))
        self.JPY_table.setHorizontalHeaderLabels(self.headlines)
        self.JPY_table.setRowCount(4)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        update()
        self.load_curr_table_data()

    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.time_show.setText(label_time)

    def show_table(self):
        if self.sender().objectName() == 'show_ft':
            self.RUB_table.show()
        if self.sender().objectName() == 'show_st':
            self.EUR_table.show()
            self.rep_val_1.show()
            self.replace_btn_1.show()
            if self.rep_val_1.currentText() == 'JPY':
                self.JPY_11.setText('(100:1)')
                self.JPY_12.setText('(100:1)')
            elif self.rep_val_1.currentText() == 'CHF':
                self.CHF_1.setText('(100:1)')
        if self.sender().objectName() == 'show_tt':
            self.USD_table.show()
            self.rep_val_2.show()
            self.replace_btn_2.show()
            if self.rep_val_2.currentText() == 'JPY':
                self.JPY_21.setText('(100:1)')
                self.JPY_22.setText('(100:1)')
            elif self.rep_val_2.currentText() == 'CHF':
                self.CHF_2.setText('(100:1)')
        if self.sender().objectName() == 'show_fft':
            self.JPY_table.show()
            self.rep_val_3.show()
            self.replace_btn_3.show()
            if self.rep_val_3.currentText() == 'JPY':
                self.JPY_31.setText('(100:1)')
                self.JPY_32.setText('(100:1)')
            elif self.rep_val_3.currentText() == 'CHF':
                self.CHF_3.setText('(100:1)')
            if self.is_jpy_error_checker:
                self.JPY_31.setText('(100:1)')
                self.JPY_32.setText('(100:1)')

    def hide_table(self):
        if self.sender().objectName() == 'hide_ft':
            self.RUB_table.hide()
        if self.sender().objectName() == 'hide_st':
            self.EUR_table.hide()
            self.rep_val_1.hide()
            self.replace_btn_1.hide()
            if self.rep_val_1.currentText() == 'JPY' or self.rep_val_1.currentText() == 'CHF':
                self.JPY_11.setText('')
                self.JPY_12.setText('')
                self.CHF_1.setText('')
        if self.sender().objectName() == 'hide_tt':
            self.USD_table.hide()
            self.rep_val_2.hide()
            self.replace_btn_2.hide()
            if self.rep_val_2.currentText() == 'JPY' or self.rep_val_2.currentText() == 'CHF':
                self.JPY_21.setText('')
                self.JPY_22.setText('')
                self.CHF_2.setText('')
        if self.sender().objectName() == 'hide_fft':
            self.JPY_table.hide()
            self.rep_val_3.hide()
            self.replace_btn_3.hide()
            if self.rep_val_3.currentText() == 'JPY' or self.rep_val_3.currentText() == 'CHF':
                self.JPY_31.setText('')
                self.JPY_32.setText('')
                self.CHF_3.setText('')
            if self.is_jpy_error_checker:
                self.JPY_31.setText('')
                self.JPY_32.setText('')

    def to_convert_window(self):
        self.CONV_WIN.show()

    def load_curr_table_data(self):
        f = open('url_data_values.txt', 'w')
        f.close()
        update()
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
                if 17 < line_num < 22:
                    if alphabet.isdisjoint(line.lower()):
                        fp, sp = line.split('%')
                        line = ''.join([fp, sp])
                        dop_elem_counter = 0
                        for elem in line.split():
                            if elem == '(100:1)':
                                continue
                            else:
                                self.JPY_table.setItem(dop_row_counter, dop_elem_counter, QTableWidgetItem(str(elem)))
                                dop_elem_counter += 1
                        dop_row_counter += 1
                if dop_row_counter >= 4:
                    dop_row_counter = 0

    @staticmethod
    def replace_val_dp(new_value):
        start_file_line = 0
        end_file_line = 0
        if new_value == 'EUR':
            start_file_line = 7
            end_file_line = 12
        elif new_value == 'USD':
            start_file_line = 12
            end_file_line = 17
        elif new_value == 'JPY':
            start_file_line = 17
            end_file_line = 22
        elif new_value == 'GBP':
            start_file_line = 22
            end_file_line = 27
        elif new_value == 'CHF':
            start_file_line = 27
            end_file_line = 32
        elif new_value == 'UAH':
            start_file_line = 32
            end_file_line = 37
        return start_file_line, end_file_line

    def replace_table(self):
        dop_row_counter = 0
        if self.sender().objectName() == 'replace_btn_1':
            value = self.rep_val_1.currentText()
            if value != 'JPY' and value != 'CHF':
                start, end = self.replace_val_dp(value)
                with open('url_data_values.txt', 'r', encoding='utf-8') as file:
                    for line_num, line in enumerate(file.readlines()):
                        if start < line_num < end:
                            fp, sp = line.split('%')
                            line = ''.join([fp, sp])
                            for elem_num, elem in enumerate(line.split()):
                                self.EUR_table.setItem(dop_row_counter, elem_num, QTableWidgetItem(str(elem)))
                            dop_row_counter += 1
                    if dop_row_counter >= 4:
                        dop_row_counter = 0
                self.JPY_11.setText('')
                self.JPY_12.setText('')
                self.CHF_1.setText('')
            else:
                start, end = self.replace_val_dp(value)
                with open('url_data_values.txt', 'r', encoding='utf-8') as file:
                    for line_num, line in enumerate(file.readlines()):
                        if start < line_num < end:
                            fp, sp = line.split('%')
                            line = ''.join([fp, sp])
                            dop_elem_counter = 0
                            for elem in line.split():
                                if elem == '(100:1)':
                                    continue
                                else:
                                    self.EUR_table.setItem(dop_row_counter, dop_elem_counter,
                                                           QTableWidgetItem(str(elem)))
                                    dop_elem_counter += 1
                            dop_row_counter += 1
                    if dop_row_counter >= 4:
                        dop_row_counter = 0
                self.JPY_11.setText('')
                self.JPY_12.setText('')
                self.CHF_1.setText('')
                if value == 'JPY':
                    self.JPY_11.setText('(100:1)')
                    self.JPY_12.setText('(100:1)')
                elif value == 'CHF':
                    self.CHF_1.setText('(100:1)')

        if self.sender().objectName() == 'replace_btn_2':
            value = self.rep_val_2.currentText()
            if value != 'JPY' and value != 'CHF':
                start, end = self.replace_val_dp(value)
                with open('url_data_values.txt', 'r', encoding='utf-8') as file:
                    for line_num, line in enumerate(file.readlines()):
                        if start < line_num < end:
                            fp, sp = line.split('%')
                            line = ''.join([fp, sp])
                            for elem_num, elem in enumerate(line.split()):
                                self.USD_table.setItem(dop_row_counter, elem_num, QTableWidgetItem(str(elem)))
                            dop_row_counter += 1
                    if dop_row_counter >= 4:
                        dop_row_counter = 0
                self.JPY_21.setText('')
                self.JPY_22.setText('')
                self.CHF_2.setText('')
            else:
                start, end = self.replace_val_dp(value)
                with open('url_data_values.txt', 'r', encoding='utf-8') as file:
                    for line_num, line in enumerate(file.readlines()):
                        if start < line_num < end:
                            fp, sp = line.split('%')
                            line = ''.join([fp, sp])
                            dop_elem_counter = 0
                            for elem in line.split():
                                if elem == '(100:1)':
                                    continue
                                else:
                                    self.USD_table.setItem(dop_row_counter, dop_elem_counter,
                                                           QTableWidgetItem(str(elem)))
                                    dop_elem_counter += 1
                            dop_row_counter += 1
                    if dop_row_counter >= 4:
                        dop_row_counter = 0
                self.JPY_21.setText('')
                self.JPY_22.setText('')
                self.CHF_2.setText('')
                if value == 'JPY':
                    self.JPY_21.setText('(100:1)')
                    self.JPY_22.setText('(100:1)')
                elif value == 'CHF':
                    self.CHF_2.setText('(100:1)')

        if self.sender().objectName() == 'replace_btn_3':
            self.is_jpy_error_checker = False
            value = self.rep_val_3.currentText()
            if value != 'JPY' and value != 'CHF':
                start, end = self.replace_val_dp(value)
                with open('url_data_values.txt', 'r', encoding='utf-8') as file:
                    for line_num, line in enumerate(file.readlines()):
                        if start < line_num < end:
                            fp, sp = line.split('%')
                            line = ''.join([fp, sp])
                            for elem_num, elem in enumerate(line.split()):
                                self.JPY_table.setItem(dop_row_counter, elem_num, QTableWidgetItem(str(elem)))
                            dop_row_counter += 1
                    if dop_row_counter >= 4:
                        dop_row_counter = 0
                self.JPY_31.setText('')
                self.JPY_32.setText('')
                self.CHF_3.setText('')
            else:
                start, end = self.replace_val_dp(value)
                with open('url_data_values.txt', 'r', encoding='utf-8') as file:
                    for line_num, line in enumerate(file.readlines()):
                        if start < line_num < end:
                            fp, sp = line.split('%')
                            line = ''.join([fp, sp])
                            dop_elem_counter = 0
                            for elem in line.split():
                                if elem == '(100:1)':
                                    continue
                                else:
                                    self.JPY_table.setItem(dop_row_counter, dop_elem_counter,
                                                           QTableWidgetItem(str(elem)))
                                    dop_elem_counter += 1
                            dop_row_counter += 1
                    if dop_row_counter >= 4:
                        dop_row_counter = 0
                self.JPY_31.setText('')
                self.JPY_32.setText('')
                self.CHF_3.setText('')
                if value == 'JPY':
                    self.JPY_31.setText('(100:1)')
                    self.JPY_32.setText('(100:1)')
                elif value == 'CHF':
                    self.CHF_3.setText('(100:1)')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
