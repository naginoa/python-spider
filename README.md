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
table = data.sheets()[0]nrows = table.nrows
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

用方法， 那就是看论文的引用次数。 在互联网上， 与论文的引用相类似的是显然是网页的链接。 因此， 佩奇和布林萌生了一个网页排序的思路， 那就是通过研究网页间的相互链接来确定排序。 具体地说， 一个网页被其它网页链接得越多， 它的排序就应该越靠前。 不仅如此， 佩奇和布林还进一步提出， 一个网页越是被排序靠前的网页所链接， 它的排序就也应该越靠前。 这一条的意义也是不言而喻的， 就好比一篇论文被诺贝尔奖得主所引用， 显然要比被普通研究者所引用更说明其价值。 依照这个思路， 网页排序问题就跟整个互联网的链接结构产生了关系， 正是这一关系使它成为了一个不折不扣的数学问题。 

思路虽然有了， 具体计算却并非易事， 因为按照这种思路， 想要知道一个网页 Wi 的排序， 不仅要知道有多少网页链接了它， 而且还得知道那些网页各自的排序——因为来自排序靠前网页的链接更有分量。 但作为互联网大家庭的一员， Wi 本身对其它网页的排序也是有贡献的， 而且基于来自排序靠前网页的链接更有分量的原则， 这种贡献与 Wi 本身的排序也有关。 这样一来， 我们就陷入了一个 “先有鸡还是先有蛋” 的循环： 要想知道 Wi 的排序， 就得知道与它链接的其它网页的排序， 而要想知道那些网页的排序， 却又首先得知道 Wi 的排序。 

为了打破这个循环， 佩奇和布林采用了一个很巧妙的思路， 即分析一个虚拟用户在互联网上的漫游过程。 他们假定： 虚拟用户一旦访问了一个网页后， 下一步将有相同的几率访问被该网页所链接的任何一个其它网页。 换句话说， 如果网页 Wi 有 Ni 个对外链接， 则虚拟用户在访问了 Wi 之后， 下一步点击那些链接当中的任何一个的几率均为 1/Ni。 初看起来， 这一假设并不合理， 因为任何用户都有偏好， 怎么可能以相同的几率访问一个网页的所有链接呢？ 但如果我们考虑到佩奇和布林的虚拟用户实际上是对互联网上全体用户的一种平均意义上的代表， 这条假设就不象初看起来那么不合理了。 那么网页的排序由什么来决定呢？ 是由该用户在漫游了很长时间——理论上为无穷长时间——后访问各网页的几率分布来决定， 访问几率越大的网页排序就越靠前。 

为了将这一分析数学化， 我们用 pi(n) 表示虚拟用户在进行第 n 次浏览时访问网页 Wi 的几率。 显然， 上述假设可以表述为 (请读者自行证明)： 

<img src="http://latex.codecogs.com/gif.latex?P_i(n+1)=\sum_{j}P_j(n)P_{j->i}/N_j">             

<img src="http://latex.codecogs.com/gif.latex?P_{n+1}=HP_n">

<img src="http://latex.codecogs.com/gif.latex?P_{n}=H^nP_0">

<img src="http://latex.codecogs.com/gif.latex?S=H+ea^t/N">

<img src="http://latex.codecogs.com/gif.latex?G=αS+(1-α)ee^T/N">

<img src="http://latex.codecogs.com/gif.latex?P_n=G^nP_0">
