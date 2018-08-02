import json, os, sys
import pygame

from src import grid
from src import cell
from src import synth
from src import backgroundreq
from src import slider
from src import label
import constants as c


class GUI:
    def __init__(self):
        """
        Intializes pygame and the pygame screen, loads the sprite groups that are needed,
        creates a model object belonging to the backgroundreq class, creates a quit button
        object belonging to the backgroundreq class (both model and quit button object are
        both added to backgroundreq sprite class), sets the amount of grid rows and columns,
        sets the grid and cell dimensions, sets the grid, creates slider objects for each
        slider and button name, creates backgroundreq objects for each slider and button name,
        and creates a label object for each slider and button name, adds each instance of the
        class to the all_sprites group, and calls the set_json_config() function to create
        a json file that stores the slider name (key) to the sliders value (value)
        """
        # Initialize environment
        self.grid_rows = 5
        self.grid_cols = 5
        self.grid_dimensions = (self.grid_rows, self.grid_cols)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption('MelodyDesign')

        # Initialize synth
        self.config = {}
        self.get_json_config()
        self.synth = synth.Synth(self.grid_dimensions, self.config)

        # Initialize sprite groups
        self.gridcells = pygame.sprite.Group()
        self.cells = pygame.sprite.Group()
        self.bg_reqs = pygame.sprite.Group()
        self.bg_labels = pygame.sprite.Group()
        self.sliders = pygame.sprite.Group()
        self.modals = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()
        self.modal_parent = backgroundreq.Backgroundreq(x=-1000, y=120, h=350, w=650, type=2)
        self.quit_button = backgroundreq.Backgroundreq(x=-1000, y=120, h=30, w=30, type=3, color=c.RED)
        self.modals.add(self.modal_parent, self.quit_button)
        self.quit_button.image.fill((250, 0, 0))

        # Set values
        self.cell_h = c.SCREEN_HEIGHT / self.grid_rows
        self.cell_w = self.cell_h
        self.cell_dimensions = self.cell_h, self.cell_w
        self.cell_sep = 2 if sum(self.grid_dimensions) < 20 else 1
        self.prev_cell = None
        self.curr_cell = None
        self.done = False

        # Create/populate grid
        self.grid = grid.Grid()
        self.populate_grid()

        # Create sliders
        self.slider_names = ['vol', 'res', 'att', 'dec', 'sus', 'rel', 'dur']
        self.slider_bg_padding = 20
        self.slider_label_w = 30
        self.slider_bg_x = c.SCREEN_HEIGHT + self.slider_bg_padding
        self.slider_bg_y = self.slider_bg_padding + 5
        self.slider_bg_h = 20
        self.slider_bg_w = c.SCREEN_WIDTH - c.SCREEN_HEIGHT - self.slider_bg_padding * 2
        self.sliders_x = self.slider_bg_x + self.slider_label_w
        self.sliders_y = self.slider_bg_padding
        self.sliders_h = self.slider_bg_h * 1.5
        self.sliders_w = 40
        self.slider_bg_total = (self.slider_bg_w - self.sliders_w - self.slider_label_w)
        self.initialize_sliders()

        # Create button(s)
        self.button_x = 620
        self.button_y = c.SCREEN_HEIGHT - self.slider_bg_padding*2.3
        self.button_sep = 100
        self.button_w = 70
        self.button_h = self.sliders_h
        self.initialize_button("Stop", 695, 400, self.button_h, 100, c.RED)
        self.initialize_button("Help", 800, 550, self.button_h, self.button_w)


        # Add sprites groups to all_sprites
        self.all_sprites = pygame.sprite.Group(tuple(self.gridcells) + tuple(self.cells) +
                                               tuple(self.bg_reqs) + tuple(self.sliders) +
                                               tuple(self.bg_labels) + tuple(self.modals))

    def get_json_config(self):
        """
        Read in config.json if exists, otherwise use initial values
        :return:
        """
        print(self.config)
        # with open("config.json"):
        #     self.config = json.load(open("config.json"))
        try:
            jsonfile = open("config.json")
        except:
            print("No config file found, using defaults")
            self.config = {k: v['def'] for (k, v) in c.defaults.items()}
        else:
            print("Config file found, user settings applied:")
            self.config = json.load(jsonfile)

    def set_json_config(self):
        """
        Takes a python dictionary object and stores it in a JSON file

        :return: None
        """
        configs = {slider.name:slider.value for slider in self.sliders}
        with open("config.json", "w") as outfile:
            json.dump(configs, outfile)

    def populate_grid(self):
        """
        If config.json exists in main project folder, populate sliders based on json data,
        otherwise use defaults from Synth() class.

        :return: None
        """
        count = 0
        y = 0
        for i in range(self.grid_rows):
            x = 0
            self.grid.matrix.append([])
            for j in range(self.grid_cols):
                cellname = "R" + str(i + 1) + "C" + str(j + 1)
                cellnum = count
                h = self.cell_h - self.cell_sep
                w = self.cell_w - self.cell_sep
                self.grid.matrix[i].append(self.gridcells.add(grid.GridCell(cellname, x, y, h, w)))
                self.grid.matrix[i].append(self.cells.add(cell.Cell(cellname, cellnum, x, y, h, w)))
                x += self.cell_w
                count += 1
            y += self.cell_h

    def initialize_sliders(self):
        """
        Create sliders, add to sprite groups.

        :return: None
        """
        for name in self.slider_names:
            # Create slider background rectangle, add to bg_reqs sprite group
            self.bg_reqs.add(backgroundreq.Backgroundreq(x=self.slider_bg_x, y=self.slider_bg_y,
                                                         h=self.slider_bg_h, w=self.slider_bg_w, type=0))

            # Create slider rectangle, add to sliders sprite group
            slider_min = c.defaults[name]['min']
            slider_max = c.defaults[name]['max']

            print(self.slider_bg_total, "-", slider_min, "/", slider_max, "-", slider_min, "=", (self.slider_bg_total - slider_min / slider_max - slider_min)*self.config[name])

            slider_x = self.sliders_x + ((self.slider_bg_total - slider_min) / (slider_max - slider_min)) * self.config[name]
            self.sliders.add(slider.Slider(name=name, value=self.config[name], x=slider_x,
                                           y=self.sliders_y, h=self.sliders_h, w=self.sliders_w))

            # Create slider rectangle, add to sliders sprite group
            self.bg_labels.add(label.Label(name=name, x=self.slider_bg_x+5, y=self.sliders_y+6,
                                           h=self.sliders_h, w=self.sliders_w, font_size=14))

            self.sliders_y += self.sliders_h + self.slider_bg_padding
            self.slider_bg_y += self.sliders_h + self.slider_bg_padding

    def initialize_button(self, name: str, x: float, y: float, h: float, w: float, color: tuple=c.LGRAY):
        """
        Create buttons, add to sprite groups.

        :return: None
        """
        self.bg_reqs.add(backgroundreq.Backgroundreq(x, y, h, w, type=1, color=color, name=name))
        self.bg_labels.add(label.Label(name=name, x=x+w/2-14, y=y+5, h=h, w=w, font_size=16))

    def sliders_events_loop(self, click: list, mx: int, my: int):
        """
        creates a for loop for the slider object that allows the object to change its x position depending on if the mouse collides
        with the slider rectangle object
        args: click, mx(int), my(int)

        :param click:
        :param mx: int
        :param my: int
        :return: None
        """
        for s in self.sliders:
            if s.rect.collidepoint((mx, my)):
                s.rect.x = mx - s.width / 2
                if s.rect.x < self.sliders_x:
                    s.rect.x = self.sliders_x
                elif s.rect.x > self.sliders_x + self.slider_bg_w - s.width - self.slider_label_w:
                    s.rect.x = self.sliders_x + self.slider_bg_w - s.width - self.slider_label_w

                slider_pos = (s.rect.x - self.sliders_x)
                slider_min = c.defaults[s.name]['min']
                slider_max = c.defaults[s.name]['max']

                s.value = (slider_pos - slider_min)/(self.slider_bg_total - slider_min) * slider_max + slider_min
                self.synth.set_vals(s.name, s.value + slider_min)
                # print(slider.name, slider.value)
                s.image.fill((100, 160, 200))
                s.font.render_to(s.image, dest=s.font_dest,
                                      text=str(round(float(s.value), 2)), fgcolor=c.WHITE)

    def buttons_events_loop(self, click: list, mx: int, my: int):
        """
        Creates a for loop for each button object that depends on a click event,
        if the user clicks the button object, a help object appears.

        :param click: list
        :param mx: int
        :param my: int
        :return: None
        """
        for button in self.bg_reqs:
            if click[0]:
                if button.rect.collidepoint((mx, my)):
                    if button.type == 1:
                        button.image.fill((250, 0, 0))
                        if button.name == "Help":
                            self.modal_parent.rect.x = 120
                            self.quit_button.rect.x = 740
                            help_inst = ["Welcome to the musical synth pad help box!",
                                         "Press a square to make a sound!",
                                         "Move the sliders to change the sound",
                                         " ",
                                         "Press 'Stop' to stop all active audio streams!",
                                         " ",
                                         "Enjoy!",
                                         "    MelodyDesign Team "]
                            help_inst_y_coor = 180
                            for sentence in help_inst:
                                text = label.Label(sentence, 250, help_inst_y_coor, 350, 350, 20)
                                self.texts.add(text)
                                self.all_sprites.add(self.texts)
                                help_inst_y_coor += 30
                        elif button.name == "Stop":
                            self.synth.stop_all()

            else:
                button.image.fill((200, 200, 200))
        for button in self.modals:
            if click[0]:
                if button.rect.collidepoint((mx, my)):
                    if button.type == 3:
                        print("WOOOHOOOO")
                        self.modal_parent.rect.x = -1000
                        self.quit_button.rect.x = -1000
                    for text in self.texts:
                        text.rect.x = -1000

    def cells_events_loop(self, click: list, mx: int, my: int):
        """
        Creates a for loop for each cell object that depends on a click event,
        if the user clicks the cell object, a corresponding Synth() object
        will make a sound, and the cell's color alpha will change based on
        the sound's output.

        :param click: bool
        :param mx: int
        :param my: int
        :return: None
        """
        chnl = 0
        for cell in self.cells:
            snd_val = int(abs(self.synth.snds[cell.num].get() * 4000))
            snd_val = 255 if snd_val > 255 else snd_val
            if snd_val:
                print(cell.name, snd_val)
            cell.image.set_alpha(snd_val)
            if click[0]:
                self.curr_cell = cell
                if self.curr_cell.rect.collidepoint((mx, my)):
                    if self.curr_cell != self.prev_cell:
                        self.curr_cell.update()
                        self.synth.play(cell.num, chnl)
                    self.prev_cell = self.curr_cell
            elif snd_val < 1 and not click[0]:
                self.synth.snds[cell.num].stop()
            else:
                self.prev_cell = 0
            chnl = 1 if chnl == 0 else 0

    def process_events(self):
        """
        Creates an event loop that runs a specific function depending on mouse events.
        The function returns True if pygame.QUIT event is triggered, causing the application
        exit, otherwise the function returns False

        :return: bool
        """
        if pygame.event.get(pygame.QUIT):
            return True
        click = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()
        self.cells_events_loop(click, mx, my)
        if click[0]:
            self.sliders_events_loop(click, mx, my)
            self.buttons_events_loop(click, mx, my)
        else:
            self.buttons_events_loop(click, mx, my)
        pygame.event.clear()
        return False

    def display_frame(self, screen: pygame.Surface):
        """
        Displays and draws the background and sprites on screen

        :param screen: pygame.Surface()
        :return: None
        """
        screen.fill(c.BLACK)
        self.all_sprites.draw(screen)
        pygame.display.flip()

    def main_loop(self):
        """
        main loop of the game

        :return: None
        """
        while not self.done:
            self.done = self.process_events()
            self.display_frame(self.screen)
        self.set_json_config()
        # for cell in self.cells:
        self.synth.stop_all()
        self.synth.pyo.stop()
        pygame.quit()
        sys.exit()
