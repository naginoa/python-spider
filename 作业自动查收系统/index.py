#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import csv
import pandas as pd

source = 'E:/素材'
sublist = []
filename = 'E:/素材'.decode('utf-8')
for i in os.listdir(filename):
    sublist.append(i.encode('utf-8'))

with open('result.csv', "w", ) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["学号", "姓名"])
    for i in sublist:
        sub_source = source+'/'+i
        filename = sub_source.decode('utf-8')
        for i in os.listdir(filename):
            name = i.encode('utf-8')
            if ' ' in name:
                if name.split(' ')[1] == '':
                    print name.split(' ')[0] if '.' not in name.split(' ')[0] else name.split(' ')[0][1:],name.split(' ')[2] #两个空格的情况
                    a = name.split(' ')[0] if '.' not in name.split(' ')[0] else name.split(' ')[0][1:]
                    b = name.split(' ')[2]
                    writer.writerow([a, b])
                else:
                    print name.split(' ')[0] if '.' not in name.split(' ')[0] else name.split(' ')[0][1:],name.split(' ')[1]
                    a = name.split(' ')[0] if '.' not in name.split(' ')[0] else name.split(' ')[0][1:]
                    b = name.split(' ')[1]
                    writer.writerow([a, b])
            if '-' in name:
                print name.split('-')[0] if '.' not in name.split('-')[0] else name.split('-')[0][1:],name.split('-')[1]
                a = name.split('-')[0] if '.' not in name.split('-')[0] else name.split('-')[0][1:]
                b = name.split('-')[1]
                writer.writerow([a, b])

df = pd.read_csv('result.csv')
df = df['学号'].value_counts()
df.to_csv('count.csv')