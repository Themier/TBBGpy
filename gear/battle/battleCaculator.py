
import random
from typing import Dict, List, Callable
from .battle import Battle
from .battleUnit import BattleUnit
from .battleNumeric import BattleNumeric


class BattleCalculator():

    @classmethod
    def GroupIsAlive(self, groupId:str):
        '''
        '''
        if Battle.ins.GroupExist(groupId):
            for roleId in Battle.ins.GetRoles(groupId):
                if BattleNumeric.Count('alive',Battle.ins.GetBattleUnit(roleId)):
                    return True

        return False


    @classmethod
    def BattleIsOver(self)->bool:
        '''
        '''
        nAlive = 0
        for gruopId in Battle.ins.GetGroups():
            if self.GroupIsAlive(gruopId):
                nAlive += 1
                if nAlive > 1:
                    return False

        return True


    @classmethod
    def AllActivedGroups(self)->List[str]:
        '''
        '''
        gs = []
        for roleId in Battle.ins['activedRoles']:
            gid = Battle.ins.GetGroupOfRole(roleId)
            if not gid in gs:
                gs.append(gid)

        return gs

    
    @classmethod
    def ActivedAliveRoleNumInGroup(self, groupId:str)->int:
        '''
        '''
        n=0
        for roleId in Battle.ins['activedRoles']:
            if Battle.ins.GetGroupOfRole(roleId) == groupId and BattleNumeric.Count('alive', Battle.ins.GetBattleUnit(roleId)):
                n+=1
        return n

    
    @classmethod
    def UnactivedAliveRoleNumInGroup(self, groupId:str)->int:
        '''
        '''
        n=0
        for roleId in Battle.ins.GetRoles(groupId):
            if (not roleId in Battle.ins['activedRoles']) and BattleNumeric.Count('alive', Battle.ins.GetBattleUnit(roleId)):
                n+=1
        return n


    @classmethod
    def CountDamagePoint(self, atker:BattleUnit, dfcer:BattleUnit, power:int)->int:
        '''
        '''
        atk = BattleNumeric.Count('realAtk', atker)
        dfc = BattleNumeric.Count('realDfc', dfcer)
        damage = int(atk * 1.0 / dfc * power)
        return damage


    @classmethod
    def RandomCheck(self, normalisedProbability:float):
        '''
        '''
        return random.uniform(0,1) < normalisedProbability


    @classmethod
    def CheckMoveScore(self, move:Dict[str, object]):
        '''
        '''
        return self.RandomCheck(move['命中率'] / 100.0)


    @classmethod
    def GetAllPossibleTargets(self, selectRule:str, moverId:str)->List:
        '''
        '''
        if selectRule == 'none':
            return []
        elif selectRule == 'enermy':
            targets = []
            for groupId in Battle.ins.GetOtherGroups(Battle.ins.GetGroupOfRole(moverId)):
                for roleId in Battle.ins['groupDict'][groupId]['roles']:
                    if roleId in Battle.ins.GetActivedRoles():
                        role = Battle.ins.GetBattleUnit(roleId)
                        if role!= None and BattleNumeric.Count('canBeChoiced', role):
                            targets.append(roleId)
            return targets
        elif selectRule == 'aly':
            targets = []
            for roleId in Battle.ins['groupDict'][Battle.ins.GetGroupOfRole(moverId)]['roles']:
                    if roleId in Battle.ins.GetActivedRoles():
                        if roleId != moverId:
                            role = Battle.ins.GetBattleUnit(roleId)
                            if role!= None and BattleNumeric.Count('canBeChoiced', role):
                                targets.append(roleId)
            return targets
        elif selectRule == 'our':
            targets = []
            for roleId in Battle.ins['groupDict'][Battle.ins.GetGroupOfRole(moverId)]['roles']:
                    if roleId in Battle.ins.GetActivedRoles():
                        role = Battle.ins.GetBattleUnit(roleId)
                        if role!= None and BattleNumeric.Count('canBeChoiced', role):
                            targets.append(roleId)
            return targets
        elif selectRule == 'exceptSelf':
            targets = []
            for roleId in Battle.ins['roleDict']:
                    if roleId in Battle.ins.GetActivedRoles():
                        if roleId != moverId:
                            role = Battle.ins.GetBattleUnit(roleId)
                            if role!= None and BattleNumeric.Count('canBeChoiced', role):
                                targets.append(roleId)
            return targets
        elif selectRule == 'any':
            targets = []
            for roleId in Battle.ins['roleDict']:
                    if roleId in Battle.ins.GetActivedRoles():
                        role = Battle.ins.GetBattleUnit(roleId)
                        if role!= None and BattleNumeric.Count('canBeChoiced', role):
                            targets.append(roleId)
            return targets
        
        return []