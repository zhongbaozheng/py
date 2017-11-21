# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy import Item, Field


class TweetsItem(Item):
    _id = Field()  # 微博id = user_id+tweets_id
    user_id = Field()  # 作者id
    content = Field()  # 内容
    clike = Field()  # 点赞数
    ccomment = Field()  # 评论数
    ctransfer = Field()  # 转发数
    pub_time = Field()  # 创建时间
    master_id = Field()  # 隶属id 如果是转发微博

    t = Field()

    # filter = 1  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
    # username = ''  # 用户名，如“Dear-迪丽热巴”
    # weibo_num = 0  # 用户全部微博数
    # weibo_num2 = 0  # 爬取到的微博数
    # following = 0  # 用户关注数
    # followers = 0  # 用户粉丝数
    # weibo_content = []  # 微博内容
    # publish_time = []  # 微博发布时间
    # up_num = []  # 微博对应的点赞数
    # retweet_num = []  # 微博对应的转发数
    # comment_num = []  # 微博对应的评论数


class WeiboItem(Item):
    filter = Field()
    username = Field()
    weibo_num = Field()
    following = Field()
    followers = Field()
    weibo_content = Field()
    publish_time = Field()
    up_num = Field()
    retweet_num = Field()
    comment_num = Field()



