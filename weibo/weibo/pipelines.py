# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import pymysql

from weibo.items import WeiboItem

con = pymysql.connect(
    host = "192.168.13.110",
    user = "root",
    password = "1213",
    db = "py",
    charset = "utf8mb4"
)

cus = con.cursor()


# #文本jison格式的存储
# class WeiboJsonPipeline(object):
#     def __init__(self):
#         self.file = codecs.open("star.json","w",encoding="utf-8")
#     #pipeline默认调用的方法
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item))+"\n"
#         self.file.write(line)
#         return item
#     def spider_closed(self):
#         self.file.close()


# filter = Field()
# username = Field()
# weibo_num = Field()
# following = Field()
# followers = Field()
# weibo_content = Field()
# publish_time = Field()
# up_num = Field()
# retweet_num = Field()
# comment_num = Field()


#MYSQL数据库存储
class WeiboDataPipeline(object):

    def process_item(self, item, spider):
        print("A")
        if isinstance(item,WeiboItem):
            print("B")
            sql = "insert into "+item['username']+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            value = (
                item['filter'],
                item['username'],
                item['weibo_num'],
                item['following'],
                item['followers'],
                item['weibo_content'],
                item['publish_time'],
                item['up_num'],
                item['retweet_num'],
                item['comment_num']
            )

        try:
            print("C")
            cus.execute("drop table if EXISTS "+item['username'])
            cus.execute('create table '+item['username']+
                        '个人信息(id int primary,'
                        +item['username']+' varchar(256),'
                        +item['filter']+' varchar(256),'
                        +item['following']+' varchar(256),'
                        +item['followers']+' varchar(256),'
                        +item['weibo_content']+' text,'
                        +item['publish_time']+' varchar(256),'
                        +item['up_num']+' varchar(256),'
                        +item['retweet_num']+' varchar(256),'
                        +item['comment_num']+' varchar(256))'")                                                                                            "")")
            cus.execute(sql,value)
            print("D")
            con.commit()
        except Exception as why:
            print(why)
            con.rollback()