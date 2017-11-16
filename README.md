# python-spider

python的一些爬虫

想写论文，但是好难啊。。。。被老师各种打击呀。。。

pagerank算法好难啊 出现孤立页面和阻尼系数之后的算法表达式为什么那么写啊

# 网易云课堂

帮北师大学姐做的 网易云课堂 爬虫和云词库 的期中作业

## 爬虫部分

如图:

![Image text](https://github.com/naginoasukara/python-spider/blob/master/%E7%BD%91%E6%98%93%E4%BA%91%E8%AF%BE%E5%A0%82/image/4.png)

网易云课堂的机制是通过payload中的json字段值来达到传输数据的作用。

pageindex表示从第几页开始，relativeoffset表示这些数据段所处的集合，orderType指是最新还是付费还是最热的方式。可以利用这些值来爬取网易云课堂的信息，并且使用的是post请求，还有headers中的cookies一定要去掉，否则会遭到屏蔽，出现403错误。

利用该机制,如下代码:

```python
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
```

结果展示：

![Image text](https://github.com/naginoasukara/python-spider/blob/master/%E7%BD%91%E6%98%93%E4%BA%91%E8%AF%BE%E5%A0%82/image/1.png)

## 词云图部分

北师大学姐提供的数据

做法:

1.将excel表格中的数据全部加入到一起。

2.使用jieba中文分词进行分词。



3.使用wordcloud进行统计词频，使用中文字体库，并且可以更换背景轮廓，进行制图。

代码：

```python

{import matplotlib.pyplot as plt  # 数学绘图库
import jieba  # 分词库
from wordcloud import WordCloud  # 词云库
from scipy.misc import imread
from os import path
import xlrd

# 1、读入xls文本数据
data = xlrd.open_workbook('data.xls')
table = data.sheets()[0]
nrows = table.nrows
text = ''
for i in range(nrows):
    colnames =  table.row_values(i) #某一行数据
    text += ','.join(colnames)

# 2、结巴分词，默认精确模式。可以添加自定义词典userdict.txt,然后jieba.load_userdict(file_name) ,file_name为文件类对象或自定义词典的路径
# 自定义词典格式和默认词库dict.txt一样，一个词占一行：每一行分三部分：词语、词频（可省略）、词性（可省略），用空格隔开，顺序不可颠倒

cut_text = jieba.cut(text)
result = "/".join(cut_text)  # 必须给个符号分隔开分词结果来形成字符串,否则不能绘制词云
print(result)

# 3、生成词云图，这里需要注意的是WordCloud默认不支持中文，所以这里需已下载好的中文字库
# 无自定义背景图：需要指定生成词云图的像素大小，默认背景颜色为黑色,统一文字颜色：mode='RGBA'和colormap='pink'
d = path.dirname(__file__)
round_coloring = imread(path.join(d, "maid.png"))
wc = WordCloud(font_path="Yahei.ttf", background_color='white', width=800,mask=round_coloring,
               height=600, max_font_size=50,
               max_words=150)  # ,min_font_size=10)#,mode='RGBA',colormap='pink')
wc.generate(result)
wc.to_file("wordcloud.png")  # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰

# 4、显示图片
plt.figure("词云图")  # 指定所绘图名称
plt.imshow(wc)  # 以图片的形式显示词云
plt.axis("off")  # 关闭图像坐标系
plt.show()
```

效果图:

![Image text](https://github.com/naginoasukara/python-spider/blob/master/%E7%BD%91%E6%98%93%E4%BA%91%E8%AF%BE%E5%A0%82/image/2.png)

![Image text](https://github.com/naginoasukara/python-spider/blob/master/%E7%BD%91%E6%98%93%E4%BA%91%E8%AF%BE%E5%A0%82/image/3.png)

在北师大大佬面前瑟瑟发抖

有人找我做淘宝......

# pagerank

\sum_{j = 1}^n a_{ij} = 1 \

<img src="http://latex.codecogs.com/gif.latex?P_i(n+1)=\sum_{j}P_j(n)P_{j->i}/N_j">             ①

<img src="http://latex.codecogs.com/gif.latex?P_{n+1}=HP_n">

<img src="http://latex.codecogs.com/gif.latex?P_{n}=H^nP_0">

<img src="http://latex.codecogs.com/gif.latex?x=\{a_1,a_2,...,a_m\}">
