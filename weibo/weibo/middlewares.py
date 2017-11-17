# -*- coding: utf-8 -*-

import random

import json

from weibo.cookies_phone import cookies
from weibo.user_agents import agents


class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        print ('-----------------------')
        request.headers['User-Agent']=random.choice(agents)

class CookiesMiddleware(object):
    def process_request(self, request, spider):
        print ('-----------------------')
        cookie = json.loads(random.choice(cookies))
        request.cookies = cookie
        print (cookie)
