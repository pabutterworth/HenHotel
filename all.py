

import RPi.GPIO as GPIO
import time
import httplib, urllib

FORWARD = 1
REVERSE = 2
STOPMOTOR = 3

MAXTIME = 30
CLOSED = 10 #this is the readingf or a closed ramp
OPEN = 50

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
  print ("Distance:"+distance+"cm")
  return distance
  #end of function howfar

def push(push_text):
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
   return now[5]

def motor(direction):
	if direction == FORWARD:
		GPIO.setup(GPIO_MOTOR_FORWARD, GPIO.OUT)
		GPIO.setup(GPIO_MOTOR_REVERSE, GPIO.OUT)
		GPIO.output(GPIO_MOTOR_FORWARD, GPIO.HIGH)
		GPIO.output(GPIO_MOTOR_REVERSE, GPIO.LOW)
	elif direction == REVERSE:
		GPIO.setup(GPIO_MOTOR_FORWARD, GPIO.OUT)
		GPIO.setup(GPIO_MOTOR_REVERSE, GPIO.OUT)
		GPIO.output(GPIO_MOTOR_FORWARD, GPIO.LOW)
		GPIO.output(GPIO_MOTOR_REVERSE, GPIO.HIGH)
	elif direction == STOPMOTOR:
		GPIO.output(GPIO_MOTOR_FORWARD, GPIO.LOW)
		GPIO.output(GPIO_MOTOR_REVERSE, GPIO.LOW)
	else:
		debugprint ("Invalid input to motor function")
	return #enf of function mortor

def closeDoor():
    working = 0
    timeout = 1
    switchabort = 2
    distanceabort = 3

    status = working
    finishtime = timer()+MAXTIME

    motor(REVERSE) #start the motor closing

    while status == working:
        if timer() >= finishtime: #timer expired
            debugprint ("TIMER EXPIRED")
            status = timeout
            pushover("Time Out - Check Ramp")
        elif howfar() <= CLOSED:  #Distance sensor shows closed
            print "Sensor states closed"
            status = closed         #All good
        elif manualswitch() != 0:
            pushover("Manual Abort")
            debugprint ("Manual Abort")
            status = switchabort
    motor(STOPMOTOR)
    return(status)

print("Starting")
GPIO.setmode(GPIO.BOARD)
closeDoor()
print("Finishing")

