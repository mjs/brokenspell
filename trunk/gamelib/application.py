
import pyglet
from pyglet.window import key, Window

from config import settings
from game import Game
from music import Music
from render import Render


class Application(object):

    def __init__(self):
        self.win = None
        self.game = None
        self.render = None
        self.music = None


    def launch(self):

        vsync = True
        if settings.getboolean('all', 'performance_test'):
            vsync = False

        self.win = Window(width=1024, height=768, vsync=vsync)
        self.win.set_exclusive_mouse()
        self.win.push_handlers(self)

        self.game = Game(self.win)

        self.render = Render(self.game.arena)
        self.render.init(self.win)

        self.game.init(self.render.images)

        self.music = Music()
        self.music.play()

        pyglet.app.run()


    def on_key_press(self, symbol, _):
        if symbol == key.M:
            self.music.toggle()
        elif symbol == key.ESCAPE:
            self.win.has_exit = True
