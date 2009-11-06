
import math

from itertools import islice
from random import randint, uniform

from pyglet import clock, image

from config import settings
from feather import Feather
from gameent import GameEnt
from enemy import Enemy


def is_touching(ent1, ent2):
    distance = math.hypot(
        (ent1.center_x + ent1.x) - (ent2.center_x + ent2.x),
        (ent1.center_y + ent1.y) - (ent2.center_y + ent2.y)
    )
    if distance < max(ent1.width, ent2.width) * 0.8:
        return True


class World(object):

    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height
        self.age = 0.0
        self.ents = []
        self.num_enemies = 0


    def add(self, ent):
        self.ents.append(ent)
        if isinstance(ent, Enemy):
            self.num_enemies += 1


    def remove(self, ent):
        self.ents.remove(ent)
        if isinstance(ent, Enemy):
            self.num_enemies -= 1
            if self.num_enemies == 0:
                self.app.next_wave()


    def spawn_enemy(self, number, delay, player):
        if player is None:
            x = uniform(0, self.width)
        else:
            x = (player.x + self.width / 2) % self.width
        y = self.height
        dx = uniform(-20, 20)
        dy = 0
        self.add(Enemy(x, y, dx=dx, dy=dy, feathers=number))
        if number > 1:
            clock.schedule_once(
                lambda _: self.spawn_enemy(number - 1, delay, player),
                delay)


    def detect_collisions(self):
        if settings.getboolean('all', 'performance_test'):
            return

        for i, ent1 in enumerate(self.ents):
            for ent2 in islice(self.ents, i+1, None):
                if is_touching(ent1, ent2):
                    ent1.collided_with(ent2)
                    ent2.collided_with(ent1)


    def remove_dead(self):
        for ent in self.ents[:]:
            if ent.remove_from_game:
                self.remove(ent)


    def wraparound(self, ent):
        if ent.x < ent.width:
            ent.x += self.width + ent.width
        if ent.x > self.width:
            ent.x -= self.width + ent.width


    def update_ents(self):
        for ent in self.ents:
            ent.update()
            self.wraparound(ent)


    def update(self, dt):
        self.age += dt
        self.detect_collisions()
        self.remove_dead()
        self.update_ents()
