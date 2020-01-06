#!/usr/bin/env python
# -*- coding! utf-8 -*-

"""
Main window to manage and run RPA projects
author: allenx
"""

import os
import sys
import time
from os.path import join, expanduser, basename, exists
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QPushButton, QCheckBox, \
    QTableWidgetItem, QFileDialog, QAbstractItemView, QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from window.window import Ui_Form


class MainWindow(QWidget, Ui_Form):

    """Main window class used to manage over RPA_projects."""

    num = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.center()
        self.init_item()
        self.thread = WheelThread()
        self.StartButton.clicked.connect(self.wheel_run)
        self.thread.sin_out.connect(self.list_add)
        self.ResetButton.clicked.connect(self.print_selected)

    def center(self):

        screen_size = QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        self.move(
            int((screen_size.width() - window_size.width()) / 2),
            int((screen_size.height() - window_size.height()) / 2)
        )

    def init_item(self):

        for i in range(40):
            item = QListWidgetItem('item {}'.format(i))
            item.setTextAlignment(Qt.AlignCenter)
            item.setFont(QFont('Fixed', 18))
            self.listWidget.addItem(item)

        select_item = self.listWidget.item(18)
        select_item.setFont(QFont('Fixed', 25))
        select_item.setSelected(True)

    def list_add(self, file_inf):

        item = QListWidgetItem(file_inf)
        item.setTextAlignment(Qt.AlignCenter)
        self.listWidget.insertItem(0, item)

        select_item = self.listWidget.item(18)
        select_item.setFont(QFont('Fixed', 25))
        self.listWidget.item(19).setFont(QFont('Fixed', 18))
        select_item.setSelected(True)

        remove_item = self.listWidget.item(40)
        self.listWidget.removeItemWidget(remove_item)

    def wheel_run(self):

        self.StartButton.setText('stop')
        self.thread.start()

    def print_selected(self):

        print(self.listWidget.selectedItems()[0].text())


class WheelThread(QThread):

    sin_out = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.num = 0

    def run(self):
        for i in range(1000):
            list_str = 'Item {}'.format(i)
            self.sin_out.emit(list_str)
            time.sleep(0.05)


if __name__ == "__main__":
    APP = QApplication(sys.argv)
    FORM = MainWindow()
    FORM.show()
    sys.exit(APP.exec_())

