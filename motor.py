"""code from
http://deepaksinghviblog.blogspot.com/2014/08/raspberrypi-to-run-dc-motor-using-l298n.html
"""
import RPi.GPIO as GPIO
from time import sleep
FORWARD = 15
REVERSE = 21

class Motor:

	def forward(x):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(FORWARD, GPIO.OUT)
		GPIO.setup(REVERSE, GPIO.OUT)
		GPIO.output(FORWARD, GPIO.HIGH)
		sleep(x)
		GPIO.output(FORWARD, GPIO.LOW)
		GPIO.cleanup()
		return 

	def reverse(x):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(FORWARD, GPIO.OUT)
		GPIO.setup(REVERSR, GPIO.OUT)
		GPIO.output(REVERSE, GPIO.HIGH)
		sleep(x)
		GPIO.output(REVERSE, GPIO.LOW)
		GPIO.cleanup()
		return


def main():
    Motor.forward(5)
	
if __name__ == '__main__':
   main()
