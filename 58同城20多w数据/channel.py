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


def get_channel_urls(url, kv):
    html = getHtmltext(url, kv)
    soup = BeautifulSoup(html, 'lxml')
    links = soup.select('ul.ym-submnu li b a')
    for link in links:
        page_url = 'http://bj.58.com' + link.get('href')
        print(page_url)


if __name__ == "__main__":
    start_url = 'http://bj.58.com/sale.shtml'
    kv = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER'}
    #get_channel_urls(start_url, kv)
    channel_list = '''
http://bj.58.com/shouji/
http://bj.58.com/tongxunyw/
http://bj.58.com/danche/
http://bj.58.com/fzixingche/
http://bj.58.com/diandongche/
http://bj.58.com/sanlunche/
http://bj.58.com/peijianzhuangbei/
http://bj.58.com/diannao/
http://bj.58.com/bijiben/
http://bj.58.com/pbdn/
http://bj.58.com/diannaopeijian/
http://bj.58.com/zhoubianshebei/
http://bj.58.com/shuma/
http://bj.58.com/shumaxiangji/
http://bj.58.com/mpsanmpsi/
http://bj.58.com/youxiji/
http://bj.58.com/jiadian/
http://bj.58.com/dianshiji/
http://bj.58.com/ershoukongtiao/
http://bj.58.com/xiyiji/
http://bj.58.com/bingxiang/
http://bj.58.com/binggui/
http://bj.58.com/chuang/
http://bj.58.com/ershoujiaju/
http://bj.58.com/bangongshebei/
http://bj.58.com/diannaohaocai/
http://bj.58.com/bangongjiaju/
http://bj.58.com/ershoushebei/
http://bj.58.com/yingyou/
http://bj.58.com/yingeryongpin/
http://bj.58.com/muyingweiyang/
http://bj.58.com/muyingtongchuang/
http://bj.58.com/yunfuyongpin/
http://bj.58.com/fushi/
http://bj.58.com/nanzhuang/
http://bj.58.com/fsxiemao/
http://bj.58.com/xiangbao/
http://bj.58.com/meirong/
http://bj.58.com/yishu/
http://bj.58.com/shufahuihua/
http://bj.58.com/zhubaoshipin/
http://bj.58.com/yuqi/
http://bj.58.com/tushu/
http://bj.58.com/tushubook/
http://bj.58.com/wenti/
http://bj.58.com/yundongfushi/
http://bj.58.com/jianshenqixie/
http://bj.58.com/huju/
http://bj.58.com/qiulei/
http://bj.58.com/yueqi/
http://bj.58.com/chengren/
http://bj.58.com/nvyongpin/
http://bj.58.com/qinglvqingqu/
http://bj.58.com/qingquneiyi/
http://bj.58.com/chengren/
http://bj.58.com/xiaoyuan/
http://bj.58.com/ershouqiugou/
http://bj.58.com/tiaozao/
http://bj.58.com/tiaozao/
http://bj.58.com/tiaozao/
    '''
    print(channel_list)