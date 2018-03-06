# -*- coding: utf-8 -*-

import re
import time
import scrapy
# from redis_spider import RedisSpider
import crawling.spiders.fileloader
from crawling.spiders.fileloader import loadurls
import json
class QidianSpider(scrapy.Spider):
    name = "qidian"
    download_delay = 0.2
    # start_urls=loadurls()
    start_urls=['http://book.qidian.com/info/1003365191',
'http://book.qidian.com/info/1003306811',
'http://book.qidian.com/info/1003541158','http://book.qidian.com/info/3681640']
# 'http://book.qidian.com/info/1003755708',
# 'http://book.qidian.com/info/1003800714',
# 'http://book.qidian.com/info/1003362175'
    #start_urls = [

        #'http://a.qidian.com/?size=-1&sign=-1&tag=-1&chanId=-1&subCateId=-1&orderId=&page=1&month=-1&style=1&action=-1&vip=-1']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback=self.book_details,priority=2)

    def parse(self, response):
        print(11)
        
        try:
            self._logger.debug("crawled url {}".format(response.request.url))

            urls = loadurls()
            print(urls)
            for url in urls:
                self._logger.error(url)
                request = scrapy.Request(url, callback=self.book_details,priority = 2)
                yield request 
        except Exception as e:
            self._logger.error(e.message)
        '''
        try:
            max_page = response.xpath(
                '//div[@class="pagination fr"]/@data-pagemax').extract_first()
            max_page = 2000 
            for i in range(2,int(max_page)+1):
                request = scrapy.Request('http://a.qidian.com/?size=-1&sign=-1&tag=-1&chanId=-1&subCateId=-1&orderId=&page=%s&month=-1&style=1&action=-1&vip=-1' % i,callback =self.parse_item ,priority = 100)
                request.meta['priority'] = -10
                yield request
            for each in response.xpath('//ul[@class="all-img-list cf"]/li/div[1]/a/@href').extract():
                request = scrapy.Request('http:'+each, callback=self.book_details,priority = 2)
                request.meta['priority'] = 0
                yield request
        except Exception as e:
            print e
        '''
    def parse_item(self, response):

        for each in response.xpath('//ul[@class="all-img-list cf"]/li/div[1]/a/@href').extract():
            request = scrapy.Request('http:'+each, callback=self.book_details,priority = 2)
            request.meta['priority'] = 0
            yield request

    def book_details(self, response):

        item = {}
        item['spiderid'] = 'qidian'
        item['url'] = response.url
        if re.match('^(http|https|ftp)\://.*.qidian.com/.*', response.url):
            item['site'] = 'qidian'
        elif re.match('^(http|https|ftp)\://.*.qdmm.com/.*', response.url):
            item['site'] = 'qdmm'
        else:
            item['site'] = ''
        item['name'] = ''
        if len(response.xpath('/html/body/div[2]/div[6]/div[1]/div[2]/h1/em/text()').extract()) != 0:
            item['name'] = response.xpath(
                '/html/body/div[2]/div[6]/div[1]/div[2]/h1/em/text()').extract_first().strip()
        elif len(response.xpath('//div[@class="title"]/h1[@itemprop="name"]/text()').extract()) != 0:
            item['name'] = response.xpath(
                '//div[@class="title"]/h1[@itemprop="name"]/text()').extract_first().strip()
        elif len(response.xpath('//div[@class="title"]/strong[@itemprop="name"]/text()').extract()) != 0:
            item['name'] = response.xpath(
                '//div[@class="title"]/strong[@itemprop="name"]/text()').extract_first().strip()
        else:
            item['name'] = ''
        item['author'] = response.xpath(
            '/html/body/div[2]/div[6]/div[1]/div[2]/h1/span/a/text()').extract_first().strip()
        item['category'] = ','.join(response.xpath('//div[@class="book-info "]/p[@class="tag"]/a/text()').extract())
        item['description'] = ''
        if response.xpath('/html/body/div[2]/div[6]/div[1]/div[2]/p[2]'):
            item['description'] = response.xpath('/html/body/div[2]/div[6]/div[1]/div[2]/p[2]/text()').extract_first().strip()
        elif len(response.xpath('//*[@id="contentdiv"]/div/div[2]/span/text()').extract()) != 0:
            for each in response.xpath('//*[@id="contentdiv"]/div/div[2]/span/text()').extract():
                item['description'] = item['description'] + each.strip()
        elif len(response.xpath('//*[@id="contentdiv"]/div/div[1]/span/text()').extract()) != 0:
            for each in response.xpath('//*[@id="contentdiv"]/div/div[1]/span/text()').extract():
                item['description'] = item['description'] + each.strip()
        else:
            item['description'] = ''
        item['description'] = item['description'][:255]
        if response.xpath('//*[@id="recCount"]/text()').extract_first():
            item['yuepiao'] = response.xpath('//*[@id="recCount"]/text()').extract_first().strip()
        elif len(response.xpath('//span[@itemprop="monthlyRecommend"]/text()').extract()) != 0:
            item['yuepiao'] = int(response.xpath(
                '//span[@itemprop="monthlyRecommend"]/text()').extract_first())
        else:
            item['yuepiao'] = response.xpath('//*[@id="monthCount"]/text()').extract_first()

        if response.xpath('//*[@id="j_bookScore"]/text()').extract():
            item['haopingzhishu'] = ''.join(response.xpath('//*[@id="j_bookScore"]/text()').extract())
        elif len(response.xpath('//*[@id="bzhjshu"]/text()').extract()) != 0:
            item['haopingzhishu'] = response.xpath(
                '//*[@id="bzhjshu"]/text()').extract_first()
        else:
            item['haopingzhishu'] = '0.0'
        # if response.xpath('/html/body/div[2]/div[6]/div[1]/div[2]/p[3]/em[3]/text()').extract_first():
        #     item['total_recommend'] = response.xpath('/html/body/div[2]/div[6]/div[1]/div[2]/p[3]/em[3]/text()').extract_first()
        # else:
        #     item['total_recommend'] = int(response.xpath(
        #         '//span[@itemprop="totalRecommend"]/text()').extract_first())
        if response.xpath('/html/body/div[2]/div[6]/div[4]/div[1]/div[2]/ul/li[2]/em').extract_first():
            item['lastupdate'] = response.xpath('/html/body/div[2]/div[6]/div[4]/div[1]/div[2]/ul/li[2]/em/text()').extract_first()
        else:
            item['lastupdate'] = response.xpath(
                '//span[@itemprop="dateModified"]/text()').extract_first()
        if response.xpath(
            '/html/body/div[2]/div[6]/div[1]/div[2]/p[1]'):
            item['biaoqian'] = ' '.join(response.xpath(
                '/html/body/div[2]/div[6]/div[1]/div[2]/p[1]/*/text()').extract()).strip()
        elif len(response.xpath('//div[@class="labels"]/div/a/text()').extract()) != 0:
            for each in response.xpath('//div[@class="labels"]/div/a/text()').extract_first().split('、'):
                item['biaoqian'] = item['biaoqian'] + each + ','
        else:
            item['biaoqian'] = ''
        item['banquan'] = response.xpath(
            '//*[@id="bookdiv"]/div/table/tbody/tr[3]/td[3]/strong/text()').extract_first().strip() if len(
            response.xpath(
                '//*[@id="bookdiv"]/div/table/tbody/tr[3]/td[3]/strong/text()').extract()) != 0 else ''
        item['status'] = response.xpath(
            '/html/body/div[2]/div[6]/div[4]/div[1]/div[2]/ul/li[2]/span/text()').extract_first()
        item['points'] = 0
        book_detail = response.xpath('//div[@class="book-info "]/p[3]//text()').extract()
        # print(book_detail)
        item['word_count'] = float(book_detail[0])
        if '万' in book_detail[1]:
            item['word_count'] = int(item['word_count']*10000)
        item['page_view'] = float(book_detail[3])
        if '万' in book_detail[4]:
            item['page_view'] = int(item['page_view']*10000)
        item['total_recommend'] = float(book_detail[8])
        if '万' in book_detail[9]:
            item['total_recommend'] = int(item['total_recommend']*10000)
        # item['page_view'] = str(response.xpath(
        #     '/html/body/div[2]/div[6]/div[1]/div[2]/p[3]/em[2]/text()').extract_first())+str(response.xpath('/html/body/div[2]/div[6]/div[1]/div[2]/p[3]/cite[2]/text()[1]/text()').extract_first())
        # item['word_count'] = str(response.xpath(
        #     '/html/body/div[2]/div[6]/div[1]/div[2]/p[3]/em[1]/text()').extract_first())+str(response.xpath('/html/body/div[2]/div[6]/div[1]/div[2]/p[3]/cite[1]/text()').extract_first())
        
        item['image'] = response.xpath(
            '//*[@id="bookImg"]/img/@src').extract_first().strip()
        item['current_date'] = time.strftime(
            '%Y-%m-%d', time.localtime(time.time()))
        # item['site'] = "qidian"
        item['shoucang'] = 0
        # item['comment_count'] = 0
        item['redpack'] = 0
        item['yuepiaoorder'] = 0
        item['flower'] = 0
        item['diamondnum'] = 0
        item['coffeenum'] = 0
        item['eggnum'] = 0
        item['redpackorder'] = 0
        item['isvip'] = ''
        item['totalrenqi'] = 0
        item['hongbao'] = 0
        item['vipvote'] = 0
        item['printmark'] = 0

        isBookId = response.url.split('/')[-1].split('.')[0]
        bookid = 0
        if isBookId.isdigit():
            bookid = response.url.split('/')[-1].split('.')[0]
        else:
            bookid = response.url.split('=')[1]
        # print (str(response.headers.getlist('Set-Cookie')[0]).split(';'))
        cookies = [t.split('=') for t in str(response.headers.getlist('Set-Cookie')[0]).split(';')]

        print(cookies)
        csrfToken = None
        # csrfToken = cookies[0][1]
        # print(csrfToken)
        for cookie in cookies:
            if cookie[0] == "b'_csrfToken":
                csrfToken = cookie[1]
                print(csrfToken)
                break
        if csrfToken:
            request = scrapy.Request("http://book.qidian.com/ajax/book/GetBookForum?_csrfToken=%s&bookId=%s&chanId=21&pageSize=0" % (csrfToken,bookid),
                                    callback=self.book_comment)
            request.meta['item'] = item
            request.meta['priority'] = 10
            yield request
        else:
            request = scrapy.Request("http://forum.qidian.com/NewForum/List.aspx?BookId=%s" % bookid,
                                    callback=self.book_details_extra)
            request.meta['item'] = item
            request.meta['priority'] = 10
            yield request

    def book_comment(self, response):
        item = response.meta['item']
        result = json.loads(response.text)
        # print(result)
        item['comment_count'] = result['data']['threadCnt']
        item['review_count']=0
        # item['comment_count'] = int(response.xpath(
        #    '//*[@id="lblPostCnt"]/text()').extract_first().strip())
        # item['review_count']=0
        # item['comment_count']=0
        yield item

    def book_details_extra(self, response):
        item = response.meta['item']
        # //*[@id="lblReviewCnt"]
        #item['review_count'] = int(response.xpath(
        #    '//ul/li/a[@class="nav-tab act"]/text()').extract_first().strip())
        result = response.xpath('//ul/li/a[@class="nav-tab act"]/text()').extract_first().strip()
        comment_count = re.search('\((\d+)\)',result).group(1)
        item['comment_count'] = int(comment_count)
        item['review_count']=0
        item['comment_count'] = int(response.xpath(
           '//*[@id="lblPostCnt"]/text()').extract_first().strip())
        item['review_count']=0
        item['comment_count']=0
        yield item
        # print item
