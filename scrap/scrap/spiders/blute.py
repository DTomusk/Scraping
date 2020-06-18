# -*- coding: utf-8 -*-
import scrapy


class BluteSpider(scrapy.Spider):
    name = 'blute'
    allowed_domains = ['https://en.m.wikipedia.org/wiki/Main_Page']
    start_urls = ['http://https://en.m.wikipedia.org/wiki/Main_Page/']

    def parse(self, response):
        pass
