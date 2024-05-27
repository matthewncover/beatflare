import RPi.GPIO as GPIO
import time, random, json

class BreadboardLED:
    def __init__(self):
        self.RED_PIN = 22
        self.GREEN_PIN = 27
        self.BLUE_PIN = 17

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RED_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_PIN, GPIO.OUT)
        GPIO.setup(self.BLUE_PIN, GPIO.OUT)

    def set_color(self, red, green, blue):
        GPIO.output(self.RED_PIN, red)
        GPIO.output(self.GREEN_PIN, green)
        GPIO.output(self.BLUE_PIN, blue)

    def run(self):
        try:
            while True:
                with open("rgb_colors.json") as f:
                    colors = json.load(f)
                r, g, b = random.choice([color for color in colors.values()])
                print(r, g, b)
                self.set_color(r, g, b)
                time.sleep(1)
                self.set_color(0, 0, 0)  #off
                time.sleep(2)
        finally:
            GPIO.cleanup()