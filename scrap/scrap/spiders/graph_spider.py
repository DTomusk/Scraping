# doing similar things to the imdb spider but saving a graph of the results 
# takes an input name in the same way and draws a graph around it 
# could store graph in a json file
# or as some object
import scrapy
from graph import Graph
import re 

class GraphSpider(scrapy.Spider):
	name = "graph"

	def start_requests(self):
		self.graph = Graph()
		yield scrapy.Request('http://m.imdb.com/find?q=%s+%s&ref_=nv_sr_sm' % (self.arg1, self.arg2))

	def parse(self, response):
		name_code = response.xpath('//a[contains(@href,"/name/nm")]/@href').get()
		# this only contains the numerical part of the code but is still a string 
		name_code = re.sub('name/nm', '', name_code.strip('/'))
		self.logger.info(name_code)
		# start the graph by adding one empty actor to the actor dictionary 
		self.graph.new_actor(name_code)
		self.graph.write_graph_to_file("my_graph.json")