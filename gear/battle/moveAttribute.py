
from typing import Dict, List, Callable


class MoveAttribute(Dict[str, object]):
    '''
    技能的属性条目
    '''

    inses = {}
    defaultValues:Dict[str, object] = {}


    def __init__(self, id:str, name:str, desc, defaultValue):
        '''
        '''
        super().__init__()
        self.id = id
        self.name = name
        self.defaultValue = defaultValue
        self.desc = desc
        self.min = min
        self.max = max
        
        MoveAttribute.inses[self.id] = self
        MoveAttribute.defaultValues[self.id] = self.defaultValue
        return


MoveAttribute('id', 'id', '', '未定义')
MoveAttribute('名字', '名字', '', '未命名')
MoveAttribute('描述', '描述', '', '')
MoveAttribute('效果', '效果', '', '')
MoveAttribute('威力', '威力', '', 0)
MoveAttribute('效果参数', '效果参数', '', 0.0)
MoveAttribute('类型', '类型', '', 'hit')
MoveAttribute('目标类型', '目标类型', '', 'enermy')
MoveAttribute('ai目标类型', 'ai目标类型', '', 'enermy')
MoveAttribute('接触', '接触', '', False)
MoveAttribute('先制等级', '先制等级', '', 0)
MoveAttribute('命中率', '命中率', '', 100)
