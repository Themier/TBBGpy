
from typing import Dict, List, Callable
import pandas


class Move(Dict[str, object]):
    '''
    一个技能对象储存了相应技能全部必要信息
    这些技能对象在游戏启动时从资源文件中读取信息并实例化，在游戏的过程中一般不改变
    技能的 id 也是从资源文件中读取的，因此可能出现重复，后加载的同id技能会覆盖早加载的

    技能类型：hit / affect
    目标选取类型：none / enermy / aly / our / exceptSelf / any
    '''

    moveDict = {}


    def __init__(self, initValue:Dict[str, object]):
        super().__init__()

        self.update({
            'id':'未定义'
            , '名字':'未命名'
            , '描述':'默认描述'
            , '效果':''
            , '威力':1, '效果参数':0.0
            , '类型':'hit'
            , '目标类型':'enermy', 'ai目标类型':'enermy'
            , '接触':False
            , '先制等级':0
            })
        self.update(initValue)

        Move.moveDict[self['id']] = self
        return


Move({'id':'击打', '名字':'击打'
            , '描述':'默认描述'
            , '效果':'单体攻击', '威力':40, '效果参数':0.0
            , '类型':'hit', '目标类型':'exceptSelf', 'ai目标类型':'enermy'
            , '接触':True, '先制等级':0})

Move({'id':'保护', '名字':'保护'
            , '描述':'默认描述'
            , '效果':'自我保护', '威力':0, '效果参数':0.0
            , '类型':'affect', '目标类型':'none', 'ai目标类型':'none'
            , '接触':False, '先制等级':5})

Move({'id':'自愈', '名字':'自愈'
            , '描述':'默认描述'
            , '效果':'自我治愈', '威力':0, '效果参数':0.5
            , '类型':'affect', '目标类型':'none', 'ai目标类型':'none'
            , '接触':False, '先制等级':0})

Move({'id':'魔法火焰', '名字':'魔法火焰'
            , '描述':'默认描述'
            , '效果':'单体攻击减攻', '威力':20, '效果参数':1.0
            , '类型':'hit', '目标类型':'exceptSelf', 'ai目标类型':'enermy'
            , '接触':False, '先制等级':0})

Move({'id':'鬼火', '名字':'鬼火'
            , '描述':'默认描述'
            , '效果':'单体烧伤', '威力':0, '效果参数':0.0
            , '类型':'affect', '目标类型':'exceptSelf', 'ai目标类型':'enermy'
            , '接触':False, '先制等级':0})
