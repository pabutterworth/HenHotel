import time
from datetime import date, timedelta, datetime, time, tzinfo, ctime
from time import sleep
import math 
from pushover import push
from doorcontrol import openDoor, closeDoor, howfar
from sun3 import calcsunriseandsunset
MAXTIME = 30
CLOSED = 10 #this is the readingf or a closed ramp
OPEN = 50

DELAY = 20 # Delay sfter sunset to close door

longitude=0.2637 #East
latitude=51.1324

def timer():
   now = time.localtime(time.time())
   return now[5]


def main():
    today=date.today()
    sunRiseHour,sunRiseMins,sunSetHour,sunSetMins = calcsunriseandsunset(today)
    print sunRiseHour,sunRiseMins,sunSetHour,sunSetMins
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

    if daytime==True:
        print "Its daytime"
        itsdaytime = True
    else:
        print "Its nighttime"
        itsdaytime = False
    
    quit = False
    oldHour = nowHour
    
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
            
      print ("Time now is" +ctime())
"""
        #Just an hourly ping to see if the wifi stops working
        if oldHour != nowHour:
            msg = "New Hour"
            push(msg)
            print msg
            oldHour = nowHour
"""
        if itsdaytime == True and daytime == False:
            push("Closing door")
            print "Its nighttime at "
            print now 
            itsdaytime = False
        
        if itsdaytime == False and daytime == True:
            push("Opening Door")
            print "Its daytime at "
            print now
            itsdaytime = True
    # End of while
#End of main
#test


if __name__ == '__main__':
   main()
