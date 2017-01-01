
import RPi.GPIO as GPIO
import time
from time import ctime
from time import sleep
import httplib, urllib
import math
import datetime
from pushover import push
debugmode = True

WORKING = 0
SUCCESS = 1
TIMEOUT = 2
SWITCHABORT = 3


FORWARD = 1
REVERSE = 2
STOPMOTOR = 3

MAX_TIME = 164
CLOSE_TIME = 164 #time to take to close
OPEN_TIME = 164 #time to open  

OPEN_DISTANCE = 70
CLOSED_DISTANCE = 24
LEEWAY = 1

#GPIO PINS
GPIO_MOTOR_FORWARD = 15
GPIO_MOTOR_REVERSE = 21
GPIO_TRIG = 23 #Distance sensor
GPIO_ECHO = 24 #Distance sensor
GPIO_UP_SWITCH = 29

def debugprint(message):
    if (debugmode == True):
	print (message)
    return


def howfar():
  #GPIO.setmode(GPIO.BOARD)
  GPIO.setup(GPIO_TRIG,GPIO.OUT)
  GPIO.setup(GPIO_ECHO,GPIO.IN)

  GPIO.output(GPIO_TRIG, False)
  debugprint ("Waiting For Sensor To Settle")
  time.sleep(0.1)

  GPIO.output(GPIO_TRIG, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIG, False)

  while GPIO.input(GPIO_ECHO)==0:
    pulse_start = time.time()

  while GPIO.input(GPIO_ECHO)==1:
    pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start
  distance = pulse_duration * 17150
  distance = round(distance, 2)
  print "Distance:",distance,"cm"
  return distance
  #end of function howfar

def timer():
   ticks = time.time()
   print ticks
   return ticks

def motor(direction):
	
	if direction == FORWARD:
		GPIO.setup(GPIO_MOTOR_FORWARD, GPIO.OUT)
		GPIO.setup(GPIO_MOTOR_REVERSE, GPIO.OUT)
		GPIO.output(GPIO_MOTOR_FORWARD, GPIO.HIGH)
		GPIO.output(GPIO_MOTOR_REVERSE, GPIO.LOW)
		debugprint("Motor:Forward")
	elif direction == REVERSE:
		GPIO.setup(GPIO_MOTOR_FORWARD, GPIO.OUT)
		GPIO.setup(GPIO_MOTOR_REVERSE, GPIO.OUT)
		GPIO.output(GPIO_MOTOR_FORWARD, GPIO.LOW)
		GPIO.output(GPIO_MOTOR_REVERSE, GPIO.HIGH)
		debugprint("Motor: Reverse")
	elif direction == STOPMOTOR:
		GPIO.output(GPIO_MOTOR_FORWARD, GPIO.LOW)
		GPIO.output(GPIO_MOTOR_REVERSE, GPIO.LOW)
		debugprint("Motor: Stop")
	else:
		debugprint ("Invalid input to motor function")
	
	return #enf of function mortor

def manualswitch():
    return 0

def closeDoor():
    status = WORKING
    finishtime = timer() + CLOSE_TIME
    print finishtime
    push("Starting Motor")
    motor(REVERSE) #start the motor closing

    while status == WORKING:
        if timer() >= finishtime: #timer expired
            debugprint ("TIMER EXPIRED")
            status = TIMEOUT
            push("Time Out - Check Ramp")

    motor(STOPMOTOR)
    push("Stopping Motor")
    message = "distance = " + howfar() + "cm"  
    push(message)
    return(status)

def openDoor():
    status = WORKING
    finishtime = timer() + OPEN_TIME
    print finishtime
    push("Starting Open Door")

    motor(FORWARD) #start the motor closing

    while status == WORKING:
        if timer() >= finishtime: #timer expired
            debugprint ("TIMER EXPIRED")
            status = TIMEOUT
            push("Time Out - Check Ramp")

    motor(STOPMOTOR)
    push("Stopping Motor")
    message = "distance = " + howfar() + "cm"  
    push(message)
    return(status)

def closeDoorTest():
    status = WORKING
    finishtime = timer() + OPEN_TIME
    starttime = timer()
    print ("Start time")
    ticks = time.time()
    print ticks

    motor(REVERSE) #start the motor closing

	
    while status == WORKING:
	fred=1
	#print timer()
        #status = SUCCESS         #All good
    motor(STOPMOTOR)
    return(status)
    
def main():
	
    message = "distance = " + howfar() + "cm"  
    push(message)
	"""
    starttime = time.time()
    try:
	GPIO.setmode(GPIO.BOARD)
  	closeDoor()
  """
    except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
        print "Key hit"
  
    #except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
     #   print "Other error or exception occurred!"  
  
    finally:  
        GPIO.cleanup() # this ensures a clean exit  
	print "In Finally function" 
	print ("Running time")
        ticks = time.time()
        print ticks-starttime


if __name__ == '__main__':
   main()

