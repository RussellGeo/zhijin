# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from spider.items import NewsMeta, NewsContent
from spider.utils import *
from spider.mongo import mongo_helper

class RfiNewsSpider(scrapy.Spider):
    name = "rfi"
    site = u''
    allowed_domains = ["rfi.fr"]
    base_url = "http://m.cn.rfi.fr"
    start_urls = [
            "http://m.cn.rfi.fr/"
    ]

    hheaders = {
        #"authority":"www.voachinese.com",
        #"method":"GET",
        #"path":"/search_product.htm?sort=d&q=apple",
        #"scheme":"https",
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "accept-encoding":"gzip, deflate, sdch, br",
        #"accept-language":"zh-CN,zh;q=0.8",
        "upgrade-insecure-requests":"1",
        "Cache-control":"max-age=0",
        #"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36",
        "referer":"http://m.cn.rfi.fr/",
    }

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        news_list = soup.find_all("h3", class_="desc")
        items = []
        for news in news_list:
            try:
                a = news.find("a")
                print "href", a.get('href'), type(a.get('href'))
                item = NewsMeta()
                item["site"] = self.site
                item["url"] = self.base_url + a.get('href')
                item["title"] = a.string
                item["datetime"] = now_datetime()

                if mongo_helper.news_url_exists(item['url']):
                    print "news exists", item['url'], item['title']
                    #continue

                print item
                #items.append(item)

                req = scrapy.Request(url = item["url"], headers = self.hheaders, callback=self.parse_content)
                req.meta['url'] = item['url']
                req.meta['title'] = item['title']

                yield req
                break
            except Exception as e:
                print e, "|||",  news
                continue
        #return items

    def parse_content(self, response):
        print "parse content"
        soup = BeautifulSoup(response.body, 'lxml')
        items = []
        try:
            content = soup.find("div", class_="bd")
            print "c===", content
            print "string === ", content.text

            item = NewsMeta()
            item["site"] = self.site
            item["url"] = response.meta['url']
            item["title"] = response.meta['title']
            item["datetime"] = now_datetime()
            item["crawled"] = 1
            item["content"] = content.text

            items.append(item)
        except Exception as e:
            print e, "|||", response.body

        return items
        pass



