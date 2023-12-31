# TBBGpy
Turn Based Battle Gear with python
# 目录
* [简介](https://github.com/Themier/TBBGpy/blob/main/README.md#%E7%AE%80%E4%BB%8B)
* [项目结构](https://github.com/Themier/TBBGpy/blob/main/README.md#%E9%A1%B9%E7%9B%AE%E7%BB%93%E6%9E%84)
* [安装和运行](https://github.com/Themier/TBBGpy/blob/main/README.md#%E5%AE%89%E8%A3%85%E5%92%8C%E8%BF%90%E8%A1%8C)
* [文档和帮助](https://github.com/Themier/TBBGpy/blob/main/README.md#%E6%96%87%E6%A1%A3%E5%92%8C%E5%B8%AE%E5%8A%A9)
* [未来计划](https://github.com/Themier/TBBGpy/blob/main/README.md#%E6%9C%AA%E6%9D%A5%E8%AE%A1%E5%88%92)
# 简介
## TBBG
TBBG 是一个回合制战斗系统框架项目，TBBG 的目标是实现一个通用的回合制战斗框架，在这个框架的基础上，使用者可以轻易地快速实现任何规则下的回合制战斗的核心模块代码，并实现逻辑与 ui 分离。  
## TBBGpy
将回合制战斗抽象化并建立一个通用模型不是一个十分简单的事情，因此，TBBG 现阶段的重心是逻辑验证和可行性验证，考虑到这一点，数据类型更自由、语法更灵活的 python 语言比 cpp 等语言更合适，因此，现阶段的 TBBG 将采用 python 语言来完成，也就是 TBBGpy。  
未来，TBBGpy 将通过 Cpp 或 C# 重写，那时的 TBBG 将可以与 Unity、UE 等引擎一同工作。  
# 项目结构
TBBG 的核心是回合制战斗的逻辑处理，具体来说，就是战斗过程中各种数据的定义、生成和互动，而不包括与图形界面有关的输入和输出。  
上述的核心部分的代码在项目目录下的 *gear/* 路径下，这些代码并非一个可运行的回合制战斗代码，而是定义一个回合制战斗所需的数据类型和方法的集合。  
如果把回合制战斗代码比作一台机器，那么 *gear/* 路径下的的代码就像一颗颗齿轮，你可以用这些齿轮组装出各种各样的机器，这也正是 TBBG 的原意。  
为了让使用者对 TBBG 能有一个更直观的了解， *examples/* 路径下有几组示例代码，运行这些代码，你会看到 TBBG 是如何工作的。  
在 *SourceFile/* 路径下，是一些图片、文本等资源文件。  
你可以在 *Documents/* 路径下找到更多的帮助信息。  
*TurnBaseGear.py* 是示例代码的启动文件，在 windows 系统中，你可以通过运行 *windowsBoot.bat* 来启动示例，更具体的过程见下一节。  
# 安装和运行
# 安装
TBBGpy 无需安装，你只需要将代码 clone 到本地或你的云端机器即可。  
# 运行
注意，TBBG 的核心代码并无程序入口，这里说的运行，是指运行 *examples/* 路径下的示例。  
在运行示例之前，你需要确保你已安装 python 和 pyQt，你需要后者是因为有些示例需要 pyQt 库来提供图形界面。  
确保你的环境已经准备好了之后，在项目根路径下使用 *python TurnBaseGear.py* 来运行示例。  
如果你使用 window 系统，那么你也可以通过双击  *windowsBoot.bat* 来直接运行示例。  
# 文档和帮助
你可以在 *Documents/* 路径下找到更多的帮助信息。  
# 未来计划
* 为了让代码的开发更有目标，我选择了一些有代表性的回合制战斗系统，TBBG 的初期开发将朝着能够模拟这些战斗系统的目标前进。我的第一个学习对象是宝可梦，第二个？或许是星穹铁道或博德之门吧。  
* 我需要一些时间整理和重构现有的代码，使它们更健康和灵活。
* 在上述两点的工作取得足够的成效后，我会开始考虑将 TBBGpy 移植到 Cpp 或 C# 上，那时，TBBG 将可以与 Unit 等更成熟的游戏引擎协同工作，获得更多的可能性。


