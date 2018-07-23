from django.shortcuts import render
from requests_oauthlib import OAuth1Session
import requests   # Web からデータを取ってくる時に使う
import json, os, codecs, io, sys
from twitter import *
import re
import html
import random
import requests
import warnings

import unicodedata
import string

def format_text(text):
    text = unicodedata.normalize("NFKC", text)  # 全角記号をざっくり半角へ置換（でも不完全）

    # 記号を消し去るための魔法のテーブル作成
    table = str.maketrans("", "", string.punctuation  + "「」、。・")
    text = text.translate(table)

    return text



warnings.filterwarnings("ignore", category=UnicodeWarning)
AT='825188365007872000-af18jBAUI5BOkiqTWrbpX28WhKA0CrL'
AS='y3ZSkUiMK60t5wmLoTcNsyMjw7sj4oHJS2kuvwfOeQj5s'
CK='jqbmCibEoOjahpBVBMuWG0km6'
CS='WKgRlgCuDl80bMbY1YwozZdztIt9mceahBNX2pnU3f9wqqy0zy'
twitter = OAuth1Session(CK, CS, AT, AS)

def appmain(request):
	message = ""
	messagelist = []
	params ={'count' : 30}#ツイート数
	url = "https://api.twitter.com/1.1/statuses/home_timeline.json?tweet_mode=extended"
	req = twitter.get(url, params = params)
	softcount = 1
	soft = []
	date = []

	if req.status_code == 200:
		timeline = json.loads(req.text)
		for tweet in (timeline):

			if r"【今日のソフト】" in tweet['full_text']:
				#if tweet['full_text'].find("今日のソフト")
				#テキストデータ作成
				message = message + tweet['full_text'] + '\n\n'
				messagelist.append(html.unescape(tweet['full_text']))
				softcount = softcount + 1
				match = re.search(r'【今日のソフト】\n?(.+)♪', tweet['full_text'])
				if match:
					tmp = match.group(1).replace('デラックス','DX');
					match = re.search(r'(.+)♪(.+)', tmp)
					while match:
						softcount = softcount + 1
						soft.append(format_text(match.group(2)))
						date.append(tweet['created_at'])
						tmp = match.group(1);
						match = re.search(r'(.+)♪(.+)', tmp)
					soft.append(format_text(tmp.strip('初登場')))
					date.append(tweet['created_at'])
					#match = re.search(r'<b>(.+)</b>', 'This is a <b>nice</b> pen')

					#ここから画像処理
				count = 1
				if "extended_entities" in tweet:
					for i in tweet['extended_entities']['media']:#画像数
						urls = i
						media_urls = urls['media_url']#画像のURLを取得
						downloads = requests.get(media_urls).content #画像のDL
						#ファイル名この真下
						images = open(tweet['user']["screen_name"] + "_" + tweet["id_str"] + '_' + str(count) + '.jpg', 'wb')
						images.write(downloads)
						images.close()
						count = count + 1

	#print(message),
	print(messagelist)
	print(softcount)
	print(soft)

	return render(request, 'app_13/main.html', {
	'messagelist' : messagelist,
	'softcount' : softcount,
	'soft_date' : zip(soft,date),
	})
