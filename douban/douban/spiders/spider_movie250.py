# -*- coding:utf-8 -*-
import scrapy
from douban.items import MovieItem


class Movie250Spider(scrapy.Spider):
    #定义爬虫名称，主要main方法使用
    name = 'doubanmovie'
    allowed_domains = ["douban.com"]
    start_urls = ["https://movie.douban.com/top250"]


    #解析数据
    def parse(self,response):
        items = []
        for info in response.xpath('//div[@class="item"]'):
            item = MovieItem()
            item['rank'] = info.xpath('div[@class="pic"]/em/text()').extract_first()
            item['title'] = info.xpath('div[@class="info"]/div[@class="hd"]/a/span/text()').extract_first()
            # item['link'] = info.xpath('/div[@class="pic"]／a/img/@src').extract_first()
            item['star'] = info.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
            item['rate'] = info.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[last()]/text()').extract_first()
            item['quote'] = info.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract_first()
            yield item
        #翻页
        next_page = response.xpath('//span[@class="next"]/a/@href')
        if next_page:
             url = response.urljoin(next_page[0].extract())
             yield scrapy.Request(url, self.parse)