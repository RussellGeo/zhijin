import pymongo
import logging

news_db = 'News'
news_meta_table = 'news_meta'

class PymongoHelper(object):
    def __init__(self, db_name, address = "mongodb://localhost:27017/"):
        print "pymongohelper init"

        self.client = pymongo.MongoClient()
        self.db = self.client[db_name]

        self.news_meta = news_meta_table

    def find(self, table, params = None):
        if params:
            return self.db[table].find(params)
        else:
            return self.db[table].find()

    def exists(self, table, params):
        cur = self.find(table, params)
        if cur.count() == 0:
            return False
        else:
            return True

    def news_meta_exists(self, params):
        return self.exists(self.news_meta, params)

    def test(self):

        #r = mycol.find({'newsid':'73f0793fdc84fa8d23c15834555d3501'})
        r = self.find('news_meta')
        print r.count()
        for x in r:
           print type(x), x['title']


mongo_helper = PymongoHelper(news_db)


