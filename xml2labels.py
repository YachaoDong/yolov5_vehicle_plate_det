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

# box: [0,6], line:[6], key_point:[7, 14]
classes = ['front_head', 'side_head', 'back_head', 'hand', 'smoke_part_box', 'smoke',
             'smoke_part_line',
             'left_eye', 'right_eye', 'left_ear', 'right_ear', 'left_mouth', 'right_mouth',  'nose']

abs_path = os.getcwd()


def convert(size, box):
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


def convert_annotation(image_id, xml_dir_path='/project/train/src_repo/dataset/xmls/',
                       txt_dir_path='/project/train/src_repo/dataset/labels/'):
    in_file = open(xml_dir_path + image_id + '.xml')
    out_file = open(txt_dir_path + image_id + '.txt', 'w')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
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
        bb = convert((w, h), b)
        # 写入bbox
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]))

        # 获取point，处理point 有visibility字段
        if obj.find('point'):
            for xmlpoint in obj.iter('point'):
                point_cls = xmlpoint.find('name').text
                point_cls_id = classes.index(point_cls)
                point_vis = int(xmlpoint.find('visibility').text)
                point_x = float(xmlpoint.find('x').text) / w
                point_y = float(xmlpoint.find('y').text) / h
                # 写入point
                out_file.write(" " + str(point_cls_id) + " " + str(point_vis) +
                               " " + str(point_x) + " " + str(point_y))

        # 获取line， 处理line
        if obj.find('polyline'):
            # print('xml_dir_path: ', image_id)
            for polyline in obj.iter('polyline'):
                polyline_name = polyline.find('name').text
                polyline_id = classes.index(polyline_name)
                polyline_xstart = float(polyline.find('xstart').text) / w
                polyline_ystart = float(polyline.find('ystart').text) / h
                polyline_xend = float(polyline.find('xend').text) / w
                polyline_yend = float(polyline.find('yend').text) / h
                # 写入polyline
                out_file.write(" " + str(polyline_id) +
                               " " + str(polyline_xstart) + " " + str(polyline_ystart) +
                               " " + str(polyline_xend) + " " + str(polyline_yend))


        out_file.write('\n')


if __name__ == '__main__':

    # 设置参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_dir_path', type=str, default='/home/data/smoke_data/images/',
                        help='img所在文件目录路径')
    parser.add_argument('--xml_dir_path', type=str, default='/home/data/smoke_data/xmls/', help='xml所在文件目录路径')
    parser.add_argument('--txt_dir_path', type=str, default=r'/home/data/smoke_data/labels/',
                        help='需要保存txt文件目录路径')
    opt = parser.parse_args()

    for image_path in glob.glob(opt.img_dir_path + "*.jpg"):  # 每一张图片都对应一个xml文件这里写xml对应的图片的路径
        image_name = image_path.split(os.sep)[-1].split('.')[0]
        convert_annotation(image_name, xml_dir_path=opt.xml_dir_path, txt_dir_path=opt.txt_dir_path)
