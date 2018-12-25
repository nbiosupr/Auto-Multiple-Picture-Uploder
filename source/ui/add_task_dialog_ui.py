from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import sys


class AddTaskDialog(object):
    def __init__(self):
        self.ui = None

        app = QApplication(sys.argv)
        self.set_ui()
        self.show()
        app.exec_()

    def set_ui(self):
        self.ui = uic.loadUi(".\\qt_ui\\add_task_dialog.ui")

    def show(self):
        self.ui.show()

    def ok_button_click_slot(self):
        pass

main_window = AddTaskDialog()