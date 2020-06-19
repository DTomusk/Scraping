# scrape imdb to find connections between actors, go through most known for movies and highest billed cast
# could produce a graph of titles and actors 
import scrapy 

class IMDBSpider(scrapy.Spider):
	name = "imdb"
	# start url is the first given actor
	found = False

	def start_requests(self):
		self.logger.info('Trying')
		# need to put -a arg1 and -a arg2 in cli
		yield scrapy.Request('http://m.imdb.com/find?q=%s+%s&ref_=nv_sr_sm' % (self.arg1, self.arg2))

	# gets the target name code or says it can't be found
	#def get_end(self, response):


	def parse(self, response):
		name_code = response.xpath('//a[contains(@href,"/name/nm")]/@href').get()
		yield scrapy.Request('http://m.imdb.com%s' % name_code, callback=self.parse_actor)

	# want the children of the list inline containing films, take the most known films, go to their pages and get the top billed actors  
	def parse_actor(self, response):
		if not self.found:
			self.logger.info(response.css('title').get())
			title_codes = response.xpath('//a[contains(@href,"/title/tt")]/@href').getall()
			# we want the first couple of title codes on the person's page
			# title codes are repeated, so we want every other code 
			for i in range(0, 10, 2):
				yield scrapy.Request('http://m.imdb.com%s' % title_codes[i], callback=self.parse_film)

	def parse_film(self, response):
		# it will keep going even if arg3 arg4 doesn't exist 
		# using a wildcard might be inefficient 
		if response.xpath('//*[contains(strong, "%s %s")]' % (self.arg3, self.arg4)).getall():
			self.found = True
			self.logger.info("Found %s %s" % (self.arg3, self.arg4))
		else:
			self.logger.info(response.css('title').get())	
			name_codes = response.xpath('//a[contains(@href,"/name/nm")]/@href').getall()
			for i in range(0, 12, 2):
				yield scrapy.Request('http://m.imdb.com%s' % name_codes[i], callback=self.parse_actor)

# so far the input format is cumbersome
# no check to see whether we'd actually find a person with the given name 
# doesn't store the links leading up to the perosn 
# only checks the most popular films and top billed cast 
# should every request come with a route that's been taken so far? 
# and what about loops? I don't look at the first name in top billed cast but that doesn't make sense
# the person we're coming from won't necessarily be the top billed 
# the start person's name has to be similar enough but the end person's has to be exact 
# this will most likely get me banned from imdb 
# can start with a non actor but must end in an actor 

#