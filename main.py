import time
import RPi.GPIO as GPIO
from datetime import date, timedelta, datetime, time, tzinfo
from time import sleep, ctime
import math 
from pushover import push
from doorcontrol import openDoor, closeDoor, howfar
from sun3 import calcsunriseandsunset
MAXTIME = 164
CLOSED = 164 #this is the readingf or a closed ramp
OPEN = 164

DELAY = 30 # Delay sfter sunset to close door

longitude=0.2637 #East
latitude=51.1324

import logging
import logging.handlers



def timer():
   now = time.localtime(time.time())
   return now[5]


def main():
    log = logging.getLogger(__name__)

    log.setLevel(logging.DEBUG)

    handler = logging.handlers.SysLogHandler(address = '/dev/log')

    formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
    handler.setFormatter(formatter)

    log.addHandler(handler)
    today=date.today()
    sunRiseHour,sunRiseMins,sunSetHour,sunSetMins = calcsunriseandsunset(today)
    print sunRiseHour,sunRiseMins,sunSetHour,sunSetMins
    now = datetime.now()
    nowHour = now.hour
    nowMins = now.minute
    #push("HenHotel starting")

    GPIO.setmode(GPIO.BOARD)
        
    daytime=False

    if nowHour > sunRiseHour and nowHour < sunSetHour:
        daytime=True
    if nowHour == sunRiseHour and nowMins >= sunRiseMins:
        daytime=True
    if nowHour == sunSetHour and nowMins < sunSetMins:
        daytime=True

    if daytime==True:
        print "Its daytime"
        log.debug('Daytime')
        itsdaytime = True
    else:
        print "Its nighttime"
        log.debug('Nighttime')
        itsdaytime = False
    
    quit = False
    oldHour = nowHour
    try:
	 
        while (quit == False):
		sleep(30) # Extend this later, or replace with an interruptable sleep
		today=date.today()
		sunRiseHour,sunRiseMins,sunSetHour,sunSetMins = calcsunriseandsunset(today)
		#Add a delay after sunset do give the birds time to go in
		sunSetMins += DELAY
		if sunSetMins >= 60:
		    sunSetHour += 1
		    sunSetMins -= 60

		now = datetime.now()
		nowHour = now.hour
		nowMins = now.minute
		daytime=False
		if nowHour > sunRiseHour and nowHour < sunSetHour:
		    daytime=True
		if nowHour == sunRiseHour and nowMins >= sunRiseMins:
		    daytime=True
		if nowHour == sunSetHour and nowMins < sunSetMins:
		    daytime=True

		if itsdaytime == True and daytime == False:
		    message = "Door Starting to close - distance = " +str(howfar()) +"cm"
                    push(message)
		    log.debug(message)
		    closeDoor()
		    message = "Door should be closed - distance = " +str(howfar()) +"cm"
                    push(message)
                    print "Its nighttime at "
	            print now 
		    itsdaytime = False

		if itsdaytime == False and daytime == True:
    		    message = "Door Starting to open - distance = " +str(howfar()) +"cm"
                    push(message)
		    log.debug(message)
		    openDoor()
		    message = "Door should be open - distance = " +str(howfar()) +"cm"
                    push(message)
		    print "Its daytime at "
		    print now
		    itsdaytime = True
    # End of while
#End of main
#test
  
    #except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
     #   print "Other error or exception occurred!"  
  
    finally: 
        GPIO.cleanup() # this ensures a clean exit 
	print "In Finally function" 
	push ("In Finally, not sure what happened - system needs a reboot")


if __name__ == '__main__':
   main()

