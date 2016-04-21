import requests as r
import rethinkdb as db
from bs4 import BeautifulSoup
from locations import cities
from datetime import datetime

base_url = 'http://trends24.in/india/'


class TrendMachine:

	def __init__(self):
		self.connection = None
		self.db_name = 'twitter'
		self.table_name = 'trends'

		self.create_storage()

	def collect_local_trends(self, city, time):
		"""
		Collect local Twitter trends information for a given location
		"""

		try:
			res = r.get("%s%s" % (base_url, city))
		except Exception, e:
			raise e

		# provides an object oriented way to iterate the HTML content
		parsed_res = BeautifulSoup(res.text)

		# select the first trend card among all available cards
		trend_cards = parsed_res.find_all('div', class_='trend-card')
		latest_trends = trend_cards[0].find_all('li')

		# data to be stored
		trend_data = {
			'place': city,
			'hour': time.strftime('%H'),
			'date': time.strftime('%b/%d/%Y')
		}

		for trend in latest_trends:
			trend_text, trend_link = trend.get_text(), trend.find('a')['href']

			try:
				trend_text = trend_text.encode('ascii', 'ignore')
				trend_data['text'], trend_data['link'] = trend_text, trend_link

				db.db(self.db_name).table(self.table_name).insert(trend_data).run(self.connection)
			except Exception, e:
				raise e

	def collect_trends(self):
		"""
		Initiate the process to collect the nationwide trends
		Enumerating over all the 'cities' defined in 'locations'
		"""

		# time when the collection has started
		time = datetime.now()

		for name, city in cities.iteritems():
			self.collect_local_trends(city, time)

	def create_storage(self):
		"""
		Create the database and table for the first time
		"""

		try:
			self.connection = db.connect()

			dbs = db.db_list().run(self.connection)
			if self.db_name not in dbs:
				db.db_create(self.db_name).run(self.connection)
				db.db(self.db_name).table_create(self.table_name).run(self.connection)

		except Exception, e:
			raise e

trend_machine = TrendMachine()
trend_machine.collect_trends()