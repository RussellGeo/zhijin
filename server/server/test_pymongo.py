#!/usr/bin/python3

import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

dblist = myclient.list_database_names()
# dblist = myclient.database_names()

for db in dblist:
    print db

mydict = { "name": "RUNOOB", "alexa": "10000", "url": "https://www.runoob.com" }

myclient['test']['test'].insert(mydict)
