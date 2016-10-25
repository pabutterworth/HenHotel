import httplib, urllib
from time import ctime
APP_TOKEN = "ahtdgjqm8w9xxv1v4bzsuwap5c6o7o"
USER_KEY = "uZ8cbsrmeoMiMJEU6MzHTVKNwrPUr2"

DEBUG = 0

def push(push_text):
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    if DEBUG != 1:
        print("Sending Pushover Notification :"+ push_text)
        conn.request("POST", "/1/messages.json",
          urllib.urlencode({
            "token": "APP_TOKEN",
            "user": "USER_KEY",
            "title": "Hen Hotel",
            "message": ctime() + " " + push_text,
          }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
    else:
        print("DEBUG: Pushover - "+ push_text)
    return
    #end of function push

push ("Testing")
