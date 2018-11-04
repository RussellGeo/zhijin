# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging
import spider.utils as utils

class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MongodbPipeline(object):

    newsmeta_collection_name = 'news_meta'
    mewscontent_collection_name = 'news_content'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item.__class__.__name__ == 'NewsMeta':
            item['newsid'] = utils.create_id(item['url'])
            item['news_class'] = "normal"
            item['source'] = spider.name

            print 'pipeline', item

            try:
                if self.db[self.newsmeta_collection_name].find({'newsid':item['newsid']}).count() == 0:
                    self.db[self.newsmeta_collection_name].insert(dict(item))
                else:
                    logging.info("duplicated url:" + item['url'])
            except Exception as e:
                logging.error("Alert(: mongodb insert error, exception:" + str(e))
        elif item.__class__.__name__ == 'NewsContent':
            pass
        else:
            print 'unknown', item.__class__.__name__
        return item

