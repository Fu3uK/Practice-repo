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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    sys.exit(app.exec())