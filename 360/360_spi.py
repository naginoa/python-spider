import requests
import json
from bs4 import BeautifulSoup, Comment


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except:
        return "产生异常"


def htmlAnalyse(html, clas):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find_all('h3', {"class": clas})
    contents = content[:-6]
    for sub in contents:
        lists = sub.find_next_sibling().find_all("li")
        pos = 0
        for li in lists:
            pos = pos + 1
            print(sub.string, ":", li.a.string, pos, li.a.attrs["href"])


def ajaxjsonAnalyse(html):
    soup = BeautifulSoup(html, "html.parser")
    contents = soup.find_all('script')
    for content in contents:
        if '"view_name"' in str(content) and '"sites"' in str(content):
            stra = str(content.string)
            strlist = stra.split('=', 1)
            stra = strlist[1]
            strlist = stra.split(';', 1)
            jcontent = strlist[0].lstrip().rstrip()
            jsdict = json.loads(jcontent)
            datalist = jsdict['data']
            for data in datalist:
                sites = data['sites']
                pos = 0
                for site in sites:
                    pos = pos + 1
                    print(data['type_item']['view_name'], ":", site['name'], pos, site['url'])


if __name__ == "__main__":
    url = "https://hao.360.cn/"
    clas = "subtitle"
    html = getHTMLText(url)
    ajaxjsonAnalyse(html)
    htmlAnalyse(html,clas)
