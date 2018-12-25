from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import sys


class LoginWindow(object):
    def __init__(self):
        self.ui = None

        app = QApplication(sys.argv)
        self.set_ui()
        self.show()
        app.exec_()

    def set_ui(self):
        self.ui = uic.loadUi(".\\qt_ui\\login.ui")

    def show(self):
        self.ui.show()

    def naver_login_click_slot(self):
        pass

main_window = LoginWindow()
