from twitter import twitter
from news import link_crawler

t_c = twitter.Twitter()
# t_c.stream_location()

crawl = link_crawler.LinkCrawler()
crawl.start()
