from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import sys


class MainWindow(object):
    def __init__(self):
        self.ui = None

        self.set_ui()
        self.show()

    def set_ui(self):
        self.ui = uic.loadUi(".\\qt_ui\\main2.ui")

    def show(self):
        self.ui.show()

    def run_click_slot(self):
        pass

    def add_task_click_slot(self):
        pass

    def update_task_click_slot(self):
        pass

    def task_list_click_slot(self):
        pass


main_window = MainWindow()

