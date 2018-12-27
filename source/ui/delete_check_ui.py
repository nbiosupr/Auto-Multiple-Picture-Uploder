from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import sys


class DeleteCheckDialog(object):
    def __init__(self, task_name):
        self.ui = None
        self.is_cancel = True

        self.task_name = task_name

        self.set_ui()
        self.show()

    def set_ui(self):
        self.ui = uic.loadUi(".\\ui\\qt_ui\\delete_check_dialog.ui")
        self.ui.task_name_edit.setText(self.task_name)

        ui = self.ui

        ui.ok_button.clicked.connect(self.ok_button_click_slot)
        ui.cancel_button.clicked.connect(self.cancel_button_click_slot)

    def show(self):
        self.ui.show()

    def ok_button_click_slot(self):
        self.is_cancel = False
        self.ui.close()

    def cancel_button_click_slot(self):
        self.is_cancel = True
        self.ui.close()
