
from pyglet import clock
from pyglet.image import create, ImageData
from pyglet.text import Label

from label2texture import label2texture
from spriteitem import SpriteItem


# scores for consecutive feather collections
scores = [5, 10, 25, 50, 100, 250, 500, 1000]


def _text2image(text, size):
    '''
    Create an image of the given score.
    '''
    label = Label(
        text,
        font_size=size,
    )
    return label2texture(label)


class HudPoints(SpriteItem):
    '''
    Represents a number floating in the sky, instanciated whenever the player
    scores some points.

    For performance, we generate bitmaps from Labels on startup, and
    display these during gameplay as sprites.
    '''

    render_layer = 3 # hud
    images = {}

    def __init__(self, x, y, consecutive_feather):
        SpriteItem.__init__(self, x, y)
        excitement = min(consecutive_feather, len(scores) - 1)
        self.frame_idx = excitement
        self.dy = 3 + excitement * 2
        self.opacity = 255


    @classmethod
    def create_images(cls):
        '''
        Generate the bitmaps that will later be used as Sprite images when
        instances of HudPoints get rendered to the screen.
        '''
        for i, score in enumerate(scores):
            image = _text2image(str(score), 16 + i * i)
            image.anchor_x = image.width / 2
            image.anchor_y = image.height / 2
            cls.images[i] = image


    def update(self):
        self.y += self.dy
        self.dy *= 0.9
        self.sprite.opacity = self.opacity
        self.opacity -= 3
        if self.opacity <= 0:
            self.remove_from_game = True

