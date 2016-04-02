import logging, os, nltk
from gensim.models import LdaModel
from gensim import corpora
from nltk.stem.wordnet import WordNetLemmatizer


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

    print new_text_lda


def main():
  logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

  new_text = """
  Tamil Nadu Medical Council (TNMC) has suspended three doctors, two of them from Chennai, for violating laws. One of the doctors has been suspended for five years, the second for a year and the third for six months. In the first instance, the licence of Ramachandran (55) of Mahalakshmi Nursing Home in Neyveli was suspended as investigations by the district authorities had revealed that he was a habitual offender who routinely revealed the gender of foetus after an ultrasound scan. He was suspended for five years as it was considered a deliberate violation of the Preconception and Prenatal Diagnostic Techniques Act. The report of an inspection conducted by the Joint Director and the Collector in 2014 was sent to the Director of Medical Services who sent the report to the TNMC. &#8220;It has been pursued since 2014 but we had to check the evidence. We placed it before the ethical committee which took the decision,&#8221; an official said. The Council also suspended laparoscopic surgeon M. Maran who was attached to Bharathiraaja Hospital in T. Nagar, Chennai, for a year on charges of misconduct and negligence. Dr. Maran had performed a bariatric surgery following which the woman developed complications and she was admitted to another private hospital. The patient died nine months later. Blank cheque &#8220;The complications following the surgery were not considered a serious negligence but giving the patient&#8217;s family a blank cheque was considered an offence,&#8221; said a member of the Council. A patient of the Women and Child Foundation in T. Nagar, Chennai, had complained that a wad of cotton was left inside her abdomen after a surgery. The doctor, Rajasekar, was punished for negligence with a six-month suspension. According to the Council members, the doctor had left the mop pad in her abdomen which was later removed. The patient is also expected to be financially compensated by the consumer court.  Downtown OPEN"
  """

  predict = Predict()
  predict.run(new_text)


if __name__ == '__main__':
  main()