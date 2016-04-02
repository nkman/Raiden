import os, time
import rethinkdb as r
from db import database
from nltk.stem.wordnet import WordNetLemmatizer

class corpusHandler:

  def __init__(self):
    self.db = database.Database()
    self.connection = self.db.connection_var()
    self.tags_table = 'tagged_data'
    self.corpus_table = 'corpus_data'
    self.create_table()

    self.start = time.time()
    self.done = 0

    self.lem = WordNetLemmatizer()

  def create_table(self):
    try:
      r.db('raiden').table_create(self.corpus_table).run(self.connection)
      print 'Created table [raiden.'+self.corpus_table+']'
    except Exception, e:
      print 'Error occured during '+self.corpus_table+' table creation! Maybe it already exists!'
      print str(e)

  def get_data(self):
    a = []
    d = r.db('raiden').table(self.tags_table).run(self.connection)
    for b in d:
      a.append(b)
    return a

  def insert_data(self, data):
    r.db('raiden').table(self.corpus_table).insert(data).run(self.connection)

  def iterate_tags(self):
    self.tagged_data = self.get_data()
    for __data in self.tagged_data:
      nouns = []
      words = [word for word in __data["words"] if word["pos"] in ["NN", "NNS"]]

      for word in words:
        nouns.append(self.lem.lemmatize(word["word"]))

      corpus_to_save = {
        "gid": __data["gid"],
        "text": __data["text"],
        "words": nouns
      }

      self.insert_data(corpus_to_save)

      self.done += 1
      if self.done % 100 == 0:
        end = time.time()
        print 'Done ' + str(self.done) + ' out of ' + str(len(self.tagged_data)) + ' in ' + str((end - self.start))
