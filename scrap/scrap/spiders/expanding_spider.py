import scrapy 
import os.path
import os 
import re
import plot
from graph import Graph
from scrapy import signals
from scrapy import Spider

# this spider looks at one film or person at a time, it can be called multiple times to grow the graph
class GrowSpider(scrapy.Spider):
	name = "grow"
	a_file = "actor_database.json"
	f_file = "film_database.json"

	def start_requests(self):
		# option for starting afresh  
		if self.arg2 == "n":
			os.remove(self.a_file)
			os.remove(self.f_file)
		if os.path.isfile(self.a_file):
			self.graph = Graph.load_graph(self.a_file, self.f_file)
			if self.arg2 == "a":
				# check that actor exists and go to parse actor 
				try:
					print(self.arg1)
				 	extension = self.graph.contains_name(self.arg1, True)
				 	print(extension)
					yield scrapy.Request('http://m.imdb.com/name/%s' % extension, callback=self.parse_actor, meta={'code':extension})
				except Exception as e:
				 	self.logger.error("Couldn't find actor")
			elif self.arg2 == "f":
				try:
				 	extension = self.graph.contains_name(self.arg1, False)
					yield scrapy.Request('http://m.imdb.com/title/%s' % extension, callback=self.parse_film, meta={'code':extension})
				except Exception as e:
				 	self.logger.error("Couldn't find film")
			else:
				self.logger.error("Invalid arg2 option, must be a or f")
		else:
			# creates a new graph and parses the first actor 
			self.graph = Graph()
			query = re.sub(' ', '+', self.arg1)
			yield scrapy.Request('http://m.imdb.com/find?q=%s&ref_=nv_sr_sm' % self.arg1)

	# parse is the initial step, it searches for the first actor and yields their page 
	def parse(self, response):
		name_extension = response.xpath('//a[contains(@href,"/name/nm")]/@href').get()
		name = re.sub('\n', '', response.xpath('//div[@class="media-body media-vertical-align"]/span[@class="h3"]/text()').get())
		code = re.sub('name/', '', name_extension.strip('/'))
		self.graph.new_actor(code, name)
		yield scrapy.Request('http://m.imdb.com%s' % name_extension, callback=self.parse_actor, meta={'code':code})

	# parses the page for a given actor by adding their top movies to their entry and adding them to the entry of the movie 
	def parse_actor(self, response):
		# extensions are what's added to the url to get a certain film
		name_code = response.meta['code']
		title_extensions = response.xpath('//div[@class="text-center filmo-caption"]/small[@class="ellipse"]/a[@href]/@href').getall()
		titles = response.xpath('//div[@class="text-center filmo-caption"]/small[@class="ellipse"]/a[@href]/text()').getall()

		for i, title_extension in enumerate(title_extensions):
			title_code = re.sub('title/', '', title_extension.strip('/'))
			title = re.sub('\n', '', titles[i].strip())
			if not self.graph.contains_code(title_code, False):
				self.graph.new_film(title_code, title)
			if not self.graph.actor_contains(name_code, title_code):
				self.graph.add_film_to_actor(name_code, title_code)
			if not self.graph.film_contains(title_code, name_code):
				self.graph.add_actor_to_film(title_code, name_code)
			
	# parse actor and parse film behave pretty much identically, they just have different requests 
	# ideally the two could be refactored down to one function 
	def parse_film(self, response):
		title_code = response.meta['code']
		name_extensions = response.xpath('//div[@class="ellipse"]/small/a/@href').getall()
		names = response.xpath('//div[@class="ellipse"]/small/a/strong/text()').getall()

		for i, name_extension in enumerate(name_extensions):
			name_code = re.sub('name/', '', name_extension.strip('/'))
			name = re.sub('\n', '', names[i].strip())
			if not self.graph.contains_code(name_code, True):
				self.graph.new_actor(name_code, name)
			if not self.graph.actor_contains(name_code, title_code):
				self.graph.add_film_to_actor(name_code, title_code)
			if not self.graph.film_contains(title_code, name_code):
				self.graph.add_actor_to_film(title_code, name_code)

	# copied from documentation 
	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(GrowSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider

	# saves graph to file when spider closes 
	def spider_closed(self, spider):
		spider.logger.info('Spider closed')
		self.graph.write_graph_to_file(self.a_file, self.f_file)
		plot.plot_graph(self.graph)


# the graph could scale nodes in terms of popularity, both for films and actors 
# need to create a user interface that calls these methods so the user doesn't have to all the time
# CLI takes two arguments for names and title even though lots of names and titles have more than two words
# CLI should take one argument and break it up accoridingly if need be 