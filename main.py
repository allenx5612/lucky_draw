#!/usr/bin/env python
# -*- coding! utf-8 -*-

"""
Just for fun
author: allenx
"""

import sys
import os
# fix pyinstaller unable to find Qt5Core.dll on PATH issue
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

import time
import math
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QTableWidgetItem, QListWidgetItem, QMessageBox, \
    QInputDialog
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
    num = 0
    font = ''
    prize = {}
    prize_text = ''

    def __init__(self):
        super().__init__()
        if sys.platform == 'win32':
            self.font = 'Microsoft YaHei UI'
        elif sys.platform == 'linux':
            self.font = 'Contarell'

        self.setupUi(self)
        self.center()
        self.init_item()
        self.thread = WheelThread()
        self.timer = QTimer()
        self.tableWidget.setCurrentItem(None)
        self.listWidget.scrollToTop()

        self.StartButton.clicked.connect(self.wheel_run)
        self.groupButton.clicked.connect(self.mode_select)
        self.drawButton.clicked.connect(self.mode_select)
        self.ResetButton.clicked.connect(self.reset_pop)
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
            item.setFont(QFont(self.font, 18, 75))
            self.listWidget.addItem(item)

        select_item = self.listWidget.item(13)
        select_item.setFont(QFont(self.font, 35, 75))
        select_item.setSelected(True)

    def list_add(self, file_inf):

        item = QListWidgetItem(file_inf)
        item.setTextAlignment(Qt.AlignCenter)
        self.listWidget.insertItem(0, item)
        self.listWidget.scrollToTop()

        select_item = self.listWidget.item(13)
        select_item.setSelected(True)
        select_item.setFont(QFont(self.font, 35, 75))
        self.listWidget.item(14).setFont(QFont(self.font, 18, 75))

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

    def mode_select(self):

        num = 0
        row = 0
        sender = self.sender()
        chinum = ['一', '二', '三', '四', '五', '六']
        if sender.text() == "抽奖":
            while True:
                prize, ok = QInputDialog.getText(self,
                                                 '奖项',
                                                 '要给奖奖取个什么名字呢？ 点击取消退出哦！',
                                                 text='神秘大奖' + chinum[num % len(chinum)]
                                                 )
                if not ok:
                    break

                count, ok = QInputDialog.getInt(self,
                                                '名额',
                                                '要给多少个人人呢? 点击取消重新设置奖项哦!',
                                                10
                                                )
                if ok:
                    if row == 0:
                        self.reset()

                    self.prize[prize] = count

                    count = math.ceil(count / 2)
                    self.tableWidget.setRowCount(self.tableWidget.rowCount() + count)
                    item = QTableWidgetItem(prize)
                    self.tableWidget.setItem(row, 0, item)
                    self.tableWidget.resizeColumnsToContents()
                else:
                    continue
                num += 1
                row += count + 1

        elif sender.text() == '分组':
            count, ok = QInputDialog.getInt(self,
                                            '组数',
                                            '要分多少个组组呢?',
                                            6
                                            )
            if ok:
                self.reset()
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + count)

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

            if self.prize:

                print(self.row, self.col)
                next_item = self.tableWidget.item(self.row + 1, 0)

                if next_item:
                    count = self.prize[self.prize_text]
                    if count % 2 == 1 and self.col:
                        self.row += 1
                        self.col -= 1

                print(self.row, self.col)
                cur_item = self.tableWidget.item(self.row, self.col)
                if cur_item:
                    self.prize_text = cur_item.text()
                    if cur_item.text() in self.prize:
                        self.row += 1
                        print(cur_item.text())

            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(self.row, self.col, item)
            self.tableWidget.resizeColumnsToContents()

            if not self.col:
                self.col += 1
            else:
                self.row += 1
                self.col -= 1

            self.timer.stop()

    def reset(self):

        NAME_LIST.extend(GROUP_LIST)
        GROUP_LIST.clear()
        self.prize.clear()
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(20)
        self.row = self.col = self.num = 0

    def reset_pop(self):

        reply = QMessageBox.information(self,
                                        "你确定?",
                                        "清理这么重大的事，你考虑好了么？",
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No
                                        )
        if reply == QMessageBox.Yes:
            self.reset()

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
                if SPEED > 0.4:
                    break
            time.sleep(SPEED)
            self.num += 1

        self.num %= length
        RESULT = True


if __name__ == "__main__":
    APP = QApplication(sys.argv)
    FORM = MainWindow()
    QSS = '''
            QWidget {
                background-color: black;
                color: orange
            }
            QListWidget {
                background-color: rgb(157, 157, 157);
                color: white;
                border: black
            }
            QTableWidget {
                background-color: rgb(157, 157, 157);
                color: white
            }
            QPushButton {
                background-color: orange;
                color: black 
            }
            QPushButton#StartButton, #groupButton {
                background-color: rgb(46, 179, 152);
                color: white
            }
            QPushButton#ResetButton, #drawButton {
                background-color: orange;
                color: black 
            }
            
    '''
    FORM.setStyleSheet(QSS)

    FORM.show()
    sys.exit(APP.exec_())
