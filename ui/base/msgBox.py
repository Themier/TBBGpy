import sys, random, time
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QStackedLayout,
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
    QDesktopWidget
)
from PyQt5.QtGui import QPalette, QColor, QFont, QPixmap, QImage
from typing import List, Dict, Callable


class MsgBox(QLabel):
    '''
    '''

    def __init__(self, wordPixelSize:int, parent=None, flags=Qt.WindowFlags()):
        '''
        '''
        super().__init__(parent, flags)
        font:QFont = self.font()
        font.setBold(True)
        font.setPixelSize(wordPixelSize)
        font.setFamily("simsun")
        self.setFont(font)
        palette:QPalette = self.palette()
        palette.setColor(QPalette.WindowText, QColor("gray"))
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setWordWrap(True)
        self.setAutoFillBackground(True)

        self.typing = False
        
        self.msgs:List[str] = []
        self.currentMsg = ''
        self.currentMsgWordIndex = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.__UpdateCurrentMsg)
        self.msgWordTimeSep = 50
        self.msgStagnateTime = 200

        self.overAction:Callable = None

        return


    def AddMsg(self, msg:str):
        '''
        '''
        self.msgs.append(msg)

        return


    def ShowMsgs(self):
        '''
        '''
        self.typing = True
        if len(self.msgs) == 0:
            time.sleep(self.msgStagnateTime / 1000.0)
            self.typing = False
            if self.overAction != None:
                self.overAction()
            return
        self.currentMsg = self.msgs.pop(0)
        self.currentMsgWordIndex = 0
        self.__UpdateCurrentMsg()
        self.timer.start(self.msgWordTimeSep)

        return


    def __UpdateCurrentMsg(self, rollToNext=True):
        '''
        '''
        n = len(self.currentMsg)
        if self.currentMsgWordIndex == n:
            self.timer.stop()
            time.sleep(self.msgStagnateTime / 1000.0)
            self.ShowMsgs()
        else:
            self.currentMsgWordIndex += 1
            self.setText(self.currentMsg[:self.currentMsgWordIndex])

        return