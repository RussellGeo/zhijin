# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from spider.items import NewsMeta
from spider.utils import *

class JiemianNewsSpider(scrapy.Spider):
    name = "jiemian"
    site = u'界面'
    allowed_domains = ["jiemian.com"]
    base_url = "https://m.jiemian.com/"
    start_urls = [
            "https://m.jiemian.com"
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        clist = soup.find_all("div", class_="news-header")
        items = []
        for news in clist:
            try:
                a = news.find("a")
                print "href", a.get('href'), type(a.get('href'))
                item = NewsMeta()
                item["site"] = self.site
                item["url"] = a.get('href')
                item["title"] = a.string
                item["datetime"] = now_datetime()
                items.append(item)
            except Exception as e:
                print e, "|||",  news
                continue
        return items



