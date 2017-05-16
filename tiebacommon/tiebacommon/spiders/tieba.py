# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.sgml import SgmlLinkExtractor 
from scrapy.selector import HtmlXPathSelector
from tiebacommon.items import SubjectItem
from tiebacommon.items import CommentItem
from tiebacommon import settings
import scrapy
import json

class TiebaSpider(CrawlSpider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com'] #备注：那些带有推广的帖子现在看起来都不是这个域名下的，所以主题文章已经过滤了推广贴
    start_urls = [settings.START_URL]
    #这里假设20天内主题帖数量<1000*50,可以根据实际调整或获取页面上每个主题帖的时间来计算出具体需要多少页！
#    for x in range(0, 2):
#        start_urls.append(settings.START_URL + "&pn=" + str((x+1) * 50))
    #rules = [Rule(LinkExtractor(allow=['/p/\d+']), 'parse_subject_shanghai')]#这里只解析主题贴
    rules = [ 
        Rule(LinkExtractor(allow=['/p/\d+']), callback='parse_subject_shanghai')
   ] 
    
    
    def parse_subject_shanghai(self, response):
        try:
            torrent = SubjectItem()
            torrent['url'] = response.url
            torrent['id'] = response.url.split('/p')[1].split('/')[1].split('?')[0]
            torrent['commentNum'] = response.xpath("//*[@id='thread_theme_5']/div[1]/ul/li[2]/span[1]/text()").extract()[0]
            #这里用id定位没有找到content,一个可能原因是用了自定义tag cc
            torrent['content'] = response.xpath("//*/cc/div/text()").extract()[0]
            dataField = json.loads(str(response.xpath("//*[@id='j_p_postlist']/div[1]/@data-field").extract()[0]))
            #很多信息在html source里没有，是在客户端用 js 生成
            torrent['created'] = dataField['content']['date'].strip()+":00"
            torrent['title'] = response.xpath("//*[@id='j_core_title_wrap']/div/h1/text()").extract()[0]
            torrent['tiebaName'] = response.xpath("//*[@id='container']/div/div[1]/div[2]/div[2]/a/text()").extract()[0].strip()
            torrent['authorName'] = response.xpath("//*[@id='j_p_postlist']/div[1]/div[2]/ul/li[3]/a/text()").extract()[0]
            torrent['authorUrl'] = response.xpath("//*[@id='j_p_postlist']/div[1]/div[2]/ul/li[3]/a/@href").extract()[0]
            torrent['authorAvatar'] = response.xpath("//*[@id='j_p_postlist']/div[1]/div[2]/ul/li[1]/div/a/img/@src").extract()[0]
            print torrent
            if not "http://tieba.baidu.com" in torrent['authorUrl']:
                torrent['authorUrl'] = "http://tieba.baidu.com" + torrent['authorUrl']
            
            hxs = HtmlXPathSelector(response)
            subject_post_div = hxs.select("//*/cc/div")[0]
            imgs = ['','',''] 
            index = 1
            for img in subject_post_div.select(".//img/@src"):
                if index > 3:
                    break
                imgs[index-1] = img.extract()
                index += 1
            torrent['image1'],torrent['image2'],torrent['image3'] = imgs
            #到这里已经完成主题帖的解析
            
            totalCommentPage =  int(response.xpath("//div[@id='thread_theme_5']/div[1]/ul/li[2]/span[2]/text()").extract()[0])
            for x in range(2, totalCommentPage):
                if (x >4):
                    pass
                url = torrent['url'] + ("?pn=%s"  % x)
                yield scrapy.Request(url=url, callback=self.parse_comments_shanghai)
            
        except:
            torrent['id'] = None
            pass
        yield torrent
        
        
    def parse_comments_shanghai(self,response):
        try:
            items = []
            print response
            hxs = HtmlXPathSelector(response)
            print "---------------------------------------------------"
            #j_p_postlist = hxs.select("//div[@id='j_p_postlist']").select(".//div[@class='l_post l_post_bright ']")
            j_p_postlist = hxs.select("//div[@id='j_p_postlist']").select(".//div[@class='l_post j_l_post l_post_bright ']")
            print "----------------------------------------got it",j_p_postlist
            for childNode in j_p_postlist:
                print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                print childNode.extract()
            #for content in j_p_postlist.select(".//div[@id='l_post l_post_bright']/text()"):
                #print '=-===content',content
        except:
            for item in items:
                item['id'] = None
            pass
        return items
