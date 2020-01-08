#!/usr/bin/env python
# -*- coding! utf-8 -*-

"""
Just for fun
author: allenx
"""

import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QTableWidgetItem, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
from window.window import Ui_Form

NAME_LIST = ['sophia he', 'dora qiu', 'amber wei', 'lou lu', 'rachel zhuo', 'gavin chen',
             'molly wang', 'helena xu', 'sadie wen', 'simona zhang', 'arthur shu', 'marian chen',
             'alisa tang', 'allen xia', 'rebecca luo', 'cristiney zhang', 'travis zou', 'cecil xu',
             'hermona fang', 'ellie ai', 'debbie ye', 'perla qiu', 'poppy wu', 'trista hu',
             'chloe sha', 'scarlett yang', 'katty pu', 'olivia cui', 'gloria qiu', 'dylan dai',
             'kate zhang', 'stephen pan', 'cathy yang', 'cloud lei'
             ]

GROUP_LIST = []
THREAD_RUN = False
RESULT = False
SPEED = 0.05


class MainWindow(QWidget, Ui_Form):
    """Just for fun"""

    row = 0
    col = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.center()
        self.init_item()
        self.thread = WheelThread()
        self.timer = QTimer()

        self.StartButton.clicked.connect(self.wheel_run)
        self.ResetButton.clicked.connect(self.reset)
        self.thread.sin_out.connect(self.list_add)
        self.timer.timeout.connect(self.group_add)

    def center(self):

        screen_size = QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        self.move(
            int((screen_size.width() - window_size.width()) / 2),
            int((screen_size.height() - window_size.height()) / 2)
        )

    def init_item(self):

        for i, name in enumerate(NAME_LIST):
            NAME_LIST[i] = name.title()

            item = QListWidgetItem(NAME_LIST[i])
            item.setTextAlignment(Qt.AlignCenter)
            item.setFont(QFont('Fixed', 18))
            self.listWidget.addItem(item)

        select_item = self.listWidget.item(15)
        select_item.setFont(QFont('Fixed', 35))
        select_item.setSelected(True)

    def list_add(self, file_inf):

        item = QListWidgetItem(file_inf)
        item.setTextAlignment(Qt.AlignCenter)
        self.listWidget.insertItem(0, item)
        self.listWidget.scrollToTop()

        select_item = self.listWidget.item(15)
        select_item.setSelected(True)
        select_item.setFont(QFont('Fixed', 35))
        self.listWidget.item(16).setFont(QFont('Fixed', 18))

    def wheel_run(self):

        global THREAD_RUN, SPEED, RESULT

        if self.StartButton.text() == '开始':
            self.StartButton.setText('停止')

            THREAD_RUN = True
            SPEED = 0.05
            self.thread.start()
        else:
            THREAD_RUN = False
            RESULT = False

            self.StartButton.setText('禁')
            self.StartButton.setEnabled(False)
            self.timer.start(1000)

    def group_add(self):

        global RESULT

        if RESULT:
            self.StartButton.setEnabled(True)
            self.StartButton.setText('开始')

            while self.listWidget.item(40):
                self.listWidget.takeItem(40)

            text = self.listWidget.selectedItems()[0].text()
            NAME_LIST.remove(text)
            GROUP_LIST.append(text)

            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(self.row, self.col, item)
            self.tableWidget.resizeColumnsToContents()

            if self.col:
                self.col += 1
            else:
                self.row += 1
                self.col -= 1

            self.timer.stop()

    def reset(self):

        if len(GROUP_LIST) == 0:
            QMessageBox.about(self, "莫清了唉， 乖乖", "都没东西了你在清你伟大的母亲大人么？")
        else:
            NAME_LIST.extend(GROUP_LIST)
            GROUP_LIST.clear()
            self.tableWidget.clearContents()
            self.row = self.col = 0

    def closeEvent(self, event):

        reply = QMessageBox.information(self,
                                        "男人都是臭不要脸的",
                                        "玩完人家就要走，果然男人都是大猪蹄子\r\n你确定不玩了么？",
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No
                                        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class WheelThread(QThread):

    sin_out = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.num = 0

    def run(self):

        global THREAD_RUN, SPEED, RESULT
        length = len(NAME_LIST)

        while True:
            list_str = NAME_LIST[self.num % length]
            self.sin_out.emit(list_str)
            if not THREAD_RUN:
                SPEED *= 1.05
                if SPEED > 0.6:
                    break
            time.sleep(SPEED)
            self.num += 1

        self.num %= length
        RESULT = True


if __name__ == "__main__":
    APP = QApplication(sys.argv)
    FORM = MainWindow()
    FORM.show()
    sys.exit(APP.exec_())
