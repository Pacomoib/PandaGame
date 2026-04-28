from direct.showbase.ShowBase import ShowBase
from M5L3PyPro_Manager import Mapmanager
from M5L3PyPro_Hero import Hero


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager()
        self.land.loadLand("land.txt")
        base.camLens.setFov(90)
        self.hero = Hero((2, 2, 3), self.land)


game = Game()
game.run()