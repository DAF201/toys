import requests
import time
from datetime import datetime
def detect_return():
    number=("0","1","2","3","4","5","6","7","8","9")
    params = {
        "mid":"672342685",
        "pn":"1",
        "ps":"20"
    }
    info = str(requests.get("http://api.bilibili.com/x/space/arc/search",params=params).text)
    av_info=info.split("aid")[1]
    av_info=av_info.split("bvid")[0]
    first_av=""
    for x in av_info:
        if x in number:
            first_av+=x
    return first_av
def comment(av):
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0, Win64, x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml,q:0.9,image/webp,image/apng,*/*,q:0.8",
        "Accept-Language": "zh-CN,zh,q:0.8"
    }
    cookie={"SESSDATA":"68fe298e%2C1641928092%2C025a5%2A71"}
    params={
        "type":"1",
        "oid":av,
        "message":"乃老师大腿别着凉了",
        "SESSDATA":"68fe298e%2C1641928092%2C025a5%2A71",
        "csrf":"ccec66ee811252f62e6155f03be396d9"
    }
    r=requests.post("http://api.bilibili.com/x/v2/reply/add", params=params,headers=send_headers,cookies=cookie).text
    return r
def main():
    record=""
    times=0
    while(True):
        if record!=detect_return():
            record=detect_return()
            comment(record)
            times=+1
            print("护腿次数："+ str(times))
            print("护腿于："+ str(datetime.now()))
            time.sleep(900)

if __name__=="__main__":
    main()
