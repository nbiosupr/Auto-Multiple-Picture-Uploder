from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import sys

from ampu import Task


class UpdateTaskDialog(object):
    def __init__(self, task_name):
        self.ui = None

        self.is_cancel = True
        self.my_task = None
        self.task_name = task_name

        self.set_ui()
        self.show()

    def set_ui(self):
        self.ui = uic.loadUi(".\\ui\\qt_ui\\update_task_dialog.ui")
        self.ui.task_name_edit.setText(self.task_name)

        ui = self.ui

        ui.file_control_button.clicked.connect(self.get_file_path_click_slot)
        ui.ok_button.clicked.connect(self.ok_button_click_slot)
        ui.cancel_button.clicked.connect(self.cancel_button_click_slot)

    def show(self):
        self.ui.exec()

    def ok_button_click_slot(self):
        ui = self.ui

        self.is_cancel = False

        task_title = ui.task_name_edit.toPlainText()
        cafe_path = ui.cafe_path_edit.toPlainText()
        menu_name = ui.board_name_edit.toPlainText()
        post_title = ui.post_title_edit.toPlainText()
        images_path = ui.images_path.toPlainText()
        number_to_divide = int(ui.number_to_divide_edit.toPlainText())

        self.my_task = Task(task_title=task_title,
                            cafe_path=cafe_path,
                            menu_name=menu_name,
                            post_title=post_title,
                            images_path=images_path,
                            number_to_divide=number_to_divide)

        self.ui.close()

    def cancel_button_click_slot(self):
        self.is_cancel = True
        self.ui.close()

    def get_file_path_click_slot(self):
        file_name = QFileDialog.getOpenFileName(self)
        self.ui.images_path.setText(file_name[0])
