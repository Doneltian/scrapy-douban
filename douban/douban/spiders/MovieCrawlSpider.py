# 使用scrapy自动实现多网页爬取功能
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from douban.items import MovieItemDetail
from douban.items import MovieItem
import re
"""
继承自CrawlSpider，实现自动爬取的爬虫。
"""
"""
首先，基类CrawlSpider提供了更完善的自动多网页爬取机制，只需要我们配置的就是rules，通过Rule对象实现链接的提取与跟进，恩，对，没了。。。就这样。详细的注释也都在程序中。
"""


class MovieCrawlSpider(CrawlSpider):
    name = "MovieCrawlSpider"
    # 设置下载延时
    download_delay = 2
    allowed_domains = ["movie.douban.com"]
    # 第一个地址
    start_urls = ['https://movie.douban.com/top250?start=0&filter=']
    # 需要替换的字符
    map_replace = {" ": "", "\\n": "", "\\u3000": ""}
    """
    class scrapy.contrib.spiders.Rule (  
        link_extractor, callback=None,cb_kwargs=None,follow=None,process_links=None,process_request=None )  
    link_extractor为LinkExtractor，用于定义需要提取的链接。
    callback参数：当link_extractor获取到链接时参数所指定的值作为回调函数。
    callback参数使用注意：

    当编写爬虫规则时，请避免使用parse作为回调函数。于CrawlSpider使用parse方法来实现其逻辑，如果您覆盖了parse方法，crawlspider将会运行失败。
    follow：指定了根据该规则从response提取的链接是否需要跟进。当callback为None,默认值为true。
    process_links：主要用来过滤由link_extractor获取到的链接。
    process_request：主要用来过滤在rule中提取到的request。
    
    """

    """
    classscrapy.contrib.linkextractors.sgml.SgmlLinkExtractor(  
            allow=(),deny=(),allow_domains=(),deny_domains=(),deny_extensions=None,restrict_xpaths=(),tags=('a','area'),attrs=('href'),canonicalize=True,unique=True,process_value=None)  
    allow：满足括号中“正则表达式”的值会被提取，如果为空，则全部匹配。
    deny：与这个正则表达式(或正则表达式列表)不匹配的URL一定不提取。
    allow_domains：会被提取的链接的domains。
    deny_domains：一定不会被提取链接的domains。
    restrict_xpaths：使用xpath表达式，和allow共同作用过滤链接。
    """

    # rules = (
    #     # Extract links matching 'category.php' (but not matching 'subsection.php')
    #     # and follow links from them (since no callback means follow=True by default).
    #     Rule(LinkExtractor(allow=('category\.php',), deny=('subsection\.php',))),
    #
    #     # Extract links matching 'item.php' and parse them with the spider's method parse_item
    #     Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
    # )

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('top250\?start\=([\d]+).*'), deny=('/standbyme/',)), callback='parse_item',follow=True),
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('subject/([\d]+)/',),deny=('/standbyme/',)), callback='parse_detail'),
    )

    def parse_item(self, response):
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
            item['detail'] = { }
            yield item

    def parse_detail(self, response):
        # self.logger.info('parse_detail function called on %s', response.url)
        sel = Selector(response)
        item_detail = MovieItemDetail()
        item_detail['title'] = sel.xpath('//div[@id="content"]/h1/span/text()').extract_first().split(' ')[0]
        item_detail['director'] = sel.xpath('//div[@id="info"]/span[1]/span[@class="attrs"]/a/text()').extract_first()
        item_detail['actor'] = sel.xpath('//div[@id="info"]/span[@class="actor"]/span[@class="attrs"]//a/text()').extract()
        item_detail['screenwriter'] = sel.xpath('//div[@id="info"]/span[2]/span[@class="attrs"]//a/text()').extract()
        item_detail['movietype'] = sel.xpath('//div[@id="info"]//span[@property="v:genre"]/text()').extract()
        item_detail['movietime'] = sel.xpath('//div[@id="info"]/span[@property="v:runtime"]/text()').extract_first()
        item_detail['year'] = sel.xpath('//div[@id="info"]//span[@property="v:initialReleaseDate"]/text()').extract()
        item_detail['language'] = sel.xpath('//div[@id="info"]/span[contains(text(), "语言:")]/following::text()[1]').extract()
        item_detail['alias'] = sel.xpath('//div[@id="info"]/span[contains(text(), "又名:")]/following::text()[1]').extract()
        summary_text = str(sel.xpath('//div[@class="related-info"]/div[@class="indent"]//span[@property="v:summary"]/text()').extract())
        # item_detail['summary'] =self.multiple_replace(summary_text,self.map_replace)
        translate = MovieCrawlSpider.make_xlat(self.map_replace)
        item_detail['summary'] = translate(summary_text)
        item_detail['posterurl'] = sel.xpath('//div[@id="mainpic"]/a/img[@rel="v:image"]/@src').extract()
        yield item_detail
    # 弃用
    @classmethod
    def multiple_replace(self,text,adict):
        rx = re.compile('|'.join(map(re.escape(adict))))

        def one_xlat(match):
            return adict[match.group[0]]
        return rx.sub(one_xlat,text)

    # 通用方法
    @staticmethod
    def make_xlat(*args, **kwds):
        adict = dict(*args, **kwds)
        rx = re.compile('|'.join(map(re.escape, adict)))

        def one_xlat(match):
            return adict[match.group(0)]

        def xlat(text):
            return rx.sub(one_xlat, text)

        return xlat

