# -*- coding: utf-8 -*-
import time

from crawling.items import SpiderNovelItem
# from redis_spider import scrapy.Spider
import re
import sys
import json
import scrapy
import crawling.spiders.fileloader
# reload(sys)
# sys.setdefaultencoding('utf-8')


class ChuangshiSpider(scrapy.Spider):
    name = "chuangshi_yunqi"
    # download_delay = 5
    start_urls = ['http://chuangshi.qq.com/bk/so4/p/1.html', 'http://yunqi.qq.com/bk/so12/n10p1']
        # 'http://chuangshi.qq.com/bk/so4/p/1.html']
    # , 'http://yunqi.qq.com/bk/so12/n10p1'
    custom_settings = {
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True,
        "REFERER_ENABLED": True,
        "DEFAULT_REQUEST_HEADERS" : {
            'Referer': 'http://chuangshi.qq.com'

        }
    }

    def parse(self, response):
        '''
        try:
            self._logger.debug("crawled url {}".format(response.request.url))
            urls = fileloader.loadurls()
            for url in urls:
                request = scrapy.Request(url, callback=self.parse_item,priority = 2)
                yield request 
        except Exception as e:
            self._logger.error(e.message)
        '''
        if re.search('yunqi\.qq\.com\/bk\/so12\/n10p1$',response.url):
            for i in range(2,5000):
            # for i in range(2, 4):
                url = re.sub('n10p1','n10p%d' %i,response.url)
                request =  scrapy.Request(url, callback=self.parse,priority = 100)
                request.meta['priority'] = -10
                request.meta['retry_times'] = 3
                yield request
        elif re.search('chuangshi\.qq\.com\/bk\/so4\/p\/1\.html',response.url):
            for i in range(2,500):
            # for i in range(2, 5):
                url = re.sub('1.html','%d.html' %i,response.url)
                request =  scrapy.Request(url, callback=self.parse,priority = 100)
                request.meta['priority'] = -10
                request.meta['retry_times'] = 3
                yield request
        
        # for yunqi
        # for each in response.xpath('//div[@id="pageHtml2"]/a/@href').extract():
        #     request =  scrapy.Request(each, callback=self.parse,priority = 100)
        #     request.meta['priority'] = -10
        #     request.meta['retry_times'] = 3
        #     yield request

        for each in response.xpath('//div[@id="detailedBookList"]/div/a/@href').extract():
            request = scrapy.Request(each, callback=self.parse_item,priority = 2)
            request.meta['priority'] = 0
            yield request
        # for chuangshi
        for each in response.xpath('//td/a[@class="green"]/@href').extract():
            request = scrapy.Request(each, callback=self.parse_item,priority = 2)
            request.meta['priority'] = 0
            yield request
        # for each in response.xpath('//a[@class="nextBtn"]/@href').extract():
        #     request = scrapy.Request(each, callback=self.parse,priority = 100)
        #     request.meta['priority'] = -10
        #     request.meta['retry_times'] = 3
        #     yield request
        
    def parse_item(self, response):
        item = {}
        item['spiderid'] = 'chuangshi_yunqi'
        item['url'] = response.url
        item['name'] = response.xpath(
            '//div[@class="main2"]/div/div[3]/strong/a/text()').extract_first()
        item['author'] = response.xpath(
            '//div[@class="au_name"]/p[2]/a/text()').extract_first()
        if not item['author']:
            if re.search('</a>(\S{1,8})说：', response.text):
                item['author'] = re.search('</a>(\S{1,8})说：', response.text).group(1)
                print(item['author'])
            else:
                print(response.xpath('//*[@id="authorWeixinContent"]/text()').extract_first())
        item['category'] = response.xpath(
            '//div[@class="main2"]/div/div[3]/a[3]/text()').extract_first()
        item['description'] = ''
        if len(response.xpath('//div[@class="info"]/p/text()').extract()) != 0:
            for each in response.xpath('//div[@class="info"]/p/text()').extract():
                item['description'] = item['description'] + each
        item['description'] = item['description'][:255]
        search_result = re.search(
            '<td>总点击：(\d+)</td><td>总人气：(\d+)</td><td>周人气：\d+</td><td>总字数：(\d+)</td>',
            response.text)
        if search_result:
            item['page_view'] = int(search_result.group(1))
            item['totalrenqi'] = int(search_result.group(2))
            item['word_count'] = int(search_result.group(3))
        else:
            item['page_view'] = 0
            item['totalrenqi'] = 0
            item['word_count'] = 0
        item['points'] = 0
        item['status'] = response.xpath(
            '//div[@class="main1"]/div[1]/i[2]/text()').extract_first()
        search_result2 = re.search(
            '<td>月点击：\d+</td><td>月人气：\d+</td><td>月推荐：(\d+)</td>',
            response.text)
        if search_result2:
            item['yuepiao'] = int(search_result2.group(1))
        else:
            item['yuepiao'] = 0
        item['biaoqian'] = ''
        if len(response.xpath('//div[@class="tags"]/text()').extract()) != 0:
            for each in response.xpath('//div[@class="tags"]/text()').extract_first().split('：')[1].strip().split('、'):
                item['biaoqian'] = item['biaoqian'] + each + ','
        item['lastupdate'] = ''
        if len(response.xpath('//*[@id="newChapterList"]/div[1]/text()').extract()) != 0:
            item['lastupdate'] = \
                response.xpath(
                    '//*[@id="newChapterList"]/div[1]/text()').extract_first().split('：')[1].split(' ')[0]
        # else:
        #     item['lastupdate']=''

        item['image'] = response.xpath(
            '//a[@class="bookcover"]/img/@src').extract_first()
        item['current_date'] = time.strftime(
            '%Y-%m-%d', time.localtime(time.time())) 
        # item['site'] = 'chuangshi'
        item['haopingzhishu'] = '0.0'
        item['redpack'] = 0
        item['yuepiaoorder'] = 0
        item['flower'] = 0
        item['diamondnum'] = 0
        item['coffeenum'] = 0
        item['eggnum'] = 0
        item['redpackorder'] = 0
        item['isvip'] = ''
        item['total_recommend'] = 0
        # item['totalrenqi'] = 0
        item['hongbao'] = 0
        item['vipvote'] = 0
        item['shoucang'] = 0
        item['review_count'] = 0
        item['printmark'] = 0
        item['banquan'] = ''
        bookid = re.search('\/(\d+)\.html',response.url).group(1)
        if re.match('^(http|https|ftp)\://chuangshi.qq.com/.*', response.url):
            item['site'] = 'chuangshi'
        elif re.match('^(http|https|ftp)\://yunqi.qq.com/.*', response.url):
            item['site'] = 'yunqi'
        else:
            item['site'] = ''

        # yield item

        if re.match('^(http|https|ftp)\://chuangshi.qq.com/.*', response.url):
            req = scrapy.Request('http://chuangshi.qq.com/novelcomment/index.html?bid=%s' % bookid, callback=self.parse_comment)
        else :
            req = scrapy.Request('http://yunqi.qq.com/novelcomment/index.html?bid=%s' % bookid, callback=self.parse_comment)
        req.meta['item'] = item
        req.meta['priority'] = 10
        yield req

    def parse_comment(self, response):
        jsObj = json.loads(response.text)
        item = response.meta['item']
        item['comment_count'] = int(jsObj['data']['commentNum'])

        yield item
