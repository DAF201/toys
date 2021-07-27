import auth
import os
import json
import sessdata_and_csrf


def setup():
    current_path = os.getcwd()
    setting = {}
    print('want to enable language filter?')
    print('yes or no')
    demand_language_filter = input()
    if demand_language_filter == 'yes':
        setting['demand_language_filter'] = True
    else:
        setting['demand_language_filter'] = False

    if demand_language_filter:
        login_data = sessdata_and_csrf.sess_and_csrf()
        setting['comment_data'] = auth.auth(login_data)

    print('wanna leave a like before you go?')
    print('yes or no')
    demand_like = input()
    if demand_like == 'yes':
        setting['demand_like'] = True
    else:
        setting['demand_like'] = False

    print('download the video?')
    print('yes or no')
    demand_download = input()
    if demand_download == 'yes':
        setting['demand_download'] = True
    else:
        setting['demand_download'] = False

    with open(current_path+'setting.json', 'w') as file:
        json.dump(setting, file)
