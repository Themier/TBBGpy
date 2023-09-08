
from typing import Dict, List, Callable
from ..battle import Battle
from ..battleUnit import BattleUnit
from ..battleNumeric import BattleNumeric



class TurnBeginAction(Dict[str, object]):
    '''
    '''

    inses = []


    def __init__(self, action:Callable[[], None]):
        super().__init__()
        self.Action = action
        
        TurnBeginAction.inses.append(self)
        return


    @classmethod
    def Action(self):
        '''
        '''
        for act in self.inses:
            act.Action()

        return

   


