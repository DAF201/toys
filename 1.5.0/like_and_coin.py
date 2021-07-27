import requests
import json

def like_and_coins(video_data,login_data):
    check_coin_url='http://api.bilibili.com/x/web-interface/archive/coins'
    coin_url='http://api.bilibili.com/x/web-interface/coin/add'
    params_check={
        'aid':video_data['av']
    }
    params_like_and_coins={
        'aid':video_data['av'],
        'multiply':'2',
        'select_like':'1',
        'csrf':login_data['csrf']
    }
    cookie={
        'SESSDATA':login_data['sessdata']
    }
    reply=requests.get(check_coin_url,params=params_check,cookies=cookie).text
    reply=json.loads(reply)
    if reply['data']['multiply']==0:
        reply=requests.post(coin_url,params=params_like_and_coins,cookies=cookie).text
        reply=json.loads(reply)
        if reply['data']['like']==True:
            print('you give %s two coins and a like'%video_data['av'])
        else:
            print('fail to like the video')
            print(reply)
    else:
        print('you have give this video coins')