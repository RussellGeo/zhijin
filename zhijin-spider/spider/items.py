# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewsMeta(scrapy.Item):
    newsid = scrapy.Field()

    source = scrapy.Field()
    title = scrapy.Field()
    datetime = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
    keywords = scrapy.Field()
    desc = scrapy.Field()
    img = scrapy.Field()

    news_class = scrapy.Field()
    score = scrapy.Field()


class NewsContent(scrapy.Item):
    newsid = scrapy.Field()
    content = scrapy.Field()

