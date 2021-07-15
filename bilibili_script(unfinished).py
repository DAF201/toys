import requests
send_headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0, Win64, x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
"Connection": "keep-alive",
"Accept": "text/html,application/xhtml+xml,application/xml,q:0.9,image/webp,image/apng,*/*,q:0.8",
"Accept-Language": "zh-CN,zh,q:0.8"}
cookie={"SESSDATA":"68fe298e%2C1641928092%2C025a5%2A71"}
params={
"type":"1",
"oid":"",
"message":"test",
"SESSDATA":"",
"csrf":""
}
def catch():
    r=requests.post("http://api.bilibili.com/x/v2/reply/add", params=params,headers=send_headers,cookies=cookie).text
    return r
print(catch())
