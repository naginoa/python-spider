import requests
from lxml import etree
import json
import csv


#获取课程的字典迭代器，n为参数代表爬取多少个
def get_course(n):
    kv = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '148',
        'Content-Type': 'application/json',
        # 'Cookie': 'EDUWEBDEVICE=8354b8579daf45ff9c03975e78001cbd; hasVolume=true; usertrack=ZUcIhlnjF1l5TAIEQvHiAg==; _ntes_nnid=afe5b7fa9ea41377ecb98165b1b55964,1508558871780; _ntes_nuid=afe5b7fa9ea41377ecb98165b1b55964; mail_psc_fingerprint=023d086130056e2fac916c0d7ebef32f; Province=0450; City=0451; __gads=ID=f1a4ce60f195323b:T=1509951825:S=ALNI_MYVAhThA7Cj-gBSAPwmJZ2KwY3VDQ; UM_distinctid=15f902463acd69-0aa48016badb1-19174438-e1000-15f902463adb88; vjuids=-2a5f8d593.15f9024807b.0.2162487b88141; vjlast=1509951832.1509951832.30; NTESSTUDYSI=2d7dbd458dc346a2973f7f872f396e7c; utm="eyJjIjoiIiwiY3QiOiIiLCJpIjoiIiwibSI6IiIsInMiOiIiLCJ0IjoiIn0=|aHR0cDovL3N0dWR5LjE2My5jb20vY2F0ZWdvcnkvcHl0aG9u"; __utma=129633230.614633666.1510318433.1510318433.1510318433.1; __utmb=129633230.38.9.1510321792497; __utmc=129633230; __utmz=129633230.1510318433.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        'edu-script-token': '1b50572d6c3b43ce830e27a913168f95',
        'Host': 'study.163.com',
        'Origin': 'http://study.163.com',
        'Referer': 'http://study.163.com/category/python',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'
    }
    #该url为获取课程信息的接口，抓包分析得知
    url2 = 'http://study.163.com/p/search/studycourse.json'
    for i in range(int(n/50)):
        payload = {
            'ctivityId': 0,
            'frontCategoryId': "-1",
            'orderType': 0,
            'pageIndex': i,
            'pageSize': 50,
            'priceType': -1,
            'relativeOffset': (i-1)*50,
            'searchTimeType': -1
        }
        r = requests.post(url2, data=json.dumps(payload), headers=kv)
        jr = json.loads(r.text)
        for j in jr['result']['list']:
            data = {
                'productName': j['productName'],
                'lectorName': j['lectorName'],
                'Price': j['originalPrice'],
                'learnerCount': j['learnerCount']
            }
            #迭代器返回
            yield data


if __name__ == '__main__':
    with open('course.csv', 'w', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['productName','lectorName','Price','learnerCount'])
        #爬取两千条数据
        for i in get_course(2000):
            #写入csv
            writer.writerow([i['productName'], i['lectorName'], i['Price'], i['learnerCount']])