import scrapy
from bs4 import BeautifulSoup
from spider.items import NewsMeta
from spider.utils import *

class FortunechinaSpider(scrapy.Spider):
    name = "fortunechina"
    site = u'财富中文网'
    allowed_domains = ["fortunechina.com"]
    base_url = "http://app.fortunechina.com/mobile/"
    start_urls = [
        "http://app.fortunechina.com/mobile/"
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



