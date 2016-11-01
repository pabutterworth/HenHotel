import time
from datetime import date, timedelta, datetime, time, tzinfo
from time import sleep
import math 
from pushover import push
from doorcontrol import openDoor, closeDoor, howfar
from sun3 import calcsunriseandsunset
MAXTIME = 30
CLOSED = 10 #this is the readingf or a closed ramp
OPEN = 50

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
    
    while (quit == False):
        sleep(30) # Extend this later, or replace with an interruptable sleep
        today=date.today()
        sunRiseHour,sunRiseMins,sunSetHour,sunSetMins = calcsunriseandsunset(today)
        now = datetime.now()
        print "Its " 
        print now
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
