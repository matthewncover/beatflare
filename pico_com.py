import serial
import numpy as np

#### Colors

rgb_dict = {
    "white":    (200, 200, 200),
    "red":      (200,   0,   0),
    "green":    (  0, 200,   0),
    "blue":     (  0,   0, 200),
    "teal":     (  0, 200, 200),
    "purple":   (200,   0, 200),
    "lime":     (200, 200,   0),
    "orange":   (128,  12,   0)
}

# from https://blog.rareschool.com/2021/01/controlling-raspberry-pi-pico-using.html
class Pico:
    TERMINATOR = '\n'.encode("UTF8")

    def __init__(self, device="COM3", baud=115200, timeout=1):

        self.serial = serial.Serial(device, baud, timeout=timeout)

    def send(self, text:str):
        """send a function call to the Pico.
        function must be present in main.py
        """
        comm = '%s\r\f' % text
        comm_encoded = comm.encode("UTF8")
        self.serial.write(comm_encoded)

    def receive(self) -> str:
        line = self.serial.read_until(self.TERMINATOR)

        return line.decode("UTF8").strip()

    def close(self):
        self.serial.close()

    #### send methods

    def fill_show_die(self, rgb=None):

        if not rgb:
            rgb = rgb_dict[np.random.choice(list(rgb_dict.keys()))]

        self.send(f"leds.fill_show(pxls=leds.die_pxls, rgb={rgb})")

    def clear(self):

        self.send("leds.clear()")


class LEDPico(Pico):

    def __init__(self):

        super().__init__()
        self.__startup()

    def __startup(self):
        self.send("from main import LEDS")
        self.send("x = LEDS()")

    def _set(self, command:list):
        """expecting a list of 5 tuples like
        (1, (200, 0, 0))
        """
        self.send(f"x._set({command})")

if __name__ == "__main__":

    import time
    x = LEDPico()

    all_purple = [(x, (150, 0, 150)) for x in range(1,6)]
    all_white = [(x, (150, 150, 150)) for x in range(1,6)]
    all_orange = [(x, (128, 12, 0)) for x in range(1,6)]
    x._set(all_purple)
    time.sleep(1)
    x._set(all_white)
    time.sleep(1)
    x._set(all_orange)

    x.close()