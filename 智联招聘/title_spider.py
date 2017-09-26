import requests
from lxml import etree
import json


def get_html_text(url, kv):
    try:
        r = requests.get(url, headers = kv)
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "网络异常"


#产生单个小title迭代器
def gen_sub_title(sub_titles):
    for sub_title in sub_titles:
        data = {
            'sub_title':sub_title.text,
            'url':"http://sou.zhaopin.com/"+sub_title.get('href'),
            'object':None
        }
        yield data


#产生整体小title迭代器
def gen_sub_titles(sub_titles):
    titles = []
    for i in range(len(sub_titles)):
        titles.append(sub_titles[i])
    index = 0
    sdata = []
    for sub in titles:
        for l in gen_sub_title(sub.xpath('p/a')):
            sdata.append(l)
        data = {
            index:sdata
        }
        sdata = []
        yield data
        index += 1


#获取具体职位信息object
def get_object(items):
    o_list = []
    div = items[0].xpath('div')
    for d in div:
        s = d.xpath('div')
        for div2 in s:
            ss = div2.xpath('a')
            sub_list = []
            for o in ss:
                data = {
                    'career':o.text,
                    'url':"http://sou.zhaopin.com/"+o.get('href')
                }
                sub_list.append(data)
            o_list.append(sub_list)
    #for a in o_list:
        #print(a)
    return o_list


start_url = "http://sou.zhaopin.com/"
kv = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER'}
context = get_html_text(start_url, kv)
selector = etree.HTML(context)
titles = selector.xpath('//*[@id="search_left_main"]/li/a')
title_list = []                       #产生title列表
for t in range(len(titles)):
    title_list.append(titles[t].text)
items = selector.xpath('//*[@id="search_right_demo"]')
sub_titles = items[0].xpath('div')
get_object(items)
o_list = get_object(items)
#一共三部分    title subtitle object  最后合成到一个字典中
result_dict = {}
index = 0              #索引
for a in gen_sub_titles(sub_titles):
    result_dict.update({title_list[index]:a.get(index)})
    index2 = 0          #索引2
    for s in result_dict[title_list[index]]:
        result_dict[title_list[index]][index2]['object'] = o_list[index]
        index2 += 1
    index += 1
with open('json.txt', 'w', encoding='utf-8') as f:
    f.write(json.dumps(result_dict, ensure_ascii=False))

#注意json模块函数中的第二个参数防止编码问题，很坑