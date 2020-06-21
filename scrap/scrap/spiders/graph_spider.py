# doing similar things to the imdb spider but saving a graph of the results 
# takes an input name in the same way and draws a graph around it 
# could store graph in a json file
# or as some object

# this whole thing is very messy and needs a lot of refactoring/rethinking 
import scrapy
from scrapy import signals 
from scrapy import Spider
from graph import Graph
import plot 
import re 

class GraphSpider(scrapy.Spider):
	name = "graph"
	query_limit = 200
	# starts off by searching for the actor given
	def start_requests(self):
		self.graph = Graph()
		yield scrapy.Request('http://m.imdb.com/find?q=%s+%s&ref_=nv_sr_sm' % (self.arg1, self.arg2))

	# creates the first node of the graph which is the actor given in the argument 
	def parse(self, response):
		# name_code is the url extension to imdb that brings up the actor's page 
		# this grabs the first name on the search page, which should be the actor we're looking for
		name_code = response.xpath('//a[contains(@href,"/name/nm")]/@href').get()
		# this should work but I don't think it's the best request to make 
		name = response.xpath('//div[@class="media-body media-vertical-align"]/span[@class="h3"]/text()').get()
		name = re.sub('\n', '', name)
		# this only contains the numerical part of the code but is still a string 
		# we could still keep the nm for clarity
		code = re.sub('name/', '', name_code.strip('/'))
		self.logger.info(code)
		self.logger.info(name)
		# start the graph by adding one empty actor to the actor dictionary 
		self.graph.new_actor(code, name)
		yield scrapy.Request('http://m.imdb.com%s' % name_code, callback=self.parse_actor, meta={'code':code})

	# takes an actor's page and scrapes the top films there 
	def parse_actor(self, response):
		if self.query_limit > 0:
			self.logger.info(response.css('title').get())
			# these refs work but I'm not sure they're optimal 
			title_codes = response.xpath('//div[@class="text-center filmo-caption"]/small[@class="ellipse"]/a[@href]/@href').getall()
			titles = response.xpath('//div[@class="text-center filmo-caption"]/small[@class="ellipse"]/a[@href]/text()').getall()
			# add titles to the dictionary here 
			# the number of titles per person should be variable, the user could input how many they want
			for i in range(0, 4):
				entry_code = re.sub('title/', '', title_codes[i].strip('/'))
				self.graph.add_film_to_actor(response.meta['code'], entry_code)
				# first need to check whether titles are already in the graph
				if self.graph.graph_contains(title_codes[i], False):
					pass
				else:
					self.graph.new_film(entry_code, titles[i])
					self.graph.add_actor_to_film(entry_code, response.meta['code'])
					self.query_limit -= 1
					yield scrapy.Request('http://m.imdb.com%s' % title_codes[i], callback=self.parse_film, meta={'code':entry_code})

	def parse_film(self, response):
		if self.query_limit > 0:
			self.logger.info(response.css('title').get())
			name_codes = response.xpath('//div[@class="ellipse"]/small/a/@href').getall()
			names = response.xpath('//div[@class="ellipse"]/small/a/strong/text()').getall()
			for i in range(0, 4):
				entry_code = re.sub('name/', '', name_codes[i].strip('/'))
				if not self.graph.graph_contains(name_codes[i], True):
					self.graph.new_actor(entry_code, names[i])
					self.graph.add_film_to_actor(entry_code, response.meta['code'])
					if not self.graph.film_contains(response.meta['code'], entry_code):
						self.graph.add_actor_to_film(response.meta['code'], entry_code)
					self.query_limit -= 1
					yield scrapy.Request('http://m.imdb.com%s' % name_codes[i], callback=self.parse_actor, meta={'code':entry_code})

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
		plot.plot_graph(self.graph)

# Should we allow for spelling errors or should we check for them? 
# at what point should we start implementing a GUI?
# the user should control how much the graph grows, 