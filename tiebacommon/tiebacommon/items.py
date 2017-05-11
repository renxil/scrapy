# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


    # define the fields for your item here like:
    # name = scrapy.Field()
class SubjectItem(scrapy.Item):  
    id = scrapy.Field()  
    url = scrapy.Field()  
    title = scrapy.Field()  
    tiebaName = scrapy.Field()  
    authorName = scrapy.Field()  
    authorUrl = scrapy.Field()  
    authorAvatar = scrapy.Field()  
    commentNum = scrapy.Field()  
    created = scrapy.Field()  
    content = scrapy.Field()  
    image1 = scrapy.Field()  
    image2 = scrapy.Field()  
    image3 = scrapy.Field()  
      
      
      
class CommentItem(scrapy.Item):  
    authorName = scrapy.Field()  
    authorUrl = scrapy.Field()  
    authorAvatar = scrapy.Field()  
    content = scrapy.Field()  
    index = scrapy.Field()  
    article_id = scrapy.Field()  
    created = scrapy.Field()  
