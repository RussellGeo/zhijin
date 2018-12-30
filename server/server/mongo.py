import pymongo
import logging

class PymongoHelper(object):
    def __init__(self, db_name, address = "mongodb://localhost:27017/"):
        print "pymongohelper init"

        self.client = pymongo.MongoClient()
        self.db = self.client[db_name]
        self.topic_db = self.client['Topic']

    def find(self, table, params = None):
        if params:
            return self.db[table].find(params)
        else:
            return self.db[table].find()

    def test(self):

        #r = mycol.find({'newsid':'73f0793fdc84fa8d23c15834555d3501'})
        r = self.find('news_meta')
        print r.count()
        for x in r:
           print type(x), x['title']

    def insert_user(self, data):
        self.topic_db['UserInfo'].insert(data)

    def insert_topic(self, data):
        self.topic_db['TopicInfo'].insert(data)

    def update_topic(self, query, data):
        self.topic_db['TopicInfo'].update_one(query, data)

    def find_users(self, params = None):
        if params:
            return self.topic_db['UserInfo'].find(params)
        else:
            return self.topic_db['UserInfo'].find()

    def find_topics(self, params = None):
        if params:
            return self.topic_db['TopicInfo'].find(params)
        else:
            return self.topic_db['TopicInfo'].find()





mongo_helper = PymongoHelper('News')


