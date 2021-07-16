import requests
from datetime import datetime
def comment(av,csrf,sessdata):
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0, Win64, x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml,q:0.9,image/webp,image/apng,*/*,q:0.8",
        "Accept-Language": "zh-CN,zh,q:0.8"
    }
    cookie={"SESSDATA":sessdata}
    params={
        "type":"1",
        "oid":av,
        "message":"乃老师大腿别着凉了\n来自护腿宝1.1测试版\n@%s"%datetime.now(),
        "SESSDATA":sessdata,
        "csrf":csrf
    }
    requests.post("http://api.bilibili.com/x/v2/reply/add", params=params,headers=send_headers,cookies=cookie)