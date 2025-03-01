import sys

import sqlite3

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        data = cursor.fetchall()
        print(data)
        conn.close()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(6)
        headers = ["ID", "Название", "Степень обжарки", "Форма", "Описание", "Цена", "Объем"]
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())