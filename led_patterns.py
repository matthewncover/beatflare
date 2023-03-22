import numpy as np
import time

class Patterns:

    def __init__(self, pico, arr):
        """
        pico: LEDPico
        arr: rgb np array (5x3)
        """

        self.pico = pico

        self.arr = arr
        if type(arr) == list:
            self.arr = np.array(arr)

    def fade(self):

        n_fades = 8
        delta = self.arr // n_fades + 1
        rgb_arr = self.arr.copy()

        for _ in range(n_fades):
            rgb_arr = np.maximum(rgb_arr - delta, 0)

            self.pico._set(rgb_arr.tolist())
            time.sleep(.025)

        self.pico.off()


if __name__ == "__main__":

    from pico_com import LEDPico

    pico = LEDPico()
    orange_arr = np.array([(128, 12, 0) for _ in range(6)])
    purple_arr = np.array([(200, 0, 200) for _ in range(6)])

    orange = Patterns(pico, orange_arr)
    purple = Patterns(pico, purple_arr)
    
    for _ in range(2):
        orange.fade()
        time.sleep(.2)
        purple.fade()
        time.sleep(1)

    pico.close()