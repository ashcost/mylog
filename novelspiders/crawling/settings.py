# -*- coding: utf-8 -*-
BOT_NAME = 'crawling'

SPIDER_MODULES = ['crawling.spiders']
NEWSPIDER_MODULE = 'crawling.spiders'
REDIS_HOST = '192.168.1.220'
SC_LOG_STDOUT = True
SC_LOG_JSON = False
SC_LOG_DIR = '/var/scrapy-cluster'
SC_LOG_LEVEL = 'DEBUG'


REFERER_ENABLED = True
QUEUE_HITS = 60
QUEUE_WINDOW = 10

MYSQL_HOST = '192.168.2.10'
MYSQL_DBNAME = 'novel_rawdata'
MYSQL_USER = 'crotonadmin'
MYSQL_PASSWD = 'Data2014'
MYSQL_PORT = 3306
WEIBO_TOKEN = '2.00ZLWYdC0KWpTW73ca4f3acb4k45rD'
# ITEM_PIPELINES = {
#     'crawling.pipelines.MySqlPipeline': 99
# }
