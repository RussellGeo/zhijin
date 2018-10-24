# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from spider.items import NewsMeta
from spider.utils import *

class FtchineseSpider(scrapy.Spider):
    name = "ftchinese"
    site = u'FT中文网'
    allowed_domains = ["ftchinese.com"]
    base_url = "http://www.ftchinese.com"
    start_urls = [
        "http://www.ftchinese.com"
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        clist = soup.find_all("div", class_="item-inner")
        items = []
        for news in clist:
            print "====", news
            try:
                a = news.find("a", class_="item-headline-link")
                print "href", a.get('href'), type(a.get('href'))
                title = a.string
                href = a.get('href')
                img = None
                desc = None
                try:
                    img = news.find("img").get("src")
                    desc = news.find('div', class_='item-lead').string
                except:
                    pass

                item = NewsMeta()
                item["site"] = self.site
                item["url"] = self.base_url + href
                item["title"] = title
                item["datetime"] = now_datetime()
                item["desc"] = desc
                item["img"] = img
                print item
                #items.append(item)
            except Exception as e:
                print e, "|||",  news
                print "||||"
            break
        return items



