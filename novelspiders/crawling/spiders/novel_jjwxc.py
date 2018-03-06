# -*- coding: utf-8 -*-
import re
from crawling.items import SpiderNovelItem
import time
import sys
import json
import scrapy
import crawling.spiders.fileloader
import logging


class HxtxSpider(scrapy.Spider):
    name = "jjwxc"
    # download_delay = 1
    start_urls = [
         
        'http://app.jjwxc.org/search/getSearchForKeyWords?offset=0&limit=20&bq=0&fw=0&yc=0&xx=0&sd=0&lx=0&fg=0&mainview=0&fbsj=0&isfinish=0&sortType=0']
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":{
            # 'crawling.middleware.CookiesMiddleware' :400,
            'crawling.middleware.PcUserAgentMiddleware' :401,
        },
        "REFERER_ENABLED":False,
        "DOWNLOAD_DELAY" : 0.25
    }
    def parse(self, response): 
        try:
            if re.search('offset=0&',response.url):
                for page in range(1,1000):
                    offset = page* 20
                    next_page = re.sub('offset=0&','offset=%d&' %offset,response.url)
                    request = scrapy.Request(next_page,callback = self.parse)
                    request.meta['priority'] = -10
                    yield request
            items =  json.loads(response.body)
            for item in items['items']:
                request = scrapy.Request('http://app.jjwxc.org/androidapi/novelbasicinfo?novelId=%s'% item['novelid'], callback=self.book_details)
                request.meta['priority'] = 0
                yield request
        except Exception as e:
            logging.error(e)

    def book_details(self, response):
        try:
            novel = json.loads(response.body)
            item = {}
            item['spiderid'] = 'jjwxc'
            #item['spiderid'] = response.meta['spiderid']
           # item['url'] = response.url
            item['name'] = novel['novelName']
            item['url'] = 'http://www.jjwxc.net/onebook.php?novelid=%s' %novel['novelId']
            item['author'] =  novel['authorName']
            item['category'] = novel['novelClass']
            item['description'] =  novel['novelIntro']
            item['yuepiao'] = 0
            item['shoucang'] = 0
            item['hongbao'] = 0
            item['biaoqian'] = novel['novelTags']
            item['haopingzhishu'] = '0.0'
            item['total_recommend'] = 0
            item['review_count'] = 0
            item['printmark'] = 0
            item['status'] = ''
           
            item['points'] = self.parse2Int(novel['novelScore'])
            item['comment_count'] =  self.parse2Int(novel['comment_count'])
            item['shoucang'] = self.parse2Int(novel['novelbefavoritedcount'])
            item['word_count'] = self.parse2Int(novel['novelSize'])
            item['lastupdate'] = novel['renewDate']
            item['image'] = novel['novelCover']
            item['current_date'] = time.strftime(
                '%Y-%m-%d', time.localtime(time.time()))
            item['site'] = "jjwxc"
            item['redpack'] = 0
            item['yuepiaoorder'] = 0
            item['flower'] = 0
            item['diamondnum'] = 0
            item['coffeenum'] = 0
            item['eggnum'] = 0
            item['redpackorder'] = 0
            item['totalrenqi'] = 0
            item['vipvote'] = 0
            item['isvip'] = novel['isVip']
            item['banquan'] = '未签约' if novel['novelStep'] == 2 else '已签约'
            item['page_view'] = self.parse2Int(novel['novip_clicks'])
            
            yield item
        except Exception as e:
            logging.error('2'*100)
            logging.error("Pase error: {}".format(e))

    def parse2Int(self,str):
        if str is None or str == '':
            return 0
        str = str.replace(',','')
        return int(str)