
from pyglet import clock

from collision import Collision
from enemy import Enemy
from event import Event
from gamecontrols import GameControls
from gameitem import GameItem
from ground import Ground
from hudmessage import HudMessage
from hudscore import HudScore
from hudtitle import HudTitle
from hudinstructions import HudInstructions
from player import Player
from sky import Sky
from typebag import TypeBag
from worlditem import WorldItem



class Game(object):

    def __init__(self, win):
        self.win = win
        self.width = win.width
        self.height = win.height
        self.wave = 0
        self.gamecontrols = None
        self._items = TypeBag()
        self.item_added = Event()
        self.item_removed = Event()
        self.collision = Collision()
        GameItem.game = self


    def __iter__(self):
        return iter(self._items)


    def add(self, item):
        self._items.add(item)

        item.added()

        # TODO: can we impliemtn all of these in item.added() methods?
        if hasattr(item, 'on_key_press'):
            self.win.push_handlers(item)

        self.item_added(item)


    def remove(self, item=None, itemid=None):
        assert (item is None) ^ (itemid is None)
        if item is None:
            item = self._items[itemid]
        self._items.remove(item)

        item.removed()

        # TODO: can we impliemtn all of these in item.removed() methods?
        if hasattr(item, 'on_key_press'):
            self.win.remove_handlers(item)
        if isinstance(item, Player):
            clock.schedule_once(lambda _: self.get_ready(), 1.5)

        self.item_removed(item)


    def init(self):
        self.add(Sky())
        self.add(Ground())
        self.add(HudTitle())
        self.gamecontrols = GameControls()
        self.add(self.gamecontrols)
        clock.schedule(self.update)


    def start(self):
        self.get_ready()

        # TODO: probably all WorldItems need to know win.width/height
        # as a class attribute, so we don't have to pass these in all over
        self.add(HudInstructions(self, self.win.width, self.win.height))
        Player.score = 0
        clock.schedule_once(lambda _: self.add(HudScore()), 1)
        clock.schedule_once(lambda _: self.spawn_wave(), 3)


    def get_ready(self):
        self.add(HudMessage('Get Ready!', 36))
        clock.schedule_once(lambda _: Player.spawn(self), 1)


    def spawn_wave(self):
        self.wave += 1
        self.add(HudMessage('Wave %d' % (self.wave,), 36))

        number = self.wave ** 2
        for n in xrange(number):
            clock.schedule_once(
                lambda _: Enemy.spawn(self),
                n * 0.25)


    def wraparound(self, item):
        if item.x < -item.width / 2:
            item.x += self.win.width + item.width
        if item.x > self.win.width + item.width / 2:
            item.x -= self.win.width + item.width


    def update(self, _):
        self.gamecontrols.update()

        to_remove = set()
        for item in self._items:
            item.update()
            if item.remove_from_game:
                to_remove.add(id(item))
            # TODO, can we find a way to iterate through WorldItems?
            if isinstance(item, WorldItem):
                self.wraparound(item)

        for itemid in to_remove:
            self.remove(itemid=itemid)

        self.collision.detect(self._items)

