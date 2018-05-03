#coding = utf-8
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame


headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
r = requests.get('http://www.moe.gov.cn/s78/A03/moe_560/jytjsj_2016/2016_qg/201708/t20170822_311603.html', headers=headers)
r.encoding = 'utf-8'
html = r.text
soup = BeautifulSoup(html, 'html.parser')
table = soup.find_all(id="content_body") 
df = pd.read_html(str(table[0]))
df = DataFrame(df[1])
print(df)
