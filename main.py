import RPi.GPIO as GPIO
import time

RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

def set_color(red, green, blue):
    GPIO.output(RED_PIN, red)
    GPIO.output(GREEN_PIN, green)
    GPIO.output(BLUE_PIN, blue)

try:
    while True:
        set_color(1, 0, 0)  #red
        time.sleep(1)
        set_color(0, 1, 0)  #green
        time.sleep(1)
        set_color(0, 0, 1)  #blue
        time.sleep(1)
        set_color(1, 1, 0)  #yellow
        time.sleep(1)
        set_color(0, 1, 1)  #cyan
        time.sleep(1)
        set_color(1, 0, 1)  #magenta
        time.sleep(1)
        set_color(1, 1, 1)  #white
        time.sleep(1)
        set_color(0, 0, 0)  #off
        time.sleep(1)
finally:
    GPIO.cleanup()
