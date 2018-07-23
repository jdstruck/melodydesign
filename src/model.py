import pygame
import numpy
from src import constants as c
project="Original"


class Grid(object):
    def __init__(self):
        # Create grid to overlay pads
        self.rows = 0
        self.cols = 0
        self.cell_h = 0
        self.cell_w = 0
        self.matrix = []
        self.color = c.GRAY

    def populate(self, grid_dimensions, cell_dimensions):
        self.rows, self.cols = grid_dimensions
        self.cell_h, self.cell_w = cell_dimensions
        sep = 2 if sum(grid_dimensions) < 20 else 1
        print(sep, grid_dimensions)
        y = 0
        for i in range(self.rows):
            x = 0
            self.matrix.append([])
            for j in range(self.cols):
                h = self.cell_h - sep
                w = self.cell_w - sep
                self.matrix[i].append(Cell(x, y, h, w))
                x += self.cell_w
            y += self.cell_h

    def __str__(self):
        result = ""
        for i in range(len(self.matrix)):
            # result += "R" + str(i+1)
            for j in range(len(self.matrix[i])):
                x = str(self.matrix[i][j].x)
                y = str(self.matrix[i][j].y)
                result += "(" + str(x) + "," + str(y) + ") "
            result += "\n"
        return result


class Cell(object):
    def __init__(self, x, y, h, w):
        # Create rect to represent the synth pad
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.rect = pygame.Rect(self.x, self.y, self.h, self.w)
        self.color = c.GRAY

    def update(self):
        color_min = 200
        rand_color = numpy.random.randint(0, 255, 3)
        # print(rand_color, sum(rand_color))
        i = 0
        if sum(rand_color) < color_min:
            while sum(rand_color) < color_min:
                # print("Color attempt " + str(i) + ": ", rand_color, sum(rand_color))
                rand_color = numpy.random.randint(10, 255, 3)
                if i == 10:
                    break
                i += 1
        # print("Accepted color: " + str(rand_color), sum(rand_color), "\n")
        self.color = rand_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
