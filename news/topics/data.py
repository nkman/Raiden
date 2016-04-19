import os, time, nltk
import rethinkdb as r
from db import database

FILE_PATH = os.path.join(os.path.dirname(__file__), '../data/stopwords.txt')
stopwords_file = os.path.abspath(FILE_PATH)

class dataHandler:

  def __init__(self):
    self.db = database.Database()
    self.connection = self.db.connection_var()
    self.table = 'tagged_data'
    self.create_table()

    self.data_table = 'raw_data'

    self.done = 0
    self.start = time.time()
    self.stopwords = {}
    self.populate_stopwords()

    self.__data = self.get_data()

  def populate_stopwords(self):
    with open(stopwords_file, 'rU') as f:
      for line in f:
        self.stopwords[line.strip()] = 1

  def create_table(self):
    try:
      r.db('Raiden').table_create(self.table).run(self.connection)
      print 'Created table [Raiden.'+self.table+']'
    except Exception, e:
      print 'Error occured during '+self.table+' table creation! Maybe it already exists!'
      print str(e)

  def get_data(self):
    a = []
    d = r.db('Raiden').table(self.data_table).pluck('desc', 'gid').run(self.connection)
    for b in d:
      a.append(b)
    return a

  def insert_data(self, data):
    r.db('Raiden').table(self.table).insert(data).run(self.connection)

  
  def iterate_data(self):
    for _data in self.__data:
      words = []
      #Make array of sentences. Similar to sentences.split('.')
      sentences = nltk.sent_tokenize(_data["desc"].lower())

      for sentence in sentences:
        #Array of words in text. Similar to sentence.split(' ')
        tokens = nltk.word_tokenize(sentence)
        text = [word for word in tokens if word not in self.stopwords]
        #Tag the words to noun(NN), conjunction(CC), preposition(IN), adverb(RB), adjective(JJ) etc..
        tagged_text = nltk.pos_tag(text)

        for word, tag in tagged_text:
          words.append({"word": word, "pos": tag})

      tagged_d = {
        "gid": _data["gid"],
        "text": _data["desc"],
        "words": words
      }

      self.insert_data(tagged_d)
      self.done += 1
      if self.done % 100 == 0:
        end = time.time()
        print 'Done ' + str(self.done) + ' out of ' + str(len(self.__data)) + ' in ' + str((end - self.start))

  def start(self):
    self.iterate_data()
