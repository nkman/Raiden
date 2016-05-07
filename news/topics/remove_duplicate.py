import os, time
import rethinkdb as r
from db import database

class removeDuplicate:

  def __init__(self):
    self.db = database.Database()
    self.connection = self.db.connection_var()
    self.raw_table = 'raw_data'
    self.count = 0

  def get_data(self):
    a = []
    d = r.db('Raiden').table(self.raw_table).pluck('gid').run(self.connection)
    for b in d:
      a.append(b['gid'])
    return a

  def delete_data(self, _id):
    d = r.db('Raiden').table(self.raw_table).filter({'id': _id}).delete().run(self.connection)
    self.count += 1
    print "Deleted " + str(self.count)

  def get_ids(self, gid):
    a = []
    d = r.db('Raiden').table(self.raw_table).filter({'gid': gid}).pluck('id').run(self.connection)
    for b in d:
      a.append(b['id'])
    return a

  def iterate_data_deletion(self):
    all_gid = self.get_data()
    for single_gid in all_gid:
      id_list = self.get_ids(single_gid)
      
      if len(id_list) > 1:
        for ids in range (1, len(id_list)):
          self.delete_data(id_list[ids])
          ids += 1
      else:
        pass
