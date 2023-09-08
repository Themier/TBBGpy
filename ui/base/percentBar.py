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


class PercentBar(QLabel):
    '''
    '''

    
    def __init__(self, maxValue:int, length:int, height:int, parent=None, flags=Qt.WindowFlags()):
        '''
        '''
        super().__init__(parent, flags)

        self.__maxValue = int(maxValue)
        self.__value = self.__maxValue
        self.__updatingValue = self.__maxValue

        self.length = int(length)
        self.height = int(height)

        self.groundColor = 'gray'
        self.mediumColor = 'orange'
        self.frontColor = 'red'

        self.groundBar = self
        self.groundBar.setLayout(QHBoxLayout())
        self.groundBar.layout().setContentsMargins(0,0,0,0)
        self.groundBarImg = QPixmap(self.length, self.height)
        self.groundBarImg.fill(QColor(self.groundColor))
        self.setPixmap(self.groundBarImg)
        
        self.mediumBar = QLabel()
        self.mediumBar.setLayout(QHBoxLayout())
        self.mediumBar.layout().setContentsMargins(0,0,0,0)
        self.mediumBarImg = QPixmap(self.length, self.height)
        self.mediumBarImg.fill(QColor(self.mediumColor))
        self.mediumBar.setPixmap(self.mediumBarImg)
        self.groundBar.layout().addWidget(self.mediumBar)
        
        self.frontBar = QLabel()
        self.frontBarImg = QPixmap(self.length, self.height)
        self.frontBarImg.fill(QColor(self.frontColor))
        self.frontBar.setPixmap(self.frontBarImg)
        self.mediumBar.layout().addWidget(self.frontBar)

        self.timer = QTimer()
        self.updateFrqc = 50
        self.updateValue = int(self.length*0.05)      # must be positive
        self.timer.timeout.connect(self.__Update)
        
        return


    def ChangeValue(self, value:int):
        '''
        '''
        self.__value = max(0, min(self.__maxValue, int(value)))
        self.timer.start(self.updateFrqc)

        return

    def __Update(self):
        '''
        '''
        res = self.__value - self.__updatingValue
        if abs(res) <= self.updateValue:
            self.__updatingValue = self.__value
            self.timer.stop()
        else:
            if res < 0:
                self.__updatingValue -= self.updateValue
            else:
                self.__updatingValue += self.updateValue

        self.__ReDraw()
        return


    def __ReDraw(self):
        '''
        '''
        if self.__value > self.__updatingValue:
            self.mediumBar.setPixmap(self.mediumBarImg.scaled(int(self.__value * float(self.length) / self.__maxValue), self.height))
            self.frontBar.setPixmap(self.frontBarImg.scaled(int(self.__updatingValue * float(self.length) / self.__maxValue), self.height))
        else:
            self.mediumBar.setPixmap(self.mediumBarImg.scaled(int(self.__updatingValue * float(self.length) / self.__maxValue), self.height))
            self.frontBar.setPixmap(self.frontBarImg.scaled(int(self.__value * float(self.length) / self.__maxValue), self.height))

        return

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()

    layout = QVBoxLayout()

    pb = PercentBar(333, 157, 23)
    layout.addWidget(pb)

    btn1 = QPushButton('0')
    btn2 = QPushButton('50')
    btn3 = QPushButton('100')
    layout.addWidget(btn1)
    layout.addWidget(btn2)
    layout.addWidget(btn3)

    btn1.pressed.connect(lambda: pb.ChangeValue(0))
    btn2.pressed.connect(lambda: pb.ChangeValue(50))
    btn3.pressed.connect(lambda: pb.ChangeValue(100))

    w.setLayout(layout)
    w.show()

    app.exec()
