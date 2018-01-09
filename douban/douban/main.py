from scrapy import cmdline
# cmdline.execute("scrapy crawl doubanmovie -o items.json".split())
cmdline.execute("scrapy crawl MovieCrawlSpider".split())