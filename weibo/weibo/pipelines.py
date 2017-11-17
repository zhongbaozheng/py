# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import pymysql
from weibo.items import TweetsItem, CommentItem, UserItem

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


#数据库存储
class WeiboDataPipeline(object):

    # _id = Field()  # 微博id = user_id+tweets_id
    # user_id = Field()  # 作者id
    # content = Field()  # 内容
    # clike = Field()  # 点赞数
    # ccomment = Field()  # 评论数
    # ctransfer = Field()  # 转发数
    # pub_time = Field()  # 创建时间
    # master_id = Field()  # 隶属id 如果是转发微博
    #
    # t = Field()
    def process_item(self, item, spider):
        sql = None
        value=None
        if isinstance(item,TweetsItem):
            sql = "insert into Tweets values(0,%s,%s,%s,%s,%s,%s,%s,%s)"
            value = (
                item['user_id'],
                item['content'],
                item['clike'],
                item['gender'],
                item['ccomment'],
                item['ctransfer'],
                item['pub_time'],
                item['master_id']
            )
        elif isinstance(item,CommentItem):
            sql = "insert into Comments values(0,%s,%s,%s,%s,%s,%s,%s)"
            value = (
                item['_id'],
                item['author_id'],
                item['water_name'],
                item['master_id'],
                item['reply_nickname'],
                item['content'],
                item['clike']
            )
        elif isinstance(item, UserItem):
            sql = "insert into Users values(0,%s,%s,%s,%s,%s,%s)"
            value = (
                item['_id'],
                item['cfollows'],
                item['cfans'],
                item['ctweets'],
                item['auth'],
                item['intro']
            )

        try:
            cus.execute(sql,value)
            con.commit()
        except Exception as why:
            print(why)
            con.rollback()