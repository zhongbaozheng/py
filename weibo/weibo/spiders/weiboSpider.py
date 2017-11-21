#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import random
import re
import time
import json
import traceback
from datetime import datetime, timedelta

import requests
import sys
from lxml import etree
from scrapy.spiders import CrawlSpider
from weibo.cookies_phone import cookies
from weibo.items import WeiboItem
from ..settings import bigV

def get_rnd_cookie():
	return random.choice(cookies)

class Spider(CrawlSpider):
    name = "weibo"
    allowed_domains = "http://weibo.cn"
    start_user_id = bigV
    scrawl_ID = set(start_user_id)  # 记录待爬的用户ID
    # start_urls = []
    # 验证登录写在start_requests()方法中，传递cookie参数。
    #也就是说实现cookie有两种方式，
    # 一种是
    # cookie = {"Cookie":
    #               "_T_WM=de9191e67236e734f5e5c5e988f47459; __guid=78840338.4269890070892027000.1511141916625.0662; SUB=_2A253F_ldDeThGeNH7FYS-SrOzDqIHXVU-4cVrDV6PUJbkdBeLUmnkW1NSpwp8hfcfqQfmbXIHV-I0kd9E5Rhwdop; SUHB=0nl-AefZ4pBEKa; SCF=AnnhwvV-vOOSwofU2YKrdCrjdEwgSKK262xLxJEntvIVN5o3R1Sd4e1zWA0IhuHm_U2DIIRlqB8CR-n7MZkJl_Y.; SSOLoginState=1511229709; _T_WL=1; _WEIBO_UID=5974394276; monitor_count=15"}
    # url = "https://weibo.cn/%d/info" % (self.user_id)
    # html = requests.get(url, cookies=self.cookie).content
    #另一种是scrapy的做法，
    #cookie的写法json格式的写法
    #然后在验证登录写在start_requests()方法中，传递cookie参数。
    # http://www.jianshu.com/p/887af1ab4200
    cookie = {"Cookie":
                  "_T_WM=de9191e67236e734f5e5c5e988f47459; __guid=78840338.4269890070892027000.1511141916625.0662; SUB=_2A253F_ldDeThGeNH7FYS-SrOzDqIHXVU-4cVrDV6PUJbkdBeLUmnkW1NSpwp8hfcfqQfmbXIHV-I0kd9E5Rhwdop; SUHB=0nl-AefZ4pBEKa; SCF=AnnhwvV-vOOSwofU2YKrdCrjdEwgSKK262xLxJEntvIVN5o3R1Sd4e1zWA0IhuHm_U2DIIRlqB8CR-n7MZkJl_Y.; SSOLoginState=1511229709; _T_WL=1; _WEIBO_UID=5974394276; monitor_count=15"}

    filter = 1  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
    username = ''  # 用户名，如“Dear-迪丽热巴”
    weibo_num = 0  # 用户全部微博数
    weibo_num2 = 0  # 爬取到的微博数
    following = 0  # 用户关注数
    followers = 0  # 用户粉丝数
    weibo_content = []  # 微博内容
    publish_time = []  # 微博发布时间
    up_num = []  # 微博对应的点赞数
    retweet_num = []  # 微博对应的转发数
    comment_num = []  # 微博对应的评论数

    # while start_urls.__len__():
    #     user_id = (int)(scrawl_ID.pop())
    #     start_urls.append()


    def start_requests(self):
        while self.scrawl_ID.__len__():
            self.user_id = self.scrawl_ID.pop()
            self.user_id = int(self.user_id)
            print("get_rnd_cookie=%s" % get_rnd_cookie())
            print("mine cookies=%s" % self.cookie)
            self.get_username()
            # self.get_user_info()
            # self.get_weibo_info()
            # self.write_txt()


    # def parse(self, response):
    #     while self.scrawl_ID.__len__():
    #         self.user_id = self.scrawl_ID.pop()
    #         self.user_id = int(self.user_id)
    #         print("get_rnd_cookie=%s" % get_rnd_cookie())
    #         print("mine cookies=%s" % self.cookie)
    #         self.get_username()
    #         self.get_user_info()
    #         self.get_weibo_info()
    #         self.write_txt()

    # 获取用户昵称
    def get_username(self):
        try:
            url = "https://weibo.cn/%d/info" % (self.user_id)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            username = selector.xpath("//title/text()")[0]
            print("username=%s" % username)
            self.username = username[:-3]
            print(u"用户名: " + self.username)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取用户微博数、关注数、粉丝数
    def get_user_info(self):
        try:
            # https: // weibo.com / p / 1004061195242865 / home?from=page_100406_profile & wvr = 6 & mod = data & is_all = 1  # place
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            print("utl=%s" % url)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            pattern = r"\d+\.?\d*"

            # 微博数
            str_wb = selector.xpath(
                "//div[@class='tip2']/span[@class='tc']/text()")[0]
            print("str_wb = %s" % str_wb)
            guid = re.findall(pattern, str_wb, re.S | re.M)
            for value in guid:
                num_wb = int(value)
                break
            self.weibo_num = num_wb
            print(u"微博数: " + str(self.weibo_num))

            # 关注数
            str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
            guid = re.findall(pattern, str_gz, re.M)
            self.following = int(guid[0])
            print(u"关注数: " + str(self.following))

            # 粉丝数

            str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
            guid = re.findall(pattern, str_fs, re.M)
            self.followers = int(guid[0])
            print(u"粉丝数: " + str(self.followers))

        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取用户微博内容及对应的发布时间、点赞数、转发数、评论数
    def get_weibo_info(self):
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            if selector.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(selector.xpath(
                    "//input[@name='mp']")[0].attrib["value"])
            pattern = r"\d+\.?\d*"
            for page in range(1, page_num + 1):
                url2 = "https://weibo.cn/u/%d?filter=%d&page=%d" % (
                    self.user_id, self.filter, page)
                html2 = requests.get(url2, cookies=self.cookie).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                if len(info) > 3:
                    for i in range(0, len(info) - 2):
                        # 微博内容
                        str_t = info[i].xpath("div/span[@class='ctt']")
                        weibo_content = str_t[0].xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        self.weibo_content.append(weibo_content)
                        print(u"微博内容：" + weibo_content)

                        # 微博发布时间
                        str_time = info[i].xpath("div/span[@class='ct']")
                        str_time = str_time[0].xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        publish_time = str_time.split(u'来自')[0]
                        if u"刚刚" in publish_time:
                            publish_time = datetime.now().strftime(
                                '%Y-%m-%d %H:%M')
                        elif u"分钟" in publish_time:
                            minute = publish_time[:publish_time.find(u"分钟")]
                            minute = timedelta(minutes=int(minute))
                            publish_time = (
                                datetime.now() - minute).strftime(
                                "%Y-%m-%d %H:%M")
                        elif u"今天" in publish_time:
                            today = datetime.now().strftime("%Y-%m-%d")
                            time = publish_time[3:]
                            publish_time = today + " " + time
                        elif u"月" in publish_time:
                            year = datetime.now().strftime("%Y")
                            month = publish_time[0:2]
                            day = publish_time[3:5]
                            time = publish_time[7:12]
                            publish_time = (
                                year + "-" + month + "-" + day + " " + time)
                        else:
                            publish_time = publish_time[:16]
                        self.publish_time.append(publish_time)
                        print(u"微博发布时间：" + publish_time)

                        # 点赞数
                        str_zan = info[i].xpath("div/a/text()")[-4]
                        guid = re.findall(pattern, str_zan, re.M)
                        up_num = int(guid[0])
                        self.up_num.append(up_num)
                        print(u"点赞数: " + str(up_num))

                        # 转发数
                        retweet = info[i].xpath("div/a/text()")[-3]
                        guid = re.findall(pattern, retweet, re.M)
                        retweet_num = int(guid[0])
                        self.retweet_num.append(retweet_num)
                        print(u"转发数: " + str(retweet_num))

                        # 评论数
                        comment = info[i].xpath("div/a/text()")[-2]
                        guid = re.findall(pattern, comment, re.M)
                        comment_num = int(guid[0])
                        self.comment_num.append(comment_num)
                        print(u"评论数: " + str(comment_num))

                        self.weibo_num2 += 1

            if not self.filter:
                print(u"共" + str(self.weibo_num2) + u"条微博")
            else:
                print(u"共" + str(self.weibo_num) + u"条微博，其中" +
                      str(self.weibo_num2) + u"条为原创微博"
                      )
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 将爬取的信息写入文件和数据库
    def write_txt(self):
        try:
            file_dir = os.path.split(os.path.realpath(__file__))[
                           0] + os.sep + "weibo"
            if not os.path.isdir(file_dir):
                os.mkdir(file_dir)
            file_path = file_dir + os.sep + "%d" % self.user_id + ".txt"
            f = open(file_path, "wb")

            if self.filter:
                result_header = u"\n\n原创微博内容：\n"
            else:
                result_header = u"\n\n微博内容：\n"
            result = (u"用户信息\n用户昵称：" + self.username +
                      u"\n用户id：" + str(self.user_id) +
                      u"\n微博数：" + str(self.weibo_num) +
                      u"\n关注数：" + str(self.following) +
                      u"\n粉丝数：" + str(self.followers) +
                      result_header
                      )
            f.write(result.encode(sys.stdout.encoding))
            for i in range(1, self.weibo_num2 + 1):
                text = (str(i) + ":" + self.weibo_content[i - 1] + "\n" +
                        u"发布时间：" + self.publish_time[i - 1] + "\n" +
                        u"点赞数：" + str(self.up_num[i - 1]) +
                        u"	 转发数：" + str(self.retweet_num[i - 1]) +
                        u"	 评论数：" + str(self.comment_num[i - 1]) + "\n\n"
                        )
                item = WeiboItem()
                item['username'] = self.username
                item['weibo_num'] = self.weibo_num
                item['following'] = self.following
                item['followers'] = self.followers
                item['up_num'] = str(self.up_num[i-1])
                item['retweet_num'] = str(self.retweet_num[i - 1])
                item['comment_num'] = str(self.comment_num[i - 1])
                item['weibo_content'] = result
                # yield item

                f.write(text.encode(sys.stdout.encoding))
            # result = result + text
            # file_dir = os.path.split(os.path.realpath(__file__))[
            #     0] + os.sep + "weibo"
            # if not os.path.isdir(file_dir):
            #     os.mkdir(file_dir)
            # file_path = file_dir + os.sep + "%d" % self.user_id + ".txt"
            # f = open(file_path, "wb")
            # f.write(result.encode(sys.stdout.encoding))
            f.close()
            print(u"微博写入文件完毕，保存路径:" + file_path)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()


    # 获取用户昵称
    def get_username(self):
        try:
            url = "https://weibo.cn/%d/info" % (self.user_id)
            html = requests.get(url, cookies=self.cookie).content
            print(html)
            selector = etree.HTML(html)
            username = selector.xpath("//title/text()")[0]
            self.username = username[:-3]
            print(u"用户名: " + self.username)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()


