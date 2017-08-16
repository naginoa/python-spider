import pymongo
import charts

client = pymongo.MongoClient('localhost',27017)
ceshi = client['copy']
item_info = ceshi['item_info']


def data_gen(types):    #产生chars字典迭代器
    length = 0
    if length <= len(area_index):    #长度控制在18
        for area,times in (zip(area_index, post_times)):
            data = {
                'name':area,
                'data':[times],
                'type':types
            }
            yield data
            length += 1


#数据清洗
for i in item_info.find():
    if len(i['area']) == 1:
        item_info.update_one({'_id':i['_id']},{'$set':{'area':'不明'}})
        #print('不明')
    elif len(i['area']) == 2 and '-' not in i['area'][1]:
        item_info.update_one({'_id':i['_id']},{'$set':{'area':'不明'}})
        #print('不明')
    elif len(i['area']) == 3:
        item_info.update_one({'_id':i['_id']},{'$set':{'area':'北京' + '-' + i['area'][0]}})
        #print('北京' + '-' + i['area'][0])
    else:
        item_info.update_one({'_id':i['_id']},{'$set':{'area':i['area'][1]}})
        #print(i['area'][1])

area_list = []
for i in item_info.find():
    if i['area'] != '不明':
        if '北京' in i['area']:
            area_list.append(i['area'].split('-')[1])
        else:
            area_list.append('其他省份')
area_index = list(set(area_list))
print(area_index)

post_times = []
for index in area_index:
    post_times.append(area_list.count(index))
print(post_times)

series = [data for data in data_gen('column')]
charts.plot(series, show='inline', options=dict(title=dict(text='58同城北京城区物品发帖量')))