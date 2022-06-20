# -*- coding: utf-8 -*-
'''
@Time    : 6/7/2022 5:06 PM
@Author  : dong.yachao
'''

import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import argparse
import glob

from pathlib import Path
import glob
import random




# box: [0,6], line:[6], key_point:[7, 14]
classes = ['truck', 'van', 'car', 'slagcar', 'bus', 'fire_truck',
           'police_car', 'ambulance',  'SUV', 'microbus', 'unknown_vehicle',
           'plate', 'double_plate']

vehicle_color = ['white', 'silver', 'grey', 'black', 'red', 'blue', 'yellow', 'green', 'brown', 'others']

abs_path = os.getcwd()


def convert(size, box):
    # box: xmin, xmax, ymin, ymax
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id, xml_path='/project/train/src_repo/dataset/xmls/',
                       txt_dir_path='/project/train/src_repo/dataset/labels/'):
    # print('xml_dir_path:', xml_dir_path)
    in_file = open(xml_path, encoding='utf-8')
    out_file = open(txt_dir_path + image_id + '.txt', 'w')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    # car bbox obj
    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        # 获取类别
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)

        # 获取bbox
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        # bbox转换 xyxy 转换为 xywh(0~1)
        # bb = convert((w, h), b)
        bb = (b[0]/w, b[2]/h, b[1]/w, b[3]/h)

        # 获取颜色
        color = obj.find('attributes').find('attribute').find('value').text
        if color not in vehicle_color:
            continue
        color_id = vehicle_color.index(color)

        # 写入 cls_id + color_id + bbox
        out_file.write(str(cls_id) + " " + str(color_id) + " " + " ".join([str(a) for a in bb]))
        # 换行
        out_file.write('\n')

    # plate poly obj
    for obj in root.iter('polygon'):
        # difficult = obj.find('difficult').text

        # 获取类别
        cls = obj.find('class').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)

        # 获取颜色
        color = ' '
        for attribute in obj.find('attributes').iter('attribute'):
            if attribute.find('name').text == 'color':
                color = attribute.find('value').text

        if color not in vehicle_color:
            continue
        color_id = vehicle_color.index(color)

        # 获取bbox
        points = obj.find('points').text
        points = points.split(';')   # ["x1,y1", "x2,y3", "x3,y3","x4,y4"]
        poly = []
        for i in points:
            x = float(i.split(',')[0]) / w
            y = float(i.split(',')[1]) / h
            poly.append(x)
            poly.append(y)

        # 写入 cls_id + color_id + poly
        out_file.write(str(cls_id) + " " + str(color_id) + " " + " ".join([str(a) for a in poly]))
        # 换行
        out_file.write('\n')

        
        

def gen_imgs_path():
    
    
    # 生成训练测试集，写入txt文件中
    with open('/home/data/vehicle_data/all_det_imgs.txt', 'r') as f1:
        all_det = f1.readlines()
        random.shuffle(all_det)
        
        num_imgs = len(all_det)
        train_percent = 0.9
        train_abs_img_paths = all_det[:int(train_percent*num_imgs)]
        test_abs_img_paths = all_det[int(train_percent*num_imgs):]
    
        with open('/home/data/vehicle_data/train.txt', 'w') as f1:
            for train_pwd in train_abs_img_paths:
                f1.write(train_pwd)

        with open('/home/data/vehicle_data/test.txt', 'w') as f1:
            for test_pwd in test_abs_img_paths:
                f1.write(test_pwd)

        with open('/home/data/vehicle_data/val.txt', 'w') as f1:
            for val_pwd in test_abs_img_paths:
                f1.write(val_pwd)
        

if __name__ == '__main__':
    
    # 获取所有的img路径
    

    # 设置参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_dir_path', type=str, default='/home/data/vehicle_data/images/',
                        help='img所在文件目录路径')
    parser.add_argument('--xml_txt_path', type=str, default='/home/data/vehicle_data/all_det_xmls.txt', help='xml所在文件目录路径')
    parser.add_argument('--txt_dir_path', type=str, default=r'/home/data/vehicle_data/labels/',
                        help='需要保存txt文件目录路径')
    opt = parser.parse_args()
    
    
    gen_imgs_path()
    
    
    
    
    with open('/home/data/vehicle_data/all_det_imgs.txt', 'r') as f1:
        for xml in f1.readlines():
            image_name = xml.strip().split(os.sep)[-1].split('.')[0]
            convert_annotation(image_name, xml_path=xml.strip().replace('.jpg', '.xml'), txt_dir_path=opt.txt_dir_path)
