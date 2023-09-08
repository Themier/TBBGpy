import random
from typing import Dict, List, Callable
from .battle import Battle
from .battleNumeric import BattleNumeric
from .battleAI import BattleAI
from .speedLine import SpeedLine
from .battleCaculator import BattleCalculator
from .timingActions.turnEndAction import TurnEndAction
from .timingActions.turnBeginAction import TurnBeginAction
from .timingActions.beforeMoveAction import BeforeMoveAction
from .timingActions.afterMoveAction import AfterMoveAction
from .timingActions.beforeChoicedAction import BeforeChoicedAction
from .timingActions.afterChoicedAction import AfterChoicedAction
from .move import Move
from .moveEffect import MoveEffect
from .signTower import SignTower


class BattleProcessor(Dict[str, object]):

    ins = None

    def __init__(self):
        super().__init__()
        if BattleProcessor.ins == None:
            BattleProcessor.ins = self

            self.processState = 'done'
            self.processIndex = 0
            self.nowProcessWeight = 0
            self.nowMoveIndex = 0

            self.update({
                '回合数':0
                })

        return


    def NewTurn(self):
        '''
        '''
        SpeedLine.ins.clear()
        self['回合数'] += 1
        SignTower.ins.Push('新回合开始', self['回合数'])

        return


    def AIAddMove(self):
        '''
        '''
        for roleId in Battle.ins.GetActivedRoles():
            role = Battle.ins.GetBattleUnit(roleId)
            if role != None and BattleNumeric.Count('canMove',role):
                role = Battle.ins.GetBattleUnit(roleId)
                ai = role['AIType'] 
                if not ai == None:
                    move = BattleAI.GetMove(ai, roleId)
                    if move != None:
                        SpeedLine.ins.AddMove(*move)
        return


    def PlayerAddMove(self, moverId:str, targetId:str, moveId:str):
        '''
        '''
        SpeedLine.ins.AddMove(moverId, targetId, moveId)
        return


    def ProcessTurn(self):
        '''
        '''
        if self.processState == 'done':
            self.processState = 'begin'
            SpeedLine.ins.Sort()
        elif self.processState == 'begin':
            self.processState = 'move'
            self.processIndex = 0
            self.nowProcessWeight = list(SpeedLine.ins.keys())[self.processIndex]
            self.nowMoveIndex = 0
        elif self.processState == 'move':
            self.nowMoveIndex += 1
            if self.nowMoveIndex >= len(SpeedLine.ins[self.nowProcessWeight]):
                self.processIndex += 1
                self.nowMoveIndex = 0
                if self.processIndex >= len(SpeedLine.ins):
                    self.processState = 'end'
                    self.processIndex = 0
                    self.nowProcessWeight = 0
                else:
                    self.nowProcessWeight = list(SpeedLine.ins.keys())[self.processIndex]
        elif self.processState == 'end':
            self.processState = 'done'
            self.processIndex = 0

        if self.processState == 'begin':
            TurnBeginAction.Action()
        elif self.processState == 'move':
            move = SpeedLine.ins[self.nowProcessWeight][self.nowMoveIndex]
            BattleProcessor.Parse(*move)
        elif self.processState == 'end':
            TurnEndAction.Action()
        else:
            return False

        return True


    @classmethod
    def Parse(self, userId:str, targetId:str, moveId:str):
        '''
        '''
        user = Battle.ins['roleDict'].get(userId, None)
        target = Battle.ins['roleDict'].get(targetId, None)
        move = Move.moveDict.get(moveId, None)
        if self.__PrepareParse(user, target, move):
            MoveEffect.Effect(move['效果'], user, target, move)
            self.__DoneMoveParse(user, target, move)

        return


    @classmethod
    def __PrepareParse(self, user, target, move)->bool:
        '''
        '''
        if move == None:
            SignTower.ins.Push('战斗日志', '无效的技能被 parse')
            return False

        if user == None:
            if target == None:
                SignTower.ins.Push('战斗消息', '{} 被使用'.format(move['名字']))
                return True
            else:
                if BattleNumeric.Count('canBeChoiced', target):
                    BeforeChoicedAction.Action(target)
                    SignTower.ins.Push('战斗消息', '{} 被 {} 瞄准了'.format(target['名字'], move['名字']))
                    return True
                else:
                    SignTower.ins.Push('战斗消息', '{} 无法被选中'.format(target['名字']))
                    return False
        else:
            if target == None:
                if BattleNumeric.Count('canMove', user):
                    BeforeMoveAction.Action(user)
                    SignTower.ins.Push('战斗消息', '{} 使用了 {}'.format(user['名字'], move['名字']))
                    return True
                else:
                    if BattleNumeric.Count('alive', user):
                        SignTower.ins.Push('战斗消息', '{} 无法使用 {}'.format(user['名字'], move['名字']))
                    return False
            else:
                if BattleNumeric.Count('canMove', user) and BattleNumeric.Count('canBeChoiced', target):
                    BeforeMoveAction.Action(user)
                    BeforeChoicedAction.Action(target)
                    SignTower.ins.Push('战斗消息', '{} 对 {} 使用了 {}'.format(user['名字'], target['名字'], move['名字']))
                    return True
                else:
                    if BattleNumeric.Count('alive', user):
                        SignTower.ins.Push('战斗消息', '{} 对 {} 使用了 {}, 但是失败了'.format(user['名字'], target['名字'], move['名字']))
                    return False

        return False


    @classmethod
    def __DoneMoveParse(self, user, target, move):
        '''
        '''
        if move != None:
            if user != None:
                AfterMoveAction.Action(user)
            if target != None:
                AfterChoicedAction.Action(target)

        return


BattleProcessor()