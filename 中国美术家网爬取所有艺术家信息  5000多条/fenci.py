# -*- coding: utf-8 -*-
import jieba.analyse
import requests


def getkeystr(content):
    sep = jieba.analyse.extract_tags(content, topK=10, withWeight=True, allowPOS=('np' ,'nr','n'))
    keylist = []
    for a, b in sep:
        # if ord(a[0]) > 127:   #去掉英文
        keylist.append(a)
    keystr = ' '.join(keylist)
    return keystr


def getHtmltext(keystr, kv):
    url = "https://www.baidu.com/s?wd=" + keystr
    try:
        r = requests.get(url, headers = kv)
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"


def getcontentlist(filename):
    with open('file.txt', encoding='utf-8') as f:
        text = f.read()  # list 存放读取的text  list2存放清洗后的text
        alllist2 = []
        alllist = text.split(':')  # 按照冒号分组
        for sub in alllist:
            sub2 = sub[:-5]  # 清洗
            alllist2.append(sub2)
        b = 0
        for a in alllist2:  # 清洗空项
            if a == '':
                b += 1
        flag = 1
        while flag <= b:
            alllist2.remove('')
            flag += 1
    return alllist2


if __name__=="__main__":
    kv = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER'}
    filename = 'file.txt'
    contentlist = getcontentlist(filename)
    for content in contentlist:
        keystr = getkeystr(content)
        htmltext = getHtmltext(keystr, kv)
        print(keystr)
