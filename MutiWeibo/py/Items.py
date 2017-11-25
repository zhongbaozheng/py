#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class WeiboItem:
    # item['filter'],   0 表示所有微博 1表示原创微博
    # item['username'],  昵称
    # item['weibo_num'], 微博数
    # item['following'], 关注数
    # item['followers'],  粉丝数
    # item['weibo_content'], 微博内容
    # item['publish_time'],  发微博时间
    # item['up_num'],        点赞数
    # item['retweet_num'],   转发数
    # item['comment_num']    评论数

    def __init__(self,username,filter,weibo_num,followers,
                 following,weibo_content,publish_time,up_num,retweet_num,comment_num):
        self.weibo_num = weibo_num
        self.filter = filter
        self.username = username
        self.followers = followers
        self.following = following
        self.weibo_content = weibo_content
        self.publish_time = publish_time
        self.up_num = up_num
        self.retweet_num = retweet_num
        self.comment_num = comment_num






