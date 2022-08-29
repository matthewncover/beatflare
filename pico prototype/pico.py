# Adapted from Tony Goodhew's work:
# https://cdn.shopify.com/s/files/1/0176/3274/files/WS_Neopixels_160_Basic.py?v=1650975803

import array, utime
from machine import Pin
import rp2
import pico.ident_beats

class Pixels:

    def __init__(self, brightness=.1, n_leds=160, pin_num=6):

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

        # return dimmer_array
        state_machine.put(dimmer_array, 8)

    def set_color(self, i, rgb):

        self.pixel_array[i] = (rgb[0]<<8) + (rgb[1]<<16) + rgb[2]

    def fill(self, rgb):

        for i in range(self.n_leds):
            self.set_color(i, rgb)

    def clear(self):

        rgb = (0, 0, 0)
        self.fill(rgb)
        self.show()


class LEDSet:

    def __init__(self, n:int):

        assert n < 9
        self.n = n
        self.split()
    
    def split(self):

        self.width = 16 // self.n
        self.idict = {
            i: [
                16*x + self.width*i
                for x in range(10)
                ]
            for i in range(self.n)
        }

n_leds = 160
# brightness = 0.9
pin_num = 6

@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_LOW, 
    out_shiftdir=rp2.PIO.SHIFT_LEFT, 
    autopull=True, pull_thresh=24
    )

def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

state_machine = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(pin_num))
state_machine.active(1)

ar = array.array("I", [0]*n_leds)

pxl = Pixels()
for n in range(8):
    n += 1

    led_set = LEDSet(n=n)

    pxl.clear()

    for i in led_set.idict.values():
        for j in i:
            pxl.set_color(j, (255, 0, 0))

    pxl.show()

    utime.sleep(2)
    pxl.clear()

print("--\nDone.")