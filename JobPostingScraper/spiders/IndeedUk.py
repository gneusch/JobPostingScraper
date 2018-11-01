# -*- coding: utf-8 -*-
import scrapy


class IndeedukSpider(scrapy.Spider):
    name = 'IndeedUk'
    allowed_domains = ['https://www.indeed.co.uk/information-technology-jobs']
    start_urls = ['http://https://www.indeed.co.uk/information-technology-jobs/']

    def parse(self, response):
        pass
