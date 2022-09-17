# Adapted from Tony Goodhew's work:
# https://cdn.shopify.com/s/files/1/0176/3274/files/WS_Neopixels_160_Basic.py?v=1650975803

import array

class Pixels:

    # def __init__(self, state_machine, brightness=.1, n_leds=160, pin_num=6):
    def __init__(self, brightness=.1, n_leds=160, pin_num=6):

        # self.state_machine = state_machine

        self.n_leds = n_leds
        self.brightness = brightness
        self.pin_num = pin_num

        self.pixel_array = array.array("I", [0]*self.n_leds)


    def show(self):

        dimmer_array = array.array("I", [0]*self.n_leds)

        for i, rgb in enumerate(self.pixel_array):
            r = int(((rgb >> 8) & 0xFF) * self.brightness)
            g = int(((rgb >> 16) & 0xFF) * self.brightness)
            b = int((rgb & 0xFF) * self.brightness)
            dimmer_array[i] = (g<<16) + (r<<8) + b
        
        return dimmer_array

    def set_color(self, i, rgb):

        self.pixel_array[i] = (rgb[0]<<8) + (rgb[1]<<16) + rgb[2]

    def fill(self, rgb):

        for i in range(self.n_leds):
            self.set_color(i, rgb)

    def clear(self):
        rgb = (0, 0, 0)
        self.fill(rgb)
    