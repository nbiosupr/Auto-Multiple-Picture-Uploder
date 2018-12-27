from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from ampu import Task

import sys


class AddTaskDialog(object):
    def __init__(self):
        self.ui = None
        self.is_cancel = True

        self.my_task = None
        try:
            self.set_ui()
        except Exception as e:
            print(e)
        self.show()

    def set_ui(self):
        self.ui = uic.loadUi(".\\ui\\qt_ui\\add_task_dialog.ui")

        ui = self.ui

        ui.file_control_button.clicked.connect(self.get_file_path_click_slot)
        ui.ok_button.clicked.connect(self.ok_button_click_slot)
        ui.cancel_button.clicked.connect(self.cancel_button_click_slot)

    def show(self):
        self.ui.exec()

    def ok_button_click_slot(self):
        ui = self.ui

        self.is_cancel = False


        task_title = ui.task_name_edit.text()
        cafe_path = ui.cafe_path_edit.text()
        menu_name = ui.board_name_edit.text()
        post_title = ui.post_title_edit.text()
        images_path = ui.images_path_edit.text()
        number_to_divide = int(ui.number_to_divide_edit.text())


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
        try:
            file_name = QFileDialog.getExistingDirectory(self.ui)
            self.ui.images_path_edit.setText(file_name)
        except Exception as e:
            print(e)
