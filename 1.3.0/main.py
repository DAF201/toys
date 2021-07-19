import time
import pickle
from os import path
from datetime import datetime
import fetch_data
import comment
import like_and_coin
import my_coins
import video_download
import blacklist


def main():
    Welcome = "please go to you broswer to get your cookie"
    enter_sessdata = "enter your SESSDATA"
    enter_csrf = "enter your csrf"
    warning = "warning, I will not be responsible for any incident that happen in the future caused by the usage of this tool, which may include suspension or blacklist, do you want to move on still?"
    session_end = "session end"
    print(warning)
    print("yes or no")
    if (input() != "no"):
        if path.isfile('data.txt'):
            inputFile = 'data.txt'
            fd = open(inputFile, 'rb')
            dataset = pickle.load(fd)
            sessdata = dataset[0]
            csrf = dataset[1]
        else:
            print(Welcome)
            print(enter_sessdata)
            sessdata=input()
            print(enter_csrf)
            csrf=input()
            dataset = [sessdata, csrf]
            outputFile = 'data.txt'
            fw = open(outputFile, 'wb')
            pickle.dump(dataset, fw)
            fw.close()
        print("do you want to download the video also?")
        print("yes or no")
        download = input()
        print("do you want a list today?")
        print("yes or no")
        bl = input()
        counter = 0
        coin_record = 2
        old_record = ""
        new_record = " "
        while(True):
            if(old_record != new_record):
                print(" ")
                new_record = fetch_data.fetch_data()
                old_record = new_record
                comment.comment(old_record,csrf,sessdata)
                if coin_record > 1:
                    like_and_coin.like_and_coin(old_record, csrf, sessdata)
                    coin_record = my_coins.my_coins(sessdata)
                else:
                    print("warning, no enough coin")
                    coin_record = my_coins.my_coins(sessdata)
                counter = +1
                if bl != "no":
                    print("catching suspicious comments...")
                    print("suspicious comments: \n")
                    blacklist.blacklist(old_record)
                print("has runs for: %s times!" % counter)
                print("current time: %s" % datetime.now())
                print("location: av%s" % old_record)
                print("coins left: %s" % coin_record)
                print(" ")
                if (download != "no"):
                    video_download.main(old_record, sessdata)
                time.sleep(60)
            else:
                print(
                    "no new video found, current time%s, entering sleep mode..." % datetime.now())
                time.sleep(60)
    else:
        print(session_end)


if __name__ == "__main__":
    main()
