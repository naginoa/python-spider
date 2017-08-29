import pymongo
import charts

client = pymongo.MongoClient('localhost',27017)
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

calc = 0
calc2 = 0
calc3 = 0
for i in item_info.find():
    if '面议' not in i['price']:
        if '万' not in i['price']:
            if int(i['price']) > 2500 and int(i['price']) < 3000:
                calc += 1
        else:
            calc2 += 1
print(calc, calc2)

def gen_data():
    calc = 0
    for i in item_info.find():
    if '面议' not in i['price']:
        if '万' not in i['price']:
            if int(i['price']) < 100:
                calc += 1
            if int(i['price']) > 2500 and int(i['price']) < 3000:
                calc += 1