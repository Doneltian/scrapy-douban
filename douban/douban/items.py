# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


"""豆瓣电影条目"""
class MovieItem(scrapy.Item):
    # 电影排名
    rank = scrapy.Field()

    # 电影标题
    title = scrapy.Field()

    # 电影详情链接
    link = scrapy.Field()

    # 电影评分
    star = scrapy.Field()

    # 影评次数
    rate = scrapy.Field()

    # 豆瓣评论
    quote = scrapy.Field()

    # 详情
    detail = scrapy.Field()

"""电影详情"""


class MovieItemDetail(scrapy.Item):
    # 电影标题
    title = scrapy.Field()

    # 导演
    director = scrapy.Field()

    # 编剧
    screenwriter = scrapy.Field()

    # 片长
    movietime = scrapy.Field()

    # 上映时间
    year = scrapy.Field()

    # 主演
    actor = scrapy.Field()

    # 类型
    movietype = scrapy.Field()

    # 语言
    language = scrapy.Field()

    # 又名
    alias = scrapy.Field()

    # 剧情简介
    summary = scrapy.Field()

    # 电影海报路径
    posterurl = scrapy.Field()