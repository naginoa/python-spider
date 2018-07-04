#coding=utf-8
import os
import urllib
import socket
from PIL import Image
# urllib.urlretrieve(url,saveFile)
import requests
import threading
import multiprocessing


global root_dir
global txt_file
global true_name
global false_name
global true_image
global false_image
global num


root_dir = ''
txt_file = 'annotation_clean_train.txt'
true_name = 'true_txt.txt'
false_name = 'false_txt.txt'
true_image = 'true_image'
false_image = 'false_image'


def gene_jgplist(txt_file):
    jpg_list = []
    with open(os.path.join(root_dir, txt_file)) as f:
        for i in f.readlines():
            jpg_list.append(i)
    return jpg_list

def download_image(root_dir,jpg,true_name,false_name,true_image,false_image,num):
    #T = open(os.path.join(root_dir,true_name),'a')
    #F = open(os.path.join(root_dir,false_name),'a')
    socket.setdefaulttimeout(7)
    #for num,i in enumerate(jpg_list[0]):

    try:
        # save image with image_name
        save_root = os.path.join(root_dir,true_image)+'/{}'.format(jpg.split()[0].split('/')[-1])
        print(save_root)
        r =requests.get(jpg.split()[0])
        if r.status_code==200:
            with open(save_root,'wb') as c:
                c.write(r.content)
            if is_jpg2(save_root):
                if is_jpg(save_root):
                    text = jpg.split()[1] + ',' + jpg.split()[0].split('/')[-1] + '\n'
                    with open(os.path.join(root_dir, true_name), 'a') as T:
                        T.write(text)  # jpg.split()[1] = class
                    print('begin-' + str(num) + '-OK', text)
                else:
                    false_path = os.path.join(root_dir, false_image)
                    os.system("mv '{}' '{}'".format(save_root, false_path))
                    with open(os.path.join(root_dir,false_name),'a') as F:
                        F.write(jpg.split()[0] + '\n')
                    print('ERROR IMAGE-' + str(num), jpg.split()[0])
            else:
                false_path = os.path.join(root_dir, false_image)
                os.system("mv '{}' '{}'".format(save_root, false_path))
                with open(os.path.join(root_dir, false_name), 'a') as F:
                    F.write(jpg.split()[0] + '\n')
                print('ERROR IMAGE-' + str(num), jpg.split()[0])
        else:
            with open(os.path.join(root_dir, false_name), 'a') as F:
                F.write(jpg.split()[0] + '\n')
            print('JUMP-Enter-name-pass' + str(num), jpg.split()[0])

    # print(i.split()[0].split('/')[-1])
    except Exception as  e:
        with open(os.path.join(root_dir, false_name), 'a') as F:
            F.write(jpg.split()[0]+'\n')
        print('ERROR IMAGE-'+str(num),jpg.split()[0])


def is_jpg(filename):
    data = open(filename, 'rb').read(11)
    if data[:4] != '\xff\xd8\xff\xe0' and data[:4] != '\xff\xd8\xff\xe1':
        return False
    if data[6:] != 'JFIF\0' and data[6:] != 'Exif\0':
        return False
    return True

def is_jpg2(filename):
    try:
        i=Image.open(filename)
        return i.format =='JPEG'
    except IOError:
        return False

def download(jpg, num):
    download_image(root_dir, jpg, true_name, false_name, true_image, false_image, num)

def run_func(args):
    download(args[0], args[1])

if __name__ == '__main__':
    jpg_list = gene_jgplist(txt_file)
    tasks =  [(y, x) for x, y in enumerate(jpg_list)]
    pool = multiprocessing.Pool(4)
    pool.map(run_func, tasks)
    pool.close()
    pool.join()
    # download_image(root_dir, txt_file, true_name, false_name, true_image,false_image)
    # run_is(url)