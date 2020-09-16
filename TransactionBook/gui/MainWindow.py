#!/usr/bin/env python
import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QTabWidget, QWidget
from TransactionBook.gui.TransactionWidget import TransactionWidget


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Window settings
        self.window_title = "Transaction Book"
        self.setWindowTitle(self.window_title)
        self.setMinimumSize(600, 400)
        self.resize(1500, 900)
        # Initialization of MainWindow elements
        self.init_menu_bar()
        self.init_central_widget()

    def init_menu_bar(self):
        menu_bar = self.menuBar()
        # File Menu
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(QAction("New File", self, triggered=self.new_file))
        file_menu.addAction(QAction("Open...", self, triggered=self.open_file))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Save", self, triggered=self.save_file))
        file_menu.addAction(QAction("Save As...", self, triggered=self.save_as_file))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Close File", self, triggered=self.close_file))
        file_menu.addAction("Exit", QApplication.quit)

    def init_central_widget(self):
        tab_widget = QTabWidget()
        transaction_tab = TransactionWidget()  # QWidget will be TransactionWidget
        account_tab = QWidget()

        tab_widget.addTab(transaction_tab, "Transactions")
        tab_widget.addTab(account_tab, "Accounts")

        self.setCentralWidget(tab_widget)


    def new_file(self):
        print("New File")

    def open_file(self):
        print("Open File")

    def save_file(self):
        print("Save")

    def save_as_file(self):
        print("Save As")

    def close_file(self):
        print("Close File")


if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec_())