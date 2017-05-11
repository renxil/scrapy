# -*- coding: utf-8 -*-
import scrapy
from tieba_bili.items import TiebaBiliItem

class BiliSpider(scrapy.Spider):
    name = "bili1"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = ['http://tieba.baidu.com/f?kw=bilibili&ie=utf-8&tab=good']
    #爬取规则,不带callback表示向该类url递归爬取
    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            self.log('Hi, this is an item page! %s' % response.url)
            item = TiebaBiliItem()
            #当前URL
            item['url'] = response.url
            item['title'] = sel.xpath('div/div/div/div/a/@title').extract()
            item['link'] = sel.xpath('div/div/div/div/a/@href').extract()
            item['desc'] = sel.xpath('div/div/div/div/a/text()').extract()
            item['author'] = sel.xpath('div/div/div/div/span/span/a/text()').extract()
            yield item
