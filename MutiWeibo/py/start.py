#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#多线程和单线程的业务场景，当属于IO密集型的环境时，此时采用多线程就会快一点
# Python的threading模块有个current_thread()
# 函数，它永远返回当前线程的实例。主线程实例的名字叫MainThread，子线程的名字在创建时指定
import sys
import traceback

sys.path.append("..")
from py.weiboSpider import Weibo
import time
import threading


class SpiderControl:

    def simpleThread(self):
        self.simpleTest()

    def mutiThreads(self):
        self.mutiTest()

    def simpleTest(self):
        # 多个用户爬虫

        print("This is a simple thread.")
        s1 = time.time()
        print(time.time())

        bigV = [
            5548590926
            , 2410034191,1678105910
        ]

        try:
            for i in bigV:
                user_id = i
                self.run_thread(user_id)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

        print("时间为%s" % (time.time() - s1))

    def run_thread(self,user_id):

        try:
            wb = Weibo(user_id, 0)  # 调用Weibo类，创建微博实例wb
            wb.start()  # 爬取微博信息
            print(u"用户名：" + wb.username)
            print(u"全部微博数：" + str(wb.weibo_num))
            print(u"关注数：" + str(wb.following))
            print(u"粉丝数：" + str(wb.followers))
            print("爬虫结束")

        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()


    def mutiTest(self):

        print("This is a muti thread.")
        s1 = time.time()
        print(time.time())

        t1 = threading.Thread(target=self.run_thread,args=(5548590926,))   #需要加个，号
        t1.start()
        t2 = threading.Thread(target=self.run_thread, args=(2410034191,))
        t2.start()
        t3 = threading.Thread(target=self.run_thread, args=(1678105910,))
        t3.start()

        print("时间为%s" % (time.time() - s1))


if __name__ == "__main__":

    sipiderControl = SpiderControl()
    # sipiderControl.simpleThread()   #花了184秒
    sipiderControl.mutiThreads()     #花了112秒

    #目前还少了一个断点续爬和cookie池问题


