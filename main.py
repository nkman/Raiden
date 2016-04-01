from twitter import twitter
from news import link_crawler, data_scraper
from news.topics import data as d

t_c = twitter.Twitter()
# t_c.stream_location()

crawl = link_crawler.LinkCrawler()
# crawl.start()

scrap = data_scraper.dataSaver()
# scrap.start()

tagging = d.dataHandler()
tagging.iterate_data()
