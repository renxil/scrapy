# -*- coding: utf-8 -*-
import scrapy


class BiliSpider(scrapy.Spider):
    name = "bili"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = ['http://tieba.baidu.com/']

    def parse(self, response):
        pass
