from machine import Pin, PWM
import time

pin_numbers = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [9, 10, 11],
    [12, 13, 14],
    [15, 16, 17],
    [18, 19, 20],
    [21, 22, 26]
    ]

pin_offset_dict = {
    0: 16, 1: 17, 2: 18,
    3: 19, 4: 20, 5: 21,
    6: 22, 7: 29, 8: 29,
    9: 29, 10: 26, 11: 29,
    12: 28, 13: 29, 14: 29,
    15: 29, 16: 0, 17: 1,
    18: 2, 19: 3, 20: 4,
    21: 5, 22: 6, 26: 10
    }

N_LEDS = 8

def rgbval_to_duty(rgbval):
    #return (255 - rgbval)*65535 // 255
    #return int((255 - rgbval) / 255 * 1023)
    return rgbval*65535 // 255


class LEDs:
    def __init__(self):

        self.pin_numbers = pin_numbers
        self.rgb_ind_dict = {'r': 0, 'g': 1, 'b': 2}
        self.leds_dict = {}

        for led_no in range(N_LEDS):
            self.leds_dict[led_no+1] = {}

            for rgb_name in 'rgb':
                pin_no = self.pin_numbers[led_no][self.rgb_ind_dict[rgb_name]]
                pin_offset_no = pin_offset_dict[pin_no]
                pwm = PWM(Pin(pin_no))
                pwm.freq(1000)
                #self.leds_dict[led_no+1][rgb_name] = pwm
                #self.leds_dict[led_no+1][rgb_name] = PWM(Pin(pin_offset_no))
                self.leds_dict[led_no+1][rgb_name] = pwm
                #self.leds_dict[led_no+1][f"~{rgb_name}"] = Pin(pin_no, Pin.OUT)
                
        #self.all_off()

    def set_rgb(self, led_nos, rgb):
        r, g, b = rgb
        for led_no in led_nos:
            led = self.leds_dict[led_no]
            led['r'].duty_u16(rgbval_to_duty(r))
            led['g'].duty_u16(rgbval_to_duty(g))
            led['b'].duty_u16(rgbval_to_duty(b))
            
            #led['~r'].off()
            #led['~g'].off()
            #led['~b'].off()

    def all_off(self):
        #for led_no in range(N_LEDS):
        #    for rgb_name in 'rgb':
        #        self.leds_dict[led_no+1][rgb_name].duty_u16(0)
        
        for pin_no in pin_offset_dict.keys():
            Pin(pin_no, Pin.OUT).off()
            
        Pin(28, Pin.OUT).off()


