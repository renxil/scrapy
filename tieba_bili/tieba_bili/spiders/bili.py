# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tieba_bili.items import TiebaBiliItem

class BiliSpider(CrawlSpider):
    name = "bili"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = ['http://tieba.baidu.com/f?kw=bilibili&ie=utf-8&tab=good']
    #爬取规则,不带callback表示向该类url递归爬取
    rules = (
        #Rule(LinkExtractor(allow=('tab=good', ))),
        Rule(LinkExtractor(allow=('good', )), callback='parse_content'),
    )
    def parse_content(self, response):
        for sel in response.xpath('//*[@id="thread_list"]/li'):
            item = TiebaBiliItem()

            item['url'] = response.url
            item['title'] = sel.xpath('div/div[2]/div[1]/div[1]/a/text()').extract()
            item['link'] = sel.xpath('div/div[2]/div[1]/div[1]/a/@href').extract()
            item['desc'] = sel.xpath('div/div[2]/div[2]/div[1]/div[1]').extract()
            item['author'] = sel.xpath('div/div[2]/div[1]/div[2]/span[1]/span[1]/a/text()').extract()

            #self.log('xxxxxxxxxxx url: %s' % item['url'])
            #self.log('xxxxxxxxxxx title: %s' % item['title'])
            #self.log('xxxxxxxxxxx author: %s' % item['author'])
            #self.log('xxxxxxxxxxx link: %s' % item['link'])
            #self.log('xxxxxxxxxxx desc: %s' % item['desc'])
            yield item
