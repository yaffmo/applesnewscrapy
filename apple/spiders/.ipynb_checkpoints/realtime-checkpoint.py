# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import  CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from apple.items import AppleItem

class RealtimeSpider(CrawlSpider):
    name = "realtime"
    start_urls = ['https://tw.appledaily.com/new/realtime/']
    rules = (Rule(LinkExtractor(allow=('new/realtime/1$'),),callback='parse_item',follow=True),)


    def parse_item(self, response):
        links = response.xpath('//*[@class="rtddd slvl"]//a//@href').extract()
        for link in links:
            yield scrapy.Request(link , callback = self.parse_detail)
    def parse_detail(self, response):
        appleitem = AppleItem()
        appleitem['title'] = response.xpath('//article//h1/text()').extract_first()
        appleitem['content'] = response.xpath('//*[@id="article"]//div//p//text()').extract_first()
        yield appleitem

