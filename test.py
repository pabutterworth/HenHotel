
from sun import Sun
from pushover import push
from time import sleep

import RPi.GPIO as GPIO
from time import sleep
#GPIO PINS
PIR_PIN = 18
FORWARD_PIN = 13
REVERSE_PIN = 15

def forward(x):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(FORWARD_PIN, GPIO.OUT)
    GPIO.output(FORWARD_PIN, GPIO.HIGH)
    debug("Forward")
    sleep(x)
    GPIO.output(FORWARD_PIN, GPIO.LOW)
    debug("Stopped")
#    GPIO.cleanup()
    return
    
def reverse(x):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(REVERSE_PIN, GPIO.OUT)
    GPIO.output(REVERSE_PIN, GPIO.HIGH)
    debug("reverse")
    sleep(x)
    GPIO.output(REVERSE_PIN, GPIO.LOW)
#    GPIO.cleanup()
    debug("stopped")
    return

def debug(x):
    print(x)
    return

# This is the start of the main program

coords = {'longitude' : 0.34, 'latitude' : 51.1  }
sun = Sun()

print sun.getSunriseTime(coords)
# Sunrise time UTC (decimal, 24 hour format)
push ("hi")
print sun.getSunriseTime( coords )['hr'] 
print sun.getSunriseTime( coords )['min']

print sun.getSunsetTime( coords )['hr'] 
print sun.getSunsetTime( coords )['min']

GPIO.setmode(GPIO.BOARD)
PIR_PIN = 26
GPIO.setup(PIR_PIN, GPIO.IN)

try:
    print ("testing c to exit")
    sleep(2)
    print ("ready")
    push("Testing")
    while True:
        if GPIO.input(PIR_PIN):
            debug("motion")
            reverse(1)
            forward(1)
        sleep(1)
except KeyboardInterrupt:
    print("quit")
    push("quit")
    GPIO.cleanup()

forward(5)
sleep(5)
reverse(5)
