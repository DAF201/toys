import time
from datetime import datetime
import fetch_data,comment,like_and_coin,my_coins
def main():
    Welcome="please go to you broswer to get your cookie"
    enter_sessdata="enter your SESSDATA"
    enter_csrf="enter your csrf"
    warning="warning, I will not be responsible for any incident that happen in the future caused by the usage of this tool, which may include suspension or blacklist, do you want to move on still?"
    session_end="session end"
    print(warning)
    print("yes or no")
    if (input()=="yes"):
        print(Welcome)
        print(enter_sessdata)
        sessdata=input()
        print(enter_csrf)
        csrf=input()
        counter=0
        coin_record=2
        old_record=""
        new_record=" "
        while(True):
            if(old_record!=new_record):
                print(" ")
                new_record=fetch_data.fetch_data()
                old_record=new_record
                comment.comment(old_record,csrf,sessdata)
                if coin_record >1:
                    like_and_coin.like_and_coin(old_record,csrf,sessdata)
                    coin_record=my_coins.my_coins(sessdata)
                else:
                    print("警告，当前硬币不足")
                    coin_record=my_coins.my_coins(sessdata)
                counter=+1
                print("护腿宝为您服务，当前次数：%s"%counter)
                print("当前时间：%s"%datetime.now())
                print("护腿地点：av%s"%old_record)
                print("剩余硬币数量：%s"%coin_record)
                print(" ")
                time.sleep(900)
            else:
                time.sleep(900)
    else:
        print(session_end)
if __name__=="__main__":
    main()
