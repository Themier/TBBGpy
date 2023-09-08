
from typing import Dict, List, Callable
from .battleUnitAttribute import BattleUnitAttribute
from .signTower import SignTower


class BattleUnit(Dict[str, object]):
    '''
    一个战斗单元
    '''

    count=0


    def __init__(self, initVal:Dict[str, object]={}):
        super().__init__()
        
        self.update(BattleUnitAttribute.defaultValues)
        self.update(initVal)
        self['id'] = str(BattleUnit.count)
        BattleUnit.count+=1

        return


    def SetValue(self, key:str, value:object, max:object=None, min:object=None):
        '''
        '''
        SignTower.ins.Push('BattleUnit属性改变', self['id'])
        self.SetValueSilent(key, value, max, min)

        return


    def SetValueSilent(self, key:str, value:object, max:object=None, min:object=None):
        '''
        '''
        self[key] = value

        if max == None:
            if key in BattleUnitAttribute.inses:
                max = BattleUnitAttribute.inses[key].max
        if min == None:
            if key in BattleUnitAttribute.inses:
                min = BattleUnitAttribute.inses[key].min

        if max != None and self[key] > max:
            self[key] = max
        elif min != None and self[key] < min:
            self[key] = min

        return




