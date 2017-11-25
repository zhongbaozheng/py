#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#云计算运维的结果
import os
import random
import sys
import urllib.request
sys.path.append("..")
from lxml import etree

class Result:

    def __init__(self,location,position):
        self.location = location
        self.position = position

       #这里需要相关职位名称、反馈率、公司、工作地点、发布时间
    def requestZhiLian(self,page):
        headers = [
            "Mozilla/5.0 (Windows NT 6.1; Win64; rv:27.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:27.0) Gecko/20100101 Firfox/27.0"
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:10.0) Gecko/20100101 Firfox/10.0"
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/21.0.1180.110 Safari/537.36"
            "Mozilla/5.0 (X11; Ubuntu; Linux i686 rv:10.0) Gecko/20100101 Firfox/27.0"
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/34.0.1838.2 Safari/537.36"
            "Mozilla/5.0 (X11; Ubuntu; Linux i686 rv:27.0) Gecko/20100101 Firfox/27.0"
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            ]
        url ='http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%B9%BF%E5%B7%9E&kw=java%E5%B7%A5%E7%A8%8B%E5%B8%88&sm=0&p='+page
        print(url)
        # sys.exit()
        #url格式不能有中文，否则会报ASCII错误
        random_header = random.choice(headers)
        req = urllib.request.Request(url)
        req.add_header("User-Agent", random_header)
        req.add_header("Get", url)
        req.add_header("Host", "sou.zhaopin.com")
        req.add_header("refer", "http://sou.zhaopin.com/")
        html = urllib.request.urlopen(req)

        contents = html.read()
        # 判断输出内容contents是否是字节格式
        if isinstance(contents, bytes):
            # 转成字符串格式
            contents = contents.decode('utf-8')
        else:
            print('输出格式正确，可以直接输出')
        selector = etree.HTML(contents)
        #注意一个tobody，对于table标签的需要将把tobody去掉

        tableList = selector.xpath("//div[@class='newlist_list_content']/table")
        print(len(tableList))
        file_dir = os.path.split(os.path.realpath(__file__))[
                       0] + os.sep + "job"
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)
        file_path = file_dir + os.sep + "JAVA工程师" + ".txt"
        f = open(file_path, "ab")

        for i in range(len(tableList)):
            if i>1:
                positionName = selector.xpath("//div[@class='newlist_list_content']/table[%d]/tr/td[@class='zwmc']/div/a/text()"% i)
                fk = selector.xpath("//div[@class='newlist_list_content']/table[%d]/tr/td[@class='fk_lv']/span/text()"% i)
                if len(fk):
                    fk = fk[0]
                else: fk="无"
                companyName = selector.xpath(
                    "//div[@class='newlist_list_content']/table[%d]/tr/td[@class='gsmc']/a/text()" % i)[0]
                companyHref = selector.xpath(
                    "//div[@class='newlist_list_content']/table[%d]/tr/td[@class='gsmc']/a/@href" % i)[0]
                scenery = selector.xpath("//div[@class='newlist_list_content']/table[%d]/tr/td[@class='zwyx']/text()" % i)[0]
                location = selector.xpath("//div[@class='newlist_list_content']/table[%d]/tr/td[@class='gzdd']/text()" % i)[0]
                issureDate = selector.xpath("//div[@class='newlist_list_content']/table[%d]/tr/td[@class='gxsj']/span/text()" % i)[0]

                print(positionName)      #职位名称
                print(fk)                #反馈率
                print(companyName)       #公司名称
                print(companyHref)       #公司简介链接
                print(scenery)           #薪酬
                print(location)          #工作地点
                print(issureDate)        #发布日期
                print('\n')
                f.write(("职位名称："+str(positionName)+"\n反馈率："+fk+"\n"
                        +"公司名称："+companyName+"\n"
                        +"公司链接："+companyHref+"\n"
                        +"薪酬："+scenery+"月\n"
                        +"工作地点："+location+"\n"
                        +"发布日期："+issureDate+"\n\n").encode(sys.stdout.encoding))
        f.close()


        print("输出完毕")



if __name__ == "__main__":

    try:

        result = Result('广州',"java工程师")
        i = 1
        for i in range(40):
            result.requestZhiLian(str(i))
            print(str(i))

    except Exception as e:
        print(e)
        print("查询职位失败！")
