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


class MovieItem(scrapy.Item):
    #电影排名
    rank = scrapy.Field()

    #电影标题
    title = scrapy.Field()

    #电影详情链接
    link = scrapy.Field()

    #电影评分
    star = scrapy.Field()

    #影评次数
    rate = scrapy.Field()

    #豆瓣评论
    quote = scrapy.Field()
