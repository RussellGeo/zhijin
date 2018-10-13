# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from spider.items import NewsMeta
from spider.utils import *

class DapentiNewsSpider(scrapy.Spider):
    name = "dapenti"
    site = u'打喷嚏'
    allowed_domains = ["dapenti.com"]
    base_url = "http://www.dapenti.com/blog/"
    start_urls = [
        "http://www.dapenti.com/blog/indexforweb.asp"
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        clist = soup.find_all("div", class_="center_title_down")
        items = []
        for center in clist:
            news_list = center.find_all("li")
            for news in news_list:
                a = news.find("a")
                try:
                    print "href", a.get('href'), type(a.get('href'))
                    item = NewsMeta()
                    item["site"] = self.site
                    item["url"] = self.base_url + a.get('href')
                    item["title"] = a.get('title')
                    item["datetime"] = now_datetime()
                    items.append(item)
                except Exception as e:
                    print e, "|||",  news
                    continue
        return items



