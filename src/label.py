import pygame
import constants as c


class Label(pygame.sprite.Sprite):
    def __init__(self, name: str, x: float, y: float, h: float, w: float, font_size: int):
        """
        Initializes sprite functionality of the label class and sets instance varibales for the name, x coordinate, y coordinate,
        width, and font size of the rectangle object(text object)

        :param name: str
        :param x: float
        :param y: float
        :param h: float
        :param w: float
        :param font_size: int
        """
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.width = w
        self.height = h
        self.font_size = font_size
        font = pygame.font.SysFont("Arial", self.font_size)
        self.image = font.render(self.name, 1, c.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
