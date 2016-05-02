# -*- coding: utf-8 -*-

import xmltodict, json, BeautifulSoup, jsontree, os
import requests as req
import rethinkdb as r
from db import database
from newspaper import Article
from threading import Thread

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
      r.db('Raiden').table_create(self.table).run(self.connection)
      r.db('Raiden').table_create('failed_links').run(self.connection)
      print 'Created table [Raiden.'+self.table+']'
    except Exception, e:
      print 'Error occured during '+self.table+' table creation! Maybe it already exists!'
      print str(e)

  def get_data(self):
    a = []
    d = r.db('Raiden').table(self.link_table).filter({'status': 'none'}).pluck('link', 'id').run(self.connection)
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
      self.insertion({"desc": "", "err": "network error", "gid": group_1['id']})

  def data_iterate(self, whole_grouped_data):
    # whole_grouped_data = self.get_data()

    for datas in whole_grouped_data:
      self.data_extractor(datas)

  def insertion(self, data):
    
    if(data['desc'] == ""):
      r.db('Raiden').table('failed_links').insert(data).run(self.connection)
      print "pass"
    else:
      r.db('Raiden').table(self.table).insert(data).run(self.connection)
      print 'inserting'

  def process_save_data(self, data, gid):
    data_to_save = jsontree.jsontree()
    data_to_save.gid = gid
    data_to_save.desc = data
    data_to_save.status = 'none'
    self.insertion(data_to_save)

  def start(self):
    self.multi_threads()

#Get total count of the table data
#Create 10 threads, parallalize it
  def get_table_count(self):
    d = r.db('Raiden').table(self.link_table).count().run(self.connection)
    return d

  def get_data_skiped(self, skip_d, limit_d):
    a = []
    d = r.db('Raiden').table(self.link_table).pluck('link', 'id').skip(skip_d).limit(limit_d).run(self.connection)
    for b in d:
      a.append(b)
    return a


class ParallelScraping:

  def multi_threads(self):

    data_saver = dataSaver()
    total_d = data_saver.get_table_count()
    total_threads = 5

    threads_d = [None]*total_threads

    for i in range(0, total_threads):
      data_saver = dataSaver()
      data_d = data_saver.get_data_skiped((i*total_d)/total_threads, total_d/total_threads)
      threads_d[i] = Thread(target=data_saver.data_iterate, args=(data_d,))
      threads_d[i].start()

    for j in range(0, total_threads):
      threads_d[j].join()
      j += 1