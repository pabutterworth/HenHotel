"""code from
http://deepaksinghviblog.blogspot.com/2014/08/raspberrypi-to-run-dc-motor-using-l298n.html
"""
import RPi.GPIO as GPIO
from time import sleep

class Motor:

	def forward(x):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(13, GPIO.OUT)
		GPIO.setup(15, GPIO.OUT)
		GPIO.output(13, GPIO.HIGH)
		sleep(x)
		GPIO.output(13, GPIO.LOW)
		GPIO.cleanup()
		return 

	def reverse(x):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(13, GPIO.OUT)
		GPIO.setup(15, GPIO.OUT)
		GPIO.output(15, GPIO.HIGH)
		sleep(x)
		GPIO.output(15, GPIO.LOW)
		GPIO.cleanup()
		return


def main():
    forward(5)
	
if __name__ == '__main__':
   main()
