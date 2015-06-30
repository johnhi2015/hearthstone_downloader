#!/usr/bin/env python3.4

import requests, math, json, os

_query_url = 'http://www.hearthstone.com.cn/cards/query'
_param1 = 'cardClass'
_param2 = 'p'

r = requests.get(_query_url)
rj = r.json()

#创建文件夹
dir = 'hearthstone'
if not os.path.exists(dir):
	print('创建文件夹     '+dir)
	os.mkdir(dir)

page_size = rj['pageSize']
for (key, value) in rj['totalPerClass'].items():
	count = 0
	print('\n\n\n开始处理     '+key)
	
	#创建文件夹
	dir = dir + r'/' + key
	if not os.path.exists(dir):
		print('创建文件夹     '+key)
		os.mkdir(dir)
		
	#配置页参数
	total = float(value)
	total = math.ceil(total / float(page_size))
	
	#获取json
	card_json_list = []
	for page in range(1, total+1):
		print('\n开始获取页数 ' + str(page) + r'/' + str(total))
		params = {}
		params[_param1]=key
		params[_param2]=page
		r = requests.get(_query_url, params=params)
		rj = r.json()
		
		card_list = rj['cards']
		
		#暂存当页字典
		card_json_list.extend(card_list)

		#下载图片
		for card in card_list:
			if card['golden'] == 1:
				img_url = card['imageUrl']
				img_dir = dir + r'/' + card['name'] + '-golden' + os.path.splitext(img_url)[1]
				if not os.path.exists(img_dir):
					count += 1
					print('(%d/%s)  下载图片: %s golden size' %(count, str(int(value)*2), card['name']))
					r = requests.get(img_url)
					with open(img_dir, 'wb') as file:
						file.write(r.content)
					
				img_url = img_url.replace(r'/g-cards/', r'/l-cards/g-cards/')
				img_dir = dir + r'/' + card['name'] + '-high-golden' + os.path.splitext(img_url)[1]
				if not os.path.exists(img_dir):
					count += 1
					print('(%d/%s)  下载图片: %s high golden size' %(count, str(int(value)*2), card['name']))
					r = requests.get(img_url)
					with open(img_dir, 'wb') as file:
						file.write(r.content)
			else:
				img_url = card['imageUrl']
				img_dir = dir + r'/' + card['name'] + os.path.splitext(img_url)[1]
				if not os.path.exists(img_dir):
					count += 1
					print('(%d/%s)  下载图片: %s normal size' %(count, str(int(value)*2), card['name']))
					r = requests.get(img_url)
					with open(img_dir, 'wb') as file:
						file.write(r.content)
				img_url = img_url.replace(r'/cards/', r'/l-cards/cards/')
				img_dir = dir + r'/' + card['name'] + '-high' + os.path.splitext(img_url)[1]
				if not os.path.exists(img_dir):
					count += 1
					print('(%d/%s)  下载图片: %s high size' %(count, str(int(value)*2), card['name']))
					r = requests.get(img_url)
					with open(img_dir, 'wb') as file:
						file.write(r.content)
			
	#保存字典
	json_str = json.dumps(card_json_list, indent=2)
	json_str_path = dir+'.json'
	if not os.path.exists(json_str_path):
		print('保存字典信息')
		with open(json_str_path, 'wb') as file:
			file.write(bytes(json_str, 'utf8'))	
			