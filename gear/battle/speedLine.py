
import random
from typing import Dict, List, Tuple, Callable
from .battleUnit import BattleUnit
from .battle import Battle
from .move import Move


class SpeedLine(Dict[float, List[Tuple]]):
    '''
    '''

    ins = None


    def __init__(self):
        if SpeedLine.ins == None:
            SpeedLine.ins = self


    def AddMove(self, moverId:str, targetId:str, moveId:str):
        '''
        '''
        mover:BattleUnit = Battle.ins.GetBattleUnit(moverId)
        move:Move = Move.moveDict[moveId]
        speedWeight = 1.0 / mover['速度'] - move['先制等级']
        if not speedWeight  in self:
            self[speedWeight] = [(moverId, targetId, moveId)]
        else:
            self[speedWeight].append((moverId, targetId, moveId))

        return 


    def Sort(self, key:Callable[[tuple], object]=None):
        '''
        '''
        self = dict(sorted(self.items(), key=key))
        for weight in self:
            random.shuffle(self[weight])
        return 


    def SortedKeys(self)->List[float]:
        '''
        '''
        sortedKeys = list(self.keys())    
        sortedKeys.sort()   # 速度线排序
        return sortedKeys


SpeedLine()