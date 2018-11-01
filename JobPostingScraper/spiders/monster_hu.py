import scrapy
import json

class MonsterHuSpider(scrapy.Spider):
    name = 'monster_hu_spider'

    start_urls =  ['https://www.monster.hu/allas/q-it-allas.aspx?jobid=198066030&stpage=1&page=1']

    def parse(self, response):
        for href in response.css('#SearchResults section.card-content h2.title a::attr(href)'):
            yield response.follow(href, self.parse_jobad)

        for href in response.css('#SearchResults + a.btn-secondary::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_jobad(self, response):
        data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())      
        yield data
