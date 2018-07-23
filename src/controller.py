import os
import pygame
from src import model
from src import constants as c


class GUI:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption('MelodyDesign')
        # Initialize grid
        self.wh = 5
        # if wh > 10
        self.grid_h = self.wh
        self.grid_w = self.wh
        self.cell_h = c.SCREEN_HEIGHT / self.grid_h
        self.cell_w = self.cell_h
        # Create/populate grid
        self.grid = model.Grid()
        self.grid.populate([self.grid_h, self.grid_w], [self.cell_h, self.cell_w])
        # Initial values
        self.lclick = False
        self.drag = False
        self.x_mouse = 0
        self.y_mouse = 0
        self.prev_cell = None
        self.curr_cell = None
        self.done = False

    def draw_grid(self, screen):
        for i in range(len(self.grid.matrix)):
            for j in range(len(self.grid.matrix[i])):
                self.grid.matrix[i][j].draw(screen)
                # pygame.draw.rect(screen, c.GRAY, self.grid.matrix[i][j])

    def display_frame(self, screen):
        screen.fill(c.BLACK)
        self.draw_grid(screen)
        pygame.display.flip()

    def process_events(self):
        for event in pygame.event.get():
            islmousedown = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            islmouseup = event.type == pygame.MOUSEBUTTONUP and event.button == 1
            ismousemotion = event.type == pygame.MOUSEMOTION
            ismousedrag = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and event.type == pygame.MOUSEMOTION
            if event.type == pygame.QUIT:
                return True
            if islmousedown:
                self.lclick = True
                self.drag = False
            if ismousedrag:
                self.lclick = False
                self.drag = True
            if islmouseup:
                self.lclick = False
                self.drag = False
                return False
            if self.lclick:
                for i in range(len(self.grid.matrix)):
                    for j in range(len(self.grid.matrix[i])):
                        self.curr_cell = self.grid.matrix[i][j]
                        if self.curr_cell.rect.collidepoint(pygame.mouse.get_pos()):
                            if islmousedown or ismousemotion and self.curr_cell != self.prev_cell:
                                self.curr_cell.update()
                                print(self.curr_cell.color)
                            self.prev_cell = self.curr_cell
        return False

    def main_loop(self):
        while not self.done:
            self.done = self.process_events()
            self.display_frame(self.screen)
        pygame.quit()

