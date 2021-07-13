import requests
import html2text

def content():
    r=requests.get('https://jtechdigital.com/')
    r=r.text
    r=html2text.html2text(r)
    return r
print(content())