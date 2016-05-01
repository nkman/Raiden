import logging, os

from gensim.models import LdaModel
from gensim import corpora


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

cwd = os.path.dirname(__file__)
dictionary_path = os.path.abspath(os.path.join(cwd, 'models/dictionary.dict'))
corpus_path = os.path.abspath(os.path.join(cwd, 'models/corpus.lda-c'))
lda_num_topics = 15
lda_model_path = os.path.abspath(os.path.join(cwd, 'models/lda_model_10_topics.lda'))

dictionary = corpora.Dictionary.load(dictionary_path)
corpus = corpora.BleiCorpus(corpus_path)
lda = LdaModel.load(lda_model_path)

i = 0
for topic in lda.show_topics(num_topics=lda_num_topics):
  print '#' + str(i) + ': ' + str(topic)
  i += 1