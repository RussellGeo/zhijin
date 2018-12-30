# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

import utils
from redis_util import redis_con

from mongo import mongo_helper
import json
import time
import random
import copy
import hashlib

def _create_id(data):
    return hashlib.md5(str(data)).hexdigest()

seq = 0
# internal function

data_map = {}

def timestr():
    global seq
    seq += 1
    return str(time.time() * 1000 + seq)

def _gen_topic_id(data = None):
    data = str(data) + timestr()
    return _create_id(data)

def _gen_user_id(data = None):
    return _gen_topic_id(data)

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

def _get_topic_list(pos, num):
    i = 0
    l = []
    while i < num:
        t = {}
        t['topicid'] = 11 + i
        t['title'] = "topic title"
        t['desc'] = "topic desc"
        t['option_num'] = 2
        t['options'] = [{'op':'option 1', 'value':11}, {'op':'option 2', 'value':99}]
        l.append(l)
    return l
    pass

# param = {title, desc, options, deadline, ref, pubdate}
def _create_topic(topic):
    data = {
            'topicid': _gen_topic_id(),
            'title': topic['title'],
            'desc': topic['desc'],
            'deadline': topic['deadline'],
            'pubdate': topic['pubdate'],
            'unit': 1,
            'source': 'official',
            'create_timestamp': int(time.time()),
            'vote_sum': 0,
            'options': json.dumps(topic['options']) if type(topic['options']) != str else topic['options'],
            'ref': json.dumps([]),
            'tags': json.dumps([]),
            'show': 0,
            'click': 0,
            'participate': 0,
            }
    mongo_helper.insert_topic(data)
    return data
    pass

def _get_topics(pos = 0, num = 10):
    cur = mongo_helper.find_topics().sort("create_timestamp", -1)
    res = []
    i = 0
    for x in cur:
        if i < pos:
            i += 1
            continue
        if i - pos > num:
            break
        xx = copy.deepcopy(x)
        xx.pop('_id')
        res.append(xx)
    return res

def _get_topic_detail(topicid):
    cur = mongo_helper.find_topics({'topicid': topicid})

    t = {}
    for x in cur:
        t = copy.deepcopy(x)
        t.pop('_id')
    return t

def _topic_vote(topicid, op_index):
    cur = mongo_helper.find_topics({'topicid': topicid})
    for x in cur:
        t = copy.deepcopy(x)
        options = json.loads(t['options'])
        t['vote_sum'] += 1
        options[op_index]['vote'] += 1
        s = 0
        for index in range(len(options)):
            if index == len(options) -1:
                options[index]['value'] = 100 - s
                continue
            options[index]['value'] = int(round(float(options[index]['vote']) / t['vote_sum'], 2) * 100)
            s += options[index]['value']
        mongo_helper.update_topic({'topicid': topicid}, {'$set': {'options': json.dumps(options)}})
        mongo_helper.update_topic({'topicid': topicid}, {'$set': {'vote_sum': t['vote_sum']}})

def _register(info):
    res = mongo_helper.find_users({'username': info['username']})
    if res.count() > 0:
        return False, "username " + info['username'] + u" 已经存在!!!"

    res = mongo_helper.find_users({'phone': info['phone']})
    if res.count() > 0:
        return False, "phone" + info['phone'] + u" 已经注册!!!"

    user_id = _gen_user_id()
    data = {
            'username':  info['username'],
            'user_id':  str(user_id),
            'phone': info['phone'],
            'email': info['email'],
            'password': info['password'],
            'timestamp': int(time.time()),
            'total': 0.0,
            'available': 0.0,
            'locking': 0.0,
            'withdrawing': 0.0,
            }
    mongo_helper.insert_user(data)

    return True, {'user_id': data['user_id'], 'phone': data['phone'], 'username': data['username'], 'total':data['total'], 'available':data['available'], 'locking':data['locking'], 'withdrawing':data['withdrawing']}

def _login(info):
    param = {
            'phone': info['phone']
            }
    res = mongo_helper.find_users(param)
    if res.count() == 0:
        return False, u"用户" + info['phone'] + u" 不存在"

    for x in res:
        if x['password'] == info['password']:
            #return True, {'user_id': x['user_id'], 'phone': x['phone'], 'username': x['username']}

            return True, {'user_id': x['user_id'], 'phone': x['phone'], 'username': x['username'], 'total':x['total'], 'available':x['available'], 'locking':x['locking'], 'withdrawing':x['withdrawing']}
    return False, u"密码错误"


def _GETPOST(req, key):
    if key in req.GET:
        return req.GET[key]
    if key in req.POST:
        return req.POST[key]
    return None

def _get_req_params(req):
    d = {}
    for k in req.GET:
        d[k] = req.GET[k]
    for k in req.POST:
        d[k] = req.POST[k]
    return d

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

# param = {pos:0, num:10}
#ret = {retcode,errmsg}
def get_topic(request):
    callback = _get_callback(request)
    print 'get topic'

    pos = int(request.GET['pos']) if 'pos' in request.GET else 0
    num = int(request.GET['num']) if 'num' in request.GET else 10

    data = _get_topic_list(pos, num)

    ret = {'retcode':0, 'errmsg':'', 'data': json.dumps(data)}

    res = None
    if callback:
        res = HttpResponse("%s(%s)" % (callback, json.dumps(ret)))
    else:
        res = HttpResponse(json.dumps(ret))

    return res

def topiclist(request):
    callback = _get_callback(request)
    print 'get topic'

    pos = int(request.GET['pos']) if 'pos' in request.GET else 0
    num = int(request.GET['num']) if 'num' in request.GET else 10

    data = _get_topics(pos, num)
    print data
    ret = {'retcode':0, 'errmsg':'', 'data': json.dumps(data)}

    res = None
    if callback:
        res = HttpResponse("%s(%s)" % (callback, json.dumps(ret)))
    else:
        res = HttpResponse(json.dumps(ret))
    return res


# param = {topicid:"", }
#ret = {retcode,errmsg}
def get_topic_detail(request):
    callback = _get_callback(request)

    topicid = _GETPOST(request, 'topicid')
    t = _get_topic_detail(topicid)
    ret = {'retcode':0, 'errmsg':'', 'data':json.dumps(t)}
    if callback:
        return HttpResponse("%s(%s)" % (callback, json.dumps(ret)))
    else:
        return HttpResponse(json.dumps(ret))

# param = {title, desc, options, deadline, ref, pubdate}
#ret = {retcode,errmsg}
def create_topic(request):
    callback = _get_callback(request)
    option1 = _GETPOST(request, 'option1')
    option2 = _GETPOST(request, 'option2')
    option3 = _GETPOST(request, 'option3')
    option4 = _GETPOST(request, 'option4')
    errmsg = ''
    if option1 is None or option2 is None or (not option3 and option4):
        errmsg = u'选项创建错误'

    options = [{'option': option1, 'value':0, 'index': 0, 'vote': 0}, {'option': option2, 'value':0, 'index': 1, 'vote': 0}]
    if option3:
        options.append({'option':option3, 'value':0, 'index': 2, 'vote': 0})
        if option4:
            options.append({'option':option4, 'value':0, 'index': 3, 'vote': 0})

    info = {
            'title': _GETPOST(request, 'title'),
            'desc': _GETPOST(request, 'desc'),
            'pubdate': _GETPOST(request, 'pubdate'),
            'deadline': _GETPOST(request, 'deadline'),
            'options': json.dumps(options)
            }

    check = True
    lack = None
    for i in info:
        if info[i] is None:
            check = False
            lack = i
    ret = {'retcode':0, 'errmsg':'', 'data': ''}
    if check and len(errmsg) == 0:
        data = _create_topic(info)
        data.pop('_id')
        ret['data'] = json.dumps(data)
    else:
        ret['retcode'] = 1
        ret['errmsg'] = u'创建失败，缺少' + str(lack)
        if len(errmsg) > 0:
            ret['errmsg'] = errmsg
    if callback:
        return HttpResponse("%s(%s)" % (callback, json.dumps(ret)))
    else:
        return HttpResponse(json.dumps(ret))


#param = {username,phone,password,email}
#ret = {retcode,errmsg}
def register(request):
    callback = _get_callback(request)
    info = {
            'phone': _GETPOST(request, 'phone'),
            'username': _GETPOST(request, 'username'),
            'password': _GETPOST(request, 'password'),
            'email': _GETPOST(request, 'email'),
            }

    ret = {'retcode':0, 'errmsg':'', 'data':''}
    status, msg = _register(info)
    if status:
        ret['data'] = json.dumps(msg)
    else:
        ret['retcode'] = 1
        ret['errmsg'] = msg
    if callback:
        return HttpResponse("%s(%s)" % (callback, json.dumps(ret)))
    else:
        return HttpResponse(json.dumps(ret))

#param = {username,phone,password}
#ret = {retcode,errmsg}
def login(request):
    callback = _get_callback(request)
    phone = _GETPOST(request, 'phone')
    password = _GETPOST(request, 'password')

    ret = {'retcode':0, 'errmsg':'', 'data':''}

    if phone and password:
        info = {
                'phone': phone,
                'password': password,
                }
        status, msg = _login(info)
        if not status:
            ret['retcode'] = 1
            ret['errmsg'] = msg
        else:
            ret['data'] = json.dumps(msg)
    else:
        ret['retcode'] = 2
        ret['errmsg'] = 'must need both phone and password'

    if callback:
        return HttpResponse("%s(%s)" % (callback, json.dumps(ret)))
    else:
        return HttpResponse(json.dumps(ret))

def topic_vote(request):
    callback = _get_callback(request)

    topicid = _GETPOST(request, 'topicid')
    op_index = _GETPOST(request, 'op_index')

    if topicid and op_index:
        _topic_vote(topicid, int(op_index))
    ret = {'retcode':0, 'errmsg':'', 'data': ''}

    res = None
    if callback:
        res = HttpResponse("%s(%s)" % (callback, json.dumps(ret)))
    else:
        res = HttpResponse(json.dumps(ret))
    return res


