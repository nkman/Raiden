import json

f = open("cities.json")

txt = f.read()

txtJson = json.loads(txt)

fileWrite = open("cityCoordId.json", "w")
i = 0
dicto = {}
a = {}

for d in txtJson:
	dicto[d['city']['id']] = {
		'city': d["city"]["name"],
		'state': d["city"]["state"],
		'lat': d["city"]["lat"],
		'lng': d["city"]["lng"]
	}

fileWrite.write(json.dumps(dicto))