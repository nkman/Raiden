import os, time, nltk
import rethinkdb as r
from db import database
from threading import Thread

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

  def get_data(self, defined_num, defined_skip):
    a = []
    d = r.db('Raiden').table(self.data_table).pluck('desc', 'gid').skip(defined_skip).limit(defined_num).run(self.connection)
    for b in d:
      a.append(b)
    return a

  def get_total_data(self):
    print "Requesting total data"
    total = r.db('Raiden').table(self.data_table).count().run(self.connection)
    return total

  def insert_data(self, data):
    r.db('Raiden').table(self.table).insert(data).run(self.connection)

  
  def iterate_data(self, defined_num, defined_skip):

    print "Iterating with defined_num=" + str(defined_num)
    done = 0
    __data = self.get_data(defined_num, defined_skip)
    for _data in __data:
      words = []
      #Make array of sentences. Similar to sentences.split('.')
      sentences = nltk.sent_tokenize(_data["desc"].lower())

      for sentence in sentences:
        #Array of words in text. Similar to sentence.split(' ')
        tokens = nltk.word_tokenize(sentence)
        #Filter out stopwrods and words with length < 3
        text = [word for word in tokens if word not in self.stopwords and len(word) > 3]
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
      done += 1
      if done % 100 == 0:
        end = time.time()
        print 'Done ' + str(done) + ' out of ' + str(len(__data)) + ' in ' + str((end - self.start))

class Start:

  def start_tagging(self):
    datahandler = dataHandler()
    total_data = datahandler.get_total_data()

    threads = [None]*10

    # Create 10 threads!
    for i in range(0, 10):
      x = dataHandler()
      threads[i] = Thread(target=x.iterate_data, args=(total_data/10, (i*total_data)/10,))
      threads[i].start()
      i += 1
    
    for j in range(0, 10):
      threads[j].join()
      j += 1

    print "Completed Tagging"
