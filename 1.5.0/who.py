import time
import json
import os


def who():
    current_path = os.getcwd()
    print('who do you want to see today?')
    print('please enter the number corresponds, no need to separate with a comma')
    print('1.AWA 2.Bella 3.Carol 4.Diana 5.Elieen')
    uid = []
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

    if len(uid) == 0:
        print('invaild input,exiting')
        time.sleep(3)
        exit()
    with open(current_path+'who.json', 'w') as file:
        json.dump(uid, file)
