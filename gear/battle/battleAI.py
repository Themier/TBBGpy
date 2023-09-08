
from typing import Dict, Tuple, List, Callable
from .battleUnit import BattleUnit
from .move import Move
from .moveEffect import MoveEffect
from .battle import Battle
from .battleCaculator import BattleCalculator
from .signTower import SignTower, BackSign


class BattleAI():
    '''
    '''
    inses = {}


    def __init__(self, id:str, getMove:Callable[[str], tuple]):
        self.id = id
        self.GetMove = getMove

        BattleAI.inses[self.id] = self
        return


    @classmethod
    def GetMove(self, id:str, moverId:str)->tuple:
        '''
        '''
        if not id in self.inses:
            return None

        return self.inses[id].GetMove(moverId)


def BANormal(moverId:str)->tuple:
    '''
    '''
    mover = Battle.ins.GetBattleUnit(moverId)
    if mover == None:
        return None
    skills = mover['技能']
    if len(skills) == 0:
        return None
    theSkillId = ''
    theTargetId = ''
    maxWeight = -999.0
    for skillId in skills:
        skill = Move.moveDict[skillId]
        weight = 0.0
        target = None
        if skill['ai目标类型'] == 'none':
            effect = skill['效果']
            weight = MoveEffect.CountWeight(effect, mover, target, skill)
        else:
            targets = BattleCalculator.GetAllPossibleTargets(skill['目标类型'], moverId)
            for target in targets:
                target = Battle.ins.GetBattleUnit(target)
                effect = skill['效果']
                weight = MoveEffect.CountWeight(effect, mover, target, skill)
        if weight > maxWeight:
            maxWeight = weight
            theSkillId = skillId
            if target != None:
                theTargetId = target['id']
            else:
                theTargetId = None
    if theSkillId == '':
        return None
        
    return (moverId, theTargetId, theSkillId)
BattleAI('正常', BANormal)
