#-*-coding:utf-8 -*-
#使用python抓取智联招聘网职位数据
import io
import sys
import math
import requests,pymysql
from pymysql import cursors
from bs4 import BeautifulSoup
from lxml import etree 
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')   

class jobs():
    def __init__(self):
        self.HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }
        self.ALL_CITY = ['北京','上海','广州','深圳','杭州','天津','武汉','西安','成都','海口','南宁','南京','苏州','合肥','济南','青岛','无锡','宁波','大连','重庆','郑州','长沙','福州','厦门','石家庄','太原','昆明','佛山','南昌','贵阳','呼和浩特']
        self.City = input("输入想要工作的城市:")
        self.Keyword = input("输入工作的关键词:")
        self.CollectionName = str(self.Keyword+'_'+self.City)
        self.CONNECTION = pymysql.connect(host='localhost',user='root',password='llj',db='dataset',charset='utf8',cursorclass=pymysql.cursors.DictCursor)    
        self.SQL = "INSERT INTO "+self.CollectionName+" (职位名称,公司名称,公司链接,职位链接,职位月薪,工作地点,发布日期,工作性质,工作经验,最低学历,招聘人数,职位类别,岗位职责描述,福利标签) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    def city_start(self):
        #启动函数，主要用来判断搜索城市【关键词】，如果指定城市，则正常调用main()执行程序；
        #若指定关键词==‘全国’，则对ALL_CITY列表中的城市依次调用main()函数进行遍历！
        if self.City=='全国':
            for item in self.ALL_CITY:
                Originpage = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=' + item + '&kw=' + self.Keyword + '&sm=0&p='
                self.mainfunction(Originpage)
                print('---------------------------------------------------------------\n')
                print(item+"所有与"+self.Keyword+"相关的工作职位已经被保存到数据库中！")
        else:
            Originpage = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=' + self.City + '&kw=' + self.Keyword + '&sm=0&p='
            self.mainfunction(Originpage)

    def mainfunction(self,Originpage):
        #函数主体，首先计算当前关键词生成的目标职位的总页面数，通过homepage()进行获取页面上职位链接、翻页递归
        #homepage()通过调用jobpage()来对当前页面所有职位链接进行遍历，获取每一条职位链接页面中的详细信息，然后通过save_mysql()存储！
        pagenum = self.total_page_number(str(Originpage+'1'))
        max_pagelength = 90 if pagenum>=90 else pagenum
        
        for i in range(1,max_pagelength+1):
            pageurl = Originpage + str(i)
            print("------------------------------------------------------------\n当前页面"+str(i)+"的职位链接:\n",pageurl)
            #获取页面上所有的职位链接，存在列表里，等待遍历具体职位页面的信息
            joblink_list = self.homepage(pageurl)
            #获取完所有职位链接后，判断当前页码是否<总页码数，是则停止，否跳转到下一页，继续遍历！
            length=len(joblink_list)+1 if len(joblink_list)<=60 else 61
            for j in range(1,length):
                try:
                    jobdata = self.jobpage(joblink_list[j-1])
                    self.save_mysql(jobdata,j)
                except Exception as e:
                    print(repr(e))
                    pass
        print("完成!")


    def total_page_number(self,url):
        #获取页面职位总数，用于下一步判断翻页的页数和函数循环执行次数的确定
        req = requests.get(url=url, headers=self.HEADERS)
        totalnum = etree.HTML(req.text).xpath('/html/body/div[3]/div[3]/div[2]/span[1]/em')[0].text
        pagenum = math.ceil(float(totalnum)/60)
        print('总共有'+str(totalnum) +'个关于'+self.Keyword +'的工作职位在'+self.City+' ->总页数 :'+str(pagenum)+'页')
        return pagenum

    def homepage(self,homeurl):   
        joblink_list = []
        try:
            req = requests.get(homeurl, headers=self.HEADERS)
            soup = BeautifulSoup(req.text,"lxml")
        except Exception as e:
            print(repr(e))
            self.homepage(homeurl)
        for item in soup.find_all("td",{"zwmc"}):
            if item.a is not None:
                if item.a.attrs['href'] is not None:
                    joblink_list.append(item.a.attrs['href'])
        return joblink_list

    def jobpage(self,joburl):
        #根据传入的参数【joburl】网址链接，获取该链接下的所有职位信息，并以jobdata【列表】形式返回
        print('------------------------------------------------------------\n' + joburl)
        req = requests.get(joburl,headers=self.HEADERS)
        page_obj = BeautifulSoup(req.text,"lxml")
        string1 = string2 = ''
        details = []
        职位链接 = joburl.strip().strip('\n')
        职位名称=公司名称=公司链接=职位月薪=工作地点=发布日期=工作性质=工作经验=最低学历=招聘人数=职位类别=岗位职责描述=福利标签=''
        try:
            obj1 = page_obj.find("div",{"class":"inner-left fl"})
            obj2 = page_obj.find("ul",{"class":"terminal-ul clearfix"})
            obj3 = page_obj.find("div",{"class":"tab-inner-cont"})
            obj4 = page_obj.find("div",{"class":"welfare-tab-box"})
            职位名称 = obj1.find("h1").get_text().strip().strip('\n')
            公司名称 = obj1.find("h2").get_text().strip().strip('\n')
            公司链接 = obj1.find("h2").find("a")["href"].strip().strip('\n')
            for item in obj2.find_all("strong"):
                details.append(item.get_text().strip().strip('\n'))
            职位月薪,工作地点,发布日期,工作性质,工作经验,最低学历,招聘人数,职位类别=details[0],details[1],details[2],details[3],details[4],details[5],details[6],details[7]
            for item in obj3.find_all("p"):
                string1 += item.get_text().strip().strip('\n')
            岗位职责描述 = string1
            for item in obj4.find_all("span"):
                string2 += item.get_text().strip().strip('\n')
            福利标签 = string2
        except Exception as e:
            print(repr(e))
            职位名称=公司名称=公司链接='无链接'
            职位月薪=工作地点=发布日期=工作性质=工作经验=最低学历=招聘人数=职位类别=岗位职责描述=福利标签='无内容'
        finally:
            jobdata = [职位名称,公司名称,公司链接,职位链接,职位月薪,工作地点,发布日期,工作性质,工作经验,最低学历,招聘人数,职位类别,岗位职责描述,福利标签]
            return jobdata

    def save_mysql(self,j_list,count):
        print('###########################################')
        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(self.SQL,(j_list[0],j_list[1],j_list[2],j_list[3],j_list[4],j_list[5],j_list[6],j_list[7],j_list[8],j_list[9],j_list[10],j_list[11],j_list[12],j_list[13]))
            self.CONNECTION.commit()
            print(j_list)
            print("当前页面中有"+str(count)+"个职位已经保存至数据库中!")
        except Exception as e:
            print(repr(e))

tasks = jobs()
tasks.city_start()
