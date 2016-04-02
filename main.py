from twitter import twitter
from news import link_crawler, data_scraper
from news.topics import data, corpus, train

t_c = twitter.Twitter()
# t_c.stream_location()

# crawl = link_crawler.LinkCrawler()
# crawl.start()

# scrap = data_scraper.dataSaver()
# scrap.start()

# tagging = data.dataHandler()
# tagging.iterate_data()

# corpus_c = corpus.corpusHandler()
# corpus_c.iterate_tags()
train.start_training()