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


class StackedBtnChoiceBox(QLabel):
    '''
    '''

    def __init__(self, nPerRow:int=2, parent=None, flags=Qt.WindowFlags()):
        '''
        '''
        super().__init__(parent, flags)
        self.setLayout(QGridLayout())

        self.btnGroups:List[QWidget] = []
        self.groupBtns:List[List[QPushButton]] = []
        self.groupChoices:List[List[str]] = []
        self.nPerRow = nPerRow
        return


    def Fill(self, groupChoices:List[List[str]], groupActions:List[List[str]]=[])->List[QPushButton]:
        '''
        '''
        self.Clear()
        return self.Add(groupChoices, groupActions)


    def SwitchBtn(self, groupIndex:int, btnIndex:int):
        '''
        '''
        self.btnGroups[groupIndex].layout().setCurrentIndex(btnIndex)
        return


    def GetGroupAndBtnIndex(self, choice:str):
        '''
        '''
        for gci in range(len(self.groupChoices)):
            if choice in self.groupChoices[gci]:
                return (gci, self.groupChoices[gci].index(choice))

        return None



    def ShowChoice(self, choice:str):
        '''
        '''
        index = self.GetGroupAndBtnIndex(choice)
        if index == None:
            return
        self.SwitchBtn(*index)

        return


    def Add(self, groupChoices:List[List[str]], groupActions:List[List[str]]=[])->List[QPushButton]:
        '''
        '''
        btns = []
        n = len(groupChoices)
        na = len(groupActions)
        if na < n:
            groupActions.extend([[None for i in range(len(igC))] for igC in groupChoices[na:]])
        now = len(self.btnGroups)
        for i in range(now, now+n):
            in_ = len(groupChoices[i-now])
            ina = len(groupActions[i-now])
            if ina < in_:
                groupActions[i-now].extend([None for i in range(in_ - ina)])
            btnGroup = QWidget()
            btnGroup.setLayout(QStackedLayout())
            groupBtn = []
            for ii in range(len(groupChoices[i-now])):
                choice = groupChoices[i-now][ii]
                btn = QPushButton(choice)
                if isinstance(groupActions[i-now][ii], Callable):
                    btn.pressed.connect(lambda i=i,ii=ii:groupActions[i-now][ii]())
                else:
                    btn.setEnabled(False)
                btnGroup.layout().addWidget(btn)
                groupBtn.append(btn)
                btns.append(btn)
            self.groupBtns.append(groupBtn)
            self.btnGroups.append(btnGroup)
            self.layout().addWidget(btnGroup, int(i / self.nPerRow), int(i % self.nPerRow))
        self.groupChoices.extend(groupChoices)

        return btns


    def Clear(self):
        '''
        '''
        for btnGroup in self.btnGroups:
            self.layout().removeWidget(btnGroup)
        self.btnGroups.clear()
        self.groupChoices.clear()

        return


    def SetAllEnable(self, enable:bool):
        '''
        '''
        for groupBtn in self.groupBtns:
            for btn in groupBtn:
                btn.setEnabled(enable)

        return


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = StackedBtnChoiceBox()

    w.Fill(
        [['1','2','3'], ['one', 'two', 'three'], ['I', 'II', 'III']]
        , [
            [lambda:print(1), lambda:w.Add([['add']]), lambda:w.Add([['addadd'],['addadd2']], [[lambda:w.ShowChoice('three')], [lambda:w.ShowChoice('II')]])]
            , [lambda:w.ShowChoice('2')]
            , [lambda:w.ShowChoice('3')]
            ]
        )

    w.show()

    app.exec()
