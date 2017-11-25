#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#连接数据库、增删改查操作
import pymysql

from py.Items import WeiboItem

#MYSQL数据库存储
class WeiboHelper(object):

    # 初始化mysql
    def __init__(self):
        self.con = pymysql.connect(
            host="192.168.13.110",
            user="root",
            password="1213",
            db="py",
            charset="utf8mb4"
        )

        self.cus = self.con.cursor()

    #插入
    def insert_item(self, WeiboItem):

        sql = "insert into "+WeiboItem.username+"(username,filter,weibo_num,following," \
                                                "followers,weibo_content,publish_time," \
                                                "up_num,retweet_num,comment_num)"+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        print(sql)
        value = (
            WeiboItem.username,
            WeiboItem.filter,
            WeiboItem.weibo_num,
            WeiboItem.following,
            WeiboItem.followers,
            WeiboItem.weibo_content,
            WeiboItem.publish_time,
            WeiboItem.up_num,
            WeiboItem.retweet_num,
            WeiboItem.comment_num
        )

        try:
            self.cus.execute('create table if not exists ' + WeiboItem.username +"("
                                 +'id int primary key not null auto_increment,'
                                 + 'username' + ' varchar(256),'
                                 + 'filter' + ' varchar(256),'
                                 + 'weibo_num'+' varchar(256),'
                                 + 'following' + ' varchar(256),'
                                 + 'followers' + ' varchar(256),'
                                 +'weibo_content'+' text,'
                                 +'publish_time'+' varchar(256),'
                                 +'up_num'+' varchar(256),'
                                 +'retweet_num'+' varchar(256),'
                                 +'comment_num'+' varchar(256))')
            self.cus.execute(sql,value)
            self.con.commit()
        except Exception as e:
            print(e)
            self.con.rollback()

class ZhiLianHelper:
    pass

