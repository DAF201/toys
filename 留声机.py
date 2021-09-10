



# 为什么有些地方看起来这么傻逼呢？因为我写完了以后才发现阿B评论上限1000，而好死不死得我又是条懒狗不想改太多了
#why does it looks so stupid somewhere? because I realized there is a word limit of comments after I finished, and I just don't want to change the whole.

#update:
#Banned by bilibili, nothing will be sent out. Other users will not see the content you sent, even the server replies you with a status code 0.


import requests
import json
import re
import time
import random
AT_CHECK_URL = 'https://api.bilibili.com/x/msgfeed/unread'
AT_ADDRESS_URL = 'https://api.bilibili.com/x/msgfeed/at?build=0&mobi_app=web'
REPLY_URL = 'https://api.bilibili.com/x/v2/reply/add'
GET_VIDEO_LIST = 'https://api.bilibili.com/x/player/pagelist'


def download_url(av):

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
               'cookie': "SESSDATA:%s" % ''
               }
    reply_data = []

    def get_info(av):
        collection = {}
        list_info = get_parts(av)
        for x in list_info['data']:
            collection[x['part']] = [x['cid'], x['page'], x['part']]
        for x in collection:
            target_url = 'https://www.bilibili.com/video/av%s?p=%s' % (
                av, collection[x][1])
            download(target_url, x)
            break
        time.sleep(random.randrange(5, 20))
        return reply_data

    def get_parts(av):
        list_params = {
            'aid': av
        }
        info = requests.get(GET_VIDEO_LIST, params=list_params).text
        info = json.loads(info)
        return info

    def download(target_url, part_name):
        res = requests.get(target_url, headers=headers)
        video_pattern = '__playinfo__=(.*?)</script><script>'
        playlist_info = json.loads(re.findall(video_pattern, res.text)[0])
        video_url = playlist_info['data']['dash']['video'][0]['baseUrl']
        audio_url = playlist_info['data']['dash']['audio'][0]['baseUrl']
        reply_data.append(video_url)
        reply_data.append(audio_url)
    return get_info(av)


def get_at_info():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    cookie = {
        
    }

    raw = requests.get(
        AT_CHECK_URL, headers=headers, cookies=cookie).text
    at_count = int(json.loads(raw)['data']['at'])
    time.sleep(random.randrange(2, 8))
    if at_count > 0:
        get_at_url(at_count)


def get_at_url(times):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    cookie = {
        
    }
    raw = requests.get(AT_ADDRESS_URL, headers=headers, cookies=cookie).text
    for x in range(0, times):
        message = {}
        if 'av' or 'AV' in json.loads(raw)['data']['items'][x]['item']['uri']:
            message['type'] = '1'
        if 'bv' or 'BV' in json.loads(raw)['data']['items'][x]['item']['uri']:
            message['type'] = '1'
        else:
            message['type'] = '0'
        message['oid'] = json.loads(
            raw)['data']['items'][x]['item']['subject_id']
        message['user'] = json.loads(
            raw)['data']['items'][x]['user']['nickname']
        reply1(message)
        reply2(message)
    time.sleep(random.randrange(0, 30))


def reply1(message):
    params = {
        'type': '1',
        'oid': message['oid'],
        'message': '@%s 视频:%s' % (message['user'], download_url(message['oid'])[0]),
        'csrf': ''
    }
    cookie = {
        
    }
    requests.post(REPLY_URL, params=params, cookies=cookie)
    time.sleep(random.randrange(5, 75))


def reply2(message):
    params = {
        'type': '1',
        'oid': message['oid'],
        'message': '@%s 音频:%s' % (message['user'], download_url(message['oid'])[1]),
        'csrf': ''
    }
    cookie = {
        
    }
    requests.post(REPLY_URL, params=params, cookies=cookie)
    time.sleep(random.randrange(6, 24))


def main():
    start = time.time()
    while(True):
        get_at_info()
        time.sleep(random.randrange(0, 120))
        end = time.time()
        if end-start > 28800:
            start = end
            time.sleep(57600)


if __name__ == '__main__':
    main()
