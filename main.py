from twitter import twitter
from news import link_crawler, data_scraper
from news.topics import data, corpus, train, predict

# t_c = twitter.Twitter()
# t_c.stream_location()

crawl = link_crawler.start_parallel()
crawl.start_link()

# scrap = data_scraper.ParallelScraping()
# scrap.multi_threads()

# tagging = data.Start()
# tagging.start_tagging()

# corpus_c = corpus.corpusHandler()
# corpus_c.iterate_tags()

# train.start_training()

# dbh = predict.dataDBHandler()
# dbh.iterate_text()
