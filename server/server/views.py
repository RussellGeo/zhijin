# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

import pymongo
import json
import time

seq = 0
# internal function

data_map = {}

def _gen_data(num = 5):
    global seq
    global data_map
    ret = []
    for i in xrange(num):
        seq += 1
        t = str(seq)
        news = {
                'src': 'src sss',
                'fallbackSrc': 'fallbackSrc aa',
                'title': 'title aa' + t,
                'desc': 'desc aa',
                'url': '/detail?news_id=' + t,
                'meta': {
                    'source': 'source1',
                    'date': 'date1',
                    'other': 'other1'
                    },
                'content': 'content ' + t
                }
        data_map[t] = news
        ret.append(news)
    return ret


# api
def test(request):
    #a = request.GET['a']
    #b = request.GET['b']
    return HttpResponse("teset response111")

def get_news(request):
    news_list= _gen_data()
    data = {'retcode': 0, 'errmsg': ""}
    data['data'] = json.dumps(news_list)

    res = HttpResponse(json.dumps(data))
    res["Access-Control-Allow-Origin"] = "*"
    return res

def get_news_detail(request):
    global data_map
    news_id = request.GET['news_id']
    callback = request.GET['callback']
    news = data_map.get(news_id, None)
    news = news if news else ''

    print 'news_id', news_id, callback, news
    res = HttpResponse("%s(%s)" % (callback, json.dumps({'retcode':0, 'errmsg':'', 'data':news})))
    res["Access-Control-Allow-Origin"] = "*"
    return res


