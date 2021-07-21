from datetime import datetime
import requests
import hashlib
import time
from os import path
import pickle
import re
import json


def get_uid():

    print("who do you want to see today?")
    print("please enter the number associated")
    print("1.AWA 2.Bella 3.Carol 4.Diana 5.Elieen")

    person = input()
    if person == 1 or "1":
        uid = "672346917"
        return uid

    elif person == 2 or "2":
        uid = "672353429"
        return uid

    elif person == 3 or "3":
        uid = "351609538"
        return uid

    elif person == 4 or "4":
        uid = "672328094"
        return uid

    elif person == 5 or "5":
        uid = "672342685"
        return uid

    else:
        print("invaild input,exiting")
        time.sleep(3)
        exit()


def comment_section(csrf):

    print("do you want to leave comment today?")
    print("yes or no")
    comment_today = input()

    if comment_today == "yes":
        print("please enter your comments")
        comment_today = input()
        comment_today = authorization(csrf, comment_today)
    return comment_today


def authorization(csrf, comment_content):

    print("please vertify your signature")
    print("signature = csrf + comment in MD5")
    print("your CSRF is %s" % csrf)
    signature = input()
    sign = csrf + comment_content
    sign = hashlib.md5(sign.encode('UTF-8')).hexdigest()
    if sign == signature:
        print("authorized")
        return comment_content
    else:
        print("authorization failed")
        comment_content = ""
        return comment_content


def comment(av, csrf, sessdata, comment_content):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0, Win64, x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml,q:0.9,image/webp,image/apng,*/*,q:0.8",
        "Accept-Language": "zh-CN,zh,q:0.8"
    }
    cookie = {
        "SESSDATA": sessdata
    }
    params = {
        "type": "1",
        "oid": av,
        "message": "%s@%s" % (comment_content, datetime.now()),
        "SESSDATA": sessdata,
        "csrf": csrf
    }
    requests.post("http://api.bilibili.com/x/v2/reply/add",
                  params=params, headers=header, cookies=cookie)


def download_section():

    print("wanna download video also?")
    print("yes or no")
    download = input()

    if download == "yes":
        download = True
        return download
    else:
        download = False
        return download


def like_and_coin_section():

    print("wanna give a like and two coins?")
    print("yes or no")
    like_coin = input()

    if like_coin == "yes":
        like_coin = True
        return like_coin
    else:
        like_coin == False
        return like_coin


def like_and_coin(av, csrf, sessdata):

    params = {
        "aid": av,
        "multiply": "2",
        "select_like": "1",
        "csrf": csrf
    }
    cookie = {"SESSDATA": sessdata}

    requests.post("http://api.bilibili.com/x/web-interface/coin/add",
                  params=params, cookies=cookie)


def blacklist_section():

    print("Do you want to enable the language filter?")
    print("yes or no")
    filter_enable = input()

    if filter_enable == "yes":
        filter_enable = True
        return filter_enable
    else:
        filter_enable = False
        return filter_enable


def blacklist(av):

    the_list = []
    Language_filter_pool = ['魔怔', '路人', '珈乐是谁', '不熟', '恶心', '离谱', '塔塔开', 'ttk','乐华','嘻嘻嘻','懂不懂','资本','厉害','[吃瓜]','[偷笑]','[鼓掌]','[星星眼]']
    url = "http://api.bilibili.com/x/v2/reply"
    params = {
        "type": "1",
        "oid": "%s" % av,
        "sort": "1",
        "pn": "",
        "ps": "49"
    }
    reply = requests.get(url, params=params).text.split('"replies":[')
    
    for x in range(0, 49):
        user = reply[x].split(',"sex"')[0]+'}'
        content = reply[x+1].split(',"plat')[0].split('message":')[1]
        for y in Language_filter_pool:
            if y in content:
                print(user + "said:\n")
                print(content + "\n")
                the_list.append(user + ":" + content)

    with open("%s.txt" % av, "w", encoding="utf-8") as f:
        counter = 1
        for x in the_list:
            f.write(str(counter) + ":\n" + x + "\n" + "\n")
            counter += 1


def fetch_data(uid):

    number = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    fetch_data_url = "http://api.bilibili.com/x/space/arc/search"
    params = {
        "mid": "%s" % uid,
        "pn": "1",
        "ps": "20"
    }
    info = str(requests.get(fetch_data_url, params=params).text)
    av_info = info.split("aid")[1]
    av_info = av_info.split("bvid")[0]
    first_av = ""

    for x in av_info:
        if x in number:
            first_av += x
    return first_av


def download_single_video(url, name, headers):

    res = requests.get(url, headers=headers)
    video_pattern = '__playinfo__=(.*?)</script><script>'
    playlist_info = json.loads(re.findall(video_pattern, res.text)[0])
    video_url = playlist_info['data']['dash']['video'][0]['baseUrl']
    audio_url = playlist_info['data']['dash']['audio'][0]['baseUrl']

    save_file(video_url, "%s.video" % name, headers)
    save_file(audio_url, "%s.audio" % name, headers)
    print('{} finished download:'.format(name))


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


def download_video(av, sessdata):

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
               'cookie': "SESSDATA:%s" % sessdata
               }
    base_url = 'https://www.bilibili.com/video/av%s' % av
    json_info = get_list_info(base_url, headers)

    for i in json_info:
        p = i['page']
        name = 'P{} - {}'.format(p, i['part'])
        url = base_url + '?p={}'.format(p)
        download_single_video(url, name, headers)


def my_coins(sessdata):
    
    coins = ""
    number = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    cookie = {"SESSDATA": sessdata}
    r = str(requests.get(
        "http://api.bilibili.com/x/space/myinfo", cookies=cookie).text)
    r = r.split("coins")[1]
    r = r.split("following")[0]

    for x in r:
        if x in number:
            coins += x
    return coins


def main():

    av_record = ""
    print("welcome, but before you start, I want to remind you that I will not be responsible for how you are going to use this tool.")
    print("I will no be responsible for the occurring of suspending or banning caused by abusing")
    print("if you agree, please say yes. Otherwise, leave blank or say no.")
    print("yes or no")
    agree = input()

    if agree != 'yes':
        print("exiting in 5 sec")
        time.sleep(5)
        exit()

    if path.isfile('data.txt'):
        inputFile = 'data.txt'
        fd = open(inputFile, 'rb')
        dataset = pickle.load(fd)
        sessdata = dataset[0]
        csrf = dataset[1]
    else:
        print("please sessdata")
        sessdata = input()
        print("please enter csrf")
        csrf = input()
        dataset = [sessdata, csrf]
        outputFile = 'data.txt'
        fw = open(outputFile, 'wb')
        pickle.dump(dataset, fw)
        fw.close()

    today_uid = get_uid()
    todays_comment = comment_section(csrf)
    today_video_download = download_section()
    today_blacklist = blacklist_section()
    today_coin_and_like = like_and_coin_section()

    while(True):
        if av_record != fetch_data(today_uid):
            av_record = fetch_data(today_uid)
            print("new video found at av%s @%s" % (av_record, datetime.now()))
            if todays_comment!="":
                comment(av_record,csrf,sessdata,todays_comment)
            if today_coin_and_like:
                like_and_coin(av_record, csrf, sessdata)
                print("coins left %s" % my_coins(sessdata))
            if today_video_download:
                download_video(av_record, sessdata)
            if today_blacklist:
                blacklist(av_record)
            print("finished, sleeping...")
            time.sleep(900)
        else:
            print("no new video found, sleeping...")
            time.sleep(900)


if __name__ == "__main__":
    main()
