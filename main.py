import time
from distance import howfar
MAXTIME = 30
CLOSED = 10 #this is the readingf or a closed ramp
OPEN = 50

def timer():
   now = time.localtime(time.time())
   return now[5]


def closeDoor():
    working = 0
    timeout = 1
    switchabort = 2
    distanceabort = 3

    status = working
    finishtime = timer()+MAXTIME

    reverse() #start the motor closing

    while status == working:
        if timer() >= finishtime: #timer expired
            print("timer expired")
            status = timeout
            pushover("Time Out - Check Ramp")
        elif howfar() <= CLOSED:  #Distance sensor shows closed
            print("Distannse sensor shows closed")
            status = closed         #All good
        elif manualswitch() != 0:
            print("Manual Abort")
            pushover("Manual Abort")
            status = switchabort
    stopmotor()
    return(status)
