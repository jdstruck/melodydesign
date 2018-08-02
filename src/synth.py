from pyo import *
import constants as c

class Synth:
    """
    Synth class initializes the Pyo server, and creates one pyo sound generator
    object, envelop object, and filter object, for each Cell() object created
    in the GUI(). The combined sound object's play() method is called when the
    user initiates mouse down event over one of the cells, based on the cell's
    "num" value.
    """
    def __init__(self, grid_dimensions: tuple, config: dict):
        self.freq = []
        self.pyo = Server(nchnls=2, buffersize=4096, duplex=0, winhost="asio").boot().start()
        self.grid_rows, self.grid_cols = grid_dimensions
        self.snds = []
        self.envs = []
        self.moogs = []
        self.freqs = self.get_freqs()
        self.config = config
        self.env_vol = self.config['vol']
        self.moog_res = self.config['res']
        self.env_att = self.config['att']
        self.env_dec = self.config['dec']
        self.env_sus = self.config['sus']
        self.env_rel = self.config['rel']
        self.env_dur = self.config['dur']

        for i in range(self.grid_rows*self.grid_cols):
            self.envs.append(Adsr(attack=self.env_att, decay=self.env_dec, sustain=self.env_sus,
                                  release=self.env_rel, dur=self.env_dur, mul=self.env_vol))
            self.snds.append(MoogLP(SuperSaw(freq=self.freqs[i], mul=self.envs[i]), res=self.moog_res))
            # self.snd_mul -= .05

    def set_vals(self, name: str, val: float):
        """
        Sets sound parameters based on slider position

        :param name: str
        :param val: float
        :return:
        """
        for i, snd in enumerate(self.snds):
            if name == 'vol':
                self.env_vol *= val
            if name == 'res':
                self.moog_res = val
                snd.res = self.moog_res
            if name == 'att':
                self.env_att = val
                self.envs[i].attack = self.env_att
            if name == 'dec':
                self.env_dec = val
                self.envs[i].decay = self.env_dec
            if name == 'sus':
                self.env_sus = val
                self.envs[i].sustain = self.env_sus
            if name == 'rel':
                self.env_rel = val
                self.envs[i].release = self.env_rel
            if name == 'dur':
                self.env_dur = val
                self.envs[i].dur = self.env_dur

    def play(self, num: int, chnl: int=0):
        """
        Calls pyo's play() method to envelope, and out() method to the sound generator object based on cell number (num)
        :param num: int
        :param chnl: int
        :return: None
        """
        self.envs[num].play()
        self.snds[num].out(chnl)

    def stop(self, num: int):
        """
        Calls pyo's stop() method to envelope and sound generator object based on cell number (num)
        :param num: int
        :return: None
        """
        self.envs[num].stop()
        self.snds[num].stop()

    def stop_all(self):
        """
        Calls pyo's stop() method on all envelope and sound generator objects
        :param num: int
        :return: None
        """
        for snd in self.snds:
            snd.stop()

    def get_freqs(self):
        """
        Based on grid dimensions, set default frequency values

        :return: list of frequency values to assign to sound/cell
        """
        basefrqs = [75, 150, 300, 600, 1200, 2400]
        four = [1, 9/8, 5/4, 3/2]
        five = [1, 9/8, 5/4, 3/2, 5/3]
        six = [1, 9/8, 5/4, 25/18, 8/5, 9/5]
        scale = []
        if self.grid_rows == 4:
            scale = four
        elif self.grid_rows == 5:
            scale = five
        elif self.grid_rows == 6:
            scale = six
        return [i*basefrqs[p] for p in range(self.grid_cols) for i in scale]
