
from glob import glob

from pyglet import resource
from pyglet.sprite import Sprite

from behaviour import Action
from feather import Feather
from gameent import GameEnt, LEFT, RIGHT


GLIDE_STEER = 0.1
FLAP_STEER = 3
FLAP_LIFT = 5


class Bird(GameEnt):

    def __init__(self, x, y, dx=0, dy=0, feathers=3):
        GameEnt.__init__(self, x, y, dx, dy)
        self.feathers = feathers
        if self.dx < 0:
            self.facing = LEFT
        else:
            self.facing = RIGHT
        self.can_flap = True
        self.last_flap = None
        self.is_alive = True
        self.actions = set()
        self.foe = None


    def reincarnate(self, x, y, feathers=3):
        GameEnt.reincarnate(self, x, y)
        self.feathers = feathers
        self.can_fall_off = False


    def act(self):
        if Action.FLAP in self.actions:
            if self.can_flap:
                self.dy += FLAP_LIFT
                self.last_flap = 0
                self.can_flap = False
        else:
            self.can_flap = True

        ddx = GLIDE_STEER
        if self.last_flap == 0:
            ddx = FLAP_STEER

        if Action.LEFT in self.actions:
            self.dx -= ddx
            self.facing = LEFT
        if Action.RIGHT in self.actions:
            self.dx += ddx
            self.facing = RIGHT


    def update(self):
        GameEnt.update(self)
        self.actions = self.think()
        self.act()
        if self.last_flap is not None:
            self.last_flap += 1


    def lose_feather(self, otherx, othery):
        self.feathers -= 1
        feather = Feather(
            self.x, self.y,
            *self.get_collision_opposite(otherx, othery),
            owner=self)
        self.level.add(feather)

        if self.feathers == 0:
            self.die()


    def get_collision_opposite(self, otherx, othery):
        directionx = self.x - otherx
        directiony = self.y - othery
        return self.dx + directionx / 3.0, self.dy + directiony / 5.0


    def die(self):
        self.is_alive = False
        self.can_fall_off = True


    def collided_with(self, other):
        if self.is_alive:
            if other.is_player or other.is_enemy:
                if other.is_alive:
                    GameEnt.collided_with(self, other)
                    if self.y < other.y:
                        self.foe = other
                        if other.is_enemy != self.is_enemy:
                            self.lose_feather(other.x, other.y)
            elif other.is_feather and other.owner is not self:
                other.remove_from_game = True
                self.feathers += 1


    def animate(self):
        action = 'flight' if self.is_alive else 'dead'
        flapping = (
            self.is_alive and (
                (self.last_flap is not None
                 and self.last_flap < 5)
                or Action.FLAP in self.actions)
        )
        if flapping:
            action = 'flap'

        self.sprite.rotation = self.dx * 3

        frame = '%s-%s-%s' % (type(self).__name__, action, self.facing,)
        self.sprite.image = self.sprite_images[frame]
        self.update_sprite_stats()
