import requests
import time

def gettime():
    try:
        localtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        return localtime
    except:
	    return "获取时间发生错误"
		
def getHTMLText(url):
    try:
        kv = {'user-agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}
        r = requests.get(url, headers = kv)
        r.raise_for_status()
        if("360" in url):
            r.encoding = 'utf-8'
        else:
            r.encoding = r.apparent_encoding
        return r.text
    except:
        return "爬取网页产生异常"
	
if __name__=="__main__":
    lib=["https://www.hao123.com/","https://www.2345.com/","https://hao.360.cn/"]
    listnum=0
    for url in lib:
        listnum=listnum+1
        filename="spider"+str(listnum)+"_"+gettime()+'.txt'
        print(getHTMLText(url))
        print(filename)
        with open(filename,'w',encoding='utf-8') as f:
            f.write(getHTMLText(url))
            f.close()
