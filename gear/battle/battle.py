
from .battleUnit import BattleUnit
from .battleGroup import BattleGroup
from .battleNumeric import BattleNumeric
from typing import Dict, List

class Battle(Dict[str, object]):
    '''
    一个回合制战斗

    属性：
	    角色字典    { id : BattleUnit, ... }
	    角色阵营字典  { id : BattleGroup, ... }
    方法：
	    判断阵营是否存在
	    添加阵营
	    判断角色是否存在
	    添加角色
        判断一个角色是否存活
	    检查一个阵营是否还有人存活
	    检查战斗是否已经结束
	    获取一个角色所属的阵营
	    获取指定阵营以外的全部阵营
	    从一个阵营中随机获取一个角色
	    从一个阵营中随机获取一个指定大小的角色列表
	    获取一个角色的战斗信息
    '''

    ins = None

    def __init__(self, *a, **k):
        super().__init__()
        if Battle.ins == None:
            Battle.ins = self

            self['roleDict']:Dict[str, BattleUnit] = {}
            self['groupDict']:Dict[str, BattleGroup] = {}

            self['activedNumPerSide'] = 1
            self['activedGroups'] = []
            self['activedRoles']:List[str] = []
            self['activedRolesLocation'] = {}

        return


    def GroupExist(self, groupId:str)->bool:
        '''
        '''
        return groupId in self['groupDict']


    def AddGroup(self, group:BattleGroup, *a, **k):
        '''
        添加一个阵营
        '''
        if not self.GroupExist(group['id']):
            self['groupDict'][group['id']] = group

        return


    def GetGroups(self)->List[str]:
        '''
        '''
        return list(self['groupDict'].keys())


    def RoleExist(self, roleId:str)->bool:
        '''
        '''
        return roleId in self['roleDict']


    def AddRole(self, role:BattleUnit, groupId:str, *a, **k):
        '''
        添加一个角色
        '''
        if not self.RoleExist(role['id']):
            if self.GroupExist(groupId):
                self['roleDict'][role['id']] = role
                self['groupDict'][groupId].AddRole(role['id'])

        return


    def GetRoles(self, groupId=None)->List[str]:
        '''
        '''
        if groupId == None:
            return list(self['roleDict'].keys())
        elif isinstance(groupId, str):
            group =self['groupDict'].get(groupId, None)
            if group==None:
                return []
            else:
                return group['roles']
        elif isinstance(groupId, list):
            roles = []
            for igroupId in groupId:
                roles.append(self.GetRoles(igroupId))
            return roles

        return []


    def GetActivedRoles(self)->List[str]:
        '''
        '''
        return list(self['activedRoles'])


    def RoleIsActived(self, roleId:str)->bool:
        '''
        '''
        return roleId in self.GetActivedRoles()


    def SetActiveRole(self, roleId:str):
        '''
        '''
        if not self.RoleIsActived(roleId):
            self['activedRoles'].append(roleId)
            self['activedRoles'].sort(key=lambda id:self.GetBattleUnit(id)['速度'], reverse=True)

        return


    def UnsetActiveRole(self, roleId:str):
        '''
        '''
        if self.RoleIsActived(roleId):
            self['activedRoles'].remove(roleId)

        return


    def GetGroupOfRole(self, roleId:str, *a, **k)->str:
        '''
        返回指定角色所属的阵营
        '''
        for igroup in self['groupDict']:
            if roleId in self['groupDict'][igroup]['roles']:
                return igroup

        return None


    def GetOtherGroups(self, groupId:str, *a, **k)->List[str]:
        '''
        返回除给定阵营外其余全部阵营的名字
        '''
        groups = []
        for igroup in self['groupDict']:
            if igroup == groupId:
                continue
            groups.append(igroup)

        return groups


    def GetRandomRole(self, groupId:str, *a, **k)->str:
        '''
        从指定阵营中取出随机角色
        '''
        if groupId in self['groupDict']:
            return choice(self['groupDict'][groupId]['roles'])

        return None


    def GetRandomRoles(self, groupId:str, num:int, *a, **k)->List[str]:
        '''
        从指定阵营中取出随机角色列表
        '''
        if groupId in self['groupDict']:
            return sample(self['groupDict'][groupId]['roles'], num)

        return None


    def GetBattleUnit(self, roleId:str, *a, **k)->BattleUnit:
        '''
        获取一个角色的 BattleUnit
        '''
        return self['roleDict'].get(roleId, None)


    def GetBattleGroup(self, groupId:str, *a, **k)->BattleUnit:
        '''
        '''
        return self['groupDict'].get(groupId, None)


Battle()



