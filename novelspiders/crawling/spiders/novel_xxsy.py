# -*- coding: utf-8 -*-
import time
import re
import json
from crawling.items import SpiderNovelItem
# from redis_spider import scrapy.Spider
import scrapy


class XxsySpider(scrapy.Spider):
    name = "xxsy"
    # download_delay = 1
    # PAGE_SIZE = 400
    #start_urls = ['http://www.xxsy.net/search?s_wd=&pn=1&sort=1']

    def parse(self, response):
        self._logger.debug("crawled url {}".format(response.request.url))
        pn = int(re.search('pn=(\d+)',response.url).group(1))
        if pn == 1:
            page_count = 1000
            for i in range(2, page_count +1):
                next_page = re.sub('pn=1','pn=%d' %i,response.url)
                request = scrapy.Request(next_page,priority = 100)
                request.meta['priority'] = -10
                yield request
        for node in response.xpath('//div[@class="result-list"]/ul/li'):
            try: 
                item = {}
                item['spiderid'] = response.meta['spiderid'] 
                item['url'] = "http://www.xxsy.net" + node.xpath('div[@class="info"]/h4/a/@href').extract_first()
                item['name'] = node.xpath('div[@class="info"]/h4/a/text()').extract_first()
                item['author'] = node.xpath('div[@class="info"]/h4/span/a[1]/text()').extract_first()
                values = node.xpath('div[@class="info"]/p[@class="number"]/span/text()').extract()
                #item['page_view'] = values[0].replace(u'总点击：','') 
                item['word_count'] = int(values[4].replace(u'字数：',''))
                item['lastupdate'] = values[3].replace('更新：','')
                item['yuepiao'] = values[1].replace('月票：','')
                item['category'] = node.xpath('div[@class="info"]/h4/span[@class="subtitle"]/a[2]/text()').extract_first()
                item['description'] = node.xpath('div[@class="info"]/p[@class="detail"]/text()').extract_first()
                #item['shoucang'] = int(node.xpath('li[@class="title"]/span[3]/text()').extract_first())
                item['status'] = node.xpath('div[@class="info"]/h4/span[@class="subtitle"]/span/text()').extract_first()
                item['banquan'] = '' #node.xpath('li[@class="title"]/span[3]/text()').extract_first()
                
                item['biaoqian'] = node.xpath('div[@class="info"]/h4/span[@class="subtitle"]/a[3]/text()').extract_first()
                
                item['image'] = node.xpath('//a[@class="book commonbook"]/img/@src').extract_first()
                item['current_date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                item['points'] = 0
                item['site'] = 'xxsy'
                item['haopingzhishu'] = '0.0'
                item['comment_count']=0
                item['redpack']=0
                item['yuepiaoorder']=0
                item['flower']=0
                item['diamondnum']=0
                item['coffeenum']=0
                item['eggnum']=0
                item['redpackorder']=0
                item['isvip']=''
                item['total_recommend']=0
                item['totalrenqi']=0
                item['hongbao']=0
                item['vipvote']=0
                item['review_count'] = 0
                item['printmark'] = 0
                # print item
                req = scrapy.Request(item['url'] , callback=self.parse_item,priority = 2)
                req.meta['item'] = item
                req.meta['priority'] = 0
                yield req
            except Exception as e:
                self._logger.error(e)
    def parse_item(self, response):
        item = response.meta['item'] 
        try:
            values = response.xpath('//p[@class="sub-data"]/span/em/text()').extract()
            item['page_view'] = self.parseString(values[1])
            item['shoucang'] = self.parseString(values[2])
            yield item
        except Exception as e:
            self._logger.error(e)
    def parseString(self,strValue):
        result = 0
        self._logger.debug(strValue)
        data = float(re.search('([\d.]+)',strValue).group(1))
        self._logger.debug(data)
        if '万' in strValue:
            result = data* 10000
        if '亿' in strValue:
            result = data* 100000000
        return result

