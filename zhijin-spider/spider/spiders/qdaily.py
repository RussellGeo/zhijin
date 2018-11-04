# -*- coding: utf-8 -*-

import scrapy
import re
from bs4 import BeautifulSoup
from spider.items import NewsMeta
from spider.utils import *

class QdailyNewsSpider(scrapy.Spider):
    name = "qdaily"
    site = u'好奇心日报'
    allowed_domains = ["qdaily.com"]
    base_url = "http://m.qdaily.com"
    start_urls = [
        "http://m.qdaily.com/mobile/homes.html"
    ]

    score = [6,6,6,6,5,5,5,5,4,4,4,4,4,3]
    index = 0

    def parse(self, response):
        items = []
        soup = BeautifulSoup(response.body, 'lxml')

        clist = soup.find_all("a", class_=re.compile("swiper-slide*"))
        for news in clist:
            try:
                url = news.get('href')
                title = news.get('data-title')

                item = NewsMeta()
                item["site"] = self.site
                item["url"] = self.base_url + url
                item["title"] = title
                item["datetime"] = now_datetime()

                item["score"] = self.score[self.index]
                self.index = min(len(self.score) - 1, self.index + 1)

                print item
                items.append(item)
            except Exception as e:
                print e, "|||",  news
                continue


        clist = soup.find_all("a", class_="com-grid-article")
        for news in clist:
            try:
                url = news.get('href')
                title = news.find("h1").string

                item = NewsMeta()
                item["site"] = self.site
                item["url"] = self.base_url + url
                item["title"] = title
                item["datetime"] = now_datetime()

                item["score"] = self.score[self.index]
                self.index = min(len(self.score) - 1, self.index + 1)

                print item
                items.append(item)
            except Exception as e:
                print e, "|||",  news
                continue
        return items



