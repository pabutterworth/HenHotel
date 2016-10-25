import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
PIR_PIN = 26
GPIO.setup(PIR_PIN, GPIO.IN)

try:
	print ("testing c to exit")
	time.sleep(2)
	print ("ready")
	while True:
		if GPIO.input(PIR_PIN):
			print("motion")
		time.sleep(1)
except KeyboardInterrupt:
	print("quit")
	GPIO.cleanup()