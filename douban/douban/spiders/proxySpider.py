import scrapy

from douban.items import MovieItem


class ProxieSpider(scrapy.Spider):
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

    name = "proxie"
    allowed_domains = ["*.douban.com"]
    start_urls = ['https://movie.douban.com/top250?start=0&filter=']

    def parse(self, response):
        # self.logger.info('parse_item function called on %s', response.url)
        for info in response.xpath('//div[@class="item"]'):
            item = MovieItem()
            item['rank'] = int(info.xpath('div[@class="pic"]/em/text()').extract_first())
            item['title'] = info.xpath('div[@class="info"]/div[@class="hd"]/a/span/text()').extract_first()
            # item['link'] = info.xpath('/div[@class="pic"]／a/img/@src').extract_first()
            item['star'] = info.xpath(
                'div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
            item['rate'] = info.xpath(
                'div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[last()]/text()').extract_first()
            item['quote'] = info.xpath(
                'div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract_first()
            item['detail'] = {}
            yield item