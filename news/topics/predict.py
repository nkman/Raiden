import logging, os, nltk, time
from gensim.models import LdaModel
from gensim import corpora
from nltk.stem.wordnet import WordNetLemmatizer

import rethinkdb as r
from db import database

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class Predict():
  def __init__(self):

    cwd = os.path.dirname(__file__)
    dictionary_path = os.path.abspath(os.path.join(cwd, 'models/dictionary.dict'))
    lda_model_path = os.path.abspath(os.path.join(cwd, 'models/lda_model_50_topics.lda'))

    self.dictionary = corpora.Dictionary.load(dictionary_path)
    self.lda = LdaModel.load(lda_model_path)

  def load_stopwords(self):
    FILE_PATH = os.path.join(os.path.dirname(__file__), '../data/stopwords.txt')
    stopwords_file = os.path.abspath(FILE_PATH)
    stopwords = {}
    with open(stopwords_file, 'rU') as f:
      for line in f:
        stopwords[line.strip()] = 1

    return stopwords

  def extract_lemmatized_nouns(self, new_text):
    stopwords = self.load_stopwords()
    words = []

    sentences = nltk.sent_tokenize(new_text.lower())
    for sentence in sentences:
      tokens = nltk.word_tokenize(sentence)
      text = [word for word in tokens if word not in stopwords]
      tagged_text = nltk.pos_tag(text)

      for word, tag in tagged_text:
        words.append({"word": word, "pos": tag})

    lem = WordNetLemmatizer()
    nouns = []
    for word in words:
      if word["pos"] in ["NN", "NNS"]:
        nouns.append(lem.lemmatize(word["word"]))

    return nouns

  def run(self, new_text):
    nouns = self.extract_lemmatized_nouns(new_text)
    new_text_bow = self.dictionary.doc2bow(nouns)
    new_text_lda = self.lda[new_text_bow]

    return new_text_lda

class dataDBHandler:

  def __init__(self):
    self.db = database.Database()
    self.connection = self.db.connection_var()
    self.table = 'raw_data'
    self.link_table = 'links'
    self.start = time.time()
    self.done = 0

    self.topic_table = 'topic_fraction'
    self.create_table()

    self.predict = Predict()

  def create_table(self):
    try:
      r.db('raiden').table_create(self.topic_table).run(self.connection)
      print 'Created table [raiden.'+self.topic_table+']'
    except Exception, e:
      print 'Error occured during '+self.topic_table+' table creation! Maybe it already exists!'
      print str(e)

  def insert_data(self, data):
    r.db('raiden').table(self.topic_table).insert(data).run(self.connection)

  def get_ids(self):
    a = []
    d = r.db('raiden').table(self.link_table).pluck('city', 'id').group('city').run(self.connection)
    for b in d:
      temp = {}
      for b1 in b:
        temp[b1[0]] = b1[1]

      ids = []
      for x in d[b]:
        ids.append(x['id'])

      a.append({'city': temp, 'ids': ids})
    
    #Output of the form ./samples/1.json
    return a

  def get_desc(self, ids):
    text = ' '
    for _id in ids:
      d = r.db('raiden').table(self.table).filter({'gid': _id}).pluck('desc').run(self.connection)
      for x in d:
        text += x['desc']
        text += '\n'

    return text

  def iterate_text(self):
    id_list = self.get_ids()
    total_city = len(id_list)

    for _id in id_list:
      desc = self.get_desc(_id['ids'])
      prediction = self.predict.run(desc)

      x = {}
      x['prediction'] = prediction
      x['city'] = _id['city']

      self.insert_data(x)
      self.done += 1
      
      end = time.time()
      print 'Done ' + str(self.done) + ' out of ' + str(total_city) + ' in ' + str((end - self.start))
