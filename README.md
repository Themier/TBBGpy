# TBBGpy
Turn Based Battle Gear with python
# 简介
## TBBG
TBBG 是一个回合制战斗系统框架项目，TBBG 的最终目标是实现一个通用的回合制战斗框架，在这个框架的基础上，使用者可以轻易地实现任何规则的回合制战斗的核心代码。  
## TBBGpy
将回合制战斗抽象化并建立一个通用模型不是一个简单的事情，因此，TBBG 现阶段的重心是逻辑验证和可行性验证，考虑到这一点，数据类型更自由、语法更简单的 python 语言比 cpp 等语言更合适，因此，现阶段的 TBBG 将采用 python 语言来完成，也就是 TBBGpy。  
未来，TBBGpy 将通过 Cpp 或 C# 重写。  
# 项目结构
TBBG 的核心是回合制战斗的逻辑处理，具体来说，就是战斗过程中各种数据的定义、生成和互动，而不包括图形界面的输入和输出。  
上述的核心部分的代码在项目目录下的 *gear/* 路径下，这些代码并非一个可运行的回合制战斗代码，而是定义一个回合制战斗可以用到的抽象数据结构的集合。  
如果把回合制战斗代码比作一台机器，那么 *gear/* 路径下的的代码就像一颗颗齿轮，你可以用这些齿轮组装出各种各样的机器，这也正是 TBBG 的原意。  
为了让使用者对 TBBG 能有一个更直观的了解， *examples/* 路径下有几组示例代码，运行这些代码，你会知道 TBBG 是如何工作的。  
在 *SourceFile/* 路径下，是一些图片、文本等资源文件。  
使用者可以在 *Documents/* 路径下找到更多的帮助信息。  
*TurnBaseGear.py* 是 *examples/* 路径下的示例代码的启动文件，在 windows 系统中，你可以通过运行 *windowsBoot.bat* 来启动示例，更具体的过程见下一节。  
# 安装和运行
# 安装
TBBGpy 无需安装，你只需要将代码 clone 到本地或你的云端机器即可。  
# 运行
注意，TBBG 的核心代码并无程序入口，这里说的运行，是指运行 *examples/* 路径下的示例。  
在运行示例之前，你需要确保你已安装 python 和 pyQt，你需要后者是因为有些示例需要 pyQt 库来提供图形界面。  
确保你的环境已经准备好了之后，在项目根路径下使用 *python TurnBaseGear.py* 来运行示例。  
如果你使用 window 系统，那么你可以通过双击  *windowsBoot.bat* 来运行示例。  
# 文档和帮助
使用者可以在 *Documents/* 路径下找到更多的帮助信息。  
# 未来计划
* 为了让代码的开发更有目标，我选择了一些有代表性的回合制战斗系统，TBBG 的初期开发将朝着能够模拟这些战斗系统的目标前进。我的第一个学习对象是宝可梦，第二个？或许是星穹铁道吧。  
* 我需要大量的时间整理和重构现有的代码，使其能够真正做到抽象化。
* 在宝可梦和新穹铁道的模拟工作，以及代码的抽象工作初步取得成效后，我将考虑将 TBBGpy 移植到 Cpp 或 C# 上，那时，TBBG 将可以与 Unit 协同工作，获得更多的可能性。


