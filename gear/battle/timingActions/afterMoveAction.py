
from typing import Dict, List, Callable
from ..battle import Battle
from ..battleUnit import BattleUnit
from ..battleNumeric import BattleNumeric



class AfterMoveAction(Dict[str, object]):
    '''
    '''

    inses = []


    def __init__(self, action:Callable[[BattleUnit], None]):
        super().__init__()
        self.Action = action
        
        AfterMoveAction.inses.append(self)
        return


    @classmethod
    def Action(self, bu:BattleUnit):
        '''
        '''
        for act in self.inses:
            act.Action(bu)

        return

   



