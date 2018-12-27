from PyQt5.QtWidgets import *
from .login_ui import LoginWindow
from .main_ui import MainWindow

import sys

class UiController:
    def __init__(self):
        self.__app = QApplication(sys.argv)
        self.__core = None
        self.login_ui = None
        self.main_ui = None

    def set_core(self, core):
        self.__core = core

    def start(self):
        self.login_ui = LoginWindow(self.__core)
        print('login_ui 닫혔어용')
        if not self.__core.is_login():
            exit()
        self.main_ui = MainWindow(self.__core)


