# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

# json格式
import MySQLdb
from twisted.enterprise import adbapi


class WeiboJsonPipeline(object):
    def __init__(self):
        self.file = codecs.open("star.json","w",encoding="utf-8")
    #pipeline默认调用的方法
    def process_item(self, item, spider):
        line = json.dumps(dict(item))+"\n"
        self.file.write(line)
        return item
    def spider_closed(self):
        self.file.close()



#数据库存储
class WeiboDataPipeline(object):

    #初始化
    def __init__(self,dbpool):
        self.dbpool = dbpool
        self.dbpool = adbapi.ConnectionPool(
            'MySQLdb',
            host='192.168.13.107',
            db='crawlpicturesdb',
            user='root',
            passwd='1213',
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',
            use_unicode=False
        )
    # 静态的方法
    @classmethod
    def from_settings(cls,settings):

        dbparams=dict(
            host = settings["MYSQL_HOST"],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,

        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparams)
        return cls(dbpool)

    # pipeline默认调用的方法
    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.__conditonal_insert,item)
        query.addErrback(self._handle_error,item,spider)
        return item


    # 插入数据，私有化
    def __conditonal_insert(self,tx,item):

        sql = "insert into %s(......) values(%s,%s....)"
        params = (item["x"],item["y"])
        tx.execute(sql,params)

    #错误处理
    def _handle_error(self,failure,item,spider):
        print("-----database operate exception------")
        print("-------------------------------------")
        print(failure)
