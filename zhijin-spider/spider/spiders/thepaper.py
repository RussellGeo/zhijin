# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from spider.items import NewsMeta
from spider.utils import *

class ThepaperNewsSpider(scrapy.Spider):
    name = "thepaper"
    site = u'澎湃'
    allowed_domains = ["thepaper.cn"]
    base_url = "https://m.thepaper.cn/"
    start_urls = [
            "https://m.thepaper.cn/"
    ]

    score = [5,5,4,4,4,3,3,3,3,2]
    index = 0

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        clist = soup.find_all("div", class_="txt_t")
        items = []
        for news in clist:
            try:
                a = news.find("a")
                print "href", a.get('href'), type(a.get('href'))
                item = NewsMeta()
                item["site"] = self.site
                item["url"] = self.base_url + a.get('href')
                item["title"] = a.string
                item["datetime"] = now_datetime()

                item["score"] = self.score[self.index]
                self.index = min(len(self.score) - 1, self.index + 1)

                items.append(item)
            except Exception as e:
                print e, "|||",  news
                continue
        return items



