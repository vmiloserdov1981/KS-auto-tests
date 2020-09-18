import requests
from lxml import html

ip = "http://10.10.20.39"
page = requests.get(f'{ip}:8080/video')
webpage = html.fromstring(page.content)
names = webpage.xpath('//a/@href')
for i in names:
    url = f'{ip}:4444/video/{i}'
    requests.delete(url)
