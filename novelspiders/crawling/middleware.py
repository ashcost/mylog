# -*- coding: utf-8 -*-
import random
from crawling.user_agents import mobile_agents
from crawling.user_agents import pc_agents


'''     
class CookiesMiddlewareStatic(object):
    def process_request(self, request, spider):
        cookie = random.choice(cookies)
        request.cookies = cookie
'''
class MobileUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(mobile_agents)
        request.headers["User-Agent"] = agent

class PcUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(pc_agents)
        request.headers["User-Agent"] = agent

class WeiboIndexAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(pc_agents)
        request.headers["User-Agent"] = agent
        request.headers["Referer"] = 'http://data.weibo.com/index/hotword'