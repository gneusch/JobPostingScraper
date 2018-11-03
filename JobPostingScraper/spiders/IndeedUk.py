# -*- coding: utf-8 -*-
import datetime
import json
import scrapy
import urlparse
from JobPostingScraper.items import JobPosting

class IndeedukSpider(scrapy.Spider):
    name = 'IndeedUk'
    date = datetime.datetime.now()
    
    #start_urls = ['https://www.indeed.co.uk/information-technology-jobs']
    #start_urls = ['https://www.indeed.co.uk/jobs?q=information+technology&fromage=last']
    start_urls = ['https://www.indeed.co.uk/jobs?q=information+technology&sort=date']

    custom_settings = {
        'LOG_FILE': 'log/' + date.strftime('%Y') + '-' + date.strftime('%m') + '-' + date.strftime('%d') + '-' + date.strftime('%H') + '-' + date.strftime('%M') + '-' + date.strftime('%S') + '-' + 'IndeedUk.txt',
    }

    def parse(self, response):

        titlesResultPage = response.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " result ")]//a[contains(@data-tn-element,"jobTitle")]/@title').extract()
        i = 0
        for jobId in response.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " result ")]/@data-jk').extract():
            jobPosting = JobPosting()
            jobPosting['crawling_date'] = IndeedukSpider.date.strftime('%Y') + '-' + IndeedukSpider.date.strftime('%m') + '-' + IndeedukSpider.date.strftime('%d')
            jobPosting['posting_id'] = jobId
            jobPosting['title_result_page'] = titlesResultPage[i]
            i += 1 
            jobUrl = urlparse.urljoin(response.url, 'viewjob?jk=' + jobId)
            yield scrapy.Request(jobUrl, callback=self.parse_jobad, meta={'job_posting': jobPosting})

        for nextPage in response.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " pagination ")]/a[./span[contains(concat(" ", normalize-space(@class), " "), " pn ")]/span[contains(concat(" ", normalize-space(@class), " "), " np ")]]/@href').extract():
            yield response.follow(urlparse.urljoin(response.url, nextPage), self.parse)

    def parse_jobad(self, response):

        jobPosting = response.meta.get('job_posting')
        jobComponent = response.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " jobsearch-JobComponent ")]') 
        firstdiv = jobComponent.xpath('.//div[1]') 
        jobPosting['title_posting'] = firstdiv.xpath('.//h3[contains(concat(" ", normalize-space(@class), " "), " jobsearch-JobInfoHeader-title ")]/text()').extract_first(default='N/A')
        jobPosting['company'] = firstdiv.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " jobsearch-InlineCompanyRating ")]/div[1]/text()').extract_first(default='N/A') 
        jobPosting['job_description'] = jobComponent.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " jobsearch-JobComponent-description ")]/node()').extract() #have to be handled as an array - with extract_first() we can lose information
        jobPosting['posting_time'] = jobComponent.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " jobsearch-JobMetadataFooter ")]/text()').extract_first(default='N/A') 

        if firstdiv.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " jobsearch-InlineCompanyRating ")]/div[2]/text()').extract_first() is not None and firstdiv.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " jobsearch-InlineCompanyRating ")]/div[2]/text()').extract_first().strip() == '-':
            jobPosting['job_location'] = firstdiv.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " jobsearch-InlineCompanyRating ")]/div[3]/text()').extract_first(default='N/A')
            jobPosting['company_rating_value'] = 'N/A'
            jobPosting['company_rating_count'] = 'N/A'
        else: 
            jobPosting['job_location'] = firstdiv.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " jobsearch-InlineCompanyRating ")]/div[4]/text()').extract_first(default='N/A')
            jobPosting['company_rating_value'] = firstdiv.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " icl-Ratings ")]/meta[@itemprop="ratingValue"]/@content').extract_first(default='N/A')
            jobPosting['company_rating_count'] = firstdiv.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " icl-Ratings ")]/meta[@itemprop="ratingCount"]/@content').extract_first(default='N/A')


        yield jobPosting

