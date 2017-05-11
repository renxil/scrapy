# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import settings
import traceback
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from datetime import datetime

def strtodatetime(datestr,format):      
    return datetime.strptime(datestr,format)  

class TiebacommonPipeline(object):
    def __init__(self):
        self.date_time_format = "%Y-%m-%d %H:%M:%S"
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                    host = settings.MySQL_SERVER,
                    db = settings.MySQL_SERVER_DB,
                    port = settings.MySQL_SERVER_PORT,
                    user = settings.MySQL_SERVER_USER,
                    passwd = settings.MySQL_SERVER_PWD,
                    cp_reconnect = True,
                    cursorclass = MySQLdb.cursors.DictCursor,
                    charset = 'utf8',
                    use_unicode = True) 

    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item).addErrback(self.handle_error)
        return item
    
    def _conditional_insert(self, tx, item):
            if item.get('id') and item.get('created'):
                today = datetime.now()
                postDay = strtodatetime(item.get('created'), self.date_time_format)
                #从这里限制只更新20天内的数据
                if (today - postDay).days <= int(settings.TOTAL_DAYS):
                    args= (item['id'],
                     item['title'],
                     item['url'],
                     item['tiebaName'],
                     item['authorName'],
                     item['authorUrl'],
                     item['authorAvatar'],
                     item['content'],
                     item['created'],
                     item['image1'],
                     item['image2'],
                     item['image3'],  
                     item['commentNum'],
                     item['commentNum']
                     )
                                    
                    sql = '''insert into tieba_articles(id, title, url, tiebaName, authorName, authorUrl, authorAvatar,content,created,image1,image2,image3,commentNum)  
                          VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s') ON DUPLICATE KEY UPDATE commentNum = '%s'
                          ''' % args
                
                    tx.execute(sql)
     
    def handle_error(self, e):
        log.err(e)    

