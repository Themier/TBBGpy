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


class ChoiceBox(QLabel):
    '''
    '''

    def __init__(self, nPerRow:int=3, parent=None, flags=Qt.WindowFlags()):
        '''
        '''
        super().__init__(parent, flags)
        self.setLayout(QGridLayout())
        self.btns = []
        self.nPerRow = nPerRow
        
        return


    def Fill(self, choices:List[str], actions:List[Callable])->List[QPushButton]:
        '''
        '''
        self.Clear()
        return self.Add(choices, actions)


    def Add(self, choices:List[str], actions:List[Callable])->List[QPushButton]:
        '''
        '''
        n = len(choices)
        na = len(actions)
        now = len(self.btns)
        if na < n:
            actions.extend([None * (n-na)])
        for i in range(now, now+n):
            choice = choices[i-now]
            btn = QPushButton(choice)
            if isinstance(actions[i-now], Callable):
                btn.pressed.connect(lambda i=i:actions[i-now]())
            else:
                btn.setEnabled(False)
            self.btns.append(btn)
            self.layout().addWidget(btn, int(i / self.nPerRow), int(i % self.nPerRow))

        return self.btns


    def Clear(self):
        for btn in self.btns:
            self.layout().removeWidget(btn)
        self.btns.clear()

        return


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = ChoiceBox()

    w.Fill(['1','2','3'], [lambda:print(1), lambda:w.Add(['4'], [lambda:print(4)]), lambda:w.Fill(['5', '6'], [lambda:print(5), lambda:w.Clear()])])

    w.show()

    app.exec()