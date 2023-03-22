import numpy as np, json
import time

from pico_com import LEDPicoCom

class Lights:

    N_LEDS = 6

    def __init__(self):

        self.pico = LEDPicoCom()
        self.__init_rgb_dict()

    def __init_rgb_dict(self):

        with open('./rgb_colors.json') as f:
            self.rgb_dict = json.load(f)

    def _set(self, color:str, leds:list):
        """make rgb array to apply methods to
        """

        rgb = self.rgb_dict[color]
        arr = [[0]*3 if x not in leds else rgb for x in range(1,self.N_LEDS)]

        self.arr = np.array(arr)

    def _fill(self, color:str, leds=None):
        """fills [0,0,0] arrays in `arr` with `color`
        """
        assert color in self.rgb_dict.keys(), "color not yet accepted"

        rgb = self.rgb_dict[color]

        if leds is None:
            fill_rows = np.where((self.arr == [0]*3).all(axis=1))[0]
            self.arr[fill_rows] = rgb

        else:
            self.arr[[x-1 for x in leds]] = rgb

    def fade(self):

        n_fades = 8
        delta = self.arr // n_fades + 1
        rgb_arr = self.arr.copy()

        for _ in range(n_fades):
            rgb_arr = np.maximum(rgb_arr - delta, 0)

            self.pico._set(rgb_arr.tolist())
            time.sleep(.025)

        self.pico.off()

    def stagger(self):
        """WIP
        """

        for i in range(self.N_LEDS):
            rgb_arr = self.arr.copy()
            rgb_arr[~(np.arange(self.arr.shape[0]) == i)] = [0,0,0]

            self.pico._set(rgb_arr.tolist())
            time.sleep(.2)


if __name__ == "__main__":

    lights = Lights()
    
    lights._set('orange', [1,3,5])
    lights.fade()
    time.sleep(.7)
    lights._fill('purple', [2, 4]) #that's cool
    lights.fade()

    lights.pico.close()