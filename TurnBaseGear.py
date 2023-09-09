'''
    宝可梦中技能瞄准的应当是一个位置而非对象
'''

if __name__ == '__main__':
    import sys, random, os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    from gear.battle.signTower import SignTower
    from gear.battle.battleUnit import BattleUnit
    from gear.battle.battleGroup import BattleGroup
    from gear.battle.battle import Battle
    from gear.battle.battleProcessor import BattleProcessor

    from examples.pokemon_like_Qt.ui.battle import BattleWindow

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    bw = BattleWindow()

    app.exec()



