import pygame
import numpy
import constants as c


class Cell(pygame.sprite.Sprite):
    def __init__(self, name: str, num: int, x: int, y: int, h: int, w: int):
        """
        Initializes sprite functionality and sets instance variables for name of cell,
        the cell number, the x coordinate, y coordinate height and width of the cell's
        rectangle object, and sets cells transparency to change based on sound input

        :param name: str
        :param num: int
        :param x: int
        :param y: int
        :param h: int
        :param w: int
        """
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.num = num
        self.image = pygame.Surface((h, w))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.h = h
        self.rect.w = w
        self.color = c.GRAY
        self.alpha = 255
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)

    def update(self):
        """
        calls get_rand_color function and sets color of cell to result of function

        :return: None
        """
        self.color = self.get_rand_color()
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)
        return

    def get_rand_color(self):
        """
        sets color minimum, and generates random tuple values to set color of cells to random color, if the tuple generated is lower
        than the color minimum, the random number generator produces a maximum of 10 other values, if none of these values are greater
        than the color minimum, the color generated is accepted and displayed

        :return: tuple
        """
        color_min = 200
        self.color = list(numpy.random.randint(0, 255, 3))
        i = 0
        while sum(self.color) < color_min:
            self.color = list(numpy.random.randint(10, 255, 3))
            if i == 10:
                break
            i += 1
        return self.color
