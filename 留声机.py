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
               'cookie': "SESSDATA:%s" % 'cb3a2f81%2C1642359109%2C65bbc%2A71'
               }
    reply_data = {}

    def get_info(av):
        collection = {}
        list_info = get_parts(av)
        for x in list_info['data']:
            collection[x['part']] = [x['cid'], x['page'], x['part']]
        for x in collection:
            target_url = 'https://www.bilibili.com/video/av%s?p=%s' % (
                av, collection[x][1])
            download(target_url, x)
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
        reply_data[part_name] = [video_url, audio_url]
    return get_info(av)


def get_at_info():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    cookie = {
        '_uuid': 'AB5A6FFA-7965-34F8-191E-A6CABDC176D286439infoc',
        'buvid3': '55A79A46-C249-4390-93EE-F51B1A4A19D1148827infoc',
        'fingerprint': 'b70b18c4c28cbaaaa2c51cfa2643b66e',
        'buvid_fp': '5F0C73BC-B75F-4ECA-AE85-1138C4329C23167613infoc',
        'buvid_fp_plain': '5F0C73BC-B75F-4ECA-AE85-1138C4329C23167613infoc',
        'PVID': '1',
        'CURRENT_FNVAL': '80',
        'SESSDATA': '8b7108c1%2C1642886233%2Cd4a44%2A71',
        'bili_jct': '63c72b06aa405872c8b70fa494678d9a',
        'DedeUserID': '328456121',
        'DedeUserID__ckMd5': 'dffc4f0440137ad2',
        'sid': '4igjj519', 'dy_spec_agreed': '1',
        'bp_video_offset_328456121': '552242471110039155',
        'bp_t_offset_328456121': '552263001054781720',
        'blackside_state': '1'
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
        '_uuid': 'AB5A6FFA-7965-34F8-191E-A6CABDC176D286439infoc',
        'buvid3': '55A79A46-C249-4390-93EE-F51B1A4A19D1148827infoc',
        'fingerprint': 'b70b18c4c28cbaaaa2c51cfa2643b66e',
        'buvid_fp': '5F0C73BC-B75F-4ECA-AE85-1138C4329C23167613infoc',
        'buvid_fp_plain': '5F0C73BC-B75F-4ECA-AE85-1138C4329C23167613infoc',
        'PVID': '1',
        'CURRENT_FNVAL': '80',
        'SESSDATA': '8b7108c1%2C1642886233%2Cd4a44%2A71',
        'bili_jct': '63c72b06aa405872c8b70fa494678d9a',
        'DedeUserID': '328456121',
        'DedeUserID__ckMd5': 'dffc4f0440137ad2',
        'sid': '4igjj519', 'dy_spec_agreed': '1',
        'bp_video_offset_328456121': '552242471110039155',
        'bp_t_offset_328456121': '552263001054781720',
        'blackside_state': '1'
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
        'csrf': '63c72b06aa405872c8b70fa494678d9a'
    }
    cookie = {
        '_uuid': 'AB5A6FFA-7965-34F8-191E-A6CABDC176D286439infoc',
        'buvid3': '55A79A46-C249-4390-93EE-F51B1A4A19D1148827infoc',
        'fingerprint': 'b70b18c4c28cbaaaa2c51cfa2643b66e',
        'buvid_fp': '5F0C73BC-B75F-4ECA-AE85-1138C4329C23167613infoc',
        'buvid_fp_plain': '5F0C73BC-B75F-4ECA-AE85-1138C4329C23167613infoc',
        'PVID': '1',
        'CURRENT_FNVAL': '80',
        'SESSDATA': '8b7108c1%2C1642886233%2Cd4a44%2A71',
        'bili_jct': '63c72b06aa405872c8b70fa494678d9a',
        'DedeUserID': '328456121',
        'DedeUserID__ckMd5': 'dffc4f0440137ad2',
        'sid': '4igjj519', 'dy_spec_agreed': '1',
        'bp_video_offset_328456121': '552242471110039155',
        'bp_t_offset_328456121': '552263001054781720',
        'blackside_state': '1'
    }
    requests.post(REPLY_URL, params=params, cookies=cookie)
    time.sleep(random.randrange(5, 75))


def reply2(message):
    params = {
        'type': '1',
        'oid': message['oid'],
        'message': '@%s 音频:%s' % (message['user'], download_url(message['oid'])[1]),
        'csrf': '63c72b06aa405872c8b70fa494678d9a'
    }
    cookie = {
        '_uuid': 'AB5A6FFA-7965-34F8-191E-A6CABDC176D286439infoc',
        'buvid3': '55A79A46-C249-4390-93EE-F51B1A4A19D1148827infoc',
        'fingerprint': 'b70b18c4c28cbaaaa2c51cfa2643b66e',
        'buvid_fp': '5F0C73BC-B75F-4ECA-AE85-1138C4329C23167613infoc',
        'buvid_fp_plain': '5F0C73BC-B75F-4ECA-AE85-1138C4329C23167613infoc',
        'PVID': '1',
        'CURRENT_FNVAL': '80',
        'SESSDATA': '8b7108c1%2C1642886233%2Cd4a44%2A71',
        'bili_jct': '63c72b06aa405872c8b70fa494678d9a',
        'DedeUserID': '328456121',
        'DedeUserID__ckMd5': 'dffc4f0440137ad2',
        'sid': '4igjj519', 'dy_spec_agreed': '1',
        'bp_video_offset_328456121': '552242471110039155',
        'bp_t_offset_328456121': '552263001054781720',
        'blackside_state': '1'
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
