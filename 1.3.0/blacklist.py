import requests
listy = []


def blacklist(av):
    kw = ['魔怔', '路人', '珈乐是谁', '不熟', '恶心', '离谱', '塔塔开', 'ttk']
    url = "http://api.bilibili.com/x/v2/reply"
    params = {
        "type": "1",
        "oid": "%s" % av,
        "sort": "1",
        "pn": "",
        "ps": "49"
    }
    reply = requests.get(url, params=params).text.split('"replies":[')
    for x in range(0, 49):
        user = reply[x].split(',"sex"')[0]+'}'
        content = reply[x+1].split(',"plat')[0].split('message":')[1]
        for y in kw:
            if y in content:
                print(user + "said:\n")
                print(content + "\n")
                listy.append(user + ":" + content)
    record()


def record():
    with open("record.txt", "w", encoding="utf-8") as f:
        counter = 1
        for x in listy:
            f.write(str(counter) + ":\n" + x + "\n" + "\n")
            counter += 1
