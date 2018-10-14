# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

import pymongo
import json
import time

seq = 0
# internal function
def _gen_data(num = 2):
    global seq
    ret = []
    seq += 1
    for i in xrange(num):
        t = str(seq)
        news = {
                'src': 'src sss',
                'fallbackSrc': 'fallbackSrc aa',
                'title': 'title aa' + t,
                'desc': 'desc aa',
                'url': '/url1',
                'meta': {
                    'source': 'source1',
                    'date': 'date1',
                    'other': 'other1'
                    }
                }
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


