import requests
import json
import os
from os import path


def new_video_check(uid):
    current_path = os.getcwd()
    video_data = {}
    fetch_data_url = 'http://api.bilibili.com/x/space/arc/search'
    param = {
        'mid': uid,
        'order': 'pubdate',
        'pn': '1',
        'ps': '1'
    }
    reply = requests.get(fetch_data_url, params=param).text
    title = json.loads(reply)['data']['list']['vlist'][0]['title']
    av = json.loads(reply)['data']['list']['vlist'][0]['aid']
    reply = {}
    reply['title'] = title
    reply['av'] = av
    
    if path.isfile(current_path + '\last_video_fetched%s.json'%uid):
        with open(current_path + '\last_video_fetched%s.json'%uid, 'r') as saved_data:
            video_data = json.load(saved_data)
            if video_data['av'] != av or video_data['title'] != title:
                video_data['title'] = title
                video_data['av'] = av
                video_data['updated'] = True
                print('updating data for %s'%uid)
            else:
                video_data['updated'] = False
                print('no new video found under %s'%uid)
        with open(current_path + '\last_video_fetched%s.json'%uid, 'w') as saved_data:
            json.dump(video_data, saved_data)
    else:
        with open(current_path + '\last_video_fetched%s.json'%uid, 'w') as saved_data:
            video_data['title'] = title
            video_data['av'] = av
            video_data['updated'] = True
            json.dump(video_data, saved_data)
            print('creating new record for %s'%uid)
    return video_data
