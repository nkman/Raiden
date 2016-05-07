# -*- coding: utf-8 -*-

#city list taken from - https://github.com/nshntarora/Indian-Cities-JSON
import xmltodict, json, os, time
import requests as req
import rethinkdb as r
from db import database
from threading import Thread

FILE_PATH = os.path.join(os.path.dirname(__file__), 'data/cities.json')
city_file = os.path.abspath(FILE_PATH)

f = open(city_file, 'r')
cities = f.read()
f.close()

parsed_cities = json.loads(cities)

class LinkCrawler:
  
  def __init__(self):
    self.table = 'links'
    self.db = database.Database()
    self.connection = self.db.connection_var()
    self.url = 'https://news.google.com/news?output=rss&num=30&q='
    self.session = req.Session()
    self.create_table()

  def create_table(self):
    try:
      r.db('Raiden').table_create(self.table).run(self.connection)
      print 'Created table [Raiden.'+self.table+']'
    except Exception, e:
      print 'Error occured during '+self.table+' table creation! Maybe it already exists!'
      print str(e)
  
  def save_json(self, item):
    # item = json.dumps(json.loads(item).update({}))
    r.db('Raiden').table(self.table).insert(item).run(self.connection)

  def iterate_item(self, items, city):
    # items = json.loads(items)
    items = items['rss']['channel']['item']
    for item in items:
      item['city'] = city
      item['status'] = 'non'
      del item['description']
      self.save_json(item)

  def get_data(self, city):
    print "Getting data of "+city["name"]

    try:
      data = self.session.get(self.url + city['name'], verify=False)
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
      #os.system('say "Enter the captcha in browser manually"')
      #raw_input()
      self.session = req.Session()


  def start_lc(self, i_i, per_thread):

    for i in range(i_i*per_thread, (i_i*per_thread)+per_thread):
      self.get_data(parsed_cities[i])
      i += 1

total_city = len(parsed_cities)
total_thread = 4

per_thread = total_city/total_thread
working_threads = [None]*total_thread

class start_parallel:

  def start_link(self):
    for i in range(0, total_thread):
      linkCrawler = LinkCrawler()
      working_threads[i] = Thread(target=linkCrawler.start_lc, args=(i, per_thread,))
      working_threads[i].start()
      i+=1

    for j in range(0, total_thread):
      working_threads[j].join()
      j+=1

    print "completes the link crawling"
