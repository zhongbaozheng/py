# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_id = scrapy.Field() # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
    filter = scrapy.Field()  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
    username = scrapy.Field() # 用户名，如“Dear-迪丽热巴”
    weibo_num = scrapy.Field() # 用户全部微博数
    weibo_num2 = scrapy.Field() # 爬取到的微博数
    following = scrapy.Field() # 用户关注数
    followers = scrapy.Field() # 用户粉丝数
    weibo_content = scrapy.Field() # 微博内容
    publish_time = scrapy.Field()# 微博发布时间
    up_num = scrapy.Field()# 微博对应的点赞数
    retweet_num = scrapy.Field()# 微博对应的转发数
    comment_num = scrapy.Field()# 微博对应的评论数

