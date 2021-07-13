import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

DB_NAME = "films1.db"


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI3.ui", self)
        self.con = sqlite3.connect(DB_NAME)
        self.update_result()
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.edit_film)
        self.pushButton_3.clicked.connect(self.delete_elem)
        self.pushButton_4.clicked.connect(self.add_film)
        self.modified = {}
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        query = "SELECT * FROM films ORDER BY id"
        result = cur.execute(query).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название фильма', 'Год выпуска', 'Жанр', 'Продолжительность'])
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def add_film(self):
        dialog = AddFilmWidget(self)
        dialog.show()

    def edit_film(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if not ids:
            self.statusBar().showMessage('Ничего не выбрано')
            return
        else:
            self.statusBar().showMessage('')
        dialog = AddFilmWidget(self, film_id=ids[0])
        dialog.show()

    def delete_elem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы с id " + ",".join(ids),
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute("DELETE FROM films WHERE id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)
            self.con.commit()
            self.update_result()


class AddFilmWidget(QMainWindow):
    def __init__(self, parent=None, film_id=None):
        super().__init__(parent)
        self.con = sqlite3.connect(DB_NAME)
        self.params = {}
        uic.loadUi('addFilm.ui', self)
        self.selectGenres()
        self.film_id = film_id
        if film_id is not None:
            self.pushButton.clicked.connect(self.edit_elem)
            self.pushButton.setText('Отредактировать')
            self.setWindowTitle('Редактирование записи')
            self.get_elem()

    def get_elem(self):
        cur = self.con.cursor()
        item = cur.execute(
            f"SELECT f.id, f.title, f.year, g.title, f.duration FROM films as f JOIN genres as g ON g.id = f.genre WHERE f.id = {self.film_id}").fetchone()
        self.title.setPlainText(item[1])
        self.year.setPlainText(str(item[2]))
        self.comboBox.setCurrentText(item[3])
        self.duration.setPlainText(str(item[4]))

    def selectGenres(self):
        req = "SELECT * from genres"
        cur = self.con.cursor()
        for value, key in cur.execute(req).fetchall():
            self.params[key] = value
        self.comboBox.addItems(list(self.params.keys()))

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    sys.exit(app.exec())