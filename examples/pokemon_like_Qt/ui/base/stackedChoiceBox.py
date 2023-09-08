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


class StackedChoiceBox(QLabel):
    '''
    '''

    def __init__(self, autoShowHideNavi=True, parent=None, flags=Qt.WindowFlags()):
        '''
        '''
        super().__init__(parent, flags)
        self.setLayout(QHBoxLayout())
        self.pageLayout = QStackedLayout()
        self.naviLayout = QVBoxLayout()
        self.page = QWidget()
        self.page.setLayout(self.pageLayout)
        self.navi = QWidget()
        self.navi.setLayout(self.naviLayout)
        self.layout().addWidget(self.page)
        self.layout().addWidget(self.navi)
        self.upNaviBtn = QPushButton("👆")
        self.upNaviBtn.pressed.connect(self.GotoPrePage)
        self.downNaviBtn = QPushButton("👇")
        self.downNaviBtn.pressed.connect(self.GotoNxtPage)
        self.naviLayout.addWidget(self.upNaviBtn)
        self.naviLayout.addWidget(self.downNaviBtn)

        self.pages:List[QLabel] = []
        self.btns:List[QPushButton] = []
        self.nRow = 2
        self.nCol = 2

        self.autoShowHideNavi = autoShowHideNavi
        
        self.AutoShowHideNavi()
        return


    def ShowNavi(self):
        '''
        '''
        self.navi.show()
        return


    def HideNavi(self):
        '''
        '''
        self.navi.hide()


    def AutoShowHideNavi(self):
        '''
        '''
        if self.autoShowHideNavi:
            if len(self.pages )> 1:
                self.ShowNavi()
            else:
                self.HideNavi()

        return


    def Fill(self, choices:List[str], actions:List[Callable])->List[QPushButton]:
        '''
        '''
        self.Clear()
        return self.Add(choices, actions)


    def GotoPage(self, index):
        '''
        '''
        self.pageLayout.setCurrentIndex(index)
        return


    def GotoPrePage(self):
        '''
        '''
        currentIndex = self.pageLayout.currentIndex()
        if currentIndex == 0:
            maxIndex = len(self.pages) - 1
            currentIndex = maxIndex
        else:
            currentIndex -= 1
            
        self.GotoPage(currentIndex)
        return


    def GotoNxtPage(self):
        '''
        '''
        currentIndex = self.pageLayout.currentIndex()
        maxIndex = len(self.pages) - 1
        if currentIndex == maxIndex:
            currentIndex = 0
        else:
            currentIndex += 1
            
        self.GotoPage(currentIndex)
        return


    def Add(self, choices:List[str], actions:List[Callable])->List[QPushButton]:
        '''
        '''
        n = len(choices)
        na = len(actions)
        now = len(self.btns)
        nPerPage = self.nRow * self.nCol
        if na < n:
            actions.extend([None * (n-na)])
        for i in range(now, now+n):
            pagei = int(i / nPerPage)
            if pagei >= len(self.pages):
                ipage = QLabel()
                ipage.setLayout(QGridLayout())
                self.pages.append(ipage)
                self.pageLayout.addWidget(ipage)
            ipage = self.pages[pagei]
            indexInPage = int(i % nPerPage)
            choice = choices[i-now]
            btn = QPushButton(choice)
            if isinstance(actions[i-now], Callable):
                btn.pressed.connect(lambda i=i:actions[i-now]())
            else:
                btn.setEnabled(False)
            self.btns.append(btn)
            ipage.layout().addWidget(btn, int(indexInPage / self.nRow), int(indexInPage % self.nRow))

        self.AutoShowHideNavi()
        return self.btns


    def Clear(self):
        for igrid in self.pages:
            self.pageLayout.removeWidget(igrid)
        self.GotoPage(0)
        self.pages.clear()
        self.btns.clear()

        return


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = StackedChoiceBox()

    w.Fill(['1','2','3'], [lambda:print(1), lambda:w.Add(['4'], [lambda:print(4)]), lambda:w.Add(['5', '6'], [lambda:print(5), lambda:w.Clear()])])

    w.show()

    app.exec()
