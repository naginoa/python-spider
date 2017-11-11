# python-spider

python的一些爬虫

帮北师大学姐做的 网易云课堂 爬虫和云词库 的其中作业

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



