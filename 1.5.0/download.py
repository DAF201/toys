import requests
import json
import re
def download(login_data,video_data):
    def download_single_video(url, name, headers):

        res = requests.get(url, headers=headers)
        video_pattern = '__playinfo__=(.*?)</script><script>'
        playlist_info = json.loads(re.findall(video_pattern, res.text)[0])
        video_url = playlist_info['data']['dash']['video'][0]['baseUrl']
        audio_url = playlist_info['data']['dash']['audio'][0]['baseUrl']

        save_file(video_url, "%s.video" % name, headers)
        save_file(audio_url, "%s.audio" % name, headers)
        print('{} finished downloading:'.format(name))

    def save_file(url, type, headers):

        download_content = requests.get(url, headers=headers).content

        with open('{}.mp4'.format(type), 'wb') as output:
            output.write(download_content)

    def get_list_info(url, headers):

        aid_pattern = 'window.__INITIAL_STATE__={"aid":(\d*?),'
        res = requests.get(url, headers=headers)
        aid = re.findall(aid_pattern, res.text)[0]
        playlist_json_url = 'https://api.bilibili.com/x/player/pagelist?aid={}'.format(
            aid)
        json_info = json.loads(requests.get(
            playlist_json_url, headers=headers).content.decode('utf-8'))['data']
        return json_info

    def download_video():
        print('starts downloading')
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
                    'cookie': "SESSDATA:%s" %login_data['sessdata']
                    }
        base_url = 'https://www.bilibili.com/video/av%s' %video_data['av']
        json_info = get_list_info(base_url, headers)

        for i in json_info:
            p = i['page']
            name = 'P{} - {}'.format(p, i['part'])
            url = base_url + '?p={}'.format(p)
            download_single_video(url, name, headers)

    download_video()