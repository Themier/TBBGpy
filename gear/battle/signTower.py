
from typing import List, Dict, Callable

class BackSign(Dict[str, any]):
    '''
    反馈信号
    通过反馈信号，接受信号的一方可以向发信方传递信息
    '''

    def __init__(self, initValue=None):
        super().__init__()
        self.value = initValue



class SignTower(dict):
    '''
        信号塔

        单例
        接受一个包含参数 subject:str 和值 value:any 的信号，将所有在 subject 下注册的函数调用
        如果 value 为 None，调用函数时不赋予参数
        如果 value 为 tuple，以 tuple 作为函数的参数列表
        否则，以 value 为 函数的参数
    '''

    ins = None

    def __init__(self):
        super().__init__()
        if SignTower.ins == None:
            SignTower.ins = self


    def Regist(self, subject:str, f:Callable):
        if not subject in self:
            self[subject] = [f]
        else:
            if not f in self[subject]:
                self[subject].append(f)

        return


    def Disregist(self, subject:str, f:Callable):
        if subject in self:
            if f in self[subject]:
                self[subject].remove(f)

        return


    def Push(self, subject:str, value=None):
        if value == None:
            print(f"{subject}")
        else:
            print(f"{subject}  :  {value}")
        if subject in self:
            for f in self[subject]:
                if value == None:
                    f()
                elif isinstance(value, tuple):
                    f(*value)
                else:
                    f(value)

        return


SignTower()
