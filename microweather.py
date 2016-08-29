# get weather info from openweathermap.org
# using zipcode, but could easily change to something else
# requires an openweathermap account for the api key

import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "api.openweathermap.org" 
apikey = "YOUR API KEY"
zipcode = "YOUR ZIP CODE"

url = "/data/2.5/weather?zip=%s,us&APPID=%s" % (zipcode, apikey)

getreq = """GET %s HTTP/1.1\r\nHost: %s\r\n\r\n""" % (url, host)

port = 80

s.connect((host, port))
s.send(getreq)

site = s.recv(1024)
s.close()
sitesplit = site.split("\r\n\r\n")
headers = sitesplit[0]
print(headers)

data = json.loads(sitesplit[-1])
des = data["weather"][0]["main"]
temp = int(float(data["main"]["temp"]) * (9.0/5.0) - 459.67)
print(des, temp)
