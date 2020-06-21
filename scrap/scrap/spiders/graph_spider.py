# doing similar things to the imdb spider but saving a graph of the results 
# takes an input name in the same way and draws a graph around it 
# could store graph in a json file
# or as some object

# this whole thing is very messy and needs a lot of refactoring/rethinking 
import scrapy
from scrapy import signals 
from scrapy import Spider
from graph import Graph
import re 

class GraphSpider(scrapy.Spider):
	name = "graph"

	# starts off by searching for the actor given
	def start_requests(self):
		self.graph = Graph()
		yield scrapy.Request('http://m.imdb.com/find?q=%s+%s&ref_=nv_sr_sm' % (self.arg1, self.arg2))

	# creates the first node of the graph which is the actor given in the argument 
	def parse(self, response):
		# name_code is the url extension to imdb that brings up the actor's page 
		# this grabs the first name on the search page, which should be the actor we're looking for
		name_code = response.xpath('//a[contains(@href,"/name/nm")]/@href').get()
		# this only contains the numerical part of the code but is still a string 
		# we could still keep the nm for clarity
		code = re.sub('name/', '', name_code.strip('/'))
		self.logger.info(code)
		# start the graph by adding one empty actor to the actor dictionary 
		self.graph.new_actor(code)
		yield scrapy.Request('http://m.imdb.com%s' % name_code, callback=self.parse_actor, meta={'code':code})

	# takes an actor's page and scrapes the top films there 
	def parse_actor(self, response):
		self.logger.info(response.css('title').get())
		title_codes = response.xpath('//a[contains(@href,"/title/tt")]/@href').getall()
		# add titles to the dictionary here 
		for i in range(0, 10, 2):
			entry_code = re.sub('title/', '', title_codes[i].strip('/'))
			self.graph.add_film_to_actor(response.meta['code'], entry_code)
			# first need to check whether titles are already in the graph
			if self.graph.graph_contains(title_codes[i], False):
				pass
			else:
				self.graph.new_film(entry_code)
				self.graph.add_actor_to_film(entry_code, response.meta['code'])

				yield scrapy.Request('http://m.imdb.com%s' % title_codes[i], callback=self.parse_film, meta={'code':entry_code})

	def parse_film(self, response):
		self.logger.info(response.css('title').get())
		name_codes = response.xpath('//a[contains(@href,"/name/nm")]/@href').getall()
		for i in range(0, 12, 2):
			entry_code = re.sub('name/', '', name_codes[i].strip('/'))
			if not self.graph.graph_contains(name_codes[i], True):
				self.graph.new_actor(entry_code)
				self.graph.add_film_to_actor(entry_code, response.meta['code'])
				# this should only be called if that actor isn't already under the film
				# if not self.graph.film_contains(response.meta['code'], entry_code):
				if not self.graph.film_contains(response.meta['code'], entry_code):
					self.graph.add_actor_to_film(response.meta['code'], entry_code)

	# copied from documentation 
	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(GraphSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider

	# saves graph to file when spider closes 
	def spider_closed(self, spider):
		spider.logger.info('Spider closed')
		self.graph.write_graph_to_file("my_graph.json")

# Should we allow for spelling errors or should we check for them? 
# at what point should we start implementing a GUI?