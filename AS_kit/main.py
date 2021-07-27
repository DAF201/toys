import json
import time
import datetime
from datetime import datetime
import os
import threading
import hashlib
import requests
import re
from os import path


class bot():
    def __init__(self, uid, login, Authorization, configuration) -> None:

        self.lock = threading.Lock()

        self.uid = uid
        self.login_data = login
        self.Auth = Authorization
        self.configuration = configuration

    def get_new_video(self) -> dict:

        current_path = os.getcwd()
        video_data = {}
        fetch_data_url = 'http://api.bilibili.com/x/space/arc/search'
        param = {
            'mid': self.uid,
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

        if path.isfile(current_path + '\last_video_fetched%s.json' % self.uid):
            with open(current_path + '\last_video_fetched%s.json' % self.uid, 'r') as saved_data:
                video_data = json.load(saved_data)
                if video_data['av'] != av or video_data['title'] != title:
                    video_data['title'] = title
                    video_data['av'] = av
                    video_data['updated'] = True
                    print('updating data for %s' % self.uid)
                else:
                    video_data['updated'] = False
                    print('no new video found under %s' % self.uid)
            with open(current_path + '\last_video_fetched%s.json' % self.uid, 'w') as saved_data:
                json.dump(video_data, saved_data)
        else:
            with open(current_path + '\last_video_fetched%s.json' % self.uid, 'w') as saved_data:
                video_data['title'] = title
                video_data['av'] = av
                video_data['updated'] = True
                json.dump(video_data, saved_data)
                print('creating new record for %s' % self.uid)
        return video_data

    def language_filter(self) -> None:

        final = []
        user_uid = []
        content = []
        url = 'http://api.bilibili.com/x/v2/reply'
        params = {
            'type': '1',
            'oid': self.get_new_video()['av'],
            'pn': '1',
            'ps': '49'
        }
        reply = requests.get(url, params=params).text
        reply = json.loads(reply)
        reply = reply['data']['replies']
        for x in reply:
            for y in ['阴阳','4000','运营','老铁','宠粉','打call','魔怔', '路人', '珈乐是谁', '不熟', '恶心', '离谱', '塔塔开', 'ttk', '乐华', '嘻嘻嘻', '懂不懂', '资本', '厉害', '[吃瓜]', '[偷笑]', '[鼓掌]', '[星星眼]', '机器人', '战场']:
                if y in x['content']['message'].encode('utf-8').decode('utf-8'):
                    user_uid.append(x['member']['mid'])
                    content.append(x['content']['message'])
        final = dict(zip(user_uid, content))
        for key in final:
            print(key+'\n'+final[key]+'\n')
        with open('user_and_comments@%s.json' % self.get_new_video()['av'], 'w') as file:
            json.dump(final, file)

    def like_and_coins(self) -> None:

        check_coin_url = 'http://api.bilibili.com/x/web-interface/archive/coins'
        coin_url = 'http://api.bilibili.com/x/web-interface/coin/add'
        params_check = {
            'aid': self.get_new_video()['av']
        }
        params_like_and_coins = {
            'aid': self.get_new_video()['av'],
            'multiply': '2',
            'select_like': '1',
            'csrf': self.login_data['csrf']
        }
        cookie = {
            'SESSDATA': self.login_data['sessdata']
        }
        reply = requests.get(
            check_coin_url, params=params_check, cookies=cookie).text
        reply = json.loads(reply)
        if reply['data']['multiply'] == 0:
            reply = requests.post(
                coin_url, params=params_like_and_coins, cookies=cookie).text
            reply = json.loads(reply)
            if reply['data']['like']:
                print('you give %s two coins and a like' %
                      self.get_new_video()['av'])
            else:
                print('fail to like the video')
                print(reply)
        else:
            print('you have give this video coins')

    def comment(self):
        if self.Auth['auth']:
            comment_url = 'http://api.bilibili.com/x/v2/reply/add'
            params = {
                'type': '1',
                'oid': self.get_new_video()['av'],
                'message': self.Auth['contains']+'\n来自AS_kit1.5_test @%s'%datetime.now(),
                'csrf': self.login_data['csrf'],
                'SESSDATA': self.login_data['sessdata']
            }
            cookie = {
                'SESSDATA': self.login_data['sessdata']
            }
            text = requests.post(
                comment_url, params=params, cookies=cookie).text
            text = json.loads(text)
            if text['data']['success_toast'] == '发送成功':
                print('you said %s' % self.Auth['contains'])
            else:
                print('comment failed')
                print(text)
        else:
            print('you have no access to it')

    def download(self) -> None:

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
                       'cookie': "SESSDATA:%s" % self.login_data['sessdata']
                       }
            base_url = 'https://www.bilibili.com/video/av%s' % self.get_new_video()['av']
            json_info = get_list_info(base_url, headers)

            for i in json_info:
                p = i['page']
                name = 'P{} - {}'.format(p, i['part'])
                url = base_url + '?p={}'.format(p)
                download_single_video(url, name, headers)

        download_video()

    def main(self) -> None:

        while(True):
            try:
                self.lock.acquire()
                if self.get_new_video()['updated']:
                    self.get_new_video()
                    if self.Auth['auth']:
                        self.comment()
                    if self.configuration['like_and_coin']:
                        self.like_and_coins()
                    if self.configuration['blacklist']:
                        self.language_filter()
                    if self.configuration['download']:
                        self.download()
            finally:
                self.lock.release()
                print('finished at @%s\n'%datetime.now())
                time.sleep(self.configuration['interval'])


def who() -> list:

    vaild = ['1', '2', '3', '4', '5', '6']
    uid = []

    print('who do you want to see today?')
    print('please enter the number corresponds, no need to separate with a comma')
    print('1.AWA 2.Bella 3.Carol 4.Diana 5.Elieen 6.The_Shark')

    person = input()
    if '1' in person:
        uid.append('672346917')

    if '2' in person:
        uid.append('672353429')

    if '3' in person:
        uid.append('351609538')

    if '4' in person:
        uid.append('672328094')

    if '5' in person:
        uid.append('672342685')

    if '6' in person:
        uid.append('434334701')

    if len(uid) == 0:
        print('no input,exiting')
        time.sleep(3)
        exit()

    for x in person:
        if x not in vaild:
            print('contains invaild input,exiting')
            time.sleep(3)
            exit()

    return uid


def auth(login_data) -> dict:

    auth_data = {}

    print('want to say anything today?')
    print('yes or no')
    demand_talk = input()

    if demand_talk == 'yes':
        print('want do you want to say?')
        print('enter your words')
        original = input()
        contains_talk = login_data['csrf']+original
        print('vertify time')
        print('enter the sign')
        print('sign = your csrf + what you tried to say in MD5, your csrf is %s' %
              login_data['csrf'])
        sign = input()

        if sign == hashlib.md5((contains_talk).encode('UTF-8')).hexdigest():
            print('success')
            auth_data['auth'] = True
            auth_data['contains'] = original
        else:
            print('failed')
            print(hashlib.md5(
                (contains_talk+login_data['csrf']).encode('UTF-8')).hexdigest())
            auth_data['auth'] = False

    else:
        print('silence is gold right? Buddy')
        auth_data['auth'] = False

    return auth_data


def config() -> dict:

    config_data = {}

    print('do you want to give the new video a like and two coins?')
    print('yes or no')
    like_and_coin = input()
    if like_and_coin == 'yes':
        print('smart move')
        config_data['like_and_coin'] = True
    else:
        print('that is okay,anyway...')
        config_data['like_and_coin'] = False

    print('wanna download the video as a souvenir?')
    print('yes or no')
    dl_video = input()
    if dl_video == 'yes':
        print('smart choice')
        config_data['download'] = True
    else:
        print('I will keep you some sapce this time')
        config_data['download'] = False

    print('do you want a list today?')
    print('yes or no')
    a_list = input()
    if a_list == 'yes':
        config_data['blacklist'] = True
    else:
        config_data['blacklist'] = False

    print('want to set a scanning interval?(can not be less than half min)')
    print('yes or no')
    time_lock = input()
    if time_lock == 'yes':
        print('please enter number of seconds')
        time_lock = input()
        try:
            if int(time_lock) < 30:
                print('too fast, set to 30 seconds')
                config_data['interval'] = 30
            else:
                print('setting scanning interval to %s' % time_lock)
                config_data['interval'] = int(time_lock)
        except:
            print('invaild,setting time to 15 min')
            config_data['interval'] = 900
        finally:
            return config_data


def login_data() -> dict:

    login_data = {}

    if path.isfile('data.json'):
        inputFile = 'data.json'
        with open(inputFile, 'r') as fd:
            login_data = json.loads(fd.read())
    else:
        print('please enter sessdata')
        sessdata = input()
        print('please enter csrf')
        csrf = input()
        login_data['sessdata'] = sessdata
        login_data['csrf'] = csrf
        outputFile = 'data.json'
        with open(outputFile, 'w') as fw:
            json.dump(login_data, fw)
    return login_data


def starting() -> None:
    id_list = who()
    login = login_data()
    Authorization = auth(login)
    configuration_data = config()
    if len(id_list) == 1:
        a = bot(id_list[0], login, Authorization, configuration_data)

        t1 = threading.Thread(target=a.main, args=())

        t1.start()

        t1.join()

    elif len(id_list) == 2:
        a = bot(id_list[0], login, Authorization, configuration_data)
        b = bot(id_list[1], login, Authorization, configuration_data)

        t1 = threading.Thread(target=a.main, args=())
        t2 = threading.Thread(target=b.main, args=())

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    elif len(id_list) == 3:
        a = bot(id_list[0], login, Authorization, configuration_data)
        b = bot(id_list[1], login, Authorization, configuration_data)
        c = bot(id_list[2], login, Authorization, configuration_data)

        t1 = threading.Thread(target=a.main, args=())
        t2 = threading.Thread(target=b.main, args=())
        t3 = threading.Thread(target=c.main, args=())

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

    elif len(id_list) == 4:
        a = bot(id_list[0], login, Authorization, configuration_data)
        b = bot(id_list[1], login, Authorization, configuration_data)
        c = bot(id_list[2], login, Authorization, configuration_data)
        d = bot(id_list[3], login, Authorization, configuration_data)

        t1 = threading.Thread(target=a.main, args=())
        t2 = threading.Thread(target=b.main, args=())
        t3 = threading.Thread(target=c.main, args=())
        t4 = threading.Thread(target=d.main, args=())

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

    elif len(id_list) == 5:
        a = bot(id_list[0], login, Authorization, configuration_data)
        b = bot(id_list[1], login, Authorization, configuration_data)
        c = bot(id_list[2], login, Authorization, configuration_data)
        d = bot(id_list[3], login, Authorization, configuration_data)
        e = bot(id_list[4], login, Authorization, configuration_data)

        t1 = threading.Thread(target=a.main, args=())
        t2 = threading.Thread(target=b.main, args=())
        t3 = threading.Thread(target=c.main, args=())
        t4 = threading.Thread(target=d.main, args=())
        t5 = threading.Thread(target=e.main, args=())

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()

    elif len(id_list) == 6:
        a = bot(id_list[0], login, Authorization, configuration_data)
        b = bot(id_list[1], login, Authorization, configuration_data)
        c = bot(id_list[2], login, Authorization, configuration_data)
        d = bot(id_list[3], login, Authorization, configuration_data)
        e = bot(id_list[4], login, Authorization, configuration_data)
        f = bot(id_list[5], login, Authorization, configuration_data)

        t1 = threading.Thread(target=a.main, args=())
        t2 = threading.Thread(target=b.main, args=())
        t3 = threading.Thread(target=c.main, args=())
        t4 = threading.Thread(target=d.main, args=())
        t5 = threading.Thread(target=e.main, args=())
        t6 = threading.Thread(target=f.main, args=())

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()

if __name__=='__main__':
    starting()
