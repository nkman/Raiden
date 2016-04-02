# -*- coding: utf-8 -*-

#city list taken from - https://github.com/nshntarora/Indian-Cities-JSON
import xmltodict, json, os
import requests as req
import rethinkdb as r
from db import database

FILE_PATH = os.path.join(os.path.dirname(__file__), 'data/cities.json')
city_file = os.path.abspath(FILE_PATH)

f = open(city_file, 'r')
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
    # items = json.loads(items)
    items = items['rss']['channel']['item']
    for item in items:
      item['city'] = city
      item['status'] = 'no'
      del item['description']
      self.save_json(item)

  def get_data(self, city):
    print "Getting data of "+city["name"]

    try:
      data = req.get(self.url + city['name'], verify=False)
    except Exception, e:
      print 'Network error for city=' + city['name']
      return
    
    if(data.status_code == 200):
      try:
        data_json = xmltodict.parse(str(data.text.encode('utf-8')))
        self.iterate_item(data_json, city)
      except Exception, e:
        print 'Error '+str(e)+' has been occured for city='+city["name"]
    else:
      print 'Error in status code for city '+ city["name"]

  def start(self):
    for city in self.cities:
      self.get_data(city)
