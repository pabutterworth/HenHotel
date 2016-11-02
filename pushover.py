import httplib, urllib
from time import ctime
APP_TOKEN = "ap1zxxfpdcnbkkfk5fk9daoob78hpb"
USER_ID = "uZ8cbsrmeoMiMJEU6MzHTVKNwrPUr2"

debug = False

"""urgent - send as -2 to generate no notification/alert, -1 to 
always send as a quiet notification, 1 to display as high-priority 
and bypass the user's quiet hours, or 2 to also require confirmation from the user"""

def push(push_text, urgent=1):
    title = "Hen Hotel :" +ctime()
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    if debug == False:
        conn.request("POST", "/1/messages.json",urllib.urlencode({"token": APP_TOKEN ,"user":
            USER_ID, "message": push_text,"title": title}),
            { "Content-type": "application/x-www-form-urlencoded" })
    print "Pushover:  " + push_text
    return  # End of function push


def main()
    push("normal message")
    push("Priority message 1",1)
    push("Priority message 2",2)
        
        
if __name__ == '__main__':
   main()
