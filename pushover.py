import httplib, urllib
from time import ctime
APP_TOKEN = "ap1zxxfpdcnbkkfk5fk9daoob78hpb"
USER_ID = "uZ8cbsrmeoMiMJEU6MzHTVKNwrPUr2"

debug = True

def push(push_text):
    title = "Hen Hotel :" +ctime()
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    if debug == False:
        conn.request("POST", "/1/messages.json",urllib.urlencode({"token": APP_TOKEN ,"user":
            USER_ID, "message": push_text,"title": title}),
            { "Content-type": "application/x-www-form-urlencoded" })
    print "Pushover:  " + push_text
    return  # End of function push

push("Door opened successfully")
