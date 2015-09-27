import requests
import xmltodict
import rethinkdb as r

TRENDING_URL = 'http://www.google.co.in/trends/hottrends/atom/feed?pn=p3'

#r.connect('localhost', 28015).repl()
#r.use('raiden')

# create table 'trending' if it's not present
try:
	#r.db('raiden').table_create('trending').run()
	print 'Created table [raiden.trending]'
except Exception, e:
	pass

try:
	trending_xml_res = requests.get(TRENDING_URL)
	trending_xml_txt = trending_xml_res.text
	trending_xml = xmltodict.parse(trending_xml_txt)
except Exception, e:
	raise e

for trending_item in trending_xml['rss']['channel']['item']:
	print "\n"*2

	# skips languages other than English
	try:
		trending_item['title'].decode('ascii')
	except Exception, UnicodeDecodeError:
		continue

	trending_data = {
		'title': trending_item['title'],
		'timestamp': trending_item['pubDate'],
		'traffic': trending_item['ht:approx_traffic'],
		'image': trending_item['ht:picture']
	}

	print trending_item['title']
	for trending_news_item in trending_item['ht:news_item']:
		print trending_news_item
