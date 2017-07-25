import requests
from bs4 import BeautifulSoup, Comment

def getHTMLText(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"
	
def htmlAnalyse(html, clas, name = ""):
    soup = BeautifulSoup(html,"html.parser")
    source = soup.find('a', {"class":clas}, string = name)
    bro = source.find_next_sibling().find_all('a')
    pos = 0
    for text in bro:
        pos = pos+1
        print(source.string, ":", text.string, pos, text.attrs['href'])
		
def htmlAnalyse2(html, clas, name = ""):
    soup = BeautifulSoup(html,"html.parser")
    source = soup.find('a', {"class":clas},string = name)
    pos = 0
    for son in source.parent.find_next_sibling().find_next_siblings():
        pos = pos+1
        print(source.string, ":", son.a.string, pos, son.a.attrs['href'])

def codeAnalyse(html, clas, name = ""):
    soup = BeautifulSoup(html,"html.parser")
    source = soup.find('code', id = "__cnt_0_4")
    soup = BeautifulSoup(str(source),"html.parser")
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    soup = BeautifulSoup(comments[0],"html.parser")
    source = soup.find('a', {"class":clas},string = name)
    pos = 0
    for son in source.parent.find_next_sibling().find_next_siblings():
        pos = pos+1
        print(source.string, ":", son.a.string, pos, son.a.attrs['href'])

def print_Result(html):
    htmlAnalyse(html, clas[0], namelist[0])
    clac = 1;
    while(clac < len(namelist)):
        htmlAnalyse(html, clas[1],namelist[clac])
        clac = clac+1
    clac = 0
    while(clac < len(namelist2)):
        htmlAnalyse2(html, clas[2],namelist2[clac])
        clac = clac+1
    clac = 0
    while(clac < len(namelist3)):
        codeAnalyse(html, clas[2],namelist3[clac])
        clac = clac+1
	
if __name__=="__main__":
    url = "https://www.hao123.com/"
    clas = ["guesslike-industry-title g-ib s-fc20 s-fc20h 1","guesslike-industry-title g-ib s-fc20 s-fc20h ","coolsite-itemname s-fc20"]
    namelist = ["游戏","优选","生活","新热","健康"]
    namelist2 = ["推 荐","视 频","影 视","游 戏","新 闻","军 事"]
    namelist3 = ["体 育","购 物","商 城","旅 游","小 说","手 机","社 交","直 播","软 件","招 聘","汽 车","页 游","网 游",
    "动 漫","音 乐","金 融","财 经","女 性","彩 票","银 行","邮 箱","酷 站"]
    html = getHTMLText(url)
    print_Result(html)