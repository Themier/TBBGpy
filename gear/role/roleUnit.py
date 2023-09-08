
from typing import Dict, List, Callable


class RoleUnit(Dict[str, object]):
    '''
    一个角色单元
    '''

    count=0


    def __init__(self, initVal:Dict[str, object]={}):
        super().__init__()

        self.update({'攻击':1, '防御':1, '速度':1, 'hp':1, '最大Hp':1, '名字':'未命名', '技能':[], })
        self.update(initVal)
        self['id'] = str(BattleUnit.count)
        BattleUnit.count+=1

        return


    def Update(self, d:Dict[str,object]):
        '''
        更新字典内容
        '''
        d['id']=self['id']
        self.update(d)

        return


    def ChangeValue(self, key:str, change:object, max:object=None, min:object=None):
        '''
        '''
        if not key in self:
            self[key] = 0.0
        self[key]+=change
        if max != None and self[key] > max:
            self[key] = max
        elif min != None and self[key] < min:
            self[key] = min

        return




