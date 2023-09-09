
from typing import Dict, List, Callable


class MoveAttribute(Dict[str, object]):
    '''
    技能的属性条目
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


MoveAttribute('id', 'id', '', '未定义')
MoveAttribute('名字', '名字', '', '未命名')
MoveAttribute('描述', '描述', '', 10, 0, 99999)
MoveAttribute('效果', '效果', '', 100, 0, 99999)
MoveAttribute('威力', '威力', '', 100, 0, 99999)
MoveAttribute('效果参数', '效果参数', '', 0, -6, 6)
MoveAttribute('类型', '类型', '', 0, -6, 6)
MoveAttribute('目标类型', '目标类型', '', '未命名')
MoveAttribute('ai目标类型', 'ai目标类型', '', '正常')
MoveAttribute('接触', '接触', '', [])
MoveAttribute('先制等级', '先制等级', '', False)
