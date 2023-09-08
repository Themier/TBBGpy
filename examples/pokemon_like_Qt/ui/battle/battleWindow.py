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

from gear.battle.signTower import SignTower
from gear.battle.battle import Battle
from gear.battle.move import Move
from gear.battle.battleGroup import BattleGroup
from gear.battle.battleUnit import BattleUnit
from gear.battle.battleProcessor import BattleProcessor
from gear.battle.battleCaculator import BattleCalculator

from ..base.choiceBox import ChoiceBox
from ..base.stackedBtnChoiceBox import StackedBtnChoiceBox
from ..base.stackedChoiceBox import StackedChoiceBox
from ..base.msgBox import MsgBox
from ..base.percentBar import PercentBar


class BattleWindow(QWidget):

    ins = None
    

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        if BattleWindow.ins != None:
            return
        super().__init__(parent=parent, flags=flags)

        self.theBattle = None
        self.activedPlayerControlingRoles = []
        self.movedActivedPlayerControlingRoles = []
        self.focusedRole = None

        self.startBtn = None
        self.startBox =None
        self.msgBox:MsgBox = None
        self.moveBox = None
        self.choiceBox = None
        self.leftOptLayout = QStackedLayout()

        self.rightOptBox = None

        # 加载窗体图像
        self.mainBgImg = QPixmap()
        if not self.mainBgImg.load("SourceFile/img/backGround.png", "png"):
            raise "战斗窗口主背景加载失败"

        # 设置窗口无边框
        self.setWindowFlags(
            Qt.FramelessWindowHint
           )
        # 根据窗体图像调整大小，并居中
        self.resize(self.mainBgImg.size())
        screenRect = QApplication.desktop().screenGeometry()
        self.move(
            int((screenRect.width() - self.mainBgImg.size().width())*0.5)
            , int((screenRect.height() - self.mainBgImg.size().height())*0.5))
        # 根布局
        self.setLayout(QStackedLayout())

        # 主背景
        mainMarginFactor = 0.03
        mainMargin:int = min(
            int(self.mainBgImg.size().width()*mainMarginFactor)
            , int(self.mainBgImg.size().height()*mainMarginFactor)
            )
        self.mainBg = self.__InitMainWidget(self.layout(), self.mainBgImg, mainMargin)
        self.layout().addWidget(self.mainBg)

         # 战斗背景
        self.battleBgImg, self.battleBg = self.__initBattleWidget(self.mainBg.layout(), 0)

        # 战斗上部背景
        self.topBgImg, self.topBg = self.__initTopWidget(self.battleBg.layout(), 0)

        #- 战斗双边
        self.leftHpBarBox = QWidget()
        self.leftHpBarBox.setLayout(QVBoxLayout())
        self.rightHpBarBox = QWidget()
        self.rightHpBarBox.setLayout(QVBoxLayout())
        self.topBg.layout().addWidget(self.leftHpBarBox)
        self.topBg.layout().addWidget(self.rightHpBarBox)
        self.activedRoleHpBarDict = {}

        # 战斗下部背景
        self.bottomBgImg, self.bottomBg = self.__initBottomWidget(self.battleBg.layout(), 0)

        #- 战斗左操作区
        leftOptMargin = int(min(self.mainBgImg.size().height()*0.02, self.mainBgImg.size().width()*0.02))
        self.leftOptBgImg, self.leftOptBg = self.__InitLeftOptWidget(self.bottomBg.layout(), leftOptMargin)

        #- 消息盒子
        self.__initMsgBox('')

        #- 技能盒子
        self.__initMoveBox()

        #- 启动栏
        self.__initStartBox()
        self.leftOptLayout.setCurrentIndex(2)

        #- 选择盒子
        self.__initChoiceBox()

        #- 战斗右操作区
        rightOptMargin = leftOptMargin
        self.rightOptBgImg, self.rightOptBg = self.__initRightOptWidget(self.bottomBg.layout(), rightOptMargin)
        self.__initOptBtns(self.rightOptBg.layout())

        #- 信号塔
        SignTower.ins.Regist('ui技能选中目标', self.MoveTargetGot)
        SignTower.ins.Regist('ui战斗结束', self.close)
        SignTower.ins.Regist('战斗消息', self.msgBox.AddMsg)
        
        BattleWindow.ins = self
        self.show()
        return
    

    def __initOptBtns(self, rightOptLayout):
        '''
        初始化选项盒子
        '''
        self.rightOptBox = StackedBtnChoiceBox()
        self.rightOptBox.Fill(
                [
                    ['\n行动\n']
                    , ['\n背包\n']
                    , ['\n交换\n']
                    , ['\n逃跑\n', '\n返回\n']
                ]
                , [
                    [self.ForwardToMovesBox]
                    , [self.ForwardToBagWindow]
                    , [self.ForwardToAliesWindow]
                    , [self.ForwardToRunWindow, self.BackToMessage]
                ]
            )
        self.rightOptBox.SetAllEnable(False)

        rightOptLayout.addWidget(self.rightOptBox)
        return 


    def __initRightOptWidget(self, bottomLayout, rightOptMargin):
        '''
        初始化选项盒子
        '''
        rightOptBgImg:QPixmap = QPixmap()
        if not rightOptBgImg.load("SourceFile/img/battleRightOptBg.png", "png"):
            raise "加载战斗界面右操作区背景失败"
        rightOptBg:QLabel = QLabel()
        rightOptBg.setPixmap(rightOptBgImg)
        self.bottomBg.layout().addWidget(rightOptBg)
        #--
        rightOptLayout:QGridLayout = QGridLayout()
        rightOptLayout.setContentsMargins(
            rightOptMargin, rightOptMargin
            , rightOptMargin, rightOptMargin
            )
        rightOptBg.setLayout(rightOptLayout)

        return rightOptBgImg, rightOptBg


    def __initChoiceBox(self):
        '''
        初始化选择盒子
        '''
        self.choiceBox = ChoiceBox()
        self.leftOptLayout.addWidget(self.choiceBox)

        return


    def FillChoiceBox(self, choices:List[str], signSubject:str, signValues:List[any]=[]):
        '''
        填充选择盒子
        '''        
        nGetChoices = len(choices)
        if nGetChoices == 0:
            self.choiceBox.Fill(['没有可选择目标'], [self.BackToMessage])
        else:
            nGetSignValues = len(signValues)
            if nGetSignValues < nGetChoices:
                signValues.extend(choices[nGetChoices - nGetSignValues :])
            choiceItems = signValues

            actions = [lambda i=i:SignTower.ins.Push(signSubject, choiceItems[i]) for i in range(len(choices))]
            self.choiceBox.Fill(choices, actions)

        return


    def ShowChoiceBox(self):
        '''
        '''
        self.leftOptLayout.setCurrentIndex(3)
        self.rightOptBox.SetAllEnable(False)
        self.ShowBackBtn()
        return


    def FinishChoiceBox(self):
        '''
        '''
        self.rightOptBox.SetAllEnable(True)
        self.BackToMessage()
        return


    def MoveTargetGot(self, moverId:str, targetId:str, moveId:str):
        '''
        '''
        if not moverId in self.movedActivedPlayerControlingRoles:
            self.movedActivedPlayerControlingRoles.append(moverId)
            BattleProcessor.ins.PlayerAddMove(moverId, targetId, moveId)
            self.FinishChoiceBox()

            self.CheckTurnPrepare()
        return


    def __initMoveBox(self):
        '''
        初始化技能盒子
        '''
        self.moveBox = StackedChoiceBox()
        self.leftOptLayout.addWidget(self.moveBox)

        return


    def FillMoveBox(self, moves:List[str]):
        '''
        '''
        self.moveBox.Fill(moves, [
            self.moveBtn_1_clicked, self.moveBtn_2_clicked
            , self.moveBtn_3_clicked, self.moveBtn_4_clicked])

        return


    def __initStartBox(self):
        '''
        初始化启动栏
        '''
        self.startBtn = QPushButton("\n开始\n")
        self.startBtn.pressed.connect(self.StartBattle)
        startLayout = QHBoxLayout()
        self.startBox = QLabel()

        startLayout.addWidget(self.startBtn)
        self.startBox.setLayout(startLayout)
        self.leftOptLayout.addWidget(self.startBox)

        return 


    def __initMsgBox(self, initMsg):
        '''
        初始化消息盒子
        '''
        self.msgBox = MsgBox(int(min(self.mainBgImg.size().height()*0.07, self.mainBgImg.size().width()*0.07)))
        self.leftOptLayout.addWidget(self.msgBox)

        return 


    def __InitLeftOptWidget(self, bottomLayout, contentMargin):
        '''
        初始化战斗左操作区
        '''
        leftOptBgImg:QPixmap = QPixmap()
        if not leftOptBgImg.load("SourceFile/img/battleLeftOptBg.png", "png"):
            raise "加载战斗界面左操作区背景失败"
        leftOptBg:QLabel = QLabel()
        leftOptBg.setPixmap(leftOptBgImg)
        bottomLayout.addWidget(leftOptBg)
        leftOptLayoutH:QHBoxLayout = QHBoxLayout()
        leftOptLayoutH.setContentsMargins(
            contentMargin, contentMargin
            , contentMargin, contentMargin
            )
        leftOptBg.setLayout(leftOptLayoutH)
        leftOptLayoutH.addLayout(self.leftOptLayout)

        return leftOptBgImg, leftOptBg


    def __initBottomWidget(self, battleLayout, contentMargin):
        '''
        初始化战斗下部窗体
        '''
        bottomBgImg:QPixmap = QPixmap()
        if not bottomBgImg.load("SourceFile/img/battleBottomBg.png", "png"):
            raise "加载战斗界面上部背景失败"
        bottomBg:QLabel = QLabel()
        bottomBg.setPixmap(bottomBgImg)
        battleLayout.addWidget(bottomBg)
        bottomLayout:QHBoxLayout = QHBoxLayout()
        bottomLayout.setContentsMargins(
            contentMargin, contentMargin
            , contentMargin, contentMargin
            )
        bottomBg.setLayout(bottomLayout)

        return bottomBgImg, bottomBg


    def __initTopWidget(self, battleLayout, contentMargin):
        '''
        初始化战斗上部窗体
        '''
        topBgImg:QPixmap = QPixmap()
        if not topBgImg.load("SourceFile/img/battleTopBg.png", "png"):
            raise "加载战斗界面上部背景失败"
        topBg:QLabel = QLabel()
        topBg.setPixmap(topBgImg)
        battleLayout.addWidget(topBg)
        topLayout:QHBoxLayout = QHBoxLayout()
        topLayout.setContentsMargins(
            contentMargin, contentMargin
            , contentMargin, contentMargin
            )
        topBg.setLayout(topLayout)

        return topBgImg, topBg


    def __initBattleWidget(self, mainLayout, contentMargin):
        '''
        初始化战斗窗体
        '''
        battleBgImg:QPixmap = QPixmap()
        if not battleBgImg.load("SourceFile/img/battleBg.png", "png"):
            raise "加载战斗界面战斗背景失败"
        battleBg:QLabel = QLabel()
        battleBg.setPixmap(battleBgImg)
        mainLayout.addWidget(battleBg)
        battleLayout:QVBoxLayout = QVBoxLayout()
        battleLayout.setContentsMargins(
            contentMargin, contentMargin
            , contentMargin, contentMargin
            )
        battleBg.setLayout(battleLayout)

        return battleBgImg, battleBg


    def __InitMainWidget(self, rootLayout, img, contentMargin):
        '''
        初始化主窗体
        '''
        mainBg:QLabel = QLabel()
        mainBg.setPixmap(self.mainBgImg)
        mainLayout:QVBoxLayout = QVBoxLayout()
        mainLayout.setContentsMargins(
            contentMargin, contentMargin
            , contentMargin, contentMargin
            )
        mainBg.setLayout(mainLayout)

        return mainBg

    
    def ShowRunBtn(self):
        '''
        '''
        self.rightOptBox.ShowChoice('\n逃跑\n')
        return 


    def ShowBackBtn(self):
        '''
        '''
        self.rightOptBox.ShowChoice('\n返回\n')
        return


    def ShowMoves(self):
        '''
        '''
        self.FillMoveBox(self.focusedRole['技能'])
        self.leftOptLayout.setCurrentIndex(1)
        self.ShowBackBtn()

        return


    def ForwardToMovesBox(self):
        '''
        '''
        self.ShowMoves()
        self.ShowBackBtn()


    def ShowBag(self):
        '''
        '''
        #self.leftOptLayout.setCurrentIndex(2)

        return


    def ForwardToBagWindow(self):
        '''
        '''
        self.ShowBag()
        #self.ShowBackBtn()


    def ShowAlies(self):
        '''
        '''
        #self.leftOptLayout.setCurrentIndex(3)

        return


    def ForwardToAliesWindow(self):
        '''
        '''
        self.ShowAlies()
        #self.ShowBackBtn()


    def ShowRunWindow(self):
        '''
        '''
        #self.leftOptLayout.setCurrentIndex(4)

        return


    def ForwardToRunWindow(self):
        '''
        '''
        self.ShowRunWindow()
        self.ShowBackBtn()


    def ShowMsgBox(self):
        '''
        '''
        self.leftOptLayout.setCurrentIndex(0)


    def BackToMessage(self):
        '''
        '''
        self.rightOptBox.SetAllEnable(True)
        self.ShowMsgBox()
        self.ShowRunBtn()

        return


    def moveBtn_clicked(self, index:int):
        moveId = self.focusedRole['技能'][index]
        move = Move.moveDict[moveId]
        selectRule = move['目标类型']
        moverId = self.focusedRole['id']
        if selectRule == 'none':
            self.MoveTargetGot(moverId, None, moveId)
        else:
            targets = BattleCalculator.GetAllPossibleTargets(selectRule, moverId)
            if len(targets) == 1:
                self.MoveTargetGot(moverId, targets[0], moveId)
            else:
                self.FillChoiceBox([Battle.ins.GetBattleUnit(target)['名字'] for target in targets], 'ui技能选中目标', [(moverId,t,moveId) for t in targets])
                self.ShowChoiceBox()

        return


    def moveBtn_1_clicked(self):
        return self.moveBtn_clicked(0)


    def moveBtn_2_clicked(self):
        return self.moveBtn_clicked(1)


    def moveBtn_3_clicked(self):
        return self.moveBtn_clicked(2)


    def moveBtn_4_clicked(self):
        return self.moveBtn_clicked(3)


    def NewTurn(self):
        '''
        '''
        if self.CheckOver():
            return

        BattleProcessor.ins.NewTurn()

        self.activedPlayerControlingRoles.clear()
        self.movedActivedPlayerControlingRoles.clear()
        for roleId in self.theBattle.GetActivedRoles():
            role = Battle.ins.GetBattleUnit(roleId)
            if role['AIType'] == None:
                self.activedPlayerControlingRoles.append(role)

        BattleProcessor.ins.AIAddMove()
        self.CheckTurnPrepare()

        return


    def CheckOver(self):
        '''
        '''
        if BattleCalculator.BattleIsOver():
            self.BattleOver()
            return True

        return False


    def BattleOver(self):
        '''
        '''
        self.FillChoiceBox(['\n战斗结束\n'], 'ui战斗结束', [None])
        self.ShowChoiceBox()

        return


    def ProcessTurn(self):
        '''
        '''
        turnContinue = BattleProcessor.ins.ProcessTurn()
        for roleId in self.activedRoleHpBarDict:
                role = Battle.ins.GetBattleUnit(roleId)
                self.activedRoleHpBarDict[roleId].ChangeValue(role['hp'])
        if turnContinue:
            self.msgBox.overAction = lambda:self.ProcessTurn()
        else:
            self.msgBox.overAction = lambda:self.NewTurn()
        self.msgBox.ShowMsgs()

        return


    def CheckTurnPrepare(self):
        '''
        '''
        if len(self.activedPlayerControlingRoles) == 0:
            self.rightOptBox.SetAllEnable(False)
            self.ProcessTurn()
        else:
            self.focusedRole = self.activedPlayerControlingRoles.pop(0)
            self.msgBox.AddMsg('{} 等待行动'.format(self.focusedRole['名字']))
            self.ShowMsgBox()
            self.msgBox.overAction = lambda:self.rightOptBox.SetAllEnable(True)
            self.msgBox.ShowMsgs()
            
        return


    def StartBattle(self): 
        if self.theBattle != None:
            return
        
        leftGroup = BattleGroup({'名字':'红方'})
        rightGroup = BattleGroup({'名字':'蓝方'})
        leftFirstRole = BattleUnit({'名字':'红1', '技能':['击打', '自愈', '魔法火焰'], 'hp':250, '最大Hp':250, 'AIType':None})
        leftRole2 = BattleUnit({'名字':'红2', '技能':['击打'], 'hp':50, '最大Hp':50, 'AIType':None})
        rightFirstRole = BattleUnit({'名字':'蓝1', '技能':['击打', '鬼火'], 'hp':100, '最大Hp':100, '速度':11})
        battle = Battle.ins
        battle.AddGroup(leftGroup)
        battle.AddGroup(rightGroup)
        battle.AddRole(leftFirstRole, leftGroup['id'])
        battle.AddRole(leftRole2, leftGroup['id'])
        battle.AddRole(rightFirstRole, rightGroup['id'])
        battle.SetActiveRole(leftFirstRole['id'])
        battle.SetActiveRole(rightFirstRole['id'])

        self.theBattle = battle

        for roleId in self.theBattle['activedRoles']:
            if roleId in leftGroup['roles']:
                role = Battle.ins.GetBattleUnit(roleId)
                hpBar = PercentBar(role['最大Hp'], 100, 20)
                hpBar.ChangeValue(role['hp'])
                self.leftHpBarBox.layout().addWidget(hpBar)
                self.activedRoleHpBarDict[role['id']] = hpBar
            elif roleId in rightGroup['roles']:
                role = Battle.ins.GetBattleUnit(roleId)
                hpBar = PercentBar(role['最大Hp'], 100, 20)
                hpBar.ChangeValue(role['hp'])
                self.rightHpBarBox.layout().addWidget(hpBar)
                self.activedRoleHpBarDict[role['id']] = hpBar
        
        self.NewTurn()
        return







