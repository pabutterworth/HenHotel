import httplib, urllib
from time import ctime
APP_TOKEN = "ahtdgjqm8w9xxv1v4bzsuwap5c6o7o"
USER_KEY = "uZ8cbsrmeoMiMJEU6MzHTVKNwrPUr2"

DEBUG = 1

def push(push_text):
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    if !DEBUG
        conn.request("POST", "/1/messages.json",
          urllib.urlencode({
            "token": "APP_TOKEN",
            "user": "USER_KEY",
            "title": "Hen Hotel",
            "message": ctime() + " " + push_text,
          }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
    return #end of function push

push ("Testing")
