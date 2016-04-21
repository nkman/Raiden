import re
import sys
import requests
from newspaper import Article
from nltk.corpus import stopwords

from nltk.stem.porter import *
porter_stemmer = PorterStemmer()

#url = 'http://www.indiatimes.com/news/india/delhi-traffic-snarls-force-2-women-to-give-birth-to-babies-in-bus-auto-rickshaw-246838.html'
url = 'http://www.indiatimes.com/news/india/this-indian-techie-gave-up-his-us-job-to-generate-crores-for-india-s-poorest-farmers-246656.html'

article = Article(url)
article.download()
article.parse()

data = article.text.encode('ascii','ignore')
data = data.lower()

chars_to_remove = ['.', '(', ')', ',', '"', ':', ';', '?', '!']

data = data.translate(None, ''.join(chars_to_remove))
data = data.replace("\n", " ")
data = data.replace("-", " ")

data_list = data.split(" ")

filtered_data_list = [word for word in data_list if word not in stopwords.words('english')]

for word in filtered_data_list:
	if word is not "":
		if (porter_stemmer.stem(word) == word):
			word = word.replace("'", "")

			response = requests.get('http://127.0.0.1:6767/face/suggest/?q=' + word)
			res = response.json()
			for place in res:
				if (word == place['phrase']):
					print place
					sys.exit(0)


