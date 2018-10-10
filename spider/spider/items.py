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
    _id = scrapy.Field()
    show = scrapy.Field()
    source = scrapy.Field()

    site = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    datetime = scrapy.Field()
    keywords = scrapy.Field()
    content = scrapy.Field()

