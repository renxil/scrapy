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
        Rule(LinkExtractor(allow=('', )), callback='parse_content'),
    )
    def parse_content(self, response):
        for sel in response.xpath('//ul/li'):
            self.log('Hi, this is an item page! %s' % response.url)
            item = TiebaBiliItem()
        #当前URL
        #print response.url
            item['url'] = response.url
        #title = response.selector.xpath("//div[@id='pagelet_frs-list/pagelet/thread_list']/ul/li/a[@class='j_th_tit']/@title").extract()
            self.log('xxxxxxxxxxx title: %s' % sel.xpath('div/div/div/div/a/@title').extract())

        #item['title'] = sel.xpath('div/div/div/div/a/@title').extract()
        #item['link'] = sel.xpath('div/div/div/div/a/@href').extract()
        #item['desc'] = sel.xpath('div/div/div/div/a/text()').extract()
        #item['author'] = sel.xpath('div/div/div/div/span/span/a/text()').extract()
            yield item
