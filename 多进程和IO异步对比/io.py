from bs4 import BeautifulSoup
import time
import requests
import pymongo
import random
import asyncio


# 共用部分
clients = pymongo.MongoClient('localhost')
db = clients["wandoujia"]
col = db["info"]

urls = ['http://www.wandoujia.com/award?page={}'.format(num) for num in range(1, 46)]
UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'www.wandoujia.com',
    'User-Agent': random.choice(UA_LIST)
}

proxies = {
    'http': 'http://123.206.6.17:3128',
    'https': 'http://123.206.6.17:3128'
}


def method_3():
    async def get_url(url):
        async with aiohttp.ClientSession() as session:  # await关键字将暂停协程函数的执行，等待异步IO返回结果。
            async with session.get(url) as html:
                response = await html.text(encoding="utf-8")  # await关键字将暂停协程函数的执行，等待异步IO返回结果。
                return response

    async def parser(url):
        html = await get_url(url)
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find_all(class_='title')
        app_title = soup.find_all(class_='app-title')
        item_cover = soup.find_all(class_='item-cover')
        icon_cover = soup.select('div.list-wrap > ul > li > div.icon > img')
        for title_i, app_title_i, item_cover_i, icon_cover_i in zip(title, app_title, item_cover, icon_cover):
            content = {
                'title': title_i.get_text(),
                'app_title': app_title_i.get_text(),
                'item_cover': item_cover_i['data-original'],
                'icon_cover': icon_cover_i['data-original']
            }
            col.insert(content)
            print('成功插入一组数据' + str(content))

    start = time.time()
    loop = asyncio.get_event_loop()
    tasks = [parser(url) for url in urls]
    loop.run_until_complete(asyncio.gather(*tasks))
    print(time.time() - start)

if __name__ == '__main__':
    method_3()