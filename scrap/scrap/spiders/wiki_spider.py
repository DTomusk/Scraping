import scrapy 

class WikiSpider(scrapy.Spider):
	name = "wiki"
	allowed_domains = ['wikipedia.org']
	start_urls = [
		'https://www.wikipedia.org/',
	]

	# first off, print the title of every page linked to the homepage 
	def parse(self, response):
		self.logger.info('Spoderman')
		for href in response.css("a::attr(href)").getall():
			yield scrapy.Request("http://"+href.strip("u/"), callback=self.parse_title)

	def parse_title(self, response):
		self.logger.info(response.xpath("//title/text()"))


	# you can write new functions to parse pages one level down
	# that is, you can give links to parse and say that they should be parsed too 