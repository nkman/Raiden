# -*- coding: utf-8 -*-

import xmltodict, json, BeautifulSoup, jsontree, os
import requests as req
import rethinkdb as r
from db import database

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
    # self.create_table()

  def create_table(self):
    try:
      r.db('raiden').table_create(self.table).run(self.connection)
      print 'Created table [raiden.'+self.table+']'
    except Exception, e:
      print 'Error occured during '+self.table+' table creation! Maybe it already exists!'
      print str(e)

  def get_data(self):
    return r.db('raiden').table(self.link_table).run(self.connection)

  def data_extractor(self, group_1):
    data = req.get(group_1.link)
    if(data.status_code == 200):
      self.process_save_data(data, group_1.id)
    else:
      print 'Error occured to get data from ' + group_1.link

  def data_iterate(self):
    whole_grouped_data = self.get_data()

    f = open('sample.txt', 'w')
    f.write(str(whole_grouped_data))
    f.close()

    for datas in whole_grouped_data:
      for data in datas.reduction:
        self.data_extractor(data)

  def insertion(self, data):
    r.db('raiden').table(self.table).insert(data).run(self.connection)

  def process_save_data(self, data):
    soup = BeautifulSoup.BeautifulSoup(data, gid)
    p_text = soup.findAll('p')

    a = ''

    for p in p_text:
      a += str(p.renderContents())

    data_to_save = jsontree.jsontree()

    data_to_save.gid = gid
    data_to_save.desc = a
    self.insertion(data_to_save)

  def start(self):
    # self.data_iterate()
    print self.get_data()
