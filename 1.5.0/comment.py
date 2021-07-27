import requests
import json

def comment(video_data,auth,login_data):
    if auth['auth']==True:
        comment_url = 'http://api.bilibili.com/x/v2/reply/add'
        params = {
            'type': '1',
            'oid': video_data['av'],
            'message': auth['comment'],
            'csrf': login_data['csrf'],
            'SESSDATA':login_data['sessdata']
        }
        cookie={
            'SESSDATA':login_data['sessdata']
        }
        text=requests.post(comment_url,params=params,cookies=cookie).text
        text=json.loads(text)
        if text['data']['success_toast']=='发送成功':
            print('you said %s'%auth['comment'])
        else:
            print('comment failed')
            print(text)
    else:
        print('you have no access to it')