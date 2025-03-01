import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QDialog


class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.coffee_id = coffee_id
        if self.coffee_id:
            self.load_coffee_data()
        self.saveButton.clicked.connect(self.save_data)

    def load_coffee_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee WHERE id = ?", (self.coffee_id,))
        data = cursor.fetchone()
        conn.close()
        if data:
            self.nameEdit.setText(data[1])
            self.roastLevelEdit.setText(data[2])
            self.groundOrWholeEdit.setText(data[3])
            self.descriptionEdit.setText(data[4])
            self.priceEdit.setText(str(data[5]))
            self.packageSizeEdit.setText(str(data[6]))

    def save_data(self):
        name = self.nameEdit.text()
        roast_level = self.roastLevelEdit.text()
        ground_or_whole = self.groundOrWholeEdit.text()
        description = self.descriptionEdit.text()
        price = float(self.priceEdit.text())
        package_size = int(self.packageSizeEdit.text())

        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()
        if self.coffee_id:
            cursor.execute('''
                UPDATE coffee SET name=?, roast_level=?, ground_or_whole=?, description=?, price=?, package_size=?
                WHERE id=?
            ''', (name, roast_level, ground_or_whole, description, price, package_size, self.coffee_id))
        else:
            cursor.execute('''
                INSERT INTO coffee (name, roast_level, ground_or_whole, description, price, package_size)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, roast_level, ground_or_whole, description, price, package_size))
        conn.commit()
        conn.close()
        self.accept()


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.load_data()
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

    def load_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        data = cursor.fetchall()
        conn.close()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(7)
        headers = ["ID", "Название", "Степень обжарки", "Форма", "Описание", "Цена", "Объем"]
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

    def add_coffee(self):
        dialog = AddEditCoffeeForm(self)
        if dialog.exec():
            self.load_data()

    def edit_coffee(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            coffee_id = int(self.tableWidget.item(selected_row, 0).text())
            dialog = AddEditCoffeeForm(self, coffee_id)
            if dialog.exec():
                self.load_data()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
