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
from pytz import timezone
import unicodedata
import string
from dateutil import parser
from collections import Counter

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
	params ={'count' : 10}#ツイート数
	url = "https://api.twitter.com/1.1/statuses/user_timeline.json?user_id=3195831606"
	req = twitter.get(url, params = params)
	soft = []
	img_lnk = ''
	if req.status_code == 200:
		timeline = json.loads(req.text)
		for tweet in (timeline):

			if r"【今日のソフト】" in tweet['text']:
				if "extended_entities" in tweet:
					img_lnk=tweet['extended_entities']['media'][0]['media_url']
				#if tweet['text'].find("今日のソフト")
				#テキストデータ作成
				match = re.search(r'【今日のソフト】\n?(.+)♪', tweet['text'])
				if match:
					tmp = match.group(1).replace('デラックス','DX');
					match = re.search(r'(.+)♪(.+)', tmp)
					while match:
						softcount = softcount + 1
						soft.append(format_text(match.group(2)))
						date.append(parser.parse(tweet['created_at']).astimezone(timezone('Asia/Tokyo')))
						tmp = match.group(1);
						match = re.search(r'(.+)♪(.+)', tmp)
					soft.append(format_text(tmp.strip('初登場')))
					#match = re.search(r'<b>(.+)</b>', 'This is a <b>nice</b> pen')
				break
	return render(request, 'app_13/main.html', {
		'soft' : soft,
		'img_lnk' : img_lnk,
	})

def soft(request):
	message = ""
	messagelist = []
	params ={'count' : 500}#ツイート数
	softcount = 1
	soft = []
	date = []
	img_lnk = []
	l_id = ''
	for i in range(1,10):
		url = "https://api.twitter.com/1.1/statuses/user_timeline.json?user_id=3195831606" + l_id
		req = twitter.get(url, params = params)
		if req.status_code == 200:
			timeline = json.loads(req.text)
			if not timeline:
				print('はらへった')
				break
			for tweet in (timeline):
				l_id = '&max_id='+tweet['id_str']
				if r"【今日のソフト】" in tweet['text']:

					#if tweet['text'].find("今日のソフト")
					#テキストデータ作成
					message = message + tweet['text'] + '\n\n'
					messagelist.append(html.unescape(tweet['text']))
					softcount = softcount + 1
					match = re.search(r'【今日のソフト】\n?(.+)♪', html.unescape(tweet['text']))
					if match:
						tmp = match.group(1).replace('デラックス','DX');
						match = re.search(r'(.+)♪(.+)', tmp)
						f = False
						while match:
							f = True
							softcount = softcount + 1
							soft.append(format_text(match.group(2)).strip('or').strip('です').strip(r'は '))
							date.append(parser.parse(tweet['created_at']).astimezone(timezone('Asia/Tokyo')))
							tmp = match.group(1);
							match = re.search(r'(.+)♪(.+)', tmp)
						else:
							if not f:
								match = re.search(r'(.+)or(.+)', tmp)
								while match:
									f = True
									softcount = softcount + 1
									soft.append(format_text(match.group(2)).strip('です').strip(r'は '))
									date.append(parser.parse(tweet['created_at']).astimezone(timezone('Asia/Tokyo')))
									tmp = match.group(1);
									match = re.search(r'(.+)or(.+)', tmp)
						soft.append(format_text(tmp.strip('初登場').strip('or').strip('です').strip(r'は ')))
						date.append(parser.parse(tweet['created_at']).astimezone(timezone('Asia/Tokyo')))
						#match = re.search(r'<b>(.+)</b>', 'This is a <b>nice</b> pen')

						#ここから画像処理


		#print(message),

		#ころすぞ

	counter = Counter(soft)



	return render(request, 'app_13/soft.html', {
	'messagelist' : messagelist,
	'softcount' : softcount,
	'soft_date' : zip(soft,date),
	'img_lnk' : img_lnk,
	'freq' : counter.most_common()
	})
