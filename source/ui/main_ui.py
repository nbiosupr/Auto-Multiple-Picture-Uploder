from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel

from .update_task_dialog_ui import UpdateTaskDialog
from .add_task_dialog_ui import AddTaskDialog
from .delete_check_ui import DeleteCheckDialog

from ampu import Task

import sys


class MainWindow(object):
    def __init__(self, task_manager):
        self.ui = None
        self.task_manager = task_manager

        self.selected_task = None

        app = QApplication(sys.argv)
        self.set_ui()
        self.show()
        app.exec_()

    def set_ui(self):
        self.ui = uic.loadUi(".\\ui\\qt_ui\\main.ui")
        ui = self.ui

        ui.add_task_button.clicked.connect(self.add_task_click_slot)
        ui.run_button.clicked.connect(self.run_click_slot)
        ui.update_task_button.clicked.connect(self.update_task_click_slot)
        ui.delete_task_button.clicked.connect(self.delete_task_click_slot)

    def show(self):
        self.ui.show()

    def run_click_slot(self):
        self.task_manager.execute()

    def add_task_click_slot(self):
        add_task_dialog = AddTaskDialog()
        if add_task_dialog.is_cancel:
            return
        my_task = add_task_dialog.my_task

        self.task_manager.add_task_with_task(my_task)
        self.refresh_list_view()

    def update_task_click_slot(self):
        update_task_dialog = UpdateTaskDialog(self.selected_task)
        if update_task_dialog.is_cancel:
            return
        my_task = update_task_dialog.my_task

        self.task_manager.update_task_with_task(my_task)

    def delete_task_click_slot(self):
        delete_task_dialog = DeleteCheckDialog(self.selected_task)
        if delete_task_dialog.is_cancel:
            return

        self.task_manager.delete_task(self.selected_task)
        self.refresh_list_view()

    def task_list_click_slot(self):
        ui = self.ui
        my_task = self.task_manager.read_task(self.selected_task)

        ui.cafe_path_edit.setText(my_task.cafe_path)
        ui.menu_name_edit.setText(my_task.menu_name)
        ui.post_title_edit.setText(my_task.post_title)
        ui.images_path_edit.setText(my_task.images_path)
        ui.number_to_divide_edit.setText(str(my_task.number_to_divide))

        ui.right_frame.setEnabled(True)
        ui.run_button.setEnabled(True)

    def refresh_list_view(self):
        task_name_list = self.task_manager.get_task_name_list()
        model = QStandardItemModel()
        for task_name in task_name_list:
            model.appendRow(QStandardItem(task_name))
        self.ui.task_list_view.setModel(model)

