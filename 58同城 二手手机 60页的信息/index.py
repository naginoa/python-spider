# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


def getHtmltext(url, kv):
    try:
        r = requests.get(url, headers = kv)
        r.encoding = 'utf-8'
        return r.text
    except:
        return '产生异常'


def get_item_info(who, url, kv):                  #获取每一组信息
    text = getHtmltext(url, kv)
    soup = BeautifulSoup(text, 'lxml')
    price = '.price_now' if who == 0 else '.price'
    area = '.palce_li' if who == 0 else '.c_25d'
    want = '.want_person' if who == 0 else None
    views = '.look_time' if who == 0 else '.time'
    data = {
        'title':soup.title.text.split('】')[1].strip('\r').strip('\n').strip(' '),  #清洗数据
        'price':soup.select(price)[0].text,
        'area':list(soup.select(area)[0].stripped_strings) if soup.select('.c_25d') or soup.select('.palce_li') else None,
        'want':soup.select(want)[0].text if who == 0 else None,
        'views':soup.select(views)[0].text,
        'cate':'个人' if who == 0 else '商家',
        'url':url
    }
    print(data)


def get_links_from(who=0 ,calc=2):               #获取商家和个人的url表
    url = 'http://bj.58.com/shouji/{}/pn{}/?'.format(str(who), str(clac))
    html = getHtmltext(url, kv)
    urls = []
    soup = BeautifulSoup(html, 'lxml')
    selector = 'td.t > a.t' if who == 0 else 'div.left a.t'    #个人和商家页面结构不同 因此函数内部需要分辨
    links = soup.select(selector)
    for link in links:
        if 'jump' not in link.get('href'):
            urls.append(link.get('href').split('?')[0])
    return urls


if __name__ =="__main__":
    kv = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER'}
    whos = [0, 1]
    clac = 0
    for who in whos:
        for clac in range(2, 30):
            urls = get_links_from(who, clac)
            for url in urls:
                get_item_info(who, url, kv)
