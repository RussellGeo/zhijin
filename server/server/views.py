# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

import utils
from redis_util import redis_con

from mongo import mongo_helper
import json
import time

seq = 0
# internal function

data_map = {}

def _showed(token, newsid):
    return redis_con.sismember(token, newsid)

def _showing(token, newsid):
    return redis_con.sadd(token, newsid)

def _gen_data(token, num = 5):
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

def _get_news_from_mongo(token, num = 10):
    cur = mongo_helper.find('news_meta')
    ret = []
    for x in cur:
        if token and _showed(token, x['newsid']):
            continue
            pass
        news = {}
        news['src'] = x['url']
        news['fallbackSrc'] = 'none'
        news['title'] = x['title']
        news['desc'] = ''
        if 'crawled' in news and news['crawled'] == 1:
            news['url'] = '/detail?news_id=' + x['newsid']
        else:
            news['url'] = '/'

        news['meta'] = {'source': x['source'], 'date': x['datetime'], 'other': ''}
        ret.append(news)
        _showing(token, x['newsid'])
        num -= 1
        if num <= 0:
            break
    return ret

def _cookie_auth(request):
    if 'token' not in request.COOKIES:
        return False
    return redis_con.exists(request.COOKIES['token'])

def _get_token(request):
    token = request.COOKIES.get("token", None)
    if not token:
        token = utils.create_id()
        print 'created token', token
    return token

def _get_callback(request):
    return request.GET.get("callback", None)


# api
def test(request):
    #a = request.GET['a']
    #b = request.GET['b']
    return HttpResponse("teset response111")

def get_news(request):
    token = _get_token(request)
    callback = _get_callback(request)
    print "token", token
    #news_list = _gen_data(token)
    news_list = _get_news_from_mongo(token)
    data = {'retcode': 0, 'errmsg': ""}
    data['data'] = json.dumps(news_list)

    res = None
    if callback:
        res = HttpResponse("%s(%s)" % (callback, json.dumps(data)))
    else:
        res = HttpResponse(json.dumps(data))
    #res["Access-Control-Allow-Origin"] = "106.12.124.186:8080"
    res.set_cookie('token', token)
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


