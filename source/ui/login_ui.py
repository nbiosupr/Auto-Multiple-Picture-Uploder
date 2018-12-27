from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import sys


class LoginWindow(object):
    def __init__(self, task_manager):
        self.ui = None
        self.task_manager = task_manager

        app = QApplication(sys.argv)
        self.set_ui()
        self.show()
        app.exec_()

    def set_ui(self):
        self.ui = uic.loadUi(".\\ui\\qt_ui\\login.ui")
        ui = self.ui
        ui.naver_login_button.clicked.connect(self.naver_login_click_slot)

    def show(self):
        self.ui.show()

    def naver_login_click_slot(self):
        self.task_manager.naver_login()
        if self.task_manager.is_login():
            self.ui.close()
