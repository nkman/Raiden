#city list taken from - https://github.com/nshntarora/Indian-Cities-JSON
import xmltodict, json
import requests as req
import rethinkdb as r
from db import database

f = open('./data/cities.json', 'r')
cities = f.read()
f.close()

class LinkCrawler:
  
  def __init__(self):
    self.table = 'links'
    self.cities = json.loads(cities)
    self.db = database.Database()
    self.connection = self.db.connection_var()
    self.url = 'https://news.google.com/news?output=rss&num=30&q='
    self.create_table()

  def create_table(self):
    try:
      r.db('raiden').table_create(self.table).run(self.connection)
      print 'Created table [raiden.'+self.table+']'
    except Exception, e:
      print 'Error occured during '+self.table+' table creation! Maybe it already exists!'
      print str(e)
  
  def save_json(self, item):
    # item = json.dumps(json.loads(item).update({}))
    r.db('raiden').table(self.table).insert(item).run(self.connection)

  def iterate_item(self, items, city):
    items = json.loads(items)
    items = items['rss']['item']
    for item in items:
      item['city'] = city
      del item['description']
      save_json(json.dumps(item))

  def get_data(self, city):
    print "Getting data of "+city["name"]
    data = req.get(self.url + city['name'])
    if(data.status_code == 200):
      try:
        data_json = xmltodict.parse(data.text)
        # data_json = json.dumps(data_json)
        self.iterate_item(data_json, city)
      except Exception, e:
        print 'Error '+str(e)+' has been occured for city='+city["name"]
    else:
      print 'Error in status code for city '+ city["name"]

  def start(self):
    for city in self.cities:
      get_data(city)
