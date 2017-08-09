from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
ceshi = client['ceshi']
url_list = ceshi['url_list3']
item_info = ceshi['item_info3']

#spider1
def get_links_from(channel, who=0 ,page=2):               #获取商家和个人的url表
    url = '{}/{}/pn{}/'.format(channel, str(who), str(page))
    html = requests.get(url, headers = kv)
    time.sleep(1)
    urls = []
    soup = BeautifulSoup(html.text, 'lxml')
    selector = 'td.t > a.t' if who == 0 else 'div.left a.t'    #个人和商家页面结构不同 因此函数内部需要分辨
    links = soup.select(selector)
    if soup.find('td','t') or soup.find('div.left a.t'):
        for link in links:
            if 'jump' not in link.get('href'):
                urls.append(link.get('href').split('?')[0])
                url_list.insert_one({'url':link.get('href').split('?')[0]})
    else:   #空页
        pass
    print(urls)

#spider2

def get_item_info(who, url, kv):                  #获取每一组信息
    html = requests.get(url, kv)
    soup = BeautifulSoup(html.text, 'lxml')
    no_exists = '404' not in soup.find("h1").text
    if no_exists:                                 #存在该商品可能被购买
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
        item_info.insert_one(data)
        print(data)
    else:
        pass


if __name__ == "__main__":
    kv = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER'}
    whos = [0, 1]
    get_links_from('http://bj.58.com/tushubook/', 0, 2)
    get_item_info(0, 'http://zhuanzhuan.58.com/shouji/24605954621114x.shtml', kv)






