import pygame
import pygame.freetype
import constants as c


class Backgroundreq(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, h: float, w: float,
                 type: int, color: tuple=c.LGRAY, name: str="bg"):
        """
        Initializes sprite functionality for the Backgroundreq class and creates instance variables
        for x coordinate, y coordinate, height, width type, and color of rectangle object

        :param x: float
        :param y: float
        :param h: float
        :param w: float
        :param type: int
        :param color: tuple
        """
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.height = h
        self.width = w
        self.type = type
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
