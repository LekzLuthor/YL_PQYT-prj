import sys
import requests
from Parcing import update
from PyQt5 import uic
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem


class ConvertWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('convertor_window.ui', self)
        self.accept_button.clicked.connect(self.convert)
        self.replace_btn.clicked.connect(self.replace)

    # Функция получает на вход валют из которой нужно конвертировать, и валюту в которую нужно конвертировать
    # и возвращает их соотношение
    @staticmethod
    def get_data(from_cur, to_cur):
        alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        if from_cur == to_cur:
            return 1
        with open('url_data_values.txt', encoding='utf-8') as file:
            if to_cur == 'RUB':
                for line in file.readlines():
                    if from_cur in line.split()[0].split('/')[0]:
                        return float(line.split()[1].replace(',', '.'))
            if from_cur == 'RUB':
                for line in file.readlines():
                    if to_cur in line.split()[0].split('/')[0] and from_cur in line.split()[0].split('/')[1]:
                        return round((1 / float(line.split()[1].replace(',', '.'))), 4)
            elif from_cur == 'EUR':
                for line in file.readlines():
                    if alphabet.isdisjoint(line.lower()):
                        if to_cur in line.split()[0].split('/')[1] and from_cur in line.split()[0].split('/')[0]:
                            return float(line.split()[1].replace(',', '.'))
            elif from_cur == 'USD':
                for line in file.readlines():
                    if alphabet.isdisjoint(line.lower()):
                        if to_cur in line.split()[0].split('/')[1] and from_cur in line.split()[0].split('/')[0]:
                            return float(line.split()[1].replace(',', '.'))
            elif from_cur == 'JPY':
                for line in file.readlines():
                    if alphabet.isdisjoint(line.lower()):
                        if to_cur in line.split()[0].split('/')[1] and from_cur in line.split()[0].split('/')[0]:
                            if str(line.split()[1]) == '(100:1)':
                                return float(line.split()[2].replace(',', '.'))
                            else:
                                return float(line.split()[1].replace(',', '.'))
            elif from_cur == 'GBP':
                for line in file.readlines():
                    if alphabet.isdisjoint(line.lower()):
                        if to_cur in line.split()[0].split('/')[1] and from_cur in line.split()[0].split('/')[0]:
                            return float(line.split()[1].replace(',', '.'))
            elif from_cur == 'CHF':
                for line in file.readlines():
                    if to_cur in line.split()[0].split('/')[0] and from_cur in line.split()[0].split('/')[1]:
                        if str(line.split()[1]) == '(100:1)':
                            return round((1 / float(line.split()[2].replace(',', '.'))), 4)
                        else:
                            return round((1 / float(line.split()[1].replace(',', '.'))), 4)
            elif from_cur == 'UAH':
                for line in file.readlines():
                    if to_cur in line.split()[0].split('/')[0] and from_cur in line.split()[0].split('/')[1]:
                        return round((1 / float(line.split()[1].replace(',', '.'))), 4)

    # Конвертация валют
    def convert(self):
        first_value_count = self.first_count.value()
        first_value = self.first_value.currentText()
        second_value = self.second_value.currentText()
        exchange = self.get_data(first_value, second_value)
        self.second_count.setValue(float(first_value_count * exchange))

    # Функция меняет значения местами, привязана к кнопке посередине
    def replace(self):
        first_value_count = self.first_count.value()
        second_value_count = self.second_count.value()
        self.first_count.setValue(second_value_count)
        self.second_count.setValue(first_value_count)
