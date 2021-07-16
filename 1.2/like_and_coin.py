import requests
def like_and_coin(av,csrf,sessdata):
    params={
        "aid": av,
        "multiply" : "2",
        "select_like" : "1",
        "csrf": csrf
    }
    cookie={"SESSDATA":sessdata}
    requests.post("http://api.bilibili.com/x/web-interface/coin/add",params=params,cookies=cookie)