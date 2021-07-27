import requests
import json
def sensative_comments(video_data):
        final = []
        user_uid = []
        content = []
        url = 'http://api.bilibili.com/x/v2/reply'
        params = {
            'type': '1',
            'oid': video_data['av'],
            'pn': '1',
            'ps': '49'
        }
        reply = requests.get(url, params=params).text
        reply = json.loads(reply)
        reply = reply['data']['replies']
        for x in reply:
            for y in ['魔怔', '路人', '珈乐是谁', '不熟', '恶心', '离谱', '塔塔开', 'ttk', '乐华', '嘻嘻嘻', '懂不懂', '资本', '厉害', '[吃瓜]', '[偷笑]', '[鼓掌]', '[星星眼]','机器人','战场']:
                if y in x['content']['message'].encode('utf-8').decode('utf-8'):
                    user_uid.append(x['member']['mid'])
                    content.append(x['content']['message'])
        final = dict(zip(user_uid, content))
        for key in final:
            print(key+'\n'+final[key]+'\n')
        with open('user_and_comments@%s.json'%video_data['av'], 'w') as file:
            json.dump(final, file)