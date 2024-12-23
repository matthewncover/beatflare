from machine import Pin, PWM
from utime import sleep

def rtd(rgbval):
    """rgbval to duty"""
    return rgbval*65535 // 255

class LEDS:

    pin_numbers = [
        [3, 4, 5],      #led1
        [6, 7, 8],      #led2
        [9, 10, 11],    #led3
        [12, 13, 14],   #led4
        [15, 16, 17],   #led5
        ]

    def __init__(self):

        self.led_dict = {
            led_no: {
                rgb: PWM(Pin(pin_no)) 
                for (rgb, pin_no) in zip('rgb', self.pin_numbers[led_no])
                } 
            for led_no in range(5)
            }

    def _set(self, rgb_set:list):
        """expecting a nested list of 5 rgb triples
        """
        
        for led_no, rgb in enumerate(rgb_set):
            for rgb_name, rgb_val in zip('rgb', rgb):
                self.led_dict[led_no][rgb_name].duty_u16(rtd(rgb_val))

    def all_off(self):
        for led_no in self.led_dict.keys():
            for rgb_name in 'rgb':
                self.led_dict[led_no][rgb_name].duty_u16(0)

###

#all_orange = [(x, (128, 12, 0)) for x in range(1,6)]
#all_purple = [(x, (150, 0, 150)) for x in range(1,6)]

#_set(all_orange)
#sleep(1)
#_set(all_purple)
#sleep(1)
#all_off()