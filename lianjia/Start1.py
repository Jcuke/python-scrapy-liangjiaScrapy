# -*- coding: utf-8 -*-
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from spiders.LianjiaSpider import LianjiaSpider

spider = LianjiaSpider()  # 这里改为你的爬虫类名
# settings = get_project_settings()
# crawler = CrawlerProcess(settings)
# crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
# crawler.configure()
# crawler.crawl(spider)
# crawler.start()
# log.start()
# reactor.run()



process = CrawlerProcess(get_project_settings())
process.crawl(spider, domain='wh.lianjia.com')
process.start()
