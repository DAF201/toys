import os
from os import path
import pickle


def sess_and_csrf():
    current_path = os.getcwd()
    login_data = {}

    if path.isfile(current_path + 'data.txt'):
        inputFile = current_path + 'data.txt'
        fd = open(inputFile, 'rb')
        dataset = pickle.load(fd)
        sessdata = dataset[0]
        csrf = dataset[1]
    else:
        print('please enter sessdata')
        sessdata = input()
        print('please enter csrf')
        csrf = input()
        dataset = [sessdata, csrf]
        outputFile = current_path + 'data.txt'
        fw = open(outputFile, 'wb')
        pickle.dump(dataset, fw)
        fw.close()

    login_data['sessdata'] = sessdata
    login_data['csrf'] = csrf
    return login_data