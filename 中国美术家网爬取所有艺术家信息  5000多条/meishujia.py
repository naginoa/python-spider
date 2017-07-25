import requests
import re
import time
from bs4 import BeautifulSoup
from urllib import parse


def getHTMLText(url):
    kv = {'user-agent': 'Mozilia/5.0'}
    try:
        time.sleep(1)
        r = requests.get(url, headers = kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"


def getUrltexts(html, clas):
    soup = BeautifulSoup(html, 'html.parser')
    source_string = soup.find('ul', {'class': clas})
    alists = source_string.find_all('a')
    urltexts = []
    for a in alists:
        pattern = 'tag.*'
        string = a.attrs['href']
        result = re.search(pattern, string)
        if (result != None):
            urltext = result.group()[4:]
            urltexts.append(urltext)

    return urltexts


def getsubUrllists(urltexts):
    base = 'http://artist.meishujia.cn/index.php?page=1&act=pps&smid=2&tag='
    suburllists = []
    for text in urltexts:
        test = text.encode('gb2312')
        test2 = parse.quote(test)
        subur = base + test2
        suburllists.append(subur)

    return suburllists


def loopHTML(suburllists):
    for sub in suburllists:              #第一层循环
        html = getHTMLText(sub)
        soup = BeautifulSoup(html, 'html.parser')
        page = 1
        a = soup.find('li', {'class': 'sert3'})
        pattern = '/.*页'
        page_sum = re.search(pattern, a.string)
        page_sum = int(page_sum.string[2:-1])
        while (page <= page_sum):       #第二层循环
            b = 'page=.'  # 修改url链接中的page=字段实现翻页
            result = re.sub(b, 'page=' + str(page), sub)
            html = getHTMLText(result)
            soup = BeautifulSoup(html, 'html.parser')
            page = page + 1
            try:
                for aa in soup.find_all('a', {'class': 'i42bs'}):     #第三层循环
                    ssuburl = aa.attrs['href']
                    keyword = aa.string
                    print(keyword, ':')
                    ssuburl = ssuburl + '/?said=528'
                    html = getHTMLText(ssuburl)
                    soup = BeautifulSoup(html, 'html.parser')
                    td = soup.find('td', {'align':'justify'})
                    plists = td.find_all('p')
                    if(len(plists) != 0):
                        for p in plists:
                            if(p.string != None):
                                print(p.string)
                    else:
                        print(td.get_text())
            except:
                print('该页面为空页~')


if __name__ == "__main__":
    url = "http://artist.meishujia.cn/"
    clas = "i92"
    html = getHTMLText(url)
    urltexts = getUrltexts(html, clas)
    suburllists = getsubUrllists(urltexts)
    loopHTML(suburllists)