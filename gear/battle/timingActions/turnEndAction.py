
from typing import Dict, List, Callable
from ..battle import Battle
from ..battleUnit import BattleUnit
from ..battleNumeric import BattleNumeric
from ..signTower import SignTower



class TurnEndAction(Dict[str, object]):
    '''
    '''

    inses = []


    def __init__(self, action:Callable[[], None]):
        super().__init__()
        self.Action = action
        
        TurnEndAction.inses.append(self)
        return


    @classmethod
    def Action(self):
        '''
        '''
        for act in self.inses:
            act.Action()

        return

   
def TEClearProtect():
    '''
    '''
    for roleId in Battle.ins['activedRoles']:
        role = Battle.ins.GetBattleUnit(roleId)
        if role == None:
            continue
        if BattleNumeric.Count('protected', role):
            role.SetValue('保护疲劳', True)
        else:
            role.SetValue('保护疲劳', False)
        role.SetValue('保护', False)
    return
TurnEndAction(TEClearProtect)

def TEBurnHurt():
    '''
    '''
    for roleId in Battle.ins['activedRoles']:
        role = Battle.ins.GetBattleUnit(roleId)
        if BattleNumeric.Count('bured', role) and BattleNumeric.Count('alive', role):
            SignTower.ins.Push('战斗消息', '{} 因为烧伤而受到伤害.'.format(role['名字']))
            role.SetValue('hp', int(role['hp']-role['最大Hp']/16.0))
    return
TurnEndAction(TEBurnHurt)

