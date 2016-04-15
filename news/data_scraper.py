# -*- coding: utf-8 -*-

import xmltodict, json, BeautifulSoup, jsontree, os
import requests as req
import rethinkdb as r
from db import database
from newspaper import Article

FILE_PATH = os.path.join(os.path.dirname(__file__), 'data/cities.json')
city_file = os.path.abspath(FILE_PATH)

f = open(city_file, 'r')
cities = f.read()
f.close()

class dataSaver:

  def __init__(self):
    self.table = 'raw_data'
    self.link_table = 'links'
    self.cities = json.loads(cities)
    self.db = database.Database()
    self.connection = self.db.connection_var()
    self.create_table()

  def create_table(self):
    try:
      r.db('raiden').table_create(self.table).run(self.connection)
      print 'Created table [raiden.'+self.table+']'
    except Exception, e:
      print 'Error occured during '+self.table+' table creation! Maybe it already exists!'
      print str(e)

  def get_data(self):
    a = []
    d = r.db('raiden').table(self.link_table).filter({'status': 'no'}).pluck('link', 'id').run(self.connection)
    for b in d:
      a.append(b)
    return a

  def data_extractor(self, group_1):

    try:
      a = Article(group_1['link'])
      a.download()
      a.parse()
      data = a.text.encode('ascii','ignore')
      self.process_save_data(data, group_1['id'])

    except Exception, e:
      print 'Network Error'
      pass

  def data_iterate(self):
    whole_grouped_data = self.get_data()

    for datas in whole_grouped_data:
      self.data_extractor(datas)

  def insertion(self, data):
    print 'inserting'
    r.db('raiden').table(self.table).insert(data).run(self.connection)

  def process_save_data(self, data, gid):
    data_to_save = jsontree.jsontree()
    data_to_save.gid = gid
    data_to_save.desc = data
    self.insertion(data_to_save)

  def start(self):
    self.data_iterate()
