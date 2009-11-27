
from math import atan2

from spriteitem import SpriteItem


GRAVITY = 0.2
LEFT, RIGHT = 'L', 'R'


class WorldItem(SpriteItem):

    AIR_RESIST = 0.98

    is_player = False
    is_enemy = False
    is_feather = False
    can_fall_off = False


    def __init__(self, x=0, y=0, dx=0, dy=0):
        SpriteItem.__init__(self, x, y)
        self.dx = dx
        self.dy = dy
        self.ddx = 0
        self.ddy = 0


    def update(self):
        self.dx += self.ddx
        self.dx *= self.AIR_RESIST
        self.dy += self.ddy - GRAVITY
        self.dy *= self.AIR_RESIST
        self.ddx = 0
        self.ddy = 0
        self.x += self.dx
        self.y += self.dy
        self.test_for_fall_off_screen()


    def test_for_fall_off_screen(self):
        if self.can_fall_off:
            if self.y < -self.height / 2:
                self.remove_from_game = True
        else:
            if self.y < self.height / 2:
                self.y = self.height / 2
                self.dy = abs(self.dy) * 0.5

