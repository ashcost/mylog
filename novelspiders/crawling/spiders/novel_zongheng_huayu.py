# encoding: utf-8
from crawling.items import SpiderNovelItem
import time
import re
import scrapy
import crawling.spiders.fileloader


class ZonghengSpider(scrapy.Spider):
    name = "zongheng_huayu"
    # download_delay = 1
    #start_urls = ['http://book.zongheng.com/store/c0/c0/b0/u1/p1/v9/s9/t0/ALL.html'] 男
    #start_urls = ['http://book.zongheng.com/store/c0/c0/b9/u1/p1/v9/s9/t0/ALL.html']  所有
    #'http://book.zongheng.com/store/c0/c0/b1/u1/p1/v9/s9/t0/ALL.html' 女
    
    def parse(self, response):
        '''
        try:
            self._logger.debug("crawled url {}".format(response.request.url))
            urls = fileloader.loadurls() 
            for url in urls:
                self._logger.debug("crawled url {}".format(url))
                if re.match('zongheng\.com',url):
                    request = scrapy.Request(url, callback=self.book_details_zongheng,priority = 2)
                    yield request
                else:
                    request = scrapy.Request(url, callback=self.book_details_huayu,priority = 2)
                    yield request
        except Exception as e:
            self._logger.error(e.message)
        '''
        max_page = response.xpath('//div[@class="page"]/div/a[last()-1]/@page').extract_first()
        if int(max_page)>200:
            max_page = 200
        for i in range(1,int(max_page) + 1):
            next_page = re.sub('\/p\d+\/','/p%d/' %i,response.url)
            request = scrapy.Request(next_page, callback=self.parse_item,priority = 100)
            request.meta['priority'] = -10
            yield request
        for each in response.xpath('//span[@class="chap"]/a[@class="fs14"]/@href').extract():
            if re.match('^(http|https|ftp)\://book.zongheng.com/.*', each):
                request = scrapy.Request(each, callback=self.book_details_zongheng,priority = 2)
            else:
                request = scrapy.Request(each, callback=self.book_details_huayu,priority = 2)
            request.meta['priority'] = 0
            yield request
        
    def parse_item(self, response):
        for each in response.xpath('//span[@class="chap"]/a[@class="fs14"]/@href').extract():
            # print each
            if re.match('^(http|https|ftp)\://book.zongheng.com/.*', each):
                request = scrapy.Request(each, callback=self.book_details_zongheng,priority = 2)
            else:
                request = scrapy.Request(each, callback=self.book_details_huayu,priority = 2)
            request.meta['priority'] = 0
            yield request
    
    def book_details_huayu(self, response):
        try:
            item = {}
            item['spiderid'] = response.meta['spiderid']
            item['url'] = response.url
            item['name'] = response.xpath('//div[@class="booktitle"]/div/h1/a/text()').extract_first()
            item['author'] = response.xpath('//div[@class="booktitle"]/div/h1/span/a/text()').extract_first()
            item['category'] = response.xpath('//div[@class="loca title"]/a[3]/text()').extract_first()
            item['page_view'] = int(response.xpath('//div[@class="booknumber"]/text()').extract()[1].strip())
            item['comment_count'] = int(response.xpath('//span[@class="total_threads"]/text()').extract_first())
            item['word_count'] = int(response.xpath('//div[@class="booknumber"]/text()').extract()[2].strip())
            item['description'] = ''
            if len(response.xpath('//p[@class="jj"]/text()').extract())!=0:
                for each in response.xpath('//p[@class="jj"]/text()').extract():
                    item['description'] = item['description']+each
            item['description'] = item['description'][:255]
            item['points'] = int(response.xpath('//div[@class="booknumber"]/text()').extract()[4].strip())
            # print response.xpath('//div[@class="booktitle"]/div/h1/b/text()').extract()
            item['banquan'] = ''
            if len(response.xpath('//div[@class="booktitle"]/div/h1/b/text()').extract()) != 0:
                item['banquan'] = response.xpath('//div[@class="booktitle"]/div/h1/b/text()').extract_first()
            item['yuepiao'] = 0
            item['yuepiaoorder'] = 0
            item['flower']=0 
            item['diamondnum']=0
            item['coffeenum']=0
            item['eggnum']=0 
            item['redpack']= 0
            item['redpackorder']=0 
            item['isvip']=''
            item['shoucang'] = 0
            item['haopingzhishu']='0.0'
            item['total_recommend']=0 
            item['totalrenqi']=0
            item['hongbao']=0 
            item['vipvote']=0
            item['review_count'] = 0
            item['printmark'] = 0
            item['lastupdate'] = response.xpath('//div[@class="booknumber"]/text()').extract()[5].strip()
            item['status'] = ''
            if response.xpath('//div[@class="booktitle"]/div[2]/@class').extract_first() == 'lzz':
                item['status'] = '连载中'
            if response.xpath('//div[@class="booktitle"]/div[2]/@class').extract_first() == 'ywj':
                item['status'] = '已完结'
            item['biaoqian'] = ''
            if len(response.xpath('//div[@class="wz"]/p[2]/a/text()').extract()) != 0:
                # print response.xpath('//div[@class="wz"]/p[2]/a/text()').extract().encode('utf-8')
                # print len(response.xpath('//div[@class="wz"]/p[2]/a/text()').extract())
                for each in response.xpath('//div[@class="bookinfo"]/div[2]/p[2]/a/text()').extract():
                    # print each.encode('utf-8')
                    item['biaoqian'] = item['biaoqian'] + each + ','
            item['image'] = response.xpath('//div[@class="img"]/a/img/@src').extract_first()
            item['current_date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item['site'] = 'huayu'
            
            yield item
        except Exception as e:
            print ('huayu:' + response.url)
            print (e)
    def book_details_zongheng(self, response):
        try:
            item = {}
            item['spiderid'] = response.meta['spiderid']
            item['url'] = response.url
            item['name'] = response.xpath('//div[@class="main"]/div[2]/h1/a/text()').extract_first()
            item['author'] = response.xpath('//div[@class="main"]/div[2]/div[1]/a[1]/text()').extract_first()
            item['category'] = response.xpath('//div[@class="main"]/div[2]/div[1]/a[2]/text()').extract_first()
            if len(response.xpath('//div[@class="vote_info"]/p[3]/text()').extract()) != 0:
                item['page_view'] = int(response.xpath('//div[@class="vote_info"]/p[3]/text()').extract_first().strip())
            else:
                item['page_view'] = 0
            if len(response.xpath('//div[@class="vote_info"]/p[5]/text()').extract()) != 0:
                item['total_recommend'] = int(
                    response.xpath('//div[@class="vote_info"]/p[5]/text()').extract_first().strip())
            else:
                item['total_recommend'] = 0
            if len(response.xpath('//div[@class="vote_info"]/p[6]/text()').extract()) != 0:
                item['comment_count'] = int(response.xpath('//div[@class="vote_info"]/p[6]/text()').extract_first().strip())
            else:
                item['comment_count'] = 0
            item['word_count'] = int(response.xpath('//div[@class="main"]/div[2]/div[1]/span/text()').extract_first())
            item['description'] = ''
            if len(response.xpath('//div[@class="main"]/div[2]/div[2]/p/text()').extract())!=0:
                for each in response.xpath('//div[@class="main"]/div[2]/div[2]/p/text()').extract():
                    item['description'] = item['description'] + each
            item['description'] = item['description'][:255]
            item['points'] = 0
            item['yuepiao'] = int(response.xpath('//div[@class="vote_info"]/p[1]/text()').extract_first())
            item['shoucang'] = int(response.xpath('//div[@class="vote_info"]/p[4]/text()').extract_first())
            item['status'] = response.xpath('//meta[@name="og:novel:status"]/@content').extract_first()
            item['image'] = response.xpath('//div[@class="main"]/div[1]/p/a/img/@src').extract_first()
            item['current_date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item['site'] = 'zongheng'
            item['haopingzhishu'] = '0.0'
            item['redpack']=0
            item['yuepiaoorder']=0
            item['flower']=0
            item['diamondnum']=0
            item['coffeenum']=0
            item['eggnum']=0
            item['redpackorder']=0
            item['isvip']=''
            item['banquan'] = ''
            item['totalrenqi'] = 0
            item['lastupdate'] = ''
            item['hongbao']=0
            item['biaoqian'] = ''
            item['vipvote']=0
            item['review_count'] = 0
            item['printmark'] = 0
            yield item
        except Exception as e:
            print ('zongheng:' + response.url)
            print (e)
