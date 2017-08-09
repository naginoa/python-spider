import pymongo

client = pymongo.MongoClient('localhost', 27017)
walden = client['walden']
sheet_lines = walden['sheet_lines']

with open('la.txt') as f:
    lines = f.readlines()
    for a, b in enumerate(lines):
        data = {
            'index': a,
            'line': b,
            'words': len(b.split())
        }
        if data['line'] != ' \n':  # 清洗
            # print(data)
            sheet_lines.insert_one(data)
#$lt/$lte/$gt/$gte/$ne   依次等价于</<=/>/>=/!=
for item in sheet_lines.find({'words':{'$lt':30}}):
    print(item)
