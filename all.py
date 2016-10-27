

import RPi.GPIO as GPIO
import time
from time import ctime
from time import sleep
import httplib, urllib
import math
import datetime

coords = {'longitude' : 0.34, 'latitude' : 51.1  }

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
GPIO_UP_SWITCH = 29

def debugprint(message):
    if (debugmode == True):
	print (message)
    return


class Sun:

    def getSunriseTime( self, coords ):
        return self.calcSunTime( coords, True )

    def getSunsetTime( self, coords ):
        return self.calcSunTime( coords, False )

    def getCurrentUTC( self ):
        now = datetime.datetime.now()
        return [ now.day, now.month, now.year ]

    def calcSunTime( self, coords, isRiseTime, zenith = 90.8 ):

        # isRiseTime == False, returns sunsetTime

        day, month, year = self.getCurrentUTC()

        longitude = coords['longitude']
        latitude = coords['latitude']

        TO_RAD = math.pi/180

        #1. first calculate the day of the year
        N1 = math.floor(275 * month / 9)
        N2 = math.floor((month + 9) / 12)
        N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
        N = N1 - (N2 * N3) + day - 30

        #2. convert the longitude to hour value and calculate an approximate time
        lngHour = longitude / 15

        if isRiseTime:
            t = N + ((6 - lngHour) / 24)
        else: #sunset
            t = N + ((18 - lngHour) / 24)

        #3. calculate the Sun's mean anomaly
        M = (0.9856 * t) - 3.289

        #4. calculate the Sun's true longitude
        L = M + (1.916 * math.sin(TO_RAD*M)) + (0.020 * math.sin(TO_RAD * 2 * M)) + 282.634
        L = self.forceRange( L, 360 ) #NOTE: L adjusted into the range [0,360)

        #5a. calculate the Sun's right ascension

        RA = (1/TO_RAD) * math.atan(0.91764 * math.tan(TO_RAD*L))
        RA = self.forceRange( RA, 360 ) #NOTE: RA adjusted into the range [0,360)

        #5b. right ascension value needs to be in the same quadrant as L
        Lquadrant  = (math.floor( L/90)) * 90
        RAquadrant = (math.floor(RA/90)) * 90
        RA = RA + (Lquadrant - RAquadrant)

        #5c. right ascension value needs to be converted into hours
        RA = RA / 15

        #6. calculate the Sun's declination
        sinDec = 0.39782 * math.sin(TO_RAD*L)
        cosDec = math.cos(math.asin(sinDec))

        #7a. calculate the Sun's local hour angle
        cosH = (math.cos(TO_RAD*zenith) - (sinDec * math.sin(TO_RAD*latitude))) / (cosDec * math.cos(TO_RAD*latitude))

        if cosH > 1:
            return {'status': False, 'msg': 'the sun never rises on this location (on the specified date)'}

        if cosH < -1:
            return {'status': False, 'msg': 'the sun never sets on this location (on the specified date)'}

        #7b. finish calculating H and convert into hours

        if isRiseTime:
            H = 360 - (1/TO_RAD) * math.acos(cosH)
        else: #setting
            H = (1/TO_RAD) * math.acos(cosH)

        H = H / 15

        #8. calculate local mean time of rising/setting
        T = H + RA - (0.06571 * t) - 6.622

        #9. adjust back to UTC
        UT = T - lngHour
        UT = self.forceRange( UT, 24) # UTC time in decimal format (e.g. 23.23)

        #10. Return
        hr = self.forceRange(int(UT), 24)
        min = round((UT - int(UT))*60,0)

        return {
            'status': True,
            'decimal': UT,
            'hr': hr,
            'min': min 
        }

    def forceRange( self, v, max ):
        # force v to be >= 0 and < max
        if v < 0:
            return v + max
        elif v >= max:
            return v - max

        return v

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
    result = 0
    GPIO.setup(GPIO_UP_SWITCH,GPIO.IN)
    if GPIO.input(GPIO_UP_SWITCH)==0:
	print("Switch in Up position")
	result = 1
    return result

def closeDoor():
  
    status = WORKING
    finishtime = timer() + CLOSE_TIME
    print finishtime

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

def openDoor():
    status = WORKING
    finishtime = timer() + OPEN_TIME
    print finishtime

    motor(FORWARD) #start the motor closing

    while status == WORKING:
        if timer() >= finishtime: #timer expired
            debugprint ("TIMER EXPIRED")
            status = TIMEOUT
            pushover("Time Out - Check Ramp")
        elif howfar() >= OPEN_DISTANCE:  #Distance sensor shows closed
            print "Sensor states open"
            status = SUCCESS         #All good
        elif manualswitch() != 0:
            pushover("Manual Abort")
            debugprint ("Manual Abort")
            status = SWITCHABORT
    motor(STOPMOTOR)
    return(status)


print("Starting")

sun = Sun()

print sun.getSunriseTime(coords)
# Sunrise time UTC (decimal, 24 hour format)
push ("hi")
print sun.getSunriseTime( coords )['hr'] 
print sun.getSunriseTime( coords )['min']

print sun.getSunsetTime( coords )['hr'] 
print sun.getSunsetTime( coords )['min']
GPIO.setmode(GPIO.BOARD)
print "close door"
closeDoor()
sleep(3)
print "open door"
openDoor()
print("Finishing")

