import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '获取网站内容时出错'

def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr.find_all('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string,tds[3].string])

def printUnivList(ulist, num):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^1}"
    f = open('unirank.txt','w')
    f.write(tplt.format("排名","学校名称","总分",chr(12288)))
    for i in range(num):
        u = ulist[i]
        f.writelines("\n"+tplt.format(i+1,u[1],u[3],chr(12288)))
	
def main():
    uinfo = []
    url = "http://www.zuihaodaxue.com/zuihaodaxuepaiming2017.html"
    html = getHTMLText(url)
    fillUnivList(uinfo,html)
    printUnivList(uinfo,200)

main()