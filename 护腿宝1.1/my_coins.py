import requests
def my_coins(sessdata):
    coins=""
    number=("0","1","2","3","4","5","6","7","8","9")
    cookie={"SESSDATA":sessdata}
    r=str(requests.get("http://api.bilibili.com/x/space/myinfo",cookies=cookie).text)
    r=r.split("coins")[1]
    r=r.split("following")[0]
    for x in r:
        if x in number:
            coins+=x
    return coins