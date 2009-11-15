
from random import uniform

from pyglet import clock

from arena import Arena
from config import settings
from enemy import Enemy
from gameitem import GameItem
from ground import Ground
from hudmessage import HudMessage
from hudscore import HudScore
from hudtitle import HudPressAnyKey
from hudinstructions import HudInstructions
from player import Player
from sky import Sky
from sounds import play


class Game(object):

    def __init__(self, win):
        self.width = win.width
        self.height = win.height
        self.score = 0
        self.num_enemies = 0

        self.arena = Arena(win, self)
        GameItem.arena = self.arena


    def init(self, win):

        self.arena.item_added += self.on_add_item
        self.arena.item_removed += self.on_remove_item

        sky = Sky(self.width, self.height)
        self.arena.add(sky)

        ground = Ground()
        self.arena.add(ground)

        hudtitle = HudPressAnyKey(self, self.width, self.height)
        self.arena.add(hudtitle)

        if settings.getboolean('all', 'performance_test'):
            self.spawn_wave(number=256)

        clock.schedule(self.arena.update)


    def start(self):
        self.get_ready()

        hudscore = HudScore(self, self.width, self.height)
        self.arena.add(hudscore)

        hudinstructions = HudInstructions(
            self, self.width, self.height)
        self.arena.add(hudinstructions)

        clock.schedule_once(lambda _: self.spawn_wave(), 3)


    def get_ready(self):
        self.arena.add(
            HudMessage('Get Ready!',
                self, self.width, self.height))
        clock.schedule_once(lambda _: self.spawn_player(), 2)


    def spawn_player(self):
        player = Player(self.width / 2, self.height, self)
        player.remove_from_game = False
        player.is_alive = True
        self.arena.add(player)


    def spawn_wave(self, number=None):
        if number is None:
            number = 4

        self.arena.add(
            HudMessage('Here they come...',
                self, self.width, self.height))

        for n in xrange(number):
            clock.schedule_once(lambda _: self.spawn_enemy(), 1.7 * n)


    def spawn_enemy(self):
        x = uniform(0, self.width)
        y = self.height + 32
        dx = uniform(-20, 20)
        self.arena.add(Enemy(x, y, dx=dx, dy=0))


    def player_died(self):
        self.arena.add(
            HudMessage('Oh no!',
                self, self.width, self.height))
        play('ohno')
        clock.schedule_once(lambda _: self.get_ready(), 2)


    def on_add_item(self, _, item):
        if isinstance(item, Enemy):
            self.num_enemies += 1


    def on_remove_item(self, _, item):
        if isinstance(item, Enemy):
            self.num_enemies -= 1
            if self.num_enemies == 0:
                self.spawn_wave()

        if isinstance(item, Player):
            self.player_died()

