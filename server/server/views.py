# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

import pymongo
import json

def test(request):
    #a = request.GET['a']
    #b = request.GET['b']
    return HttpResponse("teset response111")

def get_news(request):

    news_1 = {
            'src': 'src sss',
            'fallbackSrc': 'fallbackSrc aa',
            'title': 'title aa',
            'desc': 'desc aa',
            'url': '/url'
            }
    news_2 = {
            'src': '2src sss',
            'fallbackSrc': '2fallbackSrc aa',
            'title': '2title aa',
            'desc': 'desc aa',
            'url': '/url',
            'meta': {
                'source': 'source',
                'date': 'date',
                'other': 'other'
                }
            }
    ret = [news_1, news_2]
    return HttpResponse(json.dumps(ret))
