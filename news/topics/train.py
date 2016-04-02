import gensim
from gensim.corpora import BleiCorpus
from gensim import corpora

import os, time, logging
import rethinkdb as r
from db import database

class Corpus(object):
  def __init__(self, cursor, tag_dictionary, corpus_path):
    self.cursor = cursor
    self.tag_dictionary = tag_dictionary
    self.corpus_path = corpus_path

  def __iter__(self):
    for tag in self.cursor:
      yield self.tag_dictionary.doc2bow(tag["words"])

  def serialize(self):
    BleiCorpus.serialize(self.corpus_path, self, id2word=self.tag_dictionary)
    return self


class Dictionary(object):
  def __init__(self, cursor, dictionary_path):
    self.cursor = cursor
    self.dictionary_path = dictionary_path

  def build(self):
    dictionary = corpora.Dictionary(tag["words"] for tag in self.cursor)
    dictionary.filter_extremes(keep_n=100000)
    dictionary.compactify()
    corpora.Dictionary.save(dictionary, self.dictionary_path)

    return dictionary


class Train:
  def __init__(self):
    pass

  @staticmethod
  def run(lda_model_path, corpus_path, num_topics, id2word):
    corpus = corpora.BleiCorpus(corpus_path)
    lda = gensim.models.LdaModel(corpus, num_topics=num_topics, id2word=id2word)
    lda.save(lda_model_path)

    return lda

class dbHandler:

  def __init__(self):
    self.db = database.Database()
    self.connection = self.db.connection_var()
    self.corpus_table = 'corpus_data'
    
  def get_data(self):
    a = []
    d = r.db('raiden').table(self.corpus_table).run(self.connection)
    for b in d:
      a.append(b)
    return a

def start_training():
  logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

  cwd = os.path.dirname(__file__)
  dictionary_path = os.path.abspath(os.path.join(cwd, 'models/dictionary.dict'))
  corpus_path = os.path.abspath(os.path.join(cwd, 'models/corpus.lda-c'))
  lda_num_topics = 20
  lda_model_path = os.path.abspath(os.path.join(cwd, 'models/lda_model_50_topics.lda'))

  corpus_cursor = dbHandler().get_data()

  dictionary = Dictionary(corpus_cursor, dictionary_path).build()
  Corpus(corpus_cursor, dictionary, corpus_path).serialize()
  Train.run(lda_model_path, corpus_path, lda_num_topics, dictionary)
