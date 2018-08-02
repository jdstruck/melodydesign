import pygame
import pygame.freetype
import constants as c


class Slider(pygame.sprite.Sprite):
    """
    Initializes sprite functionality of slider class and sets instance variables for the name, value of the slider, minimum value
    and maximum value the slider is set to, x coordinate, y coordinate, height and width of rectangle object
    args: name(str), value(int), min(int), max(int), x(int), y(int), h(int), w(int)
    """
    active = ""

    def __init__(self, name: str, value: float,
                 x: float, y: float, h: float, w: float):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.width = w
        self.height = h
        self.value = value
        self.max = max
        self.min = min
        self.active = False
        self.image = pygame.Surface((self.width, self.height))
        self.color = (100, 160, 200)
        self.image.fill(self.color) # (100,200,200))
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.font_dest = self.width/2-8, self.height/2-5
        self.font_text = str(round(float(self.value), 2))
        # self.font_y = self.height/2-5
        self.font = pygame.freetype.SysFont("Arial", 12)
        self.font.render_to(self.image, dest=self.font_dest, text=self.font_text,
                            bgcolor=self.color, fgcolor=c.WHITE)
