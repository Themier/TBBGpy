
from typing import Dict, List, Callable
from .battleUnit import BattleUnit
from .battleNumeric import BattleNumeric
from .battleCaculator import BattleCalculator
from .timingActions.beforeAttackedAction import BeforeAttackedAction
from .timingActions.beforeCuredAction import BeforeCuredAction
from .timingActions.afterAttackedAction import AfterAttackedAction
from .timingActions.afterCuredAction import AfterCuredAction
from .signTower import SignTower


class MoveEffect():
    '''
    '''

    inses = {}


    def __init__(self, id:str, effect:Callable[[BattleUnit, BattleUnit, dict], None], weightCounter:Callable[[BattleUnit, BattleUnit, dict], float]):
        self.id = id
        self.Effect = effect
        self.weightCounter = weightCounter

        MoveEffect.inses[self.id] = self
        return


    @classmethod
    def Effect(self, id:str, user:BattleUnit, target:BattleUnit, move:Dict[str, object])->None:
        if id in self.inses:
            self.inses[id].Effect(user, target, move)
        return


    @classmethod
    def CountWeight(self, id:str, user:BattleUnit, target:BattleUnit, move:Dict[str, object])->float:
        if id in self.inses:
            return self.inses[id].weightCounter(user, target, move)
        return


def singleHit(user:BattleUnit, target:BattleUnit, move:Dict[str, object])->None:
    '''
    '''
    if BattleNumeric.Count('canHit', user) and BattleNumeric.Count('canBeHited', target):
        BeforeAttackedAction.Action(target)
        damage = BattleCalculator.CountDamagePoint(user, target, move['威力'])
        target.SetValue('hp', target.get('hp')-damage, target['最大Hp'], 0)
        SignTower.ins.Push('战斗消息','{} 受到了 {} 点伤害'.format(target['名字'], damage))
        target.SetValue('最后受伤值', damage)
        target.SetValue('最后受伤来自', user['id'])
        AfterAttackedAction.Action(target)
    else:
        SignTower.ins.Push('战斗消息','{} 因保护而免受伤害'.format(target['名字']))
    return
def singleHitWeight(user:BattleUnit, target:BattleUnit, move:Dict[str, object])->float:
    '''
    '''
    if BattleNumeric.Count('canHit', user) and BattleNumeric.Count('canBeHited', target):
        damage = BattleCalculator.CountDamagePoint(user, target, move['威力'])
        return float(damage)
    return 0.0
MoveEffect('单体攻击', singleHit, singleHitWeight)


def selfRecover(user:BattleUnit, target:BattleUnit, move:Dict[str, object])->None:
    '''
    '''
    if BattleNumeric.Count('canMove', user):
        BeforeCuredAction.Action(user)
        value = int(user.get('最大Hp', 0)*1.0*move['效果参数'])
        user.SetValue('hp', user['hp'] +value, user['最大Hp'], 0)
        SignTower.ins.Push('战斗消息','{} 恢复了 {} 点hp'.format(user['名字'], value))
        AfterCuredAction.Action(user)
    return
def selfRecoverWeight(user:BattleUnit, target:BattleUnit, move:Dict[str, object])->float:
    '''
    '''
    if BattleNumeric.Count('canMove', user):
        return int(user.get('最大Hp', 0)*1.0*move['效果参数'])
    return 0.0
MoveEffect('自我治愈', selfRecover, selfRecoverWeight)


def selfProtect(user:BattleUnit, target:BattleUnit, move:Dict[str, object])->None:
    '''
    '''
    if not BattleNumeric.Count('protectTired'):
        user.SetValue('保护', True)
        SignTower.ins.Push('战斗消息','{} 受到了保护'.format(user['名字']))
    else:
        SignTower.ins.Push('战斗消息','{} 无法受到保护'.format(user['名字']))
    return
def selfProtectWeight(user:BattleUnit, target:BattleUnit, move:Dict[str, object])->float:
    '''
    '''
    if user.get('保护', False) or user.get('保护疲劳', False):
        return 0.0
    return int(user['最大Hp']-user['hp'])
MoveEffect('自我保护', selfProtect, selfProtectWeight)


def singleHitDownTargetAttack(user:BattleUnit, target:BattleUnit, move:Dict[str, object])->None:
    '''
    '''
    if BattleNumeric.Count('canHit', user) and BattleNumeric.Count('canBeHited', target):
        BeforeAttackedAction.Action(target)
        damage = BattleCalculator.CountDamagePoint(user, target, move['威力'])
        target.SetValue('hp', target.get('hp')-damage, target['最大Hp'], 0)
        SignTower.ins.Push('战斗消息','{} 受到了 {} 点伤害'.format(target['名字'], int(damage)))
        target.SetValue('攻击等级', target['攻击等级']-int(move['效果参数']), 6, -6)
        SignTower.ins.Push('战斗消息','{} 攻击等级降低为 {}'.format(target['名字'], int(target['攻击等级'])))
        target.SetValue('最后受伤值', damage)
        target.SetValue('最后受伤来自', user['id'])
        AfterAttackedAction.Action(target)
    else:
        SignTower.ins.Push('战斗消息','{} 因保护而免受伤害'.format(target['名字']))
    return
def singleHitDownTargetAttackWeight(user:BattleUnit, target:BattleUnit, move:Dict[str, object])->float:
    '''
    '''
    if BattleNumeric.Count('canHit', user) and BattleNumeric.Count('canBeHited', target):
        damage = BattleCalculator.CountDamagePoint(user, target, move['威力'])
        targetAtk = target.get('攻击', 0.0)
        atkLevel = target.get('攻击等级', 0)
        affect = 0.0
        if atkLevel != -6:
            affect = targetAtk * 0.5 * int(move['效果参数'])
        return int(damage) + int(affect)
    return 0.0
MoveEffect('单体攻击减攻', singleHitDownTargetAttack, singleHitDownTargetAttackWeight)


def singleBurn(user:BattleUnit, target:BattleUnit, move:Dict[str, object])->None:
    '''
    '''
    if BattleNumeric.Count('canHit', user) and BattleNumeric.Count('canBeHited', target):
        if not BattleNumeric.Count('bured', target):
            target.SetValue('烧伤', True)
            SignTower.ins.Push('战斗消息','{} 被烧伤了'.format(target['名字']))
        else:
            SignTower.ins.Push('战斗消息','{} 受到保护'.format(target['名字']))
    return
def singleBurnWeight(user:BattleUnit, target:BattleUnit, move:Dict[str, object])->float:
    '''
    '''
    if BattleNumeric.Count('canHit', user) and BattleNumeric.Count('canBeHited', target):
        if not BattleNumeric.Count('bured', target):
            return 100.0
    return 0.0
MoveEffect('单体烧伤', singleBurn, singleBurnWeight)




