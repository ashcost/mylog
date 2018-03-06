# -*- coding: utf-8 -*-

# Define here the models for your scraped items

from scrapy import Item, Field

class RawResponseItem(Item):
    appid = Field()
    crawlid = Field()
    url = Field()
    response_url = Field()
    status_code = Field()
    status_msg = Field()
    response_headers = Field()
    request_headers = Field()
    body = Field()
    links = Field()
    attrs = Field()
    success = Field()
    exception = Field()
    spiderid = Field() 


class TiebaStats(RawResponseItem): 
    url = Field()
    member_count = Field(default=0)
    sign_count = Field(default=0)
    post_count = Field(default=0) 
    thread_count = Field(default=0)
    name = Field()
    category = Field()
    day = Field()
    
    
class TVComment(RawResponseItem):
    commentid = Field()
    title = Field()
    up = Field()
    down = Field()
    rep = Field()
    content = Field()
    createtime = Field()
    createtime_raw = Field()
    
class NovelComment(RawResponseItem):
    commentid = Field()
    title = Field()
    content = Field()
    createtime = Field()
    createtime_raw = Field()
    
class WeiboItem(RawResponseItem):
    created_at = Field()
    
    profile_url = Field()
    id = Field() # 16位微博ID
    mid = Field() # 16位微博ID 
    idstr = Field() # 字符串型的微博ID
    text = Field()  
    #####
    source = Field()
    userid = Field()  # just uid  
    reposts_count = Field()
    comments_count = Field()
    attitudes_count = Field() 
 
    
class WeiboTopicItem(RawResponseItem):
    topic = Field()
    topic_url = Field()
    read_count = Field()
    discuss = Field()
    fans = Field()
    qa = Field()
    host_name = Field()
    host_url = Field()
    host_tweets = Field()
    host_follows = Field()
    host_fans = Field()
    crawltime = Field()

class WeiboTopicCommentItem(RawResponseItem):
    created_at = Field()
    commentid = Field()
    content = Field()
    user = Field()
    reposts_count = Field()
    comments_count = Field()
    attitudes_count = Field()


class NewsItem(RawResponseItem):
    title = Field()
    pubtime = Field()
    crawltime = Field()
    web = Field()

class SpiderNovelItem(RawResponseItem):
    # define the fields for your item here like:
    name = Field(default=None)  # 小说书名
    url = Field(default=None)  # 小说链接
    author = Field(default=None)  # 小说作者
    category = Field(default=None)  # 小说类别
    page_view = Field(default=0)  # 小说阅读量
    word_count = Field(default=0)  # 小说字数
    description = Field(default=None)  # 小说描述
    points = Field(default=0)  # 小说积分
    yuepiao = Field(default=0)  # 小说月票
    shoucang = Field(default=0)  # 收藏
    comment_count = Field(default=0)  # 评论数
    review_count = Field(default=0)  # 主题数
    redpack = Field(default=0)  # 荷包
    yuepiaoorder = Field(default=0)  # 月票排名
    flower = Field(default=0)  # 鲜花
    diamondnum = Field(default=0)  # 钻石
    coffeenum = Field(default=0)  # 咖啡
    eggnum = Field(default=0)  # 鸡蛋
    redpackorder = Field(default=0)  # 荷包收入排名
    isvip = Field(default=None)  # VIP书籍
    status = Field(default=None)  # 小说状态
    image = Field(default=None)  # 小说图片
    banquan = Field(default=None)  # 小说版权
    hongbao = Field(default=0)  # 红包
    vipvote = Field(default=0)  # 投贵宾
    biaoqian = Field(default=None)  # 小说标签
    haopingzhishu = Field(default=0)  # 小说好评指数
    weekclickCount = Field(default=0)  # 本周阅读数
    monthclickCount = Field(default=0)  # 本月阅读数
    bookSignInCount = Field(default=0)  # 累计签到数
    printmark = Field(default=0)  # 盖个章
    total_recommend = Field(default=0)  # 小说总推荐
    totalrenqi = Field(default=0)  # 小说人气
    pubtime = Field(default=None)  # 小说上线时间
    lastupdate = Field(default=None)  # 小说最新更新日期
    current_date = Field(default=None)  # 抓取数据日期
    site = Field(default=None)  # 小说所在网站