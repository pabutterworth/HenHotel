

import RPi.GPIO as GPIO
import time
from time import ctime
import httplib, urllib

WORKING = 0
SUCCESS = 1
TIMEOUT = 2
SWITCHABORT = 3


FORWARD = 1
REVERSE = 2
STOPMOTOR = 3

MAX_TIME = 30
CLOSE_TIME = 10 #time to take to close
OPEN_TIME = 10 #time to open  

OPEN_DISTANCE = 70
CLOSED_DISTANCE = 20

debugmode = True #Used to stop pushover messages being sent

#Pushover Keys
APP_TOKEN = "ap1zxxfpdcnbkkfk5fk9daoob78hpb"
USER_ID = "uZ8cbsrmeoMiMJEU6MzHTVKNwrPUr2"

#GPIO PINS

GPIO_MOTOR_FORWARD = 13
GPIO_MOTOR_REVERSE = 15
GPIO_TRIG = 23 #Distance sensor
GPIO_ECHO = 24 #Distance sensor

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

def pushover(push_text):
    title = "Hen Hotel :" +ctime()
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    if debugmode == False:
        conn.request("POST", "/1/messages.json",urllib.urlencode({"token": APP_TOKEN ,"user":
            USER_ID, "message": push_text,"title": title}),
            { "Content-type": "application/x-www-form-urlencoded" })
    print "Pushover:  " + push_text
    return  # End of function push


def timer():
   now = time.localtime(time.time())
   print now[5]
   return now[5]

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
    finishtime = timer()+CLOSE_TIME
    print "Finishtime = "+finishtime

    motor(REVERSE) #start the motor closing

    while status == WORKING:
        if timer() >= finishtime: #timer expired
            debugprint ("TIMER EXPIRED")
            status = TIMEOUT
            pushover("Time Out - Check Ramp")
        elif howfar() <= CLOSED_DISTANCE:  #Distance sensor shows closed
            print "Sensor states closed"
            status = SUCCESS         #All good
        elif manualswitch() != 0:
            pushover("Manual Abort")
            debugprint ("Manual Abort")
            status = SWITCHABORT
    motor(STOPMOTOR)
    return(status)

print("Starting")
GPIO.setmode(GPIO.BOARD)
closeDoor()
print("Finishing")

