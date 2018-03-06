from builtins import object
# -*- coding: utf-8 -*-

# Define your item pipelines here

import ujson
import datetime as dt
import sys
import traceback
import base64
from builtins import bytes, str

from datetime import datetime
from hashlib import md5
from scrapy.exceptions import DropItem
from crawling.items import TiebaStats,TVComment,WeiboTopicCommentItem,NovelComment,WeiboItem,WeiboTopicItem
from twisted.enterprise import adbapi
import logging


class MySqlPipeline(object):
    """A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool
        logging.debug("setup MySql Pipeline")
    
    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
            cp_reconnect = True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs) 
        return cls(dbpool)
        
    def process_item(self,item,spider): 
        # item['appid'] = spider.appid
        # item['crawlid'] = spider.crawlid
        # run db query in the thread pool
        logging.debug("Processing item in MySqlPipeline")
        if isinstance(item, TiebaStats):
            d = self.dbpool.runInteraction(self._do_tiebastats_upsert, item, spider) 
        elif isinstance(item, TVComment):
            d = self.dbpool.runInteraction(self._do_tvcomment_upsert, item, spider)
        elif isinstance(item, WeiboTopicItem):
            d = self.dbpool.runInteraction(self._do_weibotopic_upsert, item, spider)
        
        elif isinstance(item, WeiboTopicCommentItem):
            d = self.dbpool.runInteraction(self._do_weibotopiccomment_upsert, item, spider) 
        
        elif isinstance(item, NovelComment):
            d = self.dbpool.runInteraction(self._do_novelcomment_upsert, item, spider)
        
        elif isinstance(item, WeiboItem):
            d = self.dbpool.runInteraction(self._do_weibo_upsert, item, spider)
        
        elif item['spiderid'] == 'weibocomments':
            d = self.dbpool.runInteraction(self._do_weibocomment_upsert, item, spider)
        
        elif item['spiderid'] == 'weiboindex':
            d = self.dbpool.runInteraction(self._do_weiboindex_upsert, item, spider)
        elif item['spiderid'] == 'tvplaycount':
            d = self.dbpool.runInteraction(self._do_tvplaycount_upsert, item, spider)
        
        elif item['spiderid'] == 'tvcomment':
            d = self.dbpool.runInteraction(self._do_tvcomment_upsert, item, spider)
        elif item['spiderid'] == 'moviecomments':
            d = self.dbpool.runInteraction(self._do_moviecomment_upsert, item, spider)
        elif item['spiderid'] == 'cpnews':
            d = self.dbpool.runInteraction(self._do_cpnews_upsert, item, spider)
        elif item['spiderid'] == 'cpplaycount':
            d = self.dbpool.runInteraction(self._do_cpplaycount_upsert, item, spider)
        else:
            d = self.dbpool.runInteraction(self._do_novel_upsert, item, spider)
        
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d
    def _do_novel_upsert(self, conn, item, spider):
        print('*'*100)
        # now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        try:
            if item['current_date']:
                now = item['current_date']
            else:
                now = date.today()
            if 'pubtime' not in item.keys():
                item['pubtime'] = None
            conn.execute("""
                        replace INTO `rawdata`
                                    (`name`,
                                    `url`,
                                    `author`,
                                    `category`,
                                    `page_view`,
                                    `word_count`,
                                    `description`,
                                    `points`,
                                    `yuepiao`,
                                    `shoucang`,
                                    `comment_count`,
                                    `review_count`,
                                    `redpack`,
                                    `yuepiaoorder`,
                                    `flower`,
                                    `diamondnum`,
                                    `coffeenum`,
                                    `eggnum`,
                                    `redpackorder`,
                                    `isvip`,
                                    `status`,
                                    `imageurl`,
                                    `banquan`,
                                    `biaoqian`,
                                    `haopingzhishu`,
                                    `total_recommend`,
                                    `totalrenqi`,
                                    `pubtime`,
                                    `lastupdate`,
                                    `crawldate`,
                                    `hongbao`,
                                    `vipvote`,
                                    `printmark`,
                                    `site`)
                                    VALUES
                                    (%s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s)
                    """, (
                item['name'], item['url'], item['author'], item['category'], item['page_view'], item['word_count'],
                item['description'], item['points'], item['yuepiao'], item['shoucang'], item['comment_count'],
                item['review_count'],item['redpack'], item['yuepiaoorder'], item['flower'], item['diamondnum'],
                item['coffeenum'], item['eggnum'], item['redpackorder'], item['isvip'], item['status'], item['image'],
                item['banquan'], item['biaoqian'], item['haopingzhishu'], item['total_recommend'], item['totalrenqi'],
                item['pubtime'], item['lastupdate'], now, item['hongbao'], item['vipvote'], item['printmark'],item['site']))
            #result = conn.fetchall()
        except Exception as e:
            logging.error("Insert item to Mysql faild.")
            logging.error('$$'*100)
            print(e)

    def _do_weibo_upsert(self,conn,item,spider):
        conn.execute("""replace into `spider_result_weibo_timeline` 
        (`mid`,`created_at`,`text`,`source`,`userid`,`profile_url`,`appid`,`crawlid`,`reposts_count`,`comments_count`,`attitudes_count`)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", 
        (item['mid'],item['created_at'],item['text'],
        item['source'],item['userid'],item['profile_url'],
        item['appid'],item['crawlid'],item['reposts_count'],
        item['comments_count'],item['attitudes_count']))
        logging.debug("Item updated in db: %s" % item['mid'])

    def _do_cpnews_upsert(self,conn,item,spider):
        """Perform an insert or update.""" 
        #item.setdefault('name', None)
        #item.setdefault('category', None)
        #item.setdefault('url', None) 
        #insert into `spider_result_comments` (`id`,`url`,`commentid`,`title`,`content`,`createtime`,`createtime_raw`,`appid`,`crawlid`)
 
        conn.execute("""replace into `spider_result_cpnews` 
        (`url`,`cpname`,`newscount`,`appid`,`crawlid`)
        values(%s,%s,%s,%s,%s);""", 
        (item['url'],item['attrs']['cpname'],
        item['attrs']['newscount'],
        item['appid'],item['crawlid']))
        logging.debug("Item updated in db: %s" % item['attrs']['cpname'])
    def _do_cpplaycount_upsert(self,conn,item,spider):
        """Perform an insert or update.""" 
        #item.setdefault('name', None)
        #item.setdefault('category', None)
        #item.setdefault('url', None) 
        #insert into `spider_result_comments` (`id`,`url`,`commentid`,`title`,`content`,`createtime`,`createtime_raw`,`appid`,`crawlid`)
 
        conn.execute("""replace into `spider_result_cpplaycount` 
        (`url`,`cpname`,`playcount`,`title`,`appid`,`crawlid`)
        values(%s,%s,%s,%s,%s,%s);""", 
        (item['attrs']['url'],item['attrs']['cpname'],item['attrs']['playcount'],
        item['attrs']['title'],
        item['appid'],item['crawlid']))
        logging.debug("Item updated in db: %s" % item['attrs']['url'])
    def _do_novelcomment_upsert(self,conn,item,spider):
        """Perform an insert or update."""
        item.setdefault('createtime', None)
        #item.setdefault('name', None)
        #item.setdefault('category', None)
        #item.setdefault('url', None) 
        #insert into `spider_result_comments` (`id`,`url`,`commentid`,`title`,`content`,`createtime`,`createtime_raw`,`appid`,`crawlid`)
 
        conn.execute("""replace into `spider_result_comments` 
        (`url`,`commentid`,`title`,`content`,`createtime`,`createtime_raw`,`appid`,`crawlid`)
        values(%s,%s,%s,%s,%s,%s,%s,%s);""", 
        (item['url'],item['commentid'],item['title'],
        item['content'],item['createtime'],item['createtime_raw'],
        item['appid'],item['crawlid']))
        logging.debug("Item updated in db: %s" % item['content'])       
    # def _do_weibocomment_upsert(self,conn,item,spider):
    #     conn.execute("""replace into `spider_result_weibo_comments` 
    #     (`mid`,`created_at`,`statusid`,`text`,`source`,`userid`,`appid`,`crawlid`,`gender`)
    #     values(%s,%s,%s,%s,%s,%s,%s,%s,%s);""", 
    #     (item['mid'],item['created_at'],item['statusid'],item['text'],
    #     item['source'],item['userid'],
    #     item['appid'],item['crawlid'],item['gender']))
    #     logging.debug("Item updated in db: %s" % item['mid'])

    def _do_weibocomment_upsert(self,conn,item,spider):
        conn.execute("""replace into `spider_result_weibocomments` 
        (`id`,`weibo_url`,`created_at`,`source`,`userid`,`screen_name`,`text`,`appid`,`crawlid`)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s);""", 
        (item['attrs']['id'],item['attrs']['weibo_url'],item['attrs']['created_at'],item['attrs']['source'],item['attrs']['userid'],
        item['attrs']['screen_name'],item['attrs']['text'],
        item['appid'],item['crawlid']))
        logging.debug("Item updated in db: %s" % item['attrs']['text'])
    
    def _do_weiboindex_upsert(self,conn,item,spider):
        conn.execute("""insert ignore into `spider_result_weiboindex` 
        (`keyword`,`wid`,`pc`,`mobile`,`total`,`day`,`appid`,`crawlid`)
        values(%s,%s,%s,%s,%s,%s,%s,%s);""", 
        (item['attrs']['keyword'],item['attrs']['wid'],item['attrs']['pc'],item['attrs']['mobile'],
        item['attrs']['total'],item['attrs']['day'],
        item['appid'],item['crawlid']))
        result = conn.fetchall()
        logging.debug("Item updated in db: %s %s" % (item['attrs']['wid'], result))
    
    def _do_weibotopic_upsert(self,conn,item,spider):
        conn.execute("""replace into `spider_result_weibotopic` 
        (`topic`,`topic_url`,`read_count`,`discuss`,`fans`,`qa`,`host_name`,`host_url`,`host_tweets`,`host_follows`,`host_fans`,`appid`,`crawlid`,`crawltime`)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", 
        (item['topic'],item['topic_url'],item['read_count'],item['discuss'],
        item['fans'],item['qa'],item['host_name'],item['host_url'],item['host_tweets'],
        item['host_follows'],item['host_fans'],
        item['appid'],item['crawlid'],item['crawltime']))
        logging.debug("Item updated in db: %s" % (item['topic']))

    def _do_weibotopiccomment_upsert(self,conn,item,spider):
        conn.execute("""replace into `spider_result_weibotopiccomments` 
        (`created_at`,`commentid`,`content`,`user`,`reposts_count`,`comments_count`,`attitudes_count`,`appid`,`crawlid`)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s);""", 
        (item['created_at'],item['commentid'],item['content'],item['user'],
        item['reposts_count'],item['comments_count'],item['attitudes_count'],
        item['appid'],item['crawlid']))
        logging.debug("Item updated in db: %s" % (item['content']))


    def _do_tvplaycount_upsert(self,conn,item,spider):
        item.setdefault('createtime', None)
        conn.execute("""replace into `spider_result_playcount` 
        (`appid`,`crawlid`,`title`,`description`,`url`,`website`,`playcount`,`createtime`)
        values(%s,%s,%s,%s,%s,%s,%s,%s);""", 
        (item['appid'],item['crawlid'],item['attrs']['title'],
        item['attrs']['description'],item['attrs']['url'],item['attrs']['website'],
        item['attrs']['playcount'],item['attrs']['createtime']))
        logging.debug("Item updated in db: %s" % (item['attrs']['url']))


    def _do_tvcomment_upsert(self,conn,item,spider):
        """Perform an insert or update."""
        item.setdefault('createtime', None)
        #item.setdefault('name', None)
        #item.setdefault('category', None)
        #item.setdefault('url', None) 
        #insert into `spider_result_comments` (`id`,`url`,`commentid`,`title`,`content`,`createtime`,`createtime_raw`,`appid`,`crawlid`)
        conn.execute("""replace into `spider_result_comments` 
        (`url`,`commentid`,`title`,`content`,`createtime`,`createtime_raw`,`appid`,`crawlid`)
        values(%s,%s,%s,%s,%s,%s,%s,%s);""", 
        (item['url'],item['commentid'],item['title'],
        item['content'],item['createtime'],item['createtime_raw'],
        item['appid'],item['crawlid']))
        logging.debug("Item updated in db: %s" % item['content'])

    def _do_moviecomment_upsert(self,conn,item,spider):
        """Perform an insert or update."""
        item.setdefault('createtime', None)
        conn.execute("""replace into `spider_result_comments` 
        (`url`,`commentid`,`title`,`content`,`createtime`,`createtime_raw`,`appid`,`crawlid`)
        values(%s,%s,%s,%s,%s,%s,%s,%s);""", 
        (item['attrs']['url'],item['attrs']['commentid'],item['attrs']['title'],
        item['attrs']['content'],item['attrs']['createtime'],item['attrs']['createtime_raw'],
        item['appid'],item['crawlid']))
        logging.debug("Item updated in db: %s" % item['content'])

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        logging.debug(failure,item)
    
    def _do_tiebastats_upsert(self, conn, item, spider): 
        """Perform an insert or update."""
        item.setdefault('name', None)
        item.setdefault('category', None)
        item.setdefault('url', None) 
        conn.execute("""replace into `tbl_tiebastats` 
        (`url`,`name`,`category`,`day`,`member_count`,`sign_count`,`post_count`,`thread_count`)
        values(%s,%s,%s,%s,%s,%s,%s,%s);""", 
        (item['url'],item['name'],item['category'],
        item['day'],item['member_count'],item['sign_count'],
        item['post_count'],item['thread_count']))
        logging.debug("Item updated in db: %s" % (item['url']))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        logging.debug(failure)
