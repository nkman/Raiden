import json
import requests as req

SERVER_KEY = "AIzaSyCIplbLWIyiankR9NoNmOd6fSbuZLvOkGc"

base = "https://maps.googleapis.com/maps/api/geocode/json?address="

f = open("cities.json")

txt = f.read()

txtJson = json.loads(txt)

fileWrite = open("cityPredId.json", "w")
i = 0
dicto = {}
for jsn in txtJson:
	Id = jsn["city"]["id"]
	prediction = jsn["prediction"]
	dicto[Id] = prediction
	print i
	i = i + 1

fileWrite.write(json.dumps(dicto))