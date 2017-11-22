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

## 1.基本思路

在互联网上， 与论文的引用相类似的是显然是网页的链接。 因此， 佩奇和布林萌生了一个网页排序的思路， 那就是通过研究网页间的相互链接来确定排序。 具体地说， 一个网页被其它网页链接得越多， 它的排序就应该越靠前。 不仅如此， 佩奇和布林还进一步提出， 一个网页越是被排序靠前的网页所链接， 它的排序就也应该越靠前。 这一条的意义也是不言而喻的， 就好比一篇论文被诺贝尔奖得主所引用， 显然要比被普通研究者所引用更说明其价值。 依照这个思路， 网页排序问题就跟整个互联网的链接结构产生了关系， 正是这一关系使它成为了一个不折不扣的数学问题。 
思路虽然有了， 具体计算却并非易事， 因为按照这种思路， 想要知道一个网页 Wi 的排序， 不仅要知道有多少网页链接了它， 而且还得知道那些网页各自的排序——因为来自排序靠前网页的链接更有分量。 但作为互联网大家庭的一员， Wi 本身对其它网页的排序也是有贡献的， 而且基于来自排序靠前网页的链接更有分量的原则， 这种贡献与 Wi 本身的排序也有关。 这样一来， 我们就陷入了一个 “先有鸡还是先有蛋” 的循环： 要想知道 Wi 的排序， 就得知道与它链接的其它网页的排序， 而要想知道那些网页的排序， 却又首先得知道 Wi 的排序。 为了打破这个循环， 佩奇和布林采用了一个很巧妙的思路， 即分析一个虚拟用户在互联网上的漫游过程。 他们假定： 虚拟用户一旦访问了一个网页后， 下一步将有相同的几率访问被该网页所链接的任何一个其它网页。 换句话说， 如果网页 Wi 有 Ni 个对外链接， 则虚拟用户在访问了 Wi 之后， 下一步点击那些链接当中的任何一个的几率均为 1/Ni。 初看起来， 这一假设并不合理， 因为任何用户都有偏好， 怎么可能以相同的几率访问一个网页的所有链接呢？ 但如果我们考虑到佩奇和布林的虚拟用户实际上是对互联网上全体用户的一种平均意义上的代表， 这条假设就不象初看起来那么不合理了。 那么网页的排序由什么来决定呢？ 是由该用户在漫游了很长时间——理论上为无穷长时间——后访问各网页的几率分布来决定， 访问几率越大的网页排序就越靠前。 

为了将这一分析数学化， 我们用 pi(n) 表示虚拟用户在进行第 n 次浏览时访问网页 Wi 的几率。 显然， 上述假设可以表述为 (请读者自行证明)： a
<img src="http://latex.codecogs.com/gif.latex?P_i(n+1)=\sum_{j}P_j(n)P_{j->i}/N_j">   

为符号简洁起见， 我们将虚拟用户第 n 次浏览时访问各网页的几率合并为一个列向量 pn， 它的第 i 个分量为 pi(n)， 并引进一个只与互联网结构有关的矩阵 H， 它的第 i 行 j 列的矩阵元为 Hij = pj→i/Nj， 则上述公式可以改写为： 

<img src="http://latex.codecogs.com/gif.latex?P_{n+1}=HP_n">

熟悉随机过程理论的读者想必看出来了， 上述公式描述的是一种马尔可夫过程 (Markov process)， 而且是其中最简单的一类， 即所谓的平稳马尔可夫过程 (stationary Markov process)， 而 H 则是描述马尔可夫过程中的转移概率分布的所谓转移矩阵 (transition matrix)。 不过普通马尔可夫过程中的转移矩阵通常是随机矩阵 (stochastic matrix)， 即每一列的矩阵元之和都为 1 的矩阵 (请读者想一想， 这一特点的 “物理意义” 是什么？)。 而我们的矩阵 H 却可能有一些列是零向量， 从而矩阵元之和为 0， 它们对应于那些没有对外链接的网页， 即所谓的 “悬挂网页” (dangling page)。 
<img src="http://latex.codecogs.com/gif.latex?P_{n}=H^nP_0">
\其中 p0 为虚拟读者初次浏览时访问各网页的几率分布 (在佩奇和布林的原始论文中， 这一几率分布被假定为是均匀分布)。\
## 2.问题及解决

如前所述， 佩奇和布林是用虚拟用户在经过很长——理论上为无穷长——时间的漫游后访问各网页的几率分布， 即 limn→∞pn， 来确定网页排序的。 这个定义要想管用， 显然要解决三个问题： 

1.极限 limn→∞pn 是否存在？

2.如果极限存在， 它是否与 p0 的选取无关？
如果极限存在， 并且与 p0 的选取无关， 它作为网页排序的依据是否真的合理？
如果这三个问题的答案都是肯定的， 那么网页排序问题就算解决了。 反之， 哪怕只有一个问题的答案是否定的， 网页排序问题也就不能算是得到了满意解决。 那么实际答案如何呢？ 很遗憾， 是后一种， 而且是其中最糟糕的情形， 即三个问题的答案全都是否定的。 这可以由一些简单的例子看出。 比方说， 在只包含两个相互链接网页的迷你型互联网上， 如果 p0 = (1, 0)T， 极限就不存在 (因为几率分布将在 (1, 0)T 和 (0, 1)T 之间无穷振荡)。 而存在几个互不连通 (即互不链接) 区域的互联网则会使极限——即便存在——与 p0 的选取有关 (因为把 p0 选在不同区域内显然会导致不同极限)。 至于极限存在， 并且与 p0 的选取无关时它作为网页排序的依据是否真的合理的问题， 虽然不是数学问题， 答案却也是否定的， 因为任何一个 “悬挂网页” 都能象黑洞一样， 把其它网页的几率 “吸收” 到自己身上 (因为虚拟用户一旦进入那样的网页， 就会由于没有对外链接而永远停留在那里)， 这显然是不合理的。 这种不合理效应是如此显著， 以至于在一个连通性良好的互联网上， 哪怕只有一个 “悬挂网页”， 也足以使整个互联网的网页排序失效， 可谓是 “一粒老鼠屎坏了一锅粥”。 
为了解决这些问题， 佩奇和布林对虚拟用户的行为进行了修正。 首先， 他们意识到无论真实用户还是虚拟用户， 当他们访问到 “悬挂网页” 时， 都不应该也不会 “在一棵树上吊死”， 而是会自行访问其它网页。 对于真实用户来说， 自行访问的网页显然与各人的兴趣有关， 但对于在平均意义上代表真实用户的虚拟用户来说， 佩奇和布林假定它将会在整个互联网上随机选取一个网页进行访问。 用数学语言来说， 这相当于是把 H 的列向量中所有的零向量都换成 e/N (其中 e 是所有分量都为 1 的列向量， N 为互联网上的网页总数)。 如果我们引进一个描述 “悬挂网页” 的指标向量 (indicator vector) a， 它的第 i 个分量的取值视 Wi 是否为 “悬挂网页” 而定——如果是 “悬挂网页”， 取值为 1， 否则为 0——并用 S 表示修正后的矩阵， 则： 

<img src="http://latex.codecogs.com/gif.latex?S=H+ea^t/N">

显然， 这样定义的 S 矩阵的每一列的矩阵元之和都是 1， 从而是一个不折不扣的随机矩阵。 这一修正因此而被称为随机性修正 (stochasticity adjustment)。 这一修正相当于剔除了 “悬挂网页”， 从而可以给上述第三个问题带来肯定回答 (当然， 这一回答没有绝对标准， 可以不断改进)。 不过， 这一修正解决不了前两个问题。 为了解决那两个问题， 佩奇和布林引进了第二个修正。 他们假定， 虚拟用户虽然是虚拟的， 但多少也有一些 “性格”， 不会完全受当前网页所限， 死板地只访问其所提供的链接。 具体地说， 他们假定虚拟用户在每一步都有一个小于 1 的几率 α 访问当前网页所提供的链接， 同时却也有一个几率 1-α 不受那些链接所限， 随机访问互联网上的任何一个网站。 用数学语言来说 (请读者自行证明)， 这相当于是把上述 S 矩阵变成了一个新的矩阵 G： 

<img src="http://latex.codecogs.com/gif.latex?G=aS+(1-a)ee^T/N">

这个矩阵不仅是一个随机矩阵， 而且由于第二项的加盟， 它有了一个新的特点， 即所有矩阵元都为正 (请读者想一想， 这一特点的 “物理意义” 是什么？)， 这样的矩阵是所谓的素矩阵 (primitive matrix)。 这一修正因此而被称为素性修正 (primitivity adjustment)。 
经过这两类修正， 网页排序的计算方法就变成了：

<img src="http://latex.codecogs.com/gif.latex?P_n=G^nP_0">

## 3.pagerank简单计算实现：

如果网页T存在一个指向网页A的连接，则表明T的所有者认为A比较重要，从而把T的一部分重要性得分赋予A。这个重要性得分值为：PR（T）/L(T)

其中PR（T）为T的PageRank值，L(T)为T的出链数，则A的PageRank值为一系列类似于T的页面重要性得分值的累加。，即一个页面的得票数由所有链向它的页面的重要性来决定，到一个页面的超链接相当于对该页投一票。一个页面的PageRank是由所有链向它的页面（链入页面）的重要性经过递归算法得到的。一个有较多链入的页面会有较高的等级，相反如果一个页面没有任何链入页面，那么它没有等级。

假设一个由只有4个页面组成的集合：A，B，C和D。如果所有页面都链向A，那么A的PR（PageRank）值将是B，C及D的和。

<img src="http://img.my.csdn.net/uploads/201209/20/1348120060_7086.png">
       
继续假设B也有链接到C，并且D也有链接到包括A的3个页面。一个页面不能投票2次。所以B给每个页面半票。以同样的逻辑，D投出的票只有三分之一算到了A的PageRank上。

<img src="http://img.my.csdn.net/uploads/201209/20/1348120099_6078.png">
       
换句话说，根据链出总数平分一个页面的PR值。

<img src="http://img.my.csdn.net/uploads/201209/20/1348120123_5802.png">

由于存在一些出链为0，也就是那些不链接任何其他网页的网， 也称为孤立网页，使得很多网页能被访问到。因此需要对 PageRank公式进行修正，即在简单公式的基础上增加了阻尼系数（damping factor）q， q一般取值q=0.85。

其意义是，在任意时刻，用户到达某页面后并继续向后浏览的概率。 1- q= 0.15就是用户停止点击，随机跳到新URL的概率）的算法被用到了所有页面上，估算页面可能被上网者放入书签的概率。

最后，即所有这些被换算为一个百分比再乘上一个系数q。由于下面的算法，没有页面的PageRank会是0。所以，Google通过数学系统给了每个页面一个最小值。

<img src="http://img.my.csdn.net/uploads/201209/20/1348120862_4424.png">
      
这个公式就是.S Brin 和 L. Page 在《The Anatomy of a Large- scale Hypertextual Web Search Engine Computer Networks and ISDN Systems 》定义的公式。

-------------------------------------------

重点来了！！！！！

在最后一个式子中，阻尼系数乘原来的式子表示有该几率是原来的情况。而（1-q）表示会有（1-q）的几率跳转到一个新的页面，那么为何计算pagerank值是直接加（1-q）而不是（1-q）*1/N，1/N 表示 随机跳转到一个页面的几率，符合之前的思想。

查阅资料，英文版的wiki：

<a href="https://en.wikipedia.org/wiki/PageRank" >点此跳转</a>

其中有提到，英文原文的公式是上图，但是再后来的时候有修改为我们一个认为的正确的方式：

<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/7c3da6d608ba21cac0bbfc96e59615ffe8f33360">

然后我分别使用了pygragh模块，制作了简单的图和实现。还有MapReduce版本的，注释在代码中，详情可以去看。

## pagerank总结

谷歌的两位创始人在提出这个伟大算法的前提下，都是在数学知识储备非常充足的前提下，无论是公式的证明，极限的存在与否，马尔科夫模型的理解程度。并且和之前学习的机器学习算法有想通之处，就是讲一堆变量抽象为向量，使用向量进行计算。和朱老师聊过之后，何为数学思想，就是将现实的问题抽象为数学问题，数学建模也好，算法的创新也好，这个抽象为数学的思想，正是我们计算机人所缺少的。因此学习数学尤为重要。




