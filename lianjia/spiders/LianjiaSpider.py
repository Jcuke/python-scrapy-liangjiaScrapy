# -*- coding: utf-8 -*-
import chardet
import scrapy
import sys
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule, Request
from scrapy.selector import Selector
from lianjia.items import LianjiaItem

reload(sys)
sys.setdefaultencoding('utf-8')

class LianjiaSpider(scrapy.Spider):
    name = "s001"
    allowed_domains = ["wh.lianjia.com"]
    start_urls = ["http://wh.lianjia.com/ershoufang/"]
    rules = [
        # Rule(SgmlLinkExtractor(allow=(r'http://wh.lianjia.com/ershoufang/pg\d+/')), callback="parse_item")
        Rule(SgmlLinkExtractor(allow=(r'http://wh.lianjia.com/ershoufang/pg\d+/', r'http://wh.lianjia.com/ershoufang/\d+.html')), callback="parse_item")
    ]
    pageNo = 0
    def parse(self, response):
        sel = Selector(response)
        item = LianjiaItem()

        citys = []
        districts = []
        realEstateAgents = []
        ages = []
        houseTypes = []
        unitPrices = []
        prices = []
        residentialNames = []
        publicTimes = []
        acreages = []
        titles = []

        titles = sel.xpath('//*[@class="title"]/a/text()').extract()
        residentialNames = sel.xpath('//*[@class="houseInfo"]/a/text()').extract()

        propss = sel.xpath('//*[@class="houseInfo"]/text()').extract()
        for x in propss:
            houseTypes.append(x.split(' | ')[1])
            acreage = str(x.split(' | ')[2]).replace(unicode("平米", 'utf-8'),"")
            acreages.append(acreage)

        followInfos = sel.xpath('//*[@class="followInfo"]/text()').extract()
        for x in followInfos:
            publicTimeTemp = str(x).split(" / ")[2]
            if publicTimeTemp.find(unicode("个月以前发布", 'utf-8')) > -1:
                publicTime = publicTimeTemp.replace(unicode("个月以前发布", 'utf-8'), "")
                publicTime = int(publicTime) * 30
            else:
                publicTime = publicTimeTemp.replace(unicode("天以前发布", 'utf-8'), "")
            publicTimes.append(publicTime)

        prices = sel.xpath('//*[@class="totalPrice"]/span/text()').extract()
        unitPrices1 = sel.xpath('//*[@class="unitPrice"]/span/text()').extract()
        for x in unitPrices1:
            unitPrice = str(x).replace(unicode("单价", 'utf-8'), "").replace(unicode("元/平米", 'utf-8'), "")
            unitPrices.append(unitPrice)

        ages1 = sel.xpath('//div[@class="positionInfo"]/text()').extract()
        for x in ages1:
            age = str(x).split("  ")[1]
            ages.append(age)


        detailHrefs = sel.xpath('//*[@class="title"]/a/@href').extract()
        for index in range(len(titles)):
            item = LianjiaItem()
            item['title'] = titles[index]
            item['residentialName'] = residentialNames[index]
            item['houseType'] = houseTypes[index]
            item['acreage'] = acreages[index]
            item['publicTime'] = publicTimes[index]
            item['price'] = prices[index]
            item['unitPrice'] = unitPrices[index]
            item['age'] = ages[index].decode()
            yield Request(detailHrefs[index], meta={'item': item}, callback=self.parseHouseDetail)



        #yield item

        # nextlink = response.xpath('/html/body/div[4]/div[1]/div[5]/div[2]/div/a[1]/text()').extract()
        # print nextlink
        # if nextlink:
        #     link = nextlink[0]
        #     yield Request(self.url + link, callback=self.parse)

        xpage = "http://wh.lianjia.com/ershoufang/pgT/"
        self.pageNo = self.pageNo + 1
        xpage = xpage.replace("T", str(self.pageNo))
        self.start_urls[0] = xpage
        yield Request(self.start_urls[0], callback=self.parse)

        #yield Request('http://wh.lianjia.com/ershoufang/104100177724.html', meta={'item' : item}, callback=self.parseHouseDetail)

    def parseHouseDetail(self, response):
        item = response.meta['item']
        sel = Selector(response)
        item['district'] = sel.xpath('//div[@class="areaName"]/span[@class="info"]/a[1]/text()').extract()[0]
        #目前只保存一张图片
        item['imageUrl'] = []
        item['imageUrl'] = sel.xpath('//*[@class="list"]/div/img/@src').extract()
        return item

