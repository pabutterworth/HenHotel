#!/usr/bin/env python2.7  

from datetime import date, timedelta, datetime, time, tzinfo
import math 

def sinrad(deg):
    return math.sin(deg * math.pi/180)

def cosrad(deg):
    return math.cos(deg * math.pi/180)

def calculateHourfromjuliandate(jd):
    jd=jd+.5
    secs=int((jd-int(jd))*24*60*60+.5)
    mins=int(secs/60)
    hour=int(mins/60)  
    return hour

def calculateMinsfromjuliandate(jd):
    jd=jd+.5
    secs=int((jd-int(jd))*24*60*60+.5)
    mins=int(secs/60)
    hour=int(mins/60)  
    return mins % 60
    
def calcsunriseandsunset(dt):
    a=math.floor((14-dt.month)/12)
    y = dt.year+4800-a
    m = dt.month+12*a -3
    julian_date=dt.day+math.floor((153*m+2)/5)+365*y+math.floor(y/4)-math.floor(y/100)+math.floor(y/400)-32045
    
    nstar= (julian_date - 2451545.0 - 0.0009)-(longitude/360)
    n=round(nstar)
    jstar = 2451545.0+0.0009+(longitude/360) + n
    M=(357.5291+0.98560028*(jstar-2451545)) % 360
    c=(1.9148*sinrad(M))+(0.0200*sinrad(2*M))+(0.0003*sinrad(3*M))
    l=(M+102.9372+c+180) % 360
    jtransit = jstar + (0.0053 * sinrad(M)) - (0.0069 * sinrad(2 * l))
    delta=math.asin(sinrad(l) * sinrad(23.45))*180/math.pi
    H = math.acos((sinrad(-0.83)-sinrad(latitude)*sinrad(delta))/(cosrad(latitude)*cosrad(delta)))*180/math.pi
    jstarstar=2451545.0+0.0009+((H+longitude)/360)+n
    jset=jstarstar+(0.0053*sinrad(M))-(0.0069*sinrad(2*l))
    jrise=jtransit-(jset-jtransit)
    return (calculateHourfromjuliandate(jrise),calculateMinsfromjuliandate(jrise),calculateHourfromjuliandate(jset),calculateMinsfromjuliandate(jset) )


    
longitude=0.2637 #East
latitude=51.1324

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

    if daytime==True:
	print "Its daytime"
    else:
	print "Its nighttime"

if __name__ == '__main__':
   main()

