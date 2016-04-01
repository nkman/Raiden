import os, time, nltk
from settings import Settings
import rethinkdb as r
from db import database

class dataHandler:

  def __init__(self):
    self.table = 'tagged_data'
    self.db = database.Database()
    self.connection = self.db.connection_var()
    self.create_table()
    self.data_table = 'raw_data'
  
  def create_table(self):
    try:
      r.db('raiden').table_create(self.table).run(self.connection)
      print 'Created table [raiden.'+self.table+']'
    except Exception, e:
      print 'Error occured during '+self.table+' table creation! Maybe it already exists!'
      print str(e)

  def get_data(self):
    a = []
    d = r.db('raiden').table(self.data_table).pluck('desc', 'gid').run(self.connection)
    for b in d:
      a.append(b)

  def insert_data(self, data):
    r.db('raiden').table(self.table).insert(data).run(self.connection)

