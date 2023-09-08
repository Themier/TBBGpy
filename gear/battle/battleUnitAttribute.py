
from typing import Dict, List, Callable


class BattleUnitAttribute(Dict[str, object]):
    '''
    战斗单元的属性
    不与具体的战斗单元绑定，而是一种客观存在
    '''

    inses = {}
    defaultValues:Dict[str, object] = {}


    def __init__(self, id:str, name:str, desc, defaultValue, min=None, max=None):
        '''
        '''
        super().__init__()
        self.id = id
        self.name = name
        self.defaultValue = defaultValue
        self.desc = desc
        self.min = min
        self.max = max
        
        BattleUnitAttribute.inses[id] = self
        BattleUnitAttribute.defaultValues[id] = self.defaultValue
        return


BattleUnitAttribute('攻击', '攻击', '', 10, 0, 99999)
BattleUnitAttribute('防御', '防御', '', 10, 0, 99999)
BattleUnitAttribute('速度', '速度', '', 10, 0, 99999)
BattleUnitAttribute('hp', 'hp', '', 100, 0, 99999)
BattleUnitAttribute('最大Hp', '最大Hp', '', 100, 0, 99999)
BattleUnitAttribute('攻击等级', '攻击等级', '', 0, -6, 6)
BattleUnitAttribute('防御等级', '防御等级', '', 0, -6, 6)
BattleUnitAttribute('名字', '名字', '', '未命名')
BattleUnitAttribute('AIType', 'AIType', '', '正常')
BattleUnitAttribute('技能', '技能', '', [])
BattleUnitAttribute('保护', '保护', '', False)
BattleUnitAttribute('保护疲劳', '保护疲劳', '', False)
BattleUnitAttribute('最后受伤值', '最后受伤值', '', 0)
BattleUnitAttribute('最后受伤来自', '最后受伤来自', '', '')
BattleUnitAttribute('烧伤', '烧伤', '', False)
BattleUnitAttribute('睡眠', '睡眠', '', False)
