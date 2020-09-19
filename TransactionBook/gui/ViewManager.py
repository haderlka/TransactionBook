from PySide2.QtWidgets import QTableWidgetItem
from TransactionBook.gui.MainWindow import MainWindow


class ViewManager:
    def __init__(self):
        self.main_window = MainWindow(self)
        self.send_callbacks = True

    def set_transaction_table(self, column_headings, data):
        self.send_callbacks = False
        num_rows = len(data)
        num_columns = len(data[0])
        assert num_columns == len(column_headings), \
            "ViewManager.set_transaction_table: Number of column headings must match the columns in data"

        table = self.main_window.transaction_widget.table
        table.setColumnCount(num_columns)
        table.setRowCount(num_rows)
        table.setHorizontalHeaderLabels(column_headings)

        for row in range(num_rows):
            for column in range(num_columns):
                cell_content = QTableWidgetItem(data[row][column])
                table.setItem(row, column, cell_content)
        self.send_callbacks = True

    def cb_transaction_changed(self, item):
        if self.send_callbacks:
            new_content = item.text()
            row = item.row()
            print(f"Cell changed: {item.text()}, Row: {item.row()}")