# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from douban.items import MovieItemDetail
from douban.items import MovieItem


class DoubanPipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        self.collectionname_movieitem = settings["MONGODB_MOVIEITEM"]
        self.collectionname_moviedetail = settings["MONGODB_MOVIEDETAIL"]

        # 创建数据库库链接
        client = pymongo.MongoClient(host=host,port=port)

        # 指定数据库
        mydb = client[dbname]

        # 存放电影条目数据的集合名
        self.col_movieitem = mydb[self.collectionname_movieitem]

        # 存放电影详情的集合名
        # self.col_moviedetail = mydb[self.collectionname_moviedetail]

    def process_item(self, item, spider):
        if isinstance(item, MovieItem):
            DoubanPipeline.handle_movieitem(self, item)
        elif isinstance(item, MovieItemDetail):
            DoubanPipeline.handle_movieitemdetail(self, item)
        else:
            pass
        return item


    """
    处理电影条目
    """
    def handle_movieitem(self, item):
        data = dict(item)
        self.col_movieitem.insert(data)

    """
    处理电影明细
    """
    def handle_movieitemdetail(self, item):
        self.col_movieitem.update({"title": item["title"]}, {"$set": {"detail": item}})
        return item
