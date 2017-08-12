from bs4 import BeautifulSoup
from multiprocessing import Pool
from channel import channel_list
from headers import kv
from headers import proxies
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
ceshi = client['58']
url_list = ceshi['url_list']
item_info = ceshi['item_info']


# spider1
def get_links_from(channel, who=0, page=2):  # 获取商家和个人的url表
    url = '{}/{}/pn{}/'.format(channel, str(who), str(page))
    html = requests.get(url, headers=kv, proxies=proxies)
    time.sleep(1)
    urls = []
    soup = BeautifulSoup(html.text, 'lxml')
    selector = 'td.t > a.t' if soup.find('td', 't') else 'div.left a.t'  # 个人和商家页面结构不同 因此函数内部需要分辨
    links = soup.select(selector)
    if soup.find('td', 't') or soup.select('div.left a.t'):
        for link in links:
            if 'jump' not in link.get('href'):
                urls.append(link.get('href').split('?')[0])
                url_list.insert_one({'url':link.get('href').split('?')[0]})
    else:  # 空页
        pass
    return urls  # 完成


# spider2
def get_item_info(who, url, kv):  # 获取每一组信息
    html = requests.get(url, headers=kv, proxies=proxies)
    # time.sleep(1)
    soup = BeautifulSoup(html.text, 'lxml')
    no_exists = '404' not in soup.find("h1").text
    if no_exists:  # 存在该商品可能被购买
        try:
            price = '.price_now' if soup.select('.price_now') else '.price'
            area = '.palce_li' if soup.select('.palce_li')else 'c_25d'
            area_a = list((soup.select('.su_con'))[-2].stripped_strings) if soup.select('.su_con') else None
            want = '.want_person' if soup.select('.want_person') else None
            views = '.look_time'
            data = {
                'title': soup.title.text.strip(),  # 清洗数据
                'price': soup.select(price)[0].text.strip(),
                'area': list(soup.select(area)[0].stripped_strings) if soup.select('.c_25d') or soup.select('.palce_li') else list((soup.select('.su_con'))[-2].stripped_strings) if soup.select('.su_con') else None,
                'want': soup.select(want)[0].text.strip() if soup.select('.want_person') else None,
                'views': soup.select(views)[0].text.strip() if soup.select(views) else get_views_from2(url),
                'time': soup.select('.time')[0].text.strip() if soup.select('.time') else None,
                'cate': '个人' if who == 0 else '商家',
                'url': url,
            }
            item_info.insert_one(data)
            #print(data)
        except:
            print('timeover')
    else:
        pass


def get_views_from2(url):
    kv2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER',
        'Referer': 'http://bj.58.com/ershoujiaju/30255819125435x.shtml?',
    }
    ID = url.split('/')[-1][:-7]  # 取ID号
    url_js = 'http://jst1.58.com/counter?infoid={}&userid=&uname=&sid=555789872'.format(str(ID))
    context = requests.get(url_js, headers=kv2).text
    views = context.split('=')[-1]
    return views


def get_views_from3(url):  # 备用
    kv3 = {
        'Host': 'jst1.58.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER',
        'Referer': 'http://bj.58.com/ershoushebei/31020167338937x.shtml?',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': 'id58=Cn5lxFhktTCpNxDlYCMMAg==; als=0; bj58_id58s="ekcwdi1XdzdMV1M1ODE2NA=="; gr_user_id=ae910cdd-5030-40dc-aacb-1f30d01c4408; Hm_lvt_3bb04d7a4ca3846dcc66a99c3e861511=1484140260; Hm_lvt_e15962162366a86a6229038443847be7=1484120314,1484140297; __autma=253535702.971785459.1484140260.1484140260.1490019419.2; __utma=253535702.855450639.1484120247.1484120247.1490019419.2; __utmz=253535702.1484120247.1.1.utmcsr=changzhi.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/; wmda_uuid=75afb6b4c62fc5b48cad4372e5a0e8b8; wmda_new_uuid=1; wmda_visited_projects=%3B1409632296065; commontopbar_myfeet_tooltip=end; myfeet_tooltip=end; es_ab=0; 58home=bj; nab=WBHUANGYE_122_25049812; ipcity=changzhi%7C%u957F%u6CBB%7C0; city=bj; sessionid=a41844e4-4fd3-4637-9855-d388b355d828; GA_GTID=0d4000f6-0000-17be-e195-ffd5d992b25b; _ga=GA1.2.855450639.1484120247; _gid=GA1.2.1113197810.1502417295; bj58_new_uv=15; final_history=31033011422654%2C31020167338937%2C27881001184687%2C30819729748678%2C30896584095174; commontopbar_city=1%7C%u5317%u4EAC%7Cbj; abtest=WBHUANGYE_122_25049812; 58tj_uuid=088478e3-567f-4e33-89e3-680f2deb0404; new_session=1; new_uv=18; utm_source=; spm=; init_refer=; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1502418928,1502445555; Hm_lpvt_e2d6b2d0ec536275bb1e37b421085803=1502456060; gr_session_id_98e5a48d736e5e14=238c5d6e-cff7-4910-9184-aebbebb937a2'
    }
    ID = url.split('/')[-1][:-7]  # 取ID号
    url_js = 'http://jst1.58.com/counter?infoid={}&userid=&uname=&sid=555789872'.format(str(ID))
    context = requests.get(url_js, headers=kv3).text
    views = context.split('=')[-1]
    return views


def get_all_link_from(channel):
    whos = [0, 1]
    for who in whos:
        for i in range(1, 100):
            urls = get_links_from(channel, who, i)


def get_all_items_from(channel):
    whos = [0, 1]
    for who in whos:
        for i in range(1, 100):
            get_item_info(who, channel, kv)


if __name__ == "__main__":
    channels = channel_list.split('\n')
    channels.remove('')
    pool = Pool()                            #多进程
    #pool.map(get_all_link_from, channels)
    urls = []
    for post in url_list.find():           #多进程分步
        urls.append(post['url'])
    pool.map(get_all_items_from, urls)