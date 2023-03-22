import serial
import numpy as np

# from https://blog.rareschool.com/2021/01/controlling-raspberry-pi-pico-using.html
class PicoCom:
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


class LEDPicoCom(PicoCom):

    def __init__(self):

        super().__init__()
        self.__startup()

    def __startup(self):
        self.send("from main import LEDS")
        self.send("x = LEDS()")

    def _set(self, rgb_array:list):
        """expecting a 5x3 array / nested list
        """
        self.send(f"x._set({rgb_array})")

    def off(self):

        self.send("x.all_off()")

if __name__ == "__main__":

    import time, json
    import numpy as np
    x = LEDPicoCom()

    with open("./color_to_rgb.json") as f:
        color_dict = json.load(f)

    rgb_arr = np.random.choice([0, 0, 128, 200, 200], (5, 3))
    n_fades = 8
    delta = rgb_arr // n_fades
    empty_arr = np.zeros(rgb_arr.shape)
    for _ in range(n_fades):
        rgb_arr = np.maximum(rgb_arr - delta, 0)

        x._set(rgb_arr.tolist())
        time.sleep(.025)
    
    x.off()
    x.close()