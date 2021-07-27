import json
import time
import datetime
from datetime import datetime
import time
import os
from multiprocessing import Process
import who
import new_video_check
import sessdata_and_csrf
import download
import auth
import comment
import like_and_coin
import language_filter
import starting

def run(uid, login_data, demand_language_filter, comment_data, demand_like,demand_download):
    while(True):
        video_data = new_video_check.new_video_check(uid)
        if video_data['updated'] == True:
            if demand_language_filter:
                language_filter.sensative_comments(video_data)
            if comment_data['auth']:
                comment.comment(video_data, comment_data, login_data)
            if demand_like:
                like_and_coin.like_and_coins(video_data, login_data)
            if demand_download:
                download.download(login_data,video_data)
            print('finished at @%s for %s'%(datetime.now(),uid))
        time.sleep(900)
process_list = []
if __name__ == '__main__':

    who.who()
    current_path = os.getcwd()
    login_data = sessdata_and_csrf.sess_and_csrf()
    with open(current_path+'who.json', 'r') as file:
        person = json.load(file)

    starting.setup()
    with open(current_path+'setting.json', 'r') as file:
        file = json.load(file)
        demand_language_filter=file['demand_language_filter']
        comment_data=file['comment_data']
        demand_like=file['demand_like']
        demand_download=file['demand_download']


    for i in range(0, len(person)):
        p = Process(target=run, args=(
            person[i], login_data, demand_language_filter, comment_data, demand_like,demand_download))
        p.start()
        process_list.append(p)

    for i in process_list:
        p.join()
