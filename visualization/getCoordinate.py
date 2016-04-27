import json
import requests as req

SERVER_KEY = "AIzaSyCIplbLWIyiankR9NoNmOd6fSbuZLvOkGc"

base = "https://maps.googleapis.com/maps/api/geocode/json?address="

f = open("topic_fraction.json")

txt = f.read()

txtJson = json.loads(txt)

fileWrite = open("cities.json", "w")
i = 1
for jsn in txtJson:
	city = jsn["city"]["name"]
	state = jsn["city"]["state"]
	r = req.get(base + city + "+" + state + "&key=" + SERVER_KEY)
	jLatLng = json.loads(r.text)
	lat = jLatLng['results'][0]['geometry']['location']['lat']
	lng = jLatLng['results'][0]['geometry']['location']['lng']
	jsn["city"]["lat"] = state(lat)
	jsn["city"]["lng"] = str(lng)
	print i
	i = i + 1

fileWrite.write(json.dumps(txtJson))