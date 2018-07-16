from django.shortcuts import render
from requests_oauthlib import OAuth1Session
import requests   # Web からデータを取ってくる時に使う
import bs4        # スクレイピング
import json
from twitter import *

AT='825188365007872000-af18jBAUI5BOkiqTWrbpX28WhKA0CrL'
AS='y3ZSkUiMK60t5wmLoTcNsyMjw7sj4oHJS2kuvwfOeQj5s'
CK='jqbmCibEoOjahpBVBMuWG0km6'
CS='WKgRlgCuDl80bMbY1YwozZdztIt9mceahBNX2pnU3f9wqqy0zy'
twitter = OAuth1Session(CK, CS, AT, AS)

def appmain(request):
	url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

	params ={'count' : 1}
	req = twitter.get(url, params = params)

	if req.status_code == 200:
		timeline = json.loads(req.text)
		for tweet in timeline:
			#print(tweet['text'])
			#print('----------------------------------------------------')
			s=tweet['text']
	else:
		print("ERROR: %d" % req.status_code)
    
    return render(request, '.html', {
        'tw_1' : s,
    })
