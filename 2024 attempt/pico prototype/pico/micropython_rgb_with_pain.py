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

N_LEDS = 8

def rgbval_to_duty(rgbval):
    return rgbval*65535 / 255


class LEDs:
    def __init__(self):

        self.pin_numbers = pin_numbers
        self.rgb_ind_dict = {'r': 0, 'g': 1, 'b': 2}
        self.leds_dict = {}

        for led_no in range(N_LEDS):
            self.leds_dict[led_no+1] = {}

            for rgb_name in 'rgb':
                pin_no = self.pin_numbers[led_no][self.rgb_ind_dict[rgb_name]]
                pwm = PWM(Pin(pin_no))
                pwm.freq(1000)
                self.leds_dict[led_no+1][rgb_name] = pwm

    def set(self, led_nos, rgb):
        r, g, b = rgb
        for led_no in led_nos:
            led = self.leds_dict[led_no]
            led['r'].duty_u16(rgbval_to_duty(r))
            led['g'].duty_u16(rgbval_to_duty(g))
            led['b'].duty_u16(rgbval_to_duty(b))

    def fade_to_off(self, led_nos, duration):
        current_rgb = {}
        for led_no in led_nos:
            current_rgb[led_no] = (
                self.leds_dict[led_no]['r'].duty_u16() // 256,
                self.leds_dict[led_no]['g'].duty_u16() // 256,
                self.leds_dict[led_no]['b'].duty_u16() // 256
            )

        duty_increments = {
            led_no: {
                rgb: - self.leds_dict[led_no][rgb].duty_u16() / (duration * 1000 // self.leds_dict[led_no][rgb].freq())
                for rgb in 'rgb'
            }
            for led_no in led_nos
        }

        start_time = time.ticks_ms()
        while time.ticks_ms() < start_time + duration * 1000:
            elapsed_time = time.ticks_diff(time.ticks_ms(), start_time)
            for led_no in led_nos:
                for rgb in 'rgb':
                    current_duty = self.leds_dict[led_no][rgb].duty_u16()
                    increment = duty_increments[led_no][rgb] * elapsed_time
                    new_duty = current_duty + increment
                    self.leds_dict[led_no][rgb].duty_u16(int(new_duty))
            time.sleep(0.001)

        self.set(led_nos, (0, 0, 0))

    def all_off(self):
        for led_no in range(N_LEDS):
            for rgb_name in 'rgb':
                self.leds_dict[led_no+1][rgb_name].duty_u16(0)