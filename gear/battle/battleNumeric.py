
from typing import Dict, List, Callable
import pandas


class BattleNumeric(Dict[str, object]):
    '''
    战斗中的计算项
    是单元属性的拓展概念，这些计算项可以完全由单独的战斗单元计算出来
    '''

    inses = {}


    def __init__(self, id:str, name:str, desc:str, pamType:type, valType:type, Count:Callable[[object], object], min=None, max=None):
        super().__init__()
        self.id = id
        self.name = name
        self.pamType = pamType
        self.valType = valType
        self.Count = Count
        self.desc = desc
        self.min = min
        self.max = max

        BattleNumeric.inses[self.id] = self
        return


    @classmethod
    def Count(self, id:str, pam):
        '''
        '''
        if id in self.inses:
            return self.inses[id].Count(pam)
        else:
            print('undefine item {}'.format(id))
        return None


BattleNumeric('alive', 'alive', '是否存活'
              , Dict[str, object], bool
              , lambda p:p['hp']>0)

BattleNumeric('canBeChoiced', 'canBeChoiced', '是否可以被选中'
              , Dict[str, object], bool
              , lambda p:BattleNumeric.Count('alive', p))

BattleNumeric('canMove', 'canMove', '是否可以行动'
              , Dict[str, object], bool
              , lambda p:BattleNumeric.Count('alive', p) and (not BattleNumeric.Count('sleeping', p)))

BattleNumeric('atkLevelFactor', 'atkLevelFactor', '攻击等级对真实攻击力的影响'
              , Dict[str, object], float
              , lambda p: (p['攻击等级'] + 2.0)/2 if p['攻击等级'] > 0 else 2.0 / (2 - p['攻击等级']))

BattleNumeric('atkStateFactor', 'atkStateFactor', '异常状态对真实攻击力的影响'
              , Dict[str, object], float
              , lambda p: 0.5 if BattleNumeric.Count('bured', p) else 1.0)

BattleNumeric('realAtk', 'realAtk', '真实攻击力'
              , Dict[str, object], int
              , lambda p:int(BattleNumeric.Count('atkStateFactor', p) * BattleNumeric.Count('atkLevelFactor', p) * p['攻击']))

BattleNumeric('dfcLevelFactor', 'dfcLevelFactor', '防御等级对真实防御力的影响'
              , Dict[str, object], float
              , lambda p: (p['防御等级'] + 2.0)/2 if p['防御等级'] > 0 else 2.0 / (2 - p['防御等级']))

BattleNumeric('realDfc', 'realDfc', '真实防御力'
              , Dict[str, object], int
              , lambda p:int(BattleNumeric.Count('dfcLevelFactor', p) * p['防御']))

BattleNumeric('protected', 'protected', '被保护'
              , Dict[str, object], bool
              , lambda p:p.get('保护'))

BattleNumeric('protectTired', 'protectTired', '保护疲劳'
              , Dict[str, object], bool
              , lambda p:p.get('保护疲劳'))

BattleNumeric('canBeHited', 'hitable', '可被攻击'
              , Dict[str, object], bool
              , lambda p:BattleNumeric.Count('alive', p) and BattleNumeric.Count('canBeChoiced', p) and (not BattleNumeric.Count('protected', p)))

BattleNumeric('canHit', 'hitable', '可攻击'
              , Dict[str, object], bool
              , lambda p:BattleNumeric.Count('alive', p) and BattleNumeric.Count('canMove', p))

BattleNumeric('bured', 'bured', '被烧伤'
              , Dict[str, object], bool
              , lambda p:p['烧伤'])

BattleNumeric('sleeping', 'sleeping', '睡眠中'
              , Dict[str, object], bool
              , lambda p:p['睡眠'])



