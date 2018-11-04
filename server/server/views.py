# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

import utils
from redis_util import redis_con

from mongo import mongo_helper
import json
import time
import random

seq = 0
# internal function

data_map = {}

def _showed(token, newsid):
    return redis_con.sismember(token, newsid)

def _showing(token, newsid):
    redis_con.sadd(token, newsid)
    redis_con.expire(token, 7*24*3600)

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

def _get_sort_key(news):
    return news['score']

def _calc(news_list, num = 10):
    news_list.sort(key = _get_sort_key, reverse = True)
    return news_list[0:10]
    pass

def _get_news_from_mongo(token, num = 10):
    cur = mongo_helper.find('news_meta').sort("datetime", -1)
    ret = []
    candidate_num = num * 10
    for x in cur:
        if token and _showed(token, x['newsid']):
            continue
            pass
        news = {}
        news['src'] = x['url']
        news['fallbackSrc'] = 'none'
        news['title'] = x['title']
        desc = x.get('desc', '')
        if len(desc) == 0 and len(x['title']) >= 20:
            desc = x['title']
        #news['desc'] = '' if 'desc' not in x else x['desc']
        news['desc'] = desc
        news['newsid'] = x['newsid']
        news['score'] = x.get('score', 5)
        if 'crawled' in x and x['crawled'] == 1:
            news['url'] = '/detail?news_id=' + x['newsid']
        else:
            news['url'] = '/'

        news['meta'] = {'source': x['site'], 'date': x['datetime'][:16], 'other': ''}
        ret.append(news)
        #_showing(token, x['newsid'])
        candidate_num -= 1
        if candidate_num <= 0:
            break
    news_ret = random.sample(ret, len(ret))
    news_ret = _calc(news_ret)
    for news in news_ret:
        _showing(token, news['newsid'])

    return news_ret

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

def reorder(news_list):
    return random.sample(news_list, len(news_list))
    pass

def get_news(request):
    token = _get_token(request)
    callback = _get_callback(request)
    print "token", token
    #news_list = _gen_data(token)
    news_list = _get_news_from_mongo(token)
    news_list = reorder(news_list)
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

    cur = mongo_helper.find('news_meta', {'newsid': news_id})
    news = {}
    for x in cur:

        news['src'] = x['url']
        news['fallbackSrc'] = 'none'
        news['title'] = x['title']
        news['desc'] = ''
        if 'crawled' in news and news['crawled'] == 1:
            news['url'] = '/detail?news_id=' + x['newsid']
        else:
            news['url'] = '/'

        news['meta'] = {'source': x['site'], 'date': x['datetime'][:16], 'other': ''}
        news['content'] = x['content']

    print 'news_id', news_id, callback, news
    res = HttpResponse("%s(%s)" % (callback, json.dumps({'retcode':0, 'errmsg':'', 'data':news})))
    #res["Access-Control-Allow-Origin"] = "*"
    return res


