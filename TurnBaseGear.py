'''
    动画
'''

if __name__ == '__main__':
    import sys, random, os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    from gear.battle.signTower import SignTower
    from gear.battle.battleUnit import BattleUnit
    from gear.battle.battleGroup import BattleGroup
    from gear.battle.battle import Battle
    from gear.battle.battleProcessor import BattleProcessor

    from ui.battle.battleWindow import BattleWindow

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    bw = BattleWindow()

    app.exec()



