# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from spider.items import NewsMeta
from spider.utils import *

class FortunechinaSpider(scrapy.Spider):
    name = "fortunechina"
    site = u'财富中文网'
    allowed_domains = ["fortunechina.com"]
    base_url = "http://app.fortunechina.com/"
    start_urls = [
        "http://app.fortunechina.com/mobile/"
    ]

    score = [6,6,6,5,5,5,5,4,4,4,4,4,3]
    index = 0

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        clist = soup.find_all("dl", class_="newslist")
        items = []
        for center in clist:
            news_list = center.find_all("dt")
            for news in news_list:
                a = news.find("a")
                try:
                    print "href", a.get('href'), type(a.get('href'))
                    item = NewsMeta()
                    item["site"] = self.site
                    item["url"] = self.base_url + a.get('href')
                    item["title"] = a.string
                    item["datetime"] = now_datetime()
                    item["score"] = self.score[self.index]
                    self.index = min(len(self.score) - 1, self.index + 1)
                    #print item
                    items.append(item)
                except Exception as e:
                    print e, "|||",  news
                    continue
        return items



