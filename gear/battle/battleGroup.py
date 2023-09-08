
from typing import List, Dict



class BattleGroup(Dict[str, object]):

    counter:int =0

    def __init__(self, initValue:Dict[str, object], *a, **k):
        super().__init__()
        
        self.update({'roles':[], '名字':'未命名'})
        self.update(initValue)

        self['id'] = str(BattleGroup.counter)
        BattleGroup.counter += 1

        return


    def RoleExsits(self, roleId:str):
        return roleId in self['roles']


    def AddRole(self, roleId:str):
        if not self.RoleExsits(roleId):
            self['roles'].append(roleId)

        return


    def RemoveRole(self, roleId:str):
        if self.RoleExsits(roleId):
            self['roles'].remove(roleId)

        return


