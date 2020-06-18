# scrape imdb to find connections between actors, go through most known for movies and highest billed cast
import scrapy 

class IMDBSpider(scrapy.Spider):
	name = "imdb"
	# start url is the first given actor

	def start_requests(self):
		self.logger.info('Trying')
		yield scrapy.Request('http://m.imdb.com/find?q=%s+%s&ref_=nv_sr_sm' % (self.arg1, self.arg2))

	def parse(self, response):
		name_code = response.xpath('//a[contains(@href,"/name/nm")]/@href').get()
		yield scrapy.Request('http://m.imdb.com%s' % name_code, callback=self.parse_actor)

	def parse_actor(self, response):
		self.logger.info(response.css('title').get())
