# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item


class JobpostingscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobPosting(Item):
    crawling_date = scrapy.Field()
    posting_id = scrapy.Field()
    title_result_page = scrapy.Field()
    title_posting = scrapy.Field()
    company = scrapy.Field()
    company_rating_value = scrapy.Field()
    company_rating_count = scrapy.Field()
    job_description = scrapy.Field()
    posting_time = scrapy.Field()
    job_location = scrapy.Field()
