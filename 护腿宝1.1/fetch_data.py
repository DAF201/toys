import requests
def fetch_data():
    number=("0","1","2","3","4","5","6","7","8","9")
    fetch_data_url="http://api.bilibili.com/x/space/arc/search"
    params = {
        "mid":"672342685",
        "pn":"1",
        "ps":"20"
    }
    info = str(requests.get(fetch_data_url,params=params).text)
    av_info=info.split("aid")[1]
    av_info=av_info.split("bvid")[0]
    first_av=""
    for x in av_info:
        if x in number:
            first_av+=x
    return first_av