import requests
from lxml import html
import os

if os.getenv('CLEAR_VIDEOS') == 'true':
    ip = os.getenv('SELENOID_IP', '127.0.0.1')
    page = requests.get(f'http://{ip}:8080/video')
    webpage = html.fromstring(page.content)
    names = webpage.xpath('//a/@href')
    for i in names:
        url = f'http://{ip}:4444/video/{i}'
        requests.delete(url)
