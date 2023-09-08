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
上述的核心部分的代码在项目目录下的 *gear/* 路径下，这些代码并非一个可运行的回合制战斗代码，而是定义一个回合制战斗可以用到的通用抽象数据结构的集合。  
如果把回合制战斗代码比作一台机器，那么 *gear/* 路径下的的代码就像一颗颗齿轮，你可以用这些齿轮组装出各种各样的机器，这也正是 TBBG 的原意。  
为了让使用者对 TBBG 能有一个更直观的了解， *examples/* 路径下有几组示例代码，运行这些代码，你会知道 TBBG 是如何工作的。  
在 *SourceFile/* 路径下，是一些图片、文本等资源文件。  
*TurnBaseGear.py* 是 *examples/* 路径下示例代码的启动文件，在 windows 系统中，你可以通过运行 *windowsBoot.bat* 来启动示例，更具体的过程见下一节。  
# 

