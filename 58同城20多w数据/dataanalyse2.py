http: // www.cnblogs.com / TTyb / p / 6051366.
html
import pymongo
import charts

client = pymongo.MongoClient('localhost', 27017)
ceshi = client['copy']
item_info = ceshi['item_info']

'''for i in item_info.find():             #数据清洗
    if '现价' in i['price']:
        item_info.update_one({'_id':i['_id']},{'$set':{'price':i['price'].split('：')[1].split('元')[0]}})
    else:
        if '元' in i['price']:
            item_info.update_one({'_id':i['_id']},{'$set':{'price':i['price'].split(' ')[0]}})
        else:
            pass
'''

re_list = []


def gen_data(pre, after, re_list):
    calc = 0
    for i in item_info.find():
        if '面议' not in i['price']:
            if '万' not in i['price']:
                if int(i['price']) > pre and int(i['price']) < after:
                    calc += 1
    sub_list = [str(pre) + '-' + str(after), calc]
    re_list.append(sub_list)


key_list = [[0, 100], [100, 500], [500, 1000], [1000, 1500], [1500, 2000], [2000, 2500], [2500, 3000], [3000, 3500],
            [3500, 4000], [4000, 4500], [4500, 5000]]


def final_data(key_list, re_list):
    calc = 0
    for key in key_list:
        gen_data(key[0], key[1], re_list)
        gen_data(5000, 10000, re_list)
    for i in item_info.find():
        if '万' in i['price']:
            calc += 1
    re_list.append(['万元以上', calc])
    calc = 0
    for i in item_info.find():
        if '面议' in i['price']:
            calc += 1
    re_list.append(['面议', calc])


final_data(key_list, re_list)
print(re_list)

options = {
    'charts': {'zoomType': 'xy'},
    'title': {'text': '58北京地区物品价格对比'},
    'subtitle': {'text': '来自风平浪静的明天'}
}
series = [{
    'type': 'pie',
    'name': 'Browser share',
    'data': [data for data in re_list],
}]
charts.plot(series, show='inline', options=options)
