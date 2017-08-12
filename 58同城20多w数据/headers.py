import random

kv = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER'}
proxy_list = [
    'https://42.202.130.246:3128',
    'http://180.157.235.74:8088',
    'https://101.37.79.125:3128',
    'http://115.29.106.191:8088',
    'http://139.196.176.18:9797',
    'http://125.77.25.118:80',
    'http://116.11.254.37:80',
]
proxy_ip = random.choice(proxy_list)
proxies = {'https': proxy_ip}
