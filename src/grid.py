import pygame
import constants as c


class Grid():
    def __init__(self):
        """
        initializes the grid class and sets variable default values
        """
        # Create grid to overlay pads
        self.rows = 0
        self.cols = 0
        self.cell_h = 0
        self.cell_w = 0
        self.matrix = []
        self.color = c.GRAY

    def __str__(self):
        """
        overwrites default print string method
        return: result(str)
        """
        result = ""
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                x = str(self.matrix[i][j].x)
                y = str(self.matrix[i][j].y)
                result += "(" + str(x) + "," + str(y) + ") "
            result += "\n"
        return result


class GridCell(pygame.sprite.Sprite):
    def __init__(self, name, x, y, h, w):
        """
        initializes GridCell sprite functionality and creates instance variables for the name, x coordinate, y coordinate,
        height, and width of the rectangle, the color of the rectangle is set to gray
        args: x(int), y(int), h(int), w(init)
        """
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.Surface((h, w))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.h = h
        self.rect.w = w
        self.color = c.GRAY
        self.alpha = 200
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)

    def draw(self, screen):
        """
        draws the rectangle object on screen
        """
        pygame.draw.rect(screen, self.image.fill(self.color), self.rect, width=2)
